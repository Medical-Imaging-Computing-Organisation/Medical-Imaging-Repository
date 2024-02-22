 import numpy as np
from numba import njit, prange

def Generate_Position_Vectors_And_Matrices(EArray, DetectorArray):
    '''
    
    @author = Chris
    Spherical Polar Rotation Matrices by Richard in this version.
    
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
    beta_arr = np.zeros((unique_index_pairs.size,2))
    

    
    # Iterable - calculating vector and matrix elements
    # @njit(parallel=True)
    def Populate_Output_Array(EArray, DetectorArray, vec_mat_arr, angle_arr, unique_index_pairs):
        for i in range(0, unique_index_pairs.size):
        
            # Generate OA Vector
            vec_mat_arr[i,:3] = 0.01 * DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],4]),1:4]
            vec_mat_arr[i, 3:6] = 0
            # Generate BA Vector (Values only)
            vec_mat_arr[i,6:9] = -0.01 *  DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],5]),1:4] + vec_mat_arr[i,:3]
                    
            # Calculate uncertainties on BA Vector
            vec_mat_arr[i,9:12] = np.power(np.power(DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],4]),1:4],2) + 
                                      np.power(DetectorArray[np.where(DetectorArray[:,0]==EArray[unique_index_pairs[i],5]),1:4],2), 0.5)
        
            # Calculating angles for each pair
            angle_arr[i,0] = np.arccos(vec_mat_arr[i,8]/np.linalg.norm(vec_mat_arr[i,6:9])) # angle alpha
            angle_arr[i,1] = np.arccos(vec_mat_arr[i,7]/np.linalg.norm(vec_mat_arr[i,6:9])) # angle beta
            angle_arr[i,2] = np.arccos(vec_mat_arr[i,6]/np.linalg.norm(vec_mat_arr[i,6:9])) # angle gamma
            #calculating beta moduli for each pair
            beta_arr[i,0] = np.linalg.norm(vec_mat_arr[i,6:9]) #beta
            beta_arr[i,1] = np.linalg.norm(vec_mat_arr[i,6:8]) #beta_T
            #dx = vec_mat_arr[i,6]
            #dy = vec_mat_arr[i,7]
            #dz = vec_mat_arr[i,8]
            #T and P are the Theta and Phi spherical polar coordinates for the beta vector. 
            # Generating rotation matrix elements for each pair
            vec_mat_arr[i,20] = vec_mat_arr[i,8]/beta_arr[i,0] #mark #R33 cos(T)
            vec_mat_arr[i,13] = -vec_mat_arr[i,7]/beta_arr[i,1] #mark  R12 -sin(P)
            vec_mat_arr[i,16] = vec_mat_arr[i,6]/beta_arr[i,1] #mark R22 cos(P)
            vec_mat_arr[i,12] = vec_mat_arr[i,20]*vec_mat_arr[i,16] #pole  R11 cos(P)*cos(T)
            vec_mat_arr[i,14] = vec_mat_arr[i,6]/beta_arr[i,0] #R13 cos(P)sin(T)
            vec_mat_arr[i,15] = -vec_mat_arr[i,20]*vec_mat_arr[i,13] #pol R21 sin(P)cos(T)
            vec_mat_arr[i,17] = vec_mat_arr[i,7]/beta_arr[i,0] #R23 sin(P)sin(T)
            vec_mat_arr[i,18] = -beta_arr[i,1]/beta_arr[i,0] #R31 -sin(T)
            vec_mat_arr[i,19] = 0 #R32 matrix component is 0, no rotation about x axis.
        
            # Generating rotation matrix error elements
            vec_mat_arr[i,21]
            vec_mat_arr[i,22]
            vec_mat_arr[i,23]
            vec_mat_arr[i,24]
            vec_mat_arr[i,25] =  
            vec_mat_arr[i,25] =by*np.sqrt(vec_mat_arr[i,25])/(b_t**3)
            vec_mat_arr[i,26]
            vec_mat_arr[i,27]
            vec_mat_arr[i,28] = 0
            
            vec_mat_arr[i,29] = (bz**2)[(bx*dbx)**2 + (by*dby)**2]+(b_t**4)*dbz**2
            vec_mat_arr[i,29] = np.sqrt(vec_mat_arr[i,29])/(b**3)
            dr33 = np.divide(dr33,beta_arr[i,0]**3)
            # This requires a significant time investment towards tedious array multiplications, it will be done during 
            #         week 3 in time for the whole code throughput calculating errors
            #the "error matrix" may be easier to work out for the spherical polar rotation matrix than 
            #for the Rodrigues cross product rotation matrix, could be wrong but if use my function, 
            #i can get on with working out the error for each term over the weekend (working on slides rn)
        
            vec_mat_arr[i,21:30] = 0 # for now the errors are set to 0
        
        
            # Copying across the scatterer and absorber indices for function 3
            vec_mat_arr[i,30:32] = EArray[unique_index_pairs[i], 4:6]
        
    
    
        # return the vector & matrix array
        return vec_mat_arr

    output_arr = Populate_Output_Array(EArray, DetectorArray, vec_mat_arr, angle_arr, unique_index_pairs)
    return output_arr
