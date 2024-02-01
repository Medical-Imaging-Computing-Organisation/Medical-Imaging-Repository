# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:56:20 2024

@author: alfie
"""

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

def find_true_coincidences(tau, E0, arr0, arr1, arr2=None, arr3=None, arr4=None, arr5=None, arr6=None, arr7=None):
    '''
    For events observed in between two and eight detectors, this function finds
    which events occurred within a given coincidence window of each other AND
    could correspond to a single Compton scatter followed by a photoelectric
    absorption using energy conservation rules.
    
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
        same units as the energies of the events in the input arrays
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
    ave_tstep0 = (arr0[-1, 2] - arr0[0, 2]) / arr0.shape[0]
    ave_tstep1 = (arr1[-1, 2] - arr1[0, 2]) / arr1.shape[0]
    '''
    ave_tstep2 = (arr2[-1, 2] - arr2[0, 2]) / arr2.shape[0]
    ave_tstep3 = (arr3[-1, 2] - arr3[0, 2]) / arr3.shape[0]
    ave_tstep4 = (arr4[-1, 2] - arr4[0, 2]) / arr4.shape[0]
    ave_tstep5 = (arr5[-1, 2] - arr5[0, 2]) / arr5.shape[0]
    ave_tstep6 = (arr6[-1, 2] - arr6[0, 2]) / arr6.shape[0]
    ave_tstep7 = (arr7[-1, 2] - arr7[0, 2]) / arr7.shape[0]
    '''

    # determine the region in arr1 to examine for coincidences
    test_window_size = int(5 * tau / ave_tstep1) # in dimensions of indices
    print(test_window_size)
    # define an array to contain the coincident events
    temp_arr = np.ndarray((arr0.shape[0], test_window_size, 4), dtype=np.float32) 
    
    @njit(parallel=True)
    def find_time_coincidences(tau, arr0, arr1, temp_arr, ave_tstep0, ave_tstep1):
        
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
        package = np.empty((test_window_size, 4))
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

            temp_arr[i] = package
       
        return temp_arr
    
    x = find_time_coincidences(tau, arr0, arr1, temp_arr, ave_tstep0, ave_tstep1)
    # get rid of the zeros
    x = x[~np.all(x == 0, axis=2)]
    return x

print(find_true_coincidences(tau, E0, arr0, arr1))