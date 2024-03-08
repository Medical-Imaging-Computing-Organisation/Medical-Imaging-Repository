import csv
import copy

#detector parameters, to be modified depending on the initial geometry being used
#detectorn = [index, radius, x, dx, y, dy, z, dz]
detector0 = [0, 2.54, 7.071, 1.77, 7.071, 1.77,	0, 1.77]
detector1 = [1, 2.54, 7.071, 1.77, -7.071, 1.77, 0,	1.77]
detector2 = [2, 2.54, 7.071, 1.77, 0, 1.77,	7.071, 1.77]
detector3 = [3, 2.54, 7.071, 1.77, 0, 1.77, -7.071, 1.77]
detector4 = [4, 7.63, 30.306, 4.315, 0, 4.315, 17.207, 4.315]
detector5 = [5, 7.63, 30.306, 4.315, 0, 4.315, -17.207, 4.315]
detector6 = [6, 7.63, 30.306, 4.315, 17.207, 4.315, 0, 4.315]
detector7 = [7, 7.63, 30.306, 4.315, -17.207, 4.315, 0, 4.315]
detector_array = [detector0, detector1, detector2, detector3, detector4, detector5, detector6, detector7]
#geometry_array contains a copy of the initial setup
geometry_array = []
geometry_array.append(copy.deepcopy(detector_array))

#new_geometry_array will contain all the new setups
new_geometry_array = []

#process of changing geometry

#making a copy of geometry_array each time so that the original is not changed
new_copy1 = copy.deepcopy(geometry_array)
#change the range until maximum x, y, and z values reached
for i in range (178):
    for j in new_copy1:
        for k in j:
            #incrementing x by 0.25 until max reached
            if k[2] < 0:
                k[2] -= 0.25
            if k[2] >= 0:
                k[2] += 0.25
            if k[4] < 0:
                k[4] -= 1.02
            if k[4] >= 0:
                k[4] += 1.02
            if k[6] < 0:
                k[6] -= 0.13
            if k[6] >= 0:
                k[6] += 0.13
    #append each new setup to new_geometry_array   
    new_geometry_array.append(copy.deepcopy(new_copy1))

new_copy2 = copy.deepcopy(geometry_array)
for i in range (731):
    for j in new_copy2:
        for k in j:
            #incrementing y by 0.25 until max reached
            if k[2] < 0:
                k[2] -= 0.061
            if k[2] >= 0:
                k[2] += 0.061
            if k[4] < 0:
                k[4] -= 0.25
            if k[4] >= 0:
                k[4] += 0.25
            if k[6] < 0:
                k[6] -= 0.031
            if k[6] >= 0:
                k[6] += 0.031
    #append each new setup to new_geometry_array   
    new_geometry_array.append(copy.deepcopy(new_copy2))
    
new_copy3 = copy.deepcopy(geometry_array)
for i in range (91):
    for j in new_copy3:
        for k in j:
            #incrementing z by 0.25 until max reached
            if k[2] < 0:
                k[2] -= 0.49
            if k[2] >= 0:
                k[2] += 0.49
            if k[4] < 0:
                k[4] -= 2.01
            if k[4] >= 0:
                k[4] += 2.01
            if k[6] < 0:
                k[6] -= 0.25
            if k[6] >= 0:
                k[6] += 0.25
    #append each new setup to new_geometry_array   
    new_geometry_array.append(copy.deepcopy(new_copy3))
    
#writing to a CSV
for i in new_geometry_array:
    filename = 'CSV_2_Geometry' + str(new_geometry_array.index(i)) +'.csv'
    with open(filename, 'w', newline='') as csvfile:
        for j in i:
            for k in j:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(k)