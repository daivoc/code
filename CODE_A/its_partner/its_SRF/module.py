#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import subprocess 
import socket 
import fcntl
import struct
import logging
import logging.handlers
import shutil

from hashlib import sha256

import json
import traceback
import requests
from requests.auth import HTTPDigestAuth

### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
reload(sys)
sys.setdefaultencoding('utf-8')

			
## 환경설정 파일(JSON) 읽기
def readConfig(path='.'):
	with open('%s/config.json'%path) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 읽기
def saveConfig(cfg):
	with open('config.json', 'w') as json_file: ## 저장
		json.dump(cfg, json_file, indent=4)

def check_ping(ip):
	response = os.system("ping -c 1 " + ip)
	# and then check the response...
	if response == 0: ## pingstatus = "Network Active"
		return 1
	else: ## pingstatus = "Network Error"
		return 0

def get_ip_address(ifname): ## get_ip_address('eth0') -> '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def check_opened_port(name):
	ports={'FTP':21,'SSH':22,'SMTP':25,'DNS':53,'HTTP':80,'NNTP':119,'RPC':135,'NetBT':137,'NetBT':138,'NetBT':139,'LDAP':389,'HTTPS':443,'SMB':445,'ISAKMP':500,'CAMERA':554,'SNEWS':563,'RPC':593,'LDAP':636,'IAS':1645,'IAS':1646,'L2TP':1701,'PPTP':1723,'IAS':1812,'IAS':1813,'MGC':3268,'MGC':3269,'RDP':3389,'RLS':50001,'ITS':64446}
	port = ports[name]
	ip_class=get_ip_address('eth0').rsplit('.',1)[0] #eth0,enp2s0
	port_info = []
	
	for ips in range(2,255):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.settimeout(0.01)
		ip='%s.%s'%(ip_class,ips)

		if sock.connect_ex((ip,port)):
			pass
		else:
			# port_info[ip] += "'%s':'%s'"%(name,ip)
			port_info.insert(0, ip)
			
		sock.close()
	return port_info
			
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_its_spotter(id): 
	# cmd = "kill $(ps aux | grep 'spotter.js %s' | awk '{print $2}' | head -n 1)" % id
	cmd = "kill $(ps aux | grep 'spotter.js' | awk '{print $2}' | head -n 1)"
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return p
	
# 확인된 변수로 데몬을 실행 한다
def run_its_spotter(path, id): 
	cmd = "node %s/spotter.js %s 2>&1 & " % (path, id)
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p
	
def detectionList(data, min=0, max=999):
	jData = json.loads(data)
	objResult = len(jData['result'])
	if objResult: ## 결과물이 있을때만 
		resultAll = '' 
		for i in range(objResult):
			if min < jData['result'][i]['stats']['rcs'] < max: ##  rcs Level Check

				resultAll += "\n%s %s "%(jData['result'][i]['frameId'], i) 
			
				## detections.json -> result -> stats
				statsAll = jData['result'][i]['stats']
				for key, value in statsAll.iteritems():
					resultAll += "\n%s:%s,"%(key, value)
				# statsAmplitude = statsAll['amplitude']
				# statsRcs = statsAll['rcs']
				# statsLocalSnr = statsAll['localSnr']
				# statsDopplerMean = statsAll['dopplerMean']
				# statsDopplerVariance = statsAll['dopplerVariance']
				# statsRangeMean = statsAll['rangeMean']
				# statsRangeVariance = statsAll['rangeVariance']
				# statsAngleMean = statsAll['angleMean']
				# statsAngleVariance = statsAll['angleVariance']
				# statsEnergyMean = statsAll['energyMean']
				# statsEnergyVariance = statsAll['energyVariance']
				
				## detections.json -> result -> geolocation
				geoloAll = jData['result'][i]['geolocation']
				for key, value in geoloAll.iteritems():
					resultAll += "\n%s:%s,"%(key, value)
				# geoloLatitude = geoloAll['latitude']
				# geoloLongitude = geoloAll['longitude']
				# geoloAltitude = geoloAll['altitude']
				# geoloAccuracy = geoloAll['accuracy']
				# geoloAltitudeAccuracy = geoloAll['altitudeAccuracy']
				# geoloHeading = geoloAll['heading']
				# geoloBearing = geoloAll['bearing']
				# geoloSpeed = geoloAll['speed']

				## detections.json -> result -> observation
				obserAll = jData['result'][i]['observation']
				for key, value in obserAll.iteritems():
					resultAll += "\n%s:%s,"%(key, value)
				# obserRange = obserAll['range']
				# obserRadialVelocity = obserAll['radialVelocity']
				# obserHorizontalAngle = obserAll['horizontalAngle']
				# obserAzimuthAngle = obserAll['azimuthAngle']
				# obserVerticalAngle = obserAll['verticalAngle']
				# obserAltitudeAngle = obserAll['altitudeAngle']
					
		if resultAll:
			return resultAll
		else:
			return None
	else:
		return None

