#!/usr/bin/python
# -*- coding: utf-8 -*-

# import socket
# import sys
# import binascii
# import os, traceback
# import fcntl
# import struct
# import time
# import subprocess 
# import re
# import math
# import json

# import MySQLdb
# from warnings import filterwarnings
# filterwarnings('ignore', category = MySQLdb.Warning)
from module import *

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
	
def cmd04(packet): # 스켄영역(Area) Set 정보
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
		
	## AUTO Scan 값, 색 채우기
	objInfo = "<path class='html_scan' d='M%s 0 %s Z' />" % (orgX, objInfo)
			
	return objInfo, cntObj
	
def cmd05(packet): # 존(zone Type) 정보
	respCode = errorCheck(packet) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = getValue(packet)
	objInfo = '%s %s %s %s %s %s' % (hex2int(dataObj[0:4]), hex2int(dataObj[4:8]), dataObj[8:14], dataObj[14:17], dataObj[17:18], hex2int(dataObj[18:22]))
	return (objInfo)
	
def cmd06(packet): # 이벤트 발생정보 
	# respCode = errorCheck(packet) # errorCheck(code)
	# if respCode:
	# 	return respCode

	dataObj = getValue(packet)
	cntObj = len(dataObj)/20 # 20 바이트씩 그룹핑 - 기본 Object Info Size
	count = 0
	# objInfo = ''
	objArr = []
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
		# objInfo += '%s,%s,%s,%s|' % (re.sub('-', '',str(objID)), str(objX), str(objY), str(objD))
		objArr.append([objID, objX, objY, objD])
		
		count = count + 1
		
		# print objID, objX, objY, objD
	return objArr # objInfo

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

## 센서 컨트롤 커멘드 생성 값 리턴
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
	
def realtime_monitoring(ip,port,objInfo):
    # 로컬 모니터링 맵에 이밴트 전송
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

# # Filter ##############################################    
# def filterSize(diameter): ## 이벤트 크기 제한
# 	result = 0 # 0:invalid, 1:valid
# 	for idx, val in enumerate(db_allowSize):
# 		# print(idx, val)
# 		limits = val.split(":")
# 		if(int(diameter) >= int(limits[0]) and int(diameter) <= int(limits[1])): # 이밴트 크기 비교
# 			result = 1
# 	return result

# def filterArea(X, Y): # 이벤트의 위치에 따른 수용 또는 거부
# 	# ['167:2445_186:2838', '1590:2811_1607:2840']
# 	# allowZone과 ignoreZone 모두 설정이 되어있으면 ignoreZone은 무시한다.
# 	# if ((db_sensor_allowZone and db_sensor_ignoreZone) or db_sensor_allowZone): # 영역내 이벤트만 수용한다.
# 	if (db_sensor_allowZone): # 영역내 이벤트만 수용한다.
# 		checkZone = db_sensor_allowZone
# 		innerEvent = 1
# 		result = 0
# 	elif (db_sensor_ignoreZone): # 영역내 이벤트는 무시 한다.
# 		checkZone = db_sensor_ignoreZone
# 		innerEvent = 0
# 		result = 1 
# 	else:
# 		# 어떤 영역도 설정되지 않았으면 모두를 유효이벤트로 처리 한다.
# 		return [ 1, 1 ]

# 	# 0:invalid, 1:valid
# 	for idx, val in enumerate(checkZone):
# 		try:
# 			# 1_253_155|229:438_5320:4611
# 			# 1_300_180|4152:2525_10913:9286
# 			name, value = val.split("|") # 1_253_155|229:438_5320:4611
# 			eventID = int(name[0:1]) # 229:438_5320:4611
# 			valX, valY = value.split("_") # 229:438_5320:4611
# 			minXY = valX.split(":")
# 			maxXY = valY.split(":")
# 			minX = minXY[0]
# 			minY = minXY[1]
# 			maxX = maxXY[0]
# 			maxY = maxXY[1]
# 			# if (((int(X) < int(minX)) and (int(X) > int(maxX))) or ((int(Y) < int(minY)) and (int(Y) > int(maxY)))):
# 			# if ((int(X) < minX) and (int(X) > maxX)) and ((int(Y) < minY) and (int(Y) > maxY)):
# 			# if ((int(X) >= minX) and (int(X) <= maxX)) or ((int(Y) >= minY) and (int(Y) <= maxY)):
# 			# if 10000 <= number <= 30000:
# 			# print(idx, val, eventID)
			
