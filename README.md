# Medical Imaging Computing Upcoming Goals:


## Image Reconstruction:

#### Create the Direct Back Projection Algorithm:


- Write code (maths) for generating angles and hence cones using the selected events. (Bottleneck)
- Write code for generating a heatmap of cone overlaps and plot it, resulting in the image. (Bottleneck)

### Image Reconstruction Current Roles:

- Work on cone generation side of bottleneck: Chris, Richard

- Work on meshgrid and heatmap side of bottleneck: Alfie, Adam

### Agreed Formats

Output from CSV Extraction: 
- Array one describes every event recorded in every detector, giving the energy deposited (E) and the time at which it occurred (t) as well as uncertainities on these and the index of the detector in whih the event occurred. We expect many events (order hundreds of thousands).
[[detector index, E, t, delta E, delta t], [detector index, E, t, delta E, delta t], ...]
- Array two gives the position of each detector as (x, y, z) coordinates in the lab reference system along with uncertainties on these measurements, as well as whether the detector is intended to be a scatter or absorber. We expect only a few detectors (e.g. 4).
[[detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], [detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], ...]
- Array three gives valid pairing of detectors (e.g. 0 1 and 0 2) as well as a ballpark estimate of the solid angle uncertainty between the pairs. We expect approximately n! (factorial of n) detector pairs where n is the number of detectors.
[[Scatterer Index, Absorber Index, Ballpark solid angle uncertainty between pair], [Scatterer Index, Absorber Index, Ballpark solid angle uncertainty between pair] ...]

Output from Coincidence Detection to Cone Generation:
- Array one describes every event identified as a true coincidence, giving the energy deposited in the Compton scatter (E1) and the energy deposited in the PE absorption (E2) along with the index of the detector in which the scatter and absorbtion were detected. We expect many events (~1000).
[[E1, E2, scatterer index, absorber index], [E1, E2, scatterer index, absorber index], ...]
- Array two is passed through from CSV Extraction and gives the position of each detector using the same format as above:
[[detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], [detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], ...]

DBP Cone Generation Internals (relevant to Chris and Richard):
- Function 1 (Richard) Calculate Angles: From the Coincidence Detection output array [[E1, E2, scatterer index, absorber index], [E1, E2, scatterer index, absorber index], ...], use Compton Kinematics to calculate angles theta. Output: [[theta, Scatterer Index, Absorber Index], [theta, Scatterer Index, Absorber Index] ...]
- Function 2 (Chris) Calculate Position Vectors and Rotation Matrices: From Coincidence Detection output array [[E1, E2, scatterer index, absorber index], [E1, E2, scatterer index, absorber index], ...] and Detector Position Array [[detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], [detector index, x, y, z, delta x, delta y, delta z, Sc/Ab], ...], find the set of position vectors and corresponding rotation matrices. Output: [[Vector from Origin to Scatterer, Vector from Absorber to Scatterer, Rotation Matrix, Scatterer Index, Absorber Index], [Vector from Origin to Scatterer, Vector from Absorber to Scatterer, Rotation Matrix, Scatterer Index, Absorber Index], ...]
- Function 3 (Richard) Merge Arrays: From the outputs of Function 1 and 2, merge relevant information into a single array. Output; [[Vector from Origin to Scatterer, Vector from Absorber to Scatterer, theta, Rotation Matrix], [Vector from Origin to Scatterer, Vector from Absorber to Scatterer, theta, Rotation Matrix] ...]
- Function 4 (Chris) Generate set of points corresponding to cones: From the output of Function 3, generate a set of points that correspond to those populated by the surfaces of cones. Output: [[x, y, z], [x, y, z] ...]
- Error propagation will be investigated after the bottleneck is satisfied

Output from Cone Generation:
- Array containing sets of xyz points corresponding to points that are populated by cones:
[[x, y, z], [x, y, z] ...]
- While errors are not yet considered, the output array will subsequently be of the format [[x, y, z, delta x, delta y, delta z], [x, y, z, delta x, delta y, delta z] ...] once they are.

Output from Meshgrid and Heatmap:
- 3D image displaying voxels, colour coded according to number of cones that have passed through them
- 2D slice images for planar compression of the 3D images


## Monte Carlo:

- Produce a simple spectrum to give to Experimental Lab team.
- Generate simple data for IR team testing purposes


### Monte Carlo Current Roles:

- Coding primary generator and step action: James
- Coding event action, sum and round (outputting into an array): Euan
- Data postprocessing in Python: Lorea
(May need to schedule a meeting between Lorea and Chris once Chris has CPU parallelization working to see if Lorea's postprocessing code can be sped up)




# Medical Imaging Computing Completed Goals:

## Image Reconstruction:

- Write code for extracting from pre-agreed CSV-style data set provided by Labs. (Chris)
- Write code for identifying which events are coincident and correspond to a compton scatter followed by photoelectric absorption. Discard other events. (Alfie)

## Monte Carlo:

- Attend Tony's lessons on Geant4
- Learn the relevant physics and equations required for possible events within the detectors, in preparation for predictive modelling. (Essentially already programmed in to Geant4)

