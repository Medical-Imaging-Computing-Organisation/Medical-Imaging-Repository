# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:58:17 2024

This script is for identifying pairs of coincident events in the back-to-back 
detector setup. It takes a CSV file of the format agreed between Chris and the
lab data team and outputs an array of the format:

    [[i, j, t1, t2, delta_t1, delta_t2],
     [i, j, t1, t2, delta_t1, delta_t2],
     ...]

where i and j are the indices of the coincident events in the CSV file; t1 and
t2 are the times at which events i and j occurred; and delta_t1 and delta_t2
are the uncertainties on t1 and t2.

The CSV_Extract function was written by Chris. The rest of the code was
written by Alfie.
"""
# Imports
import numpy as np # can use cupy instead of numpy if you want to do GPU stuff
import pandas as pd
from pathlib import Path

tau = 10 # choose your coincidence window here (in the same time units as your CSV data)
# specify where your Energy-Time CSV file can be found here
# note: for windows Folder_Path, swap all \ to /
Folder_Path = ''
File1_Name = ''

# specify your delimiter for all CSV(s) here (eg. place a , or ; inside the '')
Delimiter = ''

# specify where optional Detector Location and Detector Pairing CSV files can be found here (de-comment the code)
#File2_Name = ''
#File3_Name = ''

def CSV_Extract(Delimiter, Folder_Path, File1_Name, File2_Name=None, File3_Name=None, Multiprocess=False, Header=None):
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
                    Multiprocess (boolean): Whether to use CPU parallelization for data extraction, default is False
                        Note: Multiprocess assumes 8 available threads                                      
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
    import multiprocessing
    
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
    
    # Multiprocessing branch - in development
    if Multiprocess == True:
    
        in_development = "Code still in development, will be added as soon as possible. Please use regular processing for now."
        
        return in_development
        
    # Concurrent branch - functioning
    else:
        
        # Read Energy-Time CSV and populate numpy array with its data
        df1 = Read_CSV(CSV1Location, [0,1,2,3,4], Header, np.float32)
        arr1 = df1.values
        
        # Conditional for Detector Location CSV
        if File2_Name != None:
            
            # Read Detector Location CSV, accounting for floats/strings, and populate numpy array with its data
            df2_1 = Read_CSV(CSV2Location, [0,1,2,3,4,5,6], Header, np.float32)
            arr2_1 = df2_1.values
            df2_2 = Read_CSV(CSV2Location, [7], Header, str)
            arr2_2 = df2_2.values
            arr2 = np.hstack((arr2_1, arr2_2))
            
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

# For the purposes of the initial lab test in week 1, only the Energy-Time array needs to be created, and Multiprocessing isn't strictly necessary
# If the Energy-Time CSV has a header row, comment out the first all_events line and de-comment the second, replacing Header with the row numbers that are headers (eg. 0 if it's solely the first row)
all_events = CSV_Extract(Folder_Path, File1_Name)
#all_events = CSV_Extract(Folder_path, File1_Name, None, None, False, Header)
all_coincidences = np.empty(4)

for i in range(len(all_events)):
    # iterate over every event in the input array
    # extract time information from the i^th event
    t1 = all_events[i, 2]
    delta_t1 = all_events[i, 4]

    # calculate limits of the coincidence window for the i^th event
    t_max = t1 + delta_t1 + tau
    t_min = t1 - delta_t1 - tau

    for j in range(i+1, len(all_events)):
        # now iterate over every event AFTER the i^th event in the input array
        # extract time information from the j^th event
        t2 = all_events[j, 2]
        delta_t2 = all_events[j, 4]

        # test whether the j^th event falls within the limits calculated above
        if bool(t_min <= t2 - delta_t2 and t_max >= t2 + delta_t2) is True:
            # if True, events i and j form a coincident pair
            coincidence_info = np.array([i, j, t1, t2, delta_t1, delta_t2])
            all_coincidences = np.vstack(all_coincidences, coincidence_info)

print(all_coincidences)