## curl admin:its_iot@192.168.0.62/api/network.json/settings -X POST -H 'Content-Type: application/json' -d '{ "default": { "enabled": false } }'		
## JSON Http Request
def set_network(sensor_url,payload):
	sensor_url = "%s/api/network.json/settings"%(sensor_url)
		
	try: 
		data_json = json.dumps(payload)
		result = requests.post(sensor_url, data=data_json)
		return result.json() # result.text , result.json(), result.status_code
	except:
		return 0 # "\Error: %s" % sensor_url
	
def set_geolocation(sensor_url,payload):
	sensor_url = "%s/api/geolocation.json/settings"%(sensor_url)
		
	try: 
		data_json = json.dumps(payload)
		result = requests.post(sensor_url, data=data_json)
		return result.json() # result.text , result.json(), result.status_code
	except:
		return 0 # "\Error: %s" % sensor_url

def set_admin_pass(sensor_url):
	sensor_url = "%s/api/auth.json/settings"%(sensor_url)
	payload = { "admin":{ "roles":[ "readData","readSettings","writeSettings","userAdmin" ],"password":"its_iot" } }

	try: 
		data_json = json.dumps(payload)
		result = requests.post(sensor_url, data=data_json)
		return result.json() # result.text , result.json(), result.status_code
	except:
		return 0 # "\Error: %s" % sensor_url

def set_push_tracks(sensor_url,payload):
	sensor_url = "%s/api/tracks.json/subscriptions"%(sensor_url)
	result = ''
	## 현재 등록된 아이템을 읽어들인다.
	jData = requests.get(sensor_url).json()
	if jData:
		if jData['success'] is True:
			for key in jData['result'].keys(): ## 키값을 통해 아이템을 삭제한다.
				data_json = json.dumps(key)
				jDataTmp = requests.delete(sensor_url, data=data_json).json()
				result += "\tDeleted ID:" + key + "\n"
	else: ## 오류 종료
		print ("\tGet Error")
		return 0
			
	## 신규 아이템을 등록 한다.
	data_json = json.dumps(payload)
	jData = requests.post(sensor_url, data=data_json).json()
	if jData:
		if jData['success'] is True:
			result += "\tPosted ID:" + jData['result']['id'] + "\n"
	else: ## 오류 종료
		print ("\tPost Error")
		return 0

	return result

def check_system_license(license, key):
	serial = ''
	f = open('/proc/cpuinfo','r')
	for line in f:
		if line[0:6]=='Serial':
			serial = line[10:26]
	f.close()

	if sha256(serial + key).hexdigest() == license:
		return 1
	else:
		return 0
		
# def set_push_notifications(sensor_url,payload='',request=''):
	# try: 
		# if request is 'post':
			# data_json = json.dumps(payload)
			# result = requests.post(sensor_url, data=data_json) ## payload 는 등록하고자 하는 정보
		# elif request is 'delete':
			# data_json = json.dumps(payload)
			# result = requests.delete(sensor_url, data=data_json) ## payload 는 삭제하고자 하는 정보
		# elif request is 'get':
			# result = requests.get(sensor_url)
		# else:
			# return 0
		# return result.json() # result.text , result.json(), result.status_code
	# except:
		# return 0 #  "\tError: %s" % sensor_url
	
