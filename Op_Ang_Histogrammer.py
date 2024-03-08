# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:02:28 2024

@author: richa
"""
def Op_Ang_Histogrammer(f1Out,f2Out, pair):
    '''
    

    Parameters
    ----------
    f1Out : ndarray
        Function 1 output of opening angles.
    f2Out : ndarray
        Function 2 output of beta vectors
    pair : array
        np.array([Sc, Ab]), 1D array of the detector pair to be extracted.

    Returns
    -------
    fig : obj
    ax : obj
        use plt.show() to display figure object.

    '''
    delete_indices = []
    for j in range(f1Out.shape[0]):
        print(j)
        if np.array_equal(f1Out[j,2:4], pair):
            print('good')
        else:
            delete_indices.append(j)
    f1Out = np.delete(f1Out, delete_indices, axis = 0) #f1 but only with one detector pair specified by pair. 
    delete_indexes = []
    for i in range(f2Out.shape[0]):
        print(j)
        if np.array_equal(f2Out[i,30:32], pair):
            print('good')
        else:
            delete_indexes.append(i)
    f2Out = np.delete(f2Out, delete_indexes, axis = 0)
    
    #scatterer = f2[0,0:3]
    #beta_vector = f2[0,6:9]
    
    beta = np.sqrt(np.dot(f2[0,6:9], f2[0,6:9]))
    scatterer_d = np.sqrt(np.dot(f2[0,0:3], f2[0,0:3]))
    cos = np.dot(f2[0,0:3], -f2[0,6:9])/(beta*scatterer_d)
    ex_angle = np.arccos(cos)*180/np.pi
    angle = 180*f1Out[:,0]/np.pi
    
    fig, ax = plt.subplots()
    ax.hist(angle, bins = 36, label = 'Opening Angles')
    ax.axvline(ex_angle, color ='r', label = 'Angle between rs and beta')
    #ax.axvline(np.mean(angle), color = 'r')
    ax.set_title(f'Histogram of Opening Angles for [{int(pair[0])},{int(pair[1])}]')
    ax.set_xlabel('Opening angle (degrees)')
    ax.set_ylabel('counts')
    ax.legend(loc = 'upper right')

    return fig, ax