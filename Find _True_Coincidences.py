# Imports
import numpy as np
from numba import njit
from numba import prange

# Parameters (currently set to unphysical test values)
tau = 1
E0 = 6
arr0 = np.array([[0, 10, 1, 0.1, 0.1],
        [0, 10, 2, 0.1, 0.2],
        [0, 10, 2.5, 0.1, 0.1],
        [0, 12, 2.7, 0.2, 0.1],
        [0, 10, 3, 0.3, 0.1],
        [0, 8, 4.5, 0.5, 0.2],
        [0, 10, 5, 0.2, 0.2],
        [0, 11, 5.2, 0.2, 0.1],
        [0, 12, 5.3, 0.1, 0.4],
        [0, 9, 5.6, 0.3, 0.1],
        [0, 7, 5.8, 0.1, 0.1],
        [0, 3, 5.9, 0.2, 0.1],
        [0, 4, 6.1, 0.4, 0.1],
        [0, 6, 6.3, 0.2, 0.1],
        [0, 10, 6.9, 0.1, 0.1],
        [0, 11, 7.1, 0.1, 0.1],
        [0, 12, 7.4, 0.1, 0.1],
        [0, 13, 7.5, 0.2, 0.2],
        [0, 12, 7.8, 0.1, 0.1],
        [0, 14, 8, 0.2, 0.2],
        [0, 15, 8.2, 0.1, 0.1],
        [0, 16, 8.5, 0.2, 0.3],
        [0, 17, 8.8, 0.3, 0.1],
        [0, 13, 9.1, 0.1, 0.1],
        [0, 14, 9.3, 0.2, 0.2],
        [0, 15, 9.7, 0.1, 0.1],
        [0, 16, 10, 0.1, 0.1]
        ])

arr1 = np.array([[1, 12, 1, 0.1, 0.2],
        [1, 11, 1.1, 0.1, 0.1],
        [1, 13, 1.8, 0.2, 0.1],
        [1, 9, 2.6, 0.1, 0.2],
        [1, 10, 2.9, 0.2, 0.1],
        [1, 15, 3.2, 0.4, 0.1],
        [1, 13, 3.4, 0.2, 0.2],
        [1, 16, 4, 0.1, 0.4],
        [1, 12, 4.1, 0.1, 0.1],
        [1, 11, 4.7, 0.2, 0.3],
        [1, 13, 5, 0.1, 0.1],
        [1, 14, 5.2, 0.2, 0.2],
        [1, 13, 5.4, 0.1, 0.1],
        [1, 15, 5.6, 0.2, 0.2],
        [1, 11, 5.9, 0.1, 0.1],
        [1, 13, 6.0, 0.2, 0.3],
        [1, 15, 7.1, 0.1, 0.2],
        [1, 8, 7.2, 0.2, 0.2],
        [1, 9, 7.3, 0.1, 0.1],
        [1, 10, 7.5, 0.1, 0.1],
        [1, 11, 7.8, 0.2, 0.2],
        [1, 12, 8.0, 0.1, 0.1],
        [1, 13, 8.3, 0.4, 0.2],
        [1, 14, 8.4, 0.1, 0.1],
        [1, 15, 8.8, 0.1, 0.1],
        [1, 11, 8.9, 0.2, 0.2],
        [1, 12, 9.1, 0.3, 0.2],
        [1, 8, 9.4, 0.2, 0.1],
        [1, 10, 10, 0.1, 0.1]
        ])

arr2 = np.array([[2, 13, 1, 0.1, 0.1],
        [2, 12, 1.2, 0.1, 0.2],
        [2, 10, 2.4, 0.1, 0.1],
        [2, 13, 2.9, 0.2, 0.1],
        [2, 11, 3.2, 0.3, 0.1],
        [2, 9, 4.1, 0.5, 0.2],
        [2, 8, 4.5, 0.2, 0.2],
        [2, 13, 5.1, 0.2, 0.1],
        [2, 12, 5.4, 0.1, 0.4],
        [2, 8, 5.5, 0.3, 0.1],
        [2, 7, 5.6, 0.1, 0.1],
        [2, 2, 6.1, 0.2, 0.1],
        [2, 8, 6.2, 0.4, 0.1],
        [2, 4, 6.4, 0.2, 0.1],
        [2, 9, 7.2, 0.1, 0.1],
        [2, 12, 7.3, 0.1, 0.1],
        [2, 14, 7.6, 0.1, 0.1],
        [2, 15, 7.7, 0.2, 0.2],
        [2, 11, 7.8, 0.1, 0.1],
        [2, 10, 8.1, 0.2, 0.2],
        [2, 12, 8.2, 0.1, 0.1],
        [2, 13, 8.4, 0.2, 0.3],
        [2, 16, 8.6, 0.3, 0.1],
        [2, 11, 9, 0.1, 0.1],
        [2, 15, 9.2, 0.2, 0.2],
        [2, 15, 9.5, 0.1, 0.1],
        [2, 16, 10, 0.1, 0.1]
        ])


