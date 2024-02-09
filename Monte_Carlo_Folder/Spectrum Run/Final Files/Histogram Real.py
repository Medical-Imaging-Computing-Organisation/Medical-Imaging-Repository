import matplotlib.pyplot as plt
import csv
with open(r"C:\Users\euan6\Downloads\Real Spectrums\2 inch real.txt", 'r') as file:
    countlist = [float(line.strip()) for line in file]
numberlist = []
for i in range(len(countlist)):
    numberlist.append(i)
    
numberlist = numberlist[:-1250]
countlist = countlist[:-1250]

print(countlist)
print(numberlist)



plt.figure('Histogram of Energy Depositions')
plt.xlabel('Energy deposition (Mev)')
plt.ylabel('Count')
plt.title('Number Of Times Energy Is Deposited')
plt.plot(numberlist, countlist, color='k')
