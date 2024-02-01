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
    
    
    # Imports, can be commented out when this function is being externally called and they are already imported
    import numpy as np
    import pandas as pd
    from pathlib import Path
    
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




if __name__ == "__main__":
    

    # Local test path
    Folder_Path = 'C:/Users/chris/Documents/Medical_Physics_Group_Study/Lab_CSVs'
    File1_Name = 'merged_nodelay.csv'
    # Delimiter for merged_nodelay file
    Delimiter = ','
    # Format for the merged_nodelay data reading
    x = CSV_Extract_Multiple_Channel_Files(Delimiter, 1, Folder_Path, File1_Name, None, None, None, None, None, None, None, None, None, 0)

