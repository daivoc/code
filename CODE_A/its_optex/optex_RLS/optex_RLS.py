#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import binascii
import os, traceback
import fcntl
import struct
import time
import subprocess 
import re
import math
import MySQLdb

import config_db as c
from module_for_optex import *
from module_for_mysql import *

from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

def all(packet):
	return binascii.hexlify(packet).decode()

def hex2int(dataObj): # 정수를 부호있는 숫자로 변환
	x = int(binascii.hexlify(dataObj).decode(), 16)
	if x > 0x7FFFFFFF:
		x -= 0x100000000
	return x
	
def errorCheck(packet):
	code = packet.split('\n')[3][2:4]
	if code == '00':
		msg = ''
	elif code == '10':
		msg = '[%s] Requested command is not supported.' % code
	elif code == '11':
		msg = '[%s] Format Error.' % code
	elif code == '12':
		msg = '[%s] Requested command is ignored because it is doubled.' % code
	else:
		msg = '[%s] Unknow Error' % code
	return msg	

def getValue(packet):
	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	return dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.

def cmd00(packet): # Sensor information.
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	# ['OPTEX', 'RLS-3060', 'SH', '0100', '\x00\x1f\xd1\x16\x06\xd3', '', '']
	# print(packet.splitlines()[0]) # 'OPTEX'
	# print(packet.splitlines()[1]) # 'RLS-3060'
	# print(packet.splitlines()[2]) # 'SH'
	# print(packet.splitlines()[3]) # '0100'
	# print(packet.split('\n\n\r')[0])
	return '%s %s %s' % (packet.splitlines()[0], packet.splitlines()[1], packet.splitlines()[2]) # INFO

def cmd01(packet): # 맥 어드레스
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode
	return all(getValue(packet))
	
def cmd02(packet): # 버전 정보
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode
	return getValue(packet)
	
def cmd03(packet): # 유니트 아이디
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode
	return getValue(packet)
	
def cmd04(packet): #  Area Set 정보
	# http://www.mathbang.net/159 삼각법 참고
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = getValue(packet)
	cntObj = len(dataObj)/4 # 4 바이트씩 그룹핑 - 기본 Object Info Size (760개)
	
	count = 0
	objInfo = ''
	unitAngle = 0.25 # float(190/760)
	while (count < cntObj):
		orgX = 0 # 30000 # 출력화면의 X축 0점이 30000에서 시작한다.
		fLN = count * 4
		tLN = fLN + 4
		# print all(dataObj[fLN:tLN])
		length = hex2int(dataObj[fLN:tLN])
		angle = math.radians(unitAngle * (count - 20)) # 시작이 -20번째부터 진행 한다(총 185도)
		distX = int(length * math.cos(angle))
		distY = int(length * math.sin(angle))
		
		# print '%s:%s-%s:%s' % (count, unitAngle * (count - 20), distX, distY)
		
		objInfo += "L %s %s " % (distX + orgX, distY)
		count = count + 1
		
	objInfo = "<path d='M%s 0 %s Z' fill='#ffa50073' />" % (orgX, objInfo)
			
	return objInfo, cntObj
	
def cmd05(packet): # 존(zone Type) 정보
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = getValue(packet)
	objInfo = '%s %s %s %s %s %s' % (hex2int(dataObj[0:4]), hex2int(dataObj[4:8]), dataObj[8:14], dataObj[14:17], dataObj[17:18], hex2int(dataObj[18:22]))
	return (objInfo)
	
