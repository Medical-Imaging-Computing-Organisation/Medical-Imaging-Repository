import matplotlib.pyplot as plt
import csv
data = []
with open(r"C:\Users\euan6\OneDrive\One Drive Auto-Files\Documents\Euan\University\Modules\Group Studies\IR Check\CSV1_Smeared_G_D1.csv", 'r') as file:
    csvreader = csv.reader(file)
    i = 1
    #print("ababbabbaba")
    for row in csvreader:
        if i % 2 == 1:
            data.append(float(row[1]))
            #print("a")
            #print(float(row[1]))
        else:
            data[int(i / 2)-1] += float(row[1])
            #print("b")
            #print(float(row[1]))
            #print(data[int(i/2)-1])
        i += 1

"""
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
"""

# D1 3" total = 821655

plt.figure('Histogram of Energy Depositions')
plt.xlabel('Energy deposition (Mev)')
plt.ylabel('Count')
plt.title('3" Spectrum (Detector 1)')
plt.rcParams['figure.dpi'] = 2000
plt.show(block=False)
plt.hist(data, bins=50, color='k')
