#!/usr/bin/env python3

import numpy as np
import csv
import glob
import matplotlib.pyplot as plt
import os 

#--------------------------------------------------------------------------------------->
# _We define the z-x-z rotation matrix as a function so we can calculate it after the angles 
# are calculated.

def eulerzxz(th1,th2,th3):
	return np.array( 
			( 
				(
					np.cos(th1)*np.cos(th3) - np.cos(th2)*np.sin(th1)*np.sin(th3), 
					(-1)*np.cos(th2)*np.sin(th1) - np.cos(th2)*np.cos(th3)*np.sin(th1),
					np.sin(th1)*np.sin(th2) 
				),
				(
					np.cos(th3)*np.sin(th1) + np.cos(th1)*np.cos(th2)*np.sin(th3),
					np.cos(th1)*np.cos(th2)*np.cos(th3) - np.sin(th1)*np.sin(th3),
					(-1)*np.cos(th1)*np.sin(th2) 
				),
				(
					np.sin(th2)*np.sin(th3),
					np.cos(th3)*np.sin(th2),
					np.cos(th2)
				)
			)
		)

#--------------------------------------------------------------------------------------->
# _We save the list of text files which contain coordinates of picked points
# _Crown size and rotations are defined (crown size is 14.5nm and pixel size is 0.53 so ~70pixels)

CrownSize = 27 
CrownRotation = 33.75 * np.pi/180

MapList = glob.glob("pickedpoints/points*.pos")


#--------------------------------------------------------------------------------------->
# _Setsfile of tomograms maps and Mapsfile of trfs sets are opened (in defs folder) to be read by i3 package
# _The major loop over text files begins here and goes over all the files (one per tomogram):
# _Tomogram number is saved in numset from the file name
# _The file is opened to read the coordinates

Setsfile = open("defs/sets","w")
Mapsfile = open("defs/maps","w")
for map in range(len(MapList)):
	d = {}
	List = []
	List = '%s'%(MapList[map])
	numset = int(List[19:21])

	numtrf = 0 #number of the  trf file

	map_string = '../maps TR%02d.map ../maps/TR%02d.tlt \n' %(numset,numset)
	Mapsfile.write(map_string)
	
	csvFile = open(MapList[map], 'rt')	#the "rb" mode opens the file in binary format for reading
	csvReader = csv.reader(csvFile, delimiter='\t') # it separates the file line by line
	
	Positionfile = open('positions-final.csv','w')
	
#--------------------------------------------------------------------------------------->
# _The loop over pairs of start and end points is started (#each row in the file represents 
#a thick fillament that has several segments and all of them have the same euler angles)
# _Slopes in x, y, and z are calculated
# _The number of crowns is calculated from the length of the picked filament 
# -The crown points got fit to the filament as they should be

	for row in csvReader:	
	
		d = row[0:] # is an array of strings here which are the coordinates 
		#print(d)

		p = np.zeros(np.size(d)) 

		for i in range(np.size(d)):
			p[i] = np.float(d[i]) #p is the numbers for coordinates (string to float)
		#print(p)

		dx = p[3] - p[0]#the format of input is x1 y1 z1 for start point and x2 y2 z2 for end points 
		dy = p[4] - p[1]
		dz = p[5] - p[2]

		lenght = np.sqrt(dx**2 + dy**2 + dz**2)

		mx = dx / lenght #cos of angels that the line makes with the axes
		my = dy / lenght 
		mz = dz / lenght

		numpoint = int(lenght / CrownSize) #number of points fitting in the selected filament
		#print(numpoint) 

#--------------------------------------------------------------------------------------->
# _All of the middle points are generated using the crown size  slopes c and they are 
#saved in a 3 by (number of points) array	

		points = np.zeros(shape=(numpoint,3))#an array of all the points on one filament
				
		x=[]
		y=[]
	
		for i in range(numpoint):
			points[i][0] = p[0] + mx * i * CrownSize # going up one crown by one crown
			points[i][1] = p[1] + my * i * CrownSize # going up one crown by one crown
			points[i][2] = p[2] + mz * i * CrownSize # going up one crown by one crown
			
			plt.plot(points[i][0],points[i][1],'bo')
		points = points.astype(int) #make the point integer because there are pixels cant be float
		#print(points)

		
#--------------------------------------------------------------------------------------->
# _An IF statement makes sure the filament is more than 3 crowns long, otherwise the program
#jumps to the next filament. This is needed to avoid short filaments

		
		if numpoint < 3: 
			continue 
			
#--------------------------------------------------------------------------------------->
# _The angles are calculated from the slopes to make the rotation happen.
#Note that the first two angles are the same for all subvolumes. We add 90 degrees to the 
#tilt angle to put the filaments on Z-axis

			
		th1 = np.arcsin(dy/np.sqrt(dx**2+dy**2))
		if th1 < 0:
			th1 = np.pi/2 - th1 
		else:
			th1 = th1 - np.pi/2

		th2 = np.arcsin(dz/lenght) + np.pi/2

		
