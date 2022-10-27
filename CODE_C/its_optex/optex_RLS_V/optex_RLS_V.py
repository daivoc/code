#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import subprocess 
import pymysql
import requests
import socket 
import shutil
import logging
import logging.handlers
import struct
import binascii
import os, traceback
import fcntl
import re
import math
import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO
import json

from multiprocessing import Process
from requests.auth import HTTPDigestAuth
from PIL import Image, ImageDraw, ImageFont
from warnings import filterwarnings
filterwarnings('ignore', category = pymysql.Warning)

### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
reload(sys)
sys.setdefaultencoding('utf-8')

############# Audio
def audioOut(file, volume=500): # 
	# os.system('omxplayer %s &'%file) ## os.system('omxplayer http://192.168.0.5/tmp/dog-howling-yapping-daniel_simon.mp3 &')
	# cmd = "omxplayer %s >/dev/null & " % file
	# p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
	cmd = "omxplayer --vol %s %s >/dev/null & " % (volume,file)
	# cmd = "omxplayer --vol %s %s " % (volume,file)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
############# Audio

def alertOut(port, druation): # GPIO Port No. , Action Due
	insert_socket_GPWIO(id=port, status=0, msg='')
	time.sleep(druation)
	insert_socket_GPWIO(id=port, status=1, msg='')
		
def alertOutACU(ip, port, id, dueTime, enc): # GPIO Port No. , Action Due
	# print ip, port, id, dueTime, enc
	insert_ACU_GPWIO(ip=ip, port=port, id=id, status=1, msg='', enc=enc)
	time.sleep(dueTime)
	insert_ACU_GPWIO(ip=ip, port=port, id=id, status=0, msg='', enc=enc)
	# print "Done: %s"%dueTime

# 센서 아이피 확인 
def check_sensor(sensorIP):
    return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error
	
## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_realtime_RLS_V(arg): 
	# path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	# cmd = "cd /var/www/html/its_web/%s; node realtime_RLS.js %s 2>&1 & " % (path, arg)
	cmd = "node %s/realtime_RLS.js %s 2>&1 & " % (ITS_rls_v_path, arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def MASQUERADE(active,ip,port):
	if active:
		# 연결 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(port,ip)
	else:
		# 차단 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		sudo iptables -D FORWARD -i eth0 -j ACCEPT
		sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE
		sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(port,ip)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return (active,ip,port)

# 원격 카메라 이미지 다운로드
# ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/wits_%s.jpg  -q -o /dev/null
def run_wget_image(source, target): 
	cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (source, target)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
def download_image(host, file, enc): 
	if(enc):
		a = host.rsplit('@',1)[0] # 맨 마지막 @를 기준으로 첫번째 요쇼
		b = a.split('://',1)[1] # 맨 처음 :// 를 기준으로 두번째요소 선택
		c = b.split(':',1) # admin:optex59:://@@71!!
		user = c[0]
		pwd = c[1]
		r = requests.get(host, auth=HTTPDigestAuth(user, pwd), stream=True)
	else:
		r = requests.get(host, stream=True)
		
	if r.status_code == 200:
		with open(file, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
	return r.status_code # , host
	
def get_img_n_wmark(host, file, text, enc): 
	# 이미지 다운로드 후 워터마크 등록
	if(enc):
		a = host.rsplit('@',1)[0] # 맨 마지막 @를 기준으로 첫번째 요쇼
		b = a.split('://',1)[1] # 맨 처음 :// 를 기준으로 두번째요소 선택
		c = b.split(':',1) # admin:optex59:://@@71!!
		user = c[0]
		pwd = c[1]
		r = requests.get(host, auth=HTTPDigestAuth(user, pwd), stream=True)
	else:
		r = requests.get(host, stream=True)
	
	if r.status_code == 200:
		with open(file, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
		
		# 워터마크 등록
		# 이미지 생성 일시는 카메라자체 시간이 나오도록 
		try: 
			image = Image.open(open(file, 'rb'))
			draw = ImageDraw.Draw(image)
			font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",30)
			draw.text((900, 1000), text, font=font) # X, Y 해상도에 위치함
			image.save(file,optimize=True,quality=100)
		except:
			return r.status_code, "Warning: Watermark"
	return r.status_code, "Snapshot OK"
		
# 프로그램 오류 발생시 부모프로그램 다시 실행 한다.
def restart_its(): 
	cmd = "python /home/pi/optex_RLS_V/run_optex.pyc"
	print(cmd)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 프로그램 오류 발생시 시스템 다시 시작 한다.
def reboot_its():
	print ("reboot")
	os.system('sudo reboot')
	return

# 오래된 파일 삭제
def run_remove_old_file(path, day):
	if (path and day):
		cmd = "find %s -type f -ctime %s -exec rm -rf {} \;" % (path, day) # day 이후 모두 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		cmd = "find %s -type d -empty -delete" % (path)	 # 비어있는 폴더 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

#############################################################
#############################################################
	
def isTableExist(tableName): ###################### Optex REDSCAN
	query = "SELECT * FROM information_schema.tables WHERE table_schema = '"+db_name+"' AND table_name = '"+tableName+"' LIMIT 1;"
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		if result: # 테이블이 존재 하면
			return 0
		else: # 테이블이 존재 하지 않으면
			return 1
	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def create_table_w_log_RLS_V(postfix=''): # create_table_w_log(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		if(postfix):
			tableName = ITS_sensor_log_table + '_' + postfix
			if isTableExist(tableName):
				tbl_w_log_sensor_sql = """
					CREATE TABLE IF NOT EXISTS %s (
					`w_id` int(11) NOT NULL AUTO_INCREMENT,
					`w_evt_id` int(11) NOT NULL DEFAULT '0',
					`w_evt_X` float NOT NULL DEFAULT '0',
					`w_evt_Y` float NOT NULL DEFAULT '0',
					`w_evt_S` float NOT NULL DEFAULT '0',
					`w_evt_zone` varchar(16) NULL DEFAULT '',
					`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					PRIMARY KEY (`w_id`)
					) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
					""" % tableName
				cursor.execute(tbl_w_log_sensor_sql) # create table
				conn.commit()
				return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
 	except pymysql.Warning as warning:
		pass
	finally:
		cursor.close()
		conn.close()
		
def insert_event_RLS_V(tableName, w_evt_id=0, w_evt_X=0, w_evt_Y=0, w_evt_S=0, w_evt_zone=''): 
	query = "INSERT INTO "+ITS_sensor_log_table+"_"+tableName+"(w_evt_id, w_evt_X, w_evt_Y, w_evt_S, w_evt_zone) VALUES(%s, %s, %s, %s, %s)"
	args = (w_evt_id, w_evt_X, w_evt_Y, w_evt_S, w_evt_zone)
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

## 레코드 갯수가 limit 값을 넘으면 로래된 레코드를 삭제 한다.
def delete_over_limit_log(tblIs, limit):
	query = "DELETE FROM `"+tblIs+"` WHERE `w_id` < (SELECT MIN(m.`w_id`) FROM (SELECT `w_id` FROM `"+tblIs+"` ORDER BY `w_id` DESC LIMIT "+limit+") m)"
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def insert_socket_status_UNION(serial, name, ip, port, model, board, tableID, status, msg): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((ip,port))
		msg_data = ('id=%s,name=%s,ip=%s,model=%s,board=%s,tableID=%s,status=%s,msg=%s' % (serial, name, ip, model, board, tableID, status, msg))
		node.send(msg_data) 
		node.close() 
		return ("status_msg")
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
def insert_socket_GPWIO(id, status, msg): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		# node.connect((ip,port))
		node.connect(('localhost', 8040))
		msg_data = ('id=%s,status=%s,msg=%s' % (id, status, msg))
		return node.send(msg_data) 
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
def insert_ACU_GPWIO(ip, port, id, status, msg, enc): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((ip,int(port)))
		# node.connect(('localhost', 8040))
		msg_data = ('id=%s,status=%s,msg=%s,enc=%s' % (id, status, msg, enc))
		return node.send(msg_data) 
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 

## 호스트로 이밴트 상태 전송
def send_event_to_host(host, port, subject, serial, status, shot='', zone=''): 
	# 모니터링을 위한 beep 선언
	if status == 0 or status == 2 : # Active_Event, Error_Event
		beep = 0
	else:
		beep = 1
		
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data = ('id=%s,name=%s,beep=%s,status=%s,shot=%s,subzone=%s' % (serial, subject, beep, status, shot, zone))
		s.send(msg_data) 
		s.close() 
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 

## PRESET Http Request 
## 아이디와 비밀번호 추출후 암호화 옵션에 따라 HTTPDigestAuth 적용
## 프리셋 전송 
## request -> https://dgkim5360.tistory.com/entry/python-requests
def send_camera_PRESET(host, enc, id):
	url = "%s%s" % (host,id)
	try:
		if(enc):
			a = host.rsplit('@',1)[0] ## http://root:pass <- http://root:pass@host/command?option=id
			b = a.split('://',1)[1] ## root:pass <- http://root:pass
			c = b.split(':',1) ## id_pass[0] = root, id_pass[1] = pass <- root:pass
			user = c[0]
			pwd = c[1]
			req = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=0.1)
		else:
			req = requests.get(url, timeout=0.1)
		return "%s %s" % (req.status_code, id) # req.text
	except:
		# return "requests.get Error: %s" % url
		return 0
		
# def send_PARSER_REQUEST(content):
def send_PARSER_REQUEST(user, pwd, url, enc):
	## content = 'root||password||http://host/command?option=id||1'
	try:
		user = user
		pwd = pwd
		url = url
		enc = int(enc)
		if(enc):
			req = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=0.1)
		else:
			req = requests.get(url, timeout=0.1)
		return req.status_code # req.text
	except:
		# return "requests.get Error: %s" % url
		return 0	

def apiJson(content):
	elements = content.split('||') 
	host = elements[0]
	port = int(elements[1])
	opt1 = elements[2]
	if host and port and opt1:
		pass
	else:
		return 0

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		s.send(opt1) 
		s.close() 
		return("Sent IP:%s"% host)
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 

def read_table_w_cfg_sensor_all(wr_id=''): # Optex Microwave
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_RLS_V + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "

	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_field_w_cfg_status(wr_id=''): 
	query = "SELECT w_sensor_stop, w_sensor_reload, w_sensor_disable, w_alarm_disable FROM " + ECOS_table_prefix + ECOS_table_RLS_V + " WHERE wr_id = " + wr_id
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def set_reload_w_cfg_reload(wr_id=''): 
	query = "UPDATE " + ECOS_table_prefix + ECOS_table_RLS_V + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def check_scheduledDate(wr_id=''): # Optex Microwave
	scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	query = "SELECT COUNT(*) as cnt FROM " + ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + ECOS_table_RLS_V + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		return result

	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def check_scheduledWeek(wr_id='', weekNo=''): # Optex Microwave
	# 편의상 2017년 1월 1일 첫째 주 일요일 부터 토요일 까지를 주간 예약 시간표로 사용한다.
	# 예약된 날짜와 요일에 마추어서 현재 시간을 결합해서 검색을 한다.
	# date.weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6. 
	# print ECOS_week_map[weekNo], "ECOS_week_map[weekNo]"
	# scheduledWeek = time.strftime("%Y-%m-%dT%H:%M:%S")
	scheduledWeek = ECOS_week_map[weekNo]+time.strftime("T%H:%M:%S") # 2017-01-01 + 현재시간
	query = "SELECT COUNT(*) as cnt FROM " + ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + ECOS_table_RLS_V + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
	# print query
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		return result

	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
## Module END ##



# def all(packet):
# 	return binascii.hexlify(packet).decode()

# def hex2int(dataObj): # 정수를 부호있는 숫자로 변환
# 	x = int(binascii.hexlify(dataObj).decode(), 16)
# 	if x > 0x7FFFFFFF:
# 		x -= 0x100000000
# 	return x
	
# def errorCheck(packet):
# 	try:
# 		code = packet.split('\n')[3][2:4]
# 	except:
# 		return 'Error when Split Packet'
		
# 	if code == '00':
# 		msg = ''
# 	elif code == '10':
# 		msg = '[%s] Requested command is not supported.' % code
# 	elif code == '11':
# 		msg = '[%s] Format Error.' % code
# 	elif code == '12':
# 		msg = '[%s] Requested command is ignored because it is doubled.' % code
# 	else:
# 		msg = '[%s] Unknow Error' % code
# 	return msg	

# def getValue(packet):
# 	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
# 	return dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.

# def cmd00(packet): # Sensor information.
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	# ['OPTEX', 'RLS-3060', 'SH', '0100', '\x00\x1f\xd1\x16\x06\xd3', '', '']
# 	# print(packet.splitlines()[0]) # 'OPTEX'
# 	# print(packet.splitlines()[1]) # 'RLS-3060'
# 	# print(packet.splitlines()[2]) # 'SH'
# 	# print(packet.splitlines()[3]) # '0100'
# 	# print(packet.split('\n\n\r')[0])
# 	return '%s %s %s' % (packet.splitlines()[0], packet.splitlines()[1], packet.splitlines()[2]) # INFO

# def cmd01(packet): # 맥 어드레스
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode
# 	return all(getValue(packet))
	
# def cmd02(packet): # 버전 정보
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode
# 	return getValue(packet)
	
# def cmd04(packet): #  Area Set 정보
# 	# http://www.mathbang.net/159 삼각법 참고
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	dataObj = getValue(packet)
# 	cntObj = len(dataObj)/4 # 4 바이트씩 그룹핑 - 기본 Object Info Size (760개)
	
# 	count = 0
# 	maxX = 0
# 	maxY = 0
# 	minX = 0
# 	minY = 0
# 	objInfo = ''
# 	unitAngle = 0.25 # float(190/760)
# 	while (count < cntObj):
# 		orgX = 0 # 30000 # 출력화면의 X축 0점이 30000에서 시작한다.
# 		fLN = count * 4
# 		tLN = fLN + 4
# 		# print all(dataObj[fLN:tLN])
# 		length = hex2int(dataObj[fLN:tLN])
# 		angle = math.radians(unitAngle * (count - 20)) # 시작이 -20번째부터 진행 한다(총 185도)
# 		distX = int(length * math.cos(angle))
# 		distY = int(length * math.sin(angle))
		
# 		if (maxX < distX): maxX = distX
# 		if (maxY < distY): maxY = distY
# 		if (minX > distX): minX = distX
# 		if (minY > distY): minY = distY

# 		# print 'No:%3s, Ag:%6s, X:%5s, Y:%5s' % (count, unitAngle * (count - 20), distX, distY)
		
# 		objInfo += "L %s %s " % (distX + orgX, distY)
# 		count = count + 1
		
# 	objInfo = "<path class='html_scan' d='M%s 0 %s Z' />" % (orgX, objInfo)
			
# 	return objInfo, cntObj, maxX, maxY, minX, minY
	
# def cmd05(packet): # 존(zone Type) 정보
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	dataObj = getValue(packet)
# 	# objInfo = '%s %s %s %s %s %s' % (hex2int(dataObj[0:4]), hex2int(dataObj[4:8]), dataObj[8:14], dataObj[14:17], dataObj[17:18], hex2int(dataObj[18:22]))
# 	# return (objInfo)
# 	return (hex2int(dataObj[0:4]), hex2int(dataObj[4:8]), dataObj[8:14], dataObj[14:17], dataObj[17:18], hex2int(dataObj[18:22]))
	
# def cmd06(packet): # 이벤트 발생정보 
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return 0 ## 데이터 오류

# 	dataObj = getValue(packet)
# 	cntObj = len(dataObj)/20 # 20 바이트씩 그룹핑 - 기본 Object Info Size
# 	count = 0
# 	objInfo = ''
# 	while (count < cntObj):
# 		fFX = count * 20
# 		fFY = fFX + 4
# 		fOX = fFY + 4
# 		fOY = fOX + 4
# 		fSZ = fOY + 4
		
# 		tFX = fFX + 4
# 		tFY = fFY + 4
# 		tOX = fOX + 4
# 		tOY = fOY + 4
# 		tSZ = fSZ + 4
		
# 		objID = '%s%s' % (hex2int(dataObj[fFX:tFX]),hex2int(dataObj[fFY:tFY])) # First X,Y coordinate
# 		objX = hex2int(dataObj[fOX:tOX]) # X-coordinate of detected object.
# 		objY = hex2int(dataObj[fOY:tOY]) # Y-coordinate of detected object.
# 		objD = hex2int(dataObj[fSZ:tSZ]) # Size of the detected object

# 		# objInfo += '%s,' % str(12000-(hex2int(dataObj[fOX:tOX])+6000)) # 화면 표시용 X-coordinate of detected object.
# 		objInfo += '%s,%s,%s,%s|' % (re.sub('-', '',str(objID)), str(objX), str(objY), str(objD))
		
# 		count = count + 1
		
# 		# print objID, objX, objY, objD
# 	return objInfo

# def cmd07(packet): # 기본 좌표 정보
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	dataObj = getValue(packet)
# 	objInfo = '%s %s %s' % (dataObj[0:4], dataObj[4:8], dataObj[8:12])
# 	return (objInfo)
	
# def cmd08(packet): # 센서 이벤트 출력 정보
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	return getValue(packet)

# def cmd09(packet): # 릴레이 정보
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	return getValue(packet)

# def cmd10(packet): # 마스킹/얼로케이션 파일
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	return getValue(packet)

# def cmd11(packet): # 마스킹/얼로케이션 영역
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	if respCode:
# 		return respCode
# 	dataObj = getValue(packet)
# 	zone_type = int(dataObj[0:1]) # 0 means current setting is masking. 1 means current setting is allocating.
# 	dataObj = dataObj[2:] # 3번째 문자이후의 모든 데이터를 선별한다.
# 	cntObj = len(dataObj)
# 	count = 0
# 	objInfo = ''
# 	zone_data = ''
# 	zone_html = ''
# 	zone_color = {}
# 	zone_color[0] = '#006400'
# 	zone_color[1] = '#ed143d'
# 	zone_color[2] = '#9400d3'
# 	zone_color[3] = '#000080'
# 	zone_color[4] = '#800000'
# 	zone_color[5] = '#ffa500'
# 	zone_color[6] = '#009e9e'
# 	zone_color[7] = '#f4ff00'
# 	zone_color[14] = '#000000'
	
# 	sizeXY = 300
# 	offset = 30000
		
# 	while (count < cntObj):
# 		fFX = count * 1
# 		tFX = fFX + 1
		
# 		tmp_zone = dataObj[fFX:tFX]
# 		if ord(tmp_zone) is not 0x0F:
# 			# 순서 값에서 행과 열값을 구하기 위해 가로 총수 200으로 나누어 몫을 행으로 나머지 값을 열로 선언한다.
# 			# 행의 시작이 아래부터 시작 함으로 전체 행 및 열값에 단위길이 300(mm)를 곱한다.
# 			zX = (count % 200 * sizeXY) - offset
# 			zY = (99 - (count / 200)) * sizeXY
# 			zT = hex2int(tmp_zone) # zone type
# 			zone_data += '%d:%d:%d,' % (zX,zY,zT)
# 			zone_html += "<rect style='fill:%s20; stroke:%s; stroke-width:2px;' x='%s' y='%s' width='%s' height='%s'></rect>" % (zone_color[zT],zone_color[zT],zX,zY,sizeXY,sizeXY)
		
# 		count = count + 1
		
# 	return (zone_type, zone_html) # mask or allocating and data
	
# def cmd12(packet): # 모델명
# 	respCode = errorCheck(packet) # errorCheck(code)
# 	# respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
# 	if respCode:
# 		return respCode

# 	dataObj = getValue(packet)
# 	len_m_name = int(all(dataObj[0:1]))
# 	m_name = dataObj[1:len_m_name+1]
# 	len_s_name = int(all(dataObj[len_m_name+1:len_m_name+2]))
# 	s_name = dataObj[len_m_name+2:len_m_name+2+len_s_name]
# 	objInfo = '%s %s' % (m_name, s_name)
# 	return (objInfo) 

# def reqCommand(id):
# 	command = {}
# 	command['cmd01'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][01][LF][LF][CR]'	# Requests MAC address.
# 	command['cmd02'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][02][LF][LF][CR]'	# Requests version number.
# 	command['cmd04'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][04][00][LF][LF][CR]'	# Requests detection area information. 
# 	command['cmd05'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][05][LF][LF][CR]'	# Requests zone (area AB) information.
# 	command['cmd06'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][50][0011][LF][LF][CR]'	#  To start the report by limiting the number of detected objects to 50 and specifing 50 ms for valid report interval,
# 	command['cmd06I'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][25][0100][LF][LF][CR]'	#  To start the report by limiting the number of detected objects to 25 and specifing 5000 ms for valid report interval,
# 	command['cmd06S'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][0][00][0000][LF][LF][CR]'	# STOP Requests detected object information. 
# 	command['cmd06L'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][30][0000][LF][LF][CR]'	# To request only one report limiting the number of detected object to 30.
# 	command['cmd07'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][07][LF][LF][CR]'	# Requests basic parameter of detection area. 
# 	command['cmd08'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][08][LF][LF][CR]'	# TCP - Requests destination of Redwall Event Code (REC) and sending sample REC.
# 	# command['cmd09'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][09][02][600][LF][LF][CR]'	# In case of activating Output 02 10 minutes (600 sec.) Controls the relay output.
# 	command['cmd09'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][09][02][0][LF][LF][CR]'	# In case of activating Output 02 10 minutes (600 sec.) Controls the relay output.
# 	command['cmd10'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][10][CS][LF][LF][CR]'	# Requests/switches masking/allocating File.
# 	command['cmd11'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][11][LF][LF][CR]'	# Requests masking/allocating area information.
# 	command['cmd12'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][12][LF][LF][CR]'	# Requests model name.(Only 2020)
# 	return command[id].replace('[','').replace(']','').replace('LF','\n').replace('CR','\r')
	
# def get_ip_address(ifname): ## 자신 아이피 확인  get_ip_address('eth0')  # '192.168.0.110'
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	return socket.inet_ntoa(fcntl.ioctl(
# 		s.fileno(),
# 		0x8915,  # SIOCGIFADDR
# 		struct.pack('256s', ifname[:15])
# 	)[20:24])
	
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
	return "%s,%s,%s,%s" % (id, iX, iY, iS)
		
def filterZone4(type, X, Y, D, maxX, maxY, minX, minY, pSet):
	# ('2020', '670', '356', '58', 4103, 959, 0, -178), pSet
	X = int(X) # X값
	Y = int(Y) # Y값
	D = int(D) # 직경
	maxX = int(maxX)
	maxY = int(maxY)
	minX = int(minX)
	minY = int(minY)
	
	uX = (maxX - (minX)) / pSet[0] ## 전체 길이 X / pSet[0] = 단위 길이 X
	uY = (maxY - (minY)) / pSet[1] ## 전체 길이 Y / pSet[1] = 단위 길이 Y
	lX = X / 10 # 센지로 표시 Location X
	lY = Y / 10 # 센지로 표시 Location Y
	lD = D / 10 # 센지로 표시 Location S
	
	areaX = 0
	areaY = ''
	for i, j in enumerate(range(minX, maxX, uX)):
		if X > j: 
			areaX = i
	for i, j in enumerate(range(minY, maxY, uY)):
		if Y > j: 
			areaY = chr(ord('A') + i)
	area = '%s%d'%(areaY,areaX)	
	# print(type, X, Y, D, maxX, maxY, minX, minY, pSet)
	# print(areaY, lX, lY, lD, area, uX, uY) 
	return(areaY, lX, lY, lD, area) 
		
def filterSize(diameter): ## 이벤트 크기 제한
	result = 0 # 0:invalid, 1:valid
	for idx, val in enumerate(db_allowSize):
		# print(idx, val)
		limits = val.split(":")
		if(int(diameter) >= int(limits[0]) and int(diameter) <= int(limits[1])): # 이밴트 크기 비교
			result = 1
	return result

def filterArea(X, Y): # 이벤트의 위치에 따른 수용 또는 거부
	# ['167:2445_186:2838', '1590:2811_1607:2840']
	# allowZone과 ignoreZone 모두 설정이 되어있으면 ignoreZone은 무시한다.
	# if ((db_sensor_allowZone and db_sensor_ignoreZone) or db_sensor_allowZone): # 영역내 이벤트만 수용한다.
	if (db_sensor_allowZone): # 영역내 이벤트만 수용한다.
		checkZone = db_sensor_allowZone
		innerEvent = 1
	elif (db_sensor_ignoreZone): # 영역내 이벤트는 무시 한다.
		checkZone = db_sensor_ignoreZone
		innerEvent = 0
	else:
		# 어떤 영역도 설정되지 않았으면 모두를 유효이벤트로 처리 한다.
		# 단 이벤트 아이디는 유효아이디(0 ~ 3)이 아닌 9 로 처리 한다.
		return [ 1, 0 ]

	for idx, val in enumerate(checkZone):
		try:
			# 1_253_155|229:438_5320:4611
			# 1_300_180|4152:2525_10913:9286
			name, value = val.split("|") # 1_253_155|229:438_5320:4611
			eventID = int(name[0:1]) # 229:438_5320:4611
			valX, valY = value.split("_") # 229:438_5320:4611
			minXY = valX.split(":")
			maxXY = valY.split(":")
			minX = minXY[0]
			minY = minXY[1]
			maxX = maxXY[0]
			maxY = maxXY[1]
			# if (((int(X) < int(minX)) and (int(X) > int(maxX))) or ((int(Y) < int(minY)) and (int(Y) > int(maxY)))):
			# if ((int(X) < minX) and (int(X) > maxX)) and ((int(Y) < minY) and (int(Y) > maxY)):
			# if ((int(X) >= minX) and (int(X) <= maxX)) or ((int(Y) >= minY) and (int(Y) <= maxY)):
			# if 10000 <= number <= 30000:
			# print(idx, val, eventID)
			
			if (int(X) >= int(minX)) and (int(X) <= int(maxX)) and (int(Y) >= int(minY)) and (int(Y) <= int(maxY)):
				return [ innerEvent, eventID ]
		except:
			continue
	return [0, 0] # 아이디는 유효아이디(0 ~ 3)이 아닌 9 로 처리 한다.

def getImgPath(): 
	# print time.strftime('%Y/%m/%d')
	tmpYear = img_data_sub+time.strftime('%Y/') # 년도 방
	if not os.path.exists(tmpYear): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpYear)
		os.chmod(tmpYear, 0o777)
	tmpMonth = tmpYear+time.strftime('%m/') # 월별 방
	if not os.path.exists(tmpMonth): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpMonth)
		os.chmod(tmpMonth, 0o777)
	tmpDay = tmpMonth+time.strftime('%d/') # 일별 방
	if not os.path.exists(tmpDay): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpDay)
		os.chmod(tmpDay, 0o777)
	tmpFullPath = tmpDay+time.strftime('%H/') # 시간별 방
	if not os.path.exists(tmpFullPath): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpFullPath)
		os.chmod(tmpFullPath, 0o777)
	tmpName = time.strftime('%M_%S-URL_01') + ".jpg"
	thisImgName = tmpFullPath + tmpName
	return thisImgName