# 			if (int(X) >= int(minX)) and (int(X) <= int(maxX)) and (int(Y) >= int(minY)) and (int(Y) <= int(maxY)):
# 				return [ innerEvent, eventID ]
# 		except:
# 			continue
			
# 	return [ result, 0 ]
# # Filter ##############################################    

# Filter ##############################################    
def filterSizeArea(event): ## 이벤트 크기 제한
    MAX = config["db"]["sensor_ignoreE"] # : 5000.0,
    MIN = config["db"]["sensor_ignoreS"] # Min: 254.0,
    evtD = event[3]
    if evtD >= MIN and evtD <= MAX: # 이밴트 크기 비교
        pass
    else:
        return

    ALLOW = config["db"]["sensor_allowZone"] # "sensor_allowZone": "0_544_196|1930:1133_3092:1752,1_595_12|1406:-206_2645:1691",
    IGNORE = config["db"]["sensor_ignoreZone"] # "sensor_ignoreZone": "0_210_144|-105:-99_1374:2652,2_487_235|716:1218_3412:2872",
    if (ALLOW): # 영역내 이벤트만 수용한다.
        checkZone = ALLOW
        allowIS = 1
    elif (IGNORE): # 영역내 이벤트는 무시 한다.
        checkZone = IGNORE
        allowIS = 0
    else:
        return [ 9, 9 ] # 어떤 영역도 설정되지 않았으면 모두를 유효이벤트로 처리 한다.

    tmpFlag = 0
    for val in checkZone.split(","):
        try: # 1_253_155|229:438_5320:4611
            name, value = val.split("|") # 1_253_155|229:438_5320:4611
            eventID = int(name[0:1]) # 1
            valX, valY = value.split("_") # 229:438_5320:4611
            minXY = valX.split(":")
            maxXY = valY.split(":")
            minX = int(minXY[0])
            minY = int(minXY[1])
            maxX = int(maxXY[0])
            maxY = int(maxXY[1])

            # evtX = int(X)
            # evtY  =int(Y)
            evtX = int(event[1])
            evtY = int(event[2])

            # print (minX,"<",evtX,"<",maxX,"-",minY,"<",evtY,"<",maxY)
            if allowIS:
                if (minX <= evtX <= maxX) and (minY <= evtY <= maxY):
                    return [ 1, eventID ] # 1: Allow
            else:
                if (minX <= evtX <= maxX) and (minY <= evtY <= maxY):
                    tmpFlag = 1
        except:
            continue
    if tmpFlag == 0 and allowIS == 0: # 거부영역이며 설정영역내에 이밴트가 없었으면.
        return [ 2, 9 ]
    return
# Filter ##############################################    
## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)
		

