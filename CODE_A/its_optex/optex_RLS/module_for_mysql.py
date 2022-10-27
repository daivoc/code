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

table_RLS = c.ECOS_table_prefix+c.ECOS_table_RLS

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
 	except MySQLdb.Warning, warning:
		pass
	finally:
		cursor.close()
		conn.close()
		
def insert_event_RLS(tableName, w_evt_id=0, w_evt_X=0, w_evt_Y=0, w_evt_S=0, w_evt_zone=''): 
	query = "INSERT INTO "+c.ITS_sensor_log_table+"_"+tableName+"(w_evt_id, w_evt_X, w_evt_Y, w_evt_S, w_evt_zone) VALUES(%s, %s, %s, %s, %s)"
	args = (w_evt_id, w_evt_X, w_evt_Y, w_evt_S, w_evt_zone)
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
		
		
def send_event_to_host(host, port, subject, serial, status, shot=''): 
	# 모니터링을 위한 beep 선언
	if status: # Active_Event, Error_Event
		beep = 1
	else:
		beep = 0
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		msg_data = ('id=%s,name=%s,beep=%s,shot=%s,status=%s' % (serial, subject, beep, shot, status))
		s.send(msg_data) 
		s.close() 
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close() 

		
def read_table_w_cfg_sensorID(): ###################### Optex REDSCAN
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

def read_field_w_cfg_status(wr_id=''): 
	query = "SELECT w_sensor_stop, w_sensor_reload, w_sensor_disable, w_alarm_disable FROM " + table_RLS + " WHERE wr_id = " + wr_id
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
		
def set_reload_w_cfg_reload(wr_id=''): 
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

def check_scheduledDate(wr_id=''): # Optex Microwave
	scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	query = "SELECT COUNT(*) as cnt FROM " + c.ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + c.ECOS_table_RLS + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
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
	query = "SELECT COUNT(*) as cnt FROM " + c.ITS_sensor_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + c.ECOS_table_RLS + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
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
