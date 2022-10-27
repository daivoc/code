#!/usr/bin/env python
# -*- coding: utf-8 -*-  

'''
사용법
프로그램 내에서 아래의 기능을 실행 한다.

def insert_socket_GPWIO(id, status, msg): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		# node.connect((ip,port))
		node.connect(('localhost', share["port"]["gpwio"]["portIn"]))
		msg_data = ('id=%s,status=%s,msg=%s' % (id, status, msg))
		node.send(msg_data) 
		node.close() 
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 
'''

import time
import MySQLdb
import subprocess 
import json
# from config import *

# 모니터링을 위한 지도파일을 생성한다.
def make_GPWIO_map():
	jquery = '%s/jquery/jquery-3.1.1.min.js' % share["path"]["common"]
	__script_jquery_js__ = '<script>'+open(jquery, 'r').read()+'</script>'

	bootstrap_js = '%s/bootstrap/js/bootstrap.min.js' % share["path"]["common"]
	__style_bootstrap_js__ = '<script>'+open(bootstrap_js, 'r').read()+'</script>'
	bootstrap_css = '%s/bootstrap/css/bootstrap.min.css' % share["path"]["common"]
	__style_bootstrap_css__ = '<style>'+open(bootstrap_css, 'r').read()+'</style>'
	
	bootstrap_toggle_js = '%s/bootstrap/js/bootstrap-toggle.min.js' % share["path"]["common"]
	__style_bootstrap_toggle_js__ = '<script>'+open(bootstrap_toggle_js, 'r').read()+'</script>'
	bootstrap_toggle_css = '%s/bootstrap/css/bootstrap-toggle.min.css' % share["path"]["common"]
	__style_bootstrap_toggle_css__ = '<style>'+open(bootstrap_toggle_css, 'r').read()+'</style>'
	
	with open(owner["file"]["html_source"], 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_js__', __style_bootstrap_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css__', __style_bootstrap_css__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_toggle_js__', __style_bootstrap_toggle_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_toggle_css__', __style_bootstrap_toggle_css__)
		
		with open(owner["file"]["html_target"], 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()

def itsMemberConfig(id, field): # table
	cursor = None
	conn = None
	query = "SELECT " + field + " FROM g5_member WHERE mb_id = '" + id + "'" 
	try:
		conn = MySQLdb.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
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

def read_table_w_cfg_gpwio(): ##
	query = "SELECT * FROM " + share["table"]["gpwio"] + " WHERE w_gpwio_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_gpio(): ##
	query = "SELECT * FROM " + share["table"]["gpio"] + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_GPWIO(): 
	# cmd = "kill $(ps aux | grep 'node GPACU.js' | awk '{print $2}')"
	cmd = "kill $(ps aux | grep 'node GP[AW][CI][UO].js' | awk '{print $2}')"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_GPWIO"
	
def run_demon_GPWIO(): 
	cmd = "cd %s; node GPWIO.js 2>&1 & "
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_GPWIO"
	
## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def requestParse(content):
	## content = 'root||password||http://host/command?option=id||1'
	try:
		elements = content.split('||') 
		requestInfo = {
				'user':elements[0],
				'pass':elements[1],
				'url':elements[2],
				'enc':int(elements[3])
			}
		return requestInfo
	except:
		# return "requests.get Error: %s" % url
		return 0
		
def ipPortParse(content):
	## content = 'root||password||192.168.0.10||1234||Opt1||Opt2'
	try:
		elements = content.split('||') 
		connectInfo = {
				'user':elements[0],
				'pass':elements[1],
				'host':elements[2],
				'port':int(elements[3]),
				'opt1':elements[4],
				'opt2':elements[5]
			}
		return connectInfo
	except:
		# return "requests.get Error: %s" % url
		return 0
	
if __name__ == '__main__':
	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print share["file"]["html_src"]
	## 예: print share["mysql"]["db_host"]
	share = readConfig('/home/pi/common/config.json')

	ioB = str(itsMemberConfig('its','mb_4')['mb_4']).strip() # 인터페이스 IO 보드 확인 ITS/ACU
	# print(ioB.upper())
	if ioB == "acu":
		print("ITS ACU can't take GPWIO. Check Config..")
		exit()
	else:
		pass

	owner = readConfig('/home/pi/GPWIO/config.json') 
	owner['status'] = share['status'].copy()
	owner['file'] = {}
	owner['file']['html_source'] = "/home/pi/GPWIO/GPWIO.html"
	owner['file']['html_target'] = "/home/pi/GPWIO/index.html"
	owner['interface'] = {}
	owner['interface']['portIn'] = share['port']['gpwio']['portIn']
	owner['interface']['portOut'] = share['port']['gpwio']['portOut']

	## GPWIO 정보 수집
	owner['cover'] = {}
	owner['group'] = {}
	for row in read_table_w_cfg_gpwio():
		owner['cover'][row['w_gpwio_cover']] = row['w_gpwio_group']
		owner['group'][row['w_gpwio_group']] = {}
		owner['group'][row['w_gpwio_group']]['name'] = row['wr_subject']
		owner['group'][row['w_gpwio_group']]['status'] = row['w_gpwio_status']
		owner['group'][row['w_gpwio_group']]['alertP'] = row['w_alert_Port']
		owner['group'][row['w_gpwio_group']]['alertV'] = row['w_alert_Value']
		owner['group'][row['w_gpwio_group']]['addr1'] = row['w_host_Addr1']
		owner['group'][row['w_gpwio_group']]['port1'] = row['w_host_Port1']
		owner['group'][row['w_gpwio_group']]['addr2'] = row['w_host_Addr2']
		owner['group'][row['w_gpwio_group']]['port2'] = row['w_host_Port2']
		owner['group'][row['w_gpwio_group']]['gpwio'] = row['w_gpwio_serial']
		owner['group'][row['w_gpwio_group']]['sensor'] = row['w_sensor_serial']
		
		## 모니터링 시스템으로 이벤트 정보 전송(IP, Port)
		owner['group'][row['w_gpwio_group']]['monitoringIpPort'] = []
		if row['w_host_Addr1'] and row['w_host_Port1']:
			owner['group'][row['w_gpwio_group']]['monitoringIpPort'].append({ "addr":row['w_host_Addr1'], "port":row['w_host_Port1'] })
		if row['w_host_Addr2'] and row['w_host_Port2']:
			owner['group'][row['w_gpwio_group']]['monitoringIpPort'].append({ "addr":row['w_host_Addr2'], "port":row['w_host_Port2'] })
		
		## Target URL에 이벤트에 따른 Request 전송(user, password, url, htmldigest)
		owner['group'][row['w_gpwio_group']]['customRequest'] = []
		newRequest = requestParse(row['wr_4'])
		if newRequest: owner['group'][row['w_gpwio_group']]['customRequest'].append(newRequest)
		newRequest = requestParse(row['wr_5'])
		if newRequest: owner['group'][row['w_gpwio_group']]['customRequest'].append(newRequest)
		newRequest = requestParse(row['wr_6'])
		if newRequest: owner['group'][row['w_gpwio_group']]['customRequest'].append(newRequest)
		newRequest = requestParse(row['wr_7'])
		if newRequest: owner['group'][row['w_gpwio_group']]['customRequest'].append(newRequest)
		
		## Target IP에 필요한 시스템으로 이벤트 정보(IP, Port)
		owner['group'][row['w_gpwio_group']]['customIpPort'] = []
		newIpPort = ipPortParse(row['wr_8'])
		if newIpPort: 
			owner['group'][row['w_gpwio_group']]['customIpPort'].append(newIpPort)
		newIpPort = ipPortParse(row['wr_9'])
		if newIpPort: 
			owner['group'][row['w_gpwio_group']]['customIpPort'].append(newIpPort)

	owner['lst_gpio'] = {}
	for row in read_table_w_cfg_gpio():
		owner['lst_gpio'][row['w_device_id']] = {}
		owner['lst_gpio'][row['w_device_id']]['name'] = row['wr_subject']
		owner['lst_gpio'][row['w_device_id']]['addr1'] = row['w_host_Addr']
		owner['lst_gpio'][row['w_device_id']]['port1'] = row['w_host_Port']
		owner['lst_gpio'][row['w_device_id']]['addr2'] = row['w_host_Addr2']
		owner['lst_gpio'][row['w_device_id']]['port2'] = row['w_host_Port2']
		owner['lst_gpio'][row['w_device_id']]['serial'] = row['w_sensor_serial']

	###############################################
	## 파일 config.json내용 저장
	saveConfig(owner,share["path"]["gpwio"]+'/gpwio.json') ## 저장

	
	print(kill_demon_GPWIO())
	make_GPWIO_map()
	print(run_demon_GPWIO())		
	exit()	