def cmd06(packet): # 이벤트 발생정보 
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = getValue(packet)
	cntObj = len(dataObj)/20 # 20 바이트씩 그룹핑 - 기본 Object Info Size
	count = 0
	objInfo = ''
	while (count < cntObj):
		fFX = count * 20
		fFY = fFX + 4
		fOX = fFY + 4
		fOY = fOX + 4
		fSZ = fOY + 4
		
		tFX = fFX + 4
		tFY = fFY + 4
		tOX = fOX + 4
		tOY = fOY + 4
		tSZ = fSZ + 4
		
		objID = '%s%s' % (hex2int(dataObj[fFX:tFX]),hex2int(dataObj[fFY:tFY])) # First X,Y coordinate
		objX = hex2int(dataObj[fOX:tOX]) # X-coordinate of detected object.
		objY = hex2int(dataObj[fOY:tOY]) # Y-coordinate of detected object.
		objD = hex2int(dataObj[fSZ:tSZ]) # Size of the detected object

		# objInfo += '%s,' % str(12000-(hex2int(dataObj[fOX:tOX])+6000)) # 화면 표시용 X-coordinate of detected object.
		objInfo += '%s,%s,%s,%s|' % (re.sub('-', '',str(objID)), str(objX), str(objY), str(objD))
		
		count = count + 1
		
		# print objID, objX, objY, objD
	return objInfo

def cmd07(packet): # 기본 좌표 정보
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = getValue(packet)
	objInfo = '%s %s %s' % (dataObj[0:4], dataObj[4:8], dataObj[8:12])
	return (objInfo)
	
def cmd08(packet): # 센서 이벤트 출력 정보
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	return getValue(packet)

def cmd09(packet): # 릴레이 정보
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	return getValue(packet)

def cmd10(packet): # 마스킹/얼로케이션 파일
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	return getValue(packet)

def cmd11(packet): # 마스킹/얼로케이션 영역
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode
	dataObj = getValue(packet)
	zone_type = int(dataObj[0:1]) # 0 means current setting is masking. 1 means current setting is allocating.
	# zone_type = int(all(dataObj[0:1]))-30 # 0 means current setting is masking. 1 means current setting is allocating.
	dataObj = dataObj[2:] # 3번째 문자이후의 모든 데이터를 선별한다.
	cntObj = len(dataObj)
	count = 0
	objInfo = ''
	zone_data = ''
	zone_html = ''
	zone_color = {}
	zone_color[0] = '#006400'
	zone_color[1] = '#ed143d'
	zone_color[2] = '#9400d3'
	zone_color[3] = '#000080'
	zone_color[4] = '#800000'
	zone_color[5] = '#ffa500'
	zone_color[6] = '#009e9e'
	zone_color[7] = '#f4ff00'
	zone_color[14] = '#000000'
	
	sizeXY = 300
	offset = 30000
		
	while (count < cntObj):
		fFX = count * 1
		tFX = fFX + 1
		
		tmp_zone = dataObj[fFX:tFX]
		if ord(tmp_zone) is not 0x0F:
			# 순서 값에서 행과 열값을 구하기 위해 가로 총수 200으로 나누어 몫을 행으로 나머지 값을 열로 선언한다.
			# 행의 시작이 아래부터 시작 함으로 전체 행 및 열값에 단위길이 300(mm)를 곱한다.
			zX = (count % 200 * sizeXY) - offset
			zY = (99 - (count / 200)) * sizeXY
			zT = hex2int(tmp_zone) # zone type
			zone_data += '%d:%d:%d,' % (zX,zY,zT)
			zone_html += "<rect style='fill:%s20; stroke:%s; stroke-width:2px;' x='%s' y='%s' width='%s' height='%s'></rect>" % (zone_color[zT],zone_color[zT],zX,zY,sizeXY,sizeXY)
		
		count = count + 1
		
	return (zone_type, zone_html) # mask or allocating and data
	
def cmd12(packet): # 모델명
	respCode = errorCheck(packet) # errorCheck(code)
	# respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = getValue(packet)
	len_m_name = int(all(dataObj[0:1]))
	m_name = dataObj[1:len_m_name+1]
	len_s_name = int(all(dataObj[len_m_name+1:len_m_name+2]))
	s_name = dataObj[len_m_name+2:len_m_name+2+len_s_name]
	objInfo = '%s %s' % (m_name, s_name)
	return (objInfo) 

