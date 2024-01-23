# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:05:11 2024

@author: Richard Malone
"""
import numpy as np
#np.array([[E1, E2, scatterer index, absorber index],
#          [E1, E2, scatterer index, absorber index]])
#array is a 4xN array
def compton_function(array, E0, Me):
    '''
    Calculates the compton scattering angle from the energies 
    
    Parameters
    ----------
    array : array of 4 columns and large number of rows.
        column 0 : float?
            E1: the energy deposited at the scatterer
        column 1 : float?
            E2: the energy deposited at the aborber
        column 2 : integer
            Sc: the index of the scatterer
        column 3 : integer
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
    output : array of 3 columns and same number of rows (hopefully)
        column 0 : float?
            theta: compton scattering angle defining a cone of possible origins
        column 1 : integer
            Sc: the index of the scatterer
        column 2 : integer
            Ab : the index of the absorber

    '''#find an accepted value for Me and set it to a constant arg
    TA = np.transpose(array)
    E1 = TA[0]
    E2 = TA[1]
    MeE2 = np.multiply(Me,E2) #E2 array multiplied by constant
    E0E1 = np.multiply(E0,E1) #E1 array multiplied by constant
    C = np.divide(MeE2,E0E1) #E2 array divided by E1 array
    Cos = np.subtract(1,C)
    theta = np.arccos(Cos) #we do not expect an angle greater than 90 degrees. 
    #so we expect the domain of arccos to be 0<= Cos <= 1
    TB = np.array([theta,TA[2], TA[3]])
    output = np.transpose(TB)
    
    
    #legacy error propogation:
    #percent=((E0_err/E0)^2+(E1_err/E1)^2+(E2_err/E2)^2+(Me_err/Me)^2)
    #cos_err=np.multiply(C,np.sqrt(percent))
    #theta_err=cos_err/np.sin(theta)
    #return np.array([theta, theta_err])
    
    return output