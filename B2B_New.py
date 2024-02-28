# Imports
import numpy as np
import os
import pandas as pd
from pathlib import Path
from numba import njit
from numba import prange
from matplotlib import pyplot as plt



# Function parameters (change as required)
tau = 1E6
Delimiter = ','
Header = 0
# Fill in the location and name of your energy-time data CSV file
Folder_Path = os.getcwd() # can leave this as is if your file is saved in the same folder as this script
ETFile0_Name = 'merged_nodelay.csv'

def detector_time_fit(arr, plot_fit=False, plot_difference=False):
    '''
    
    MODIFIED FOR merged_nodelay.csv
    
    @author = Chris
    
    Takes a detector energy-time array and generates a linear fit for its timestamps and the difference between the fit and data.
    Optionally can plot graphs of the fit or differences.
    
    
            Parameters:
                arr (numpy array): Energy-time array output of CSV extraction
                
                
            Returns:
                coeffs, difference
                
                
                
                    coeffs: linear fit coefficients y = coeffs[0] * x + coeffs[1]
                    
                    difference: 1D array of input array length containing the difference between fit and data for each index in the detector
    
    
    '''
    
    
    # Extract the time column from the detector array
    det_time_arr = arr[:,1]
    
    
    # calculate index values
    index_values = np.arange(0, arr[:,1].shape[0], 1)
    
    
    # calculate linear time fit of detector array
    coeffs = np.polyfit(index_values, det_time_arr, 1)
    
    # calculate difference between fit timestamp and actual timestamp
    difference = arr[:,1] - (coeffs[0]*index_values + coeffs[1])
    
    # plot fit and data if requested
    if plot_fit == True:
        fig, ax = plt.subplots()
        
        ax.scatter(index_values, det_time_arr, label='Data')
        ax.plot(index_values, coeffs[0]*index_values + coeffs[1], label='Fit', color='r')
        ax.set(xlabel='Detector Index', ylabel='Timestamp')
        ax.legend()
        ax.grid()

        
        plt.show()
    
    # plot difference between fit and data if requested
    if plot_difference == True:
        fig, ax = plt.subplots()
        
        ax.plot(index_values, difference, label='Difference')
        ax.set(xlabel='Detector Index', ylabel='Difference between fit and data')
        ax.legend()
        ax.grid()

        
        plt.show()
    
    return coeffs, difference

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






# this code is just for the data format in merged_nodelay.csv
master_array = CSV_Extract(Delimiter, Folder_Path, ETFile0_Name, None, None, Header)

arrA = master_array[0:3113656]

arrB = master_array[3113657:]


# determine the region in arrB to examine for coincidences
# test_window_size = int(5 * tau / ave_tstepB) # in dimensions of indices
search_window_size = 1000
test_window_size = 10


temp_arr = np.ndarray((arrA.shape[0], test_window_size, 2), dtype=np.float32)

# generate linear fits for arrA and arrB
arrA_coeffs, arrA_difference = detector_time_fit(arrA)
arrB_coeffs, arrB_difference = detector_time_fit(arrB)

package = np.empty((arrA.shape[0], test_window_size, 2), dtype=np.float32)
column0 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)
column1 = np.empty((arrA.shape[0], test_window_size), dtype=np.float32)


@njit(parallel=True)
def modified_b2b_func(tau, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, column0, column1, package):
    
    # MODIFIED FOR merged_nodelay.csv

    # extract time information from arrA and arrB
    tA = arrA[:, 1]
    # tB = arrB[:, 2]
    delta_tA = arrA[:, 4]
    delta_tB = arrB[:, 4]
    
    # MODIFIED FOR merged_nodelay.csv
    # set all errors to 0
    delta_tA[:] = 0
    delta_tB[:] = 0

    # calculate limits of time coincidence window for each event in arrA
    t_max = tA + tau + delta_tA
    t_min = tA - tau - delta_tA
    

    print('Starting Loop')
    
    for i in prange(0, arrA.shape[0]):
    # iterate over every event in arrA. For the i^th event:          
        
        
        
        
        # generate initial guess of j from linear fit

        initial_j = int((tA[i]-arrB_coeffs[1])/arrB_coeffs[0])
        
        
        
        # use initial j guess to inform search window size
        search_max = int(min(arrB[:,1].shape[0]-1, initial_j+search_window_size))
        search_min = int(max(0, initial_j-search_window_size))
        
        search_window = arrB[int(search_min) : int(search_max)]
        
        j = search_min + np.argmin((tA[i] - search_window[:,1])**2 )
    
        
        # calculate limits of the testing window for the i^th event in arrA
        test_min = int(min(arrB[:,1].shape[0]-1-test_window_size, max(0, min(j - 1.5 * test_window_size, arrB.shape[0]))))
        test_max = int(min(arrB[:,1].shape[0]-1, max(test_min+test_window_size, min(j + test_window_size, arrB.shape[0]))))

        test_window = arrB[int(test_min) : int(test_max)]

        # check which elements in test_window are between limits of tau
        time_test = np.where( (t_min[i] <= test_window[:,1] - test_window[:,4]) & (t_max[i] >= test_window[:,1] + test_window[:,4]) )[0]
        coinc_events = test_window[time_test]
        
        # quick fix
        if coinc_events.shape[0] > test_window_size:
            coinc_events = coinc_events[:test_window_size]
        # print(i)
        # print(coinc_events[:,1])
        # print("----------------")
        
        
        column0[i][:coinc_events.shape[0]] = tA[i]
        column0[i][coinc_events.shape[0]:] = 0
        

         
        column1[i][:coinc_events.shape[0]] = coinc_events[:,1]
        column1[i][coinc_events.shape[0]:] = 0
        

        # package up the info we want about each coincident pair of events
        package[i, :, 0] = column0[i]
        package[i, :, 1] = column1[i]
        

        temp_arr[i] = package[i]
       
    return temp_arr

x = modified_b2b_func(tau, arrA, arrB, temp_arr, arrA_coeffs, arrB_coeffs, arrA_difference, arrB_difference, column0, column1, package)
#print(np.reshape(x[x[:,-1] != 0], (x.shape[0], -1, x.shape[-1])))
x = x[~np.all(x == 0, axis=2)]

print(x)
