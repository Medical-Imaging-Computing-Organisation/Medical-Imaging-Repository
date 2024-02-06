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
    
    # Use is_unique function to find all unique Scatterer and Absorber index pairs
    unique_index_pairs = np.where(is_unique(EArray[:,4], EArray[:,5])==True)[0]
    # print(unique_index_pairs)
    # Define output array according to number of unique Scatterer-Absorber Pairs present in data
    vec_mat_arr = np.zeros((unique_index_pairs.size, 32), dtype=np.float32) # change to empty once errors are being calculated
    
    # Define angle array for each pair and unit vectors
    angle_arr = np.zeros((unique_index_pairs.size, 3))
    

    
    # Iterable - calculating vector and matrix elements
    # @njit(parallel=True)
    def Populate_Output_Array(EArray, DetectorArray, vec_mat_arr, angle_arr, unique_index_pairs):
        for i in range(0, unique_index_pairs.size):
        
            # Generate OA Vector
            vec_mat_arr[i,:3] = DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],4]),1:4]
            vec_mat_arr[i, 3:6] = 0
            # Generate BA Vector (Values only)
            vec_mat_arr[i,6:9] = DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],5]),1:4]
                    
            # Calculate uncertainties on BA Vector
            vec_mat_arr[i,9:12] = np.power(np.power(DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],4]),1:4],2) + 
                                      np.power(DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],5]),1:4],2), 0.5)
        
            # Calculating angles for each pair
            angle_arr[i,0] = np.arccos(vec_mat_arr[i,8]/np.linalg.norm(vec_mat_arr[i,6:9])) # angle alpha
            angle_arr[i,1] = np.arccos(vec_mat_arr[i,7]/np.linalg.norm(vec_mat_arr[i,6:9])) # angle beta
            angle_arr[i,2] = np.arccos(vec_mat_arr[i,6]/np.linalg.norm(vec_mat_arr[i,6:9])) # angle gamma
        
            # Generating rotation matrix elements for each pair
            vec_mat_arr[i,12] = np.cos(angle_arr[i,1]) * np.cos(angle_arr[i,2])
            vec_mat_arr[i,13] = np.sin(angle_arr[i,0]) * np.sin(angle_arr[i,1]) * np.cos(angle_arr[i,2]) - np.cos(angle_arr[i,0]) * np.sin(angle_arr[i,2])
            vec_mat_arr[i,14] = np.cos(angle_arr[i,0]) * np.sin(angle_arr[i,1]) * np.cos(angle_arr[i,2]) + np.sin(angle_arr[i,0]) * np.sin(angle_arr[i,2])
            vec_mat_arr[i,15] = np.cos(angle_arr[i,1]) * np.sin(angle_arr[i,2])
            vec_mat_arr[i,15] = np.sin(angle_arr[i,0]) * np.sin(angle_arr[i,1]) * np.sin(angle_arr[i,2]) + np.cos(angle_arr[i,0]) * np.cos(angle_arr[i,2])
            vec_mat_arr[i,16] = np.cos(angle_arr[i,0]) * np.sin(angle_arr[i,1]) * np.sin(angle_arr[i,2]) - np.sin(angle_arr[i,0]) * np.cos(angle_arr[i,2])
            vec_mat_arr[i,17] = np.sin(angle_arr[i,1]) * (-1)
            vec_mat_arr[i,18] = np.sin(angle_arr[i,0]) * np.cos(angle_arr[i,1])
            vec_mat_arr[i,19] = np.cos(angle_arr[i,0]) * np.cos(angle_arr[i,1])
        
            # Generating rotation matrix error elements
        
            # This requires a significant time investment towards tedious array multiplications, it will be done during 
            #         week 3 in time for the whole code throughput calculating errors
        
            vec_mat_arr[i,20:30] = 0 # for now the errors are set to 0
        
        
            # Copying across the scatterer and absorber indices for function 3
            vec_mat_arr[i,30:32] = EArray[unique_index_pairs[i], 4:6]
        
    
    
        # return the vector & matrix array
        return vec_mat_arr

    output_arr = Populate_Output_Array(EArray, DetectorArray, vec_mat_arr, angle_arr, unique_index_pairs)
    return output_arr