###################################################
###################################################
def main ():
    # Create a TCP/IP socket
    sockS30 = socket.create_connection((config["db"]["sensor_Addr"], config["sensor"]["sensorPort"])) # 센서 연결

    # sockS30.sendall(reqCommand('cmd99'))
    # data_tmp = sockS30.recv(1024)
    # result_cmd99 = cmd99(data_tmp)
    # print "password: ", result_cmd99

    # mac address
    sockS30.sendall(reqCommand('cmd01'))
    data_tmp = sockS30.recv(1024)
    result_cmd01 = cmd01(data_tmp)
    print "MAC address: ", result_cmd01

    # version
    sockS30.sendall(reqCommand('cmd02'))
    data_tmp = sockS30.recv(1024)
    result_cmd02 = cmd02(data_tmp)
    print "Version: ", result_cmd02

    # unit ID
    sockS30.sendall(reqCommand('cmd03'))
    data_tmp = sockS30.recv(1024)
    result_cmd03 = cmd03(data_tmp)
    print "Unit ID: ", result_cmd03

    # area No
    sockS30.sendall(reqCommand('cmd04')) # 센서에 자료('cmd04') 요청 - 총 760 라인
    data_tmp = ''
    # 기본크기를 알수 없는 패킷정보를 읽어들인다.
    # '0a0a0d' 값이 나오면 페켄의 끝임.
    while True:
        data_tmp += sockS30.recv(1024)
        if all(data_tmp[-3:]) == '0a0a0d':
            # print 'last socket'
            break
    if data_tmp:
        result_cmd04, result_cmd04_2 = cmd04(data_tmp) # SVG Value 와 요소 갯수를 Return 한다.
        print "No. of detection area: ", result_cmd04_2
        # print result_cmd04
        # print data_tmp # 바이너리 파일임
    else:
        print "error get detection area"

    #####################################
        
    # zone information
    sockS30.sendall(reqCommand('cmd05'))
    data_tmp = sockS30.recv(1024)
    result_cmd05 = cmd05(data_tmp).split(' ')
    print "Radius of area A/B: Type A:%s, B:%s, Type:%s, #:%s, H/V:%s, V:%s"%(result_cmd05[0],result_cmd05[1],result_cmd05[2],result_cmd05[3],result_cmd05[4],result_cmd05[5])

    # basic parameter
    sockS30.sendall(reqCommand('cmd07'))
    data_tmp = sockS30.recv(1024)
    result_cmd07 = cmd07(data_tmp)
    print "Angle, No. of lines, Center of lines: ", result_cmd07

    # destination of Redwall
    sockS30.sendall(reqCommand('cmd08'))
    data_tmp = sockS30.recv(1024)
    result_cmd08 = cmd08(data_tmp)
    print "Communication by (TCP)(UDP): ", result_cmd08

    # relay output
    sockS30.sendall(reqCommand('cmd09'))
    data_tmp = sockS30.recv(1024)
    result_cmd09 = cmd09(data_tmp)
    print "Relay output: ", result_cmd09

    # masking/allocating file
    sockS30.sendall(reqCommand('cmd10'))
    data_tmp = sockS30.recv(1024)
    result_cmd10 = cmd10(data_tmp)
    print "Masking/Allocating file: ", result_cmd10

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
            print "Allocate zone: Enabled", result_cmd11_A
        else:
            result_cmd11_M = result_cmd11[1]
            print "Mask zone: Enabled", result_cmd11_M
    else:
        print "No masking/allocating area"

    # model name
    sockS30.sendall(reqCommand('cmd12'))
    data_tmp = sockS30.recv(1024)
    result_cmd12 = cmd12(data_tmp)
    if '2020' in result_cmd12: 
        type_RLS = "2020" # 센서타입 2020 또는 3060
    else:
        type_RLS = "3060" # 센서타입 2020 또는 3060
    print "Model name: ", result_cmd12 # , all(data_tmp)
    print "Running RLS Realtime Monitoring - http://%s:%s" % (config["db"]["system_ip"], config["interface"]["portOut"])

    #################################################
    # 템플릿 HTML 파일을 읽고 관련 정보로 치환하여
    # nodeJs의 common 소스로 저장한다.
    path = "/home/pi/optex_VEHICLE" 
    source = "%s/realtime_RLS_templet.html" % path # Optex Theme
    target = "%s/realtime_RLS_%s.html" % (path, config["interface"]["portIn"]) # Optex Theme

    html_style = '''
<style>
.html_scan { stroke-width: 10px; stroke: beige; fill: darkseagreen; opacity: 0.6; }
.html_grid { stroke:red; stroke-width:10px; }
.html_zone { fill:#faebd738; stroke:gray; stroke-width:8px; }
.html_frame { fill:#00000040; }
.html_over { fill:#bb9ab780; stroke:black; stroke-width:10px; }
</style>
'''
    ## 바탕화면 크기 설정
    width = 50000
    height = 50000
    min_x = -(width/4) # 시작점 X
    min_y = -(height/4) # 시작점 Y
    # min_x = 0 # 시작점 X
    # min_y = 0 # 시작점 Y
    ## SVG viewBox = "<min-x>, <min-y>, <width>, <height>"
    html_viewBox = "%s %s %s %s" % (min_x, min_y, width, height)
    html_grid = '' # 박스 프레임에 눈금자를 그린다.
    gridStep = 1000 # 미리미터 

    if '2020' in result_cmd12: ## 2020
        start_x = -2700
        start_y = -2700
        size_x = 32700
        size_y = 32700
        for i in range((start_x//gridStep), (size_x//gridStep)-1):
            html_grid += "<path class='html_grid' id='grid_v_%s' d='M %s -3000 v 33000'></path>" % (i,(i*gridStep))
        for i in range((start_y//gridStep), (size_y//gridStep)-1):
            html_grid += "<path class='html_grid' id='grid_h_%s' d='M -3000 %s h 33000'></path>" % (i,(i*gridStep))
        html_frame = "<path class='html_frame' d='M 0,0 v 30000 a -30000,-30000 0 0,0 30000,-30000 Z'></path>"
        html_over = "<path class='html_over' d='M 0 30000 L -2700 30000 L 0 0 L 30000 -2700 L 30000 0 L 0 0 Z'></path>"
        html_zone = "" # "<rect class='html_zone' x='0' y='0' width='20000' height='20000'></rect>"

    else: ## 3060
        start_x = -30000
        start_y = -2700
        size_x = 60000
        size_y =  32700
        for i in range((start_x//gridStep), (size_x//gridStep)-1):
            html_grid += "<path class='html_grid' id='grid_v_%s' d='M %s -3000 v 33000'></path>" % (i,((i*gridStep)-30000))
        for i in range((start_y//gridStep), (size_y//gridStep)-1):
            html_grid += "<path class='html_grid' id='grid_h_%s' d='M -30000 %s h 60000'></path>" % (i,(i*gridStep))
        # d="M 200,200 L 400,200 A 100,100 0 0,1 200,200 Z"
        html_frame = "<path class='html_frame' d='M -30000 0 C -30000 40000, 30000 40000, 30000 0 Z'></path>"
        html_over = "<path class='html_over' d='M -30000 0 L -30000 -2700 L 0 0 L 30000 -2700 L 30000 0 L 0 0 Z'></path>"
        html_zone = "" #"<rect class='html_zone' x='-15000' y='0' width='30000' height='30000'></rect>"
        # html_zone += "<rect class='html_zone' x='-30000' y='0' width='30000' height='30000'></rect>"
        # html_zone += "<rect class='html_zone' x='0' y='0' width='30000' height='30000'></rect>"

    try:
        with open(config["path"]["img"]+'/ims/'+config["file"]["rls_map"]) as content_file:
            html_background = '<image'+content_file.read().split('<image')[1].replace('</svg>', '')
            # re.sub('<?xml.*<image', '<image', html_background)
            # html_background = re.sub(re.compile('svg.*<image'),"<image",content_file.read())
            # html_background = re.sub('.*<image', '<image', content_file.read())
            print html_background
    except EnvironmentError:
        print('Open error %s' % config["file"]["rls_map"])
        html_background = ''
        
    tag_model = "__model_and_rev__"
    tag_version = "__version__"
    tag_viewBox = "__svg_viewBox__" # svg id="svg_id" viewBox
    tag_zone = "__boundary_of_zone__"
    tag_area = "__boundary_of_area__"
    tag_mask = "__boundary_of_mask__"
    tag_allocate = "__boundary_of_allocate__"
    tag_background = "__boundary_of_background__"
    tag_grid = "__boundary_of_grid__"
    tag_frame = "__boundary_of_frame__"
    tag_over = "__boundary_of_over__"
    tag_style = "__svg_style__"

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

    # 템플릿 파일에 확인된 정보 적용
    replacements = {tag_model:result_cmd12, tag_version:result_cmd02, tag_zone:html_zone, tag_area:result_cmd04, tag_mask:result_cmd11_M, tag_allocate:result_cmd11_A, tag_grid:html_grid, tag_frame:html_frame, tag_background:html_background, tag_over:html_over, tag_viewBox:html_viewBox, tag_style:html_style, inc_jq:__script_jquery_js__, inc_jq_ui:__script_jquery_ui_js__, inc_jq_ui_css:__style_jquery_ui_css__, inc_svg_pan_zoom:__svg_pan_zoom__}
    with open(source) as infile, open(target, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)

    # run_demon_realtime_VEHICLE(config["interface"]["portIn"])

    # # 관제 SVG 틀로 사용하기 위한 기본 프레임을 템플릿으로 생성 
    # f = open("/var/www/html/its_web/ecos.html", 'w')
    # f.write("<html><head>")
    # f.write("<?xml version='1.0' encoding='utf-8'?>")
    # f.write(html_style)

    # f.write(__script_jquery_js__)
    # f.write(__script_jquery_ui_js__)
    # f.write(__style_jquery_ui_css__)
    # f.write(__svg_pan_zoom__)

    # f.write("</head><body>")
    # f.write("<svg viewBox='%s'>"%html_viewBox)

    # f.write("<g transform='scale(1) translate(0 0) rotate(0 0 0)'>")
    # f.write(html_zone)
    # f.write(html_frame)
    # f.write(html_over)
    # f.write(html_grid)
    # f.write(result_cmd04) ## Auto Scanned Boundary
    # f.write("</g>")

    # f.write("</svg>")
    # f.write("</body></html>")
    # f.close()	

    # 데이터베이스 테이블 생성
    tableName = config["db"]["sensor_Addr"].replace(".", "_")
    returnMsg = create_table_RLS_RAW(tableName) # postfix='' + IP address
    # print returnMsg # 0 - Success

    sockS30.sendall(reqCommand('cmd06')) # 센서에 자료('cmd06') 요청
    try:
        # Send data
        print "ready to receiving.."
        while True:
            try:
                data_tmp = sockS30.recv(1024)
                result_cmd06 = cmd06(data_tmp) # 센서로 부터 받은 자료
                for singleEvent in result_cmd06:
                    eventArea, eventID = filterSizeArea(singleEvent)
                    # print(eventArea, eventID)
                    if(eventArea): # 이밴트 크기 비교 Valid or Not
                        singleEvent = ','.join([str(i) for i in singleEvent])
                        realtime_monitoring(config["db"]["system_ip"],config["interface"]["portIn"],singleEvent)
            except:
                # 알수 없는 오류
                continue
    finally:
        print 'closing socket_S30'
        sockS30.close()

if __name__ == '__main__':
    if len(sys.argv) > 1: 
        config = readConfig('/home/pi/optex_VEHICLE/config_'+str(sys.argv[1])+'.json')
    else:
        exit("No Config Information, Check Sensor's Config...")


    # ############ logging ################
    # # 로그 파일 초기화 참고:  http://gyus.me/?p=418

    # if not os.path.exists(config["path"]["log"]): # config["path"]["log"] 폴더 생성
    # 	os.makedirs(config["path"]["log"])
    # logger = logging.getLogger(config["db"]["sensor_serial"]) # 로거 인스턴스를 만든다
    # fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
    # loggerLevel = logging.DEBUG
    # filename = config["path"]["log"]+config["db"]["sensor_serial"]+'.log'
    # fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
    # fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
    # streamHandler = logging.StreamHandler()
    # fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
    # streamHandler.setFormatter(fomatter)
    # logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
    # # logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
    # # 로거 인스턴스 로그 예
    # logger.setLevel(loggerLevel)
    # # logger.info("TEST START")
    # # logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
    # # logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
    # # logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
    # # logger.info("TEST END!")
    # ############ logging ################

    # ############ Images ################
    # # 이미지 파일 초기화 
    # if not os.path.exists(ITS_img_data): # ITS_img_data 폴더 생성
    # 	os.makedirs(ITS_img_data)
    # # 센서 이벤트 스크린샷 이미지 저장 폴더명
    # img_data_sub = ITS_img_data + config["db"]["sensor_serial"] + "/"
    # if not os.path.exists(img_data_sub): # ITS_img_data 내의 서브 사진 폴더 생성
    # 	os.makedirs(img_data_sub)
    # ############ Images ################

    # varPort = int(db_sensor_Addr.split('.')[2]) + int(db_sensor_Addr.split('.')[3])
    # nodeIn = 50001 + varPort # db_sensor_Addr = '192.168.168.30' -> 50199
    # nodeOut = 51001 + varPort # db_sensor_Addr = '192.168.168.30' -> 51199
    # print('\nRunning RLS Realtime Monitoring - http://%s:%s' %(db_system_ip,nodeOut))
    # logger.info('\nRunning RLS Realtime Monitoring - http://%s:%s' %(db_system_ip,nodeOut))

    print "\n"
    print "Sensor Addr:", config["db"]["sensor_Addr"]
    print "Sensor Port:", config["sensor"]["sensorPort"]
    print "Rcv. Port:", config["interface"]["portIn"]
    print "UI Port:", config["interface"]["portOut"]
    print "SensorID:",config["db"]["sensor_serial"]
    print "Accept Size:",config["db"]["sensor_ignoreS"], config["db"]["sensor_ignoreE"]
    print "Allow Area:",config["db"]["sensor_allowZone"]
    print "Refuse Area:",config["db"]["sensor_ignoreZone"]

    run_demon_realtime_VEHICLE(config["interface"]["portIn"])

    try:
        main()
    except KeyboardInterrupt:
        kill_demon_realtime_RLS()
        print ("\nCancelled")
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(1)