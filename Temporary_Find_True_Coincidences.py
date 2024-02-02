# Imports
import numpy as np
from numba import njit
from numba import prange
import pandas as pd

# Parameters (remember to change based on units of your data)
tau = 0.001 # time coincidence window
epsilon = 0.01 # energy coincidence window
E0 = 0.662 # initial photon energy

def find_true_coincidences(tau, epsilon, E0, arr0, arr1):
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
    
    
    # determine the region in arr1 to examine for coincidences
    test_window_size = int(5 * tau / ave_tstep1) # in dimensions of indices

    # define an array to contain the coincident events
    temp_arr = np.ndarray((arr0.shape[0], test_window_size, 4), dtype=np.float32) 
    
    @njit(parallel=True)
    def two_array_tester(tau, epsilon, E0, arrA, arrB, temp_arr, ave_tstepA, ave_tstepB):
        '''
        Takes events observed in two detectors (A and B) and finds pairs which
        pass the tau test and the E0 test

        Parameters
        ----------
        tau : TYPE
            DESCRIPTION.
        arrA : TYPE
            DESCRIPTION.
        arrB : TYPE
            DESCRIPTION.
        temp_arr : TYPE
            DESCRIPTION.
        ave_tstepA : TYPE
            DESCRIPTION.
        ave_tstepB : TYPE
            DESCRIPTION.

        Returns
        -------
        temp_arr : TYPE
            DESCRIPTION.

        '''
        tstep_ratio_AB = ave_tstepA / ave_tstepB
        
        # extract time information from arrA and arrB
        tA = arrA[:, 2]
        #tB = arrB[:, 2]
        delta_tA = arrA[:, 4]
        delta_tB = arrB[:, 4]
        
        # calculate limits of time coincidence window for each event in arrA
        t_max = tA + tau + delta_tA
        t_min = tA - tau - delta_tA
        
        # extract energy information from arrA
        EA = arrA[:, 1]
        #EB = arrB[:, 1]
        delta_EA = arrA[:, 3]
        #delta_EB = arrB[:, 3]
        
        # define for use later
        package = np.empty((test_window_size, 4))
        column0 = np.empty(test_window_size)
        column1 = np.empty(test_window_size)
        column2 = np.empty(test_window_size)
        column3 = np.empty(test_window_size)

        for i in range(0, arrA.shape[0]):

            # define corresponding index j in arrB    
            j = tstep_ratio_AB * i

            # calculate limits of the testing window for the i^th event in arrA
            test_max = int(j + 0.5 * test_window_size)
            if test_max > arrB.shape[0]:
                test_max = arrB.shape[0]
            test_min = int(j - 0.5 * test_window_size)
            if test_min < 0:
                test_min = 0
            #print(test_min, j, test_max)

            test_window = arrB[test_min : test_max]

            # check which elements in test_window are between limits of tau
            tau_test = np.where( (t_min[i] <= test_window[:,2] - delta_tB[i]) & (t_max[i] >= test_window[:,2] + delta_tB[i]) )
            coinc_events = test_window[tau_test]

            # extract energy information from events which passed tau test
            EB = coinc_events[:,1]
            delta_EB = coinc_events[:,3]
            
            # apply energy conservation test to events which passed tau test
            energy_test = np.where( (EA[i] + delta_EA[i] + EB + delta_EB >= E0 - epsilon) & (E0 + epsilon >= EA[i] - delta_EA[i] + EB - delta_EB) )
            valid_events = coinc_events[energy_test]

            #TODO: make sure events are time ordered (scatter then absorb)
            
            #events_before = valid_events[np.where(valid_events[:,2] < tA[i])]
            #events_after = valid_events[np.where(valid_events[:,2] > tA[i])]

            #TODO: add a way to get rid of pairs of events with E2 = 0

            # energy of arr0 event
            column0[:valid_events.shape[0]] = arrA[i, 1]
            column0[valid_events.shape[0]:] = 0
            
            # energy of scatter event
            #column0[:events_before.shape[0]] = events_before[:, 1]
            #column0[events_before.shape[0]:valid_events.shape[0]] = arrA[i, 1]
            #column0[valid_events.shape[0]:] = 0

            # energy of arr1 events
            column1[:valid_events.shape[0]] = valid_events[:, 1]
            column1[valid_events.shape[0]:] = 0
            
            # energy of absorption event
            #column1[:events_before.shape[0]] = arrA[i, 1]
            #column1[events_before.shape[0]:valid_events.shape[0]] = events_after[:, 1]
            #column1[valid_events.shape[0]:] = 0

            # uncertainty on energy of arr0 event
            column2[:valid_events.shape[0]] = arrA[i, 3]
            column2[valid_events.shape[0]:] = 0

            # uncertainties on energies of arr1 events
            column3[:valid_events.shape[0]] = valid_events[:, 3]
            column3[valid_events.shape[0]:] = 0

            # package up the columns
            package[:, 0] = column0
            package[:, 1] = column1
            package[:, 2] = column2
            package[:, 3] = column3

            temp_arr[i] = package

        return temp_arr

    x = two_array_tester(tau, epsilon, E0, arr0, arr1, temp_arr, ave_tstep0, ave_tstep1)
    # get rid of the zeros
    x = x[~np.all(x == 0, axis=2)]
    return x


# Input format:
# Call this function multiple times, with arr0 and arr1, then vstack in the control document
