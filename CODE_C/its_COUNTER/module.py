#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import MySQLdb
import subprocess 
import time
import sys
import os
import socket 
import datetime

import RPi.GPIO as GPIO
import config as c
import logging
import logging.handlers

from collections import deque

# from module_for_COUNTER import *
# from module_for_mysql import *

from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

table_COUNTER = c.ECOS_table_prefix+c.ECOS_table_COUNTER

################ Database
def database_test(): # COUNTER
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		return 1
	except:
		return 0
def read_table_w_cfg_sensorID_COUNTER(): # COUNTER Port
	cmd = "SELECT * FROM " + table_COUNTER + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	# print cmd
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(cmd)
		return cursor.fetchall()

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_sensor_COUNTER(wr_id=''):
	cmd = "SELECT * FROM " + table_COUNTER + " WHERE wr_id = " + wr_id + " AND w_sensor_disable = 0 "
	# print cmd
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(cmd)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()
				
def set_reload_w_cfg_sensor_COUNTER(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	query = "UPDATE " + table_COUNTER + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
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
		
def create_table_w_log_sensor_COUNTER(postfix=''): # create_table_w_log_sensor_COUNTER(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		# 호스트, 사용자, 비밀번호, 데이터베이스 명 your host, usually localhost # your username # your password # name of the database ex: its
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		# prepare a cursor object using cursor() method
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		if(postfix):
			postfix = '_' + postfix

		cmd = """
			CREATE TABLE IF NOT EXISTS %s%s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_status` int(11) NOT NULL DEFAULT '0',
			`w_msg` varchar(16) DEFAULT NULL,
			`w_year` int(11) NOT NULL DEFAULT '0',
			`w_month` int(11) NOT NULL DEFAULT '0',
			`w_week` int(11) NOT NULL DEFAULT '0',
			`w_day` int(11) NOT NULL DEFAULT '0',
			`w_hour` int(11) NOT NULL DEFAULT '0',
			`w_min` int(11) NOT NULL DEFAULT '0',
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (`w_id`)
			) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
			""" % (c.ITS_sensor_log_table, postfix)
		# print cmd
		cursor.execute(cmd) # create table
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
 	except MySQLdb.Warning, warning:
		pass
	finally:
		cursor.close()
		conn.close()

def insert_event_log_COUNTER(tableName, status, msg):
	# time.struct_time(tm_year=2015, tm_mon=4, tm_mday=19, tm_hour=13, tm_min=21, tm_sec=40, tm_wday=6, tm_yday=109, tm_isdst=-1)
	now = datetime.datetime.now()
	t = now.timetuple()
	cmd = "INSERT INTO "+c.ITS_sensor_log_table+"_"+tableName+"(w_status, w_msg, w_year, w_month, w_week, w_day, w_hour, w_min) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
	args = (status, msg, t.tm_year, t.tm_mon, t.tm_wday, t.tm_mday, t.tm_hour, t.tm_min)
	# print cmd
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(cmd, args)
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

########################################
## 참고 : http://ilab.cs.byu.edu/python/socket/exceptions.html
########################################
def insert_socket_monitor_COUNTER(ip, port, serial, subject, dirStat, valueIs, eventOn): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((ip,port))
		msg_data = ('ip=%s,serial=%s,subject=%s,dirStat=%s,valueIs=%s,eventOn=%s' % (ip, serial, subject, dirStat, valueIs, eventOn))
		node.send(msg_data) 
		node.close() 
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
		
def insert_socket_for_IMS(host, port, id, name, beep=0, latS=0, lngS=0, latE=0, lngE=0, shot='', msg=''): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	node.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		node.connect((host,port))
		msg_data=('id=%s,name=%s,beep=%s,shot=%s,latS=%s,lngS=%s,latE=%s,lngE=%s,msg=%s'%(id,name,beep,shot,latS,lngS,latE,lngE,msg))
		node.send(msg_data) 
		node.close() 
		return 1 # + msg_data
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 


################ GPIO  - Sensor for SR04T
def initPortGPIO(GPIO_TRIG, GPIO_ECHO):
	GPIO.setwarnings(False) # Disable warnings
	GPIO.setmode(GPIO.BCM) # We will be using the BCM GPIO numbering
	GPIO.setup(GPIO_TRIG,GPIO.OUT) # Select which GPIOs you will use, Set TRIGGER to OUTPUT mode
	GPIO.setup(GPIO_ECHO,GPIO.IN) # Set ECHO to INPUT mode
	GPIO.output(GPIO_TRIG, False) # Set TRIGGER to LOW
	time.sleep(0.5) # Let the sensor settle for a while

def getEventGPIO(GPIO_TRIG, GPIO_ECHO):
	GPIO.output(GPIO_TRIG, True) # set TRIGGER to HIGH
	time.sleep(0.00001) # Send 10 microsecond pulse to TRIGGER and wait 10 microseconds
	GPIO.output(GPIO_TRIG, False) # set TRIGGER back to LOW
	start = time.time() # Create variable start and give it current time
	stop = start # Create variable start and give it current time
	while GPIO.input(GPIO_ECHO)==0: # Refresh start value until the ECHO goes HIGH = until the wave is send
		start = time.time()
	while GPIO.input(GPIO_ECHO)==1: # Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW
		stop = time.time()
	measuredTime = stop - start # Calculate the time it took the wave to travel there and back
	distanceBothWays = measuredTime * 33112 # # Calculate the travel distance by multiplying the measured time by speed of sound - cm/s in 20 degrees Celsius
	distance = int(distanceBothWays / 2) # Divide the distance by 2 to get the actual distance from sensor to obstacle, distance = distanceBothWays / 2
	return distance

################ Kill and Run
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_COUNTER_table(): 
	cmd = "kill $(ps aux | grep '[n]ode table_COUNTER.js' | awk '{print $2}')"
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

# 확인된 변수로 데몬을 실행 한다
def run_demon_COUNTER_table(arg): 
	# path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	# cmd = "cd /var/www/html/its_web/%s; node table_COUNTER.js %s 2>&1 & " % (path, arg)
	cmd = "node table_COUNTER.js %s %s 2>&1 & " % (arg, c.ITS_M_map_target)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 실행하고 있는 'dndmon'란 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_COUNTER(): 
	cmd = "kill $(ps aux | grep '[p]ython -u -W ignore /home/pi/COUNTER/COUNTER.pyc' | awk '{print $2}')"
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)	
	
