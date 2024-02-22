import numpy as np
from numba import njit, prange

def Generate_Position_Vectors_And_Matrices(EArray, DetectorArray):
    '''
    
    @author = Chris
    
    Takes the detector pair coincident energy and detector position information arrays and generates the system vectors and rotation matrices for each pair
    
    
            Parameters:
                    EArray (Numpy Array): Array from coincidence detection containing energy depositions and 
                                            corresponding detector indices
                                                    
                    DetectorArray (Numpy Array): Array from CSV extraction containing positional information 
                                                    for each detector
            
            Required imports:
                    import numpy as np
                    from numba import njit
                    from numba import prange
            
            Returns:
                    vec_mat_arr (Numpy Array): Output array containing the scatterer position vectors, detector pair 
                                                    beta vectors and rotation matrices for each detector pair present 
                                                    in coincidence data
                        
                        vec_mat_arr: [[OAx, OAy, OAz, Delta OAx, Delta OAy, Delta OAz, BAx, BAy, BAz, Delta BAx, Delta BAy, 
                                        Delta BAz, R11, R12, R13, R21, R22, R23, R31, R32, R33, Delta R11, Delta R12, 
                                        Delta R13, Delta R21, Delta R22, Delta R23, Delta R31, Delta R32, Delta R33, 
                                        Scatterer Index, Absorber Index],  ... ]

    
    '''
    # Internal function - finding unique index pairs from EArray's Scatterer and Absorber Indices
    # NOTE: Will not be suitable for Numba and is a 'just works' function for now to get a working prototype
    # NOTE: Will be an absolute pain for Chris' GPU logistics later on - may genuinely have to be reduced to for loops
    def is_unique(*indices):
        arr = np.vstack(indices)
        _, ind = np.unique(arr, axis=1, return_index=True)
        out = np.zeros(shape=arr.shape[1], dtype=bool)
        out[ind] = True
        return out
    
    # # Use is_unique function to find all unique Scatterer and Absorber index pairs
    # unique_index_pairs = np.where(is_unique(EArray[:,4], EArray[:,5])==True)[0]
    # # print(unique_index_pairs)
    # # Define output array according to number of unique Scatterer-Absorber Pairs present in data
    # vec_mat_arr = np.zeros((unique_index_pairs.size, 32), dtype=np.float32) # change to empty once errors are being calculated
    
    # # Define angle array for each pair and unit vectors
    # angle_arr = np.zeros((unique_index_pairs.size, 3))
    
    
    unique_index_pairs = np.where(is_unique(EArray[:,4], EArray[:,5])==True)[0]
    vec_mat_arr = np.zeros((unique_index_pairs.size, 32), dtype=np.float32)
    Normalised_BA = np.zeros((unique_index_pairs.size, 3))
    theta = np.zeros((unique_index_pairs.size, 1))
    e_z = np.array([0, 0, 1])
    a = np.zeros((unique_index_pairs.size, 3))
    a_T = np.zeros((unique_index_pairs.size, 3, 1))
    cross = np.zeros((unique_index_pairs.size, 3))
    mag_cross = np.zeros((unique_index_pairs.size, 1))
    S_a = np.zeros((unique_index_pairs.size, 3, 3))
    R = np.zeros((unique_index_pairs.size, 3, 3))

    
    # Iterable - calculating vector and matrix elements
    # @njit(parallel=True)
    def Populate_Output_Array(EArray, DetectorArray, vec_mat_arr, angle_arr, unique_index_pairs):
        for i in range(0, unique_index_pairs.size):

            # Generate OA Vector
            vec_mat_arr[i,:3] = 0.01 * DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],4]),1:4]
            vec_mat_arr[i, 3:6] = 0
            # Generate BA Vector (Values only)
            vec_mat_arr[i,6:9] = -(0.01 * DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],5]),1:4] - vec_mat_arr[i,:3])

            # Calculate Normalised BA Vector
            Normalised_BA[i] = vec_mat_arr[i,6:9] / np.sqrt(np.dot(vec_mat_arr[i,6:9], vec_mat_arr[i,6:9]))

            # Calculate uncertainties on BA Vector
            vec_mat_arr[i,9:12] = 0


            # Rodrigues' rotation matrix formulation

            # Filter for when unit-z vector and BA are parallel/antiparallel
            if np.dot(e_z, Normalised_BA[i]) == 1:
                vec_mat_arr[i, 12:15] = [1, 0, 0]
                vec_mat_arr[i, 15:18] = [0, 1, 0]
                vec_mat_arr[i, 18:21] = [0, 0, 1]
            elif np.dot(e_z, Normalised_BA[i]) == -1:
                vec_mat_arr[i, 12:15] = [-1, 0, 0]
                vec_mat_arr[i, 15:18] = [0, -1, 0]
                vec_mat_arr[i, 18:21] = [0, 0, -1]
            else:
                # Calculate cross product of unit-z vector and normalised BA vector, accounting for right handed system
                cross[i] = np.cross(e_z, Normalised_BA[i])

                mag_cross[i] = np.sqrt(np.dot(cross[i], cross[i]))

                a[i] = cross[i]/mag_cross[i]

                a_T[i] = a[i][:, np.newaxis]

                # Calculating angle of rotation
                theta[i] = np.arcsin(mag_cross[i])

                # accounting for orientation relative to e_z
                if Normalised_BA[i, 2] < 0:
                    theta[i] = -theta[i] + np.pi
                #elif Normalised_BA[i, 2] > 0:
                    #theta[i] = theta[i]






                # Calculating S_a tensor
                S_a[i,0,0] = 0
                S_a[i,0,1] = -a[i,2]
                S_a[i,0,2] = a[i,1]
                S_a[i,1,0] = a[i,2]
                S_a[i,1,1] = 0
                S_a[i,1,2] = -a[i,0]
                S_a[i,2,0] = -a[i,1]
                S_a[i,2,1] = a[i,0]
                S_a[i,2,2] = 0


                # Calculating Rotation Matrix
                # R[i] = np.tensordot(a[i], a_T[i], axes=0) + (np.identity(3) - np.tensordot(a[i], a_T[i], axes=0)) * np.cos(theta[i]) + S_a * np.cos(theta[i])

                R[i] = np.identity(3) + np.sin(theta[i]) * S_a[i] + (1-np.cos(theta[i]))* np.matmul(S_a[i], S_a[i])



                # Generating rotation matrix elements for each pair
                vec_mat_arr[i,12] = R[i,0,0]
                vec_mat_arr[i,13] = R[i,0,1]
                vec_mat_arr[i,14] = R[i,0,2]
                vec_mat_arr[i,15] = R[i,1,0]
                vec_mat_arr[i,16] = R[i,1,1]
                vec_mat_arr[i,17] = R[i,1,2]
                vec_mat_arr[i,18] = R[i,2,0]
                vec_mat_arr[i,19] = R[i,2,1]
                vec_mat_arr[i,20] = R[i,2,2]



            # Generating rotation matrix error elements

            # This requires a significant time investment towards tedious array multiplications, it will be done during 
            #         week 3 in time for the whole code throughput calculating errors

            vec_mat_arr[i,21:30] = 0 # for now the errors are set to 0


            # Copying across the scatterer and absorber indices for function 3
            vec_mat_arr[i,30:32] = EArray[unique_index_pairs[i], 4:6]
        
    
    
        # return the vector & matrix array
        return vec_mat_arr

    output_arr = Populate_Output_Array(EArray, DetectorArray, vec_mat_arr, theta, unique_index_pairs)
    return output_arr
