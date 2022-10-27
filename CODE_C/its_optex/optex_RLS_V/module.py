#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import subprocess 
import MySQLdb
import requests
import socket 
import shutil
import errno
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
filterwarnings('ignore', category = MySQLdb.Warning)

from config import *

# ## 공용 모듈 일어들임
# import imp
# authRequest = imp.load_compiled("*", ITS_common_path+"/m_authRequest.pyc") ## 예) common.MyClass() load_compiled
# findAngle = imp.load_compiled("*", ITS_common_path+"/m_findAngle.pyc") ## 예) common.MyClass() load_compiled

### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
reload(sys)
sys.setdefaultencoding('utf-8')

def database_test(): # Optex Microwave
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		return 1
	except:
		return 0

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
	
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)
	
# # 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
	
def kill_demon_check_RLS_V(): 
	cmd = "pkill -9 -ef optex_RLS_V.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	# cmd = "pkill -9 -ef optex_RLS_alarm.pyc 2>&1" 
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# time.sleep(1)
	# return p
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_check_RLS_V(arg): # python -W ignore
	cmd = "python /home/pi/optex_RLS_V/optex_RLS_V.pyc %s 2>&1 & " % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	# ## ## optex_RLS_alarm 동시 실행
	# cmd = "python /home/pi/optex_RLS_V/optex_RLS_alarm.pyc %s 2>&1 & " % arg
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
# def kill_demon_realtime_RLS_V(arg): 
	# cmd = "kill $(ps aux | grep '[n]ode realtime_RLS.js %s' | awk '{print $2}')" % arg
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# time.sleep(1)
	
def kill_demon_realtime_RLS_V(): 
	cmd = "pkill -9 -ef realtime_RLS.js 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return p
	
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

	
# 라즈베리 CPU Serial Code
def get_serial(): # 라즈베리 전용 코드
	# Extract serial from cpuinfo file
	cpuserial = "0000000000000000"
	try:
		f = open('/proc/cpuinfo','r')
		for line in f:
			if line[0:6]=='Serial':
				cpuserial = line[10:26]
		f.close()
	except:
		cpuserial = "ERROR000000000"
	return cpuserial
	
# 초단위를 시간차이값 형태로 변환 예: 2초 -> 0:00:02.000000
def conv_sec_2_time(second):
	return datetime.timedelta(seconds=second)

# 시간을 초로 반환한다.
def conv_time_2_sec(times):
	return times.total_seconds()

# 화면내용 삭제
def clear_screen(): # 초기 화면 내용 삭제 
	subprocess.call('clear',shell=True)

# 화면버퍼 출력
def print_buff(string): 
	sys.stdout.write(string)

screen_put = os.fdopen(sys.stdout.fileno(), 'w', 0)
def dot_out(str='.'):
	screen_put.write(str)

#############################################################
#############################################################
	
def isTableExist(tableName): ###################### Optex REDSCAN
	query = "SELECT * FROM information_schema.tables WHERE table_schema = '"+db_name+"' AND table_name = '"+tableName+"' LIMIT 1;"
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		if result: # 테이블이 존재 하면
			return 0
		else: # 테이블이 존재 하지 않으면
			return 1
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def create_table_w_log_RLS_V(postfix=''): # create_table_w_log(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
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
	except MySQLdb.Error as error:
		print(error)
 	except MySQLdb.Warning as warning:
		pass
	finally:
		cursor.close()
		conn.close()
		
def insert_event_RLS_V(tableName, w_evt_id=0, w_evt_X=0, w_evt_Y=0, w_evt_S=0, w_evt_zone=''): 
	query = "INSERT INTO "+ITS_sensor_log_table+"_"+tableName+"(w_evt_id, w_evt_X, w_evt_Y, w_evt_S, w_evt_zone) VALUES(%s, %s, %s, %s, %s)"
	args = (w_evt_id, w_evt_X, w_evt_Y, w_evt_S, w_evt_zone)
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

## 레코드 갯수가 limit 값을 넘으면 로래된 레코드를 삭제 한다.
def delete_over_limit_log(tblIs, limit):
	query = "DELETE FROM `"+tblIs+"` WHERE `w_id` < (SELECT MIN(m.`w_id`) FROM (SELECT `w_id` FROM `"+tblIs+"` ORDER BY `w_id` DESC LIMIT "+limit+") m)"
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
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
		
