#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

## lineAC: Distance Sensor to Camera, lineAB: Sensor to End point
## angleOCB: Angle Camera to Sensor angleOCA: Cmaera to End point
## Return 삼각형 내각, 카메라 좌표, 샌서 X방향을 보는 카메라 앵글 
def sinInDegrees(x) :
    return math.sin(math.radians(x))

def cosInDegrees(x) :
    return math.cos(math.radians(x))

def inverseSinInDegrees(x) :
    return math.asin(math.radians(x))

def inverseCosInDegrees(x) :
    return math.acos(math.radians(x))
	
# def solveSSA(lineAC, lineAB, angleOCB, angleOCA) :
    # angleSCT = angleOCA - angleOCB
    # angleSTC = math.degrees(inverseSinInDegrees(math.degrees(lineAC * sinInDegrees(angleSCT) / lineAB)))
    # angleCST = 180 - angleSCT - angleSTC
    # if angleCST > 90 :
        # print("Angle CST is greater than 90")
        # lineCB = (sinInDegrees(angleCST) * lineAC) / sinInDegrees(angleSTC)
        # Cy = lineCB * sinInDegrees(angleSTC)
        # Cx = lineCB * cosInDegrees(angleSTC)
    # else :
        # print("Angle CST is less than 90")
        # Cy = lineAC * sinInDegrees(angleCST)
        # Cx = lineAC * cosInDegrees(angleCST)
    # angleOCX = angleOCA - angleSCT - angleSTC
    # return angleSCT, angleSTC, angleCST, Cy, Cx, angleOCX

# def solveSSA(lineAC, lineAB, angleOCB, angleOCA) :
	# angleSCT = angleOCA - angleOCB
	# angleSTC = math.degrees(sinInDegrees((lineAC * sinInDegrees(angleSCT) / lineAB)))
	# angleCST = 180 - angleSCT - angleSTC
	# angleOCX = angleOCA - angleSCT - angleSTC
	# print angleSCT, angleSTC, angleCST
	# Cx = -(inverseCosInDegrees(angleSCT + angleSTC))
	# Cy = inverseSinInDegrees(angleSCT + angleSTC)
	# return angleSCT, angleSTC, angleCST, Cy, Cx, angleOCX

## SCTO : Sensor, Camera, Target, Orgin
def solveSSA(SC, ST, angleOCS, angleOCT) :
	if angleOCS < 0 : angleOCS = 360 + angleOCS
	if angleOCT < 0 : angleOCT = 360 + angleOCT
	angleSCT = angleOCS - angleOCT
	
	## Case Middle 1, 2, 3, 4, 5
	if abs(angleSCT) == 180.0: ## Case Middle 3
		return 0, 0, 0, 0, SC, angleOCT % 360
	elif angleSCT == 0: 
		if SC < ST: ## Case Middle 1
			return 0, 0, 180, 0, SC, angleOCT % 360
		elif SC > ST: ## Case Middle 5
			return 0, 180, 0, 0, SC, (180 + angleOCS) % 360
	elif angleSCT > 0: 
		if SC == ST and angleOCT == 0 : ## Case Middle 4
			return 0, 0, 0, 0, SC, (180 + angleOCS) % 360
	elif angleSCT < 0: 
		if SC == 0: ## Case Middle 2
			return 0, 0, 0, 0, 0, angleOCT % 360
	
	## Case Upper 1, 2, 3, 4, 5
	angleSTC = math.degrees(math.asin(math.sin(math.radians(angleSCT)) / ST * SC))
	angleCST = 180 - angleSCT - angleSTC
	# print angleSCT, angleSTC, angleCST
	Cx = SC * math.cos(math.radians(angleCST))
	Cy = SC * math.sin(math.radians(angleCST))
	angleAX = angleOCS - angleSCT - angleSTC
	if angleAX >= 360 : 
		angleAX = angleAX - 360
	elif  angleAX < 0 : 
		angleAX = angleAX + 360
	else:
		pass
		
	return angleSCT, angleSTC, angleCST, Cy, Cx, angleAX

