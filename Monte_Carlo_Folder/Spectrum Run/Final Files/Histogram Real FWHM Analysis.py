import matplotlib.pyplot as plt
import csv
import numpy as np
with open(r"C:\Users\euan6\Downloads\Real Spectrums\3 inch real.txt", 'r') as file:
    countlist = [float(line.strip()) for line in file]
numberlist = []
for i in range(len(countlist)):
    numberlist.append(i)
    
numberlist = numberlist[:-1250]
countlist = countlist[:-1250]

counts = np.array(countlist[654:-20])
energy = np.array(numberlist[654:-20])

peak = np.max(counts)

half_count = np.argmax(counts)

cut_count = counts[half_count:]
index1 = np.argmin(np.abs(peak / 2 - cut_count)) + half_count

cut_count = counts[:-half_count]
index2 = np.argmin(np.abs(peak / 2 - cut_count))

print(peak)
print(energy[np.argmax(counts)])
print("")
print(index1)
print(index2)
print("")
print(counts[index1])
print(energy[index1])
print("")
print(counts[index2])
print(energy[index2])
print("")

FWHM = np.abs(energy[index1] - energy[index2])

print(FWHM)



plt.figure('Histogram of Energy Depositions')
plt.xlabel('Energy deposition (KeV)')
plt.ylabel('Count')
plt.title('Number Of Times Energy Is Deposited')
plt.plot(energy, counts, color='k')
