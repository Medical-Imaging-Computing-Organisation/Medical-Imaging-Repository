# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:07:55 2024

@author: Richard Malone
"""
import numpy as np
import matplotlib.pyplot as plt
import Function5 as F5
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

# @njit(parallel=True)
def cones_generator(a, p, Lmax, Measure=None):
    '''
    Ensure all inputs bare the same energy units, especially the electron 
    rest energy E=Me*c^2
    Parameters
    ----------
    a : array
        The input array with N rows and 32 columns
    p : integer
        The number of points to generate along the x and y plane
        equal to the square root of the number of points per cone
    Lmax: float
        the upper limit on the modulus of all x y and z values produced.
    Returns
    -------
    points : array
        array of points to be plotted by the heatmap,
        3 cartesian columns, N*p^2 rows of position 3-vectors
    '''
    theta = a[:, 0]
    n0 = 100  # points per m^2
    alpha = 1.5
    umax = p * np.sqrt(np.divide(np.sin(theta), alpha * n0 * np.pi))

    x = np.linspace(-umax, umax, p).T
    u = np.empty((theta.size, p, p), dtype=np.float32)
    v = np.empty((theta.size, p, p), dtype=np.float32)
    for i in range(umax.size):
        u[i], v[i] = np.meshgrid(x[i], x[i])

    r = np.multiply(p ** 2, a.shape[0])
    w = np.sqrt(np.add(np.square(u), np.square(v)))
    w = np.einsum('ijk,i->ijk', w, 1 / np.tan(theta))

    vector = np.array([u, v, w]).T

    rotMatrix = np.array([[a[:, 14], a[:, 17], a[:, 20]],
                          [a[:, 15], a[:, 18], a[:, 21]],
                          [a[:, 16], a[:, 19], a[:, 22]]]).T

    vector = np.einsum('...jk,...k', rotMatrix, vector)
    vector += a[:, 2:5]
    if Measure is not None:
        vector = np.moveaxis(vector, [2], [0]).reshape((theta.size, -1, 3))
        hits = np.invert(np.any(np.abs(vector) > Lmax, axis=2)).sum(axis=1)
        vector = vector.reshape((r, 3))
        vector = np.delete(vector, np.where(np.abs(vector) > Lmax)[0], axis=0)
        return vector, hits
    else:
        vector = vector.reshape((r, 3))
        vector = np.delete(vector, np.where(np.abs(vector) > Lmax)[0], axis=0)
        return vector

''' Building voxel grid '''
def build_voxels(dnsy=51, lim=2.5):
    # dnsy number density operator
    # lim  extension of area in all directions from origin
    voxel_r = lim / dnsy  # voxel radius
    x = np.linspace(-lim + voxel_r, lim - voxel_r, dnsy, endpoint=True)
    y, z = x, x  # cube dimensions
    h, v, d = np.meshgrid(x, y, z, sparse=False)  # Horizontal, vertical, depth
    data = np.zeros((dnsy, dnsy, dnsy))  # empty dataset
    return h, v, d, data, voxel_r, dnsy, lim

def voxel_fit(h, v, d, xyz, shape, voxel_r):
    """Fitting into voxels"""
    # usually cone_points will be xyz
    data1 = np.zeros(shape)  # temporary dataset
    cs = np.digitize(xyz, h[0, :, 0] + voxel_r, right=True)
    # returns indices for xyz bins to fit into voxels
    try:
        np.add.at(data1, (cs[:, 1], cs[:, 0], cs[:, 2]), 1)  # if dupe
    except IndexError:
        print("You've provided values outside of the limits to F4.")
    # adds 1 to every voxel specified, including duplicate indices
    return data1

if __name__ == "__main__":

    try:
        plt.close()
    finally:
        pass

    # test data
    N = 2
    theta = np.pi * np.linspace(20, 20, N) / 180
    x1 = np.linspace(-1, 1, N)
    y1 = np.linspace(0, 0, N)
    z1 = np.linspace(-2, -2, N)
    null = np.linspace(0, 0, N)
    one = np.linspace(1, 1, N)
    T = np.linspace(np.radians(0), np.radians(0), N)
    rotation = 1
    if rotation == 1:  # x-rotation
        R11, R12, R13 = one, null, null
        R21, R22, R23 = null, one * np.cos(T), -one * np.sin(T)
        R31, R32, R33 = null, one * np.sin(T), one * np.cos(T)
    if rotation == 2:  # y-rotation
        R11, R12, R13 = one * np.cos(T), null, one * np.sin(T)
        R21, R22, R23 = null, one, null
        R31, R32, R33 = -one * np.sin(T), null, one * np.cos(T)
    if rotation == 3:  # z-rotation
        R11, R12, R13 = one * np.cos(T), -one * np.sin(T), null
        R21, R22, R23 = one * np.sin(T), one * np.cos(T), null
        R31, R32, R33 = null, null, one
    array_in_test = np.zeros((N, 32))
    array_in_test[:, 0] = theta
    array_in_test[:, 14] = R11
    array_in_test[:, 15] = R12
    array_in_test[:, 16] = R13
    array_in_test[:, 17] = R21
    array_in_test[:, 18] = R22
    array_in_test[:, 19] = R23
    array_in_test[:, 20] = R31
    array_in_test[:, 21] = R32
    array_in_test[:, 22] = R33
    array_in_test[:, 2] = x1
    array_in_test[:, 3] = y1
    array_in_test[:, 4] = z1

    h, v, d, data, voxel_r, dnsy, lim = build_voxels(51, 2.5)
    # process = psutil.Process(os.getpid())
    # base_memory_usage = process.memory_info().rss
    # start = timer()
    root_points = 100
    points = cones_generator(array_in_test, root_points, lim)
    data = voxel_fit(h, v, d, points, data.shape, voxel_r)
    # data[25, 25, 40] = 40
    # for n in np.linspace(0, N, 20):
    #     points = cones_generator(array_in_test[int(n):int(n+N/20)], 100, -2.5, 2.5, -2.5, 2.5)
    #     data += voxel_fit(h, v, d, points)
    # print(f"{timer()-start}", "seconds")
    # lmu = process.memory_info().rss - base_memory_usage
    # print(f'memory used {lmu}')

    ''' Drawing all that '''
    fig, ax = F5.draw(h, v, d, dnsy, data, voxel_r)
    plt.show()
