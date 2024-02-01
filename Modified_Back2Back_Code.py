# Imports
import numpy as np
import pandas as pd
from pathlib import Path
from numba import njit
from numba import prange
from numba import set_num_threads

# set_num_threads(16)

# Generating test data for Alfie
# Format [[detector index, energy, time, delta E, delta t], ...] for each detector

# # Detector 1 
# detector1_fake_arr = np.ndarray((4000000,5), dtype=np.float32)
# detector1_fake_arr[:,0] = 0
# detector1_fake_arr[:,1] = 662
# detector1_fake_arr[:,2] = np.arange(1414, 4001414, 1)
# detector1_fake_arr[:,3] = np.random.rand(4000000)
# detector1_fake_arr[:,4] = np.random.rand(4000000)

# detector2_fake_arr = np.ndarray((4000000,5), dtype=np.float32)
# detector2_fake_arr[:,0] = 1
# detector2_fake_arr[:,1] = 662
# detector2_fake_arr[:1000000,2] = np.arange(1414.2, 1001414.2, 1) # 0.2 time units apart for the first 1 million data points
# detector2_fake_arr[1000000:2000000,2] = np.arange(2414, 1002414, 1) # 1000 time units apart for the second 1 million data points
# detector2_fake_arr[2000000:3000000,2] = np.arange(2001414.3, 3001414.3, 1) # 0.3 time units apart for the third 1 million data points
# detector2_fake_arr[3000000:4000000,2] = np.arange(8001414.3, 9001413.3, 1) # a lot of time units apart for the third 1 million data points
# detector2_fake_arr[:,3] = np.random.rand(4000000)
# detector2_fake_arr[:,4] = np.random.rand(4000000)

# Function parameters (change as required)
tau = 1000000000
Delimiter = ','
Number_of_Files = 1
Header = 0
# Fill in the location and name of your energy-time data CSV file
Folder_Path = 'C:/Users/chris/Documents/Medical_Physics_Group_Study/Lab_CSVs'
ETFile0_Name = 'merged_nodelay.csv'

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
        
    if ETFile2_Name != None:
        ETLocation_Array[2] = BaseLocation + "\\" + ETFile2_Name
            
    if ETFile3_Name != None:
        ETLocation_Array[3] = BaseLocation + "\\" + ETFile3_Name
                
    if ETFile4_Name != None:
        ETLocation_Array[4] = BaseLocation + "\\" + ETFile4_Name
                    
    if ETFile5_Name != None:
        ETLocation_Array[5] = BaseLocation + "\\" + ETFile5_Name
                        
    if ETFile6_Name != None:
        ETLocation_Array[6] = BaseLocation + "\\" + ETFile6_Name
                            
    if ETFile7_Name != None:
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






# this code is just for the data format in merged_nodelay.csv
master_array = CSV_Extract_Multiple_Channel_Files(Delimiter, Number_of_Files, Folder_Path, ETFile0_Name, None, None, None, None, None, None, None, None, None, Header)[0]

arr_det0 = master_array[0:3113656]

arr_det1 = master_array[3113657:]




tau = 1E8
# determine the region to examine for coincidences (time_width = 1.5 * tau)
test_window_size = int(1.5 * tau / ave_tstep2) # in dimensions of indices
output_arr = np.ndarray((arr1.shape[0], test_window_size, 2), dtype=np.float32)


@njit(parallel=True)
def modified_b2b_func(tau, arr1, arr2, output_arr):
    
    
    ave_tstep1 = (arr1[-1, 1] - arr1[0, 1]) / arr1.shape[0]
    ave_tstep2 = (arr2[-1, 1] - arr2[0, 1]) / arr2.shape[0]
    t_step_ratio = ave_tstep2 / ave_tstep1
#     print(ave_tstep1)
#     print(ave_tstep2)
    
    
    # extract time information
    t1 = arr1[:, 1] # COMMENT THIS OUT FOR MAIN CODE
#     t1 = arr1[i, 2]  # DECOMMENT THIS FOR MAIN CODE

    t2 = arr2[:, 1] # COMMENT THIS OUT FOR MAIN CODE
#     t2 = arr2[i, 2]  # DECOMMENT THIS FOR MAIN CODE
    
#     calculate limits of the coincidence window for each event
    t_max = t1 + tau
    t_min = t1 - tau
    
    
    for i in prange(test_window_size, min(arr1.shape[0], arr2.shape[0]) - test_window_size):
        
        
#         calculate limits of the testing window for the i^th event
        test_max = int(i + 0.5 * test_window_size)
        test_min = int(i - 0.5 * test_window_size)
        
    
        test_window = t2[test_min : test_max]

#         coin = np.where( (t_min[i] <= test_window) & (t_max[i] >= test_window) )
        coin = np.where( (t_min[i] <= t2) & (t_max[i] >= t2) )

        coinc_events = test_window[coin]
        
        
       
        
        
        
        

modified_b2b_func(tau, arr_det0, arr_det1, output_arr)



