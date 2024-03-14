# edit for CSV2' positions
def CSV_Extract_NewCSV2(Delimiter, Folder_Path, File1_Name, File2_Name=None, File3_Name=None, Header=None):
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
                    Energy-Time CSV: | Detector Index (int) | X (float32) | Y (float32) | Z (float32) | Energy (float32) | Time (float32) | Delta Energy (float32) | Delta Time (float32) |
                    
                    
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
        df2_1 = Read_CSV(CSV2Location, [0,1,2,3,4,5,6,7,8,9,10,11,12,13], Header, np.float32)
        df2_1.iloc[:,[0,1,2,4,6,3,5,7,8,10,12,9,11,13]]
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
    
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    from timeit import default_timer as timer
    
    def detector_polynomial_time_fit(arr):
        
        
        
        # Extract the time column from the detector array
        det_time_arr = arr[:,2]
        
        # # calculate the difference in times
        # time = det_time_arr[1:] - det_time_arr[:-1]
        
        # calculate index values
        index_values = np.arange(0, arr[:,2].shape[0], 1)
        
        
        # # mean of data
        # mean = np.mean(time)
        
        # # standard deviation of data
        # std_dev = np.std(time)
        
        # # package return values
        # return_arr[0] = mean+std_dev
        # return_arr[1] = mean
        # return_arr[2] = std_dev
        
        
        # calculate linear time fit of detector array
        coeffs = np.polyfit(index_values, det_time_arr, 1)
        
        # calculate difference between fit timestamp and actual timestamp
        difference = arr[:,2] - (coeffs[0]*index_values + coeffs[1])
        
        
        return coeffs, difference

    E0 = 0.662  # MeV
    dE0 = 3E-5  # MeV
    Me = 0.51099895000  # MeV
    tau = 0.001
    epsilon = 0.01
    Delimiter = ';'
    Header = 0
    Folder_Path = os.getcwd()
    ETFile0 = 'CH0 Feb08 Setup 3 A.csv'
    # ETFile1 = 'CSV1_Full_Exact_D2.csv'
    # ETFile2 = 'CSV1_Full_Exact_D3.csv'
    # ETFile3 = 'CSV1_Full_Exact_D4.csv'
    
    # ETFile0 = 'CSV1_D1.csv'
    # ETFile1 = 'CSV1_D2.csv'
    # ETFile2 = 'CSV1_D3.csv'
    # ETFile3 = 'CSV1_D4.csv'
    # Det_Pos = 'CSV 2.csv'

    print("Started!")
    CSV_Start = timer()
    # arr0, Det_Pos_arr = CSV_Extract(',', Folder_Path, Det_Pos, Det_Pos)
    arr0 = CSV_Extract(Delimiter, Folder_Path, ETFile0)
    # arr1 = CSV_Extract(Delimiter, Folder_Path, ETFile1)
    # arr2 = CSV_Extract(Delimiter, Folder_Path, ETFile2)
    # arr3 = CSV_Extract(Delimiter, Folder_Path, ETFile3)

    print("CSV Extraction Done in {} s".format(timer() - CSV_Start))
    
    # arr0_timestep = calculate_av_tstep(arr0)
    # arr1_timestep = calculate_av_tstep(arr1)
    # arr2_timestep = calculate_av_tstep(arr2)
    # arr3_timestep = calculate_av_tstep(arr3)
    
    arr0_coeffs, arr0_difference = detector_polynomial_time_fit(arr0)
    # arr1_coeffs = detector_polynomial_time_fit(arr1)
    # arr2_coeffs = detector_polynomial_time_fit(arr2)
    # arr3_coeffs = detector_polynomial_time_fit(arr3)
    
    print(arr0_coeffs)
    # print(arr1_coeffs)
    # print(arr2_coeffs)
    # print(arr3_coeffs)
    
    
    dummy_x_values_0 = np.arange(0, arr0[:,2].shape[0], 1)
    # dummy_x_values_1 = np.arange(0, arr1[:,2].shape[0], 1)
    # dummy_x_values_2 = np.arange(0, arr2[:,2].shape[0], 1)
    # dummy_x_values_3 = np.arange(0, arr3[:,2].shape[0], 1)
    
    # calculating difference^2 between timestamp and fit
    difference2 = (arr0[:,2] - (arr0_coeffs[0]*dummy_x_values_0 + arr0_coeffs[1]))
    
    
    
    fig, ax = plt.subplots()
    # ax.scatter(dummy_x_values_0, arr0[:,2], label='Det0')
    # ax.plot(dummy_x_values_1, arr1[:,2], label='Det1')
    # ax.plot(dummy_x_values_2, arr2[:,2], label='Det2')
    # ax.plot(dummy_x_values_3, arr3[:,2], label='Det3')
    
    # ax.plot(dummy_x_values_0, arr0_coeffs[0]*dummy_x_values_0**2 + arr0_coeffs[1]*dummy_x_values_0 + arr0_coeffs[2], label='Fit0', color='r')
    
    ax.plot(dummy_x_values_0, arr0_difference, label='Squared Difference')
    
    
    
    
    # ax.plot(dummy_x_values_0, (arr0[:,2]-arr0_coeffs[1]-arr0_difference)/arr0_coeffs[0], label='Squared Difference')
    
    # ax.axhline(mean, 0, time.shape[0], color='g')
    # ax.axhline(mean-std_dev, 0, time.shape[0], color='r')
    # ax.axhline(mean+std_dev, 0, time.shape[0], color='r')
    ax.set(xlabel='Detector Index', ylabel='Squared Difference of timestamp vs fit predicted timestamp')
    ax.legend()
    ax.grid()

    
    plt.show()