# pairing array needs to be of the form below, where detectors 0,1 are scatterers and 2,3 are absorbers
# pair_arr = np.array([ [0, 2], [0, 3], [1, 2], [1, 3] ])



def find_true_coincidences(tau, E0, pairing_arr, arr0, arr1, arr2=None, arr3=None, arr4=None, arr5=None, arr6=None, arr7=None):
    '''
    For events observed between two to eight detectors, this function finds
    which events occurred within a given coincidence window of each other AND
    could correspond to a single Compton scatter followed by a photoelectric
    absorption using energy conservation rules. The function considers pairs
    of detectors that are pre-specified to prevent a factorial time complexity
    with increasing detectors.
    
    Required Imports
    ----------
    import numpy as np
    from numba import njit
    from numba import prange

    Parameters
    ----------
    tau : float
        Chosen coincidence window. Must be given in the same time units as the
        timestamps of the events in the input arrays.
    E0 : float
        Initial photon energy (=662 keV in most cases). Must be given in the
        same units as the energies of the events in the input arrays.
    pairing_arr: array
        Array that contains the pairs of detectors to have coincidences investigated.
    arr0 : array
        Array of events which were observed in the first detector.
    arr1 : array
        Array of events which were observed in the second detector.
    arr2-7 : arrays (optional)
        Additional arrays giving events observed in more detectors.

    Returns
    -------
    None.

    '''
    
    # define tstep array, containing both the ave_tstep and array itself for future use
    ave_tstep_arr = np.ndarray((8,2), dtype=np.ndarray)
    
    ave_tstep_arr[0][0] = (arr0[-1, 2] - arr0[0, 2]) / arr0.shape[0]
    ave_tstep_arr[0][1] = arr0
    ave_tstep_arr[1][0] = (arr1[-1, 2] - arr1[0, 2]) / arr1.shape[0]
    ave_tstep_arr[1][1] = arr1
    
    if arr2 is not None:
        ave_tstep_arr[2][0] = (arr2[-1, 2] - arr2[0, 2]) / arr2.shape[0]
        ave_tstep_arr[2][1] = arr2
    if arr3 is not None:
        ave_tstep_arr[3][0] = (arr3[-1, 2] - arr3[0, 2]) / arr3.shape[0]
        ave_tstep_arr[3][1] = arr3
    if arr4 is not None:
        ave_tstep_arr[4][0] = (arr4[-1, 2] - arr4[0, 2]) / arr4.shape[0]
        ave_tstep_arr[4][1] = arr4
    if arr5 is not None:
        ave_tstep_arr[5][0] = (arr5[-1, 2] - arr5[0, 2]) / arr5.shape[0]
        ave_tstep_arr[5][1] = arr5
    if arr6 is not None:
        ave_tstep_arr[6][0] = (arr6[-1, 2] - arr6[0, 2]) / arr6.shape[0]
        ave_tstep_arr[6][1] = arr6
    if arr7 is not None:
        ave_tstep_arr[7][0] = (arr7[-1, 2] - arr7[0, 2]) / arr7.shape[0]
        ave_tstep_arr[7][1] = arr7
        
    # define pairing info array, containing all the information about the detector pairing
    pairing_info = np.ndarray((pairing_arr.shape[0], 5), dtype=np.ndarray)
    
    # iterate through each detector pairing and extract all required information from them
    for k in range(0, pairing_arr.shape[0]):
        pairing_info[k][0] = ave_tstep_arr[ int(pairing_arr[k][0]) ][0]
        pairing_info[k][1] = ave_tstep_arr[ int(pairing_arr[k][1]) ][0]
        pairing_info[k][2] = int(5 * tau / pairing_info[k][1])
        pairing_info[k][3] = ave_tstep_arr[ int(pairing_arr[k][0]) ][1]
        pairing_info[k][4] = ave_tstep_arr[ int(pairing_arr[k][1]) ][1]
    
   
    
    
    
    
    
    
    
    # internal function for finding the coincidences between a detector pair
    @njit(parallel=True)
    def find_time_coincidences(tau, test_window_size, arr0, arr1, temp_arr, ave_tstep0, ave_tstep1, arr0_index, arr1_index):
        
        tstep_ratio_01 = ave_tstep0 / ave_tstep1
        
        # extract time information from arr0 and arr1
        t0 = arr0[:, 2]
        # t1 = arr1[:, 2]
        delta_t0 = arr0[:, 4]
        delta_t1 = arr1[:, 4]
        
        # calculate limits of coincidence window (tau) for each event in arr0
        t_max = t0 + tau + delta_t0
        t_min = t0 - tau - delta_t0
        
        # define for use later
        package = np.empty((test_window_size, 6))
        column0 = np.empty(test_window_size)
        column1 = np.empty(test_window_size)
        column2 = np.empty(test_window_size)
        column3 = np.empty(test_window_size)

        for i in prange(0, arr0.shape[0]):

            # define corresponding index j in arr2        
            j = tstep_ratio_01 * i

            # calculate limits of the testing window for the i^th event
            test_max = int(j + 0.5 * test_window_size)
            if test_max > min(arr0.shape[0], arr1.shape[0]):
                test_max = min(arr0.shape[0], arr1.shape[0])
            test_min = int(j - 0.5 * test_window_size)
            if test_min < 0:
                test_min = 0

            test_window = arr1[test_min : test_max]

            # check which elements in test_window are between limits of tau
            coin = np.where( (t_min[i] <= test_window[2] - delta_t1[i]) & (t_max[i] >= test_window[2] + delta_t1[i]) )
            coinc_events = test_window[coin]
            print(coinc_events)

            # energy of arr0 event
            column0[:coinc_events.shape[0]] = arr0[i, 1]
            column0[coinc_events.shape[0]:] = 0
            
            # energy of arr1 events
            column1[:coinc_events.shape[0]] = coinc_events[:, 1]
            column1[coinc_events.shape[0]:] = 0
            
            # uncertainty on energy of arr0 event
            column2[:coinc_events.shape[0]] = arr0[i, 3]
            column2[coinc_events.shape[0]:] = 0
            
            # uncertainties on energies of arr1 events
            column3[:coinc_events.shape[0]] = coinc_events[:, 3]
            column3[coinc_events.shape[0]:] = 0
            
            # package up the columns
            package[:, 0] = column0
            package[:, 1] = column1
            package[:, 2] = column2
            package[:, 3] = column3
            package[:, 4] = arr0_index
            package[:, 5] = arr1_index

            temp_arr[i] = package
       
        return temp_arr
    
    # define an array to contain coincident events for all specified detector pairings
    return_arr = np.empty((0, 6), dtype=np.float32)
        
        
    # iterate through each detector pairing and find their coincidences - dynamic so cannot be numba'd
    for j in range(0, pairing_arr.shape[0]):
        
        # define an array to contain the coincident events
        temp_arr = np.ndarray((arr0.shape[0], pairing_info[j][2], 4), dtype=np.float32) 
            
        x_j = find_time_coincidences(tau, pairing_info[j][2], pairing_info[j][3], 
                                        pairing_info[j][4], temp_arr, pairing_info[j][1], 
                                        pairing_info[j][2], pairing_arr[j][0], pairing_arr[j][1])
        
        # remove zeros
        x_j = x_j[~np.all(x_j == 0, axis=2)]
        return_arr = np.vstack((return_arr, x_j))
    
    
#     # determine the region in arr1 to examine for coincidences
#     test_window_size_0 = int(5 * tau / ave_tstep1) # in dimensions of indices
    
    
#     x = find_time_coincidences(tau, test_window_size_0, arr0, arr1, temp_arr, ave_tstep0, ave_tstep1)
#     # get rid of the zeros
#     x = x[~np.all(x == 0, axis=2)]
#     return x

    return return_arr

# print(find_true_coincidences(tau, E0, arr0, arr1))