# {"serial":"60169","model":"CK10","version":"3.21.0-01044","userSession":null,"timestamp":947453862142,"errors":[],"warnings":[],"success":true,"result":{"macAddr":"2e:52:46:2a:6f:7b","dns":"8.8.8.8 8.8.4.4","default":{"auto":true,"mode":"static","ipaddr":"169.254.254.254","netmask":"255.255.0.0","gateway":null,"cidr":"16","enabled":true},"userAddrs":[{"auto":true,"mode":"static","ipaddr":"192.168.0.72","netmask":"255.255.255.0","gateway":"192.168.0.1","cidr":"24"}],"user":{"auto":true,"mode":"static","ipaddr":"192.168.0.72","netmask":"255.255.255.0","gateway":"192.168.0.1","cidr":"24"},"dhcp":{"auto":true,"mode":"dhcp","ipaddr":"192.168.0.62","netmask":"255.255.255.0","gateway":"192.168.0.1","cidr":"24","enabled":true,"ipv6Addr":null,"addressType":"ipv4"},"deviceName":"spotter60169","mDns":{"enabled":true}}}


# ### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
# reload(sys)
# sys.setdefaultencoding('utf-8')

# def alertOut(port, druation): # CAM Port No. , Action Due
	# insert_socket_GPWIO(id=port, status=0, msg='')
	# time.sleep(druation)
	# insert_socket_GPWIO(id=port, status=1, msg='')
	# # if(CAM.input(port)):
		# # CAM.output(port, False)
		# # time.sleep(druation)
		# # CAM.output(port, True)
	# # else:
		# # pass

# # def alertOn(port): # CAM Port No. , Action Due
	# # CAM.output(port, False)
# # def alertOff(port): # CAM Port No. , Action Due
	# # CAM.output(port, True)

# # Network Port를 사용하고 있는 프로세서 종료
# def kill_port_CAM(arg): 
	# cmd = "sudo kill -9 `sudo lsof -t -i:%s`" % arg
	# # print cmd
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# # time.sleep(1)

# # 실행하고 있는 'dndmon'란 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
# def kill_demon_CAM(arg): 
	# cmd = "kill $(ps aux | grep 'CAM.pyc %s' | awk '{print $2}')" % arg
	# # print cmd
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# # time.sleep(1)

# # 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
# def kill_demon_CAM_js(arg): 
	# cmd = "kill $(ps aux | grep 'CAM.js %s' | awk '{print $2}')" % arg
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# # time.sleep(1)

# # 확인된 변수로 데몬을 실행 한다
# def run_demon_CAM(arg): 
	# cmd = "python -u -W ignore /home/pi/CAM/CAM.pyc %s 2>&1 & " % arg 
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# # 확인된 변수로 데몬을 실행 한다
# def run_demon_CAM_js(arg): 
	# # path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	# # cmd = "cd /var/www/html/its_web/%s; node CAM.js %s 2>&1 & " % (path, arg)
	# cmd = "cd /home/pi/CAM/; node CAM.js %s 2>&1 & " % (arg)
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# # 원격 카메라 이미지 다운로드
# # ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/wits_%s.jpg  -q -o /dev/null
# def run_wget_image(source, target): 
	# cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (source, target)
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# # 프로그램 오류 발생 또는 설정 변경후 다시 자신의 프로그램을 다시 시작 한다.
# def restart_myself():
	# os.execv(sys.executable, [sys.executable] + sys.argv)

# # 프로그램 오류 발생시 부모프로그램 다시 실행 한다.
# def restart_wits(): 
	# cmd = "python /home/pi/CAM/run_CAM.pyc"
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# # 프로그램 오류 발생시 시스템 다시 시작 한다.
# def reboot_wits():
	# os.system('/sbin/shutdown -r now')

# # 오래된 파일 삭제
# def run_remove_old_file(path, day):
	# if (path and day):
		# cmd = "find %s -type f -ctime %s -exec rm -rf {} \;" % (path, day) # day 이후 모두 삭제
		# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		# cmd = "find %s -type d -empty -delete" % (path)	 # 비어있는 폴더 삭제
		# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