## 센서 특성상 x축이 각도 0 으로 설정하기 위해 -90를 더한다.
## Panning, Tilting 모두를 구하는데 사용한다.
def getAngle(x,y) :
	return math.degrees(math.atan2(x,y)) - 90 

## 임의의 두 각으로부터 차이각	
def findAngleDiff(Orgin, Source) :
	angleDiff = abs(((Orgin - Source + 180) % 360) - 180)
	return angleDiff
	
## 두점간의 거리 
## https://ko.wikipedia.org/wiki/%EB%91%90_%EC%A0%90_%EC%82%AC%EC%9D%B4%EC%9D%98_%EA%B1%B0%EB%A6%AC
def distanceXY(x1, y1, x2, y2):
	distanceX = (x2 - x1)**2
	distanceY = (y2 - y1)**2
	distance = math.sqrt(distanceX + distanceY)
	return distance
	
## 카메라(센서기준 또는 지표면 기준)의 좌표를 찾는다.
## 임의의 점 K를 각을 찾아낸다.
## C: findC를 통해 확인된 카메라의 좌표값
## K: 센서로부터 받은 임의의 위치의 죄표
def findSCK_C(C, K, OCS, hC) :
	Cx, Cy = C
	Kx, Ky = K

	## Tilting 각을 찾아내는 루틴
	distance = distanceXY(Cx, Cy, Kx, Ky) ## 카메라와 임의의 위치 까지 거리
	angleT = getAngle(distance, hC)  ## 탄젠트(거리 / 높이) = 각도
	rAngle = getAngle((Kx - Cx), (Ky - Cy)) ## 기준점을 카메라 위치로 이동후 계산
	
	angleP = rAngle + OCS
	if angleP > 360: 
		angleP = angleP - 360
	elif angleP < 0:
		angleP = 360 + angleP
	return angleP, angleT, distance
	
