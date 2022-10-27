#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import datetime
import socket 
import shutil
import MySQLdb
import requests
import os
import sys
import subprocess 
import fcntl
import struct
import binascii
import logging
import logging.handlers
import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO

from requests.auth import HTTPDigestAuth
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from PIL import Image, ImageDraw, ImageFont
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)


from config import *

## 공용 모듈 일어들임
import imp
authRequest = imp.load_compiled("*", ITS_common_path+"/m_authRequest.pyc") ## 예) common.MyClass() load_compiled
findAngle = imp.load_compiled("*", ITS_common_path+"/m_findAngle.pyc") ## 예) common.MyClass() load_compiled

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
		
def create_table_w_log_BSS(postfix=''): # create_table_w_log_BSS(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		if(postfix):
			postfix = '_' + postfix
		tbl_w_log_sensor_sql = """
			CREATE TABLE IF NOT EXISTS %s%s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			`w_cfg_id` int(11) NOT NULL DEFAULT '0',

			`w_bss_slave` varchar(32) NULL DEFAULT '', 
			`w_bss_device` varchar(32) NULL DEFAULT '',
			`w_bss_distent` int(11) NOT NULL DEFAULT '0',
			`w_bss_error` int(11) NOT NULL DEFAULT '0',
			`w_bss_level` int(11) NOT NULL DEFAULT '0',
			`w_bss_alarm` varchar(32) NULL DEFAULT '',
			`w_bss_type` varchar(32) NULL DEFAULT '',
			`w_bss_speed` int(11) NOT NULL DEFAULT '0',

			`w_event_zeroDist` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_outLevel` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_outCount` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_cnt` int(11) NOT NULL DEFAULT '0',
			`w_event_ignore` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_schedule` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_sent` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_shot` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_error` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_mail` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_alert` tinyint(1) NOT NULL DEFAULT '0',
			`w_event_desc` varchar(128) NULL DEFAULT '',
			`w_event_stat` varchar(128) NULL DEFAULT '',

			`w_opt_0` float NOT NULL DEFAULT '0',
			`w_opt_1` float NOT NULL DEFAULT '0',
			`w_opt_2` int(11) NOT NULL DEFAULT '0',
			`w_opt_3` int(11) NOT NULL DEFAULT '0',
			`w_opt_4` varchar(32) NULL DEFAULT '',
			`w_opt_5` varchar(32) NULL DEFAULT '',
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % (ITS_sensor_log_table, postfix)
		cursor.execute(tbl_w_log_sensor_sql) # create table
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
 	except MySQLdb.Warning, warning:
		pass
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

# def insert_socket_GPWIO(id, status, msg): 
	# node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# try: 
		# # node.connect((ip,port))
		# node.connect(('localhost', 8040))
		# msg_data = ('id=%s,status=%s,msg=%s' % (id, status, msg))
		# node.send(msg_data) 
		# node.close() 
		# return 1
	# except socket.error:
		# return 0
	# except socket.timeout:
		# return 0
	# finally:
		# node.close() 
		
def insert_socket_log_BSS(serial, wr_subject, beep, lat_s, lng_s, lat_e, lng_e, shot, host, port, dist, speed, zone, error):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data = ('id=%s,name=%s,beep=%s,status=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,shot=%s,dist=%s,speed=%s,zone=%s,subzone=%s' % (serial, wr_subject, beep, error, lat_s, lng_s, lat_e, lng_e, shot, dist, speed, zone, int(dist/10)))
		s.send(msg_data) 
		# print msg_data
		s.close() 
		return ("Sent %s:%s" % (host, port))
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
		
def send_camera_PRESET_PARSER(content):
	## content = 'root||password||http://host/command?option=id||1'
	try:
		elements = content.split('||') 
		user = elements[0]
		pwd = elements[1]
		url = elements[2]
		enc = int(elements[3])
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

# // G:\Development\ecos_its-OPTEX\its_GPWIO\GPWIO.js	
# // G:\Development\ecos_its-OPTEX\its_MONITOR\its_M_map.js
# G:\Development\ecos_its-OPTEX\its_GPIO\module.py

def divisysPopupID(content):
	elements = content.split('||') 
	usr = elements[0]
	pwd = elements[1]
	host = elements[2]
	port = int(elements[3])
	opt1 = elements[4]
	opt2 = elements[5]

	if not opt1:
		return 0
	if not opt2:
		opt2 = "99"
		
	# packet = '\x02' + opt2 + '\x3b\x30\x03'
	# packet = '\x02' + opt2 + '\x3b\x39\x39\x03'
	packet = '\x02' + opt1 + '\x3b' + opt2 + '\x03'

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		s.send(packet) 
		s.close() 
		return("Sent ID:%s"% str(opt2))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 
				
# ## 한화테크원 TSM-2100 JSON Http Request
# ## https://stackoverflow.com/questions/9733638/post-json-using-python-requests
# def insert_post_log_BSS_JSON(host, serial, wr_subject, status, beep, shot, dist, zone, enc):
	# # import requests
	# # url = 'http://httpbin.org/post'
	# # data = {"data" : "24.3"}
	# # data_json = json.dumps(data)
	# # headers = {'Content-type': 'application/json'}
	# # response = requests.post(url, data=data_json, headers=headers)
	# # response.json()
	# preset = str(int(dist//10000) + 1) # value 값: 0 ~ 99999 cm 미리미터 값의 10미터 단위로 나눈후 더하기 1
	# # dateTime = datetime.datetime.now() # "Sent":"0000-00-00 00:00:00 +0000",
	# dateTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	
	# data = {"Sender":"%s"%wr_subject,"Sent":"%s +0900"%dateTime,"Event":[{"EventCode":"alert","Description":"","Parameter":[{"Key":"id","Value":"%s"%serial},{"Key":"name","Value":"%s"%wr_subject},{"Key":"shot","Value":"%s"%shot},{"Key":"dist","Value":"%s"%dist},{"Key":"zone","Value":"%s"%zone},{"Key":"preset","Value":"%s"%preset}]}]}
	
	# # print data
	
	# try:
		# # data_json = json.dumps(data)
		# headers = {'Content-type': 'application/json'}
		# # r = requests.post(host, json=data_json, headers=headers)
		# # r = requests.get('http://httpbin.org/get', json={"key": "value"})
		# # r = requests.post('http://httpbin.org/post', json={"key": "value"})
		# # r = requests.post('http://httpbin.org/post', json=data_json)
		# # r = requests.post(host, json=data_json, headers=headers)
		# r = requests.post(host, json=data, headers=headers)
		# return r.status_code # r.text , r.json(), r.status_code
	# except:
		# return "requests.post Error: %s" % host

	
# ## 한화테크원 PTZ Camera PRESET Http Request
# ## http://user:pass@192.168.0.37/stw-cgi/ptzcontrol.cgi?msubmenu=preset&action=control&Preset=1
# def insert_get_log_BSS_PRESET(host, serial, wr_subject, status, beep, shot, dist, zone, enc):
	# preset = str(int(dist//10000) + 1) # value 값: 0 ~ 99999 미리미터 값의 10미터 단위로 나눈후 더하기 1
	# url = "%s%s" % (host,preset)
	# try:
		# if(enc):
			# # host = "http://admin:optex59@192.168.0.37/stw-cgi/video.cgi?msubmenu=stream&action=view"
			# # host = "http://root:pass@192.168.0.38/axis-cgi/com/ptz.cgi?pan=0&tilt=0&zoom=1&focus=1&iris=1&brightness=1&autofocus=on"
			# a = host.rsplit('@',1)[0]
			# b = a.split('://',1)[1]
			# c = b.split(':',1) # admin:optex59:://@@71!!
			# user = c[0]
			# pwd = c[1]
			# r = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=0.1)
		# else:
			# r = requests.get(url, timeout=0.1)
		# return "%s Ps:%s" % (r.status_code, preset) # r.text
	# # except r.exceptions.Timeout:
		# # return "Timeout  %s" % host
	# except:
		# return "requests.get Error: %s" % host

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
			return r.status_code, "Downloaded image Format Error %s" % file
			
	# time.sleep(10) 스레드 테스트
	return r.status_code, "Snapshot OK"
	
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
		
# node.js로 실시간 GUI관제 서비스를 위해 위트 IP(BSS_system_ip)와 port 8000 + IP 조합 으로 강제 촐력	
def insert_socket_monitor_BSS(serial, wr_subject, lat_s, lng_s, lat_e, lng_e, host, port, dist, alarmOut, sensorType, zone): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,alarmOut=%s,sensorType=%s,zone=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, sensorType, zone))
		node.send(msg_data) 
		node.close() 
		# print msg_data
		return ("Sent %s:%s" % (host, port))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
# node.js로 실시간 GUI관제 서비스를 위해 위트 IP(BSS_system_ip)와 port 8000 + IP 조합 으로 강제 촐력	
# insert_socket_monitor_BSS 에서 위치 레벨 속도 추가 
def insert_socket_monitor_BSS_OBJ(serial='', wr_subject='', lat_s='', lng_s='', lat_e='', lng_e='', host='', port='', dist='', alarmOut='', sensorType='', zone='', obj_length='', obj_time='', obj_speed='', obj_move='', obj_level=''): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if (sensorType is 0): zone = 0 # 대항형이면 거리를 무시하고 존값을 0으로 설정한다.
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,alarmOut=%s,sensorType=%s,zone=%s,obj_length=%s,obj_time=%s,obj_speed=%s,obj_move=%s,obj_level=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, sensorType, zone, obj_length, obj_time, obj_speed, obj_move, obj_level))
		node.send(msg_data) 
		node.close() 
		# print msg_data
		return ("Sent %s:%s" % (host, port))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
def insert_event_log_BSS(tableName, w_cfg_id=0, w_bss_slave='', w_bss_device='', w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='', w_bss_type='', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='', w_event_desc='', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5=''): 
	query = "INSERT INTO "+ITS_sensor_log_table+"_"+tableName+"(w_cfg_id, w_bss_slave, w_bss_device, w_bss_distent, w_bss_error, w_bss_level, w_bss_alarm, w_bss_type, w_bss_speed, w_event_cnt, w_event_zeroDist, w_event_outLevel, w_event_outCount, w_event_ignore, w_event_schedule, w_event_sent, w_event_shot, w_event_error, w_event_stat, w_event_desc, w_opt_0, w_opt_1, w_opt_2, w_opt_3, w_opt_4, w_opt_5) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	args = (w_cfg_id, w_bss_slave, w_bss_device, w_bss_distent, w_bss_error, w_bss_level, w_bss_alarm, w_bss_type, w_bss_speed, w_event_cnt, w_event_zeroDist, w_event_outLevel, w_event_outCount, w_event_ignore, w_event_schedule, w_event_sent, w_event_shot, w_event_error, w_event_stat, w_event_desc, w_opt_0, w_opt_1, w_opt_2, w_opt_3, w_opt_4, w_opt_5)
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
		
def read_table_w_cfg_sensorID_BSS(): # Optex Microwave
	# query = "SELECT wr_id, w_sensor_noOfZone, w_virtual_Addr FROM " + ECOS_table_prefix + ECOS_table_BSS + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_BSS + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
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

def read_table_w_cfg_sensor_BSS(wr_id=''): # Optex Microwave
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_BSS + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "
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

def read_field_w_cfg_serial_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_sensor_serial FROM " + ECOS_table_prefix + ECOS_table_BSS + " WHERE wr_id = " + wr_id
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

def read_field_w_cfg_status_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_sensor_stop, w_sensor_reload, w_alarm_disable FROM " + ECOS_table_prefix + ECOS_table_BSS + " WHERE wr_id = " + wr_id
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
		
def set_reload_w_cfg_reload_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_sensor_reload(0/1) 값에 따라 동작
	query = "UPDATE " + ECOS_table_prefix + ECOS_table_BSS + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
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

def check_scheduledDate_BSS(wr_id=''): # Optex Microwave
	scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	query = "SELECT COUNT(*) as cnt FROM " + ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + ECOS_table_BSS + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
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
		
def check_scheduledWeek_BSS(wr_id='', weekNo=''): # Optex Microwave
	# 편의상 2017년 1월 1일 첫째 주 일요일 부터 토요일 까지를 주간 예약 시간표로 사용한다.
	# 예약된 날짜와 요일에 마추어서 현재 시간을 결합해서 검색을 한다.
	# date.weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6. 
	# print ECOS_week_map[weekNo], "ECOS_week_map[weekNo]"
	# scheduledWeek = time.strftime("%Y-%m-%dT%H:%M:%S")
	scheduledWeek = ECOS_week_map[weekNo]+time.strftime("T%H:%M:%S") # 2017-01-01 + 현재시간
	query = "SELECT COUNT(*) as cnt FROM " + ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + ECOS_table_BSS + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
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

def itsMemberConfig(field): # table
	cursor = None
	conn = None
	query = "SELECT " + field + " FROM g5_member WHERE mb_id = 'manager'" 
	# mb_4 - system ip address
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchone() # 커서의 fetchall()는 모두, fetchone()은 하나의 Row, fetchone(n)은 n개 만큼
	except MySQLdb.Error as error:
		return 0
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()


################################################################

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

# multiprocessing 라이브러리를 이용해서 일정시간(druation)동안 알람을 발생 시킨다.
# Using - Process(target=alarmOut, args=(2,7)).start()
# http://mydb.tistory.com/245
# http://studymake.tistory.com/498

def audioOut(file): # 
	# os.system('omxplayer %s &'%file) ## os.system('omxplayer http://192.168.0.5/tmp/dog-howling-yapping-daniel_simon.mp3 &')
    # os.system("omxplayer " + file + " &")
	cmd = "omxplayer %s >/dev/null & " % file
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
def alertOut(port, druation): # GPIO Port No. , Action Due
	insert_socket_GPWIO(id=port, status=0, msg='')
	time.sleep(druation)
	insert_socket_GPWIO(id=port, status=1, msg='')
	# if(GPIO.input(port)):
	# 	GPIO.output(port, False)
	# 	time.sleep(druation)
	# 	GPIO.output(port, True)
	# else:
	# 	pass
		
# def alertOn(port): # GPIO Port No. , Action Due
	# GPIO.output(port, False)
# def alertOff(port): # GPIO Port No. , Action Due
	# GPIO.output(port, True)

# 자신 아이피 확인 
def get_ip_address(ifname): # get_ip_address('eth0')  # '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])
	
# 센서 아이피 확인 
def check_sensor(sensorIP):
    return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error

# # MYSQL 실행 확인 
# def check_mysql():
	# # cmd = "ps -fU mysql | grep mysqld.sock | wc -l"
	# cmd = "ps -fU mysql | grep mysqld | wc -l"
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	# return p.communicate()
    # # return os.system("pgrep mysql | wc -l") # IF RETURN 0 THAT Network Active ELSE Network Error

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BSS01(): 
	# cmd = "kill $(ps aux | grep '[p]ython /home/pi/optex_BSS/optex_BSS01.pyc' | awk '{print $2}')" 
	cmd = "kill $(ps aux | grep 'optex_BSS01.pyc' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_BSS01(arg): 
	# cmd = "python -u -W ignore /home/pi/optex_BSS/optex_BSS01.pyc %s 2>&1 & " % arg
	# -W ignore : 콘솔 출력 GPIO.setwarnings(False) to disable warnings
	cmd = "python /home/pi/optex_BSS/optex_BSS01.pyc %s 2>&1 & " % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
			
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BSS01_map(): 
	# cmd = "kill $(ps aux | grep '[n]ode table_BSS_map.js' | awk '{print $2}')" 
	cmd = "kill $(ps aux | grep 'table_BSS_map.js' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_BSS01_map(arg):
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node table_BSS_map.js %s 2>&1 & " % (path, arg)
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_UNION_table(): 
	cmd = "kill $(ps aux | grep '[n]ode table_union.js' | awk '{print $2}')"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_UNION_table(arg): 
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node table_union.js %s 2>&1 & " % (path, arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BSS01_table(): 
	# cmd = "kill $(ps aux | grep '[n]ode table_BSS.js' | awk '{print $2}')" 
	cmd = "kill $(ps aux | grep 'table_BSS.js' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_BSS01_table(arg): 
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node table_BSS.js %s 2>&1 & " % (path, arg)
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 모니터링을 위한 리얼타임 그레프파일을 생성한다.
def make_table_map_html(source, target, content):
	__script_jquery_js__ = '/home/pi/common/jquery/jquery-3.1.1.min.js'
	__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	__script_jquery_ui_js__ = '/home/pi/common/jquery/ui/jquery-ui.js'
	__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	__style_jquery_ui_css__ = '/home/pi/common/jquery/ui/jquery-ui.css'
	__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	
	# __svg_pan_zoom__ = '/home/pi/common/svg-pan-zoom/svg-pan-zoom.js'
	# __svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'
	__smoothiecharts__ = '/home/pi/common/smoothiecharts/smoothie.js'
	__smoothiecharts__ = '<script>'+open(__smoothiecharts__, 'r').read()+'</script>'
	
	# __svg_content__ = open(content, 'r').read()
	
	# print __style_jquery_ui_css__
	with open(source, 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
		# tmp_its_tmp = tmp_its_tmp.replace('__svg_pan_zoom__', __svg_pan_zoom__)
		tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
		# tmp_its_tmp = tmp_its_tmp.replace('__svg_content__', __svg_content__)
		with open(target, 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()

def restart_BSS():
	# print(sys.executable, sys.executable, " ", sys.argv)
	os.execl(sys.executable, sys.executable, *sys.argv)

# 원격 카메라 이미지 다운로드
# ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/ITS_%s.jpg  -q -o /dev/null
def run_wget_image(source, target): 
	cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (source, target)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 프로그램 오류 발생 또는 설정 변경후 다시 자신의 프로그램을 다시 시작 한다.
def restart_myself():
	# os.execv(__file__, sys.argv)
	print sys.executable, " ", sys.argv
	# os.execv(sys.executable, [sys.executable] + sys.argv)
	os.execv(__file__, sys.argv)

# 프로그램 오류 발생시 부모프로그램 다시 실행 한다.
def restart_its(): 
	## command to run - tcp only ##
	cmd = "python /home/pi/optex_BSS/run_optex.pyc"
	# cmd = "python demon.pyc %s 2>&1 & " % arg 
	print(cmd)
	## run it ##
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	# 프로그램 오류 발생시 시스템 다시 시작 한다.
def reboot_its():
	# os.system('/sbin/shutdown -r now')
	os.system('sudo reboot')


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

def get_current_location_BSS(lat_s,lng_s,lat_e,lng_e, tmp_distant, MAX_stepOfZone, MAX_numberOfZone): # 좌표와 좌표 특정한 중간점의 좌표
	# print lat_s,lng_s,lat_e,lng_e, tmp_distant, MAX_stepOfZone, MAX_numberOfZone
	# 37.486487358 127.10386268 37.48644736 127.106177675 18304.0 1000.0 200
	# 37.486487358 127.10386268 37.48644736 127.106177675 17473.0 1000.0 200
	# 37.486487358 127.10386268 37.48644736 127.106177675 15811.0 1000.0 200
	# 37.486487358 127.10386268 37.48644736 127.106177675 24121.0 1000.0 200
	# 37.486447360 127.10617767
	
	unit_coord_lat = (lat_e - lat_s) / MAX_numberOfZone
	unit_coord_lng = (lng_e - lng_s) / MAX_numberOfZone
	dist_zone = tmp_distant / MAX_stepOfZone
	lat_s_n = lat_s + (unit_coord_lat * dist_zone)
	lng_s_n = lng_s + (unit_coord_lng * dist_zone)
	lat_e_n = lat_s_n + unit_coord_lat
	lng_e_n = lng_s_n + unit_coord_lat

	# print lat_s_n,lng_s_n,tmp_distant
	coordinate = []
	coordinate = [lat_s_n,lng_s_n,lat_e_n,lng_e_n,dist_zone]
	
	return coordinate
	
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
			