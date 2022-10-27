#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import datetime
import subprocess 
import socket 
import urllib
import requests
import MySQLdb
import threading
import logging
import logging.handlers
import RPi.GPIO as GPIO
import json

from hashlib import sha256
from multiprocessing import Process
from requests.auth import HTTPDigestAuth
from multiprocessing.pool import ThreadPool
from PIL import Image, ImageDraw, ImageFont
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

# from config import *

# ## 공용 모듈 일어들임
# import imp
# # authRequest = imp.load_source("*", ITS_common_path+"/m_authRequest.py") ## 예) common.MyClass() load_source
# authRequest = imp.load_compiled("*", ITS_common_path+"/m_authRequest.pyc") ## 예) common.MyClass() load_compiled

### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
reload(sys)
sys.setdefaultencoding('utf-8')

############# Audio
audioFlag = "/home/pi/common/audioOut"
def audioCheckFlag(): ## 오디오 포트 확인 ## audioFlag란 파일이 존재하면 사용중으로 간주, 바로 종료
	if os.path.isfile(audioFlag):
		# print('checkFlag Busy %s'%audioFlag)
		return 1
	else:
		return 0
		
def audioMakeFlag(): ## 오디오 포트 예약 ## audioFlag 파일을 생성하여 오디오 중복 실행을 방지
	open(audioFlag, 'a').close()
	# print('makeFlag %s'%audioFlag)
	
def audioRemoveFlag(): ## 오디오 포트 해지 ## audioFlag 파일을 삭재하여 오디오 실행을 허용함
	if os.path.isfile(audioFlag):
		os.remove(audioFlag)
	# print('removeFlag %s'%audioFlag)

def audioOutTime(file, time): ## 음악을 틀은후 특정시간(time)후 플래그 삭제
	if audioCheckFlag():
		return 0
	else:
		audioMakeFlag()
		audioOut(file)
		threading.Timer(time, audioRemoveFlag).start()

def audioOut(file): # 
	cmd = "omxplayer %s >/dev/null & " % file
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
############# Audio

def alertOut(port, druation): # BIGDATA Port No. , Action Due
	insert_socket_GPWIO(id=port, status=0, msg='')
	time.sleep(druation)
	insert_socket_GPWIO(id=port, status=1, msg='')

# 실행하고 있는 'dndmon'란 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BIGDATA(arg): 
	# cmd = "kill $(ps aux | grep '[p]ython -u -W ignore /home/pi/BIGDATA/BIGDATA.pyc' | awk '{print $2}')"
	cmd = "kill $(ps aux | grep 'BIGDATA.pyc %s' | awk '{print $2}')" % arg
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BIGDATA_table(): 
	cmd = "kill $(ps aux | grep '[n]ode table_BIGDATA.js' | awk '{print $2}')"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

# 확인된 변수로 데몬을 실행 한다
def run_BIGDATA(arg): 
	cmd = "python -u -W ignore /home/pi/BIGDATA/BIGDATA.pyc %s 2>&1 & " % arg 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 확인된 변수로 데몬을 실행 한다
def run_demon_BIGDATA_table(arg): 
	# path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	# cmd = "cd /var/www/html/its_web/%s; node table_BIGDATA.js %s 2>&1 & " % (path, arg)
	cmd = "cd /home/pi/BIGDATA/; node table_BIGDATA.js %s 2>&1 & " % (arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

# 프로그램 오류 발생 또는 설정 변경후 다시 자신의 프로그램을 다시 시작 한다.
def restart_myself():
	os.execv(sys.executable, [sys.executable] + sys.argv)

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
########################################
########################################

def getImgPath(img_data_dir): 
	## 이벤트 스크린샷을 위한 파일 경로 추출
	# print time.strftime('%Y/%m/%d')
	tmpYear = img_data_dir+time.strftime('%Y/') # 년도 방
	if not os.path.exists(tmpYear): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpYear)
	tmpMonth = tmpYear+time.strftime('%m/') # 월별 방
	if not os.path.exists(tmpMonth): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpMonth)
	tmpDay = tmpMonth+time.strftime('%d/') # 일별 방
	if not os.path.exists(tmpDay): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpDay)
	tmpFullPath = tmpDay+time.strftime('%H/') # 시간별 방
	if not os.path.exists(tmpFullPath): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpFullPath)
	tmpName = time.strftime('%M_%S-URL_01') + ".jpg"
	thisImgName = tmpFullPath + tmpName
	return thisImgName

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
		
########################################
########################################

# socket은 위-모듈에서 선언함 ex: from socket import *
# 참고 : /its_web/utility/socket/server.py and client.py
# 참고 : http://ilab.cs.byu.edu/python/socket/exceptions.html
########################################
def insert_socket_log_BIGDATA(w_s_serial, wr_subject, latS, lngS, latE, lngE, host, port, count, block, status, msg, shot='', video=''): 
	## URL 인코딩
	video = urllib.quote(video)
	# 모니터링을 위한 beep 선언
	if status == 1 or  status == 9: # Active_Event, Error_Event
		beep = 1
	else:
		beep = 0
	# s = None 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data=('id=%s,name=%s,beep=%s,status=%s,shot=%s,video=%s,count=%s,block=%s,msg=%s,latS=%s,lngS=%s,latE=%s,lngE=%s'%(w_s_serial,wr_subject,beep,status,shot,video,count,block,msg,latS,lngS,latE,lngE))
		s.send(msg_data) 
		s.close() 
		return 1 # + msg_data
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 
	
