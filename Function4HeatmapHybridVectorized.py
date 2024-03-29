# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:07:55 2024

@author: Richard Malone
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
# from numba import njit
# from timeit import default_timer as timer
# import psutil
# import os


'''
Function 4 (Richard) Generate set of points corresponding to cones: 
    From the output of Function 3, generate a set of points that correspond to 
    those populated by the surfaces of cones. 
    Output: [[x, y, z], [x, y, z] ...]
'''

#if we had a single xyz point, this is the operation we want to carry out. 

# def cone(x,y,theta):
#     z=np.sqrt(np.add(np.square(x),np.square(y)))
#     z=np.einsum('jk,i',z,1/np.tan(theta))
#     return z
    
#since N>P, for loop through P instead of N, apply N using Numpy for each xyz row of points

# @njit(parallel=True)
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
    u, v = np.meshgrid(x, y)
    r = np.multiply(p**2,a.shape[0])
    theta = a[:, 0]
    # w = cone(u, v, theta)
    w=np.sqrt(np.add(np.square(u),np.square(v)))
    w=np.einsum('jk,i',w,1/np.tan(theta))
    
    vector = np.array([np.tile(u, (w.shape[0],1,1)),
                        np.tile(v, (w.shape[0],1,1)), w]).T
    
    rotMatrix = np.array([[a[:,14], a[:,17], a[:,20]],
                          [a[:,15], a[:,18], a[:,21]],
                          [a[:,16], a[:,19], a[:,22]]]).T
    # print(vector)
    vector = np.einsum('...jk,...j', rotMatrix, vector)
    vector += a[:, 2:5]
    vector = vector.reshape((r, 3))
    vector = np.delete(vector, np.where(np.abs(vector)>Lmax)[0], axis=0)
    # lmu = process.memory_info().rss - base_memory_usage
    # print(f'memory used {lmu}')
    return vector


''' Building voxel grid '''
def build_voxels(dnsy=51, lim=2.5):
    # dnsy number density operator
    # lim  extension of area in all directions from origin
    voxel_r = lim/dnsy  # voxel radius
    x = np.linspace(-lim+voxel_r, lim-voxel_r, dnsy, endpoint=True)
    y, z = x, x  # cube dimensions
    h, v, d = np.meshgrid(x, y, z, sparse=False)  # Horizontal, vertical, depth
    data = np.zeros((dnsy, dnsy, dnsy))  # empty dataset
    return h, v, d, data, voxel_r, dnsy, lim



def voxel_fit(h, v, d, xyz, shape, voxel_r):
    '''Fitting into voxels'''
    # usually cone_points will be xyz
    data1 = np.zeros(shape)  # temporary dataset
    cs = np.digitize(xyz, h[0, :, 0]+voxel_r, right=True)
    # returns indices for xyz bins to fit into voxels
    np.add.at(data1, (cs[:, 1], cs[:, 0], cs[:, 2]), 1)  # if dupe
    # adds 1 to every voxel specified, including duplicate indices
    return data1

if __name__ == "__main__":

    try:
        plt.close()
    finally:
        pass
    
    #test data
    N = 1000
    theta = np.pi*np.linspace(20,50, N)/180
    x1 = np.linspace(0,0, N)
    y1 = np.linspace(-2,-2, N)
    z1 = np.linspace(0,0, N)
    null = np.linspace(0,0,N)
    one = np.linspace(1,1,N)
    T = np.linspace(0, np.pi/2, N)
    rotation = 1
    if rotation == 1: # x-rotation
        R11, R12, R13 = one, null, null
        R21, R22, R23 = null, one*np.cos(T), -one*np.sin(T)
        R31, R32, R33 = null, one*np.sin(T), one*np.cos(T)
    if rotation == 2: #y-rotation
        R11, R12, R13 = one*np.cos(T),null, one*np.sin(T)
        R21, R22, R23 = null, one, null
        R31, R32, R33 = -one*np.sin(T), null, one*np.cos(T)
    if rotation == 3: #z-rotation
        R11, R12, R13 = one*np.cos(T), -one*np.sin(T), null
        R21, R22, R23 = one*np.sin(T), one*np.cos(T), null
        R31, R32, R33 = null, null, one
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

    h, v, d, data, voxel_r, dnsy, lim = build_voxels(51, 2.5)
    # process = psutil.Process(os.getpid())
    # base_memory_usage = process.memory_info().rss
    # start = timer()
    points = cones_generator(array_in_test, 100, -2.5, 2.5, -2.5, 2.5)
    data = voxel_fit(h, v, d, points, data.shape, voxel_r)

    # for n in np.linspace(0, N, 20):
    #     points = cones_generator(array_in_test[int(n):int(n+N/20)], 100, -2.5, 2.5, -2.5, 2.5)
    #     data += voxel_fit(h, v, d, points)
    # print(f"{timer()-start}", "seconds")
    # lmu = process.memory_info().rss - base_memory_usage
    # print(f'memory used {lmu}')


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
