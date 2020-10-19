#!/usr/bin/env python3

import sys


pdbname=sys.argv[1]

f = open(pdbname, 'r')
lines = f.readlines()

Atomlist = []

for l in lines:

  words = l.split()
  Atomlist.append(words)  
f.close()

flag= input("Do you want to center by mass or geometry [m/g]:")
if flag =='g':
	i = 0
	sumx = 0
	sumy = 0
	sumz = 0
	for atom in Atomlist:
		x = float(atom[6])
		y = float(atom[7])
		z = float(atom[8])
		sumx = sumx + x
		sumy = sumy + y
		sumz = sumz + z
		i = i+1
	
	x_cm = sumx/i
	y_cm = sumy/i
	z_cm = sumz/i
	  

else: 
#sigma mixi / sigma mi
	sm = 0
	smx = 0
	for atom in Atomlist:
		if atom[-1] == 'C':
			m = 12.01
		if atom[-1]== 'N':
			m = 14.00
		if atom[-1]== 'O':
			m = 15.99
		if atom[-1] == 'H':
			m = 1.00
		if atom[-1] == 'S':
			m = 32.07
		if atom[-1] == 'P':
			m = 30.97
		if atom[-1] == 'MG':
			m = 24.30
		sm = sm + m
		x = float(atom[6])
		smx = smx + m*x

	x_cm = smx/sm
	
	sm = 0
	smy = 0
	for atom in Atomlist:
		if atom[-1] == 'C':
			m = 12.01
		if atom[-1]== 'N':
			m = 14.01
		if atom[-1]== 'O':
			m = 16.0
		if atom[-1] == 'H':
			m = 1.01
		if atom[-1] == 'S':
			m = 32.07
		if atom[-1] == 'P':
			m = 30.97
		if atom[-1] == 'MG':
			m = 24.30
		sm = sm + m
		y = float(atom[7])
		smy = smy + m*y

	y_cm = smy/sm
	
	sm = 0
	smz = 0
	for atom in Atomlist:
		if atom[-1] == 'C':
			m = 12.01
		if atom[-1]== 'N':
			m = 14.01
		if atom[-1]== 'O':
			m = 16.0
		if atom[-1] == 'H':
			m = 1.01
		if atom[-1] == 'S':
			m = 32.07
		if atom[-1] == 'P':
			m = 30.97
		if atom[-1] == 'MG':
			m = 24.30
		sm = sm + m
		z = float(atom[8])
		smz = smz + m*z

	z_cm = smz/sm


################################# editing
fout = open("output.pdb",'w')
for atom in Atomlist:
	x = float(atom[6]) - x_cm
	y = float(atom[7]) - y_cm
	z = float(atom[8]) - z_cm
	occ = "{:6.2f}".format(float(atom[9]))
	temp = "{:6.2f}".format(float(atom[10]))
	serial = int(atom[1])
	chainID = int(atom[5])
	line = '%s %6s  %-3s %s %s%4s %s%s%s%s%s%12s\n' %(atom[0],serial,atom[2],atom[3],atom[4],chainID,"{:11.3f}".format(x),"{:8.3f}".format(y),"{:8.3f}".format(z),occ,temp,atom[11])
	fout.write(line)
		

fout.close()