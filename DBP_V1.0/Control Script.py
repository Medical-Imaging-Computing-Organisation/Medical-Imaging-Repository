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
ETFile0 = 'CH0 Feb22 Setup 7 A.csv'
ETFile1 = 'CH1 Feb22 Setup 7 A.csv'
ETFile2 = 'CH2 Feb22 Setup 7 A.csv'
ETFile3 = 'CH3 Feb22 Setup 7 A.csv'
ETFile4 = 'CH4 Feb22 Setup 7 A.csv'
ETFile5 = 'CH5 Feb22 Setup 7 A.csv'
ETFile6 = 'CH6 Feb22 Setup 7 A.csv'
ETFile7 = 'CH7 Feb22 Setup 7 A.csv'
Det_Pos = 'positionsetup CSV2 S7 22Feb A.csv'
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
array_reducing_factor = 1

fCo04 = fCo04[:int(fCo04.shape[0]/array_reducing_factor)]
fCo05 = fCo05[:int(fCo05.shape[0]/array_reducing_factor)]
fCo06 = fCo06[:int(fCo06.shape[0]/array_reducing_factor)]
fCo07 = fCo07[:int(fCo07.shape[0]/array_reducing_factor)]
fCo14 = fCo14[:int(fCo14.shape[0]/array_reducing_factor)]
fCo15 = fCo15[:int(fCo15.shape[0]/array_reducing_factor)]
fCo16 = fCo16[:int(fCo16.shape[0]/array_reducing_factor)]
fCo17 = fCo17[:int(fCo17.shape[0]/array_reducing_factor)]
fCo24 = fCo24[:int(fCo24.shape[0]/array_reducing_factor)]
fCo25 = fCo25[:int(fCo25.shape[0]/array_reducing_factor)]
fCo26 = fCo26[:int(fCo26.shape[0]/array_reducing_factor)]
fCo27 = fCo27[:int(fCo27.shape[0]/array_reducing_factor)]
fCo34 = fCo34[:int(fCo34.shape[0]/array_reducing_factor)]
fCo35 = fCo35[:int(fCo35.shape[0]/array_reducing_factor)]
fCo36 = fCo36[:int(fCo36.shape[0]/array_reducing_factor)]
fCo37 = fCo37[:int(fCo37.shape[0]/array_reducing_factor)]





# fCo = np.vstack((fCo1, fCo2, fCo3, fCo4, fCo5, fCo6))
# fCo = np.vstack((fCo04, fCo05, fCo06, fCo14, fCo15, fCo16, fCo24, fCo25, fCo26, fCo34, fCo35, fCo36))
fCo = np.vstack((fCo04, fCo05, fCo06, fCo07, fCo14, fCo15, fCo16, fCo17, fCo24, fCo25, fCo26, fCo27, fCo34, fCo35, fCo36, fCo37))
print("Overall Coincidence Done in {} s".format(timer() - Coincidence_Start))

# fCo = fCo[0:1]

F1_Start = timer()
a = np.empty((fCo.shape[0], 4), dtype=np.float32)
f1 = F1.compton_function(a, fCo, E0, dE0, Me)
print("F1 Done in {} s".format(timer() - F1_Start))

F2_Start = timer()
f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, Det_Pos_arr)
print("F2 Done in {} s".format(timer() - F2_Start))

F3_Start = timer()
f3 = F3.PutEmTogether(f1, f2)
print("F3 Done in {} s".format(timer() - F3_Start))

F4_Start = timer()
h, v, d, data, voxel_r, dnsy, lim = F4.build_voxels(51, 0.4)
max_size = 15000
split_f3 = np.array_split(f3, (len(f3)+(max_size-1)) // max_size)
points = np.zeros((1, 3))
p = 32
n0 = 4000
for f3 in split_f3:
    points = np.append(points,
                F4.cones_generator(f3, p, lim, n0=n0), axis=0)
    print('%i chunk done' % f3.shape[0])
data = F4.voxel_fit(h, v, d, points[1:], data.shape, voxel_r)
print("F4 Done in {} s".format(timer() - F4_Start))

F5_Start = timer()
fig, ax = F5.draw(h, v, d, dnsy, data, voxel_r, Det_Pos_arr, 1)
print("F5 done in %f s" % (timer() - F5_Start))
runLabel = (f"Tau %.4f, Epsilon %.4fMeV, Voxel Density %i, Limits %icm, Point limits %i, Point Density %i/m$^2$"
            % (tau, epsilon, dnsy, 100*lim, p, n0))
ax[4].text(x=-12*lim, y=-2*lim, s=runLabel, fontsize=9)
plt.show()

