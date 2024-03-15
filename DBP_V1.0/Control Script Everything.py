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

# import CSV_Multiple_Detector_File_Extraction as ExH0 Feb29 Setup 8 A
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
ETFile0 = 'CH0 Feb29 Setup 8 A.csv'
ETFile1 = 'CH1 Feb29 Setup 8 A.csv'
ETFile2 = 'CH2 Feb29 Setup 8 A.csv'
ETFile3 = 'CH3 Feb29 Setup 8 A.csv'
ETFile4 = 'CH4 Feb29 Setup 8 A.csv'
ETFile5 = 'CH5 Feb29 Setup 8 A.csv'
ETFile6 = 'CH6 Feb29 Setup 8 A.csv'
ETFile7 = 'CH7 Feb29 Setup 8 A.csv'
# ETFile0 = 'CSV1_D1.csv'
# ETFile1 = 'CSV1_D2.csv'
# ETFile2 = 'CSV1_D3.csv'
# ETFile3 = 'CSV1_D4.csv'
Det_Pos = 'positionsetup CSV2 S8 29Feb A.csv'
# Number_of_Files = 4
start = timer()

print("Started!")
CSV_Start = timer()
_, Det_Pos_arr = Ex.CSV_Extract(';', Folder_Path, Det_Pos, Det_Pos)
arr0 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile0)
arr1 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile1)
arr2 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile2)
arr3 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile3)
arr4 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile4)
arr5 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile5)
arr6 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile6)
arr7 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile7)

print("CSV Extraction Done in {} s".format(timer() - CSV_Start))

Fit_Start = timer()
arr0_coeffs, arr0_difference = Df.detector_time_fit(arr0, False, False)
arr1_coeffs, arr1_difference = Df.detector_time_fit(arr1, False, False)
arr2_coeffs, arr2_difference = Df.detector_time_fit(arr2, False, False)
arr3_coeffs, arr3_difference = Df.detector_time_fit(arr3, False, False)
arr4_coeffs, arr4_difference = Df.detector_time_fit(arr4, False, False)
arr5_coeffs, arr5_difference = Df.detector_time_fit(arr5, False, False)
arr6_coeffs, arr6_difference = Df.detector_time_fit(arr6, False, False)
arr7_coeffs, arr7_difference = Df.detector_time_fit(arr7, False, False)

print("Detector Fits Done in {} s".format(timer() - Fit_Start))


