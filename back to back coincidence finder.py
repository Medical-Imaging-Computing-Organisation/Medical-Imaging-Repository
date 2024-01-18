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
# specify where your CSV file can be found here
Folder_Path = ''
File1_Name = ''

def CSV_Extract(Folder_Path, File1_Name, File2_Name=None, File3_Name=None, Header=None):
    '''
    Takes from 1-3 CSV file locations and extracts their data to cupy arrays
    
            Parameters:
                    Folder_Path (string): The local directory path where the CSV(s) are stored
                    File1_Name (string): The file name of the first CSV to have data extracted
                    
            Optional Parameters:
                    File2_Name (string): The file name of the second CSV to have data extracted
                    File3_Name (string): The file name of the third CSV to have data extracted
                    Header: Optional specification for CSVs containing a header row, default is None
                    
            Returns:
                    arr1 (,arr2, arr3) (CuPy Array): Cupy Arrays with the data from input CSVs
                    
    '''   
    # Forming full location path for CSV1, creating pandas DataFrame and transferring to numpy (cupy) array
    BaseLocation = str(Path(Folder_Path))
    CSV1Location = BaseLocation + "\\" + File1_Name
    df1 = pd.read_csv(CSV1Location, sep=';', header=Header, dtype=np.float32)
    arr1 = df1.values

    # Performing the same for optional second and third CSVs if applicable
    if File2_Name != None:
        CSV2Location = BaseLocation + "\\" + File2_Name
        df2 = pd.read_csv(CSV2Location, sep=';', header=Header, dtype=np.float32)
        arr2 = df2.values
        if File3_Name != None:
            CSV3Location = BaseLocation + "\\" + File3_Name
            df3 = pd.read_csv(CSV3Location, sep=';', header=Header, dtype=np.float32)
            arr3 = df3.values
            return arr1, arr2, arr3
        else:
            return arr1, arr2
    else:
        return arr1

all_events = CSV_Extract(Folder_Path, File1_Name)
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