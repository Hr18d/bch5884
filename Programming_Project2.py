#!/usr/bin/env python3
#https://github.com/Hr18d/bch5884.git
#Hosna Rastegarpouyani


import sys
import numpy as np
from matplotlib import pyplot

if len(sys.argv) != 2:
	print ("Usage: Programming_Project2.py <chromatogramfilename>")
	print ("_____________________________________________________")
	sys.exit()
	
chromatogramfilename = sys.argv[1]

#-----------------------------------------------------------> read the chromatogram file

chromatogramfile = open(chromatogramfilename,'r')
lines = chromatogramfile.readlines()
chromatogramfile.close()

#---------------------> make two lists: one for time points and another absorption value

time = []
absorption = []
i=1
for line in lines[3:]:
	words = line.split()
	try:
		time.append(float(words[0]))
		absorption.append(float(words[1]))
	
	except:
		print("could not parse line:", i)
		continue
	i+=1

#-> measure the mean of the data (absorption) to distinguish between real peaks and noises

sum = 0
for y in absorption:
	sum += y
mean = sum/len(absorption)

#------------------------------------------------> find the peaks using scipy find_peaks
# pk stands for peak

from scipy.signal import find_peaks

peaks, _ = find_peaks(absorption, height= mean)

pk_value = []
x_value = []
for i in peaks:
	pk_value.append(absorption[i])
	x_value.append(time[i])
	

print("The threshold is %.3f" %(mean))	
print('Maximum absorbance values(peaks): ',pk_value)
print("Peak indexes are: ", peaks)
print('Times at which maximum absorbance occurred: ',x_value)

#----------------> find the boundaries by sliding both ways off of a peak and reaching the
# boundaries by considering the fact that the point after (or before) the current point 
# has either a greater value or an equal value
# rp stands for the right-point
# lp stands for the leftpoint

rightboundary = []
leftboundary = []
rp = [.0,.0]
lp = [.0,.0]

for p in peaks:
	index = 0
	while True:
		index += 1
		if absorption[p+index+1] >= absorption[p+index]:
			rightboundary.append([time[p+index], absorption[p+index]])
			rp = [.0,.0]
			break
			
	while True:
		index += 1  
		if absorption[p-index-1] >= absorption[p-index]:
			leftboundary.append([time[p-index], absorption[p-index]])
			lp = [.0,.0]
			break

rp = np.array(rightboundary)
lp = np.array(leftboundary)

#-------------------------> plot the result on a graph with marked peaks and boundaries 

pyplot.plot(time,absorption,rp[:,0],rp[:,1],'g^',lp[:,0],lp[:,1],'r^',x_value, pk_value,'b^')

for a,b in zip(x_value, pk_value): 
	pyplot.text(a, b, str(b))
pyplot.show()
