# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:03:20 2024

@author: alfie

This script takes a numpy array describing a series of events recorded in
multiple detectors and determines which events correspond to a photon
undergoing Compton scatter followed by photoelectric absorption.

The input array (called 'all_events') must be in this format:

    [[detector index, E, t, delta E, delta t],
     [detector index, E, t, delta E, delta t],
     [detetor index, E, t, delta E, delta t],
     ...]

    where detector index (float) is an integer describing which detector the
    event occurred in;
    E (float) is the energy deposited in the event;
    t (float) is the time at which the event occurred;
    delta E (float) is the uncertainty on the measurement of E;
    and delta t (float) is the uncertainty on the measurement of t.

The output array (called 'valid_pairs') is given in this format:

    [[E1, E2, scat. index, abs. index],
     [E1, E2, scat. index, abs. index],
     [E1, E2, scat. index, abs. index],
     ...]

    where E1 (float) is the energy deposited by the photon in Compton
    scattering;
    E2 (float) is the energy deposited by the photon in photolectric
    absorption;
    scat. index (float) is the detector index of the detector where the
    Compton scatter occurred;
    and abs. index (float) is the detector index of the detector where the
    photoelectric absorption occurred.

"""
import numpy as np

tau = 1 # coincidence window in [time units]
E0 = 2 # initial photon energy in [energy units]
# need to check with lab data team whether we're working in seconds and keV

# input_format = [[detector index, E, t, delta E, delta t], ...]
test_array = np.array([[0, 1, 2, 0.1, 0.1],
                       [1, 1, 2.5, 0.1, 0.1],
                       [1, 1, 2.6, 0.2, 0.3],
                       [0, 2, 1, 0.1, 0.2],
                       [0, 1, 2, 0.2, 0.2]])
all_events = test_array # replace this with the array from Chris' code

valid_pairs = np.empty(4) # elements will be added to this later

for i in range(len(all_events)):
    # iterate over every event in the input array

    # define the event under consideration and extract all its information
    # this will be known as "Event 1" and is the i^th event in all_events
    current_event1 = all_events[i,:]
    det_index1 = current_event1[0]
    E1 = current_event1[1]
    t1 = current_event1[2]
    delta_E1 = current_event1[3]
    delta_t1 = current_event1[4]

    # defining quantities for use in the 'tau test'
    t_max = t1 + delta_t1 + tau
    t_min = t1 - delta_t1 - tau

    events_in_window = np.array([], dtype='i')

    for j in range(i+1, len(all_events)):
        # now iterate over every event AFTER the current Event 1
        # this prevents duplicate pairs being created
        # check which ones occurred within the coincidence window of Event 1

        # define the event currently being compared to Event 1
        # this will be known as "Event 2" and is the j^th event in all_events
        # extract the time information from it
        current_event2 = all_events[j,:]
        t2 = current_event2[2]
        delta_t2 = current_event2[4]

        # tau test - is Event 2 within the coincidence window of Event 1?
        if bool(t_min <= t2 - delta_t2 and t_max >= t2 + delta_t2) is True:
            # if True, the index of Event 2 is appended to events_in_window
            events_in_window = np.append(events_in_window, j)

        # printing events_in_window here is a good check if code misbehaves

    for k in events_in_window:
        # finally, we iterate over the events which passed the tau test
        # our goal is to find pairs of events which satisfy E1 + E2 = E0

        # Event 1 is still the i^th event in all_events
        # Here we redefine Event 2 as the k^th event in events_in_window
        # We therefore only have to iterate over a subset of the original data
        # Extract the required information from Event 2 as before
        current_event2 = all_events[k,:]
        det_index2 = current_event2[0]
        E2 = current_event2[1]
        delta_E2 = current_event2[3]
        t2 = current_event2[2]
        delta_t2 = current_event2[4]

        # defining quantities for use in the 'energy test'
        E_max = E1 + delta_E1 + E2 + delta_E2
        E_min = E1 - delta_E1 + E2 - delta_E2

        # energy test - do E1 and E2 sum to E0?
        if bool(E_min <= E0 <= E_max) is True:
            # if True then the two events being considered form a valid pair
            if t1 + delta_t1 < t2 - delta_t2:
                # event 1 DEFINITELY happened BEFORE event 2
                # so det_index1 is scatterer and det_index2 is absorber
                event_pair = np.array([E1, E2, det_index1, det_index2])
                valid_pairs = np.vstack((valid_pairs, event_pair))
            if t1 - delta_t1 > t2 + delta_t2:
                # event 1 DEFINITELY happened AFTER event 2
                # so det_index2 is scatterer and det_index 1 is absorber
                event_pair = np.array([E1, E2, det_index2, det_index1])
                valid_pairs = np.vstack((valid_pairs, event_pair))
            else:
                # the events occurred too close together in time to separate
                # so we can't reliably tell which detector was the scatterer
                # this means we should chuck out this pair
                pass

print(valid_pairs)
# output_format = [[E1, E2, scatterer index, absorber index], ...]
