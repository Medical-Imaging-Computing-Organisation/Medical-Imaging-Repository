import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC


def draw(h, v, d, dnsy, data, voxel_r):
    fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(10, 5),
                                 per_subplot_kw={1: {'projection': '3d', 'xlabel': 'x', 'ylabel': 'y', 'zlabel': 'z'},
                                                 2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                                                 3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                                                 4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'}})

    try:  # Colour map creation in try to prevent recreation error
        color_array = plt.get_cmap('YlOrRd')(range(256))
        color_array[:, -1] = np.linspace(0.0, 1.0, 256)
        map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
        plt.colormaps.register(cmap=map_object)
    except ValueError:
        pass

    XYZ = ax[1].scatter(h, v, d, marker='s', s=2000 / dnsy, c=data, cmap="YlOrRd_alpha2")
    plt.colorbar(XYZ, location='left')

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
    stdevdist = std * voxel_r
    var = int(stdevdist // (2 * voxel_r))
    print("Plane depth", var)
    # var = int
    XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[hot[0] - var:hot[0] + var + 1, :, :], axis=0), cmap="YlOrRd")
    cb2 = plt.colorbar(XZ)  # X-Z and Y-Z colour maps
    YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, hot[1] - var:hot[1] + var + 1, :], axis=1), cmap="YlOrRd")
    cb3 = plt.colorbar(YZ)
    XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, hot[2] - var:hot[2] + var + 1], axis=2).T, cmap="YlOrRd")
    cb4 = plt.colorbar(XY)
    ax[1].set_title('3D Graph')
    loclabel = ("Hottest voxel found at:\nX: %.5f\nY: %.5f\nZ: %.5f"
                % (h[hot], v[hot], d[hot]))
    ax[2].text(x=-15, y=0, s=loclabel)
    plt.tight_layout()
    return fig, ax
