

def CSV_Extract(Folder_Path, File1_Name, File2_Name, File3_Name, Multiprocess=False, Header=None):
    '''

    @author: chris


    Takes 3 CSV file locations in pre-specified format and extracts their data to Numpy Arrays
    
            Parameters:
                    Folder_Path (string): The local directory path where the CSV(s) are stored
                    File1_Name (string): The file name of the Energy-Time CSV to have data extracted
                    File2_Name (string): The file name of the Detector Location CSV to have data extracted
                    File3_Name (string): The file name of the Detector Pairing CSV to have data extracted
                    
            Optional Parameters:
                    Multiprocess (boolean): Whether to use CPU parallelization for data extraction, default is False
                        Note: Multiprocess assumes 8 available threads
                                        
                    Header: Optional specification for when CSVs contain a header row, default is None
                    
            Returns:
                    arr1, arr2, arr3 (Numpy Array): Numpy Arrays with the data from input CSVs
                
                        arr1: [[Detector Index, Energy, Time, Delta Energy, Delta Time], ...]
                        arr2: [[Detector Index, x, y, z, Delta x, Delta y, Delta z, Sc/Ab], ...]
                        arr3: [[Scatterer Index, Absorber Index, Ballpark Angular Uncertainty], ...]
                    
    '''
    # Imports
    import numpy as np
    import pandas as pd
    from pathlib import Path
    import multiprocessing
    
    # Forming full location path for each CSV
    BaseLocation = str(Path(Folder_Path))
    CSV1Location = BaseLocation + "\\" + File1_Name
    CSV2Location = BaseLocation + "\\" + File2_Name
    CSV3Location = BaseLocation + "\\" + File3_Name
    
    
    # Internal processing function for reading CSVs via Pandas
    def Read_CSV(Location, columns, Header, datatype):
        df = pd.read_csv(Location, sep=';', usecols=columns, header=Header, dtype=datatype)
        return df
    
    # Multiprocessing branch - in development
    if Multiprocess == True:
        
        print("Code still in development, will be added as soon as possible. Please use regular processing for now.")
        
        
    # Concurrent branch - functioning
    else:
        # Read Energy-Time CSV and populate numpy array with its data
        df1 = Read_CSV(CSV1Location, [0,1,2,3,4], Header, np.float32)
        arr1 = df1.values
        
        # Read Detector Location CSV, accounting for floats/strings, and populate numpy array with its data
        df2_1 = Read_CSV(CSV2Location, [0,1,2,3,4,5,6], Header, np.float32)
        arr2_1 = df2_1.values
        df2_2 = Read_CSV(CSV2Location, [7], Header, str)
        arr2_2 = df2_2.values
        arr2 = np.hstack((arr2_1, arr2_2))
        
        # Read Detector Pairing CSV and populate numpy array with its data
        df3 = Read_CSV(CSV3Location, [0,1,2], Header, np.float32)
        arr3 = df3.values


    return arr1, arr2, arr3






if __name__ == "__main__":
    

    EnergyTimeCSVName = 'test1.csv'
    DetectorPositionCSVName = 'test2.csv'
    DetectorPairingCSVName = 'test3.csv'
    BaseLocation = str(Path("C:/Users/chris/Documents/Medical_Physics_Group_Study/Lab_CSVs"))


    EnergyTimeCSVLocation = BaseLocation + "\\" + EnergyTimeCSVName
    DetectorPositionCSVLocation = BaseLocation + "\\" + DetectorPositionCSVName
    DetectorPairingCSVLocation = BaseLocation + "\\" + DetectorPairingCSVName

    start = timer()
    x,y,z = CSV_Extract(BaseLocation, EnergyTimeCSVName, DetectorPositionCSVName, DetectorPairingCSVName)
    print(timer()-start)
