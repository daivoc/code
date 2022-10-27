#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import requests
import socket 
import errno
import time

import config_db as c
from config_sensor import *

from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

table_RLS = c.ECOS_table_prefix+c.ECOS_table_PARKING

def database_test(): # Optex Microwave
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		return 1
	except:
		return 0
		
def isTableExist(tableName): ###################### Optex REDSCAN
	query = "SELECT * FROM information_schema.tables WHERE table_schema = '"+c.db_name+"' AND table_name = '"+tableName+"' LIMIT 1;"
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
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

def create_table_w_log_RLS(postfix=''): # create_table_w_log(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		if(postfix):
			tableName = c.ITS_sensor_log_table + '_' + postfix
			if isTableExist(tableName):
				tbl_w_log_sensor_sql = """
					CREATE TABLE IF NOT EXISTS %s (
					`w_id` int(11) NOT NULL AUTO_INCREMENT,
					`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

					`w_rls_md` varchar(4) NULL DEFAULT '', 
					`w_rls_id` varchar(4) NULL DEFAULT '', 
					`w_rls_ma` varchar(4) NULL DEFAULT '', 
					`w_rls_la` varchar(4) NULL DEFAULT '', 
					`w_rls_ca` varchar(4) NULL DEFAULT '', 
					`w_rls_cc` varchar(4) NULL DEFAULT '', 
					`w_rls_dq` varchar(4) NULL DEFAULT '', 
					`w_rls_ar` varchar(4) NULL DEFAULT '', 
					`w_rls_am` varchar(4) NULL DEFAULT '', 
					`w_rls_tr` varchar(4) NULL DEFAULT '', 
					`w_rls_so` varchar(4) NULL DEFAULT '', 
					`w_rls_ta` varchar(4) NULL DEFAULT '', 
					
					`w_rls_dist` int(11) NOT NULL DEFAULT '0',
					`w_rls_size` int(11) NOT NULL DEFAULT '0',
					`w_rls_speed` int(11) NOT NULL DEFAULT '0',

					`w_zone_a1` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_a2` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_b1` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_b2` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_a11` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_a12` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_a21` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_a22` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_b11` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_b12` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_b21` tinyint(1) NOT NULL DEFAULT '0',
					`w_zone_b22` tinyint(1) NOT NULL DEFAULT '0',
					
					`w_event_cnt` int(11) NOT NULL DEFAULT '0',
					`w_event_ignore` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_schedule` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_sent` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_shot` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_error` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_mail` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_alert` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_desc` varchar(128) NULL DEFAULT '',
					
					`w_shot_url` varchar(256) NULL DEFAULT '',
					
					`w_opt_0` float NOT NULL DEFAULT '0',
					`w_opt_1` float NOT NULL DEFAULT '0',
					`w_opt_2` int(11) NOT NULL DEFAULT '0',
					`w_opt_3` int(11) NOT NULL DEFAULT '0',
					`w_opt_4` varchar(32) NULL DEFAULT '',
					`w_opt_5` varchar(32) NULL DEFAULT '',
					PRIMARY KEY (`w_id`)
					) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
					""" % tableName
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
		
def create_table_w_log(postfix=''): # create_table_w_log(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		if(postfix):
			tableName = c.ITS_sensor_log_table + '_' + postfix
			if isTableExist(tableName):
				tbl_w_log_sensor_sql = """
					CREATE TABLE IF NOT EXISTS %s (
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

					`w_event_cnt` int(11) NOT NULL DEFAULT '0',
					`w_event_zeroDist` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_outLevel` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_outCount` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_ignore` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_schedule` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_sent` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_shot` tinyint(1) NOT NULL DEFAULT '0',
					`w_event_error` tinyint(1) NOT NULL DEFAULT '0',
					
					`w_event_stat` varchar(128) NULL DEFAULT '',
					`w_event_desc` varchar(128) NULL DEFAULT '',
					`w_opt_0` float NOT NULL DEFAULT '0',
					`w_opt_1` float NOT NULL DEFAULT '0',
					`w_opt_2` int(11) NOT NULL DEFAULT '0',
					`w_opt_3` int(11) NOT NULL DEFAULT '0',
					`w_opt_4` varchar(32) NULL DEFAULT '',
					`w_opt_5` varchar(32) NULL DEFAULT '',
					PRIMARY KEY (`w_id`)
					) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
					""" % tableName
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
		
# utility > status > status_union.php - home > menu > status
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
		
# 관제실 모니터링 서버로 호스트 및 포트 정보를 통해 자료 전송
def insert_socket_log(serial, wr_subject, lat_s, lng_s, lat_e, lng_e, face, ipAddr, ipPort, cap_max, cap_cur, status, msg): 
	host = ipAddr    # The remote host
	port = ipPort 
	# s = None 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,face=%s,max=%s,current=%s,status=%s,msg=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, face, cap_max, cap_cur, status, msg))
		s.send(msg_data) 
		s.close() 
		return
	except socket.error as error:
		return error
	except socket.timeout:
		return error
	finally:
		s.close() 

# 로컬 실시간 모니터 관제 서비스를 위한 이벤트 전송 
# tablePARKING.js와 연동되어 움직인다.
# ITS 자신의 특정포트(9XXX)를 통한 실시간 관제 home > menu > config > monitor
# utility > nodejs_table > tableSPEED.js
def insert_socket_SIGN_BOARD(serial, wr_subject, ipAddr, myPortIn, cap_max, cap_cur, beep):
	host = ipAddr
	port = myPortIn 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,cap_max=%s,cap_cur=%s, beep=%s' % (serial, wr_subject, cap_max, cap_cur, beep))
		node.send(msg_data) 
		node.close() 
		# print msg_data
		# return ("Sent %s:%s" % (host, port))
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
def insert_socket_monitor(serial, wr_subject, lat_s, lng_s, lat_e, lng_e, ipAddr, myPortIn, ignore, alarmOut, area, zone): 
	host = ipAddr
	port = myPortIn 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((host,port))
		msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,ignore=%s,alarmOut=%s,area=%s,zone=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, ignore, alarmOut, area, zone))
		node.send(msg_data) 
		node.close() 
		# print msg_data
		# return ("Sent %s:%s" % (host, port))
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
	
