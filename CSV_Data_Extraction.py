# This will be our code for extracting data from the CSV-style output from labs

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
    # Imports
    import cupy as np
    import pandas as pd
    from pathlib import Path
    
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


