import numpy as np
from matplotlib import pyplot as plt

def detector_time_fit(arr, plot_fit=False, plot_difference=False):
    '''
    
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
    det_time_arr = arr[:,2]
    
    
    # calculate index values
    index_values = np.arange(0, arr[:,2].shape[0], 1)
    
    
    # calculate linear time fit of detector array
    coeffs = np.polyfit(index_values, det_time_arr, 1)
    
    # calculate difference between fit timestamp and actual timestamp
    difference = arr[:,2] - (coeffs[0]*index_values + coeffs[1])
    
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



