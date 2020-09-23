#!/usr/bin/env python3


xA=float(input("Enter the X coordinate of point A:="))
yA=float(input("Enter the Y coordinate of point A:="))
xB=float(input("Enter the X coordinate of point B:="))
yB=float(input("Enter the Y coordinate of point B:="))
xC=float(input("Enter the X coordinate of point C:="))
yC=float(input("Enter the Y coordinate of point C:="))

import math 
 
dxAB=xB-xA
dyAB=yB-yA
dxAC=xC-xA
dyAC=yC-yA
dxBC=xC-xB
dyBC=yC-yB
 
a=math.sqrt(dxBC**2+dyBC**2)
b=math.sqrt(dxAC**2+dyAC**2)
c=math.sqrt(dxAB**2+dyAB**2)

a2=a**2
b2=b**2
c2=c**2
 
Alpha= math.acos((b2+c2-a2)/(2*b*c));
Beta= math.acos((a2+c2-b2)/(2*a*c));
Gamma= math.acos((a2+b2-c2)/(2*a*b));
 
Alpha= Alpha*180/math.pi;
Beta= Beta*180/math.pi;
Gamma= Gamma*180/math.pi;

 
print("The angle of Alpha is",Alpha)
print("The angle of Beta is",Beta)
print("The angle of Gamma is",Gamma)
















































