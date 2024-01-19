# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 16:27:34 2024

@author: Richard Malone
"""
import numpy as np
import scipy as sp

def betavector(x1, y1, z1, x2, y2, z2):
    '''
    Ensure all inputs bare the same length units.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    beta : Array
        the vector defining the direction of the cone axis from the detectors.
    '''
    dx=x1-x2
    dy=y1-y2
    dz=z1-z2
    beta=np.array([dx,dy,dz])
    return beta

class detpair:
    '''
    go from r(absorb) to r(scat) to create the axis of the cone.
    create functions that take energies and return cone axis angles,
    using uvw coordinates as spherical polars about the cone axis. 
    Cone axis = polar axis. 
    
    Ensure all positions are in the samw units.
    '''
    def __init__(self, scatt, absorb):
        self.x1 = scatt[0]
        self.y1 = scatt[1]
        self.z1 = scatt[2]
        self.x2 = absorb[0]
        self.y2 = absorb[1]
        self.z2 = absorb[2]
        
        self.beta = betavector(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)
        self.b = np.squareroot(np.sum(np.square(beta)))
        self.bt = np.squareroot(np.sum(np.square(beta[0]),np.square(beta[1])))
        self.bts = np.square(bt)
        self.btb = np.multiply(bt,b)
        self.psi = np.divide(np.multiply(dx,dy),bts)
        self.delt = np.divide(np.multiply(dz,dx),btb)
        self.gam = np.divide(np.multiply(dz,dy),btb)
        self.Y = np.divide(dy,b)
        self.Xs = np.square(np.divide(dx,bt))
        #we want the above to be ran only once for each detector pair. 
    def cone_angle(self, E0, E0_err, E1, E1_err, E2, E2_err, Me, Me_err = 0):
        '''
        Ensure all inputs bare the same energy units, especially the electron rest energy E=Me*c^2
        Parameters
        ----------
        E0 : Float
            The initial photon energy.
        E1 : Flaot
            The energy deposited during the compton scatter.
        E2 : Float
            The energy of the scattered photon.
        Me : Float
            The rest energy of the electron
        Returns
        -------
        theta : Float
            The angle of the compton cone from the w axis. 
        theta_err : Float
            The error on the angle as derived from the compton energy equation.
        '''
        C = Me*E2/(E0*E1)
        Cos = 1-C
        theta = np.arccos(Cos)
        percent=((E0_err/E0)^2+(E1_err/E1)^2+(E2_err/E2)^2+(Me_err/Me)^2)
        cos_err=C*np.sqrt(percent)
        theta_err=cos_err/np.sin(theta)
        return np.array([theta, theta_err])   
        
    def coneequations(self, x, y, theta):
        '''
        
        Parameters
        ----------
        x : Float
            The x-axis position in the master frame
        y : Float
            The y-axis position in the master frame
        theta: Flaot
            The cone angle to generate
        Returns
        -------
        z_plus : Float
            the plus solution to the z position of the cone equation
        z_minus: Float
            the minus solution to the z position of the cone equation.
        '''
        #anything below this will probably be ran thousands, possibly millions of times to produce an image
        dx = self.beta[0]
        dy = self.beta[1]
        dz = self.beta[2]
        N = x-self.x1
        M = y-self.y1
        Tan = np.square(np.tan(theta))
        j = np.multiply(2, self.z1) - np.multiply(M, self.psi)
        c= np.multiply(N,dz) - np.multiply(M, dx) - np.multiply(dy, self.z1)
        o = np.square(M*dy/self.bt)
        h = np.multiply(np.square(self.z1), self.Xs)
        m = -np.multiply(M,self.psi,self.z1)
        ohm = o+h+m
        d = np.multiply(N,self.bt) + np.multiply(M,self.delt) - np.multiply(self.gam,self.z1)
        
        A = np.square(self.gam) + np.square(self.Y) - np.multiply(Tan, self.Xs)
        B = np.multiply(2,c,self.Y)+np.multiply(2,d,self.gam)+np.multiply(Tan, j)
        C = np.square(c)+np.square(d)-np.multiply(ohm, Tan)
        
        T1 = B/(np.multiply(2,A))
        T2 = np.sqrt((np.square(T1))-(C/A))
        
        z_plus =-T1+T2
        z_minus =-T1-T2
        return....?
    