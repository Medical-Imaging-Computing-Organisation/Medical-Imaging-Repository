# Medical Imaging Computing Upcoming Goals:


## Image Reconstruction:

#### Create the Direct Back Projection Algorithm:

- Write code for extracting energies, times and channel number from a CSV-style data set provided by Labs (I was told it would be semi-colon delimited today). We will need to be provided with which channel was plugged into which detector and where those detectors were during the measurement window. May need to change coordinate system.
- Write code for identifying which events are coincident and correspond to a compton scatter followed by photoelectric absorption. Discard other events.
- Write code (maths) for generating angles and hence cones using the selected events.
- Write code for generating a heatmap of cone overlaps and plot it, resulting in the image.

## Image Reconstruction Roles:

- Extract data into usable format from labs: Chris

- Identify Coincidences: Alfie

- Generate Cones (DBP): Richard

- Create Heatmap: Adam

### Agreed Formats

From Chris to Alfie: two numpy arrays. 
- Array one describes every event recorded in every detector, giving the energy deposited (E) and the time at which it occurred (t) as well as uncertainities on these and the index of the detector in whih the event occurred. We expect many events (order of thousands).
[[detector index, E, t, delta E, delta t], [detector index, E, t, delta E, delta t], ...]
- Array two gives the position of each detector as (x, y, z) coordinates in the lab reference system along with uncertainties on these measurements, as well as whether the detector is intended to be a scatter or absorber. We expect only a few detectors (e.g. 4).
[[detector index, x, y, z, delta x, delta y, delta z, Scat/Ab], [detector index, x, y, z, delta x, delta y, delta z, Scat/Ab], ...]

From Alfie to Richard: two numpy arrays plus a value of E0 (and maybe info about detector geometry / uncertainty - need to work out how we're doing this)
- Array one describes every event identified as a true coincidence, giving the energy deposited in the Compton scatter (E1) and the energy deposited in the PE absorption (E2) along with the index of the detector in which the scatter and absorbtion were detected. We expect many events (~1000).
[[E1, E2, scatterer index, absorber index], [E1, E2, scatterer index, absorber index], ...]
- Array two gives the position of each detector using the same format as above:
[[detector index, x, y, z, delta x, delta y, delta z], [detector index, x, y, z, delta x, delta y, delta z], ...]


## Monte Carlo:

#### Start learning Geant4:
- Attend Tony's lesson on Tuesday 16/1/24
- Familiarise with C++ and Geant4 (More details can be added once the task is started and better understood)

#### Physics, Equations, Identifying Parameters and Assumptions:
- Learn the relevant physics and equations required for possible events within the detectors, in preparation for predictive modelling.



# Medical Imaging Computing Completed Goals:

## Image Reconstruction:

## Monte Carlo:
