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
ETFile01 = 'CSV1_Smeared_G_D1.csv'
ETFile11 = 'CSV1_Smeared_G_D2.csv'
ETFile21 = 'CSV1_Smeared_G_D3.csv'
ETFile31 = 'CSV1_Smeared_G_D4.csv'
ETFile41 = 'CSV1_Smeared_G_D5.csv'
ETFile51 = 'CSV1_Smeared_G_D6.csv'
ETFile61 = 'CSV1_Smeared_G_D7.csv'
ETFile71 = 'CSV1_Smeared_G_D8.csv'
Det_Pos1 = 'CSV 2 (1).csv'

ETFile02 = 'CSV1_Exact_G_D1.csv'
ETFile12 = 'CSV1_Exact_G_D2.csv'
ETFile22 = 'CSV1_Exact_G_D3.csv'
ETFile32 = 'CSV1_Exact_G_D4.csv'
ETFile42 = 'CSV1_Exact_G_D5.csv'
ETFile52 = 'CSV1_Exact_G_D6.csv'
ETFile62 = 'CSV1_Exact_G_D7.csv'
ETFile72 = 'CSV1_Exact_G_D8.csv'
Det_Pos2 = 'CSV 2 (1).csv'

# Number_of_Files = 4
start = timer()

_, Det_Pos_arr1 = Ex.CSV_Extract(',', Folder_Path, Det_Pos1, Det_Pos1)
arr01 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile01)
arr11 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile11)
arr21 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile21)
arr31 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile31)
arr41 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile41)
arr51 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile51)
arr61 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile61)
arr71 = Ex.CSV_Extract(Delimiter1, Folder_Path, ETFile71)

_, Det_Pos_arr2 = Ex.CSV_Extract(',', Folder_Path, Det_Pos2, Det_Pos2)
arr02 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile02)
arr12 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile12)
arr22 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile22)
arr32 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile32)
arr42 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile42)
arr52 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile52)
arr62 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile62)
arr72 = Ex.CSV_Extract(Delimiter2, Folder_Path, ETFile72)


arr0_coeffs1, arr0_diff1 = Df.detector_time_fit(arr01, False, False)
arr1_coeffs1, arr1_diff1 = Df.detector_time_fit(arr11, False, False)
arr2_coeffs1, arr2_diff1 = Df.detector_time_fit(arr21, False, False)
arr3_coeffs1, arr3_diff1 = Df.detector_time_fit(arr31, False, False)
arr4_coeffs1, arr4_diff1 = Df.detector_time_fit(arr41, False, False)
arr5_coeffs1, arr5_diff1 = Df.detector_time_fit(arr51, False, False)
arr6_coeffs1, arr6_diff1 = Df.detector_time_fit(arr61, False, False)
arr7_coeffs1, arr7_diff1 = Df.detector_time_fit(arr71, False, False)

arr0_coeffs2, arr0_diff2 = Df.detector_time_fit(arr02, False, False)
arr1_coeffs2, arr1_diff2 = Df.detector_time_fit(arr12, False, False)
arr2_coeffs2, arr2_diff2 = Df.detector_time_fit(arr22, False, False)
arr3_coeffs2, arr3_diff2 = Df.detector_time_fit(arr32, False, False)
arr4_coeffs2, arr4_diff2 = Df.detector_time_fit(arr42, False, False)
arr5_coeffs2, arr5_diff2 = Df.detector_time_fit(arr52, False, False)
arr6_coeffs2, arr6_diff2 = Df.detector_time_fit(arr62, False, False)
arr7_coeffs2, arr7_diff2 = Df.detector_time_fit(arr72, False, False)

