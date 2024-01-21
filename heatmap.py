

# importing required libraries

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC


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
dnsy = 21  # number density operator
lim = 2.5  # extension of area in all directions from origin
voxel_r = lim/dnsy  # voxel radius
x = np.linspace(-lim+voxel_r, lim-voxel_r, dnsy, endpoint=True)
y, z = x, x  # cube dimensions
h, v, d = np.meshgrid(x, y, z, sparse=False)  # Horizontal, vertical, depth
data = np.zeros((dnsy, dnsy, dnsy))  # empty dataset
# data = np.arange(1, 1+dnsy**3).reshape(dnsy, dnsy, dnsy)
# index = (0, 0, 0)
# print(data[index], "loc", h[index], v[index], d[index])


def cone_something(h, v, d):
    '''Generating xyz points, to be replaced'''
    x, y = np.linspace(-lim, lim, dnsy), np.linspace(-lim, lim, dnsy)
    np.random.shuffle(x)
    z = 2*np.sqrt(x**2+y**2)-2.5
    cone_points = np.vstack((x, y, z)).T
    cone_points = np.delete(cone_points, np.where(abs(cone_points) > lim)[0], axis=0)
    '''Fitting into voxels'''
    data1 = np.zeros((dnsy, dnsy, dnsy))  # temporary dataset
    cs = np.digitize(cone_points, h[0, :, 0]+voxel_r, right=True)
    # returns indices for xyz bins to fit into voxels
    for xyz in cs:
        data1[tuple(xyz)] = 1
        # sets temp dataset points to 1 to avoid double registration
    return data1


for a in range(300):  # for now one cone is repeated
    data += cone_something(h, v, d)


''' Drawing all that '''
fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3]], figsize=(12, 6),
             per_subplot_kw={1: {'projection': '3d', 'xlabel': 'x', 'ylabel': 'y', 'zlabel': 'z'},
                             2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                             3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'}})

try:  # Colour map creation in try to prevent recreation error
    color_array = plt.get_cmap('YlOrRd')(range(256))
    color_array[:, -1] = np.linspace(0.0, 1.0, 256)
    map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
    plt.colormaps.register(cmap=map_object)
except ValueError:
    pass
XYZ = ax[1].scatter(h, v, d, marker='s', s=150, c=data, cmap="YlOrRd_alpha2")
plt.colorbar(XYZ, location='left')

# ax[1].voxels(np.ones(data.shape), alpha=0.12, edgecolor="k", shade=True)  # Voxel visualization
XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data, axis=0), cmap="YlOrRd")
cb2 = plt.colorbar(XZ)  # X-Z and Y-Z colour maps
YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data, axis=1), cmap="YlOrRd")
cb3 = plt.colorbar(YZ)


ax[1].set_title('3D Graph')
ax[1].set_zlim(-lim, lim)
plt.tight_layout()
plt.show()
