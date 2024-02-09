import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.optimize import curve_fit
data = []
with open(r"C:\Users\euan6\Downloads\Energydeps.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        for i in row:
            data.append(float(i))

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


counts = np.array(countlist[575:-60])
energy = np.array(numberlist[575:-60])*1000

peakE = np.sum(counts*energy)/np.sum(counts)
print(peakE)
stdevE = np.sqrt((np.sum(counts*energy**2)/np.sum(counts)) - peakE**2)
print(stdevE)

def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


popt, pcov = curve_fit(gauss_function, energy, counts, p0 = [1,660,75])
plt.plot(energy, gauss_function(energy, *popt), label='fit')

peakE = popt[1]
stdevE = np.abs(popt[2])

x = np.linspace(int(peakE-6*stdevE),int(peakE+6*stdevE),int(12*stdevE))
y = gauss_function(x,popt[0], peakE, stdevE)

peak = np.max(y)

half_count = np.argmax(y)

cut_count = y[half_count:]
index1 = np.argmin(np.abs(peak / 2 - cut_count)) + half_count

cut_count = y[:-half_count]
index2 = np.argmin(np.abs(peak / 2 - cut_count))

FWHM = np.abs(x[index1] - x[index2])

print(FWHM)

print(peakE)
print(stdevE)

x = np.linspace(,int(peakE+6*stdevE),int(12*stdevE))


plt.plot(energy, counts, color='k')