def makeHtml(type_RLS):
	
	#################################################
	# 템플릿 HTML 파일을 읽고 관련 정보로 치환하여
	# nodeJs의 common 소스로 저장한다.
	source = "%s/realtime_RLS_templet.html" % ITS_rls_v_path # Optex Theme
	# source_ims = "%s/realtime_RLS_templet_IMS.html" % ITS_rls_v_path # Optex Theme
	source_area = "%s/realtime_RLS_templet_Area.html" % ITS_rls_v_path # Optex Theme

	target = "%s/realtime_RLS_%s.html" % (ITS_rls_v_path, nodeIn) 
	# target_ims = "%s/realtime_RLS_%s_IMS.html" % (ITS_rls_v_path, nodeIn) # IMS
	## /theme/ecos-its_optex/utility/status/rlsArea.php 에서 사용함
	path = "/var/www/html/its_web/theme/ecos-its_optex/utility/nodeJs_table" 
	target_area = "%s/realtime_RLS_%s_Area.html" % (path, nodeIn) # Area
	
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
	html_user = '' # 센서가 아닌 사용자 수용 또는 거부 영역
	gridStep = 1000 # 미리미터 

	if type_RLS == "2020":
		# for i in range(-4, 50): ## 수직 0기준으로 위로 -4.5미터 아래로 50미터
			# html_grid += "<path id='grid_h_%s' d='M -4150 %s h 52700' stroke='silver' stroke-width='1px'></path>" % (i,(i*gridStep))
		# for i in range(-4, 100): ## 수평 0기준으로 가로 100미터
			# html_grid += "<path id='grid_v_%s' d='M %s -4150 v 52700' stroke='silver' stroke-width='1px'></path>" % (i,(i*gridStep))
		# html_frame = """
			# <path style='fill:#00000040;' d='M 0,0 v 50000 a -50000,-50000 0 0,0 50000,-50000 Z'></path>
			# <path style='fill:#00000000; stroke:gray; stroke-width:8px;' d='M 0 50000 L -4150 50000 L 0 0 L 50000 -4150 L 50000 0 L 0 0 Z'></path>
		# """
		# html_zone = """
			# <rect style='fill:#faebd738; stroke:gray; stroke-width:8px;' x='0' y='0' width='50000' height='50000'></rect>
		# """
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

	elif type_RLS == "3060":
		# for i in range(-4, 50): ## 수직 0기준으로 위로 -4.5미터 아래로 50미터
			# html_grid += "<path id='grid_h_%s' d='M -50000 %s h 100000' stroke='gray' stroke-width='1px'></path>" % (i,(i*gridStep))
		# for i in range(0, 100): ## 수평 0기준으로 가로 100미터
			# html_grid += "<path id='grid_v_%s' d='M %s -4150 v 52700' stroke='gray' stroke-width='1px'></path>" % (i,((i*gridStep)-50000))
		# html_frame = """
			# <path style="fill:#80808040; stroke:black; stroke-width:10px;" d="M 0 0 L -50000 -4150 L -50000 0 C -50000 66666, 50000 66666, 50000 0 L 50000 -4150 Z "></path>
		# """
		# html_zone = """
			# <rect style='fill:#abc7d74d; stroke:gray; stroke-width:8px;' x='-50000' y='0' width='50000' height='50000'></rect>
			# <rect style='fill:#00000000; stroke:gray; stroke-width:6px;' x='-50000' y='0' width='100000' height='50000'></rect>
			# <rect style='fill:#faebd738; stroke:gray; stroke-width:8px;' x='0' y='0' width='50000' height='50000'></rect>
		# """
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
		html_over = "<path class='html_over' d='M -30000 0 L -30000 -2700 L 0 0 L 30000 -2700 L 30000 0 L 0 0' Z></path>"
		html_zone = "" #"<rect class='html_zone' x='-15000' y='0' width='30000' height='30000'></rect>"
		# html_zone += "<rect class='html_zone' x='-30000' y='0' width='30000' height='30000'></rect>"
		# html_zone += "<rect class='html_zone' x='0' y='0' width='30000' height='30000'></rect>"
	
	# 사용자 마스킹 영역 취합
	for subItem in config["masking"]["allowGroup"]:
		# print subItem, config["masking"]["allowGroup"][subItem]
		html_user += '<path class="allowGroup" id="'+subItem+'" d="'+config["masking"]["allowGroup"][subItem]+'"></path>'
	for subItem in config["masking"]["denyGroup"]:
		# print subItem, config["masking"]["denyGroup"][subItem]
		html_user += '<path class="denyGroup" id="'+subItem+'" d="'+config["masking"]["denyGroup"][subItem]+'"></path>'
	# print html_user

	try: # 배경이미지 관련
		with open(ITS_img_data + 'ims/'+ITS_rls_map_file) as content_file:
			html_background = content_file.read()
	except EnvironmentError:
		print('Open error %s' % ITS_rls_map_file) #config["file"]["rls_map"])
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

	tag_user = "__boundary_of_user__"
	
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

	replacements = {
		tag_model:result_cmd12, 
		tag_version:result_cmd02, 
		tag_zone:html_zone, 
		tag_area:result_cmd04, 
		# tag_mask:result_cmd11_M, 
		# tag_allocate:result_cmd11_A, 
		tag_mask:'', 
		tag_allocate:'', 
		tag_grid:html_grid, 
		tag_frame:html_frame, 
		tag_background:html_background, 
		tag_over:html_over, 
		tag_viewBox:html_viewBox, 
		tag_user:html_user, 
		inc_jq:__script_jquery_js__, 
		inc_jq_ui:__script_jquery_ui_js__, 
		inc_jq_ui_css:__style_jquery_ui_css__, 
		inc_svg_pan_zoom:__svg_pan_zoom__
	}
	
	# 템플릿 파일에 확인된 정보 적용
	# For Area Setup and Monitoring
	with open(source) as infile, open(target, 'w') as outfile:
		for line in infile:
			for src, target in replacements.iteritems():
				line = line.replace(src, target)
			outfile.write(line)
	
	# # For IMS Popup
	# with open(source_ims) as infile, open(target_ims, 'w') as outfile:
	# 	for line in infile:
	# 		for src, target_ims in replacements.iteritems():
	# 			line = line.replace(src, target_ims)
	# 		outfile.write(line)
	
	# For Ignore Ares Filtering
	with open(source_area) as infile, open(target_area, 'w') as outfile:
		for line in infile:
			for src, target_area in replacements.iteritems():
				line = line.replace(src, target_area)
			outfile.write(line)