#--------------------------------------------------------------------------------------->
# _The loop over subvolumes of each filament is started
# _Rotation matrix is created using the calculated and a third angle which is 
#subvolume number * -33.75
# _TRF name for trf files is created 
# _Rotation matrix is re-written as a space-separated string with 9 numbers, using join function
#(a 3x3 matrix into 9 strings separated by space)
# _The trf file  is opened, information (trf-name, coordinates of points, Displacements from 
#integer positions which are 0 initially and will change later and the rotation matrix) 
#is written and then it is closed.	
# _Setsfile of tomograms and positionfile for i3 display are written and then are closed


		for i in range(numpoint): 
			rotmat = eulerzxz(-i*CrownRotation, th2, th1)			
			
			numtrf = numtrf + 1
			
			trf_name= "./trf/u%02d_%03d.trf" %(numset,numtrf)
			
			string_rot = ' '.join(' '.join(str(cell) for cell in row) for row in rotmat)
			trfFile = open(trf_name, 'w')

			string_pos = "%d %d %d" %(points[i][0],points[i][1],points[i][2])
			string_pos2 = "%s\n" %(string_pos) 
			Positionfile.write(string_pos2)
			string_temp = '%s %s 0.0 0.0 0.0 %s \n' %(trf_name[6:13],string_pos,string_rot)
			trfFile.write(string_temp)
			
			trfFile.close()
			sets_string = "TR%02d.map %s\n" %(numset,trf_name[6:13])
			Setsfile.write(sets_string)
	Setsfile.close()
	Positionfile.close()

#--------------------------------------------------------------------------------------->
# _The i3 routine is called to prepare the sub volumes for the next step
# _The raw tomogram with points plotted on it is displayed
# _All the points based on their x-y coordinates are plotted

os.system('source /home/taylorlab/programs/emhome/protomo-2.2.1/setup.sh')
os.system('myi3')
os.system('i3display -pos positions-final.csv maps/TR11.map')
os.system('i3mrainitial.sh')
plt.xlabel('x coordinate of points')
plt.ylabel('y coordinate of points')
plt.savefig('theplot.png')
plt.show()

#--------------------------------------------------------------------------------------->
# _a webpage containing a summary of the project is created 

f=open ("FinalProjectResult.html", "w")
f.write("<html>\n")
f.write("<head>\n")
f.write("<h1>%s</h1> <h4>%s</h4>\n" % ("Programming Final Project: Picking sub-volumes of myosin filaments \n", "Hosna Rastegarpouyani \n"))
f.write("<style> h1 {color:blue;} body {background: lightyellow; font-family:arial; text-align:justify;} </style> \n")
f.write("<head>\n")
f.write("<body>\n")
text="""The goal is to study the structure of myosin filaments from insect flight muscle using electron tomography. In order to do that, we need to align and classify the sub-volumes in the raw tomogram. We need to pick each sub-volume manually and rotate it in a way that the z axis would be on the filament axis. This is required by Protomo-i3 package which is a software package used in electron tomography for alignment and 3D reconstruction of tilt series."""
f.write("<p>%s</p>\n"% text)
text="""Subvolume averaging using protomo-i3 package needs the information in an specific format which is not easy to produce. This information includes the 3D position of the subvolumes and rotations that we intend to apply on them. The positions can be picked manually using i3display command. However we have an average of 500 subvolumes per tomogram. In this case (positive-stained myosin filament) we are dealing with helices which are mostly straight that are lying in x-y. The helical symmetry tells us that every 145A along the helix is a repeating pattern with 33.75 degrees rotation. """
f.write("<p>%s</p>\n"% text)
text="""With the help of a code we can lower the manual part to picking the start and end of each filament. The program then finds each repeating pattern along a line that it fits to the two picked points and finds the needed rotation angles."""
f.write("<p>%s</p>\n"% text)
text="""To do this the program should read the start and end points of the filaments in the tomogram from an input file where the start and end points are stored. Next, it should generate new points along the filament, each of them one crown away; dividing each picked filament to smaller fractions (the size will be chosen in i3 package). Myosin crown size is about 145A and each pixel is 5.3A, so the program needs to generate points with 27 pixel separation length. At the end we have to write the center of each box and the rotation matrix in an output file with a special format. This output is named as a trf file which is an essential file for sub-volume averaging with I3 tomography package. There will be one trf file per each sub-volume as the output of this code. """
f.write("<p>%s</p>\n"% text)
text="""For better understanding of the points generated by the program as sub-volumes, we plotted these points based on their x-y coordinates. (figure 1)."""
f.write("<p>%s</p>\n"% text)
text="""In figure 2, you can see these points on the raw image and how they are matched to the filaments."""
f.write("<p>%s</p>\n"% text)

f.write("<img src='theplot.png' height=350 />")
f.write("<img src='thumbnail_tomogram.jpg' height=350; style = \"margin-left:100px;\"/>")
f.write("<br><small>Fig 1: A plot of x-y coordinates </small>")
f.write("<small style= \"margin-left: 450px;\">Fig 2: Points as sub-volumes on the raw imag </small> ")
f.write("<br></br><br></br>\n")

f.write("</body>\n")
f.write("</html>\n")
f.close()



  













