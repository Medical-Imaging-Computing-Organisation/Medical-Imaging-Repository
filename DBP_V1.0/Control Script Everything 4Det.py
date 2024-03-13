import os
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
# import scipy.ndimage as nd
# import pandas as pd
# from pathlib import Path
# from numba import njit
# from numba import prange
# from numba import set_num_threads

# import CSV_Multiple_Detector_File_Extraction as Ex
import CSV_Data_Extraction as Ex
import Detector_time_fit as Df
import Find_True_Coincidences_No_Time_Swap as Co
import Function1 as F1
import Func2SphericPolar as F2
import Function3 as F3
import Function4HeatmapHybridVectorized as F4
import Function5 as F5

E0 = 0.662  # MeV
dE0 = 3E-5  # MeV
Me = 0.51099895000  # MeV
tau = 0
epsilon = 0
Delimiter = ';'
Header = 0
Folder_Path = os.getcwd()
ETFile0 = 'CH0 Feb08 Setup 3 A.csv'
ETFile1 = 'CH1 Feb08 Setup 3 A.csv'
ETFile2 = 'CH2 Feb08 Setup 3 A.csv'
ETFile3 = 'CH3 Feb08 Setup 3 A.csv'
# ETFile0 = 'CSV1_D1.csv'
# ETFile1 = 'CSV1_D2.csv'
# ETFile2 = 'CSV1_D3.csv'
# ETFile3 = 'CSV1_D4.csv'
Det_Pos = 'positionsetup CSV2sa 08Feb V2.csv'
# Number_of_Files = 4
start = timer()

print("Started!")
CSV_Start = timer()
arr0, Det_Pos_arr = Ex.CSV_Extract(';', Folder_Path, Det_Pos, Det_Pos)
arr0 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile0)
arr1 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile1)
arr2 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile2)
arr3 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile3)

print("CSV Extraction Done in {} s".format(timer() - CSV_Start))

Fit_Start = timer()
arr0_coeffs, arr0_difference = Df.detector_time_fit(arr0, False, False)
arr1_coeffs, arr1_difference = Df.detector_time_fit(arr1, False, False)
arr2_coeffs, arr2_difference = Df.detector_time_fit(arr2, False, False)
arr3_coeffs, arr3_difference = Df.detector_time_fit(arr3, False, False)

print("Detector Fits Done in {} s".format(timer() - Fit_Start))


Coincidence_Start = timer()
Coincidence_Start01 = timer()
fCo01 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr1, arr0_coeffs, arr1_coeffs, arr0_difference, arr1_difference)
print("Coincidence 01 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo03 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr3, arr0_coeffs, arr3_coeffs, arr0_difference, arr3_difference)
print("Coincidence 03 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo21 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr1, arr2_coeffs, arr1_coeffs, arr2_difference, arr1_difference)
print("Coincidence 21 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo23 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr3, arr2_coeffs, arr3_coeffs, arr2_difference, arr3_difference)
print("Coincidence 23 done in {} s".format(timer()-Coincidence_Start01))






allfCo = [fCo01, fCo03, fCo21, fCo23]
print("Overall Coincidence Done in {} s".format(timer() - Coincidence_Start))
dnsy = 51
data = np.zeros((len(allfCo), dnsy, dnsy, dnsy))
zeros_counter = np.zeros((len(allfCo), dnsy, dnsy, dnsy))
for i, fCo in enumerate(allfCo):
    a = np.empty((fCo.shape[0], 4), dtype=np.float32)
    f1 = F1.compton_function(a, fCo, E0, dE0, Me)
    f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, Det_Pos_arr)
    f3 = F3.PutEmTogether(f1, f2)
    F4_Start = timer()
    h, v, d, data1, voxel_r, dnsy, lim = F4.build_voxels(dnsy, 0.4)
    max_size = 30000
    split_f3 = np.array_split(f3, (len(f3)+(max_size-1)) // max_size)
    points = np.zeros((1, 3))
    for f3 in split_f3:
        points = np.append(points,
                    F4.cones_generator(f3, 32, lim, n0=4000), axis=0)
    data[i] = F4.voxel_fit(h, v, d, points[1:], data1.shape, voxel_r)
    zeros_counter[i][np.where(data[i]==0)] = 1
    
    
# sum the zero counters
zeros_sum = zeros_counter[0]
for i in range(1, zeros_counter.shape[0]):
    zeros_sum += zeros_counter[i]

# set data where originally 0 to scaled value so they're not cut entirely in multiplication
scaling_factor = 0.2

for i in range(0, data.shape[0]):
    # find maximum value for each ith element
    data_max = np.max(data[i])
    
    data[i][np.where((data[i] == 0))] = data_max*scaling_factor


# modify data according to threshold number of zeros
# threshold_zero_count = 12

# for i in range(0, data.shape[0]):
#     data[i][np.where((zeros_sum <= threshold_zero_count) & (data[i] < 1))] = 1

    
# Basic Multiplicative Option for 16 separate grids
finaldata = data[0]
for i in range(1, data.shape[0]-1):
    finaldata *= data[i]





# Trying scatterer addition option for 4 summed grids

# added_data = np.zeros((4, dnsy, dnsy, dnsy))

# added_data[0] = data[0]
# for i in range(1,4):
#     added_data[0] += data[i]

# added_data[1] = data[4]
# for i in range(5,8):
#     added_data[1] += data[i]

# added_data[2] = data[8]
# for i in range(9,12):
#     added_data[2] += data[i]

# added_data[3] = data[12]
# for i in range(12,16):
#     added_data[3] += data[i]
    
# finaldata = added_data[0]
# for i in range(1, added_data.shape[0]-1):
#     finaldata *= added_data[i]





F5_Start = timer()
fig, ax = F5.draw(h, v, d, dnsy, finaldata, voxel_r, Det_Pos_arr, 1)
print("F5 added done in %f s" % (timer() - F5_Start))
plt.show()

