# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:11:04 2024

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

N = 1000000
theta = np.linspace(1, 180, N)
theta = np.divide(np.multiply(theta,np.pi),180)
E0 = 200 #kev
Me = 510.99895000 #kev
scab = np.zeros((2,N), dtype = int)
scab[0] = np.random.randint(1,5+1, N)
scab[1] = np.random.randint(6,10+1,N)

def test_energy(theta, E0, Me):
    T = np.subtract(1,np.cos(theta))
    E2 = np.divide(np.multiply(E0,T),Me)
    E2 = np.divide(E0, np.add(E2,1))
    return E2

E2 = test_energy(theta, E0, Me)
E1 = E0-E2
array_in = np.empty((N,5), dtype=np.float32)
#print(array_in)
array_in[:,0] = E1
array_in[:,1] = E2
array_in[:,5] = scab[0]
array_in[:,4] = scab[1]

print(array_in)


r, c = np.shape(array_in)
a = np.empty((N,4), dtype=np.float32)
def compton_function(a, array_in, E0, Me):
    '''
    Calculates the compton scattering angle from the energies 
    
    Parameters
    ----------
    
    a : static array of N rows and 3 columns
    
    array_in : array of 4 columns and N rows
        column 0 : float
            E1: the energy deposited at the scatterer
        column 1 : float
            E2: the energy deposited at the aborber
        column 2 : float
            dE1 : scatterer energy uncertainty
        column 3 : float
            dE2 : absorber energy uncertainty
        column 4 : integer
            Sc: the index of the scatterer
        column 5 : integer
            Ab : the index of the absorber
            
    E0: float
        the energy of the initial photon
    Me : float
        the rest energy of the electron equal to me*c^2 where me is the 
        electron mass and c is the speed of light 
    Ensure E0 and Me are in identical energy units to those given in the array
    for E1 and E2
    
    Returns
    -------
    output : static array of N rows and 3 columns
        column 0 : float32
            theta: compton scattering angle defining a cone of possible origins
        column 1 : integer
            Sc: the index of the scatterer
        column 2 : integer
            Ab : the index of the absorber

    '''#find an accepted value for Me and set it to a constant arg
    En = np.divide(Me,E0) #float
    a[:,3] = array_in[:,4]
    a[:,4] = array_in[:,5]
    a[:,0] = np.divide(array_in[:,0],array_in[:,1]) #E1/E2
    a[:,0] = np.multiply(En, a[:,0])
    a[:,0] = np.subtract(1,a[:,0])
    a[:,0] = np.arccos(a[:,0]) 
    #we do not expect an angle greater than 90 degrees. 
    #so we expect the domain of arccos to be 0<= Cos <= 1, but it will function
    #for angles between 90 and 180. 
    
    #degree return for development only
    #a[:,0] = (180/np.pi)*np.arccos(a[:,0])
    
    #legacy error propogation: to be reimplemented later with corrected terms.
    #percent=((E0_err/E0)^2+(E1_err/E1)^2+(E2_err/E2)^2+(Me_err/Me)^2)
    #cos_err=np.multiply(C,np.sqrt(percent))
    #theta_err=cos_err/np.sin(theta)
    #return np.array([theta, theta_err])
    
    return a


a = compton_function(a, array_in, E0, Me)
print (a)

theta_result = a[:,0]
perc = np.multiply(np.divide(np.abs(np.subtract(theta,theta_result)),theta),100)
#print(perc)
avg_perc = np.mean(perc)
#print(f'error percentage = {avg_perc}% deviation from expected angle.')
degree_error_avg = avg_perc*180/(np.pi*100)
#print(f'or about {degree_error_avg} degrees')