def MASQUERADE(active,port,ipC):
	if active:
		# 연결 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination 192.168.%s.30:80;
		'''%(port,ipC)
	else:
		# 차단 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		sudo iptables -D FORWARD -i eth0 -j ACCEPT
		sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE
		sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination 192.168.%s.30:80;
		'''%(port,ipC)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

def main ():
	sockS30.sendall(reqCommand('cmd06')) # 센서에 자료('cmd06') 요청
	try:
		# print "ready to receiving.."
		
		eleID = ''
		eleIDCnt = 0
		eleAlarm = 0
		eventShotURL = ''
		setAlertTime = 0 ##  알럿 발생시 타이머 적용
		setAlertTime2 = 0 ##  알럿 발생시 타이머 적용
		setAudioTime = 0 ##  알럿 발생시 타이머 적용
		setZoneTime = 0 ##  지역이벤트 발생시 타이머 적용
		setPostTime = 0 ## 포스팅 발생 타이머 적용
		errorTimeoutCnt = 0 ## 오류 카운터 횟수, 

		# Schedule Block
		schedule_block = 0

		#  원격알람 발생시 타이머 적용
		setAlertTimeACU = 0 #

		# 지역 얼랏 변수 초기화
		db_gpwioR = 0
		db_gpwioV = 0
		db_gpwioG = 0

		# 오디오 변수 초기화
		db_audio_name = ''
		db_audio_time = 0 ## Audio Due Time
		db_audio_volume = 0

		# 오디오 출력중임을 알려주는 플레그 삭제
		if os.path.isfile(ITS_audio_flag):
			os.remove(ITS_audio_flag)
		
		while True:
			try:
				data_tmp = sockS30.recv(1024)
				result_cmd06 = cmd06(data_tmp) # 센서로 부터 받은 자료
				errorTimeoutCnt = 0
			except socket.timeout: ## 10초, 시간은 접속자 생성(create_connection)시 설정됨
				####### 주메뉴 스테이터스 - 소켓 유니온 전송 #######
				insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=result_cmd12, board=ECOS_table_RLS_V, tableID=myTableID, status=Event_type['error'], msg=Event_desc[Event_type['error']])
				logger.critical("Error: Sensor Socket Connect Timeout.")
				if db_host_Addr and db_host_Port:
					send_event_to_host(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, 9) # 내트워크 오류
				if db_host_Addr2 and db_host_Port2:
					send_event_to_host(db_host_Addr2, db_host_Port2, db_subject, db_sensor_serial, 9) # 내트워크 오류
				insert_event_RLS_V(db_sensor_serial, 0, 0, 0, 0, "timeout") ## 오류정보 DB update
				print ("Error: Sensor Socket Connect Timeout.")
				result_cmd06 = '' ## 이전의 정상데이터 초기화()
				errorTimeoutCnt += 1
				# #######################################################
				# ### 국립 중앙 박물관 ####################################
				# if db_alert2_Port and db_alert2_Value: # 
				# 	insert_socket_GPWIO(id=db_alert2_Port, status=0, msg='NC_On') ## NC
				# #######################################################
				
				if errorTimeoutCnt > 3: ## Timeout Error 횟수
					logger.critical("Error: System Reboot.")
					insert_event_RLS_V(db_sensor_serial, 0, 0, 0, 0, "reboot") ## 오류정보 DB update
					print ("Error: System Reboot.")
					reboot_its()
				else:
					continue
			
			if result_cmd06:  # 42949672541081,422,676,355|42949672541081,259,861,54|
				data = result_cmd06.split("|")
				for singleEvent in data:
					if singleEvent: # 42949672541081,422,676,355
						eleEvt = singleEvent.split(",") # 42949672541081,422,676,355

						# 이벤트 내용 출력
						# print(type_RLS, eleEvt[1], eleEvt[2], eleEvt[3], result_cmd04_3, result_cmd04_4, result_cmd04_5, result_cmd04_6)
						eventZone = filterZone4(type_RLS, eleEvt[1], eleEvt[2], eleEvt[3], result_cmd04_3, result_cmd04_4, result_cmd04_5, result_cmd04_6, RLS_preset[db_sensor_model])
						eventZoneGrp = "%s:%s:%s:%s:%s" % (eventZone[0], eventZone[1], eventZone[2], eventZone[3], eventZone[4])
						# 시작과 끝을 초기화 한 영역
						eventRZone = filterRZone(eleEvt[0], eleEvt[1], eleEvt[2], eleEvt[3], db_sensor_lat_s, db_sensor_lng_s, db_sensor_lat_e, db_sensor_lng_e)
						# 직경 제한
						eventSize = filterSize(eleEvt[3]) # 무시 직경
						# 영역 제한
						# eventArea: 분할된 영역(1 ~ 8), eventID: 사용자 설정 용역(1 ~ 4)
						eventArea, eventID = filterArea(eleEvt[1], eleEvt[2]) # 무시 영역
						# print eleIDCnt, eleEvt[0], eleEvt[1], eleEvt[2], eleEvt[3], eventArea, eventSize, eventID

						if eventID:
							eventIdxID = eventID - 1 # 어레이 시작이 0임으로 값을 찾기위헤 -1 

						if(eventSize and eventArea): # 이밴트 크기 비교 Valid or Not
							if(eleID == eleEvt[0]):
								if(eleIDCnt%db_event_holdTime == 0): # 주기 고정
									eleAlarm = 1
								else:
									eleAlarm = 0
								eleIDCnt += 1
							else:
								eleIDCnt = 0
								eleAlarm = 0

							weekNo = datetime.datetime.today().weekday() # 현재의 주일번호 확인 Monday is 0 and Sunday is 6.
							if str(weekNo): # in GPIO_sensor_sensor_week: # GPIO_sensor_sensor_week를 어레이로 변환후 오늘의 주번호와 일치하는지 확인
								scheduleWeek = check_scheduledWeek(myTableID, weekNo) # 주간 예약인지 확인
								schedule_block = scheduleWeek['cnt']
							if not schedule_block: # 주간 예약을 우선하고 아닌경우 일간 예약 확인
								scheduleDate = check_scheduledDate(myTableID) # 일간 예약인지 확인
								schedule_block = scheduleDate['cnt']

							# 여기에서 db_opt93(Reverse))이 1이면 
							# 박물관 모드 인 경우 스케줄러가 설정되면 1번 존만 표출 된다.
							if db_opt93: # 반전
								actionTime = 1
								# print(schedule_block, eventID)
								if schedule_block and eventID > 1:
									eventArea = eventID = 0
							else:
								if schedule_block:
									actionTime = 0
								else:
									actionTime = 1
								
							eleID = eleEvt[0] # 현재값 저장

							####### 실시간 스넵삿 요청및 저장 #######
							# if eleAlarm and not schedule_block: # db_event_holdTimer값을 주기로 실행 한다.
							if eleAlarm and actionTime and eventID: # db_event_holdTimer값을 주기로 실행 한다.
								logger.info("Cnt:%s Id:%s x:%s y:%s Dia:%s Area:%s"%(eleIDCnt, eleEvt[0], eleEvt[1], eleEvt[2], eleEvt[3], eventArea))
								imageInfo = "Location:%s"%(singleEvent)
								imageURL = ""
								imageName = ""
								## 스넵삿
								if db_url1: # 스넵삿이 가능한 db_url1 값이 있으면 
									eventName = getImgPath() ## image가 저장될 경로를 가지고 온다

									imageURL = eventName[21:] # 머리부분 
									imageName = eventName[-22:]
									eventShotURL = "%s%s" % (db_system_ip,imageURL)
									
									try:
										# run_wget_image(db_url1, eventName) ## image를 가지옴 최초버전
										# download_image(db_url1, eventName, db_opt91) ## image를 가지옴 버전2
										tmp_result = get_img_n_wmark(db_url1, eventName, imageInfo, db_opt91) ## image를 가지온후 워터마크 버전3
										os.chmod(eventName, 0o777)
										# print tmp_result
										result = "%s<a href=%s target=_blank>%s</a>" % (tmp_result,imageURL,imageName)
									except:
										result = "get_img_n_wmark error %s"%db_url1
										
									logger.info(result)  # get the return value from your function.

									## 오래된 파일 삭제
									run_remove_old_file(img_data_sub, date_of_old) # 
								## 스넵삿
								
								###################################
								#######  PTZ 카메라에 프리셋 전송  #######
								###################################
								if db_request1 and req1_url: # 카메라 연동 프리셋 전송
									result = send_PARSER_REQUEST(req1_user, req1_pwd, req1_url, req1_enc)
									if result:
										logger.info("sent Get/Post to %s %s"%(req1_url, result))
									else:
										logger.warning("Error, Check URL %s"%(req1_url))
								if db_request2 and req2_url: # 카메라 연동 프리셋 전송
									result = send_PARSER_REQUEST(req2_user, req2_pwd, req2_url, req2_enc)
									if result:
										logger.info("sent Get/Post to %s %s"%(req2_url, result))
									else:
										logger.warning("Error, Check URL %s"%(req2_url))


								####### API 사용자 연동 기능 #######
								if setPostTime: # 경보 주기
									pass
								else:
									if db_custom1: # 연동정보
										# ip||port||value
										result = apiJson(db_custom1)
										if result:
											logger.info("apiJson to %s %s"%(db_custom1, result))
										else:
											logger.warning("Error, Function apiJson: %s"%(db_custom1))
									if db_custom2: # 연동정보
										result = apiJson(db_custom2)
										if result:
											logger.info("apiJson to %s %s"%(db_custom2, result))
										else:
											logger.warning("Error, Function apiJson: %s"%(db_custom2))

															
								####### 실시간 원격(ACU) 알람신호 전송 #######
								if eventID and db_itsACU:
									# print setAlertTimeACU, itsACU_IP, itsACU_Port, itsACU_ID, itsACU_Zone, itsACU_Time, itsACU_Enc
									if itsACU_IP and itsACU_Port and itsACU_ID and itsACU_Time: # 출력지속시간:초( itsACU_Time:)
										if setAlertTimeACU:
											## 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
											pass
										else:
											# if eventID == itsACU_Zone: 값에 따라 릴레이 ID를 설정가능 하다.
											logger.info("Remote ACU Alert IP:%s, Port:%s, ID:%s, Zone:%s, Time:%s"%(itsACU_IP, itsACU_Port, itsACU_ID, itsACU_Zone, itsACU_Time))
											setAlertTimeACU = datetime.datetime.now()
											Process(target=alertOutACU, args=(itsACU_IP, itsACU_Port, itsACU_ID, itsACU_Time, itsACU_Enc)).start()
											# Process(target=alertOutACU, args=(itsACU_IP, itsACU_Port, 25, itsACU_Time, itsACU_Enc)).start()
								####### 실시간 알람 접점신호 발생 #######
													
								####### 호스트서버에 자료 전송 #######
								if setPostTime: # 경보 주기
									pass
								else:
									if db_host_Addr and db_host_Port:
										send_event_to_host(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, 1, eventShotURL, eventZone[4]) # 관제에 이벤트 전송
										logger.info("Host_01 %s %s %s %s %s(%s)"%(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, eventZone[4], eventID))
									if db_host_Addr2 and db_host_Port2:
										send_event_to_host(db_host_Addr2, db_host_Port2, db_subject, db_sensor_serial, 1, eventShotURL, eventZone[4]) # 관제에 이벤트 전송
										logger.info("Host_02 %s %s %s %s %s(%S)"%(db_host_Addr2, db_host_Port2, db_subject, db_sensor_serial, eventZone[4], eventID))
								####### 호스트서버에 자료 전송 #######
								
							else:
								eventShotURL = ''
							
							if setPostTime: # 경보 주기
								pass
							else:
								####### 데이터베이스 등록 #######
								insert_event_RLS_V(db_sensor_serial, eleEvt[0], eleEvt[1], eleEvt[2], eleEvt[3], eventZoneGrp)
								
								####### 데이터베이스 초과 레코드 삭제 (테이블명, 최대레코드수) #######
								delete_over_limit_log(ITS_sensor_log_table+"_"+db_sensor_serial, ITS_sensor_max_log)
								
								####### SVG 실시간 표현을 위한 이벤트 전송 #######
								if(eventRZone):
									realtime_monitoring(db_system_ip,nodeIn,eventRZone)

								####### 주메뉴 스테이터스 - 소켓 유니온 전송 #######
								insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=result_cmd12, board=ECOS_table_RLS_V, tableID=myTableID, status=Event_type['active'], msg=Event_desc[Event_type['active']])

							if setPostTime: # 경보 주기
								pass
							else:
								setPostTime = datetime.datetime.now()
								if schedule_block: logger.info("Schedule Blocked @%s"%setPostTime)
						else:
							## 이벤트 데이터는 존재하지만 조건(크기, 영역)을 만족하지 못한 이벤트
							pass
								
			elif result_cmd06 == 0: ## 데이터 북 참조
				continue
				
			else: # 휴식 상태
				# #######################################################
				# ### 국립 중앙 박물관 ####################################
				# if db_alert2_Port and db_alert2_Value: # 
				# 	insert_socket_GPWIO(id=db_alert2_Port, status=1, msg='NC_Off')
				# #######################################################
									
				if db_host_Addr and db_host_Port:
					send_event_to_host(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, 2) # 하트비트
				if db_host_Addr2 and db_host_Port2:
					send_event_to_host(db_host_Addr2, db_host_Port2, db_subject, db_sensor_serial, 2) # 하트비트
				
				if check_sensor(db_sensor_Addr):
					####### 주메뉴 스테이터스 - 소켓 유니온 전송 #######
					insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=result_cmd12, board=ECOS_table_RLS_V, tableID=myTableID, status=Event_type['error'], msg=Event_desc[Event_type['error']])
					logger.critical("Error: Sensor communication, Check sensor or IP.")
					insert_event_RLS_V(db_sensor_serial, 0, 0, 0, 0, "disconnected") ## 오류정보 DB update
					if db_host_Addr and db_host_Port:
						send_event_to_host(db_host_Addr, db_host_Port, db_subject, db_sensor_serial, 9) # 내트워크 오류
					if db_host_Addr2 and db_host_Port2:
						send_event_to_host(db_host_Addr2, db_host_Port2, db_subject, db_sensor_serial, 9) # 내트워크 오류
				else:
					####### 주메뉴 스테이터스 - 소켓 유니온 전송 #######
					insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=result_cmd12, board=ECOS_table_RLS_V, tableID=myTableID, status=Event_type['idle'], msg=Event_desc[Event_type['idle']])
				
				for row in read_field_w_cfg_status(myTableID):
					db_sensor_stop = row["w_sensor_stop"]		# `w_sensor_stop` TINYINT(1) - 일시정지
					db_sensor_reload = row["w_sensor_reload"] 	# `w_sensor_reload` TINYINT(1) - 재시동
					db_sensor_disable = row["w_sensor_disable"]	# `w_sensor_disable` TINYINT(1) -알람중지
					db_alarm_disable = row["w_alarm_disable"]	# `w_sensor_disable` TINYINT(1) -알람중지
				
				if db_sensor_reload: # 재시동
					set_reload_w_cfg_reload(myTableID) # 재시동 필드를 회복시킨다.
					restart_its()

			# print itsACU_Time, setAlertTimeACU
			if db_itsACU:
				if itsACU_Time and setAlertTimeACU:
					if (datetime.datetime.now() - setAlertTimeACU).total_seconds() > itsACU_Time:
						setAlertTimeACU = 0
			
	finally:
		print ('closing socket_S30')
		sockS30.close()