fCo041 = Co.find_true_coincidences(tau, epsilon, E0, arr01, arr41, arr0_coeffs1, arr4_coeffs1, arr0_diff1, arr4_diff1)
fCo051 = Co.find_true_coincidences(tau, epsilon, E0, arr01, arr51, arr0_coeffs1, arr5_coeffs1, arr0_diff1, arr5_diff1)
fCo061 = Co.find_true_coincidences(tau, epsilon, E0, arr01, arr61, arr0_coeffs1, arr6_coeffs1, arr0_diff1, arr6_diff1)
fCo071 = Co.find_true_coincidences(tau, epsilon, E0, arr01, arr71, arr0_coeffs1, arr7_coeffs1, arr0_diff1, arr7_diff1)
fCo141 = Co.find_true_coincidences(tau, epsilon, E0, arr11, arr41, arr1_coeffs1, arr4_coeffs1, arr1_diff1, arr4_diff1)
fCo151 = Co.find_true_coincidences(tau, epsilon, E0, arr11, arr51, arr1_coeffs1, arr5_coeffs1, arr1_diff1, arr5_diff1)
fCo161 = Co.find_true_coincidences(tau, epsilon, E0, arr11, arr61, arr1_coeffs1, arr6_coeffs1, arr1_diff1, arr6_diff1)
fCo171 = Co.find_true_coincidences(tau, epsilon, E0, arr11, arr71, arr1_coeffs1, arr7_coeffs1, arr1_diff1, arr7_diff1)
fCo241 = Co.find_true_coincidences(tau, epsilon, E0, arr21, arr41, arr2_coeffs1, arr4_coeffs1, arr2_diff1, arr4_diff1)
fCo251 = Co.find_true_coincidences(tau, epsilon, E0, arr21, arr51, arr2_coeffs1, arr5_coeffs1, arr2_diff1, arr5_diff1)
fCo261 = Co.find_true_coincidences(tau, epsilon, E0, arr21, arr61, arr2_coeffs1, arr6_coeffs1, arr2_diff1, arr6_diff1)
fCo271 = Co.find_true_coincidences(tau, epsilon, E0, arr21, arr71, arr2_coeffs1, arr7_coeffs1, arr2_diff1, arr7_diff1)
fCo341 = Co.find_true_coincidences(tau, epsilon, E0, arr31, arr41, arr3_coeffs1, arr4_coeffs1, arr3_diff1, arr4_diff1)
fCo351 = Co.find_true_coincidences(tau, epsilon, E0, arr31, arr51, arr3_coeffs1, arr5_coeffs1, arr3_diff1, arr5_diff1)
fCo361 = Co.find_true_coincidences(tau, epsilon, E0, arr31, arr61, arr3_coeffs1, arr6_coeffs1, arr3_diff1, arr6_diff1)
fCo371 = Co.find_true_coincidences(tau, epsilon, E0, arr31, arr71, arr3_coeffs1, arr7_coeffs1, arr3_diff1, arr7_diff1)
allfCo1 = [fCo041, fCo051, fCo061, fCo071, fCo141, fCo151, fCo161, fCo171,
           fCo241, fCo251, fCo261, fCo271, fCo341, fCo351, fCo361, fCo371]