def reqCommand(id):
	command = {}
	command['cmd01'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][01][LF][LF][CR]'	# Requests MAC address.
	command['cmd02'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][02][LF][LF][CR]'	# Requests version number.
	command['cmd03'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][03][LF][LF][CR]'	# Requests ID of the unit.
	command['cmd04'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][04][00][LF][LF][CR]'	# Requests detection area information. 
	command['cmd05'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][05][LF][LF][CR]'	# Requests zone (area AB) information.
	command['cmd06'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][50][0011][LF][LF][CR]'	#  To start the report by limiting the number of detected objects to 50 and specifing 50 ms for valid report interval,
	command['cmd06I'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][25][0100][LF][LF][CR]'	#  To start the report by limiting the number of detected objects to 25 and specifing 5000 ms for valid report interval,
	command['cmd06S'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][0][00][0000][LF][LF][CR]'	# STOP Requests detected object information. 
	command['cmd06L'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][30][0000][LF][LF][CR]'	# To request only one report limiting the number of detected object to 30.
	command['cmd07'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][07][LF][LF][CR]'	# Requests basic parameter of detection area. 
	command['cmd08'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][08][LF][LF][CR]'	# TCP - Requests destination of Redwall Event Code (REC) and sending sample REC.
	# command['cmd09'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][09][02][600][LF][LF][CR]'	# In case of activating Output 02 10 minutes (600 sec.) Controls the relay output.
	command['cmd09'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][09][02][0][LF][LF][CR]'	# In case of activating Output 02 10 minutes (600 sec.) Controls the relay output.
	command['cmd10'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][10][CS][LF][LF][CR]'	# Requests/switches masking/allocating File.
	command['cmd11'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][11][LF][LF][CR]'	# Requests masking/allocating area information.
	command['cmd12'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][12][LF][LF][CR]'	# Requests model name.(Only 2020)
	# command['cmd99'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][99][OPTEX][@][OPTEXP][LF][LF][CR]'	# Requests Password
	# command['cmd99'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][99][LF][LF][CR]'	# Requests Password
	return command[id].replace('[','').replace(']','').replace('LF','\n').replace('CR','\r')
	
# 자신 아이피 확인 
def get_ip_address(ifname): # get_ip_address('eth0')  # '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])
	
def realtime_monitoring(ip,port,objInfo):
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((ip,port))
		node.send(objInfo) 
		# print objInfo
		# return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 

def filterRZone(id, X, Y, D, rsx, rsy, rex, rey): # 정대 좌표에서 기준갑을 통해 상대좌표 추출
	iX = int(X) # X값
	iY = int(Y) # Y값
	iS = int(D) # 직경
	
	if (rsx < rex and rsy < rey):
		if (rsx < iX and rsy < iY and rex > iX and rey > iY):
			return "%s,%s,%s,%s" % (id, iX, iY, iS)
			# return "%s,%s,%s,%s" % (id, iX-rsx, iY-rsy, iS)
		else:
			return ""
	else:
		return "%s,%s,%s,%s" % (id, iX, iY, iS)
		
def filterZone(type, X, Y, D):
	iX = int(X) # X값
	iY = int(Y) # Y값
	iS = int(D) # 직경
	lX = iX / 1000 # 미터로 표시 Location X
	lY = iY / 1000 # 미터로 표시 Location Y
	lS = iS / 10 # 센지로 표시 Location S
	if type == "2020":
		if (iX>iY):
			zone = 'A'
		else:
			zone = 'B'
	elif type == "3060":
		if (iX>0):
			zone = 'A'
		else:
			zone = 'B'
	else:
		zone = 'X'
	return "%s:%s:%s:%s" % (zone, lX, lY, lS) 
		
def filterSize(diameter):
	result = 0 # 0:invalid, 1:valid
	for idx, val in enumerate(db_allowSize):
		# print(idx, val)
		limits = val.split(":")
		if(int(diameter) >= int(limits[0]) and int(diameter) <= int(limits[1])): # 이밴트 크기 비교
			result = 1
	return result