if __name__ == '__main__':
	
	if len(sys.argv) > 1: 
		myTableID = sys.argv[1]
	else:
		exit("No database Information, Check Sensor's Config...")


	## CONFIG ##########################################################
	# mysql
	db_host = "localhost"
	db_user = "its"
	db_pass = "GXnLRNT9H50yKQ3G"
	db_name = "its_web" # 기본 데이터베이스 

	web_name = "its_web" # 웹페이지 폴더명
	theme_name = "ecos-its_optex" # Optex Theme

	ITS_common_path = "/home/pi/common"
	ITS_utility_path = "/home/pi/utility"
	ITS_rls_v_path = "/home/pi/optex_RLS_V"
	ITS_audio_flag = "/tmp/audioOut"

	ITS_rls_map_file = "rls_map.svg"

	# 센서 환경설정 테이블 명
	ITS_RLS_row_table = "w_log_RLS_RAW" # 로그파일 테이블명의 PreFix로 사용

	ITS_sensor_log_table = "w_log_sensor" # 로그파일 테이블명의 PreFix로 사용
	ITS_sensor_blk_table = "w_block_event" # 예약차단 테이블

	ITS_sensor_max_log = "1000000" # 레코드 갯수(기본 100만)가 limit 값을 넘으면 로래된 레코드를 삭제 한다.

	ITS_log_data = "/var/www/html/"+web_name+"/data/log/" # Log File 저장 위치
	ITS_img_data = "/var/www/html/"+web_name+"/data/image/" # Log File 저장 위치
	ITS_audio_data = "/var/www/html/"+web_name+"/data/audio/" # audio File 저장 위치

	# ITS_host_gate = web_name+"/utility/sensorMgr/collectEvent.php" # w_host_enable 되어있으면 host_ip를 통해 각각의 센서에서 발생이벤트를 w_collect_event 테이블에 자료 등록

	ECOS_table_prefix = "g5_write_"
	ECOS_table_RLS_V = "g200t230" # ITS_WEB에서 생성된 테이블 

	# Sun Mon Tue Wed Thu Fri Sat 
	#  1   2   3   4   5   6   7  
	#  6   0   1   2   3   4   5  
	ECOS_week_map = {
		0 : "2017-01-02", # 월요일
		1 : "2017-01-03", # 화요일
		2 : "2017-01-04",
		3 : "2017-01-05",
		4 : "2017-01-06",
		5 : "2017-01-07",
		6 : "2017-01-01", # 일요일
	}

	######################## 사용자 설정 
	date_of_old = 30 # 일수

	# MAX_event_allowSameCount = 512; # 동일한 거리 레벨이 연속적이면 문제 제기

	# ERROR_socket_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
	# ERROR_socketRecv_cnt = 8
	# ERROR_connect_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
	# ERROR_sleep_cnt = 2 # 초
	# ERROR_recv_timeout = 16 # 초
	ERROR_check_cnt_max = 8 # 최초실행시 디비와 센서체크 오류 횟수

	Event_type = {}
	Event_type['init']	= 0
	Event_type['active']	= 1
	Event_type['idle']	= 2
	Event_type['post']	= 3
	Event_type['shot']	= 4 # 사진
	Event_type['alarm']	= 5
	Event_type['block']	= 6
	Event_type['reload']	= 7
	Event_type['start']	= 8
	Event_type['error']	= 9

	Event_desc = {}
	Event_desc[0] = 'Init. System'
	Event_desc[1] = 'Active Event'
	Event_desc[2] = 'Idle Event'
	Event_desc[3] = 'Post Event'
	Event_desc[4] = 'Snapshot'
	Event_desc[5] = 'Alarm Light'
	Event_desc[6] = 'Block/Schedule'
	Event_desc[7] = 'Reload Program'
	Event_desc[8] = 'Start Program'
	Event_desc[9] = 'Error Event' 

	########################################################
	RLS_limit_time_delta = 10 # Sec, RLS_time_delta_limit 이상 이벤트 발생이 없으면 오류 발생
	RLS_limit_time_delta_msg = "Waiting Heartbit over %s Secs. May disconnected sensor." % RLS_limit_time_delta

	# Preset
	RLS_preset = {}
	RLS_preset[''] = [0,0]
	RLS_preset['Area_1x1'] = [1,1]
	RLS_preset['Area_2x1'] = [2,1]
	RLS_preset['Area_2x2'] = [2,2]
	RLS_preset['Area_4x1'] = [4,1]
	RLS_preset['Area_4x2'] = [4,2]
	RLS_preset['Area_8x1'] = [8,1]
	RLS_preset['Area_8x2'] = [8,2]
	## CONFIG ##########################################################

	w_cfg_sensor_list_All = read_table_w_cfg_sensor_all(myTableID)
	for row in w_cfg_sensor_list_All:
		db_subject = row["wr_subject"]

		db_request1 = row["wr_4"] ## Get/Post
		if db_request1:
			req1_user, req1_pwd, req1_url, req1_enc = db_request1.split('||') 

		db_request2 = row["wr_5"] ## Get/Post
		if db_request2:
			req2_user, req2_pwd, req2_url, req2_enc = db_request2.split('||') 

		db_custom1 = row["wr_8"] ## 
		db_custom2 = row["wr_9"] ## 

		# 원격 릴레이 컨트롤
		db_itsACU = row["wr_10"] ## 
		if db_itsACU:
			itsACU_IP, itsACU_Port, itsACU_ID, itsACU_Zone, itsACU_Time, itsACU_Enc = db_itsACU.split('||') 
			itsACU_Time = float(itsACU_Time)
			# print itsACU_IP, itsACU_Port, itsACU_ID, itsACU_Zone, itsACU_Time, itsACU_Enc

		db_license = row["w_license"]
		db_device_id = row["w_device_id"]
		db_sensor_model = row["w_sensor_model"]
		db_sensor_serial = row["w_sensor_serial"]
		db_sensor_lat_s = row["w_sensor_lat_s"]
		db_sensor_lng_s = row["w_sensor_lng_s"]
		db_sensor_lat_e = row["w_sensor_lat_e"]
		db_sensor_lng_e = row["w_sensor_lng_e"]
		db_table_PortIn = row["w_table_PortIn"]
		db_event_holdTime = row["w_event_holdTime"] # 에벤트 홀드 수
		db_event_postTime = row["w_event_pickTime"] # 에벤트 전송주기
		db_system_ip = row["w_system_ip"]
		db_system_port = row["w_system_port"]
		db_virtual_Addr = row["w_virtual_Addr"]
		db_virtual_Port = row["w_virtual_Port"]
		db_sensor_Addr = row["w_sensor_Addr"]
		db_email_Addr = row["w_email_Addr"]
		db_email_Time = row["w_email_Time"]
		db_host_Addr = row["w_host_Addr"] # 관제 서버 이이피
		db_host_Port = row["w_host_Port"] # 관제 서버 포트
		db_host_Addr2 = row["w_host_Addr2"] # 관제 서버 이이피
		db_host_Port2 = row["w_host_Port2"] # 관제 서버 포트
		db_url1 = row["w_url1"] ## 스냅샷
		db_url2 = row["w_url2"] ## 스트리밍
		db_url3 = row["w_url3"] ## URL1
		db_url4 = row["w_url4"] ## URL2
		db_opt91 = row["w_opt91"]
		db_opt92 = row["w_opt92"]
		db_opt93 = row["w_opt93"]
		db_masquerade = row["w_opt94"]
		
		db_allowSize = (str(int(row["w_sensor_ignoreS"]))+':'+str(int(row["w_sensor_ignoreE"]))).split(',') # 이벤트 허용 크기
		
		if row["w_sensor_ignoreZone"]: 
			db_sensor_ignoreZone = row["w_sensor_ignoreZone"].encode("utf-8").replace(" ", "").rstrip(',').split(',') # 이벤트 무시 영역
		else:
			db_sensor_ignoreZone = []
		
		if row["w_sensor_allowZone"]: 
			db_sensor_allowZone = row["w_sensor_allowZone"].encode("utf-8").replace(" ", "").rstrip(',').split(',') # 이벤트 허용 영역
		else:
			db_sensor_allowZone = []

	print("SensorID:{}",format(db_sensor_serial))
	print("Accept Size:{}",format(db_allowSize))
	print("Allow Area:{}",format(db_sensor_allowZone))
	print("Refuse Area:{}",format(db_sensor_ignoreZone))
	# print("\tEvent Alarm: {}",format( db_alert_Port, db_alert_Value))
	# print("\tZone Alarm: {}",format( db_gpwioRelay, db_gpwioValue, db_gpwioGroup))
	print("\tACU Alarm: {}",format(db_itsACU))
	# print("\tAudio Alarm: {}",format( db_audioName, db_audioTime, db_audioVolume))

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418

	if not os.path.exists(ITS_log_data): # ITS_log_data 폴더 생성
		os.makedirs(ITS_log_data)
	logger = logging.getLogger(db_sensor_serial) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = ITS_log_data+db_sensor_serial+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	# logger.info("TEST END!")
	############ logging ################
	
	############ Images ################
	# 이미지 파일 초기화 
	if not os.path.exists(ITS_img_data): # ITS_img_data 폴더 생성
		os.makedirs(ITS_img_data)
	# 센서 이벤트 스크린샷 이미지 저장 폴더명
	img_data_sub = ITS_img_data + db_sensor_serial + "/"
	if not os.path.exists(img_data_sub): # ITS_img_data 내의 서브 사진 폴더 생성
		os.makedirs(img_data_sub)
	############ Images ################
	
	varPort = int(db_sensor_Addr.split('.')[2]) + int(db_sensor_Addr.split('.')[3])
	nodeIn = 50000 + varPort # db_sensor_Addr = '192.168.168.30' -> 50198
	nodeOut = 51000 + varPort # db_sensor_Addr = '192.168.168.30' -> 51198
	print('\nRunning RLS Realtime Monitoring - http://%s:%s' %(db_system_ip,nodeOut))
	logger.info('\nRunning RLS Realtime Monitoring - http://%s:%s' %(db_system_ip,nodeOut))

	own_cfg = ('/home/pi/optex_RLS_V/config_'+str(nodeIn)+'.json')
	if os.path.isfile(own_cfg):
		config = readConfig(own_cfg)
	else:
		print ("Error Not found %s, Check Config JSON" % own_cfg)
		exit()

	sensor_cfg = ('/home/pi/optex_RLS_V/sensorInfo.json')
	if os.path.isfile(sensor_cfg):
		sensor = readConfig(sensor_cfg)
	else:
		print ("Error Not found %s, Check Config JSON" % sensor_cfg)
		exit()

	ipC = int(db_sensor_Addr.split('.')[2])
	masqPort = ipC + nodeOut # 51000 + 168
	MASQUERADE(db_masquerade,masqPort,ipC)
	print('Running REDSCAN mini Configuration - http://%s:%s' %(db_system_ip,masqPort))

	############ create log table ################
	## 로그 테이블 생성
	returnMsg = create_table_w_log_RLS_V(db_sensor_serial) # postfix='' + mac address
	# print returnMsg # 0 - Success

	url = "http://192.168.168.30/api/info/device/get"
	username = 'root'
	password = 'RLS-3060V'

	payload = {}

	response = requests.get(url, params=payload, auth=HTTPDigestAuth(username, password))

	if response.status_code == 200:
		result = response.json()
		# print(json.dumps(result, indent = 4, sort_keys = True, default = str))
	else:
		quit("Sensor Connect eRROR")

	# sensorPort = 50001

	# #####################################
	# #####################################
	# # Create a TCP/IP socket
	# try:
	# 	sockS30 = socket.create_connection((db_sensor_Addr, sensorPort), timeout=10) # 센서 연결
	# except:
	# 	exit("Socket connection error {}:{}".format(db_sensor_Addr, sensorPort))
	
	# ## mac address
	# sockS30.sendall(reqCommand('cmd01'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd01 = cmd01(data_tmp)
	# # print "MAC address: ", result_cmd01
	result_cmd01 = sensor["gInfoDevice"]["mac"]
	# ## version
	# sockS30.sendall(reqCommand('cmd02'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd02 = cmd02(data_tmp)
	# # print "Version: ", result_cmd02
	result_cmd02 = sensor["gInfoDevice"]["version"]

	# ## area No
	# sockS30.sendall(reqCommand('cmd04')) # 센서에 자료('cmd04') 요청 - 총 760 라인
	# data_tmp = ''
	# # 기본크기를 알수 없는 패킷정보를 End of Packet(0a0a0d)이 나올때 까지 읽어들인다.
	# while True:
	# 	data_tmp += sockS30.recv(1024)
	# 	if all(data_tmp[-3:]) == '0a0a0d': 
	# 		# print 'last socket'
	# 		break
	# if data_tmp:
	# 	# result_cmd04, result_cmd04_2 = cmd04(data_tmp)
	# 	result_cmd04, result_cmd04_2, result_cmd04_3, result_cmd04_4, result_cmd04_5, result_cmd04_6 = cmd04(data_tmp)
	# else:
	# 	result_cmd04 = '' ## 760개의 요소정보
	# 	result_cmd04_2 = 0
	# 	result_cmd04_3 = 0
	# 	result_cmd04_4 = 0
	# 	result_cmd04_5 = 0
	# 	result_cmd04_6 = 0
	# # print "No. of detection area: ", result_cmd04_2, result_cmd04_3, result_cmd04_4, result_cmd04_5, result_cmd04_6

	if sensor["wsDetectArea"]["distances"]:
		dataObj = sensor["wsDetectArea"]["distances"]
		count = 0
		maxX = 0
		maxY = 0
		minX = 0
		minY = 0
		objInfo = ''
		unitAngle = 0.25 # float(190/760)
		while (count < sensor["wsDetectArea"]["steps"]):
			orgX = 0 # 30000 # 출력화면의 X축 0점이 30000에서 시작한다.
			fLN = count * 4
			tLN = fLN + 4
			# print all(dataObj[fLN:tLN])
			# length = hex2int(dataObj[fLN:tLN])
			length = dataObj[count]
			angle = math.radians(unitAngle * (count - 20)) # 시작이 -20번째부터 진행 한다(총 185도)
			distX = int(length * math.cos(angle))
			distY = int(length * math.sin(angle))
			
			if (maxX < distX): maxX = distX
			if (maxY < distY): maxY = distY
			if (minX > distX): minX = distX
			if (minY > distY): minY = distY

			# print 'No:%3s, Ag:%6s, X:%5s, Y:%5s' % (count, unitAngle * (count - 20), distX, distY)
			
			objInfo += "L %s %s " % (distX + orgX, distY)
			count = count + 1
			
		objInfo = "<path class='html_scan' d='M%s 0 %s Z' />" % (orgX, objInfo)
		result_cmd04 = objInfo
		result_cmd04_2 = sensor["wsDetectArea"]["steps"]
		result_cmd04_3 = maxX
		result_cmd04_4 = maxY
		result_cmd04_5 = minX
		result_cmd04_6 = minY
	else:
		result_cmd04 = '' ## 760개의 요소정보
		result_cmd04_2 = 0
		result_cmd04_3 = 0
		result_cmd04_4 = 0
		result_cmd04_5 = 0
		result_cmd04_6 = 0
	print("No. of detection area: ", result_cmd04_2, result_cmd04_3, result_cmd04_4, result_cmd04_5, result_cmd04_6)
	# print(objInfo)


	# ## zone information
	# sockS30.sendall(reqCommand('cmd05'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd05, result_cmd05_2, result_cmd05_3, result_cmd05_4, result_cmd05_5, result_cmd05_6 = cmd05(data_tmp)
	# # print "Radius of area A/B, Type, No. of regions, Mode: ", result_cmd05
	
	# ## basic parameter
	# sockS30.sendall(reqCommand('cmd07'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd07 = cmd07(data_tmp)
	# # print "Angle, No. of lines, Center of lines: ", result_cmd07
	
	# ## destination of Redwall
	# sockS30.sendall(reqCommand('cmd08'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd08 = cmd08(data_tmp)
	# # print "Communication by (TCP)(UDP): ", result_cmd08
	
	# ## relay output
	# sockS30.sendall(reqCommand('cmd09'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd09 = cmd09(data_tmp)
	# # print "Relay output: ", result_cmd09

	# ## masking/allocating file
	# sockS30.sendall(reqCommand('cmd10'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd10 = cmd10(data_tmp)
	# # print "Masking/Allocating file: ", result_cmd10

	# ## masking/allocating area
	# sockS30.sendall(reqCommand('cmd11'))
	# data_tmp = ''
	# # 기본크기를 알수 없는 패킷정보를 읽어들인다.
	# while True:
	# 	data_tmp += sockS30.recv(1024)
	# 	if all(data_tmp[-3:]) == '0a0a0d': 
	# 		# print 'last socket'
	# 		break
	# if data_tmp:
	# 	result_cmd11 = cmd11(data_tmp)
	# 	result_cmd11_A = '' # allocating area
	# 	result_cmd11_M = '' # masking area
	# 	if result_cmd11[0] == 1:
	# 		result_cmd11_A = result_cmd11[1]
	# 		result_cmd11 =  "Allocate zone: Enabled"
	# 	else:
	# 		result_cmd11_M = result_cmd11[1]
	# 		result_cmd11 =  "Mask zone: Enabled"
	# else:
	# 	result_cmd11_A =''
	# 	result_cmd11_M ='' 
	# 	result_cmd11 =  "No masking/allocating area"
	# # print result_cmd11, result_cmd11_A, result_cmd11_M

	# ## model name
	# sockS30.sendall(reqCommand('cmd12'))
	# data_tmp = sockS30.recv(1024)
	# result_cmd12 = cmd12(data_tmp)
	# if '2020' in result_cmd12: 
	# 	type_RLS = "2020" # 센서타입 2020 또는 3060
	# else:
	# 	type_RLS = "3060" # 센서타입 2020 또는 3060
	# # print "Model name: ", result_cmd12 # , all(data_tmp)
	result_cmd12 = result['model']
	type_RLS = "3060"
	
	#####################################
	#####################################



	## Html(SVG) 파일 생성
	## NodeJS 실행에 필요한 실시간 파일 생성
	## 노드JS 데몬 실행
	# makeHtml(type_RLS)
	makeHtml("3060")
	# argv_realtime_RLS = '%s %s' % (nodeIn, nodeOut)
	run_demon_realtime_RLS_V(nodeIn)

	print ("\n")
	print ("MAC address: %s " % result_cmd01)
	print ("Version: %s " % result_cmd02)
	print ("Cnt#:%s, MaxX:%s, MaxY:%s, MinX:%s, MinY:%s" % (result_cmd04_2, result_cmd04_3, result_cmd04_4, result_cmd04_5, result_cmd04_6))
	# print ("RadiusA/B:%s/%s, Type:%s, Regions:%s, Mode:%s, Length:%s" % (result_cmd05, result_cmd05_2, result_cmd05_3, result_cmd05_4, result_cmd05_5, result_cmd05_6))
	# print ("Angle, Total_lines, Center_lines: %s" % result_cmd07)
	# print ("Communication by (TCP)(UDP): %s " % result_cmd08)
	# print ("Relay output: %s " % result_cmd09)
	# print ("Masking/Allocating file: %s " % result_cmd10)
	# print ("Masking/Allocating area: %s " % [result_cmd11, result_cmd11_A, result_cmd11_M])
	print ("Model name: %s " % type_RLS)
	
	## 프리셋을 위한 분할 값
	print ("Preset x:%s, y:%s"%(RLS_preset[db_sensor_model][0],RLS_preset[db_sensor_model][1]))
	
	logger.info("Started Ready to Receiving..")
	insert_event_RLS_V(db_sensor_serial, 0, 0, 0, 0, "start") ## 시작 DB update


	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception as e:
		print (str(e))
		traceback.print_exc()
		os._exit(1)