# 확인된 변수로 데몬을 실행 한다
def run_COUNTER(arg): 
	cmd = "python -u -W ignore /home/pi/COUNTER/COUNTER.pyc %s 2>&1 & " % arg 
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
# 프로그램 오류 발생 또는 설정 변경후 다시 자신의 프로그램을 다시 시작 한다.
def restart_myself():
	os.execv(sys.executable, [sys.executable] + sys.argv)

# 프로그램 오류 발생시 시스템 다시 시작 한다.
def reboot_its():
	os.system('/sbin/shutdown -r now')

################ 오래된 파일 삭제
def run_remove_old_file(path, day):
	if (path and day):
		cmd = "find %s -type f -ctime %s -exec rm -rf {} \;" % (path, day) # day 이후 모두 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		cmd = "find %s -type d -empty -delete" % (path)	 # 비어있는 폴더 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

################ 이벤트 스크린샷
# ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/wits_%s.jpg  -q -o /dev/null
def getSnapshot(imagePath,targetPath): 
	# print time.strftime('%Y/%m/%d')
	tmpYear = targetPath+time.strftime('%Y/') # 년도 방
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
	cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (imagePath, thisImgName)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
	return thisImgName

################ 모니터링을 위한 지도파일을 생성한다.
def make_its_M_map(minDist,maxDist,limitDist_S,limitDist_E):
	__script_jquery_js__ = '%s/jquery/jquery-3.1.1.min.js' % c.ITS_common_path
	__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	__script_jquery_ui_js__ = '%s/jquery/ui/jquery-ui.js' % c.ITS_common_path
	__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	__style_jquery_ui_css__ = '%s/jquery/ui/jquery-ui.css' % c.ITS_common_path
	__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	__smoothiecharts__ = '%s/smoothiecharts/smoothie.js' % c.ITS_common_path
	__smoothiecharts__ = '<script>'+open(__smoothiecharts__, 'r').read()+'</script>'
	
	__COUNTER_minDist__ = str(minDist / 10)
	__COUNTER_maxDist__ = str(maxDist / 10)
	__COUNTER_limitDist_S__ = str(limitDist_S / 10)
	__COUNTER_limitDist_E__ = str(limitDist_E / 10)
	# print __COUNTER_minDist__,__COUNTER_maxDist__,__COUNTER_limitDist__
	# print __style_jquery_ui_css__
	with open(c.ITS_M_map_source, 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
		tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__COUNTER_minDist__', __COUNTER_minDist__)
		tmp_its_tmp = tmp_its_tmp.replace('__COUNTER_maxDist__', __COUNTER_maxDist__)
		tmp_its_tmp = tmp_its_tmp.replace('__COUNTER_limitDist_S__', __COUNTER_limitDist_S__)
		tmp_its_tmp = tmp_its_tmp.replace('__COUNTER_limitDist_E__', __COUNTER_limitDist_E__)
		
		with open(c.ITS_M_map_target, 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()