import matplotlib.pyplot as plt
import csv
from scipy.signal import find_peaks, peak_widths
import numpy as np

CSV1 = r"C:\Users\euan6\OneDrive\One Drive Auto-Files\Documents\Euan\University\Modules\Group Studies\Spectra_New\CH2 Feb22 Setup 7 A.csv"

data = []
with open(CSV1, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        s_count = 0
        num = ""
        for char in row[0]:
            if s_count == 1:
                num += char
            if char == ";":
                s_count += 1
        data.append(float(num[:-1]))


data = sorted(data)
numberlist = sorted(list(set(data)))
# use to get rid of 622 peak
# numberlist = numberlist[:-1]
energy_dep = {}
for i in data:
    if i not in energy_dep:
        energy_dep[i] = 1
    else:
        energy_dep[i] += 1
countlist = list(energy_dep.values())
# use to get rid of 0s and 622 peak
# countlist = countlist[:-1]
print(countlist)
print(numberlist)


# D1 3" total = 821655, prom = 10,000
# D0 1" toal = ......., prom = 3,500

plt.figure('Histogram of Energy Depositions')
plt.xlabel('Energy deposition (Mev)')
plt.ylabel('Count')
plt.title('3" Spectrum (Detector 1)')
plt.rcParams['figure.dpi'] = 2000

hist, bin_edges = np.histogram(data, bins=750)
bin_centres = (bin_edges[:-1] +bin_edges[1:])/2
peaks, _ = find_peaks(hist, prominence = 20000)
# Prominence should be increased if detecting more than 2 peaks.

width = peak_widths(hist, peaks, rel_height = 0.5)
bin_width = (bin_edges[1]-bin_edges[0])
print("Bin width = " + str(bin_width))
peak_widths = width[0] * bin_width
print("Peak widths = " + str(peak_widths))
print(width[1])
print(bin_centres[peaks])

plt.show(block=False)
plt.bar(bin_centres, hist, width=bin_edges[1] - bin_edges[0])
plt.plot(bin_centres[peaks], hist[peaks], 'ro')
