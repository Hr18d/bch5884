#!/usr/bin/env python3
#Hosna Rastegarpouyani

import sys


pdbname=sys.argv[1]

f = open(pdbname, 'r')
lines = f.readlines()

Hosnalist = []

for l in lines:

  words = l.split()
  Hosnalist.append(words)  
print(Hosnalist)
f.close()


f=open("Output.out",'w')  
for words in lines:
	f.write(words)
f.close()

