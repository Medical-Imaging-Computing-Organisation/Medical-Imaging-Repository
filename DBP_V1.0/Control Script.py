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
import Find_True_Coincidences as Co
import Function1 as F1
import Function2 as F2
import Function3 as F3
import Function4HeatmapHybridVectorized as F4
import Function5 as F5

E0 = 0.662  # MeV
dE0 = 3E-5  # MeV
Me = 0.51099895000  # MeV
tau = 0.001  # *10E9
epsilon = 0.01
Delimiter = ','
Header = 0
Folder_Path = os.getcwd()
# ETFile0 = 'CH0 01Feb Setup 2 A.csv'
# ETFile1 = 'CH1 01Feb Setup 2 B.csv'
# ETFile2 = 'CH2 01Feb Setup 2 A.csv'
# ETFile3 = 'CH3 01Feb Setup 2 B.csv'
ETFile0 = 'CSV1_D1.csv'
ETFile1 = 'CSV1_D2.csv'
ETFile2 = 'CSV1_D3.csv'
ETFile3 = 'CSV1_D4.csv'
Det_Pos = 'positionoutput2.csv'
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

Coincidence_Start = timer()
Coincidence_Start01 = timer()
fCo1 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr1)
print("Coincidence 25% done in {} s".format(timer()-Coincidence_Start01))

Coincidence_Start02 = timer()
fCo2 = Co.find_true_coincidences(tau, epsilon, E0, arr0, arr3)
print("Coincidence 50% done in {} s".format(timer()-Coincidence_Start02))

Coincidence_Start03 = timer()
fCo3 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr1)
print("Coincidence 75% done in {} s".format(timer()-Coincidence_Start03))

fCo4 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr3)
# fCo5 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr3)
# fCo6 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr3)



# fCo = np.vstack((fCo1, fCo2, fCo3, fCo4, fCo5, fCo6))
fCo = np.vstack((fCo1, fCo2, fCo3, fCo4))
print("Overall Coincidence Done in {} s".format(timer() - Coincidence_Start))


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
h, v, d, data, voxel_r, dnsy, lim = F4.build_voxels(51, 2.5)
points = F4.cones_generator(f3, 100, lim)
data = F4.voxel_fit(h, v, d, points, data.shape, voxel_r)
print("F4 Done in {} s".format(timer() - F4_Start))

F5_Start = timer()
fig, ax = F5.draw(h, v, d, dnsy, data, voxel_r)
dets = ax[1].scatter([0.03, 0.03, 0.27452, 0.27452], [0.03, -0.03, 0, 0],
                     [0, 0, 0.17121, -0.17121], marker='o', s=100)
print("F5 done in %f s" % (timer() - F5_Start))
plt.show()

