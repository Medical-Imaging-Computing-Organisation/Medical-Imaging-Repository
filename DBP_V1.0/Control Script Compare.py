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
import Function5Compare as F5

E0 = 0.662  # MeV
dE0 = 3E-5  # MeV
Me = 0.51099895000  # MeV
tau = 0.001
epsilon = 0.01
Delimiter1 = ','
Delimiter2 = ','
Header = 0
Folder_Path = os.getcwd()
ETFile01 = 'CSV1_combined_exact_good.csv'
# ETFile11 = 'CSV1_Full_Exact_D2.csv'
# ETFile21 = 'CSV1_Full_Exact_D3.csv'
# ETFile31 = 'CSV1_Full_Exact_D4.csv'
Det_Pos1 = 'CSV 2 (2).csv'

ETFile02 = 'CSV1_combined_smeared_good.csv'
# ETFile12 = 'CSV1_D2.csv'
# ETFile22 = 'CSV1_D3.csv'
# ETFile32 = 'CSV1_D4.csv'
Det_Pos2 = 'CSV 2 (2).csv'

# Number_of_Files = 4
start = timer()

arr01 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile01)
# arr01 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile01)
# arr11 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile11)
# arr21 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile21)
# arr31 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile31)
_, Det_Pos_arr1 = Ex.CSV_Extract(',', Folder_Path, Det_Pos1, Det_Pos1)

arr02 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile02)
# arr02 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile02)
# arr12 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile12)
# arr22 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile22)
# arr32 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile32)
_, Det_Pos_arr2 = Ex.CSV_Extract(',', Folder_Path, Det_Pos2, Det_Pos2)


# # # Coincidence_Start = timer()
# # # Coincidence_Start01 = timer()
# # # fCo11 = Co.find_true_coincidences(tau, epsilon, E0, arr01, arr11)
# # # fCo12 = Co.find_true_coincidences(tau, epsilon, E0, arr02, arr12)
# # # print("Coincidence 25% done in {} s".format(timer()-Coincidence_Start01))
# # #
# # # Coincidence_Start02 = timer()
# # # fCo21 = Co.find_true_coincidences(tau, epsilon, E0, arr01, arr31)
# # # fCo22 = Co.find_true_coincidences(tau, epsilon, E0, arr02, arr32)
# # # print("Coincidence 50% done in {} s".format(timer()-Coincidence_Start02))
# # # #
# # # Coincidence_Start03 = timer()
# # # fCo31 = Co.find_true_coincidences(tau, epsilon, E0, arr21, arr11)
# # # fCo32 = Co.find_true_coincidences(tau, epsilon, E0, arr22, arr12)
# # # print("Coincidence 75% done in {} s".format(timer()-Coincidence_Start03))
# # # #
# # # fCo41 = Co.find_true_coincidences(tau, epsilon, E0, arr21, arr31)
# # # fCo42 = Co.find_true_coincidences(tau, epsilon, E0, arr22, arr32)
# # # # fCo5 = Co.find_true_coincidences(tau, epsilon, E0, arr1, arr3)
# # # # fCo6 = Co.find_true_coincidences(tau, epsilon, E0, arr2, arr3)
# #
# #
# # # fCo = np.vstack((fCo1, fCo2, fCo3, fCo4, fCo5, fCo6))
# # fCo1 = np.vstack((fCo11, fCo21, fCo31, fCo41))
# # fCo2 = np.vstack((fCo12, fCo22, fCo32, fCo42))
# print("Overall Coincidence Done in {} s".format(timer() - Coincidence_Start))

fCo1 = np.zeros((int(arr01.shape[0]/2), 6))
for i in range(0, arr01.shape[0]):
    if i % 2 == 0:
        fCo1[int(i/2), 0] = arr01[i, 1]
        fCo1[int(i/2), 1] = arr01[i+1, 1]
        fCo1[int(i/2), 2] = 0
        fCo1[int(i/2), 3] = 0
        fCo1[int(i/2), 4] = arr01[i, 0]
        fCo1[int(i/2), 5] = arr01[i+1, 0]
fCo2 = np.zeros((int(arr02.shape[0]/2), 6))
for i in range(0, arr02.shape[0]):
    if i % 2 == 0:
        fCo2[int(i/2), 0] = arr02[i, 1]
        fCo2[int(i/2), 1] = arr02[i+1, 1]
        fCo2[int(i/2), 2] = 0
        fCo2[int(i/2), 3] = 0
        fCo2[int(i/2), 4] = arr02[i, 0]
        fCo2[int(i/2), 5] = arr02[i+1, 0]

'''Post coincidence, current set is no coincidence data so 
    this is seen below'''