# 데이타베이스 업데이트
def insert_event_log_RLS(tableName='',w_rls_md='',w_rls_id='',w_rls_ma='',w_rls_la='',w_rls_ca='',w_rls_cc='',w_rls_dq='',w_rls_ar='',w_rls_am='',w_rls_tr='',w_rls_so='',w_rls_ta='',w_rls_dist='0',w_rls_size='0',w_rls_speed='0',w_zone_a1='0',w_zone_a2='0',w_zone_b1='0',w_zone_b2='0',w_zone_a11='0',w_zone_a12='0',w_zone_a21='0',w_zone_a22='0',w_zone_b11='0',w_zone_b12='0',w_zone_b21='0',w_zone_b22='0',w_event_cnt='0',w_event_ignore='0',w_event_schedule='0',w_event_sent='0',w_event_shot='0',w_event_mail='0',w_event_alert='0',w_event_desc='',w_shot_url='',w_opt_0='0',w_opt_1='0',w_opt_2='0',w_opt_3='0',w_opt_4='',w_opt_5=''):
	query = "INSERT INTO "+c.ITS_sensor_log_table+"_"+tableName+"(w_rls_md,w_rls_id,w_rls_ma,w_rls_la,w_rls_ca,w_rls_cc,w_rls_dq,w_rls_ar,w_rls_am,w_rls_tr,w_rls_so,w_rls_ta,w_rls_dist,w_rls_size,w_rls_speed,w_zone_a1,w_zone_a2,w_zone_b1,w_zone_b2,w_zone_a11,w_zone_a12,w_zone_a21,w_zone_a22,w_zone_b11,w_zone_b12,w_zone_b21,w_zone_b22,w_event_cnt,w_event_ignore,w_event_schedule,w_event_sent,w_event_shot,w_event_mail,w_event_alert,w_event_desc,w_shot_url,w_opt_0,w_opt_1,w_opt_2,w_opt_3,w_opt_4,w_opt_5) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (w_rls_md,w_rls_id,w_rls_ma,w_rls_la,w_rls_ca,w_rls_cc,w_rls_dq,w_rls_ar,w_rls_am,w_rls_tr,w_rls_so,w_rls_ta,w_rls_dist,w_rls_size,w_rls_speed,w_zone_a1,w_zone_a2,w_zone_b1,w_zone_b2,w_zone_a11,w_zone_a12,w_zone_a21,w_zone_a22,w_zone_b11,w_zone_b12,w_zone_b21,w_zone_b22,w_event_cnt,w_event_ignore,w_event_schedule,w_event_sent,w_event_shot,w_event_mail,w_event_alert,w_event_desc,w_shot_url,w_opt_0,w_opt_1,w_opt_2,w_opt_3,w_opt_4,w_opt_5)
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
		return 0
	finally:
		cursor.close()
		conn.close()
		
def read_table_w_cfg_sensorID(): ###################### Optex REDSCAN
	# query = "SELECT wr_id, w_sensor_noOfZone, w_virtual_Addr FROM " + table_RLS + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	query = "SELECT * FROM " + table_RLS + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
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

def read_table_w_cfg_sensor_all(wr_id=''): # Optex Microwave
	query = "SELECT * FROM " + table_RLS + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "

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

def read_field_w_cfg_serial(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_sensor_serial FROM " + table_RLS + " WHERE wr_id = " + wr_id
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

def read_field_w_capacity_cur(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_capacity_max, w_capacity_cur FROM " + table_RLS + " WHERE wr_id = " + wr_id
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
		
def read_field_w_cfg_status(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "SELECT w_sensor_stop, w_sensor_reload, w_sensor_disable FROM " + table_RLS + " WHERE wr_id = " + wr_id
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
		
def set_reload_w_cfg_reload(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_sensor_reload(0/1) 값에 따라 동작
	query = "UPDATE " + table_RLS + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
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

def set_update_w_capacity_cur(wr_id='', traceEvent=''):
	# 0 => 'Side In',
	# 1 => 'Side Out'

	query = "UPDATE " + table_RLS + " SET w_capacity_cur = w_capacity_cur + " + str(traceEvent) + " WHERE wr_id = " + wr_id
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		# return cursor.fetchall()
		return cursor.fetchone()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def check_scheduledDate(wr_id=''): # Optex Microwave
	scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	query = "SELECT COUNT(*) as cnt FROM " + c.ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + c.ECOS_table_PARKING + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
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
		
def check_scheduledWeek(wr_id='', weekNo=''): # Optex Microwave
	# 편의상 2017년 1월 1일 첫째 주 일요일 부터 토요일 까지를 주간 예약 시간표로 사용한다.
	# 예약된 날짜와 요일에 마추어서 현재 시간을 결합해서 검색을 한다.
	# date.weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6. 
	# print ECOS_week_map[weekNo], "ECOS_week_map[weekNo]"
	# scheduledWeek = time.strftime("%Y-%m-%dT%H:%M:%S")
	scheduledWeek = ECOS_week_map[weekNo]+time.strftime("T%H:%M:%S") # 2017-01-01 + 현재시간
	query = "SELECT COUNT(*) as cnt FROM " + c.ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + c.ECOS_table_PARKING + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
	# print query
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