# # 라즈베리 CPU Serial Code
# def get_serial(): # 라즈베리 전용 코드
	# # Extract serial from cpuinfo file
	# cpuserial = "0000000000000000"
	# try:
		# f = open('/proc/cpuinfo','r')
		# for line in f:
			# if line[0:6]=='Serial':
				# cpuserial = line[10:26]
		# f.close()
	# except:
		# cpuserial = "ERROR000000000"
	# return cpuserial

# # 초단위를 시간차이값 형태로 변환 예: 2초 -> 0:00:02.000000
# def conv_sec_2_time(second):
	# return datetime.timedelta(seconds=second)

# # 시간을 초로 반환한다.
# def conv_time_2_sec(times):
	# return times.total_seconds()

# # 화면내용 삭제
# def clear_screen(): # 초기 화면 내용 삭제 
	# subprocess.call('clear',shell=True)
		
# ########################################
# ########################################

# def get_img_n_wmark(host, file, text, enc): 
	# # 이미지 다운로드 후 워터마크 등록
	# if(enc):
		# a = host.rsplit('@',1)[0] # 맨 마지막 @를 기준으로 첫번째 요쇼
		# b = a.split('://',1)[1] # 맨 처음 :// 를 기준으로 두번째요소 선택
		# c = b.split(':',1) # admin:optex59:://@@71!!
		# user = c[0]
		# pwd = c[1]
		# r = requests.get(host, auth=HTTPDigestAuth(user, pwd), stream=True)
	# else:
		# r = requests.get(host, stream=True)
		
	# if r.status_code == 200:
		# with open(file, 'wb') as f:
			# r.raw.decode_content = True
			# shutil.copyfileobj(r.raw, f)
		
		# # 워터마크 등록
		# # 이미지 생성 일시는 카메라자체 시간이 나오도록 
		# try: 
			# image = Image.open(open(file, 'rb'))
			# draw = ImageDraw.Draw(image)
			# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",30)
			# draw.text((900, 1000), text, font=font) # X, Y 해상도에 위치함
			# image.save(file,optimize=True,quality=100)
		# except:
			# return r.status_code, "Downloaded image Format Error %s" % file
			
	# # time.sleep(10) 스레드 테스트
	# return r.status_code, "Snapshot OK"
	
# ## PRESET Http Request
# def insert_get_log_CAM_PRESET(host, enc):
	# try: 
		# if(enc):
			# a = host.rsplit('@',1)[0]
			# b = a.split('://',1)[1]
			# c = b.split(':',1) # admin:optex59:://@@71!!
			# user = c[0]
			# pwd = c[1]
			# result = requests.get(host, auth=HTTPDigestAuth(user, pwd))
		# else:
			# result = requests.get(host, timeout=0.1)
		# return result.status_code # result.text , result.json(), result.status_code
	# except requests.exceptions.Timeout:
		# return "Timeout  %s" % host
	# except:
		# return "requests.get Error: %s" % host

# ## JSON Http Request
# ## https://stackoverflow.com/questions/9733638/post-json-using-python-requests
# def insert_post_log_CAM_JSON(host):
	# data = """ { "Key":"id", "Value":"value" } """
	# try: 
		# data_json = json.dumps(data)
		# result = requests.post(host, json=data_json)
		# return result.json() # result.text , result.json(), result.status_code
	# except:
		# return "requests.post Error: %s" % host
		
# def insert_url_CAM_GET(host):
	# try: 
		# result = requests.get(host, timeout=0.1)
		# return result.status_code # result.text , result.json(), result.status_code
	# except requests.exceptions.Timeout:
		# return "Timeout  %s" % host
	# except:
		# return "requests.get Error: %s" % host
		
# def insert_alarm_log_CAM(w_camera_serial, wr_subject, w_camera_lat_s, w_camera_lng_s, w_camera_lat_e, w_camera_lng_e, w_system_ip, db_table_CAM, currentDist, alarmEventCnt, url): 
	# payload = {'id':w_camera_serial, 'name':wr_subject, 'lat_s':w_camera_lat_s, 'lng_s':w_camera_lng_s, 'lat_e':w_camera_lat_e, 'lng_e':w_camera_lng_e, 'wits_ip':w_system_ip, 'table':db_table_CAM, 'zone':currentDist, 'cont':alarmEventCnt}
	# try:
		# # r = requests.get(url, params=payload)
		# r = requests.post(url, data=payload)
		# if r.status_code == 200:
			# msg = 200
	# except:
		# msg = 0
	# finally:
		# return msg
		
