import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import scipy.ndimage as ndimage
import scipy.optimize as opt
import matplotlib.ticker as ticker


def draw(h, v, d, dnsy, data1, data2, data, vr, dpa=None, resolution=None):
    def mosaic():
        fig, ax = plt.subplot_mosaic([[1, 3, 3, 4, 7], [1, 3, 3, 4, 7], [1, 3, 3, 5, 8],
                                      [2, 3, 3, 5, 8], [2, 3, 3, 6, 9], [2, 3, 3, 6, 9]],
                                     figsize=(10, 5),
                    per_subplot_kw={1: {'projection': '3d'},
                                    2: {'projection': '3d'},
                                    3: {'projection': '3d', 'xlabel': 'X axis (cm)', 'ylabel': 'Y axis(cm)', 'zlabel': 'Z axis(cm)'},
                                    4: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'z'},
                                    5: {'aspect': 'equal', 'xlabel': 'y', 'ylabel': 'z'},
                                    6: {'aspect': 'equal', 'xlabel': 'x', 'ylabel': 'y'},
                                    7: {},
                                    8: {},
                                    9: {}})
        plt.tight_layout()
        return fig, ax

    def cmap():
        try:  # Colour map creation in try-catch to prevent recreation error
            color_array = plt.get_cmap('YlOrRd')(range(256))
            color_array[:, -1] = np.linspace(0.0, 1.0, 256)**1.5
            map_object = LSC.from_list(name='YlOrRd_alpha2', colors=color_array)
            plt.colormaps.register(cmap=map_object)
            color_array = plt.get_cmap('PiYG')(range(256))
            color_array[:, -1] = np.abs(np.linspace(-1.0, 1.0, 256))**1.5
            map_object = LSC.from_list(name='PiYG2', colors=color_array)
            plt.colormaps.register(cmap=map_object)
        except ValueError:
            pass
        return

    def xyz():
        '''Draw main 3D XYZ scatter plot'''
        XYZ1 = ax[1].scatter(h, v, d, marker='s', s=50/dnsy, c=data1, cmap="YlOrRd_alpha2")
        plt.colorbar(XYZ1, location='top', pad=0.05)
        XYZ2 = ax[2].scatter(h, v, d, marker='s', s=50/dnsy, c=data2, cmap="YlOrRd_alpha2")
        plt.colorbar(XYZ2, location='bottom',
                     cax=inset_axes(ax[2], width="100%", height="5%",
                                    loc='lower center', borderpad=-3.5))
        XYZ3 = ax[3].scatter(h, v, d, marker='s', s=2000 / dnsy, c=data,
                            norm=colors.TwoSlopeNorm(vcenter=0), cmap="PiYG2")
        plt.colorbar(XYZ3, location='bottom',
                     cax=inset_axes(ax[3], width="100%", height="5%",
                                    loc='lower center', borderpad=-4))  # plots 3D heatmap


    def gaussing(data):
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
        com = com[1], com[0], com[2]  # swaps yxz into xyz maintaining tuple
        loc = np.interp(np.array(com), np.arange(h.shape[0]), h[0, :, 0])  # interpolates indices into locations

        sizes = np.mean(np.abs(np.array(H[highcluster-1])-np.array(com)), axis=0)
        locvar = sizes*2*vr  # variation in real distance
        locvar[locvar == 0] = vr

        com2 = tuple(np.rint(com).astype(int))
        isizes = np.mean(np.abs(np.array(H[highcluster - 1]) - np.array(com2)), axis=0)  # index size from rounded pos
        var = np.ceil(isizes).astype(int)  # rounds plane var up

        return loc, com2, locvar, var, gaussed #*(hotfinder!=0)


    def planars(hot1, hot2, var1, var2):
        '''Planar views'''
        midpoint = np.rint(np.mean([hot1, hot2], axis=0)).astype(int)
        var = np.ceil(np.abs(np.array(hot1)-np.array(hot2))/2).astype(int) + np.maximum(var1, var2)
        print("Plane depths", var)
        XZ = ax[4].pcolormesh(h[0], d[0], np.sum(data[midpoint[0] - var[0]:midpoint[0] + var[0] + 1, :, :], axis=0),
                              cmap="PiYG", norm=colors.TwoSlopeNorm(vcenter=0))
        plt.colorbar(XZ)  # X-Z and Y-Z colour maps
        YZ = ax[5].pcolormesh(h[0], d[0], np.sum(data[:, midpoint[1] - var[1]:midpoint[1] + var[1] + 1, :], axis=1),
                              cmap="PiYG", norm=colors.TwoSlopeNorm(vcenter=0))
        plt.colorbar(YZ)
        XY = ax[6].pcolormesh(h[0], d[0], np.sum(data[:, :, midpoint[2] - var[2]:midpoint[2] + var[2] + 1], axis=2).T,
                              cmap="PiYG", norm=colors.TwoSlopeNorm(vcenter=0))
        plt.colorbar(XY)

    def resolves(hot, loc, locvar, data):
        X = h[0, :, 0]
        FWHM = [0, 0, 0]

        def gaussian(x, amplitude, mean, stddev):
            return amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2))

        def dataplot(X, l, lv, axisdata):
            try:
                popt = opt.curve_fit(gaussian, X, axisdata,
                                     p0=[np.max(axisdata), l, lv])
                FWHM = 2 * np.sqrt(2 * np.log(2)) * popt[0][2]
                return FWHM
            except RuntimeError:
                print("Gauss fit failed")
            return np.nan

        FWHM[0] = dataplot(X, loc[0], locvar[0], data[hot[0], :, hot[2]])
        FWHM[1] = dataplot(X, loc[1], locvar[1], data[:, hot[1], hot[2]])
        FWHM[2] = dataplot(X, loc[2], locvar[2], data[hot[0], hot[1], :])
        return FWHM

    def info():
        ax[3].set_title('Gamma Imaged', va='top', fontsize=13)
        lim = np.max(h) + vr
        ax[3].set_ylim([-lim, lim])
        ax[3].set_xlim([-lim, lim])
        ax[3].set_zlim([-lim, lim])
        '''Detector locations plotted & labeled'''
        if dpa is not None:
            ax[3].scatter(0.01 * dpa[:, 1], 0.01 * dpa[:, 2], 0.01 * dpa[:, 3],
                          marker='o', s=100, alpha=0.6, c=dpa[:, 0],
                          cmap='gist_rainbow')
            for i in range(dpa.shape[0]):
                ax[3].text(x=0.01 * dpa[i, 1], y=0.01 * dpa[i, 2],
                           z=0.01 * dpa[i, 3], s=str(int(dpa[i, 0])),
                           ha='center', va='center', clip_on=True)  # Numbers labeled


    lim = np.max(h) + vr
    fig, ax = mosaic()
    cmap()
    xyz()
    loc1, com1, locvar1, var1, _ = gaussing(data1)
    loc2, com2, locvar2, var2, _ = gaussing(data2)
    ax[3].set_title('Gamma Imaged', va='top', fontsize=13)
    planars(com1, com2, var1, var2)
    ax[3].scatter([loc1[0], loc2[0]], [loc1[1], loc2[1]], [loc1[2], loc2[2]], marker='o', s=100, alpha=0.5)
    ax[3].plot([loc1[0], loc2[0]], [loc1[1], loc2[1]], [loc1[2], loc2[2]])  # source located graph

    FWHM1 = resolves(com1, loc1, locvar1, data1)
    FWHM2 = resolves(com1, loc1, locvar1, data2)

    bar3 = ax[8].bar([0, 3, 6], [100*FWHM1[0], 100*FWHM1[1], 100*FWHM1[2]], color='tab:red', label='Input 1')
    bar4 = ax[8].bar([1, 4, 7], [100*FWHM2[0], 100*FWHM2[1], 100*FWHM2[2]], color='tab:blue', label='Input 2')
    ax[8].bar_label(bar3, fmt='{:,.1f}', fontsize=5)
    ax[8].bar_label(bar4, fmt='{:,.1f}', fontsize=5)
    ax[8].set_xticks([0.5, 3.5, 6.5], ['X', 'Y', 'Z'])
    ax[8].set_ylim(0, 1.3*ax[8].get_ylim()[1])
    ax[8].legend(fontsize=5, markerscale=0.2, handlelength=0.5, ncol=2)
    ax[8].set_title('Resolution (FWHM)/cm', fontsize=9, pad=0.1)

    ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x * 100))
    for i in range(1, 7):
        ax[i].xaxis.set_major_formatter(ticks)
        ax[i].yaxis.set_major_formatter(ticks)
    for i in range(1, 4):
        ax[i].zaxis.set_major_formatter(ticks)

    info()
    return fig, ax
