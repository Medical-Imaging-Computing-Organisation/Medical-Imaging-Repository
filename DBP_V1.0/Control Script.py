import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
import plotly.graph_objects as go
import plotly.express as px
from timeit import default_timer as timer
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

E0 = 0.662  # MeV
dE0 = 3E-5  # MeV
Me = 0.51099895000  # MeV
tau = 1E10
epsilon = 0.01
Delimiter = ';'
Header = 0
Folder_Path = os.getcwd()
ETFile0 = 'CH0 01Feb Setup 2 A.csv'
ETFile1 = 'CH1 01Feb Setup 2 B.csv'
ETFile2 = 'CH2 01Feb Setup 2 A.csv'
ETFile3 = 'CH3 01Feb Setup 2 B.csv'
Det_Pos = 'positionoutput2.csv'
# Number_of_Files = 4
start = timer()

CSV_Start = timer()
arr0, Det_Pos_arr = Ex.CSV_Extract(Delimiter, Folder_Path, ETFile0, Det_Pos)
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
points = F4.cones_generator(f3, 100, -2.5, 2.5, -2.5, 2.5, lim)
data = F4.voxel_fit(h, v, d, points, data.shape, voxel_r)
print("F4 Done in {} s".format(timer() - F4_Start))

''' Drawing all that '''
fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(10, 5),
                             per_subplot_kw={1: {'projection': '3d', 'xlabel': 'x', 'ylabel': 'y', 'zlabel': 'z'},
                                             2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                                             3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                                             4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'}})

try:  # Colour map creation in try to prevent recreation error
    color_array = plt.get_cmap('YlOrRd')(range(256))
    color_array[:, -1] = np.linspace(0.0, 1.0, 256)
    map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
    plt.colormaps.register(cmap=map_object)
except ValueError:
    pass

dets = ax[1].scatter([0.03, 0.03, 0.27452, 0.27452], [0.03, -0.03, 0, 0],
                     [0, 0, 0.17121, -0.17121], marker='o', s=100)
XYZ = ax[1].scatter(h, v, d, marker='s', s=2000 / dnsy, c=data, cmap="YlOrRd_alpha2")
plt.colorbar(XYZ, location='left')

mid = np.unravel_index(np.argmax(data), data.shape)
var = int((dnsy-1) / 10)
# var = int
XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[mid[0] - var:mid[0] + var + 1, :, :], axis=0), cmap="YlOrRd")
cb2 = plt.colorbar(XZ)  # X-Z and Y-Z colour maps
YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, mid[1] - var:mid[1] + var + 1, :], axis=1), cmap="YlOrRd")
cb3 = plt.colorbar(YZ)
XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, mid[2] - var:mid[2] + var + 1], axis=2), cmap="YlOrRd")
cb4 = plt.colorbar(XY)
ax[1].set_title('3D Graph')
plt.tight_layout()
print("%.2f seconds run time" % (timer()-start))
plt.show()

