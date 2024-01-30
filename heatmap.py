

# importing required libraries

from numba import njit
import numpy as np
# import cupy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
from timeit import default_timer as timer


try:
    plt.close()
finally:
    pass

'''
h, v, d = np.meshgrid(x, y, z)
h[x, y, z], v[x, y, z],  d[x, y, z] = hoz, vert, depth coords
data[x, y, z] = value
'''

''' Building voxel grid '''
dnsy = 51  # number density operator
lim = 2.5  # extension of area in all directions from origin
voxel_r = lim/dnsy  # voxel radius
x = np.linspace(-lim+voxel_r, lim-voxel_r, dnsy, endpoint=True)
y, z = x, x  # cube dimensions
h, v, d = np.meshgrid(x, y, z, sparse=False)  # Horizontal, vertical, depth
data = np.zeros((dnsy, dnsy, dnsy))  # empty dataset
# data = np.arange(1, 1+dnsy**3).reshape(dnsy, dnsy, dnsy)
# index = (0, 0, 0)
# print(data[index], "loc", h[index], v[index], d[index])


# @njit(parallel=True)
# @njit
def voxel_fit(h, v, d, xyz):

    '''Fitting into voxels'''
    # usually cone_points will be xyz
    data1 = np.zeros(data.shape)  # temporary dataset
    cs = np.digitize(xyz, h[0, :, 0]+voxel_r, right=True)
    # returns indices for xyz bins to fit into voxels
    # data1[cs[:, 0], cs[:, 1], cs[:, 2]] = 1  # if no dupe
    np.add.at(data1, (cs[:, 0], cs[:, 1], cs[:, 2]), 1)  # if dupe
    # for abc in cs:  #njit friendly version
    #     data1[abc[0], abc[1], abc[2]] += 1
    # adds 1 to every voxel specified, including duplicate indices
    return data1

start=timer()
for a in range(30):  # for now one cone is repeated
    '''Generating xyz points, to be replaced'''
    y, z = np.linspace(-lim, lim, 10*dnsy), np.linspace(-lim, lim, 10*dnsy)
    np.random.shuffle(y)
    x = 2*np.sqrt(y**2+z**2)-2.5
    cone_points = np.vstack((x, y, z)).T
    xyz = np.delete(cone_points, np.where(np.abs(cone_points) > lim)[0], axis=0)
    data += voxel_fit(h, v, d, xyz)
print(timer()-start)

''' Drawing all that '''
fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(12, 6),
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

# ax[1].voxels(np.ones(data.shape), alpha=0.12, edgecolor="k", shade=True)  # Voxel visualization
'''Could be choosing to plot the hottest planes?
    This actually needs to consider the hottest "volume"
    otherwise different planes could be plotted'''
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
# plt.tight_layout()
plt.show()
