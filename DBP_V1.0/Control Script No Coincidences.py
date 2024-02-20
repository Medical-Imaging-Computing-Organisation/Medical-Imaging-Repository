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
ETFile0 = 'CSV1_Exact_G_D1.csv'

Det_Pos = 'CSV 2.csv'
# Number_of_Files = 4
start = timer()

print("Started!")
CSV_Start = timer()
arr0, Det_Pos_arr = Ex.CSV_Extract(',', Folder_Path, Det_Pos, Det_Pos)
arr0 = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile0)


print("CSV Extraction Done in {} s".format(timer() - CSV_Start))


fCo = np.zeros((int(arr0.shape[0]/2), 6))



# Modifying to account for perfect MC data - selecting out where the timestamps are equal
for i in range(0, arr0.shape[0]):
    if i % 2 == 0:
        fCo[int(i/2), 0] = arr0[i, 1]
        fCo[int(i/2), 1] = arr0[i+1, 1]
        fCo[int(i/2), 2] = 0
        fCo[int(i/2), 3] = 0
        fCo[int(i/2), 4] = arr0[i, 0]
        fCo[int(i/2), 5] = arr0[i+1, 0]

# fCo = fCo[0:3]

# print(fCo)
F1_Start = timer()
a = np.empty((fCo.shape[0], 4), dtype=np.float32)
f1 = F1.compton_function(a, fCo, E0, dE0, Me)
print("F1 Done in {} s".format(timer() - F1_Start))





# Manually perform function 2 to debug
F2_Start = timer()
# EArray = fCo
# DetectorArray = Det_Pos_arr

# def is_unique(*indices):
#     arr = np.vstack(indices)
#     _, ind = np.unique(arr, axis=1, return_index=True)
#     out = np.zeros(shape=arr.shape[1], dtype=bool)
#     out[ind] = True
#     return out

# unique_index_pairs = np.where(is_unique(EArray[:,4], EArray[:,5])==True)[0]
# vec_mat_arr = np.zeros((unique_index_pairs.size, 32), dtype=np.float32)
# Normalised_BA = np.zeros((unique_index_pairs.size, 3))
# theta = np.zeros((unique_index_pairs.size, 1))
# e_z = np.array([0, 0, 1])
# a = np.zeros((unique_index_pairs.size, 3))
# a_T = np.zeros((unique_index_pairs.size, 3, 1))
# cross = np.zeros((unique_index_pairs.size, 3))
# mag_cross = np.zeros((unique_index_pairs.size, 1))
# S_a = np.zeros((unique_index_pairs.size, 3, 3))
# R = np.zeros((unique_index_pairs.size, 3, 3))

# for i in range(0, unique_index_pairs.size):

#     # Generate OA Vector
#     vec_mat_arr[i,:3] = 0.01 * DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],4]),1:4]
#     vec_mat_arr[i, 3:6] = 0
#     # Generate BA Vector (Values only)
#     vec_mat_arr[i,6:9] = 0.01 *  DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],5]),1:4] - vec_mat_arr[i,:3]
    
#     # Calculate Normalised BA Vector
#     Normalised_BA[i] = vec_mat_arr[i,6:9] / np.sqrt(np.dot(vec_mat_arr[i,6:9], vec_mat_arr[i,6:9]))
            
#     # Calculate uncertainties on BA Vector
#     vec_mat_arr[i,9:12] = 0
    
    
#     # Rodrigues' rotation matrix formulation
    
#     # Filter for when unit-z vector and BA are parallel/antiparallel
#     if np.dot(e_z, Normalised_BA[i]) == 1:
#         vec_mat_arr[i,12] = 1
#         vec_mat_arr[i,13] = 0
#         vec_mat_arr[i,14] = 0
#         vec_mat_arr[i,15] = 0
#         vec_mat_arr[i,16] = 1
#         vec_mat_arr[i,17] = 0
#         vec_mat_arr[i,18] = 0
#         vec_mat_arr[i,19] = 0
#         vec_mat_arr[i,20] = 1
        
