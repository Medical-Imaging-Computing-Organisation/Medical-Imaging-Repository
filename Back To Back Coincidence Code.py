# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:50:45 2024

@author: alfie
"""
# Imports
import numpy as np
import pandas as pd
from pathlib import Path

# Function parameters (change as required)
tau = 1000000000
Delimiter = ','
Number_of_Detectors = 1
Header = 0
# Fill in the location and name of your energy-time data CSV file
Folder_Path = 'C:/Users/alfie/OneDrive/Documents/UoB/Y3 S2/Medical Imaging Group Study'
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

def find_coincidences(tau, arr1, arr2):
    '''
    @author = Alfie
    
    For events observed in two detectors, this function finds which events
    occurred within a given coincidence window of each other.
    
    Imports
    ----------
    import numpy as np

    Parameters
    ----------
    tau : float
        Chosen coincidence window. Must be given in the same time units as the
        timestamps of the events.
    arr1 : array
        Array of events which were observed in the first detector.
    arr2 : array
        Array of events which were observed in the second detector.

    Both arr1 and arr2 should use the following format:
        [[detector index, energy, time, delta E, delta t], ...]

    Returns
    -------
    output_arr: an array giving time information on all coincident pairs.
    Format is [[t1, t2, delta_t1, delta_t2]] where t1 is the time of an event
    observed in the first detector, t2 is the time of a coincident event
    observed in the second detector, and (delta_t1, delta_t2) are the
    uncertainties on these time measurements.

    '''

    # calculate the average increase in t between each consecutive event in arr2
    ave_tstep2 = (arr2[-1, 1] - arr2[0, 1]) / arr2.shape[0]
    print(ave_tstep2)
    # determine the region to examine for coincidences (time_width = 1.5 * tau)
    test_window_size = int(1.5 * tau / ave_tstep2) # in dimensions of indices
    print(test_window_size)

    output_arr = np.empty(2)
    
    print(min(arr1.shape[0], arr2.shape[0]) - test_window_size)

    for i in range(test_window_size, min(arr1.shape[0], arr2.shape[0]) - test_window_size):
        # iterate over every event in arr1
        # exclude events near the start and end to avoid having to make a comparison every loop
        # also exclude events beyond the length of arr2 (if arr2 < arr1)

        # extract time information from the i^th event
        t1 = arr1[i, 1]
        print(t1)
       # delta_t1 = arr1[i, 4]

        # calculate limits of the coincidence window for the i^th event
        t_max = t1 + tau
        t_min = t1 - tau

        # calculate limits of the testing window for the i^th event
        test_max = int(i + 0.5 * test_window_size)
        test_min = int(i - 0.5 * test_window_size)

        # fill arrays with the limit values
        t_max_arr = np.full(test_max - test_min, t_max)
        t_min_arr = np.full(test_max - test_min, t_min)

        # slice arr2 between the test window limits
        test_window = arr2[test_min : test_max]
        # extract the time info of all events in the test window
        t2_arr = test_window[:, 1]
       # delta_t2_arr = test_window[:, 4]

        # find all indices in t2_arr where t2 falls within the coincidence window
        coin = np.where(((t_min_arr <= t2_arr) & (t_max_arr >= t2_arr)))
        # retrieve the events associated with those indices
        coinc_events = test_window[coin]

        # fill arrays with the values t1 and delta_t1, length = no. of coincidences
        t1_arr = np.full(coinc_events.shape[0], t1)
       # delta_t1_arr = np.full(coinc_events.shape[0], delta_t1)

        # package up the info we want about each coincident pair of events
        pair_info = np.empty((coinc_events.shape[0], 2))
        pair_info[:,0] = t1_arr # time of event 1
        pair_info[:,1] = coinc_events[:,1] # time of event 2
       # pair_info[:,2] = delta_t1_arr # uncertainty on time of event 1
       # pair_info[:,3] = coinc_events[:,4] # uncertainty on time of event 2

        # stack this set of coincident pairs onto the end of output_arr
        output_arr = np.vstack((output_arr, pair_info))
       # print(output_arr[1:])

    return output_arr[1:]

# this code is just for the data format in merged_nodelay.csv
master_array = CSV_Extract_Multiple_Channel_Files(Delimiter, Number_of_Detectors, Folder_Path, ETFile0_Name, None, None, None, None, None, None, None, None, None, Header)[0]
#print(master_array)
arr_det0 = master_array[0:3113656]
#print(arr_det0)
arr_det1 = master_array[3113657:]
#print(arr_det1)
print(find_coincidences(tau, arr_det0, arr_det1))