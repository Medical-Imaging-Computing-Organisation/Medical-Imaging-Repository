import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC


def draw(h, v, d, dnsy, data, voxel_r, dpa):
    fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(10, 5),
                                 per_subplot_kw={1: {'projection': '3d', 'xlabel': 'X axis', 'ylabel': 'Y axis', 'zlabel': 'Z axis'},
                                                 2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                                                 3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                                                 4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'}})
    plt.tight_layout()

    try:  # Colour map creation in try-catch to prevent recreation error
        color_array = plt.get_cmap('YlOrRd')(range(256))
        color_array[:, -1] = np.linspace(0.0, 1.0, 256)
        map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
        plt.colormaps.register(cmap=map_object)
    except ValueError:
        pass

    XYZ = ax[1].scatter(h, v, d, marker='s', s=2000 / dnsy, c=data, cmap="YlOrRd_alpha2")
    plt.colorbar(XYZ, location='left')  # plots 3D heatmap

    '''weighted average stuff'''
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
    stdevdist = std * 2 * voxel_r
    var = int(stdevdist // (2 * voxel_r))
    print("Plane depth", var)

    '''Planar views'''
    XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[hot[0] - var:hot[0] + var + 1, :, :], axis=0), cmap="YlOrRd")
    cb2 = plt.colorbar(XZ)  # X-Z and Y-Z colour maps
    YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, hot[1] - var:hot[1] + var + 1, :], axis=1), cmap="YlOrRd")
    cb3 = plt.colorbar(YZ)
    XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, hot[2] - var:hot[2] + var + 1], axis=2).T, cmap="YlOrRd")
    cb4 = plt.colorbar(XY)

    ax[1].set_title('3D Graph', va='top', fontsize=13)
    loclabel = ("Hottest voxel found at:\nX: %.5f\nY: %.5f\nZ: %.5f"
                % (h[hot], v[hot], d[hot]))  # Location of hottest voxel
    lim = np.max(h) + voxel_r
    ax[1].set_ylim([-lim, lim])
    ax[1].set_xlim([-lim, lim])
    ax[1].set_zlim([-lim, lim])
    ax[2].text(x=-5.5 * lim, y=0, s=loclabel)
    '''Detector locations plotted & labeled'''
    dets = ax[1].scatter(0.01 * dpa[:, 1], 0.01 * dpa[:, 2],
                         0.01 * dpa[:, 3], marker='o', s=100, alpha=0.6,
                         c=dpa[:, 0], cmap='gist_rainbow')
    for i in range(dpa.shape[0]):
        ax[1].text(x=0.01 * dpa[i, 1], y=0.01 * dpa[i, 2],
                   z=0.01 * dpa[i, 3], s=str(int(dpa[i, 0])),
                   ha='center', va='center', clip_on=True)
    return fig, ax
