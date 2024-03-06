import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
import scipy.ndimage as ndimage


def draw(h, v, d, dnsy, data, vr, dpa=None):
    def mosaic():
        fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(10, 5),
                    per_subplot_kw={1: {'projection': '3d', 'xlabel': 'X axis', 'ylabel': 'Y axis', 'zlabel': 'Z axis'},
                                     2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                                     3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                                     4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'}})
        plt.tight_layout()
        return fig, ax

    def cmap():
        try:  # Colour map creation in try-catch to prevent recreation error
            color_array = plt.get_cmap('YlOrRd')(range(256))
            color_array[:, -1] = np.linspace(0.0, 1.0, 256)**1.5
            map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
            plt.colormaps.register(cmap=map_object)
        except ValueError:
            pass

    def xyz(data):
        '''Draw main 3D XYZ scatter plot'''
        XYZ = ax[1].scatter(h, v, d, marker='s', s=2000 / dnsy, c=data, cmap="YlOrRd_alpha2")
        plt.colorbar(XYZ, location='left')  # plots 3D heatmap

    def gaussing():
        '''Gauss view'''
        gaussed = ndimage.gaussian_filter(data, 1)
        hottest = np.max(gaussed)
        std = np.std(gaussed)
        hotfinder, hotfinds = ndimage.label((gaussed >= hottest-1*std)*1)  # labels clusters of near hottest
        H = [list(zip(*np.where(hotfinder == k))) for k in range(1, hotfinds+1)]  # compiles indices of each cluster
        highcluster = np.argmax([np.sum([gaussed[I] for I in H[i]]) for i in range(len(H))])+1  # selects highest cluster sum
        hotfinder2 = (hotfinder == highcluster)*1  # selects only highest cluster and norms to 1
        if len(H[highcluster-1]) == 1:
            com = H[highcluster-1][0]
            loc = np.array([h[com], v[com], d[com]])
            locvar = [vr, vr, vr]
            var = [1, 1, 1]
            return loc, com, locvar, var, hotfinder2
        else:
            pass

        com = ndimage.center_of_mass(data, labels=hotfinder2)  # locates centre of mass indices
        loc = np.interp(np.array(com), np.arange(h.shape[0]), h[0, :, 0])  # interpolates indices into locations
        loc[0:2] = loc[1::-1]  # swaps yxz into xyz

        ax[1].scatter(loc[0], loc[1], loc[2], marker='o', s=100, alpha=0.5)  # source located graph

        sizes = np.mean(np.abs(np.array(H[highcluster-1])-np.array(com)), axis=0)
        locvar = sizes*2*vr  # variation in real distance
        locvar[locvar == 0] = vr

        var = np.ceil(sizes).astype(int)  # rounds plane var up
        print("Plane depths", var)
        com = tuple(np.rint(com).astype(int))  # rounds com decimals to integer indices

        ax[1].plot([loc[0]]*2, [loc[1]]*2, [loc[2]-locvar[2], loc[2]+locvar[2]])
        ax[1].plot([loc[0]]*2, [loc[1]-locvar[1], loc[1]+locvar[1]], [loc[2]]*2)
        ax[1].plot([loc[0]-locvar[0], loc[0]+locvar[0]], [loc[1]]*2, [loc[2]]*2)

        return loc, com, locvar, var, (hotfinder!=0)*data

    def planars(com, var):
        '''Planar views'''
        XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[com[0] - var[0]:com[0] + var[0] + 1, :, :], axis=0), cmap="YlOrRd")
        plt.colorbar(XZ)  # X-Z and Y-Z colour maps
        YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, com[1] - var[1]:com[1] + var[1] + 1, :], axis=1), cmap="YlOrRd")
        plt.colorbar(YZ)
        XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, com[2] - var[2]:com[2] + var[2] + 1], axis=2).T, cmap="YlOrRd")
        plt.colorbar(XY)

    def info(loc, locvar):
        ax[1].set_title('3D Graph', va='top', fontsize=13)
        loclabel = (f'Predicted source location at:\n' +
                    f'X: %.5f $\\pm$ %.5f m\n' % (loc[0], locvar[0]) +
                    f'Y: %.5f $\\pm$ %.5f m\n' % (loc[1], locvar[1]) +
                    f'Z: %.5f $\\pm$ %.5f m' % (loc[2], locvar[2]))  # Location of hottest voxel
        lim = np.max(h) + vr
        ax[1].set_ylim([-lim, lim])
        ax[1].set_xlim([-lim, lim])
        ax[1].set_zlim([-lim, lim])
        ax[2].text(x=-6.5 * lim, y=0, s=loclabel)

        '''Detector locations plotted & labeled'''
        if dpa is not None:
            ax[1].scatter(0.01 * dpa[:, 1], 0.01 * dpa[:, 2], 0.01 * dpa[:, 3],
                          marker='o', s=100, alpha=0.6, c=dpa[:, 0],
                          cmap='gist_rainbow')
            for i in range(dpa.shape[0]):
                ax[1].text(x=0.01 * dpa[i, 1], y=0.01 * dpa[i, 2],
                           z=0.01 * dpa[i, 3], s=str(int(dpa[i, 0])),
                           ha='center', va='center', clip_on=True)  # Numbers labeled
    fig, ax = mosaic()
    cmap()

    loc, com, locvar, var, hotfinder = gaussing()
    xyz(data)
    planars(com, var)
    info(loc, locvar)
    return fig, ax
