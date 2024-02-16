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
import Function1 as F1
import Function2 as F2
import Function3 as F3


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
def cones_generator(a, p, Lmax):
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
    # print(vector)
    vector = np.einsum('...jk,...k', rotMatrix, vector)
    vector += a[:, 2:5]
    vector = vector.reshape((r, 3))
    # vector[:,0:2] -= 2.5
    vector = np.delete(vector, np.where(np.abs(vector) > Lmax)[0], axis=0)
    # lmu = process.memory_info().rss - base_memory_usage
    # print(f'memory used {lmu}')
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
    '''function 12->4 data'''
    
    #function 1 test data
    #np.array([[E1, E2, scatterer_index, absorber_index],[E1, E2, scatterer_index, absorber_index]])
    # array is a 4xN array
    N = 10
    theta = np.linspace(45, 45, N)
    theta = np.divide(np.multiply(theta,np.pi),180)
    E0 = 0.662 #Mev
    dE0 = 3E-5 #MeV
    Me = 0.51099895000 #Mev
    scab = np.zeros((2,N), dtype = int)
    scab[0] = np.random.randint(0,1+1, N)
    scab[1] = np.random.randint(2,3+1,N)

    def test_energy(theta, E0, Me):
        T = np.subtract(1,np.cos(theta))
        E2 = np.divide(np.multiply(E0,T),Me)
        E2 = np.divide(E0, np.add(E2,1))
        return E2

    E2 = test_energy(theta, E0, Me)
    E1 = E0-E2
    array_in = np.empty((N,6), dtype=np.float32)
    print(array_in)
    array_in[:,0] = E1
    array_in[:,1] = E2
    array_in[:,4] = scab[0]
    array_in[:,5] = scab[1]
    print(array_in)

    r, c = np.shape(array_in)
    a1 = np.empty((N,4), dtype=np.float32)
    a1 = F1.compton_function(a1, array_in, E0, dE0, Me)
    # #print (a)
    # theta_result = a1[:,0]
    # perc = np.multiply(np.divide(np.abs(np.subtract(theta,theta_result)),theta),100)
    # #print(perc)
    # avg_perc = np.mean(perc)
    # print(f'error percentage = {avg_perc}% deviation from expected angle.')
    # degree_error_avg = avg_perc*180/(np.pi*100)
    # print(f'or about {degree_error_avg} degrees')
    
    #function 2 test data, takes both F1 input and positional input
    #input to function 2
    '''[[Detector Index, x, y, z, Delta x, Delta y, Delta z, Sc/Ab], ...]'''
    
    #a2 = np.empty((D,))
    a2 = np.array([[   0,   75,   75,  -50,    0,    0,    0,],
                   [   1,   75,   75,   50,    0,    0,    0,],
                   [   2,  170,  120, -120,    0,    0,    0,],
                   [   3,  130,  160,  120,    0,    0,    0,]])
    a2 = F2.Generate_Position_Vectors_And_Matrices(array_in, a2)
    #output from function 2 
    '''[[x1, y1, z1, Delta x1, Delta y1, Delta z1, Bx, By, Bz, Delta Bx, Delta By, 
                    Delta Bz, R11, R12, R13, R21, R22, R23, R31, R32, R33, Delta R11, Delta R12, 
                    Delta R13, Delta R21, Delta R22, Delta R23, Delta R31, Delta R32, Delta R33, 
                    Scatterer Index, Absorber Index],  ... ]'''
    a3 = F3.PutEmTogether(a1,a2)
    '''[[theta, dtheta, x1, y1, z1, dx1, dy1, dz1, bx, by, bz, dbx, dby, dbz, 
        R11, R12, R13, R21, R22, R23, R31, R32, R33, Delta R11, Delta R12, 
        Delta R13, Delta R21, Delta R22, Delta R23, Delta R31, Delta R32, 
        Delta R33], 
        [...]]'''
    
    Lmax = 2.5
    root_points = 1000
    points = cones_generator(a3, root_points, Lmax)
    
    theta_result = a3[:,0]
    perc = np.multiply(np.divide(np.abs(np.subtract(theta,theta_result)),theta),100)
    #print(perc)
    avg_perc = np.mean(perc)
    print(f'error percentage = {avg_perc}% deviation from expected angle.')
    degree_error_avg = avg_perc*180/(np.pi*100)
    print(f'or about {degree_error_avg} degrees')
    

    
    # test data for function 4
    func4 = False
    if func4 == True:
        N = 2
        theta = np.pi * np.linspace(45, 45, N) / 180
        x1 = np.linspace(0, 0, N)
        y1 = np.linspace(0, 0, N)
        z1 = np.linspace(0, 0, N)
        null = np.linspace(0, 0, N)
        one = np.linspace(1, 1, N)
        T = np.linspace(0, np.radians(90), N)
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
        root_points = 1000
        points = cones_generator(array_in_test, root_points, lim)

    h, v, d, data, voxel_r, dnsy, lim = build_voxels(51, 2.5)
    # process = psutil.Process(os.getpid())
    # base_memory_usage = process.memory_info().rss
    # start = timer()
    data = voxel_fit(h, v, d, points, data.shape, voxel_r)
    # data[25, 25, 40] = 40
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
                                                 4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'}})

    try:  # Colour map creation in try to prevent recreation error
        color_array = plt.get_cmap('YlOrRd')(range(256))
        color_array[:, -1] = np.linspace(0.0, 1.0, 256)
        map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
        plt.colormaps.register(cmap=map_object)
    except ValueError:
        pass

    XYZ = ax[1].scatter(h, v, d, marker='s', s=2000 / dnsy, c=data, cmap="YlOrRd_alpha2")
    plt.colorbar(XYZ, location='left')

    hottest = np.max(data)
    hot = np.unravel_index(np.argmax(data), data.shape)
    std = np.std(data)
    # hotfinder, _ = nd.label((data >= hottest-10*std)*1)
    # hotarea = np.bincount(hotfinder.ravel())[1:]
    # print(hotarea)
    # hotdev = hotarea.mean()/2
    # print(hotarea, hotdev, "hot mean radius", std)
    # XYZ = ax[1].scatter(h, v, d, marker='s', s=2000 / dnsy, c=hotfinder, cmap="YlOrRd_alpha2")
    # plt.colorbar(XYZ, location='left')
    stdevdist = 1
    var = int((stdevdist) // (2 * voxel_r))  # NAH
    print("Plane depth", var)
    # var = int
    XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[hot[0] - var:hot[0] + var + 1, :, :], axis=0), cmap="YlOrRd")
    cb2 = plt.colorbar(XZ)  # X-Z and Y-Z colour maps
    YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, hot[1] - var:hot[1] + var + 1, :], axis=1), cmap="YlOrRd")
    cb3 = plt.colorbar(YZ)
    XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, hot[2] - var:hot[2] + var + 1], axis=2).T, cmap="YlOrRd")
    cb4 = plt.colorbar(XY)
    ax[1].set_title('3D Graph')
    loclabel = ("Hottest voxel found at:\nX: %.5f\nY: %.5f\nZ: %.5f"
                % (h[hot], v[hot], d[hot]))
    ax[2].text(x=-15, y=0, s=loclabel)
    plt.tight_layout()
    print(voxel_r)
    plt.show()
