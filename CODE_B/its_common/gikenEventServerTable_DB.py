#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# 네트워크 내의 테일 게이트의 이벤트 취합을 위한 서버측 테이블 생성
import json
# import pymysql
import pymysql
from warnings import filterwarnings
filterwarnings('ignore', category = pymysql.Warning)

def create_table_w_log_giken_server(table): # share['srvHealth']['ip']
	try:
		conn = pymysql.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		tbl_w_log_sensor_sql = """
			CREATE TABLE IF NOT EXISTS %s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_subject` varchar(32) DEFAULT NULL,
			`w_ax_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xa_cnt` int(11) NOT NULL DEFAULT '0',
			`w_bx_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xb_cnt` int(11) NOT NULL DEFAULT '0',
			`w_cx_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xc_cnt` int(11) NOT NULL DEFAULT '0',
			`w_dx_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xd_cnt` int(11) NOT NULL DEFAULT '0',
			`w_approved` int(11) NOT NULL DEFAULT '0',
			`w_unknown` int(11) NOT NULL DEFAULT '0',
			`w_timeout` int(11) NOT NULL DEFAULT '0',
			`w_ymdhm` varchar(12) DEFAULT NULL,
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			`w_serial` int(11) NOT NULL DEFAULT '0',
			PRIMARY KEY (`w_id`)
			) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
			""" % table
		cursor.execute(tbl_w_log_sensor_sql) # create table
		conn.commit()
		return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
 	except pymysql.Warning as warning:
		print(warning)
	finally:
		cursor.close()
		conn.close()

def create_table_w_log_permit_server(table): 
	try:
		conn = pymysql.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		tbl_w_log_sql = """
			CREATE TABLE IF NOT EXISTS %s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_no_image` int(1) NOT NULL DEFAULT '0',
			`w_single` int(1) NOT NULL DEFAULT '0',
			`w_multiple` int(1) NOT NULL DEFAULT '0',
			`w_low_density` int(1) NOT NULL DEFAULT '0',
			`w_anti_denial` int(1) NOT NULL DEFAULT '0',
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			`w_serial` int(11) NOT NULL DEFAULT '0',
			PRIMARY KEY (`w_id`)
			) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
			""" % table
		cursor.execute(tbl_w_log_sql) # create table
		conn.commit()
		return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
 	except pymysql.Warning as warning:
		print(warning)
	finally:
		cursor.close()
		conn.close()

def set_remote_connect(): 
	try:
		conn = pymysql.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		# 외부에서 접근 가능한 사용자 권한 부여
		sql = "GRANT ALL PRIVILEGES ON *.* TO '{}'@'%' IDENTIFIED BY '{}';".format(share['mysql']['user'],share['mysql']['pass'])
		cursor.execute(sql) # create table
		conn.commit()
		return "ALL PRIVILEGES ON"
	except pymysql.Error as error:
		print(error)
 	except pymysql.Warning as warning:
		print(warning)
	finally:
		cursor.close()
		conn.close()

def main():	

	# create_table_w_log_giken_server('w_log_giken_live') # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken_server('w_log_giken_min') # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken_server('w_log_giken_hour') # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken_server('w_log_giken_day') # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken_server('w_log_giken_week') # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken_server('w_log_giken_month') # 센서 시리얼 기준의 테이블 생성
	# create_table_w_log_giken_server('w_log_giken_sum') # 센서 시리얼 기준의 테이블 생성

	# create_table_w_log_permit_server('w_log_permit_live')
	create_table_w_log_permit_server('w_log_permit_min')
	create_table_w_log_permit_server('w_log_permit_hour')
	create_table_w_log_permit_server('w_log_permit_day')
	create_table_w_log_permit_server('w_log_permit_week')
	create_table_w_log_permit_server('w_log_permit_month')

	print("Create table of central DB")

	# 외부에서 접근 가능한 사용자 권한 부여
	print(set_remote_connect())
	print("Change bind-address to 0.0.0.0 in \n/etc/mysql/mariadb.conf.d/50-server.cnf\nRestart Database or Reboot Server.")

if __name__ == '__main__':
	with open("/home/pi/common/config.json") as json_file: # ~/common/config.json
		share = json.load(json_file)
	if(share['mysql']['host']):
		print("Server IP '{}'".format(share['mysql']['host']))
	else:
		exit("server info error!!!")
	main()