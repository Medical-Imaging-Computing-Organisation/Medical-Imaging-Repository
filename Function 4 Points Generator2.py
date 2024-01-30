# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:07:55 2024

@author: Richard Malone
"""
import numpy as np
import matplotlib.pyplot as plt
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

p = 20
x_min = -5
x_max = 5
y_min = -5
y_max = 5
x = np.linspace(x_min, x_max, p)
y = np.linspace(y_min, y_max, p)
grid = np.meshgrid(x,y)
P = np.square(p)
x = np.ndarray.flatten(grid[0])
y = np.ndarray.flatten(grid[1])

    
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
    r = np.multiply(np.square(P),N)
    points_trn = np.zeros((r, 3))
    for pr in range(P):
        u = x[pr] #x coordinate in the cone frame
        v = y[pr] #y coordinate in the cone frame
        theta = a[:,0] #column of cone angles
        w = cone(u,v,theta) #zsize=P, z coordinate in cone frame
        null = np.linspace(0,0,N)
        u = null + u #u point cast to the number of w points
        v = null + v #v point cast to a number of w points
        #points = np.array([X,Y,z])
        #R11 = array_in[:,14]  #coefficients of the rotation matrix
        #R12 = array_in[:,15] 
        #R13 = array_in[:,16]
        #R21 = array_in[:,17] 
        #R22 = array_in[:,18]
        #R23 = array_in[:,19]
        #R31 = array_in[:,20]
        #R32 = array_in[:,21] 
        #R33 = array_in[:,22]
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

    #for i in range(r):
        #cond = points_trn[i][0]<Lmax & points_trn[i][1]<Lmax & points_trn[i][2]<Lmax
        #points_trn[i] = np.where(cond, points_trn[i],0)
    #points_trn = np.where(np.max(points_trn)<Lmax, points_trn, np.array([0,0,0]))
    points_trn = np.delete(points_trn, np.where(np.abs(points_trn)>Lmax)[0], axis = 0)
    print(f'\n plotted {points_trn.size}points')
    return points_trn
#test data
N = 100
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

points = cones_generator(array_in_test, 10, -5, 5, -5, 5)


#diagnostic 3D plot
R=5
#phi=(np.pi/180)*(45)
#theta=(np.pi/180)*(90)

i = [1, 0, 0]
j = [0, 1, 0]
k = [0, 0, 1]
#r = [R*np.cos(phi)*np.sin(theta), R*np.sin(phi)*np.sin(theta), R*np.cos(theta)]
fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.set_xlim(-5, 5)
ax.set_xlabel('x')
ax.set_ylim(-5, 5)
ax.set_ylabel('y')
ax.set_zlim(-5, 5)
ax.set_zlabel('z')

#ax.quiver(0, 0, 0, r[0], r[1], r[2], color = 'r')
ax.quiver(0, 0, 0, i[0], i[1], i[2], color = 'b')
ax.quiver(0, 0, 0, j[0], j[1], j[2], color = 'y')
ax.quiver(0, 0, 0, k[0], k[1], k[2], color = 'g')

ax.scatter(points[:,0], points[:,1], points[:,2])
ax.view_init(45,45)
