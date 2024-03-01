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
#import Find_True_Coincidences as Co
import Function1 as F1


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
arr0, det = Ex.CSV_Extract(',', Folder_Path, Det_Pos, Det_Pos)
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
pair = np.array([1., 3.])

print(fCo)
# print(fCo)
F1_Start = timer()
a = np.empty((fCo.shape[0], 4), dtype=np.float32)
f1 = F1.compton_function(a, fCo, E0, dE0, Me)
print(f1)
delete = []
for j in range(f1.shape[0]):
    print(j)
    if np.array_equal(f1[j,2:4], pair):
        print('good')
    else:
        delete.append(j)
f1 = np.delete(f1, delete, axis = 0)
print("F1 Done in {} s".format(timer() - F1_Start))

#f1 = [theta,dtheta,sc,ab]
fig, ax = plt.subplots()
angle = 180*f1[:,0]/np.pi
ax.hist(angle, bins = 36)
# ax.axvline(np.mean(angle), color = 'r')
ax.set_title(f'Histogram of Opening Angles for [{int(pair[0])},{int(pair[1])}]')
ax.set_xlabel('Opening angle (degrees)')
ax.set_ylabel('counts')

plt.show()

#diagnostic 3D plot
#d=5
#phi=(np.pi/180)*(45)
#theta=(np.pi/180)*(90)
Lmax = 2
i = [1, 0, 0]
j = [0, 1, 0]
k = [0, 0, 1]
#v = [d*np.cos(phi)*np.sin(theta), d*np.sin(phi)*np.sin(theta), d*np.cos(theta)]
fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.set_title('Detector Positions')
ax.set_xlim(-Lmax, Lmax)
ax.set_xlabel('x (m)')
ax.set_ylim(-Lmax, Lmax)
ax.set_ylabel('y (m)')
ax.set_zlim(-Lmax, Lmax)
ax.set_zlabel('z (m)')

#ax.quiver(0, 0, 0, r[0], r[1], r[2], color = 'r')
ax.quiver(0, 0, 0, i[0], i[1], i[2], color = 'b', label = 'x-unit')
ax.quiver(0, 0, 0, j[0], j[1], j[2], color = 'y', label = 'y-unit')
ax.quiver(0, 0, 0, k[0], k[1], k[2], color = 'g', label = 'z-unit')
i=0
#b=beta_vectors[i]
#beta_label = f'beta vector , b = {b[0]:.3f}i+{b[1]:.3f}j+{b[2]:.3f}k'
#ax.quiver(scatterers[:,0], scatterers[:,1], scatterers[:,2], beta_vectors[:,0], beta_vectors[:,1], beta_vectors[:,2], color = 'r', label = beta_label)
#ax.quiver(absorbers[:,0], absorbers[:,1], absorbers[:,2], beta_vectors[:,0], beta_vectors[:,1], beta_vectors[:,2], color = 'r')

ax.scatter(0.01 * det[:, 1], 0.01 * det[:, 2],
                 0.01 * det[:, 3], marker='o', s=100, alpha=0.6,
                 c=det[:, 0], cmap='gist_rainbow', label = 'detectors')
ax.scatter(0.01 * det[:, 1], 0.01 * det[:, 2], 0.01 * det[:, 3],
                      marker='o', s=100, alpha=0.6, c=det[:, 0],
                      cmap='gist_rainbow')
for i in range(det.shape[0]):
    ax.text(x=0.01 * det[i, 1], y=0.01 * det[i, 2],
            z=0.01 * det[i, 3], s=str(int(det[i, 0])),
            ha='center', va='center', clip_on=True) 
ax.legend(loc='upper right')
# ax.plot(np.linspace(0,0,50),np.linspace(0,5,50),np.linspace(0,5,50))
ax.view_init(0,0)
plt.show()



