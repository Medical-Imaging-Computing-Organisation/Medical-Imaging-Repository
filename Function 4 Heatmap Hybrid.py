# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:07:55 2024

@author: Richard Malone
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
'''
Function 4 (Richard) Generate set of points corresponding to cones: 
    From the output of Function 3, generate a set of points that correspond to 
    those populated by the surfaces of cones. 
    Output: [[x, y, z], [x, y, z] ...]
'''

#if we had a single xyz point, this is the operation we want to carry out. 

def cone(x,y,theta):
    z=np.sqrt(np.add(np.square(x),np.square(y)))
    z=np.divide(z,np.tan(theta))
    return z
    
#since N>P, for loop through P instead of N, apply N using Numpy for each xyz row of points

def cones_generator(a, p, xmin, xmax, ymin, ymax, Lmax=2.5):
    '''
    Ensure all inputs bare the same energy units, especially the electron 
    rest energy E=Me*c^2
    Parameters
    ----------
    a : array
        The initial photon energy.
    p : float
        The energy deposited during the compton scatter.
    xmin : float
        The energy of the scattered photon.
    xmax : float
        The rest energy of the electron
    ymin : float
        somethin
    Lmax: float
        the upper limit on the modulus of all x y and z values.
    Returns
    -------
    theta : Float
        The angle of the compton cone from the w axis. 
    theta_err : Float
        The error on the angle as derived from the compton energy equation.
    '''
    x = np.linspace(xmin, xmax, p)
    y = np.linspace(ymin, ymax, p)
    grid = np.meshgrid(x,y)
    x = np.ndarray.flatten(grid[0])
    y = np.ndarray.flatten(grid[1])

    N, M = np.shape(a)
    P = np.square(p)
    r = np.multiply(P,N)
    points_trn = np.zeros((r, 3), dtype=np.float32)
    for pr in range(P):
        u = x[pr] #x coordinate in the cone frame
        v = y[pr] #y coordinate in the cone frame
        theta = a[:,0] #column of cone angles
        w = cone(u,v,theta) #zsize=P, z coordinate in cone frame
        null = np.linspace(0,0,N)
        u = null + u #u point cast to the number of w points
        v = null + v #v point cast to a number of w points
        #R11 = array_in[:,14]  #coefficients of the rotation matrix
        x_t = np.multiply(u,a[:,14])+ np.multiply(v,a[:,15]) + np.multiply(w,a[:,16]) #rotated x point
        y_t = np.multiply(u,a[:,17])+ np.multiply(v,a[:,18]) + np.multiply(w,a[:,19]) #rotated y point
        z_t = np.multiply(u,a[:,20])+ np.multiply(v,a[:,21]) + np.multiply(w,a[:,22]) #rotated z point
        x_t = x_t - a[:,2] #translated x point
        y_t = y_t - a[:,3] #translated y point
        z_t = z_t - a[:,4] #translated z point
        imin = np.multiply(pr,N)
        imax = np.add(N,imin)
        points_trn[imin:imax] = np.transpose(np.array([x_t,y_t,z_t]))
        print(f'\r{pr+1}points complete', end = '', flush = True)

    points_trn = np.delete(points_trn, np.where(np.abs(points_trn)>Lmax)[0], axis=0)

    return points_trn
#test data
N = 4
theta = np.pi*np.linspace(20,80, N)/180
x1 = np.linspace(2,2, N)
y1 = np.linspace(2,2, N)
z1 = np.linspace(2,2, N)
null = np.linspace(0,0,N)
R11 = np.linspace(1,1, N)
R12 = null
R13 = null
R21 = null
R22 = np.linspace(1,1,N)
R23 = null
R31 = null
R32 = null
R33 = np.linspace(1,1,N)
array_in_test = np.zeros((N,32))
array_in_test[:,0] = theta
array_in_test[:,14] = R11
array_in_test[:,15] = R12
array_in_test[:,16] = R13
array_in_test[:,17] = R21
array_in_test[:,18] = R22
array_in_test[:,19] = R23
array_in_test[:,20] = R31
array_in_test[:,21] = R32
array_in_test[:,22] = R33
array_in_test[:,2] = x1
array_in_test[:,3] = y1
array_in_test[:,4] = z1

points = cones_generator(array_in_test, 100, -2.5, 2.5, -2.5, 2.5)
# print(points)

''' Building voxel grid '''
dnsy = 51  # number density operator
lim = 2.5  # extension of area in all directions from origin
voxel_r = lim/dnsy  # voxel radius
x = np.linspace(-lim+voxel_r, lim-voxel_r, dnsy, endpoint=True)
y, z = x, x  # cube dimensions
h, v, d = np.meshgrid(x, y, z, sparse=False)  # Horizontal, vertical, depth
data = np.zeros((dnsy, dnsy, dnsy))  # empty dataset
# data = np.arange(1, 1+dnsy**3).reshape(dnsy, dnsy, dnsy)
# index = (0, 0, 0)
# print(data[index], "loc", h[index], v[index], d[index])


# @njit(parallel=True)
# @njit
def voxel_fit(h, v, d, xyz):

    '''Fitting into voxels'''
    # usually cone_points will be xyz
    data1 = np.zeros(data.shape)  # temporary dataset
    cs = np.digitize(xyz, h[0, :, 0]+voxel_r, right=True)
    # returns indices for xyz bins to fit into voxels
    # data1[cs[:, 0], cs[:, 1], cs[:, 2]] = 1  # if no dupe
    np.add.at(data1, (cs[:, 0], cs[:, 1], cs[:, 2]), 1)  # if dupe
    # for abc in cs:  #njit friendly version
    #     data1[abc[0], abc[1], abc[2]] += 1
    # adds 1 to every voxel specified, including duplicate indices
    return data1


data = voxel_fit(h, v, d, points)

''' Drawing all that '''
fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(12, 6),
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

# ax[1].voxels(np.ones(data.shape), alpha=0.12, edgecolor="k", shade=True)  # Voxel visualization
'''Could be choosing to plot the hottest planes?
    This actually needs to consider the hottest "volume"
    otherwise different planes could be plotted'''
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
# plt.tight_layout()
plt.show()