fCo042 = Co.find_true_coincidences(tau, epsilon, E0, arr02, arr42, arr0_coeffs2, arr4_coeffs2, arr0_diff2, arr4_diff2)
fCo052 = Co.find_true_coincidences(tau, epsilon, E0, arr02, arr52, arr0_coeffs2, arr5_coeffs2, arr0_diff2, arr5_diff2)
fCo062 = Co.find_true_coincidences(tau, epsilon, E0, arr02, arr62, arr0_coeffs2, arr6_coeffs2, arr0_diff2, arr6_diff2)
fCo072 = Co.find_true_coincidences(tau, epsilon, E0, arr02, arr72, arr0_coeffs2, arr7_coeffs2, arr0_diff2, arr7_diff2)
fCo142 = Co.find_true_coincidences(tau, epsilon, E0, arr12, arr42, arr1_coeffs2, arr4_coeffs2, arr1_diff2, arr4_diff2)
fCo152 = Co.find_true_coincidences(tau, epsilon, E0, arr12, arr52, arr1_coeffs2, arr5_coeffs2, arr1_diff2, arr5_diff2)
fCo162 = Co.find_true_coincidences(tau, epsilon, E0, arr12, arr62, arr1_coeffs2, arr6_coeffs2, arr1_diff2, arr6_diff2)
fCo172 = Co.find_true_coincidences(tau, epsilon, E0, arr12, arr72, arr1_coeffs2, arr7_coeffs2, arr1_diff2, arr7_diff2)
fCo242 = Co.find_true_coincidences(tau, epsilon, E0, arr22, arr42, arr2_coeffs2, arr4_coeffs2, arr2_diff2, arr4_diff2)
fCo252 = Co.find_true_coincidences(tau, epsilon, E0, arr22, arr52, arr2_coeffs2, arr5_coeffs2, arr2_diff2, arr5_diff2)
fCo262 = Co.find_true_coincidences(tau, epsilon, E0, arr22, arr62, arr2_coeffs2, arr6_coeffs2, arr2_diff2, arr6_diff2)
fCo272 = Co.find_true_coincidences(tau, epsilon, E0, arr22, arr72, arr2_coeffs2, arr7_coeffs2, arr2_diff2, arr7_diff2)
fCo342 = Co.find_true_coincidences(tau, epsilon, E0, arr32, arr42, arr3_coeffs2, arr4_coeffs2, arr3_diff2, arr4_diff2)
fCo352 = Co.find_true_coincidences(tau, epsilon, E0, arr32, arr52, arr3_coeffs2, arr5_coeffs2, arr3_diff2, arr5_diff2)
fCo362 = Co.find_true_coincidences(tau, epsilon, E0, arr32, arr62, arr3_coeffs2, arr6_coeffs2, arr3_diff2, arr6_diff2)
fCo372 = Co.find_true_coincidences(tau, epsilon, E0, arr32, arr72, arr3_coeffs2, arr7_coeffs2, arr3_diff2, arr7_diff2)
allfCo2 = [fCo042, fCo052, fCo062, fCo072, fCo142, fCo152, fCo162, fCo172,
           fCo242, fCo252, fCo262, fCo272, fCo342, fCo352, fCo362, fCo372]


'''Post coincidence, current set is no coincidence data so 
    this is seen below'''