a1 = np.empty((fCo1.shape[0], 4), dtype=np.float32)
a2 = np.empty((fCo2.shape[0], 4), dtype=np.float32)
f11 = F1.compton_function(a1, fCo1, E0, dE0, Me)
f12 = F1.compton_function(a2, fCo2, E0, dE0, Me)

f21 = F2.Generate_Position_Vectors_And_Matrices(fCo1, Det_Pos_arr1)
f22 = F2.Generate_Position_Vectors_And_Matrices(fCo2, Det_Pos_arr2)

f31 = F3.PutEmTogether(f11, f21)
f32 = F3.PutEmTogether(f12, f22)

h, v, d, data1, voxel_r, dnsy, lim = F4.build_voxels(51, 1)
points1, hits1 = F4.cones_generator(f31, 50, lim, 1000, 1)
points2, hits2 = F4.cones_generator(f32, 50, lim, 1000, 1)
data1 = F4.voxel_fit(h, v, d, points1, data1.shape, voxel_r)
data2 = F4.voxel_fit(h, v, d, points2, data1.shape, voxel_r)

# print("Voxel sum input 1:", np.sum(data1), "with", f11.shape[0],
#       "events \n(%.2f hits per event)" % (np.sum(data1)/f11.shape[0]),
#       "\nVoxel sum input 2:", np.sum(data2), "with", f12.shape[0],
#       "events \n(%.2f hits per event)" % (np.sum(data2)/f12.shape[0]),
#       "\nDifference:", np.abs(np.sum(data1)-np.sum(data2)), "points")

# hottest1 = np.max(data1)
# hi1 = np.unravel_index(np.argmax(data1), data1.shape)
# hottest2 = np.max(data2)
# hi2 = np.unravel_index(np.argmax(data2), data2.shape)
# print("Input 1 hottest voxel:", hottest1,
#       "\nInput 2 hottest voxel:", hottest2,
#       "\nDifference in value:", np.abs(hottest1-hottest2))
# dist12 = np.linalg.norm(np.array([h[hi1]-h[hi2], v[hi1]-v[hi2], d[hi1]-d[hi2]]))
# print("Distance %.5fm" % dist12)

diffdata = data1 - data2
delta_D_M = 15  # % acceptance value
# scalar = np.maximum(data1, data2 * np.max(data1)/np.max(data2))
scalar = np.maximum(data1, data2)
scalar *= 1/scalar.max()
gamma = np.sqrt((diffdata**2)/(delta_D_M**2))
# vals less than 1 pass gamma test, higher are worse
# Gamma = gamma*scalar
Gamma = np.log(gamma, out=np.zeros_like(gamma), where=(gamma != 0))*scalar

fig, ax = F5.draw(h, v, d, dnsy, data1, data2, Gamma,
                  voxel_r, np.vstack((Det_Pos_arr1, Det_Pos_arr2)))
sumbar = ax[7].bar(['Input 1', 'Input 2'], [np.sum(data1), np.sum(data2)], color=['tab:red', 'tab:blue'])
ax[7].set_ylim(0, 1.2*ax[7].get_ylim()[1])
ax[7].bar_label(sumbar, fmt='{:,.0f}')
ax[7].set_yticklabels([])
ax[7].set_title('Sum of hits', fontsize=10, pad=0.1)
eventsbar = ax[8].bar(['Input 1', 'Input 2'], [np.mean(hits1), np.mean(hits2)], color=['tab:red', 'tab:blue'])
ax[8].errorbar(['Input 1', 'Input 2'], [np.mean(hits1), np.mean(hits2)], yerr=[np.std(hits1), np.std(hits2)], fmt='o', color='k')
ax[8].set_ylim(0, 1.2*ax[8].get_ylim()[1])
ax[8].bar_label(eventsbar, fmt='{:,.0f}')
ax[8].set_yticklabels([])
ax[8].set_title('Hits per event', fontsize=10, pad=0.1)
temp = ax[9].hist(hits1, bins=50, alpha=0.7, color='tab:red')
temp2 = ax[9].hist(hits2, bins=50, alpha=0.7, color='tab:blue')
ax[9].set_title("Hits per event hist", fontsize=10, pad=0.1)
# hotdiff = ax[9].bar(['Input 1', 'Input 2'], [hottest1, hottest2], color=['tab:red', 'tab:blue'])
# ax[9].set_ylim(0, 1.2*ax[9].get_ylim()[1])
# ax[9].bar_label(hotdiff, fmt='{:,.0f}')
# ax[9].set_yticklabels([])
# ax[9].set_title('Hottest voxel values', fontsize=10, pad=0.1)
plt.show()
