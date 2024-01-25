# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:16:16 2024

@author: alfie
"""

def find_coincidences(tau, arr1, arr2):
    '''
    For events observed in two detectors, this function finds which events
    occurred within a given coincidence window of each other.

    Parameters
    ----------
    tau : float
        Chosen coincidence window. Must be given in the same time units as the
        timestamps of the events.
    arr1 : array
        Array of events which were observed in the first detector.
    arr2 : array
        Array of events which were observed in the second detector.

    Both arr1 and arr2 should use the following format:
        [[detector index, energy, time, delta E, delta t], ...]

    Returns
    -------
    output_arr: an array giving time information on all coincident pairs.
    Format is [[t1, t2, delta_t1, delta_t2]] where t1 is the time of an event
    observed in the first detector, t2 is the time of a coincident event
    observed in the second detector, and (delta_t1, delta_t2) are the
    uncertainties on these time measurements.

    '''
    # Imports
    import numpy as np

    # calculate the average increase in t between each consecutive event in arr2
    ave_tstep2 = (arr2[-1, 2] - arr2[0, 2]) / arr2.shape[0]
    # determine the region to examine for coincidences (time_width = 1.5 * tau)
    test_window_size = int(1.5 * tau / ave_tstep2) # in dimensions of indices

    output_arr = np.empty(4)

    for i in range(test_window_size, min(arr1.shape[0], arr2.shape[0]) - test_window_size):
        # iterate over every event in arr1
        # exclude events near the start and end to avoid having to make a comparison every loop
        # also exclude events beyond the length of arr2 (if arr2 < arr1)

        # extract time information from the i^th event
        t1 = arr1[i, 2]
        delta_t1 = arr1[i, 4]

        # calculate limits of the coincidence window for the i^th event
        # these also need to be arrays! This is done below for now
        t_max = t1 + delta_t1 + tau
        t_min = t1 - delta_t1 - tau

        # calculate limits of the testing window for the i^th event
        test_max = int(i + 0.5 * test_window_size)
        test_min = int(i - 0.5 * test_window_size)

        # fill arrays with the limit values
        t_max_arr = np.full(test_max - test_min, t_max)
        t_min_arr = np.full(test_max - test_min, t_min)

        # slice arr2 between the test window limits
        test_window = arr2[test_min : test_max]
        # extract the time info of all events in the test window
        t2_arr = test_window[:, 2]
        delta_t2_arr = test_window[:, 4]

        # find all indices in t2_arr where t2 falls within the coincidence window
        coin = np.where((t_min_arr <= t2_arr - delta_t2_arr) & (t_max_arr >= t2_arr + delta_t2_arr))
        # retrieve the events associated with those indices
        coinc_events = test_window[coin]

        # fill arrays with the values t1 and delta_t1, length = no. of coincidences
        t1_arr = np.full(coinc_events.shape[0], t1)
        delta_t1_arr = np.full(coinc_events.shape[0], delta_t1)

        # package up the info we want about each coincident pair of events
        pair_info = np.empty((coinc_events.shape[0], 4))
        pair_info[:,0] = t1_arr # time of event 1
        pair_info[:,1] = coinc_events[:,2] # time of event 2
        pair_info[:,2] = delta_t1_arr # uncertainty on time of event 1
        pair_info[:,3] = coinc_events[:,4] # uncertainty on time of event 2

        # stack this set of coincident pairs onto the end of output_arr
        output_arr = np.vstack((output_arr, pair_info))

    return output_arr[1:]

tau = 1
arr1 = np.array([[0, 10, 1, 0.1, 0.1],
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
arr2 = np.array([[1, 12, 1, 0.1, 0.2],
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

print(find_coincidences(tau, arr1, arr2))