#     elif np.dot(e_z, Normalised_BA[i]) == -1:
#         vec_mat_arr[i,12] = -1
#         vec_mat_arr[i,13] = 0
#         vec_mat_arr[i,14] = 0
#         vec_mat_arr[i,15] = 0
#         vec_mat_arr[i,16] = -1
#         vec_mat_arr[i,17] = 0
#         vec_mat_arr[i,18] = 0
#         vec_mat_arr[i,19] = 0
#         vec_mat_arr[i,20] = -1
        
#     else:
#         # Calculate cross product of unit-z vector and normalised BA vector, accounting for right handed system
#         cross[i] = np.cross(e_z, Normalised_BA[i])
        
#         mag_cross[i] = np.sqrt(np.dot(cross[i], cross[i]))
        
#         a[i] = cross[i]/mag_cross[i]
        
#         a_T[i] = a[i][:, np.newaxis]

#         # Calculating angle of rotation
#         theta[i] = np.arcsin(mag_cross[i])
        
        
        
        
        
        
#         # if Normalised_BA[i,2] < 0:
#         #     cross[i] = np.cross(e_z, Normalised_BA[i])
#         #     theta[i] = theta[i]
            
        
        
        
        
        
#         # Calculating S_a tensor
#         S_a[i,0,0] = 0
#         S_a[i,0,1] = -a[i,2]
#         S_a[i,0,2] = a[i,1]
#         S_a[i,1,0] = a[i,2]
#         S_a[i,1,1] = 0
#         S_a[i,1,2] = -a[i,0]
#         S_a[i,2,0] = -a[i,1]
#         S_a[i,2,1] = a[i,0]
#         S_a[i,2,2] = 0
        
        
#         # Calculating Rotation Matrix
#         # R[i] = np.tensordot(a[i], a_T[i], axes=0) + (np.identity(3) - np.tensordot(a[i], a_T[i], axes=0)) * np.cos(theta[i]) + S_a * np.cos(theta[i])
        
#         R[i] = np.identity(3) + np.sin(theta[i]) * S_a[i] + (1-np.cos(theta[i]))* np.matmul(S_a[i], S_a[i])
        
        
        
#         # Generating rotation matrix elements for each pair
#         vec_mat_arr[i,12] = R[i,0,0]
#         vec_mat_arr[i,13] = R[i,0,1]
#         vec_mat_arr[i,14] = R[i,0,2]
#         vec_mat_arr[i,15] = R[i,1,0]
#         vec_mat_arr[i,16] = R[i,1,1]
#         vec_mat_arr[i,17] = R[i,1,2]
#         vec_mat_arr[i,18] = R[i,2,0]
#         vec_mat_arr[i,19] = R[i,2,1]
#         vec_mat_arr[i,20] = R[i,2,2]
    
    

#     # Generating rotation matrix error elements

#     # This requires a significant time investment towards tedious array multiplications, it will be done during 
#     #         week 3 in time for the whole code throughput calculating errors

#     vec_mat_arr[i,21:30] = 0 # for now the errors are set to 0


#     # Copying across the scatterer and absorber indices for function 3
#     vec_mat_arr[i,30:32] = EArray[unique_index_pairs[i], 4:6]




f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, Det_Pos_arr)








print("F2 Done in {} s".format(timer() - F2_Start))

F3_Start = timer()
f3 = F3.PutEmTogether(f1, f2)
# f3 = F3.PutEmTogether(f1, vec_mat_arr)
print("F3 Done in {} s".format(timer() - F3_Start))

F4_Start = timer()
h, v, d, data, voxel_r, dnsy, lim = F4.build_voxels(51, 2.5)
points = F4.cones_generator(f3, 100, lim)
data = F4.voxel_fit(h, v, d, points, data.shape, voxel_r)
print("F4 Done in {} s".format(timer() - F4_Start))

F5_Start = timer()
fig, ax = F5.draw(h, v, d, dnsy, data, voxel_r, Det_Pos_arr)
print("F5 done in %f s" % (timer() - F5_Start))
plt.show()

