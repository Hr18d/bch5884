#!/usr/bin/env python3
#https://github.com/Hr18d/bch5884.git
#Hosna Rastegarpouyani

import sys, math

#-----------------------------------------------------> read_pdb function
def read_pdb(pdb_filename):
	'''Read and parse the pdb and return a list of atoms'''
	f = open(pdb_filename, 'r')
	lines = f.readlines()
	f.close()
	
	#-------------> parsing the pdb
	records = []
	for line in lines:
		if line[:4]=="ATOM":
			
			d={}
			d['recordname']=line[0:6]
			d['atomnumber']=int(line[6:11])
			d['atomname']=line[12:16]
			d['resName']=line[17:20]
			d['chainID']=line[21:22]
			d['resSeq']=int(line[22:26])
			d['null']=line[26:30]
			d['x']=float(line[30:38])
			d['y']=float(line[38:46])
			d['z']=float(line[46:54])
			d['occupancy']=float(line[54:60])
			d['tempfact']=float(line[60:66])
			d['null2']=line[66:76]
			d['element']=line[76:78].strip()	
			records.append(d)
				
	return records	

#------------------------------------------------------------->  RMSD function 
def RMSD(pdb1, pdb2):
	'''calculate the root mean squared deviation (RMSD) between two PDB structures'''
	atomlist = []
	for i in range(len(pdb1)): 
		atomlist.append(
			(pdb1[i]['x']-pdb2[i]['x'])**2+
			(pdb1[i]['y']-pdb2[i]['y'])**2+
			(pdb1[i]['z']-pdb2[i]['z'])**2)
	
	rmsd = math.sqrt(sum(atomlist)/len(pdb1))

	return rmsd	

pdb_1 = read_pdb('2FA9noend.pdb')
pdb_2 = read_pdb('2FA9noend2mov.pdb')

print('n:', len(pdb_1))
print('RMSD:', RMSD(pdb_1, pdb_2))


