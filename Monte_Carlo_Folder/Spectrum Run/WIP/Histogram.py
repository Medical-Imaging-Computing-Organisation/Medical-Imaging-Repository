import matplotlib.pyplot as plt
import csv
data = []
with open('Energydeps.csv', 'r') as file:
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
# use to get rid of 0s and 622 peak
# countlist = countlist[:-1]
print(countlist)
print(numberlist)

plt.figure('Histogram of Energy Depositions')
plt.xlabel('Energy deposition (Mev)')
plt.ylabel('Count')
plt.title('Number Of Times Energy Is Deposited')
plt.plot(numberlist, countlist, color ='k')




        