########################################
## NVR(Server) 서버는 센서서버(client)의 연결을 기다립니다.
## 센서서버에 NVR 서버의 IP와 PORT를 설정합니다. (기본포트: 2154, 변경가능)
## 센서서버는 NVR서버의 IP:PORT에 접속합니다.(연결유지)
## 각 구간의 센서에서 이벤트가 발생하면 센서서버는 NVR서버에 해당 코드를 전송합니다.
## NVR서버는 수신한 데이터를 동일하게 센서서버로 전송합니다.
## 1) 시작코드     : 0x02
## 2) 알람발생구간 : "1"  "12" "999"  char형으로 1자리부터 최대 3자리 까지 0x31  0x31 0x32   0x39 0x39 0x39
## 3) 구분코드     : 0x3b
## 4) 위치코드     : "1"  "2"  ~ "9"     =>  "0"으로 보냅니다.           
## 5) 종료코드     : 0x03
##    (주의) 알람발생구간 값이 '0'(0x30) 값이면 live 신호입니다.
## 예)
## PC-MAP  ->  NVR서버
## 0x02 "5"   0x3b "2" 0x03   =    5번구간의 2번위치에 이벤트발생
## 0x02 "15"  0x3b "3" 0x03   =   15번구간의 3번위치에 이벤트발생
## 0x02 "215" 0x3b "1" 0x03   =  215번구간의 1번위치에 이벤트발생
## NVR서버는 수신한 내용을 동일하게 리턴합니다.
## 구간내에 위치가 지정되지 않기때문에 위치값은 "0"으로 처리 합니다.
## 테스트 - /home/pi/utility/customPopupDIVISYS.py
## content = 'Format: USER||PASS||IP||Port||opt1||opt2'

# # DIVISYS CMS Camera Popup Info
# # VAR1 || VAR2 || SRV_IP || SRV_Port || Option_1 || Option_2
# # 변수1 || 변수2 || 서버IP || 서버Port || 선택(A,B,C,D) || 선택(a,b,c,d)
# # Option_1과 Option_2는 1개에서 4개까지 입력 가능하며 그 이상은 무시 된다.
# # Option_1과 Option_2는 입력 순서로 서로 대응 된다.
# # Ex: ||||192.168.0.202||2154||1,3,5,7,9||1,3,5,7,9
# # 테스트 - /home/pi/utility/customPopupDIVISYS.py
# # // G:\Development\ecos_its-OPTEX\its_GPWIO\GPWIO.js	
# # // G:\Development\ecos_its-OPTEX\its_MONITOR\its_M_map.js
# # G:\Development\ecos_its-OPTEX\its_GPIO\module.py

# def divisysPopupID(host, port, opt1='', opt2=''):
# 	if not opt1: # 팝업을 위한 카메라 번호
# 		return 0
# 	if not opt2: # 카메라 프리셋 번호
# 		opt2 = "99"
		
# 	# packet = '\x02' + opt2 + '\x3b\x30\x03'
# 	# packet = '\x02' + opt2 + '\x3b\x39\x39\x03'
# 	packet = '\x02' + opt1 + '\x3b' + opt2 + '\x03'

# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
# 	try: 
# 		s.connect((host,port))
# 		s.send(packet) 
# 		s.close() 
# 		return("Sent ID:%s"% str(opt2))
# 	except socket.error:
# 		return 0
# 	except socket.timeout:
# 		return 0
# 	finally:
# 		s.close() 

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


def read_table_w_cfg_sensorID(): ###################### Optex REDSCAN
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_RLS_V + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_sensor_all(wr_id=''): # Optex Microwave
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_RLS_V + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "

	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_field_w_cfg_status(wr_id=''): 
	query = "SELECT w_sensor_stop, w_sensor_reload, w_sensor_disable, w_alarm_disable FROM " + ECOS_table_prefix + ECOS_table_RLS_V + " WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def set_reload_w_cfg_reload(wr_id=''): 
	query = "UPDATE " + ECOS_table_prefix + ECOS_table_RLS_V + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def check_scheduledDate(wr_id=''): # Optex Microwave
	scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	query = "SELECT COUNT(*) as cnt FROM " + ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + ECOS_table_RLS_V + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		return result

	except MySQLdb.Error as error:
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
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		return result

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

