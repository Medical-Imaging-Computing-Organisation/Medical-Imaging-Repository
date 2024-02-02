# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:10:14 2024

@author: Adam Andrews
"""

'''
function 1 output [[theta, dtheta, Scatterer Index, Absorber Index], [...], [...]]
function 2 output [[x1, y1, z1, dx1, dy1, dz1, bx, by, bz, dbx, dby, dbz,
                    R11, R12, R13, R21, R22, R23, R31, R32, R33,
                    dR11, dR12, dR13, dR21, dR22, dR23, dR31, dR32, dR33,
                    Scatterer Index, Absorber Index], [...], [...]]
SI is index #29, AI is #30

function 3 (this) output [[theta, dtheta, OA vector, dOA, BA vector, dBA, Rotation Matrix, dR], [...]]

OA = scatterer position vector   x1, y1, z1
BA = absorber -> scatterer vector bx, by, bz
Rotation matrix R11, R12, R13, R21, R22, R23, R31, R32, R33
'''

import numpy as np

'''This function works as long as there are no duplicates in the
    function2 output of scatter index/absorber index pairs'''


def PutEmTogether(f1, f2):
    f3 = np.zeros((f1.shape[0], f2.shape[1]))
    f3[:, 0:2] = f1[:, 0:2]  # theta and dtheta
    idx = np.where((f1[:, 2:4] == f2[:, 29:31][:, None]).all(-1))[0][:f1.shape[0]]
    f3[:, 2:] = f2[idx, 0:29]  # rest of row
    return f3


if __name__ == "__main__":
    f1 = np.ones((4, 4))
    f2 = np.ones((5, 31))
    f2[0, 29:31] = [0, 0]
    f2[1, 29:31] = [0, 1]
    f2[2, 29:31] = [1, 0]
    f2[3, 29:31] = [1, 1]
    f2[4, 29:31] = [0, 2]
    f3result = PutEmTogether(f1, f2)
    # print(f3result[0])
