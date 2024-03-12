# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:05:16 2024

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

    # # define an array to contain the coincident events
    temp_arr = np.ndarray((arrA.shape[0], test_window_size, 6), dtype=np.float32)

    # # define for use later (I had to change dtype to float32 so that my laptop could cope with the memory allocation)
    package = np.empty((arrA.shape[0], test_window_size, 6), dtype=np.float32)
    column0 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column1 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column2 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column3 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column4 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column5 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)

    @njit(parallel=True)
    def two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, package, column0, column1, column2, column3, column4, column5):
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
        # tB = arrB[:, 2]
        delta_tA = arrA[:, 4]
        delta_tB = arrB[:, 4]

        # calculate limits of time coincidence window for each event in arrA
        t_max = tA + tau + delta_tA
        t_min = tA - tau - delta_tA

        # extract energy information from arrA
        EA = arrA[:, 1]
        #EB = arrB[:, 1]
        delta_EA = arrA[:, 3]
        #delta_EB = arrB[:, 3]
        

        print('Starting Loop')
        for i in prange(0, arrA.shape[0]):
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
            '''
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
            '''
            
            # version of the above without event swapping
            # just assume all events in arrA are scatters, all in arrB are absorbs
            
            # energy of scatter event
            column0[i][:valid_events.shape[0]] = arrA[i, 1]
            column0[i][valid_events.shape[0]:] = 0
            
            # energy of absorb event
            column1[i][:valid_events.shape[0]] = valid_events[:, 1]
            column1[i][valid_events.shape[0]:] = 0
            
            # uncertainty on energy scatter event
            column2[i][:valid_events.shape[0]] = arrA[i, 3]
            column2[i][valid_events.shape[0]:] = 0
            
            # uncertainty on energy of absorb event
            column3[i][:valid_events.shape[0]] = valid_events[:, 3]
            column3[i][valid_events.shape[0]:] = 0
            
            # index of scattering detector
            column4[i][:valid_events.shape[0]] = arrA[i, 0]
            column4[i][valid_events.shape[0]:] = 0
            
            # index of absorbing detector
            column5[i][:valid_events.shape[0]] = valid_events[:, 0]
            column5[i][valid_events.shape[0]:] = 0            
            
            # package up the columns
            package[i, :, 0] = column0[i]
            package[i, :, 1] = column1[i]
            package[i, :, 2] = column2[i]
            package[i, :, 3] = column3[i]
            package[i, :, 4] = column4[i]
            package[i, :, 5] = column5[i]

            # delete rows where photon was absorbed in its first interaction
            # this is unnecessary since lab have already removed photopeak (and it tends to make things go wrong)
            #noscat = np.where((column0[i] != 0) & (column1[i] - column3[i] < epsilon))[0]
            #print(noscat)
            #package[i][noscat] = np.zeros(6)

            temp_arr[i] = package[i]

        return temp_arr

    output = two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, package, column0, column1, column2, column3, column4, column5)
    # get rid of the zeros
    output = output[~np.all(output[:, :, :4] == 0, axis=2)]

    print(f'The array with {arrA.shape[0]} events was compared to the array with {arrB.shape[0]} events.')
    print(f'The script found {output.shape[0]} event pairs which it thinks are good.')
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
    start = timer()
    print("Started!")
    
    # Lab data 08 Feb setup 3
    Delimiter = ';'
    Header = 0
    Folder_Path = 'C:/Users/alfie/Documents/DBP_V1.0/08Feb Setup 3-20240213T170159Z-001/08Feb Setup 3'
    ETFile0 = 'CH0 Feb08 Setup 3 A.csv'
    ETFile1 = 'CH1 Feb08 Setup 3 A.csv'
    ETFile2 = 'CH2 Feb08 Setup 3 A.csv'
    ETFile3 = 'CH3 Feb08 Setup 3 A.csv'
    Det_Pos = 'CSV 2.csv'
    tau = 0
    epsilon = 0
    E0 = 0.662
    data_label = 'Lab 08 Feb setup 3'
    
    '''
    # Monte Carlo smeared data
    data_label = 'Monte Carlo smeared'
    Folder_Path = 'C:/Users/alfie/Documents/4 Detector setup (Times updated)/Smeared Full Events_ Detector Separated'
    ETFile0 = 'CSV1_Full_Smeared_D1 (2).csv'
    ETFile1 = 'CSV1_Full_Smeared_D2 (2).csv'
    ETFile2 = 'CSV1_Full_Smeared_D3 (2).csv'
    ETFile3 = 'CSV1_Full_Smeared_D4 (2).csv'
    Delimiter = ','
    tau = 0
    epsilon = 0.01
    E0 = 0.662
    '''
    '''
    # Monte Carlo exact data
    data_label = 'Monte Carlo exact'
    Folder_Path = 'C:/Users/alfie/Documents/4 Detector setup (Times updated)/Exact Full Events_ Detector Separated'
    ETFile0 = 'CSV1_Full_Exact_D1 (2).csv'
    ETFile1 = 'CSV1_Full_Exact_D2 (2).csv'
    ETFile2 = 'CSV1_Full_Exact_D3 (2).csv'
    ETFile3 = 'CSV1_Full_Exact_D4 (2).csv'
    Delimiter = ','
    tau = 0
    epsilon = 0.1
    E0 = 0.662
    '''
    '''
    # Monte Carlo exact coincident data
    data_label = 'Monte Carlo exact coincident'
    Folder_Path = 'C:/Users/alfie/Documents/4 Detector setup (Times updated)/Exact coincident'
    ETFile0 = 'CSV1_Exact_C_D1 (1).csv'
    ETFile1 = 'CSV1_Exact_C_D2 (1).csv'
    ETFile2 = 'CSV1_Exact_C_D3 (1).csv'
    ETFile3 = 'CSV1_Exact_C_D4 (1).csv'
    Delimiter = ','
    tau = 0
    epsilon = 0.1
    E0 = 0.662
    '''
    '''
    # Monte Carlo final small dataset smeared
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
    epsilon = 1
    E0 = 0.662
    '''
    '''
    # Monte Carlo final small dataset exact
    data_label = 'Monte Carlo final short-run exact'
    Folder_Path = 'C:/Users/alfie/Documents/Full Small data set/Full Data Set/Exact'
    ETFile0 = 'CSV1_Full_Exact_D1 (2).csv'
    ETFile1 = 'CSV1_Full_Exact_D2 (2).csv'
    ETFile2 = 'CSV1_Full_Exact_D3 (2).csv'
    ETFile3 = 'CSV1_Full_Exact_D4 (2).csv'
    ETFile4 = 'CSV1_Full_Exact_D5.csv'
    ETFile5 = 'CSV1_Full_Exact_D6.csv'
    ETFile6 = 'CSV1_Full_Exact_D7.csv'
    ETFile7 = 'CSV1_Full_Exact_D8.csv'
    Delimiter = ','
    tau = 0
    epsilon = 0.000344
    E0 = 0.662
    '''
    '''
    # Monte Carlo final small dataset exact coincident
    data_label = 'Monte Carlo final small short-run exact coincident'
    Folder_Path = 'C:/Users/alfie/Documents/Full Small data set/Coincident Events/Exact Coincident'
    ETFile0 = 'CSV1_Exact_C_D1.csv'
    ETFile1 = 'CSV1_Exact_C_D2.csv'
    ETFile2 = 'CSV1_Exact_C_D3.csv'
    ETFile3 = 'CSV1_Exact_C_D4.csv'
    Delimiter = ','
    tau = 0
    epsilon = 0
    E0 = 0.662
    '''
    '''
    # Monte Carlo final small dataset smeared good
    data_label = 'Monte Carlo final small short-run smeared good'
    Folder_Path = 'C:/Users/alfie/Documents/Full Small data set/Good Events/Smeared Good'
    ETFile0 = 'CSV1_Smeared_G_D1 (6).csv'
    ETFile1 = 'CSV1_Smeared_G_D2.csv'
    ETFile2 = 'CSV1_Smeared_G_D3.csv'
    ETFile3 = 'CSV1_Smeared_G_D4.csv'
    ETFile4 = 'CSV1_Smeared_G_D5.csv'
    ETFile5 = 'CSV1_Smeared_G_D6.csv'
    ETFile6 = 'CSV1_Smeared_G_D7.csv'
    ETFile7 = 'CSV1_Smeared_G_D8.csv'
    Delimiter = ','
    tau = 0
    epsilon = 1
    E0 = 0.662
    '''
    '''
    # Monte Carlo final small dataset exact good
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
    '''

    CSV_Start = timer()
    arr0 = CSV_Extract(Delimiter, Folder_Path, ETFile0)[:100000]
    arr1 = CSV_Extract(Delimiter, Folder_Path, ETFile1)[:100000]
    arr2 = CSV_Extract(Delimiter, Folder_Path, ETFile2)[:100000]
    arr3 = CSV_Extract(Delimiter, Folder_Path, ETFile3)[:100000]
    # arr4 = CSV_Extract(Delimiter, Folder_Path, ETFile4)
    # arr5 = CSV_Extract(Delimiter, Folder_Path, ETFile5)
    # arr6 = CSV_Extract(Delimiter, Folder_Path, ETFile6)
    # arr7 = CSV_Extract(Delimiter, Folder_Path, ETFile7)

    print("CSV Extraction Done in {} s".format(timer() - CSV_Start))
    print(f'arr0 contains {arr0.shape[0]} events.')
    print(f'arr1 contains {arr1.shape[0]} events.')
    print(f'arr2 contains {arr2.shape[0]} events.')
    print(f'arr3 contains {arr3.shape[0]} events.')
    # print(f'arr4 contains {arr4.shape[0]} events.')
    # print(f'arr5 contains {arr5.shape[0]} events.')
    # print(f'arr6 contains {arr6.shape[0]} events.')
    # print(f'arr7 contains {arr7.shape[0]} events.')
    '''
    # Generate linear time fits for each detector
    arr0_coeffs, arr0_difference = detector_polynomial_time_fit(arr0)
    arr1_coeffs, arr1_difference = detector_polynomial_time_fit(arr1)
    arr2_coeffs, arr2_difference = detector_polynomial_time_fit(arr2)
    arr3_coeffs, arr3_difference = detector_polynomial_time_fit(arr3)
    arr4_coeffs, arr4_difference = detector_polynomial_time_fit(arr4)
    arr5_coeffs, arr5_difference = detector_polynomial_time_fit(arr5)
    arr6_coeffs, arr6_difference = detector_polynomial_time_fit(arr6)
    arr7_coeffs, arr7_difference = detector_polynomial_time_fit(arr7)
    '''
    total_out = np.zeros(6)
    '''
    # 4 detector setup
    print('01')
    out01 = find_true_coincidences(tau, epsilon, E0, arr0, arr1, arr0_coeffs, arr1_coeffs, arr0_difference, arr1_difference)
    total_out = np.vstack((total_out, out01))
    #print(out01)
    print('02')
    out02 = find_true_coincidences(tau, epsilon, E0, arr0, arr2, arr0_coeffs, arr2_coeffs, arr0_difference, arr2_difference)
    total_out = np.vstack((total_out, out02))
    #print(out02)
    print('03')
    out03 = find_true_coincidences(tau, epsilon, E0, arr0, arr3, arr0_coeffs, arr3_coeffs, arr0_difference, arr3_difference)
    total_out = np.vstack((total_out, out03))    
    #print(out03)
    print('12')
    out12 = find_true_coincidences(tau, epsilon, E0, arr1, arr2, arr1_coeffs, arr2_coeffs, arr1_difference, arr2_difference)
    total_out = np.vstack((total_out, out12))
    #print(out12)
    print('13')
    out13 = find_true_coincidences(tau, epsilon, E0, arr1, arr3, arr1_coeffs, arr3_coeffs, arr1_difference, arr3_difference)
    total_out = np.vstack((total_out, out13))
    #print(out13)
    print('23')
    out23 = find_true_coincidences(tau, epsilon, E0, arr2, arr3, arr2_coeffs, arr3_coeffs, arr2_difference, arr3_difference)
    total_out = np.vstack((total_out, out23))
    #print(out23)
    '''
    '''
    # 8 detector setup (only scat/abs pairs)
    print('04')
    out01 = find_true_coincidences(tau, epsilon, E0, arr0, arr4, arr0_coeffs, arr4_coeffs, arr0_difference, arr4_difference)
    total_out = np.vstack((total_out, out01))
    #print(out01)
    print('05')
    out02 = find_true_coincidences(tau, epsilon, E0, arr0, arr5, arr0_coeffs, arr5_coeffs, arr0_difference, arr5_difference)
    total_out = np.vstack((total_out, out02))
    #print(out02)
    print('06')
    out03 = find_true_coincidences(tau, epsilon, E0, arr0, arr6, arr0_coeffs, arr6_coeffs, arr0_difference, arr6_difference)
    total_out = np.vstack((total_out, out03))    
    #print(out03)
    print('07')
    out12 = find_true_coincidences(tau, epsilon, E0, arr0, arr7, arr0_coeffs, arr7_coeffs, arr0_difference, arr7_difference)
    total_out = np.vstack((total_out, out12))
    #print(out12)
    print('14')
    out13 = find_true_coincidences(tau, epsilon, E0, arr1, arr4, arr1_coeffs, arr4_coeffs, arr1_difference, arr4_difference)
    total_out = np.vstack((total_out, out13))
    #print(out13)
    print('15')
    out23 = find_true_coincidences(tau, epsilon, E0, arr1, arr5, arr1_coeffs, arr5_coeffs, arr1_difference, arr5_difference)
    total_out = np.vstack((total_out, out23))
    #print(out23)    
    print('16')
    out01 = find_true_coincidences(tau, epsilon, E0, arr1, arr6, arr1_coeffs, arr6_coeffs, arr1_difference, arr6_difference)
    total_out = np.vstack((total_out, out01))
    #print(out01)
    print('17')
    out02 = find_true_coincidences(tau, epsilon, E0, arr1, arr7, arr1_coeffs, arr7_coeffs, arr1_difference, arr7_difference)
    total_out = np.vstack((total_out, out02))
    #print(out02)
    print('24')
    out03 = find_true_coincidences(tau, epsilon, E0, arr2, arr4, arr2_coeffs, arr4_coeffs, arr2_difference, arr4_difference)
    total_out = np.vstack((total_out, out03))    
    #print(out03)
    print('25')
    out12 = find_true_coincidences(tau, epsilon, E0, arr2, arr5, arr2_coeffs, arr5_coeffs, arr2_difference, arr5_difference)
    total_out = np.vstack((total_out, out12))
    #print(out12)
    print('26')
    out13 = find_true_coincidences(tau, epsilon, E0, arr2, arr6, arr2_coeffs, arr6_coeffs, arr2_difference, arr6_difference)
    total_out = np.vstack((total_out, out13))
    #print(out13)
    print('27')
    out23 = find_true_coincidences(tau, epsilon, E0, arr2, arr7, arr2_coeffs, arr7_coeffs, arr2_difference, arr7_difference)
    total_out = np.vstack((total_out, out23))
    #print(out23) 
    print('34')
    out01 = find_true_coincidences(tau, epsilon, E0, arr3, arr4, arr3_coeffs, arr4_coeffs, arr3_difference, arr4_difference)
    total_out = np.vstack((total_out, out01))
    #print(out01)
    print('35')
    out02 = find_true_coincidences(tau, epsilon, E0, arr3, arr5, arr3_coeffs, arr5_coeffs, arr3_difference, arr5_difference)
    total_out = np.vstack((total_out, out02))
    #print(out02)
    print('36')
    out03 = find_true_coincidences(tau, epsilon, E0, arr3, arr6, arr3_coeffs, arr6_coeffs, arr3_difference, arr6_difference)
    total_out = np.vstack((total_out, out03))    
    #print(out03)
    print('37')
    out12 = find_true_coincidences(tau, epsilon, E0, arr3, arr7, arr3_coeffs, arr7_coeffs, arr3_difference, arr7_difference)
    total_out = np.vstack((total_out, out12))
    #print(out12)
    '''
    
    #arrays = (arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7)
    arrays = (arr0, arr1, arr2, arr3)
    
    for x in range(4):
        for y in range(x, 4):
            if x == y:
                pass
            else:
                print(x, y)
                arrA_coeffs, arrA_difference = detector_polynomial_time_fit(arrays[x])
                arrB_coeffs, arrB_difference = detector_polynomial_time_fit(arrays[y])
                total_out = np.vstack((total_out, find_true_coincidences(tau, epsilon, E0, arrays[x], arrays[y], arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference)))
    
    total_out = total_out[1:]
    
    print(total_out)
    print(f'In total, {total_out.shape[0]} coincidences were identified in the {data_label} data with epsilon = {epsilon} and tau = {tau}.')
    E_scat = total_out[:,0]
    E_abs = total_out[:,1]
    E_sums = E_scat + E_abs
    
    fig = plt.figure()
    plt.hist([E_sums, E_scat, E_abs], bins=200, color=['green', 'blue', 'red'], label=['Sum of Energies', 'Scatter Energy', 'Absorption Energy'])
    plt.plot(0.662, 50, color='orange', marker='X', ms=20, label='662 keV')
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Number of counts')
    plt.title(f'Histogram showing energy distribution of find_true_coincidences output for epsilon = {epsilon}, tau={tau} with {data_label} data: 03/03/24')
    plt.legend()
    plt.show() 
    
    '''
    print('10')
    out10 = find_true_coincidences(tau, epsilon, E0, arr1, arr0, arr1_coeffs, arr0_coeffs, arr1_difference, arr0_difference)
    #print(out10)
    print('20')
    out20 = find_true_coincidences(tau, epsilon, E0, arr2, arr0, arr2_coeffs, arr0_coeffs, arr2_difference, arr0_difference)
    #print(out20)
    print('30')
    out30 = find_true_coincidences(tau, epsilon, E0, arr3, arr0, arr3_coeffs, arr0_coeffs, arr3_difference, arr0_difference)
    #print(out30)
    print('21')
    out21 = find_true_coincidences(tau, epsilon, E0, arr2, arr1, arr2_coeffs, arr1_coeffs, arr2_difference, arr1_difference)
    #print(out21)
    print('31')
    out31 = find_true_coincidences(tau, epsilon, E0, arr3, arr1, arr3_coeffs, arr1_coeffs, arr3_difference, arr1_difference)
    #print(out31)
    print('32')
    out32 = find_true_coincidences(tau, epsilon, E0, arr3, arr2, arr3_coeffs, arr2_coeffs, arr3_difference, arr2_difference)
    #print(out32)
    '''
    '''
    E_sums01 = (out01[:,0] + out01[:,1])
    E_sums02 = (out02[:,0] + out02[:,1])
    E_sums03 = (out03[:,0] + out03[:,1])
    E_sums12 = (out12[:,0] + out12[:,1])
    E_sums13 = (out13[:,0] + out13[:,1])
    E_sums23 = (out23[:,0] + out23[:,1])
    E_sums10 = (out10[:,0] + out10[:,1])
    E_sums20 = (out20[:,0] + out20[:,1])
    E_sums30 = (out30[:,0] + out30[:,1])
    E_sums21 = (out21[:,0] + out21[:,1])
    E_sums31 = (out31[:,0] + out31[:,1])
    E_sums32 = (out32[:,0] + out32[:,1])
    
    E_sums = np.array((E_sums01, E_sums02, E_sums03, E_sums12, E_sums13, E_sums23,
              E_sums10, E_sums20, E_sums30, E_sums21, E_sums31, E_sums32),
                      dtype='object')
    E_scat = np.array((out01[:,0], out02[:,0], out03[:,0], out12[:,0], out13[:,0], 
              out23[:,0], out10[:,0], out20[:,0], out30[:,0], out21[:,0], 
              out31[:,0], out32[:,0]), dtype='object')
    E_abs = np.array((out01[:,1], out02[:,1], out03[:,1], out12[:,1], out13[:,1], 
              out23[:,1], out10[:,1], out20[:,1], out30[:,1], out21[:,1], 
              out31[:,1], out32[:,1]), dtype='object')
    print(E_sums, E_scat, E_abs)
    fig = plt.figure()
    plt.hist([E_sums.flatten(), E_scat.flatten(), E_abs.flatten()], bins=5000, color=['green', 'blue', 'red'])
    plt.xlabel('Sum of energies of events identified as being a valid pair (MeV)')
    plt.ylabel('Number of counts')
    plt.title(f'Histogram showing energy sum distribution of find_true_coincidences output for epsilon = {epsilon} with smeared MC data')
    plt.show()
    '''
    # print('00')
    # out00 = find_true_coincidences(tau, epsilon, E0, arr0, arr0)
    # #print(out00)
    # print('11')
    # out11 = find_true_coincidences(tau, epsilon, E0, arr1, arr1)
    # #print(out11)
    # print('22')
    # out22 = find_true_coincidences(tau, epsilon, E0, arr2, arr2)
    # #print(out22)
    # print('33')
    # out33 = find_true_coincidences(tau, epsilon, E0, arr3, arr3)
    # #print(out33)