def filterArea(X, Y):
	# ['167:2445_186:2838', '1590:2811_1607:2840']
	result = 1 # 0:invalid, 1:valid
	for idx, val in enumerate(db_sensor_ignoreZone):
		# print(idx, val)
		area = val.split("_") # '167:2445_186:2838'
		minXY = area[0].split(":")
		maxXY = area[1].split(":")
		minX = minXY[0]
		minY = minXY[1]
		maxX = maxXY[0]
		maxY = maxXY[1]
		# if (((int(X) < int(minX)) and (int(X) > int(maxX))) or ((int(Y) < int(minY)) and (int(Y) > int(maxY)))):
		# if ((int(X) < minX) and (int(X) > maxX)) and ((int(Y) < minY) and (int(Y) > maxY)):
		# if ((int(X) >= minX) and (int(X) <= maxX)) or ((int(Y) >= minY) and (int(Y) <= maxY)):
		# if 10000 <= number <= 30000:
		
		if (int(X) >= int(minX)) and (int(X) <= int(maxX)) and (int(Y) >= int(minY)) and (int(Y) <= int(maxY)):
			return 0
	return result

	
# 센서 아이피 확인 
def check_sensor(sensorIP): # 50001 포트가 살아있는지 확인 한다.
    # return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.1)
	result = sock.connect_ex((sensorIP, 50001))
	sock.close()
	return result

def getSnapshot(db_url): 
	# 이벤트 스크린샷
	# print time.strftime('%Y/%m/%d')
	tmpYear = img_data_sub+time.strftime('%Y/') # 년도 방
	if not os.path.exists(tmpYear): # WITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpYear)
	tmpMonth = tmpYear+time.strftime('%m/') # 월별 방
	if not os.path.exists(tmpMonth): # WITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpMonth)
	tmpDay = tmpMonth+time.strftime('%d/') # 일별 방
	if not os.path.exists(tmpDay): # WITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpDay)
	tmpFullPath = tmpDay+time.strftime('%H/') # 시간별 방
	if not os.path.exists(tmpFullPath): # WITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpFullPath)
	tmpName = time.strftime('%M_%S-URL_01') + ".jpg"
	
	thisImgName = tmpFullPath + tmpName
	run_wget_image(db_url, thisImgName) # Ontime Screenshot
	
	# return thisImgName[13:] # 머리부분 /var/www/html을 제거
	return thisImgName[21:] # 머리부분 /var/www/html/its_web을 제거

def help_message(): 
	print "Usage:\n"
	print "\t%s <sensor address> [-option]\tStore event data to databases" % sys.argv[0]
	print "Option:\n"
	print "\t-i\t\tShow sensor information"
	print "\t-d\t\tShow database information"
	print "\t-r [from] [to]\tReview event history, date format is yyyy-mm-dd hh:mm:ss"
		
