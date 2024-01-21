# Medical Imaging Computing Upcoming Goals:


## Image Reconstruction:

#### Create the Direct Back Projection Algorithm:


- Write code (maths) for generating angles and hence cones using the selected events. (Bottleneck)
- Write code for generating a heatmap of cone overlaps and plot it, resulting in the image. (Bottleneck)

## Image Reconstruction Roles:

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


## Monte Carlo:

#### Start learning Geant4:
- Attend Tony's lesson on Tuesday 16/1/24
- Familiarise with C++ and Geant4 (More details can be added once the task is started and better understood)

#### Physics, Equations, Identifying Parameters and Assumptions:
- Learn the relevant physics and equations required for possible events within the detectors, in preparation for predictive modelling.



# Medical Imaging Computing Completed Goals:

## Image Reconstruction:

- Write code for extracting from pre-agreed CSV-style data set provided by Labs. (Chris)
- Write code for identifying which events are coincident and correspond to a compton scatter followed by photoelectric absorption. Discard other events. (Alfie)

## Monte Carlo:


