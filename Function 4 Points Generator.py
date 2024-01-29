# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:57:33 2024

@author: Richard Malone
"""
'''
Parallising Version
'''
import numpy as np


'''
Function 1 (Richard)
-------------------
'Calculate Angles: From the Coincidence Detection output array 
[[E1, E2, scatterer index, absorber index], 
[E1, E2, scatterer index, absorber index], ...], 
use Compton Kinematics to calculate angles theta. 
Output: 
[[theta, Scatterer Index, Absorber Index], 
[theta, Scatterer Index, Absorber Index] ...]'
'''

#np.array([[E1, E2, scatterer index, absorber index],
#          [E1, E2, scatterer index, absorber index]])
#array is a 4xN array
#array_in is the 

#array_in = np.transpose(data)
#r, c = np.shape(array_in)
a = np.empty((3,r), dtype=float32)



'''
Function 3 (Adam) Merge Arrays: From the outputs of Function 1 and 2, 
merge relevant information into a single array. 
Output; 
[[Vector from Origin to Scatterer, Vector from Absorber to Scatterer, theta, 
  Rotation Matrix], 
 [Vector from Origin to Scatterer, Vector from Absorber to Scatterer, theta, 
  Rotation Matrix] ...]

one dimension of the matrix will be the length of how many events there are:
    N is the number of events, distinct cones to generate
    appended (but not really appending) to that array, we need the positional 
    data to be added
    
    so lets say for easyness
    theta is first. then the detector data. Or mabye theta can just go on the end.
'''

'''
Function 4 (Richard) Generate set of points corresponding to cones: 
    From the output of Function 3, generate a set of points that correspond to 
    those populated by the surfaces of cones. 
    Output: [[x, y, z], [x, y, z] ...]
'''

#if we had a single xyz point, this is the operation we want to carry out. 

def cone(x,y,theta):
    z=np.sqrt(np.square(x),np.square(y))
    z=np.divide(z,np.tan(theta))
    return z
def rotation(x,y,z,R):
    vec = np.array([x,y,z])
    vec_rot = np.matmul([R,vec])
    return vec_rot
def translate(x,y,z,x1,y1,z1):
    vec = np.array([x,y,z])
    vec_sc = np.array([x1,y1,z1])
    vec_tran = vec+vec_sc
    return vec_tran
np.mat

#if we have points in an array([[x,y,z],[x,y,z],...])
def rotation(points,R):
    vec_rot = np.matmult(points,np.transpose(R))
    return vec_rot
def translation(points, vec_sc):
    vec_tran = points + vec_sc
    return vec_tran

#returning points = [[x,y,z],[x,y,z].... which is good, but all for single inputs of theta and R
'''
#we want a function that takes an array of theta and R sets and returns, well...
#if a single theta and Rset returns a 3xP matrix where P is the number of points.

#if we always generate the same number of points we could work with a 3D matrix....right?
#this 3D matrix wouldnt even be too bad, its a 3xPxN matrix where N is the number of events = cones
#at this point N would just be an index of the events, it doesnt have much 
#physical significant other than just keeping one set of cone points separate from the other
#the only issue is if the number of points P needs to vary in order to keep the surface density constant. 
#but we can cross that bridge when we can even see it, let alone come to it.

#alternatively, dynamic memory would allow us to just make this a 2D array of 
#[x,y,z] points stacked into N*P rows by simply appending those points to the matrix, 
#this would be quicker but wouldnt be possible while maintaining static memory 
#unless the number of points and events were known beforehand. plus a bunch of other potential issues.
'''
