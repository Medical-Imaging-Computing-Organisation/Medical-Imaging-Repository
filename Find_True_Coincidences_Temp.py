# Imports
import numpy as np
from numba import njit
from numba import prange
import pandas as pd
from pathlib import Path
from timeit import default_timer as timer
import os


def find_true_coincidences(tau, epsilon, E0, arrA, arrB):
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
    ave_tstepA = (arrA[-1, 2] - arrA[0, 2]) / arrA.shape[0]
    ave_tstepB = (arrB[-1, 2] - arrB[0, 2]) / arrB.shape[0]
    print(f'ave_tstepA == {ave_tstepA}')
    print(f'ave_tstepB == {ave_tstepB}')

    # determine the region in arrB to examine for coincidences
    test_window_size = int(5 * tau / ave_tstepB) # in dimensions of indices
    #test_window_size = 10
    print(f'test_window_size is {test_window_size}')

    # define an array to contain the coincident events
    temp_arr = np.ndarray((arrA.shape[0], test_window_size, 6), dtype=np.float32)

    # define for use later (I had to change dtype to float32 so that my laptop could cope with the memory allocation)
    package = np.empty((arrA.shape[0], test_window_size, 6), dtype=np.float32)
    column0 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column1 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column2 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column3 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column4 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
    column5 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)

    @njit(parallel=True)
    def two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, ave_tstepA, ave_tstepB, package, column0, column1, column2, column3, column4, column5):
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
        tstep_ratio_AB = ave_tstepA / ave_tstepB

        # extract time information from arrA and arrB
        tA = arrA[:, 2]
        #tB = arrB[:, 2]
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

            # define corresponding index j in arrB
            j = int(max(0, min(tstep_ratio_AB * i, arrB.shape[0] - 1)))
            #print(i,j)
            # calculate limits of the testing window for the i^th event in arrA
            test_max = int(max(0, min(j + test_window_size, arrB.shape[0])))
            test_min = int(max(0, min(j - 0.5 * test_window_size, arrB.shape[0])))
            test_window = arrB[test_min : test_max]
            
            # check which elements in test_window are between limits of tau
            time_test = np.where( (t_min[i] <= test_window[:,2] - delta_tB[j]) & (t_max[i] >= test_window[:,2] + delta_tB[j]) )[0]
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

    output = two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, ave_tstepA, ave_tstepB, package, column0, column1, column2, column3, column4, column5)
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
    import numpy as np
    import pandas as pd
    from pathlib import Path
    
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

if __name__ == "__main__":
    start = timer()
    CSV_Start = timer()
    
    # Lab data 08 Feb setup 3
    Delimiter = ';'
    Header = 0
    Folder_Path = os.getcwd()
    ETFile0 = 'CH0 Feb08 Setup 3 A.csv'
    ETFile1 = 'CH1 Feb08 Setup 3 A.csv'
    ETFile2 = 'CH2 Feb08 Setup 3 A.csv'
    ETFile3 = 'CH3 Feb08 Setup 3 A.csv'
    # ETFile0 = 'CSV1_D1.csv'
    # ETFile1 = 'CSV1_D2.csv'
    # ETFile2 = 'CSV1_D3.csv'
    # ETFile3 = 'CSV1_D4.csv'
    Det_Pos = 'positionsetup 08Feb.csv'

    print("Started!")
    CSV_Start = timer()
    arr0, Det_Pos_arr = CSV_Extract(';', Folder_Path, Det_Pos, Det_Pos)
    arr0 = CSV_Extract(Delimiter, Folder_Path, ETFile0)
    arr1 = CSV_Extract(Delimiter, Folder_Path, ETFile1)
    arr2 = CSV_Extract(Delimiter, Folder_Path, ETFile2)
    arr3 = CSV_Extract(Delimiter, Folder_Path, ETFile3)

    print("CSV Extraction Done in {} s".format(timer() - CSV_Start))
    tau = 1E11 # time coincidence window
    epsilon = 0.1 # energy coincidence window
    E0 = 0.662 # initial photon energy

    # Monte Carlo data (Unsmeared)
    #data = CSV_Extract_Multiple_Channel_Files(',', 4, 'C:/Users/alfie/OneDrive/Documents/UoB/Y3 S2/Medical Imaging Group Study', 'CSV1_D1.csv', 'CSV1_D2.csv', 'CSV1_D3.csv', 'CSV1_D4.csv')
    #tau = 0.001
    #epsilon = 0
    #E0 = 0.662
    
    # Monte Carlo data (smeared)
    #data = CSV_Extract_Multiple_Channel_Files(',', 4, 'D:/Smeared Energy CSV1 files', 'CSV1_Full_Smeared_D1.csv', 'CSV1_Full_Smeared_D2.csv', 'CSV1_Full_Smeared_D3.csv', 'CSV1_Full_Smeared_D4.csv')
    #tau = 0.001
    #epsilon = 0.01
    #E0 = 0.662
    

    print('01')
    out01 = find_true_coincidences(tau, epsilon, E0, arr0, arr1)
    print(out01)
    # print('02')
    # out02 = find_true_coincidences(tau, epsilon, E0, arr0, arr2)
    # #print(out02)
    # print('03')
    # out03 = find_true_coincidences(tau, epsilon, E0, arr0, arr3)
    # #print(out03)
    # print('12')
    # out12 = find_true_coincidences(tau, epsilon, E0, arr1, arr2)
    # #print(out12)
    # print('13')
    # out13 = find_true_coincidences(tau, epsilon, E0, arr1, arr3)
    # #print(out13)
    # print('23')
    # out23 = find_true_coincidences(tau, epsilon, E0, arr2, arr3)
    # #print(out23)
    # print('10')
    # out10 = find_true_coincidences(tau, epsilon, E0, arr1, arr0)
    # #print(out10)
    # print('20')
    # out20 = find_true_coincidences(tau, epsilon, E0, arr2, arr0)
    # #print(out20)
    # print('30')
    # out30 = find_true_coincidences(tau, epsilon, E0, arr3, arr0)
    # #print(out30)
    # print('21')
    # out21 = find_true_coincidences(tau, epsilon, E0, arr2, arr1)
    # #print(out21)
    # print('31')
    # out31 = find_true_coincidences(tau, epsilon, E0, arr3, arr1)
    # #print(out31)
    # print('32')
    # out32 = find_true_coincidences(tau, epsilon, E0, arr3, arr2)
    # #print(out32)

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