###################################################
###################################################
def main ():
	# Create a TCP/IP socket
	sockS30 = socket.create_connection((db_sensor_Addr, sensorPort)) # 센서 연결
	
	# sockS30.sendall(reqCommand('cmd99'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd99 = cmd99(data_tmp)
	# print "password: ", result_cmd99
	
	# mac address
	sockS30.sendall(reqCommand('cmd01'))
	data_tmp = sockS30.recv(1024)
	result_cmd01 = cmd01(data_tmp)
	# print "MAC address: ", result_cmd01
	
	# version
	sockS30.sendall(reqCommand('cmd02'))
	data_tmp = sockS30.recv(1024)
	result_cmd02 = cmd02(data_tmp)
	# print "Version: ", result_cmd02
	
	# unit ID
	sockS30.sendall(reqCommand('cmd03'))
	data_tmp = sockS30.recv(1024)
	result_cmd03 = cmd03(data_tmp)
	# print "Unit ID: ", result_cmd03

	# area No
	sockS30.sendall(reqCommand('cmd04')) # 센서에 자료('cmd04') 요청 - 총 760 라인
	data_tmp = ''
	# 기본크기를 알수 없는 패킷정보를 읽어들인다.
	while True:
		data_tmp += sockS30.recv(1024)
		if all(data_tmp[-3:]) == '0a0a0d': 
			# print 'last socket'
			break
	if data_tmp:
		result_cmd04, result_cmd04_2 = cmd04(data_tmp)
	else:
		result_cmd04 = ''
		result_cmd04_2 = 0
	# print "No. of detection area: ", result_cmd04_2, result_cmd04 # Area	

	#####################################
		
	# zone information
	sockS30.sendall(reqCommand('cmd05'))
	data_tmp = sockS30.recv(1024)
	result_cmd05 = cmd05(data_tmp)
	# print "Radius of area A/B, Type, No. of regions, Mode: ", result_cmd05
	
	# basic parameter
	sockS30.sendall(reqCommand('cmd07'))
	data_tmp = sockS30.recv(1024)
	result_cmd07 = cmd07(data_tmp)
	# print "Angle, No. of lines, Center of lines: ", result_cmd07
	
	# destination of Redwall
	sockS30.sendall(reqCommand('cmd08'))
	data_tmp = sockS30.recv(1024)
	result_cmd08 = cmd08(data_tmp)
	# print "Communication by (TCP)(UDP): ", result_cmd08
	
	# relay output
	sockS30.sendall(reqCommand('cmd09'))
	data_tmp = sockS30.recv(1024)
	result_cmd09 = cmd09(data_tmp)
	# print "Relay output: ", result_cmd09

	# masking/allocating file
	sockS30.sendall(reqCommand('cmd10'))
	data_tmp = sockS30.recv(1024)
	result_cmd10 = cmd10(data_tmp)
	# print "Masking/Allocating file: ", result_cmd10

	# masking/allocating area
	sockS30.sendall(reqCommand('cmd11'))
	data_tmp = ''
	# 기본크기를 알수 없는 패킷정보를 읽어들인다.
	while True:
		data_tmp += sockS30.recv(1024)
		if all(data_tmp[-3:]) == '0a0a0d': 
			# print 'last socket'
			break
	if data_tmp:
		result_cmd11 = cmd11(data_tmp)
		result_cmd11_A = '' # allocating area
		result_cmd11_M = '' # masking area
		if result_cmd11[0] == 1:
			result_cmd11_A = result_cmd11[1]
			result_cmd11 =  "Allocate zone: Enabled"
		else:
			result_cmd11_M = result_cmd11[1]
			result_cmd11 =  "Mask zone: Enabled"
	else:
		result_cmd11_A =''
		result_cmd11_M =''
		result_cmd11 =  "No masking/allocating area"
	# print result_cmd11, result_cmd11_A, result_cmd11_M

	# model name
	sockS30.sendall(reqCommand('cmd12'))
	data_tmp = sockS30.recv(1024)
	result_cmd12 = cmd12(data_tmp)
	if '2020' in result_cmd12: 
		type_RLS = "2020" # 센서타입 2020 또는 3060
	else:
		type_RLS = "3060" # 센서타입 2020 또는 3060
	# print "Model name: ", result_cmd12 # , all(data_tmp)
	
	#################################################
	# 템플릿 HTML 파일을 읽고 관련 정보로 치환하여
	# nodeJs의 common 소스로 저장한다.
	path = "/var/www/html/its_web/theme/ecos-its_optex/utility/nodeJs_table" 
	source = "%s/realtime_RLS_templet.html" % path # Optex Theme
	source_area = "%s/realtime_RLS_templet_Area.html" % path # Optex Theme
	target = "%s/realtime_RLS_%s.html" % (path, nodeIn) # Optex Theme
	target_area = "%s/realtime_RLS_%s_Area.html" % (path, nodeIn) # Optex Theme

	gridStep = 1000 # 1미터 - 1000
	if type_RLS == "2020":
		html_viewBox = "-2700 -2700 60000 32700"
		html_grid = ''
		for i in range(-9, 100):
			html_grid += "<path id='grid_h_%s' d='M -2700 %s h 32700' stroke='silver' stroke-width='1px'></path>" % (i,(i*gridStep))
		for i in range(-9, 100):
			html_grid += "<path id='grid_v_%s' d='M %s -2700 v 32700' stroke='silver' stroke-width='1px'></path>" % (i,(i*gridStep))
		html_frame = "<path style='fill:#00000040;' d='M 0,0 v 30000 a -30000,-30000 0 0,0 30000,-30000 Z'></path><path style='fill:#00000000; stroke:black; stroke-width:10px;' d='M 0 30000 L -2700 30000 L 0 0 L 30000 -2700 L 30000 0 '></path>"
		html_zone = "<rect style='fill:#faebd738; stroke:gray; stroke-width:8px;' x='0' y='0' width='20000' height='20000'></rect>"
	elif type_RLS == "3060":
		html_viewBox = "-30000 -2700 60000 32700"
		html_grid = ''
		for i in range(-9, 100):
			html_grid += "<path id='grid_h_%s' d='M -30000 %s h 60000' stroke='silver' stroke-width='1px'></path>" % (i,(i*gridStep))
		for i in range(0, 200):
			html_grid += "<path id='grid_v_%s' d='M %s -2700 v 32700' stroke='silver' stroke-width='1px'></path>" % (i,((i*gridStep)-30000))
		html_frame = "<path style='fill:#00000040;' d='M -30000 0 C -30000 40000, 30000 40000, 30000 0 Z'></path><path style='fill:#00000000; stroke:black; stroke-width:10px;' d='M -30000 0 L -30000 -2700 L 0 0 L 30000 -2700 L 30000 0 '></path>"
		html_zone = "<rect style='fill:#abc7d74d; stroke:gray; stroke-width:8px;' x='-30000' y='0' width='30000' height='30000'></rect> <rect style='fill:#00000000; stroke:gray; stroke-width:6px;' x='-15000' y='0' width='30000' height='30000'></rect> <rect style='fill:#faebd738; stroke:gray; stroke-width:8px;' x='0' y='0' width='30000' height='30000'></rect>"
	
	tag_nameID = "__name_and_serial__"
	tag_model = "__model_and_rev__"
	tag_version = "__version__"
	tag_viewBox = "__svg_viewBox__" # svg id="svg_id" viewBox
	tag_zone = "__boundary_of_zone__"
	tag_area = "__boundary_of_area__"
	tag_mask = "__boundary_of_mask__"
	tag_allocate = "__boundary_of_allocate__"
	tag_grid = "__boundary_of_grid__"
	tag_frame = "__boundary_of_frame__"
	
	__script_jquery_js__ = '/home/pi/common/jquery/jquery-3.1.1.min.js'
	__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	__script_jquery_ui_js__ = '/home/pi/common/jquery/ui/jquery-ui.js'
	__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	__style_jquery_ui_css__ = '/home/pi/common/jquery/ui/jquery-ui.css'
	__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	__svg_pan_zoom__ = '/home/pi/common/svg-pan-zoom/svg-pan-zoom.js'
	__svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'
	
	inc_jq = "__script_jquery_js__"
	inc_jq_ui = "__script_jquery_ui_js__"
	inc_jq_ui_css = "__style_jquery_ui_css__"
	inc_svg_pan_zoom = "__svg_pan_zoom__"

	replacements = {tag_nameID:"Name:"+db_subject+" Serial:"+db_sensor_serial, tag_model:result_cmd12, tag_version:result_cmd02, tag_zone:html_zone, tag_area:result_cmd04, tag_mask:result_cmd11_M, tag_allocate:result_cmd11_A, tag_grid:html_grid, tag_frame:html_frame, tag_viewBox:html_viewBox, inc_jq:__script_jquery_js__, inc_jq_ui:__script_jquery_ui_js__, inc_jq_ui_css:__style_jquery_ui_css__, inc_svg_pan_zoom:__svg_pan_zoom__}
	with open(source) as infile, open(target, 'w') as outfile:
		for line in infile:
			for src, target in replacements.iteritems():
				line = line.replace(src, target)
			outfile.write(line)
			
	# 센서이 감지영역만에 자료 생성
	replacements = {tag_model:result_cmd12, tag_version:result_cmd02, tag_zone:html_zone, tag_area:result_cmd04, tag_mask:result_cmd11_M, tag_allocate:result_cmd11_A, tag_grid:html_grid, tag_frame:html_frame, tag_viewBox:html_viewBox, inc_jq:__script_jquery_js__, inc_jq_ui:__script_jquery_ui_js__, inc_jq_ui_css:__style_jquery_ui_css__, inc_svg_pan_zoom:__svg_pan_zoom__}
	with open(source_area) as infile, open(target_area, 'w') as outfile:
		for line in infile:
			for src, target_area in replacements.iteritems():
				line = line.replace(src, target_area)
			outfile.write(line)

	if("cmd01" in commandID): print "MAC address: %s " % result_cmd01
	if("cmd02" in commandID): print "Version: %s " % result_cmd02
	if("cmd03" in commandID): print "Unit ID: %s " % result_cmd03
	if("cmd04" in commandID): print "No. of detection area: %s " % [result_cmd04_2, result_cmd04]
	if("cmd05" in commandID): print "Radius of area A/B, Type, No. of regions, Mode: %s " % result_cmd05
	if("cmd07" in commandID): print "Angle, No. of lines, Center of lines: %s " % result_cmd07
	if("cmd08" in commandID): print "Communication by (TCP)(UDP): %s " % result_cmd08
	if("cmd09" in commandID): print "Relay output: %s " % result_cmd09
	if("cmd10" in commandID): print "Masking/Allocating file: %s " % result_cmd10
	if("cmd11" in commandID): print "Masking/Allocating area: %s " % [result_cmd11, result_cmd11_A, result_cmd11_M]
	if("cmd12" in commandID): print "Model name: %s " % result_cmd12
	
	#################################################
	# 데이터베이스 테이블 생성
	returnMsg = create_table_w_log_RLS(db_sensor_serial) # postfix='' + mac address
	# print returnMsg # 0 - Success
	
	
	sockS30.sendall(reqCommand('cmd06')) # 센서에 자료('cmd06') 요청
	try:
		while True:
			data_tmp = sockS30.recv(1024)
			result_cmd06 = cmd06(data_tmp) # 센서로 부터 받은 자료
			if result_cmd06:  # 42949672541081,422,676,355|42949672541081,259,861,54|
				data = result_cmd06.split("|")
				for singleEvent in data:
					if singleEvent: # 42949672541081,422,676,355
						eleEvt = singleEvent.split(",") # 42949672541081,422,676,355
						eventZone = filterZone(type_RLS, eleEvt[1], eleEvt[2], eleEvt[3])
						insert_event_RLS(db_sensor_serial, eleEvt[0], eleEvt[1], eleEvt[2], eleEvt[3], eventZone)
						realtime_monitoring(db_system_ip,nodeIn,singleEvent)
						####### 호스트서버에 자료 전송 #######
						if db_host_Addr and db_host_Port:
							send_event_to_host(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, eventZone) # 관제에 이벤트 전송
						if db_host_Addr2 and db_host_Port2:
							send_event_to_host(db_host_Addr2, db_host_Port2, db_subject, db_sensor_serial, eventZone) # 관제에 이벤트 전송

						insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=result_cmd12, board=c.ECOS_table_RLS, tableID=myTableID, status=Event_type['active'], msg=Event_desc[Event_type['active']])
			else: # 휴식 상태
				send_event_to_host(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, 0) # 하트비트
				####### 주메뉴 스테이터스 - 소켓 유니온 전송 #######
				insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=result_cmd12, board=c.ECOS_table_RLS, tableID=myTableID, status=Event_type['idle'], msg=Event_desc[Event_type['idle']])
				# print all(data_tmp)
				for row in read_field_w_cfg_status(myTableID):
					db_sensor_stop = row["w_sensor_stop"]		# `w_sensor_stop` TINYINT(1) - 일시정지
					db_sensor_reload = row["w_sensor_reload"] 	# `w_sensor_reload` TINYINT(1) - 재시동
					db_sensor_disable = row["w_sensor_disable"]	# `w_sensor_disable` TINYINT(1) -알람중지
					db_alarm_disable = row["w_alarm_disable"]	# `w_sensor_disable` TINYINT(1) -알람중지
				
				if db_sensor_reload: # 재시동
					set_reload_w_cfg_reload(myTableID) # 재시동 필드를 회복시킨다.
					restart_its()
	finally:
		print 'closing socket_S30'
		sockS30.close()

