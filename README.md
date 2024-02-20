# Medical Imaging Computing Upcoming Goals:


## Image Reconstruction:

#### Create the Direct Back Projection Algorithm:


- Finalise the cone generation segment of the algorithm
- Finalise identification of coincidences

### Image Reconstruction Current Roles:

- Finalise cone generation: Chris, Richard, Adam

- Finalise coincidence detection: Alfie

### Agreed Formats

Output from CSV Extraction: 
- N arrays where N is the number of detectors used in a given experiment. Each of these arrays describes every event recorded in that detector, giving the energy deposited (E) and the time at which it occurred (t) as well as uncertainities on these and the index of the detector in which the event occurred. Each of the N arrays has the following format:
[[detector index, E, t, delta E, delta t], [detector index, E, t, delta E, delta t], ...]
- Array two gives the position of each detector as (x, y, z) coordinates in the lab reference system along with uncertainties on these measurements, as well as whether the detector is intended to be a scatter or absorber. We expect only a few detectors (e.g. 4).
[[detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], [detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], ...]
- Array three gives valid pairing of detectors (e.g. 0 1 and 0 2) as well as a ballpark estimate of the solid angle uncertainty between the pairs. We expect approximately n! (factorial of n) detector pairs where n is the number of detectors.
[[Scatterer Index, Absorber Index, Ballpark solid angle uncertainty between pair], [Scatterer Index, Absorber Index, Ballpark solid angle uncertainty between pair] ...]

Output from Coincidence Detection:
- Array one describes every event identified as a true coincidence, giving the energy deposited in the Compton scatter (E1) and the energy deposited in the PE absorption (E2) with uncertainties (delta E1, delta E2) along with the index of the detector in which the scatter and absorbtion were detected.
[[E1, E2, delta E1, delta E2, scatterer index, absorber index], [E1, E2, delta E1, delta E2, scatterer index, absorber index], ...]
- Array two is passed through from CSV Extraction and gives the position of each detector using the same format as above:
[[detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], [detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], ...]

DBP Cone Generation Internals:
- Function 1 (Richard) Calculate Angles: From the Coincidence Detection output array [[E1, E2, delta E1, delta E2, scatterer index, absorber index], [E1, E2, delta E1, delta E2, scatterer index, absorber index], ...], use Compton Kinematics to calculate angles theta. Output: [[theta, dtheta, Scatterer Index, Absorber Index], [theta, dtheta, Scatterer Index, Absorber Index] ...]
- Function 2 (Chris) Calculate Position Vectors and Rotation Matrices: From Coincidence Detection output array [[E1, E2, delta E1, delta E2, scatterer index, absorber index], [E1, E2, delta E1, delta E2, scatterer index, absorber index], ...] and Detector Position Array [[detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], [detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], ...], find the set of position vectors and corresponding rotation matrices.
- Function 2 Output: [[x1,y1,z1,dx1,dy1,dz1,bx,by,bz,dbx,dby,dbz,R11,R12,R13,R21,R22,R23,R31,R32,R33,dR11,dR12,dR13,dR21,dR22,dR23,dR31,dR32,dR33, Scatterer Index, Aborber Index],...] where Rrc are elements in the rotation matrix R=np.array([R11,R12,R13],[R21, R22, R23], [R31, R32, R33] and bx,by,bz are the coefficients of the beta vector in the master frame. 
- Function 3 (Adam) Merge Arrays: From the outputs of Function 1 and 2, merge relevant information into a single array. Output: [[theta, Vector from Origin to Scatterer, Vector from Absorber to Scatterer, theta, Rotation Matrix], [Vector from Origin to Scatterer, Vector from Absorber to Scatterer, Rotation Matrix] ...]
- - Function 3 Output: [[theta,x1,y1,z1,bx,by,bz, R11, R12, R13, R21, R22, R23, R31, R32, R33, Scatterer Index, Aborber Index],[x1,y1,z1,bx,by,bz, R11, R12, R13, R21, R22, R23, R31, R32, R33]...] where R=np.array([R11,R12,R13],[R21, R22, R23], [R31, R32, R33] and bx,by,bz are the coefficients of the beta vector in the master frame.
- Function 4 (Richard) Generate set of points corresponding to cones: From the output of Function 3, generate a set of points that correspond to those populated by the surfaces of cones. Output: [[x, y, z, delta x, delta y, delta z], ... ]
- Error propagation will be investigated after the bottleneck is satisfied

Output from Cone Generation:
- Array containing sets of xyz points corresponding to points that are populated by cones:
[[x, y, z, delta x, delta y, delta z], [x, y, z, delta x, delta y, delta z] ...]

Output from Meshgrid and Heatmap:
- 3D image displaying voxels, colour coded according to number of cones that have passed through them
- 2D slice images for planar compression of the 3D images


