import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
import scipy.ndimage as ndimage
import scipy.optimize as opt
import matplotlib.ticker as ticker


def draw(h, v, d, dnsy, data, vr, dpa=None, resolution=None):
    def mosaic():
        if resolution is None:
            fig, ax = plt.subplot_mosaic([[1, 1, 2], [1, 1, 3], [1, 1, 4]], figsize=(10, 5),
                        per_subplot_kw={1: {'projection': '3d', 'xlabel': 'X axis (cm)',
                                            'ylabel': 'Y axis (cm)', 'zlabel': 'Z axis (cm)'},
                                         2: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                                         3: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                                         4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'}})
        else:
            fig, ax = plt.subplot_mosaic([[1, 1, 2, 5], [1, 1, 3, 6], [1, 1, 4, 7]], figsize=(10, 5),
                       per_subplot_kw={1: {'projection': '3d', 'xlabel': 'X axis', 'ylabel': 'Y axis', 'zlabel':'Z axis'},
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

        return loc, com, locvar, var, gaussed #*(hotfinder!=0)

    def planars(data, com, var):
        '''Planar views'''
        XZ = ax[2].pcolormesh(h[0], d[0], np.sum(data[com[0] - var[0]:com[0] + var[0] + 1, :, :], axis=0), cmap="YlOrRd")
        plt.colorbar(XZ)  # X-Z and Y-Z colour maps
        YZ = ax[3].pcolormesh(h[0], d[0], np.sum(data[:, com[1] - var[1]:com[1] + var[1] + 1, :], axis=1), cmap="YlOrRd")
        plt.colorbar(YZ)
        XY = ax[4].pcolormesh(h[0], d[0], np.sum(data[:, :, com[2] - var[2]:com[2] + var[2] + 1], axis=2).T, cmap="YlOrRd")
        plt.colorbar(XY)

    def resolves(hot, loc, locvar, data):
        X = h[0, :, 0]

        def gaussian(x, amplitude, mean, stddev):
            return amplitude * np.exp(-((x - mean)**2)/(2*stddev**2))

        def gaussfwhm(ax, X, popt):
            ax.plot(X, gaussian(X, *popt), lw=2, alpha=.5, color='r')
            ax.plot([popt[1] - np.sqrt(2*np.log(2))*popt[2],
                     popt[1] + np.sqrt(2*np.log(2))*popt[2]],
                    [popt[0]/2]*2, color='r', alpha=0.5)
            print("FWHM", 2*np.sqrt(2*np.log(2))*popt[2])

        def dataplot(ax, X, l, lv, axisdata):
            ax.plot(X, axisdata)
            ax.axvline(x=l - lv, color='g', alpha=.3)
            ax.axvline(x=l, color='g', alpha=.5)
            ax.axvline(x=l + lv, color='g', alpha=.3)
            try:
                popt = opt.curve_fit(gaussian, X, axisdata)
                gaussfwhm(ax, X, popt[0])
            except RuntimeError:
                print("Gauss fit failed")

        dataplot(ax[5], X, loc[0], locvar[0], data[hot[0], :, hot[2]])
        dataplot(ax[6], X, loc[1], locvar[1], data[:, hot[1], hot[2]])
        dataplot(ax[7], X, loc[2], locvar[2], data[hot[0], hot[1], :])


    def info(loc, locvar):
        ax[1].set_title('3D Graph', loc='left', va='top', fontsize=13)
        loclabel = (f'Predicted source location at:\n' +
                    f'X: %.5f $\\pm$ %.5f cm\n' % (100*loc[0], 100*locvar[0]) +
                    f'Y: %.5f $\\pm$ %.5f cm\n' % (100*loc[1], 100*locvar[1]) +
                    f'Z: %.5f $\\pm$ %.5f cm' % (100*loc[2], 100*locvar[2]))  # Location of hottest voxel
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

    loc, com, locvar, var, gaussed = gaussing()
    xyz(data)
    planars(gaussed, com, var)

    ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*100))
    for i in range(1, 5):
        ax[i].xaxis.set_major_formatter(ticks)
        ax[i].yaxis.set_major_formatter(ticks)
    ax[1].zaxis.set_major_formatter(ticks)

    if resolution is not None:
        resolves(com, loc, locvar, data)
        ax[5].xaxis.set_major_formatter(ticks)
        ax[6].xaxis.set_major_formatter(ticks)
        ax[7].xaxis.set_major_formatter(ticks)
    info(loc, locvar)

    return fig, ax
