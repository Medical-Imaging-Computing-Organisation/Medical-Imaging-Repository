# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:19:50 2024

@author: Richard Malone
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
import pandas as pd
from pathlib import Path
from numba import njit
from numba import prange
from numba import set_num_threads

import CSV_Multiple_Detector_File_Extraction as Ex
import Find_True_Coincidences as Co
import Function1 as F1
import Function2 as F2
import Function3 as F3
import Function4HeatmapHybridVectorized as F4

E0 = 200  # kev
Me = 510.99895000  # kev
File2 = None
File3 = None
tau = 1000000000
Delimiter = ','
Header = 0
Folder_Path = os.getcwd()
ETFile0 = 'CSV1_D1.csv'  # ?
File2 = 'CSV1_D2.csv'
File3 = 'CSV1_D3.csv'
File4 = 'CSV1_D4.csv'
Number_of_Files = 1

fEx1, fEx2, fEx3 = Ex.CSV_Extract_Multiple_Channel_Files(Delimiter, Number_of_Files, Folder_Path,
                                            ETFile0, ETFile2_Name=File2, ETFile3_Name=File3, ETFile4_Name=File4)
# if File2 is not None:
#     fEx1 = fEx[0]
#     fEx2 = fEx[1]
#     if File3 is not None:
#         fEx3 = fEx[2]
# else:
#     fEx1 = fEx[0]

fCo = Co.find_true_coincidences(tau, E0, fEx1, fEx2)

N, c = fCo.shape
a = np.empty((N,4), dtype=np.float32)
f1 = F1.compton_function(a, fCo, E0, Me)

f2 = F2.Generate_Position_Vectors_And_Matrices(fCo, fEx2)

# f1 = np.ones((4, 4))
# f2 = np.ones((5, 31))
f3 = F3.PutEmTogether(f1, f2)

h, v, d, data, voxel_r, dnsy, lim = F4.build_voxels(51, 2.5)

points = F4.cones_generator(f3, 100, -2.5, 2.5, -2.5, 2.5)
data = F4.voxel_fit(h, v, d, points, data.shape, voxel_r)

''' Drawing all that '''
fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(10, 5),
             per_subplot_kw={1: {'projection': '3d', 'xlabel': 'x', 'ylabel': 'y', 'zlabel': 'z'},
                             2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                             3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                             4: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'x'}})

try:  # Colour map creation in try to prevent recreation error
    color_array = plt.get_cmap('YlOrRd')(range(256))
    color_array[:, -1] = np.linspace(0.0, 1.0, 256)
    map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
    plt.colormaps.register(cmap=map_object)
except ValueError:
    pass

XYZ = ax[1].scatter(h, v, d, marker='s', s=2000/dnsy, c=data, cmap="YlOrRd_alpha2")
plt.colorbar(XYZ, location='left')


mid = int((dnsy-1)/2)
var = int(mid/5)
# XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data, axis=0), cmap="YlOrRd")
XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[mid-var:mid+var+1, :, :], axis=0), cmap="YlOrRd")
cb2 = plt.colorbar(XZ)  # X-Z and Y-Z colour maps
# YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data, axis=1), cmap="YlOrRd")
YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, mid-var:mid+var+1, :], axis=1), cmap="YlOrRd")
cb3 = plt.colorbar(YZ)
XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, mid-var:mid+var+1], axis=2), cmap="YlOrRd")
cb4 = plt.colorbar(XY)

ax[1].set_title('3D Graph')
ax[1].set_zlim(-lim, lim)
plt.tight_layout()
plt.show()