if __name__ == '__main__':
	if len(sys.argv) > 1: 
		myTableID = sys.argv[1]
	else:
		exit("No database Information, Check Sensor's Config...")
		
	w_cfg_sensor_list_All = read_table_w_cfg_sensor_all(myTableID)
	for row in w_cfg_sensor_list_All:
		db_subject = row["wr_subject"]
		db_license = row["w_license"]
		# db_device_id = row["w_device_id"]
		db_sensor_serial = row["w_sensor_serial"]
		db_sensor_lat_s = row["w_sensor_lat_s"]
		db_sensor_lng_s = row["w_sensor_lng_s"]
		db_sensor_lat_e = row["w_sensor_lat_e"]
		db_sensor_lng_e = row["w_sensor_lng_e"]
		db_table_PortIn = row["w_table_PortIn"]
		db_event_holdTime = row["w_event_holdTime"] # 에벤트 홀드 수
		db_system_ip = row["w_system_ip"]
		db_system_port = row["w_system_port"]
		db_sensor_Addr = row["w_sensor_Addr"]
		db_email_Addr = row["w_email_Addr"]
		db_email_Time = row["w_email_Time"]
		db_host_Addr = row["w_host_Addr"] # 관제 서버 이이피
		db_host_Port = row["w_host_Port"] # 관제 서버 포트
		db_host_Addr2 = row["w_host_Addr2"] # 관제 서버 이이피
		db_host_Port2 = row["w_host_Port2"] # 관제 서버 포트
		db_url = row["w_url1"] #
		db_alert_Port = int(row["w_alert_Port"])
		db_alert_Value = float(row["w_alert_Value"])
		db_allowSize = (str(int(row["w_sensor_ignoreS"]))+':'+str(int(row["w_sensor_ignoreE"]))).split(',') # 이벤트 허용 크기
		if row["w_sensor_ignoreZone"]: 
			db_sensor_ignoreZone = row["w_sensor_ignoreZone"].encode("utf-8").replace(" ", "").rstrip(',').split(',') # 이벤트 무시 영역
		else:
			db_sensor_ignoreZone = []

		if db_alert_Port:
			try: # GPIO 포트 초기화
				GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
				GPIO.setup(db_alert_Port, GPIO.OUT)
				GPIO.output(db_alert_Port, GPIO.HIGH)
				if db_alarm_disable: print "Enable GPIO", db_alert_Port
			# except KeyboardInterrupt:
				# GPIO.cleanup()
			except:
				pass
			
	commandID = "cmd01 cmd02 cmd03 cmd_04 cmd05 cmd_06 cmd07 cmd08 cmd09 cmd10 cmd_11 cmd_12"
	sensorPort = 50001
	mySensorID = db_sensor_serial

	print "SensorID:",db_sensor_serial
	print "Accept Size:",db_allowSize
	print "Refuse Area:",db_sensor_ignoreZone
	
	############ Images ################
	# 이미지 파일 초기화 
	if not os.path.exists(c.ITS_img_data): # ITS_img_data 폴더 생성
		os.makedirs(c.ITS_img_data)
	# 센서 이벤트 스크린샷 이미지 저장 폴더명
	img_data_sub = c.ITS_img_data + mySensorID + "/"
	if not os.path.exists(img_data_sub): # ITS_img_data 내의 서브 사진 폴더 생성
		os.makedirs(img_data_sub)
	############ Images ################
	
	varPort = int(db_sensor_Addr.split('.')[2]) + int(db_sensor_Addr.split('.')[3])
	nodeIn = 50000 + varPort # db_sensor_Addr = '192.168.168.30' -> 50198
	nodeOut = 51000 + varPort # db_sensor_Addr = '192.168.168.30' -> 51198
	print('\nRunning RLS Realtime Monitoring - http://%s:%s' %(db_system_ip,nodeOut))
	
	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)