# ########################################
# ########################################

# # socket은 위-모듈에서 선언함 ex: from socket import *
# # 참고 : /its_web/utility/socket/server.py and client.py
# # 참고 : http://ilab.cs.byu.edu/python/socket/exceptions.html
# ########################################
# def insert_socket_log_CAM(w_s_serial, wr_subject, latS, lngS, latE, lngE, host, port, count, block, status, msg, shot=''): 
	# # 모니터링을 위한 beep 선언
	# if status == 1 or  status == 9: # Active_Event, Error_Event
		# beep = 1
	# else:
		# beep = 0
	# # s = None 
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	# try: 
		# s.connect((host,port))
		# msg_data=('id=%s,name=%s,beep=%s,shot=%s,latS=%s,lngS=%s,latE=%s,lngE=%s,count=%s,block=%s,status=%s,msg=%s'%(w_s_serial,wr_subject,beep,shot,latS,lngS,latE,lngE,count,block,status,msg))
		# s.send(msg_data) 
		# s.close() 
		# return 1 # + msg_data
	# except socket.error:
		# return 0
	# except socket.timeout:
		# return 0
	# finally:
		# s.close() 
	
# def insert_socket_spotter_CAM(serial, wr_subject, lat_s, lng_s, lat_e, lng_e, ipAddr, myPortIn, dist=0, zone=0): 
	# host = ipAddr
	# port = myPortIn 
	# node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# try: 
		# node.connect((host,port))
		# msg_data = ('id=%s,name=%s,lat_s=%s,lng_s=%s,lat_e=%s,lng_e=%s,dist=%s,zone=%s' % (serial, wr_subject, lat_s, lng_s, lat_e, lng_e, dist, zone))
		# node.send(msg_data) 
		# node.close() 
		# # print msg_data
		# return ("Sent %s:%s" % (host, port))
	# except socket.error as error:
		# print(error)
	# except socket.timeout as error:
		# print(error)
	# finally:
		# node.close() 
	
# def insert_socket_status_UNION(serial, name, ip, port, model, board, tableID, status, msg): 
	# node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# try: 
		# node.connect((ip,port))
		# msg_data = ('id=%s,name=%s,ip=%s,model=%s,board=%s,tableID=%s,status=%s,msg=%s' % (serial, name, ip, model, board, tableID, status, msg))
		# node.send(msg_data) 
		# node.close() 
		# return ("status_msg")
	# except socket.error:
		# return 0
	# except socket.timeout:
		# return 0
	# finally:
		# node.close() 

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
		
# ########################################
# ########################################

# def database_test(): # CAM
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# return 1
	# except:
		# return 0

# def create_table_w_log_camera_CAM(postfix=''): # create_table_w_log_camera_CAM(uniqueOfSensor)
	# try:
		# # 데이타베이스 테이블 생성
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor()
		# if(postfix):
			# postfix = '_' + postfix
		# tbl_w_log_camera_sql = """
			# CREATE TABLE IF NOT EXISTS %s%s (
			# `w_id` int(11) NOT NULL AUTO_INCREMENT,
			# `w_from` varchar(32) NULL DEFAULT '',
			# `w_query` varchar(64) NULL DEFAULT '',
			# `w_pan` float NOT NULL DEFAULT '0',
			# `w_tilt` float NOT NULL DEFAULT '0',
			# `w_zoom` float NOT NULL DEFAULT '0',
			# `w_focus` float NOT NULL DEFAULT '0',
			# `w_iris` float NOT NULL DEFAULT '0',
			# `w_brightness` float NOT NULL DEFAULT '0',
			# `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			# PRIMARY KEY (`w_id`)
			# ) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			# """ % (ECOS_camera_log_table, postfix)
		# # print tbl_w_log_camera_sql
		# cursor.execute(tbl_w_log_camera_sql) # create table
		# conn.commit()
		# return cursor.lastrowid
	# except MySQLdb.Error as error:
		# print(error)
 	# except MySQLdb.Warning, warning:
		# pass
	# finally:
		# cursor.close()
		# conn.close()
		
