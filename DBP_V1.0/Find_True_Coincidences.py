# Imports
import numpy as np
from numba import njit
from numba import prange
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    # Parameters (remember to change based on units of your data)
    tau = 0.001 # time coincidence window
    epsilon = 0.01 # energy coincidence window
    E0 = 0.662 # initial photon energy
'''
arr0 = np.array([[0, 10, 1, 0.1, 0.1],
        [0, 10, 2, 0.1, 0.2],
        [0, 10, 2.5, 0.1, 0.1],
        [0, 12, 2.7, 0.2, 0.1],
        [0, 10, 3, 0.3, 0.1],
        [0, 8, 4.5, 0.5, 0.2],
        [0, 10, 5, 0.2, 0.2],
        [0, 11, 5.2, 0.2, 0.1],
        [0, 12, 5.3, 0.1, 0.4],
        [0, 9, 5.6, 0.3, 0.1],
        [0, 7, 5.8, 0.1, 0.1],
        [0, 3, 5.9, 0.2, 0.1],
        [0, 4, 6.1, 0.4, 0.1],
        [0, 6, 6.3, 0.2, 0.1],
        [0, 10, 6.9, 0.1, 0.1],
        [0, 11, 7.1, 0.1, 0.1],
        [0, 12, 7.4, 0.1, 0.1],
        [0, 13, 7.5, 0.2, 0.2],
        [0, 12, 7.8, 0.1, 0.1],
        [0, 14, 8, 0.2, 0.2],
        [0, 15, 8.2, 0.1, 0.1],
        [0, 16, 8.5, 0.2, 0.3],
        [0, 17, 8.8, 0.3, 0.1],
        [0, 13, 9.1, 0.1, 0.1],
        [0, 14, 9.3, 0.2, 0.2],
        [0, 15, 9.7, 0.1, 0.1],
        [0, 16, 10, 0.1, 0.1]
        ])

arr1 = np.array([[1, 12, 1, 0.1, 0.2],
        [1, 11, 1.1, 0.1, 0.1],
        [1, 13, 1.8, 0.2, 0.1],
        [1, 9, 2.6, 0.1, 0.2],
        [1, 10, 2.9, 0.2, 0.1],
        [1, 15, 3.2, 0.4, 0.1],
        [1, 13, 3.4, 0.2, 0.2],
        [1, 16, 4, 0.1, 0.4],
        [1, 12, 4.1, 0.1, 0.1],
        [1, 11, 4.7, 0.2, 0.3],
        [1, 13, 5, 0.1, 0.1],
        [1, 14, 5.2, 0.2, 0.2],
        [1, 13, 5.4, 0.1, 0.1],
        [1, 15, 5.6, 0.2, 0.2],
        [1, 11, 5.9, 0.1, 0.1],
        [1, 13, 6.0, 0.2, 0.3],
        [1, 15, 7.1, 0.1, 0.2],
        [1, 8, 7.2, 0.2, 0.2],
        [1, 9, 7.3, 0.1, 0.1],
        [1, 10, 7.5, 0.1, 0.1],
        [1, 11, 7.8, 0.2, 0.2],
        [1, 12, 8.0, 0.1, 0.1],
        [1, 13, 8.3, 0.4, 0.2],
        [1, 14, 8.4, 0.1, 0.1],
        [1, 15, 8.8, 0.1, 0.1],
        [1, 11, 8.9, 0.2, 0.2],
        [1, 12, 9.1, 0.3, 0.2],
        [1, 8, 9.4, 0.2, 0.1],
        [1, 10, 10, 0.1, 0.1]
        ])
'''

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
    None.

    '''
    # ave_tstepA = (arrA[-1, 2] - arrA[0, 2]) / arrA.shape[0]
    # ave_tstepB = (arrB[-1, 2] - arrB[0, 2]) / arrB.shape[0]
    # print(f'ave_tstepA == {ave_tstepA}')
    # print(f'ave_tstepB == {ave_tstepB}')

    # determine the region in arrB to examine for coincidences
    # test_window_size = int(5 * tau / ave_tstepB) # in dimensions of indices
    search_window_size = 1000
    test_window_size = 10
    print(f'test_window_size is {test_window_size}')
    # test_window_radius = 1
    # print(f'test_window_radius is {test_window_radius}')

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
    
    # define an array to contain the coincident events
    # temp_arr = np.ndarray((arrA.shape[0], int(2*test_window_radius+1), 6), dtype=np.float32)

    # # define for use later (I had to change dtype to float32 so that my laptop could cope with the memory allocation)
    # package = np.empty((arrA.shape[0], int(2*test_window_radius+1), 6), dtype=np.float32)
    # column0 = np.empty((arrA.shape[0], int(2*test_window_radius+1)), dtype=np.float32)
    # column1 = np.empty((arrA.shape[0], int(2*test_window_radius+1)), dtype=np.float32)
    # column2 = np.empty((arrA.shape[0], int(2*test_window_radius+1)), dtype=np.float32)
    # column3 = np.empty((arrA.shape[0], int(2*test_window_radius+1)), dtype=np.float32)
    # column4 = np.empty((arrA.shape[0], int(2*test_window_radius+1)), dtype=np.float32)
    # column5 = np.empty((arrA.shape[0], int(2*test_window_radius+1)), dtype=np.float32)

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
            
            
            # alternative method of calculating j using detector linear fits
            
            
            
            
            initial_j = int((tA[i]-arrB_coeffs[1])/arrB_coeffs[0])
            
            
            
            
            
            # use initial j guess to inform search window size
            search_max = int(min(arrB[:,2].shape[0]-1, initial_j+search_window_size))
            search_min = int(max(0, initial_j-search_window_size))
            
            search_window = arrB[int(search_min) : int(search_max)]
            
            j = search_min + np.argmin((tA[i] - search_window[:,2])**2 )
        
            
            # calculate limits of the testing window for the i^th event in arrA
            test_min = int(min(arrB[:,2].shape[0]-1-test_window_size, max(0, min(j - 1.5 * test_window_size, arrB.shape[0]))))
            test_max = int(min(arrB[:,2].shape[0]-1, max(test_min+test_window_size, min(j + test_window_size, arrB.shape[0]))))
            
            
            
            # testing specific value(s) MC gave us
            if i in range(4001, 4002):
                print("------------------------")
                print(i)
                print("---")
                print(tA[i])
                # print(arrB_coeffs[1])
                # print(arrB_coeffs[0])
                print("-----")
                print(initial_j)
                print(search_min)
                print(search_max)
                # print(search_window)
                print("-----")
                # print((tA[i] - arrB[8605:8610,2])**2)
                print(j)        
                print(test_min)
                print(test_max)
                
            
            
            
            test_window = arrB[int(test_min) : int(test_max)]
            
            
            # testing specific value(s) MC gave us
            if i in range(4001, 4002):
                print(test_window)
                
                
            
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
            #print(events_before, events_after)
            #print(i, valid_events, events_before, events_after)

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

            # package up the columns
            package[i, :, 0] = column0[i]
            package[i, :, 1] = column1[i]
            package[i, :, 2] = column2[i]
            package[i, :, 3] = column3[i]
            package[i, :, 4] = column4[i]
            package[i, :, 5] = column5[i]

            # delete rows where photon was absorbed in its first interaction
            #noscat = np.where((column0[i] != 0) & (column1[i] - column3[i] < epsilon))[0]
            #print(noscat)
            #package[i][noscat] = np.zeros(6)

            temp_arr[i] = package[i]

        return temp_arr

    output = two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, package, column0, column1, column2, column3, column4, column5)
    # get rid of the zeros
    output = output[~np.all(output[:, :, :4] == 0, axis=2)]
    '''
    exp_runtime = arrA[-1, 2] - arrB[0, 2]
    print(f'arrA ({arrA.shape[0]} events) was compared to arrB ({arrB.shape[0]} events).')
    print(f'The script found {output.shape[0]} pairs of coincident events.')
    print(f'The experiment ran for {exp_runtime} seconds.')
    print(f'Therefore the number of coincidences detected per second was {output.shape[0] / exp_runtime}.')
    '''
    # print(output[np.where(output[:, 0] / output[:, 1] >= 2 * E0 / m_e)])
    print(f'The array with {arrA.shape[0]} events was compared to the array with {arrB.shape[0]} events.')
    print(f'The script found {output.shape[0]} event pairs which it thinks are good.')
    return output

def CSV_Extract_Multiple_Channel_Files(Delimiter, Number_of_Detectors, Folder_Path, ETFile0_Name, ETFile1_Name=None, ETFile2_Name=None, ETFile3_Name=None, ETFile4_Name=None, ETFile5_Name=None, ETFile6_Name=None, ETFile7_Name=None, File2_Name=None, File3_Name=None, Header=None):
    '''

    @author = Chris

    Takes 1-8 Energy-Time CSV file locations and 0-2 Detector Information CSV file locations in pre-specified format and extracts their data to Numpy Arrays

            Parameters:
                    Delimiter (string): Delimiter for column separation within the CSV(s)
                    Number_of_Detectors (int): Number of detectors used for the run producing the CSV
                    Folder_Path (string): The local directory path where the CSV(s) are stored
                    ETFile0_Name (string): The file name of the Energy-Time CSV to have data extracted


            Optional Parameters:
                    ETFile1_Name - ETFile7_Name (strings): The file names of up to 7 more Energy-Time CSVs to have data extracted
                    File2_Name (string): The file name of the Detector Location CSV to have data extracted
                    File3_Name (string): The file name of the Detector Pairing CSV to have data extracted                          
                    Header: Optional specification for when CSVs contain a header row, default is None

            Required Imports:
                    import numpy as np
                    import pandas as pd
                    from pathlib import Path


            Required CSV Formats:
                    Energy-Time CSV(s): | Detector Index (int) | Energy (float32) | Time (float32) | Delta Energy (float32) | Delta Time (float32) |


            Optional CSV Formats:
                    Detector Location CSV: | Detector Index (int) | x (float32) | y (float32) | z (float32) | Delta x (float32) | Delta y (float32) | Delta z (float32) | Sc/Ab (str) |
                    Detector Pairing CSV: | Scatterer Index (int) | Absorber Index (int) | Ballpark Angular Uncertainty (float32) |


            Returns:
                    arr1 (Numpy Array): Numpy Array (of Arrays) with the data from Energy-Time CSV(s)

                        arr1: [[[Detector Index, Energy, Time, Delta Energy, Delta Time], ...], [[Detector Index, Energy, Time, Delta Energy, Delta Time], ...], ...]


            Optional Returns:
                    arr2, arr3 (Numpy Arrays): Numpy Arrays with the data from Detector Location and Detector Pairing CSVs respectively

                        arr2: [[Detector Index, x, y, z, Delta x, Delta y, Delta z, Sc/Ab], ...]
                        arr3: [[Scatterer Index, Absorber Index, Ballpark Angular Uncertainty], ...]

    '''

    # Define location array, which will contain the paths for each Energy-Time CSV to be read
    ETLocation_Array = np.empty(8, dtype=np.ndarray)

    # Define array
    arr1 = np.empty(Number_of_Detectors, dtype=np.ndarray)

    # Forming base location path to folder containing CSVs
    BaseLocation = str(Path(Folder_Path))

    # Forming full location path for the first Energy-Time CSV
    ETLocation_Array[0] = BaseLocation + "\\" + ETFile0_Name

    # Forming full location paths for all other Energy-Time CSVs
    if ETFile1_Name != None:
        ETLocation_Array[1] = BaseLocation + "\\" + ETFile1_Name

    if ETFile2_Name is not None:
        ETLocation_Array[2] = BaseLocation + "\\" + ETFile2_Name

    if ETFile3_Name is not None:
        ETLocation_Array[3] = BaseLocation + "\\" + ETFile3_Name

    if ETFile4_Name is not None:
        ETLocation_Array[4] = BaseLocation + "\\" + ETFile4_Name

    if ETFile5_Name is not None:
        ETLocation_Array[5] = BaseLocation + "\\" + ETFile5_Name

    if ETFile6_Name is not None:
        ETLocation_Array[6] = BaseLocation + "\\" + ETFile6_Name

    if ETFile7_Name is not None:
        ETLocation_Array[7] = BaseLocation + "\\" + ETFile7_Name



    # Internal processing function for reading CSVs via Pandas
    def Read_CSV(Location, columns, Header, datatype):
        df = pd.read_csv(Location, sep=Delimiter, usecols=columns, header=Header, dtype=datatype)
        return df

    # Iterate through each detector and extract Energy-Time data, populating an array for each
    for i in range(Number_of_Detectors):
        df = Read_CSV(str(ETLocation_Array[i]), [0,1,2,3,4], Header, np.float32)
        arr1[i] = df.values



    # Conditional for Detector Location CSV
    if File2_Name != None:

        # Form location path for Detector Position CSV
        CSV2Location = BaseLocation + "\\" + File2_Name

        # Read Detector Location CSV, accounting for floats/strings, and populate numpy array with its data
        df2_1 = Read_CSV(CSV2Location, [0,1,2,3,4,5,6], Header, np.float32)
        arr2_1 = df2_1.values
        df2_2 = Read_CSV(CSV2Location, [7], Header, str)
        arr2_2 = df2_2.values
        arr2 = np.hstack((arr2_1, arr2_2))

        # Conditional for Detector Pairing CSV
        if File3_Name != None:

            # Form location path for Detector Pairing CSV
            CSV3Location = BaseLocation + "\\" + File3_Name

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

if __name__ == "__main__":
    data = CSV_Extract_Multiple_Channel_Files(',', 4, 'C:/Users/alfie/OneDrive/Documents/UoB/Y3 S2/Medical Imaging Group Study', 'CSV1_D1.csv', 'CSV1_D2.csv', 'CSV1_D3.csv', 'CSV1_D4.csv')
    arr0 = data[0]
    arr1 = data[1]
    arr2 = data[2]
    arr3 = data[3]

    output = find_true_coincidences(tau, epsilon, E0, arr0, arr1)
    print(output)

    exp_runtime = arr0[-1, 2] - arr0[0, 2]
    print(f'The script found {output.shape[0]} pairs of coincident events.')
    print(f'The experiment ran for {exp_runtime} seconds.')
    print(f'Therefore the number of coincidences detected per second was {output.shape[0] / exp_runtime}.')