def insert_socket_monitor_BIGDATA(serial, wr_subject, lat_s, lng_s, lat_e, lng_e, ipAddr, myPortIn, dist=0, zone=0): 
	host = ipAddr
	port = myPortIn 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,zone=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, dist, zone))
		node.send(msg_data) 
		node.close() 
		# print msg_data
		return ("Sent %s:%s" % (host, port))
	except socket.error as error:
		print(error)
	except socket.timeout as error:
		print(error)
	finally:
		node.close() 
	
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
		
########################################
########################################

def database_test(db_host, db_user, db_pass, db_name): # BIGDATA
	try:
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		return 1
	except:
		return 0

def create_table_w_log_sensor_BIGDATA(postfix=''): # create_table_w_log_sensor_BIGDATA(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		# 호스트, 사용자, 비밀번호, 데이터베이스 명 your host, usually localhost # your username # your password # name of the database ex: wits
		conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# prepare a cursor object using cursor() method
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		if(postfix):
			postfix = '_' + postfix
		# tbl_w_log_sensor_sql = """
			# CREATE TABLE IF NOT EXISTS %s%s (
			# `w_id` int(11) NOT NULL AUTO_INCREMENT,
			# `w_cfg_id` int(11) NOT NULL DEFAULT '0',
			# `w_eventId` tinyint(4) NOT NULL DEFAULT '0',
			# `w_eventDesc` varchar(32) NULL DEFAULT '',
			# `w_eventValue` float NOT NULL DEFAULT '0',
			# `w_eventStatus` varchar(128) NULL DEFAULT '',
			# `w_opt_0` float NOT NULL DEFAULT '0',
			# `w_opt_1` float NOT NULL DEFAULT '0',
			# `w_opt_2` int(11) NOT NULL DEFAULT '0',
			# `w_opt_3` int(11) NOT NULL DEFAULT '0',
			# `w_opt_4` varchar(32) NULL DEFAULT '',
			# `w_opt_5` varchar(32) NULL DEFAULT '',
			# `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			# PRIMARY KEY (`w_id`)
			# ) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			# """ % (ECOS_sensor_log_table, postfix)
		tbl_w_log_sensor_sql = """
			CREATE TABLE IF NOT EXISTS %s%s (
			`b_id` int(11) NOT NULL AUTO_INCREMENT,
			`b_grp` int(11) NOT NULL DEFAULT '100000000',
			`b_bit_0` bit NULL DEFAULT '0',
			`b_bit_1` bit NULL DEFAULT '0',
			`b_int_0` int NOT NULL DEFAULT '0',
			`b_int_1` int NOT NULL DEFAULT '0',
			`b_flo_0` float NOT NULL DEFAULT '0',
			`b_flo_1` float NOT NULL DEFAULT '0',
			`b_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % (ECOS_sensor_log_table, postfix)

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
		
def insert_event_log_BIGDATA(tableName, w_cfg_id=0, w_eventId=0, w_eventDesc='', w_eventValue=0, w_eventStatus=''): 
	query = "INSERT INTO w_log_sensor_"+tableName+"(w_cfg_id, w_eventId, w_eventDesc, w_eventValue, w_eventStatus) VALUES(%s, %s, %s, %s, %s)"
	args = (w_cfg_id, w_eventId, w_eventDesc, w_eventValue, w_eventStatus)
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

def read_table_w_cfg_sensorID_BIGDATA(): # BIGDATA Port
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_BIGDATA + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
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

def read_table_w_cfg_sensor_BIGDATA(wr_id=''):
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_BIGDATA + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "
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

def read_field_w_cfg_sensor_BIGDATA(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_BIGDATA + " WHERE wr_id = " + wr_id
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
		
def set_reload_w_cfg_sensor_BIGDATA(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "UPDATE " + ECOS_table_prefix + ECOS_table_BIGDATA + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
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
		
def check_scheduledDate_BIGDATA(wr_id=''): # 
	scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	query = "SELECT COUNT(*) as cnt FROM " + ECOS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + ECOS_table_BIGDATA + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
	# return query
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
		
def check_scheduledWeek_BIGDATA(wr_id='', weekNo=''): # Optex Microwave
	# 편의상 2017년 1월 1일 첫째 주 일요일 부터 토요일 까지를 주간 예약 시간표로 사용한다.
	# 예약된 날짜와 요일에 마추어서 현재 시간을 결합해서 검색을 한다.
	# date.weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6. 
	# print ECOS_week_map[weekNo], "ECOS_week_map[weekNo]"
	# scheduledWeek = time.strftime("%Y-%m-%dT%H:%M:%S")
	scheduledWeek = ECOS_week_map[weekNo]+time.strftime("T%H:%M:%S") # 2017-01-01 + 현재시간
	query = "SELECT COUNT(*) as cnt FROM " + ECOS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + ECOS_table_BIGDATA + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
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
			
def make_table_BIGDATA(source, target):
	# __script_jquery_js__ = '%s/jquery/jquery-3.1.1.min.js' % ITS_common_path
	# __script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	# __script_jquery_ui_js__ = '%s/jquery/ui/jquery-ui.js' % ITS_common_path
	# __script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	# __style_jquery_ui_css__ = '%s/jquery/ui/jquery-ui.css' % ITS_common_path
	# __style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	
	# __svg_pan_zoom__ = '%s/svg-pan-zoom/svg-pan-zoom.js' % ITS_common_path
	# __svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'
	__smoothiecharts__ = '%s/smoothiecharts/smoothie.js' % ITS_common_path
	__smoothiecharts__ = '<script>'+open(__smoothiecharts__, 'r').read()+'</script>'

	# print __style_jquery_ui_css__
	with open(source, 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		# tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		# tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		# tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
		# tmp_its_tmp = tmp_its_tmp.replace('__svg_pan_zoom__', __svg_pan_zoom__)
		tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
		
		with open(target, 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()	