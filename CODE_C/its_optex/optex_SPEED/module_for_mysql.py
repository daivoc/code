#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import config_db as c
import requests
import socket 
import errno
import time
import binascii

from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

table_SPEED = c.ECOS_table_prefix+c.ECOS_table_SPEED

def database_test(): # Optex Microwave
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		return 1
	except:
		return 0
	
def create_table_w_log_BSS(postfix=''): # create_table_w_log_BSS(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
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
			""" % (c.ITS_sensor_log_table, postfix)
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
		
def insert_socket_log_BSS_SPEED(BSS_sensor_serial, BSS_subject, BSS_host_Addr, BSS_host_Port, tmp_speed, eventOverSpeed, tmp_imageURL='', lightLV=''):
	host = BSS_host_Addr    # The remote host
	port = BSS_host_Port 
	# s = None 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		# msg_data = ('id=%s,name=%s,Speed=%s,SpeedOver=%s,Image=%s' % (BSS_sensor_serial, BSS_subject, tmp_speed, eventOverSpeed, tmp_imageURL))
		msg_data = ('id=%s,name=%s,Speed=%s,SpeedOver=%s,Image=%s,beep=%s,lightLV=%s' % (BSS_sensor_serial, BSS_subject, tmp_speed, eventOverSpeed, tmp_imageURL, eventOverSpeed,lightLV))
		s.send(msg_data) 
		print msg_data
		s.close() 
		return ("Sent %s:%s" % (host, port))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 

def insert_socket_log_BSS_SPEED_bin(BSS_host_Addr, BSS_host_Port, tmp_speed, eventOverSpeed):
	host = BSS_host_Addr    # The remote host
	port = BSS_host_Port 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		# 전광판 데이터 전송
		if (eventOverSpeed): 
			tmp_color = 0b100
			tmp_image = 0x02
		else:
			tmp_color = 0b010
			tmp_image = 0x01
		tmp_bright = 0xff
		tmp_hold = 0x00
			
		list_of_tmp = [0x02, 0x00, 0x0c, 0x53, 0x80, tmp_speed, tmp_color, tmp_image, tmp_bright, tmp_hold]
		xorCheck = reduce(lambda i, j: int(i) ^ int(j), list_of_tmp) # 리스트 전체를 XOR			
		list_of_values = '02000c5380%s%s%s%s%s%s03'%(format(tmp_speed, '02x'), format(tmp_color, '02x'), format(tmp_image, '02x'), format(tmp_bright, '02x'), format(tmp_hold, '02x'), format(xorCheck, '02x')) #  format(10, '02x') -> 0a
		# msg_data = binascii.a2b_hex('48656c6c6f20576f726c6421')
		msg_data = binascii.a2b_hex(list_of_values)
		
		# print msg_data
		s.send(msg_data) 
		s.close() 
		return ("Sent %s:%s" % (host, port))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 
		
def insert_socket_log_BSS_OBJ(serial='', wr_subject='', lat_s='', lng_s='', lat_e='', lng_e='', face='', ipAddr='', ipPort='', dist='', zone='', obj_length='', obj_time='', obj_speed='', obj_move='', obj_level=''):
	host = ipAddr    # The remote host
	port = ipPort 
	# s = None 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,face=%s,dist=%s,zone=%s,obj_length=%s,obj_time=%s,obj_speed=%s,obj_move=%s,obj_level=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, face, dist, zone, obj_length, obj_time, obj_speed, obj_move, obj_level))
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
		
def insert_socket_alert_BSS(serial, wr_subject, ipAddr, ipPort): 
	host = ipAddr    # The remote host
	port = ipPort 
	# s = None 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,zone=%s' % (serial, wr_subject, -1, -1, -1, -1, -1, -1))
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

def insert_socket_monitor_BSS(serial, wr_subject, lat_s, lng_s, lat_e, lng_e, ipAddr, myPortIn, dist, alarmOut, sensorType, zone): 
	host = ipAddr
	port = myPortIn 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,alarmOut=%s,sensorType=%s,zone=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, sensorType, zone))
		node.send(msg_data) 
		node.close() 
		# print msg_data, ipAddr, myPortIn
		return ("Sent %s:%s" % (host, port))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 

def insert_socket_monitor_BSS_OBJ(serial='', wr_subject='', lat_s='', lng_s='', lat_e='', lng_e='', ipAddr='', myPortIn='', dist='', alarmOut='', sensorType='', zone='', obj_overSp='', obj_time='', obj_speed='', obj_move='', obj_level=''): 
	host = ipAddr
	port = myPortIn 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,alarmOut=%s,sensorType=%s,zone=%s,length=%s,time=%s,speed=%s,move=%s,level=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, sensorType, zone, obj_overSp, obj_time, obj_speed, obj_move, obj_level))
		node.send(msg_data) 
		node.close() 
		# print msg_data, ipAddr, myPortIn
		return ("Sent %s:%s" % (host, port))
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
def insert_event_log_BSS(tableName, w_cfg_id=0, w_bss_slave='', w_bss_device='', w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='', w_bss_type='', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='', w_event_desc='', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5=''): 
	query = "INSERT INTO "+c.ITS_sensor_log_table+"_"+tableName+"(w_cfg_id, w_bss_slave, w_bss_device, w_bss_distent, w_bss_error, w_bss_level, w_bss_alarm, w_bss_type, w_bss_speed, w_event_cnt, w_event_zeroDist, w_event_outLevel, w_event_outCount, w_event_ignore, w_event_schedule, w_event_sent, w_event_shot, w_event_error, w_event_stat, w_event_desc, w_opt_0, w_opt_1, w_opt_2, w_opt_3, w_opt_4, w_opt_5) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	args = (w_cfg_id, w_bss_slave, w_bss_device, w_bss_distent, w_bss_error, w_bss_level, w_bss_alarm, w_bss_type, w_bss_speed, w_event_cnt, w_event_zeroDist, w_event_outLevel, w_event_outCount, w_event_ignore, w_event_schedule, w_event_sent, w_event_shot, w_event_error, w_event_stat, w_event_desc, w_opt_0, w_opt_1, w_opt_2, w_opt_3, w_opt_4, w_opt_5)
	# print query
	# print args
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
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
	# query = "SELECT wr_id, w_sensor_noOfZone, w_virtual_Addr FROM " + table_SPEED + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	query = "SELECT * FROM " + table_SPEED + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_sensor_BSS(wr_id=''): # Optex Microwave
	query = "SELECT * FROM " + table_SPEED + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "

	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_field_w_cfg_serial_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_sensor_serial FROM " + table_SPEED + " WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_field_w_cfg_status_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_sensor_stop, w_sensor_reload, w_alarm_disable FROM " + table_SPEED + " WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_field_w_cfg_setup_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	# query = "SELECT w_sensor_ignoreZone, w_sensor_scheduleS, w_sensor_scheduleE, w_event_holdTime, w_event_pickTime FROM " + table_SPEED + " WHERE wr_id = " + wr_id
	query = "SELECT * FROM " + table_SPEED + " WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()


		
def set_reload_w_cfg_reload_BSS(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_sensor_reload(0/1) 값에 따라 동작
	query = "UPDATE " + table_SPEED + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
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
	query = "SELECT COUNT(*) as cnt FROM " + c.ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + c.ECOS_table_SPEED + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
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
	scheduledWeek = c.ECOS_week_map[weekNo]+time.strftime("T%H:%M:%S") # 2017-01-01 + 현재시간
	query = "SELECT COUNT(*) as cnt FROM " + c.ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + c.ECOS_table_SPEED + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		return result

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
