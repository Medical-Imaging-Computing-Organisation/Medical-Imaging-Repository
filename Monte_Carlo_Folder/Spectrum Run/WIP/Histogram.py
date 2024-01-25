# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:49:26 2024

@author: izarl
"""

import numpy as np
import matplotlib.pyplot as plt
#list of 'energy depositions'
data = (0.662, 0.279437, 0.662, 0.11558, 0.662, 0.662, 0, 0, 0, 0.464853, 0, 0.0735088, 0.227799, 0, 0.14008, 0.158194, 0.662, 0, 0.662, 0.402767, 0, 0.662, 0, 0, 0.662, 0.662, 0, 0.100902, 0.191709, 0.662, 0, 0.402302, 0.315699, 0, 0, 0.662, 0.662, 0.00365875, 0, 0.662, 0.662, 0.213026, 0.027503, 0, 0.662, 0, 0.323569, 0.662, 0.662, 0.262805)
data = sorted(data)
setlist = sorted(list(set(data)))
energy_dep = {}
for i in data:
    if i not in energy_dep:
        energy_dep[i] = 1
    else:
        energy_dep[i] += 1
countlist = list(energy_dep.values())
print(countlist)
print(setlist)

plt.figure('Histogram of Energy Depositions')
plt.xlabel('Energy deposition (Mev)')
plt.ylabel('Count')
plt.title('Number Of Times Energy Is Deposited')
plt.plot(setlist, countlist, color ='k')




        