# def insert_event_log_CAM(postfix, w_from, w_query, w_pan, w_tilt, w_zoom, w_focus, w_iris, w_brightness): 
	# query = "INSERT INTO "+ECOS_camera_log_table+"_"+postfix+"(w_from, w_query, w_pan, w_tilt, w_zoom, w_focus, w_iris, w_brightness) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
	# args = (w_from, w_query, w_pan, w_tilt, w_zoom, w_focus, w_iris, w_brightness)
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor()
		# cursor.execute(query, args)
		# conn.commit()
		# return cursor.lastrowid
	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()

# def read_table_w_cfg_cameraID_CAM(): # CAM Port
	# query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_CAM + " WHERE w_camera_disable = 0" + " ORDER BY wr_id DESC" 
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# return cursor.fetchall()

	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()

# def read_table_w_cfg_camera_CAM(wr_id=''):
	# query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_CAM + " WHERE wr_id = " + wr_id + " AND w_camera_disable = 0 "
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# return cursor.fetchall()
	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()

# def read_field_w_cfg_camera_CAM(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	# query = "SELECT * FROM " + ECOS_table_prefix + ECOS_table_CAM + " WHERE wr_id = " + wr_id
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# return cursor.fetchall()
	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()
		
# def set_reload_w_cfg_camera_CAM(wr_id=''): # 일시적으로 이벤트 전송을 중지 하기 위한 기능으로 w_instant_stop(0/1) 값에 따라 동작
	# query = "UPDATE " + ECOS_table_prefix + ECOS_table_CAM + " SET w_camera_reload = '0' WHERE wr_id = " + wr_id
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# return cursor.fetchall()
	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()
		
# def check_scheduledDate_CAM(wr_id=''): # 
	# scheduledDate = time.strftime("%Y-%m-%dT%H:%M:%S")
	# query = "SELECT COUNT(*) as cnt FROM " + ECOS_camera_blk_table + " WHERE wr_id = " + wr_id + " AND bo_table = '" + ECOS_table_CAM + "' AND startdate < '" + scheduledDate + "' AND enddate > '" + scheduledDate + "'"
	# # return query
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# result = cursor.fetchone()
		# return result

	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()
		
# def check_scheduledWeek_CAM(wr_id='', weekNo=''): # Optex Microwave
	# # 편의상 2017년 1월 1일 첫째 주 일요일 부터 토요일 까지를 주간 예약 시간표로 사용한다.
	# # 예약된 날짜와 요일에 마추어서 현재 시간을 결합해서 검색을 한다.
	# # date.weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6. 
	# # print ECOS_week_map[weekNo], "ECOS_week_map[weekNo]"
	# # scheduledWeek = time.strftime("%Y-%m-%dT%H:%M:%S")
	# scheduledWeek = ECOS_week_map[weekNo]+time.strftime("T%H:%M:%S") # 2017-01-01 + 현재시간
	# query = "SELECT COUNT(*) as cnt FROM " + ECOS_camera_blk_table + " WHERE wr_id = " + wr_id + " AND w_week = 1 AND bo_table = '" + ECOS_table_CAM + "' AND startdate < '" + scheduledWeek + "' AND enddate > '" + scheduledWeek + "'"
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# result = cursor.fetchone()
		# return result

	# except MySQLdb.Error as error:
		# print(error)
	# finally:
		# cursor.close()
		# conn.close()
			
# def itsMemberConfig(field): # table
	# cursor = None
	# conn = None
	# query = "SELECT " + field + " FROM g5_member WHERE mb_id = 'manager'" 
	# # mb_4 - system ip address
	# try:
		# conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute(query)
		# return cursor.fetchone() # 커서의 fetchall()는 모두, fetchone()은 하나의 Row, fetchone(n)은 n개 만큼
	# except MySQLdb.Error as error:
		# return 0
	# finally:
		# if cursor:
			# cursor.close()
		# if conn:
			# conn.close()
		
# ########################################
# ########################################
			