Coincidence_Start = timer()
Coincidence_Start01 = timer()
fCo04 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr4, arr0_coeffs, arr4_coeffs, arr0_difference, arr4_difference)
print("Coincidence 04 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo05 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr5, arr0_coeffs, arr5_coeffs, arr0_difference, arr5_difference)
print("Coincidence 05 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo06 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr6, arr0_coeffs, arr6_coeffs, arr0_difference, arr6_difference)
print("Coincidence 06 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo07 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr7, arr0_coeffs, arr7_coeffs, arr0_difference, arr7_difference)
print("Coincidence 07 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo14 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr4, arr1_coeffs, arr4_coeffs, arr1_difference, arr4_difference)
print("Coincidence 14 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo15 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr5, arr1_coeffs, arr5_coeffs, arr1_difference, arr5_difference)
print("Coincidence 15 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo16 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr6, arr1_coeffs, arr6_coeffs, arr1_difference, arr6_difference)
print("Coincidence 16 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo17 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr7, arr1_coeffs, arr7_coeffs, arr1_difference, arr7_difference)
print("Coincidence 17 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo24 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr4, arr2_coeffs, arr4_coeffs, arr2_difference, arr4_difference)
print("Coincidence 24 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo25 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr5, arr2_coeffs, arr5_coeffs, arr2_difference, arr5_difference)
print("Coincidence 25 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo26 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr6, arr2_coeffs, arr6_coeffs, arr2_difference, arr6_difference)
print("Coincidence 26 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo27 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr7, arr2_coeffs, arr7_coeffs, arr2_difference, arr7_difference)
print("Coincidence 27 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo34 = Co.find_true_coincidences(tau, epsilon, E0, arr3, arr4, arr3_coeffs, arr4_coeffs, arr3_difference, arr4_difference)
print("Coincidence 34 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo35 = Co.find_true_coincidences(tau, epsilon, E0, arr3, arr5, arr3_coeffs, arr5_coeffs, arr3_difference, arr5_difference)
print("Coincidence 35 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo36 = Co.find_true_coincidences(tau, epsilon, E0, arr3, arr6, arr3_coeffs, arr6_coeffs, arr3_difference, arr6_difference)
print("Coincidence 36 done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start01 = timer()
fCo37 = Co.find_true_coincidences(tau, epsilon, E0, arr3, arr7, arr3_coeffs, arr7_coeffs, arr3_difference, arr7_difference)
print("Coincidence 37 done in {} s".format(timer()-Coincidence_Start01))


# Slicing arrays due to data size
# array_reducing_factor = 1
#
# fCo04 = fCo04[:int(fCo04.shape[0]/array_reducing_factor)]
# fCo05 = fCo05[:int(fCo05.shape[0]/array_reducing_factor)]
# fCo06 = fCo06[:int(fCo06.shape[0]/array_reducing_factor)]
# fCo07 = fCo07[:int(fCo07.shape[0]/array_reducing_factor)]
# fCo14 = fCo14[:int(fCo14.shape[0]/array_reducing_factor)]
# fCo15 = fCo15[:int(fCo15.shape[0]/array_reducing_factor)]
# fCo16 = fCo16[:int(fCo16.shape[0]/array_reducing_factor)]
# fCo17 = fCo17[:int(fCo17.shape[0]/array_reducing_factor)]
# fCo24 = fCo24[:int(fCo24.shape[0]/array_reducing_factor)]
# fCo25 = fCo25[:int(fCo25.shape[0]/array_reducing_factor)]
# fCo26 = fCo26[:int(fCo26.shape[0]/array_reducing_factor)]
# fCo27 = fCo27[:int(fCo27.shape[0]/array_reducing_factor)]
# fCo34 = fCo34[:int(fCo34.shape[0]/array_reducing_factor)]
# fCo35 = fCo35[:int(fCo35.shape[0]/array_reducing_factor)]
# fCo36 = fCo36[:int(fCo36.shape[0]/array_reducing_factor)]
# fCo37 = fCo37[:int(fCo37.shape[0]/array_reducing_factor)]





# fCo = np.vstack((fCo1, fCo2, fCo3, fCo4, fCo5, fCo6))
# fCo = np.vstack((fCo04, fCo05, fCo06, fCo14, fCo15, fCo16, fCo24, fCo25, fCo26, fCo34, fCo35, fCo36))
allfCo = [fCo04, fCo05, fCo06, fCo07, fCo14, fCo15, fCo16, fCo17, fCo24, fCo25, fCo26, fCo27, fCo34, fCo35, fCo36, fCo37]
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
    if f3.shape[0] > max_size:
        split_f3 = np.array_split(f3, (len(f3)+(max_size-1)) // max_size)
    else:
        split_f3 = [f3]
    points = np.zeros((1, 3))
    p = 32
    n0 = 4000
    for f3 in split_f3:
        points = np.append(points, F4.cones_generator(f3, p, lim, n0), axis=0)
    data[i] = F4.voxel_fit(h, v, d, points[1:], data1.shape, voxel_r)
    #zeros_counter[i][np.where(data[i]==0)] = 1
    
    
# sum the zero counters
#zeros_sum = zeros_counter[0]
#for i in range(1, zeros_counter.shape[0]):
    #zeros_sum += zeros_counter[i]

# set data where originally 0 to scaled value so they're not cut entirely in multiplication
#scaling_factor = 0.11

#for i in range(0, data.shape[0]):
    # find maximum value for each ith element
    #data_max = np.max(data[i])
    
    #data[i][np.where((data[i] == 0))] = data_max*scaling_factor


# modify data according to threshold number of zeros
# threshold_zero_count = 12

# for i in range(0, data.shape[0]):
#     data[i][np.where((zeros_sum <= threshold_zero_count) & (data[i] < 1))] = 1


# additive constant
additive_constant = 1 # change as needed
for i in range(0, data.shape[0]):
    data[i] = data[i] + additive_constant

    
# Basic Multiplicative Option for 16 separate grids
finaldata = data[0]
for i in range(1, data.shape[0]-1):
    finaldata *= data[i]





# Trying scatterer addition option for 4 summed grids

# added_data = np.zeros((4, dnsy, dnsy, dnsy))
# np.random.shuffle(data)
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
runLabel = (f"Tau %.4f, Epsilon %.4fMeV, Voxel Density %i, Limits %icm, Point limits %i, Point Density %i/m$^2$"
            % (tau, epsilon, dnsy, 100*lim, p, n0))
ax[4].text(x=-12*lim, y=-2*lim, s=runLabel, fontsize=9)
plt.show()

