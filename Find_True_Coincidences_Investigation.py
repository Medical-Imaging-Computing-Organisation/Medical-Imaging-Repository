# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:44:17 2024

@author: alfie
"""

# Imports
import numpy as np
from numba import njit
from numba import prange
import pandas as pd
from pathlib import Path
from timeit import default_timer as timer
import matplotlib.pyplot as plt
#import os


def find_true_coincidences(tau, epsilon, E0, arrA, arrB, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference):
    '''
    @author = Alfie
    @coauthor = Chris

    For events observed in between two and eight detectors, this function finds
    which events occurred within a given time coincidence window of each other
    AND could correspond to a single Compton scatter followed by a
    photoelectric absorption using energy conservation rules.

    NOTE: support for >2 detectors is not currently supported, for now just
    call this function for each detector pair as required.

    Required Imports
    ----------
    import numpy as np
    from numba import njit
    from numba import prange

    Parameters
    ----------
    tau : float
        Chosen time coincidence window. Must be given in the same units as the
        timestamps of the events in the input arrays.
    epsilon: float
        Chosen energy coincidence window. Must be given in the same units as
        the energies of the events in the input arrays.
    E0 : float
        Initial photon energy (=662 keV in most cases). Must be given in the
        same units as the energies of the events in the input arrays
    arrA : array
        Array of events which were observed in the first detector.
    arrB : array
        Array of events which were observed in the second detector.

    Returns
    -------
    output: array
        Array of data for each pair of events identified as being coincident.
        Format:
            [[E1, E2, delta_E1, delta_E2, scat_index, abs_index],
             [E1, E2, delta_E1, delta_E2, scat_index, abs_index],
             ...]
            where E1 is the scatter energy; E2 is the absorption energy;
            delta_E1, delta_E2 are the uncertainties on E1, E2; and scat_index,
            abs_index are the indices of the detectors where the scatter and
            absorption occurred.

    '''

    # determine the region in arrB to examine for coincidences
    search_window_size = 1000
    test_window_size = 10

    # version just for testing!
    temp_arr = np.ndarray((arrA.shape[0], test_window_size, 8), dtype=np.float32)    
    
    package = np.empty((arrA.shape[0], test_window_size, 8), dtype=np.float32)
    column0 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column1 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column2 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column3 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column4 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column5 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column6 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column7 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)    
    
    #TODO: decomment njit if you're using a large dataset
    #@njit(parallel=True)
    def two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, package, column0, column1, column2, column3, column4, column5, column6, column7):
        '''
        @author = Alfie
        @coauthor = Chris

        Takes events observed in two detectors (A and B) and finds pairs which
        could correspond to a Compton scatter followed by a photoelectric
        absorption.

        NOTE: for small datasets, keep the @njit line above commented out as
        you'll be faster without it.

        Required Imports
        ----------
        import numpy as np
        from numba import njit
        from numba import prange

        Parameters
        ----------
        tau : float
            time coincidence window.
        epsilon: float
            energy coincidence window.
        E0 : float
            initial photon energy.
        arrA : array
            array of events observed in detector A.
        arrB : array
            array of events observed in detector B.
        temp_arr : array
            empty array of shape (arrA.shape[0], test_window_size, 4) with dtype=np.float32
        ave_tstepA : float
            average increase in time between each index in arrA.
        ave_tstepB : float
            average increase in time between each index in arrB.
        package: array
            package = np.empty((arrA.shape[0], test_window_size, 6))
            Needs to be defined outside this function to keep Numba happy.
        column0, column1, ..., column5: arrays
            columnX = np.empty((arrA.shape[0], test_window_size))
            These will all form the columns of the package array.

        Returns
        -------
        temp_arr : array
            Array of valid coincident scatter-absorption event pairs. Format:

                [[E1, E2, delta_E1, delta_E2, scatIndex, absIndex],
                 [E1, E2, delta_E1, delta_E2, scatIndex, absIndex],
                 ...]

            where E1 is the energy of the scattering event; E2 is the energy
            of the absorption event; and delta_E1, delta_E2 are uncertainties
            on those values.

            NOTE - temp_arr will contain many rows filled with zeros! These
            are to be removed outside of this function before any further
            operations are performed.

        '''
        

        # extract time information from arrA and arrB
        tA = arrA[:, 2]
        #tB = arrB[:, 2]
        delta_tA = arrA[:, 4]
        #delta_tB = arrB[:, 4]

        # calculate limits of time coincidence window for each event in arrA
        t_max = tA + tau + delta_tA
        t_min = tA - tau - delta_tA

        # extract energy information from arrA
        EA = arrA[:, 1]
        #EB = arrB[:, 1]
        delta_EA = arrA[:, 3]
        #delta_EB = arrB[:, 3]
        
        for i in range(0, arrA.shape[0]):
        # iterate over every event in arrA. For the i^th event:          

            # generate initial guess of j from linear fit
            initial_j = int((tA[i]-arrB_coeffs[1])/arrB_coeffs[0])

            # use initial j guess to inform search window size
            search_max = int(min(arrB[:,2].shape[0]-1, initial_j+search_window_size))
            search_min = int(max(0, initial_j-search_window_size))
            search_window = arrB[int(search_min) : int(search_max)]
            
            # find the index j in arrB where timestamp best matches tA[i]
            j = search_min + np.argmin((tA[i] - search_window[:,2])**2 )

            # calculate limits of the testing window for the i^th event in arrA
            test_min = int(min(arrB[:,2].shape[0]-1-test_window_size, max(0, min(j - 1.5 * test_window_size, arrB.shape[0]))))
            test_max = int(min(arrB[:,2].shape[0]-1, max(test_min+test_window_size, min(j + test_window_size, arrB.shape[0]))))
            test_window = arrB[int(test_min) : int(test_max)]

            # check which elements in test_window are between limits of tau
            time_test = np.where( (t_min[i] <= test_window[:,2] - test_window[:,4]) & (t_max[i] >= test_window[:,2] + test_window[:,4]) )[0]
            coinc_events = test_window[time_test]
            
            # alternative time test
            #coinc_events = test_window[(t_min[i] <= test_window[:,2] - delta_tB[j]) & (t_max[i] >= test_window[:,2] + delta_tB[j])]
            
            # extract energy information from events which passed time test
            EB = coinc_events[:,1]
            #print(EB)
            delta_EB = coinc_events[:,3]
            
            # apply energy conservation test to events which passed time test
            energy_test = np.where( (EA[i] + delta_EA[i] + EB + delta_EB >= E0 - epsilon) & (E0 + epsilon >= EA[i] - delta_EA[i] + EB - delta_EB) )[0]
            valid_events = coinc_events[energy_test]

            # alternative energy test
            #valid_events = coinc_events[(EA[i] + delta_EA[i] + EB + delta_EB >= E0 - epsilon) & (E0 + epsilon >= EA[i] - delta_EA[i] + EB - delta_EB)]

            # group valid events by time occurred relative to event i in arrA
            events_before = valid_events[np.where(valid_events[:, 2] < tA[i])]
            events_after = valid_events[np.where(valid_events[:, 2] >= tA[i])]

            # construct data columns to be added to the output array

            # energy of scatter event
            column0[i][:events_before.shape[0]] = events_before[:, 1]
            column0[i][events_before.shape[0]:valid_events.shape[0]] = arrA[i, 1]
            column0[i][valid_events.shape[0]:] = 0

            # energy of absorption event
            column1[i][:events_before.shape[0]] = arrA[i, 1]
            column1[i][events_before.shape[0]:valid_events.shape[0]] = events_after[:, 1]
            column1[i][valid_events.shape[0]:] = 0

            # uncertainty on energy of scatter event
            column2[i][:events_before.shape[0]] = events_before[:, 3]
            column2[i][events_before.shape[0]:valid_events.shape[0]] = arrA[i, 3]
            column2[i][valid_events.shape[0]:] = 0

            # uncertainty on energy of absorption event
            column3[i][:events_before.shape[0]] = arrA[i, 3]
            column3[i][events_before.shape[0]:valid_events.shape[0]] = events_after[:, 3]
            column3[i][valid_events.shape[0]:] = 0

            # index of detector where scatter event occurred
            column4[i][:events_before.shape[0]] = events_before[:, 0]
            column4[i][events_before.shape[0]:valid_events.shape[0]] = arrA[i, 0]
            column4[i][valid_events.shape[0]:] = 0

            # index of detector where absorption event occurred
            column5[i][:events_before.shape[0]] = arrA[i, 0]
            column5[i][events_before.shape[0]:valid_events.shape[0]] = events_after[:, 0]
            column5[i][valid_events.shape[0]:] = 0
            
            # JUST FOR TESTING - timestamp of scatter event
            column6[i][:events_before.shape[0]] = events_before[:, 2]
            column6[i][events_before.shape[0]:valid_events.shape[0]] = arrA[i, 2]
            column6[i][valid_events.shape[0]:] = 0      
            
            # JUST FOR TESTING - timestamp of absorption event
            column7[i][:events_before.shape[0]] = arrA[i, 2]
            column7[i][events_before.shape[0]:valid_events.shape[0]] = events_after[:, 2]
            column7[i][valid_events.shape[0]:] = 0            

            # package up the columns
            package[i, :, 0] = column0[i]
            package[i, :, 1] = column1[i]
            package[i, :, 2] = column2[i]
            package[i, :, 3] = column3[i]
            package[i, :, 4] = column4[i]
            package[i, :, 5] = column5[i]
            package[i, :, 6] = column6[i]
            package[i, :, 7] = column7[i]

            # delete rows where photon was absorbed in its first interaction
            # this is unnecessary since lab have already removed photopeak (and it tends to make things go wrong)
            #noscat = np.where((column0[i] != 0) & (column1[i] - column3[i] < epsilon))[0]
            #print(noscat)
            #package[i][noscat] = np.zeros(6)

            temp_arr[i] = package[i]

        return temp_arr

    output = two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, package, column0, column1, column2, column3, column4, column5, column6, column7)
    # get rid of the zeros
    output = output[~np.all(output[:, :, :4] == 0, axis=2)]

    return output

def CSV_Extract(Delimiter, Folder_Path, File1_Name, File2_Name=None, File3_Name=None, Header=None):
    '''
    
    @author = Chris
    
    Takes 1-3 CSV file locations in pre-specified format and extracts their data to Numpy Arrays
    
            Parameters:
                    Delimiter (string): Delimiter for column separation within the CSV(s)
                    Folder_Path (string): The local directory path where the CSV(s) are stored
                    File1_Name (string): The file name of the Energy-Time CSV to have data extracted
                    
                    
            Optional Parameters:
                    File2_Name (string): The file name of the Detector Location CSV to have data extracted
                    File3_Name (string): The file name of the Detector Pairing CSV to have data extracted                                    
                    Header: Optional specification for when CSVs contain a header row, default is None
            
            
            Required CSV Formats:
                    Energy-Time CSV: | Detector Index (int) | Energy (float32) | Time (float32) | Delta Energy (float32) | Delta Time (float32) |
                    
                    
            Optional CSV Formats:         
                    Detector Location CSV: | Detector Index (int) | x (float32) | y (float32) | z (float32) | Delta x (float32) | Delta y (float32) | Delta z (float32) | Sc/Ab (str) |
                    Detector Pairing CSV: | Scatterer Index (int) | Absorber Index (int) | Ballpark Angular Uncertainty (float32) |
                    
                    
            Returns:
                    arr1 (Numpy Array): Numpy Array with the data from Energy-Time CSV
                
                        arr1: [[Detector Index, Energy, Time, Delta Energy, Delta Time], ...]
                       
                       
            Optional Returns:
                    arr2, arr3 (Numpy Arrays): Numpy Arrays with the data from Detector Location and Detector Pairing CSVs respectively
                        
                        arr2: [[Detector Index, x, y, z, Delta x, Delta y, Delta z, Sc/Ab], ...]
                        arr3: [[Scatterer Index, Absorber Index, Ballpark Angular Uncertainty], ...]
                    
    '''
    # Imports, for when this function is being externally called
    #import numpy as np
    #import pandas as pd
    #from pathlib import Path
    
    # Forming full location path for first (Energy-Time) CSV
    BaseLocation = str(Path(Folder_Path))
    CSV1Location = BaseLocation + "\\" + File1_Name
    
    # Forming full location paths for optional second and third (Detector Position and Detector Pairing) CSVs
    if File2_Name != None:
        CSV2Location = BaseLocation + "\\" + File2_Name
        
        if File3_Name != None:
            CSV3Location = BaseLocation + "\\" + File3_Name
    
    
    # Internal processing function for reading CSVs via Pandas
    def Read_CSV(Location, columns, Header, datatype):
        df = pd.read_csv(Location, sep=Delimiter, usecols=columns, header=Header, dtype=datatype)
        return df
        
    # Concurrent branch - functioning
    
        
    # Read Energy-Time CSV and populate numpy array with its data
    df1 = Read_CSV(CSV1Location, [0,1,2,3,4], Header, np.float32)
    arr1 = df1.values
        
    # Conditional for Detector Location CSV
    if File2_Name != None:
            
        # Read Detector Location CSV, accounting for floats/strings, and populate numpy array with its data
        df2_1 = Read_CSV(CSV2Location, [0,1,2,3,4,5,6], Header, np.float32)
        arr2 = df2_1.values
          
            
        # Conditional for Detector Pairing CSV
        if File3_Name != None:
                
            # Read Detector Pairing CSV and populate numpy array with its data
            df3 = Read_CSV(CSV3Location, [0,1,2], Header, np.float32)
            arr3 = df3.values
                
            # Returning all 3 arrays when applicable
            return arr1, arr2, arr3
            
        else:
            # Returning first 2 (Energy-Time and Detector Location) arrays when applicable
            return arr1, arr2
            
    else:
        # Returning first (Energy-Time) array when applicable
        return arr1


def detector_polynomial_time_fit(arr):
    
    
    
    # Extract the time column from the detector array
    det_time_arr = arr[:,2]
    
    # # calculate the difference in times
    # time = det_time_arr[1:] - det_time_arr[:-1]
    
    # calculate index values
    index_values = np.arange(0, arr[:,2].shape[0], 1)
    
    
    # # mean of data
    # mean = np.mean(time)
    
    # # standard deviation of data
    # std_dev = np.std(time)
    
    # # package return values
    # return_arr[0] = mean+std_dev
    # return_arr[1] = mean
    # return_arr[2] = std_dev
    
    
    # calculate linear time fit of detector array
    coeffs = np.polyfit(index_values, det_time_arr, 1)
    
    # calculate difference between fit timestamp and actual timestamp
    difference = arr[:,2] - (coeffs[0]*index_values + coeffs[1])
    
    
    return coeffs, difference


if __name__ == "__main__":
    accuracies = np.zeros(1)
    purities = np.zeros(1)
    counts = np.zeros(1)
    good_counts = np.zeros(1)
    #TODO: edit points to select a range of epsilon values for testing
    points = np.linspace(0, 0.06)
    counter = 0
    for test_eps in points:
        start = timer()
        counter = counter + 1
        print(f"Started loop {counter} / 50")
    
        # Monte Carlo final small dataset exact good
        #TODO: edit the folder path to point to the list of good events
        data_label = 'Monte Carlo final small short-run exact good'
        Folder_Path = 'C:/Users/alfie/Documents/Full Small data set/Good Events/Exact Good'
        ETFile0 = 'CSV1_Exact_G_D1 (7).csv'
        ETFile1 = 'CSV1_Exact_G_D2.csv'
        ETFile2 = 'CSV1_Exact_G_D3.csv'
        ETFile3 = 'CSV1_Exact_G_D4.csv'
        ETFile4 = 'CSV1_Exact_G_D5.csv'
        ETFile5 = 'CSV1_Exact_G_D6.csv'
        ETFile6 = 'CSV1_Exact_G_D7.csv'
        ETFile7 = 'CSV1_Exact_G_D8.csv'
        Delimiter = ','
        tau = 0
        epsilon = 0.1
        E0 = 0.662
    
        CSV_Start = timer()
        arr0 = CSV_Extract(Delimiter, Folder_Path, ETFile0)
        arr1 = CSV_Extract(Delimiter, Folder_Path, ETFile1)
        arr2 = CSV_Extract(Delimiter, Folder_Path, ETFile2)
        arr3 = CSV_Extract(Delimiter, Folder_Path, ETFile3)
        arr4 = CSV_Extract(Delimiter, Folder_Path, ETFile4)
        arr5 = CSV_Extract(Delimiter, Folder_Path, ETFile5)
        arr6 = CSV_Extract(Delimiter, Folder_Path, ETFile6)
        arr7 = CSV_Extract(Delimiter, Folder_Path, ETFile7)
    
        good_out = np.zeros(8)
        
        arrays = (arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7)
        
        for x in range(8):
            for y in range(x, 8):
                if x == y:
                    pass
                else:
                    arrA_coeffs, arrA_difference = detector_polynomial_time_fit(arrays[x])
                    arrB_coeffs, arrB_difference = detector_polynomial_time_fit(arrays[y])
                    good_out = np.vstack((good_out, find_true_coincidences(tau, epsilon, E0, arrays[x], arrays[y], arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference)))
        
        good_out = good_out[1:]
        
        # Monte Carlo final small dataset smeared
        #TODO: edit the folder path to point to the dataset you want to investigate
        data_label = 'Monte Carlo final short-run smeared'
        Folder_Path = 'C:/Users/alfie/Documents/Full Small data set/Full Data Set/Smeared'
        ETFile0 = 'CSV1_Full_Smeared_D1 (2).csv'
        ETFile1 = 'CSV1_Full_Smeared_D2 (2).csv'
        ETFile2 = 'CSV1_Full_Smeared_D3 (2).csv'
        ETFile3 = 'CSV1_Full_Smeared_D4 (2).csv'
        ETFile4 = 'CSV1_Full_Smeared_D5.csv'
        ETFile5 = 'CSV1_Full_Smeared_D6.csv'
        ETFile6 = 'CSV1_Full_Smeared_D7.csv'
        ETFile7 = 'CSV1_Full_Smeared_D8.csv'
        Delimiter = ','
        tau = 0
        epsilon = test_eps
        E0 = 0.662
        
        print('Starting full smeared data')
        
        CSV_Start = timer()
        arr0 = CSV_Extract(Delimiter, Folder_Path, ETFile0)
        arr1 = CSV_Extract(Delimiter, Folder_Path, ETFile1)
        arr2 = CSV_Extract(Delimiter, Folder_Path, ETFile2)
        arr3 = CSV_Extract(Delimiter, Folder_Path, ETFile3)
        arr4 = CSV_Extract(Delimiter, Folder_Path, ETFile4)
        arr5 = CSV_Extract(Delimiter, Folder_Path, ETFile5)
        arr6 = CSV_Extract(Delimiter, Folder_Path, ETFile6)
        arr7 = CSV_Extract(Delimiter, Folder_Path, ETFile7)
    
        total_out = np.zeros(8)
        
        arrays = (arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7)
        
        for x in range(8):
            for y in range(x, 8):
                if x == y:
                    pass
                else:
                    print(x, y)
                    arrA_coeffs, arrA_difference = detector_polynomial_time_fit(arrays[x])
                    arrB_coeffs, arrB_difference = detector_polynomial_time_fit(arrays[y])
                    total_out = np.vstack((total_out, find_true_coincidences(tau, epsilon, E0, arrays[x], arrays[y], arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference)))
        
        total_out = total_out[1:]
        
        print(f'In total, {total_out.shape[0]} coincidences were identified in the {data_label} data with epsilon = {epsilon} and tau = {tau}.')
        
        good_times = good_out[:, 6:]
        
        accuracy_score = 0
        
        for z in range(total_out.shape[0]):
            if total_out[z, 6] in good_times and total_out[z, 7] in good_times:
                accuracy_score = accuracy_score + 1
        print(f'{accuracy_score} of those coincidences were correctly identified.')
        accuracy = accuracy_score / good_out.shape[0]
        purity = accuracy_score / total_out.shape[0]
        print(f'Accuracy of output = {accuracy}')
        print(f'Purity of output = {purity}')
        accuracies = np.vstack((accuracies, accuracy))
        purities = np.vstack((purities, purity))
        counts = np.vstack((counts, total_out.shape[0]))
        good_counts = np.vstack((good_counts, accuracy_score))
        
    accuracies = accuracies[1:]
    purities = purities[1:]
    counts = counts[1:]
    good_counts = good_counts[1:]
    
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(points, accuracies, 'orange', label='Accuracy of output')
    axs[0].plot(points, purities, 'skyblue', label='Purity of output')
    axs[1].plot(points, counts, 'red', label='Number of coincidences identified')
    axs[1].plot(points, good_counts, 'green', label='Number of true positives')
    axs[0].set_xlabel('Value of Epsilon (Mev)')
    axs[1].set_xlabel('Value of Epsilon (MeV)')
    axs[0].set_ylabel('Accuracy/Purity')
    axs[1].set_ylabel('Number of IDs')
    plt.suptitle('Effect of varying epsilon on find_true_coincidences output for Monte Carlo smeared data (07/03/24)')
    axs[0].legend()
    axs[1].legend()
    plt.show()