dnsy = 51
data1 = np.zeros((len(allfCo1), dnsy, dnsy, dnsy))
hits1 = np.array([])
for i, fCo in enumerate(allfCo1):
    a = np.empty((fCo.shape[0], 4), dtype=np.float32)
    f1 = F1.compton_function(a, fCo, E0, dE0, Me)
    f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, Det_Pos_arr1)
    f3 = F3.PutEmTogether(f1, f2)
    F4_Start = timer()
    h, v, d, data0, voxel_r, dnsy, lim = F4.build_voxels(dnsy, 0.4)
    max_size = 30000
    if f3.shape[0] > max_size:
        split_f3 = np.array_split(f3, (len(f3)+(max_size-1)) // max_size)
    else:
        split_f3 = [f3]
    points = np.zeros((1, 3))
    p = 32
    n0 = 4000
    for f3 in split_f3:
        points0, hits0 = F4.cones_generator(f3, p, lim, n0, 1)
        hits1 = np.append(hits1, hits0)
        points = np.append(points, points0, axis=0)
        data1[i] += F4.voxel_fit(h, v, d, points[1:], data0.shape, voxel_r)
        print('%i chunk done' % f3.shape[0])

finaldata1 = (np.sum(data1[0:4], axis=0)*np.sum(data1[5:8], axis=0)*
              np.sum(data1[9:12], axis=0)*np.sum(data1[13:16], axis=0))
data1 = finaldata1

data2 = np.zeros((len(allfCo2), dnsy, dnsy, dnsy))
hits2 = np.array([])
for i, fCo in enumerate(allfCo2):
    a = np.empty((fCo.shape[0], 4), dtype=np.float32)
    f1 = F1.compton_function(a, fCo, E0, dE0, Me)
    f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, Det_Pos_arr2)
    f3 = F3.PutEmTogether(f1, f2)
    F4_Start = timer()
    h, v, d, data0, voxel_r, dnsy, lim = F4.build_voxels(dnsy, 0.4)
    max_size = 30000
    if f3.shape[0] > max_size:
        split_f3 = np.array_split(f3, (len(f3)+(max_size-1)) // max_size)
    else:
        split_f3 = [f3]
    points = np.zeros((1, 3))
    p = 32
    n0 = 4000
    for f3 in split_f3:
        points0, hits0 = F4.cones_generator(f3, p, lim, n0, 1)
        hits2 = np.append(hits2, hits0)
        points = np.append(points, points0, axis=0)
        data2[i] += F4.voxel_fit(h, v, d, points[1:], data0.shape, voxel_r)
        print('%i chunk done' % f3.shape[0])

finaldata2 = (np.sum(data2[0:4], axis=0)*np.sum(data2[5:8], axis=0)*
              np.sum(data2[9:12], axis=0)*np.sum(data2[13:16], axis=0))
data2 = finaldata2

# a1 = np.empty((fCo1.shape[0], 4), dtype=np.float32)
# a2 = np.empty((fCo2.shape[0], 4), dtype=np.float32)
# f11 = F1.compton_function(a1, fCo1, E0, dE0, Me)
# f12 = F1.compton_function(a2, fCo2, E0, dE0, Me)
#
# f21 = F2.Generate_Position_Vectors_And_Matrices(fCo1, Det_Pos_arr1)
# f22 = F2.Generate_Position_Vectors_And_Matrices(fCo2, Det_Pos_arr2)
#
# f31 = F3.PutEmTogether(f11, f21)
# f32 = F3.PutEmTogether(f12, f22)
#
# h, v, d, data1, voxel_r, dnsy, lim = F4.build_voxels(51, 0.4)
# points1, hits1 = F4.cones_generator(f31, 32, lim, 4000, 1)
# points2, hits2 = F4.cones_generator(f32, 32, lim, 4000, 1)
# data1 = F4.voxel_fit(h, v, d, points1, data1.shape, voxel_r)
# data2 = F4.voxel_fit(h, v, d, points2, data1.shape, voxel_r)

# print("Voxel sum input 1:", np.sum(data1), "with", f11.shape[0],
#       "events \n(%.2f hits per event)" % (np.sum(data1)/f11.shape[0]),
#       "\nVoxel sum input 2:", np.sum(data2), "with", f12.shape[0],
#       "events \n(%.2f hits per event)" % (np.sum(data2)/f12.shape[0]),
#       "\nDiff:", np.abs(np.sum(data1)-np.sum(data2)), "points")

# hottest1 = np.max(data1)
# hi1 = np.unravel_index(np.argmax(data1), data1.shape)
# hottest2 = np.max(data2)
# hi2 = np.unravel_index(np.argmax(data2), data2.shape)
# print("Input 1 hottest voxel:", hottest1,
#       "\nInput 2 hottest voxel:", hottest2,
#       "\nDiff in value:", np.abs(hottest1-hottest2))
# dist12 = np.linalg.norm(np.array([h[hi1]-h[hi2], v[hi1]-v[hi2], d[hi1]-d[hi2]]))
# print("Distance %.5fm" % dist12)

diffdata = np.abs(data1 - data2)
delta_D_M = 15  # % acceptance value
# scalar = np.maximum(data1, data2 * np.max(data1)/np.max(data2))
scalar = np.maximum(data1, data2)
scalar *= 1/scalar.max()
gamma = np.sqrt((diffdata**2)/(delta_D_M**2))
# vals less than 1 pass gamma test, higher are worse
# Gamma = gamma*scalar
Gamma = np.log10(gamma, out=np.zeros_like(gamma), where=(gamma != 0))*scalar

fig, ax = F5.draw(h, v, d, dnsy, data1, data2, Gamma,
                  voxel_r, np.vstack((Det_Pos_arr1, Det_Pos_arr2)))

ax[1].text2D(0.5, -0.35, ', '.join(ETFile01.split("_")[1:3]), fontsize=9,
             ha='center', clip_on=False, transform=ax[1].transAxes)
ax[2].text2D(0.5, 1.05, ', '.join(ETFile02.split("_")[1:3]), fontsize=9,
             ha='center', clip_on=False, transform=ax[2].transAxes)


eventsbar = ax[7].bar(['Input 1', 'Input 2'], [np.mean(hits1), np.mean(hits2)], color=['tab:red', 'tab:blue'])
ax[7].errorbar(['Input 1', 'Input 2'], [np.mean(hits1), np.mean(hits2)],
               yerr=[np.std(hits1), np.std(hits2)],
               fmt='o', color='k', capsize=5.0)
ax[7].set_ylim(0, 1.1*ax[7].get_ylim()[1])
ax[7].bar_label(eventsbar, fmt='{:,.2f}', label_type='center')
ax[7].set_yticklabels([])
ax[7].set_title('Hits per event', fontsize=10, pad=0.1)
# temp = ax[9].hist(hits1, bins=50, alpha=0.7, color='tab:red')
# temp2 = ax[9].hist(hits2, bins=50, alpha=0.7, color='tab:blue')
# ax[9].set_title("Hits per event hist", fontsize=10, pad=0.1)
# hotdiff = ax[9].bar(['Input 1', 'Input 2'], [hottest1, hottest2], color=['tab:red', 'tab:blue'])
# ax[9].set_ylim(0, 1.2*ax[9].get_ylim()[1])
# ax[9].bar_label(hotdiff, fmt='{:,.0f}')
# ax[9].set_yticklabels([])
# ax[9].set_title('Hottest voxel values', fontsize=10, pad=0.1)

fCo1 = np.vstack([fCo041, fCo051, fCo061, fCo071, fCo141, fCo151, fCo161, fCo171,
           fCo241, fCo251, fCo261, fCo271, fCo341, fCo351, fCo361, fCo371])
fCo2 = np.vstack([fCo042, fCo052, fCo062, fCo072, fCo142, fCo152, fCo162, fCo172,
           fCo242, fCo252, fCo262, fCo272, fCo342, fCo352, fCo362, fCo372])

Scatters1 = np.sum([arr01.shape[0], arr11.shape[0], arr21.shape[0], arr31.shape[0]])
Absorbs1 = np.sum([arr41.shape[0], arr51.shape[0], arr61.shape[0], arr71.shape[0]])
print("Input 1 Coincidences/Events", fCo1.shape[0]/Scatters1, fCo1.shape[0]/Absorbs1)
Scatters2 = np.sum([arr02.shape[0], arr12.shape[0], arr22.shape[0], arr32.shape[0]])
Absorbs2 = np.sum([arr42.shape[0], arr52.shape[0], arr62.shape[0], arr72.shape[0]])
print("Input 2 Coincidences/Events", fCo2.shape[0]/Scatters2, fCo2.shape[0]/Absorbs2)

bar1 = ax[9].bar([0, 3], [fCo1.shape[0]/Scatters1, fCo1.shape[0]/Absorbs1], color='tab:red', label='Input 1')
bar2 = ax[9].bar([1, 4], [fCo2.shape[0]/Scatters2, fCo2.shape[0]/Absorbs2], color='tab:blue', label='Input 2')
ax[9].bar_label(bar1, fmt='{:,.4f}', fontsize=7)
ax[9].bar_label(bar2, fmt='{:,.4f}', fontsize=7)
ax[9].set_xticks([0.5, 3.5], ['Scatterer', 'Absorber'])
ax[9].set_ylim(0, 1.3 * ax[9].get_ylim()[1])
ax[9].legend(fontsize=5, markerscale=0.2, handlelength=0.5, ncol=2)
ax[9].set_title('Coincidences/Events', fontsize=9, pad=0.1)
plt.show()