def main ():
	## SCTO : Sensor, Camera, Target, Orgin
	

	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(1.8665, 4.0468, 318.323, 274.880)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A
	
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(1.6470, 4.0468, 346.390, 278.535)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A
	
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(2.6861, 4.0468, 38.570, 296.940)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A
	
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(4.0468, 4.0468, 58.563, 346.389)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A
	
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(5.3801, 4.0468, 58.563, 19.522)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	# print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A


	angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(-0.8782, 4.0468, 256.389, 256.389)
	print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A
	
	angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(0, 4.0468, 0, 256.389)
	print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A

	angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(2.1218, 4.0468, 76.389, 256.389)
	print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A

	angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(4.0468, 4.0468, 76.389, 0)
	print "Angle SCT:%s STC:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A

	angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(5.1218, 4.0468, 76.389, 76.389)
	print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(5.814,10.551),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(7,0),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(0,9),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-3.4023,2.7951),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(1.95871,-25.1799),angleAX,3.5) ## A
	print 'A %20s %20s %20s'%findSCK_C((Cx,Cy),(-9.1095,-3.8375),angleAX,3.5) ## A



	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(1.8665, 4.0468, 194.455, 237.898)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(1.6470, 4.0468, 166.388, 234.243)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(2.6861, 4.0468, 114.208, 215.839)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(4.0468, 4.0468, 94.215, 166.389)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	# angleSCT,angleSTC,angleCST,Cy,Cx,angleAX = solveSSA(5.3801, 4.0468, 94.215, 133.256)
	# print "Angle STC:%s SCT:%s CST:%s Cy:%s Cx:%s AX:%s " % (str(angleSCT),str(angleSTC),str(angleCST),Cy,Cx,angleAX) 
	
		
	# print '\n0,0'
	# print 'A %20s %20s %20s'%findSCK_C((0,0),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((0,0),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((0,0),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((0,0),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((0,0),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((0,0),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((0,0),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((0,0),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((0,0),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((0,0),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((0,0),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((0,0),(0,0),219.6,3.5) ## L

	# print '\n9.0,0'
	# print 'A %20s %20s %20s'%findSCK_C((9.0,0),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((9.0,0),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((9.0,0),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((9.0,0),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((9.0,0),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((9.0,0),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((9.0,0),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((9.0,0),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((9.0,0),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((9.0,0),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((9.0,0),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((9.0,0),(0,0),219.6,3.5) ## L

	# print '\n0,11.0'
	# print 'A %20s %20s %20s'%findSCK_C((0,11.0),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((0,11.0),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((0,11.0),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((0,11.0),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((0,11.0),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((0,11.0),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((0,11.0),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((0,11.0),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((0,11.0),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((0,11.0),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((0,11.0),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((0,11.0),(0,0),219.6,3.5) ## L

	# print '\n12.0,-9.0'
	# print 'A %20s %20s %20s'%findSCK_C((12.0,-9.0),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((12.0,-9.0),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((12.0,-9.0),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((12.0,-9.0),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((12.0,-9.0),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((12.0,-9.0),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((12.0,-9.0),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((12.0,-9.0),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((12.0,-9.0),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((12.0,-9.0),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((12.0,-9.0),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((12.0,-9.0),(0,0),219.6,3.5) ## L

	# print '\n-17.0,0'
	# print 'A %20s %20s %20s'%findSCK_C((-17.0,0),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((-17.0,0),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((-17.0,0),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((-17.0,0),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((-17.0,0),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((-17.0,0),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((-17.0,0),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((-17.0,0),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((-17.0,0),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((-17.0,0),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((-17.0,0),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((-17.0,0),(0,0),219.6,3.5) ## L

	# print '\n-12.0,-0.20'
	# print 'A %20s %20s %20s'%findSCK_C((-12.0,-0.20),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((-12.0,-0.20),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((-12.0,-0.20),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((-12.0,-0.20),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((-12.0,-0.20),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((-12.0,-0.20),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((-12.0,-0.20),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((-12.0,-0.20),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((-12.0,-0.20),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((-12.0,-0.20),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((-12.0,-0.20),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((-12.0,-0.20),(0,0),219.6,3.5) ## L
	# print 'M %20s %20s %20s'%findSCK_C((-12.0,-0.20),(-12.0,-0.20),219.6,3.5) ## M

	# print '\n8.066, 6.919'
	# print 'A %20s %20s %20s'%findSCK_C((8.066, 6.919),(5.814,10.551),219.6,3.5) ## A
	# print 'B %20s %20s %20s'%findSCK_C((8.066, 6.919),(5.814,3.242),219.6,3.5) ## B
	# print 'C %20s %20s %20s'%findSCK_C((8.066, 6.919),(8.000,0.000),219.6,3.5) ## C
	# print 'D %20s %20s %20s'%findSCK_C((8.066, 6.919),(12.813,-9.595),219.6,3.5) ## D
	# print 'E %20s %20s %20s'%findSCK_C((8.066, 6.919),(2.907,-9.595),219.6,3.5) ## E
	# print 'F %20s %20s %20s'%findSCK_C((8.066, 6.919),(0.000,-4.950),219.6,3.5) ## F
	# print 'G %20s %20s %20s'%findSCK_C((8.066, 6.919),(-9.727,-8.625),219.6,3.5) ## G
	# print 'H %20s %20s %20s'%findSCK_C((8.066, 6.919),(-10.338,0.000),219.6,3.5) ## H
	# print 'I %20s %20s %20s'%findSCK_C((8.066, 6.919),(-6.699,3.114),219.6,3.5) ## I
	# print 'J %20s %20s %20s'%findSCK_C((8.066, 6.919),(-6.460,8.989),219.6,3.5) ## J
	# print 'K %20s %20s %20s'%findSCK_C((8.066, 6.919),(0.000,6.890),219.6,3.5) ## K
	# print 'L %20s %20s %20s'%findSCK_C((8.066, 6.919),(0,0),219.6,3.5) ## L
	# print 'M %20s %20s %20s'%findSCK_C((8.066, 6.919),(8.066, 6.919),219.6,3.5) ## M



if __name__ == '__main__':

	main()
