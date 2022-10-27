#!/usr/bin/env python
# -*- coding: utf-8 -*-  

'''
사용법
프로그램 내에서 아래의 기능을 실행 한다.

def insert_socket_GPCIO(id, status, msg): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		# node.connect((ip,port))
		node.connect(('localhost', 8040))
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
def make_GPCIO_map():
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
			
def read_table_w_cfg_gpcio(): ##
	query = "SELECT * FROM " + share["table"]["gpcio"] + " WHERE w_gpcio_disable = 0" + " ORDER BY wr_id DESC" 
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
def kill_demon_GPCIO(cfgJson): 
	cmd = "kill $(ps aux | grep '[n]ode GPCIO.js %s' | awk '{print $2}')" % cfgJson
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_GPCIO :%s" % cfgJson
	
def run_demon_GPCIO(cfgJson): 
	cmd = "node GPCIO.js %s 2>&1 & " % cfgJson
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_GPCIO :%s" % cfgJson
	
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
	## content = 'val1||val2||192.168.0.10||1234||Opt1||Opt2'
	try:
		elements = content.split('||') 
		connectInfo = {
				'val1':elements[0],
				'val2':elements[1],
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
	# owner = readConfig('/home/pi/GPCIO/config.json') 
	# owner['status'] = share['status'].copy()
	# owner['mysql'] = share['mysql'].copy()

	## GPCIO 정보 수집
	portIn = 34200
	portOut = 34300
	owner = {}
	for row in read_table_w_cfg_gpcio():
		owner['interface'] = {}
		portID = int(row['w_device_id'].split('_')[-1])
		owner['interface']['port_in'] = portIn + portID
		owner['interface']['port_out'] = portOut + portID

		owner['file'] = {}
		owner['file']['html_source'] = share["path"]["gpcio"]+'/GPCIO.html'
		owner['file']['html_target'] = share["path"]["gpcio"]+'/index_'+str(owner['interface']['port_in'])+'.html'

		owner['sensor'] = {}
		owner['sensor']['cpu_id'] = row['w_cpu_id']
		owner['sensor']['device_id'] = row['w_device_id']
		owner['sensor']['serial'] = row['w_sensor_serial']
		owner['sensor']['security'] = row['w_security_mode']
		owner['sensor']['direction'] = row['w_gpcio_direction']
		owner['sensor']['gpio_id_L'] = row['w_gpcio_detect_L']
		owner['sensor']['gpio_id_R'] = row['w_gpcio_detect_R']
		owner['sensor']['gpio_id_L'] = row['w_gpcio_detect_L']
		owner['sensor']['trigger_L'] = row['w_gpcio_trigger_L']
		owner['sensor']['trigger_R'] = row['w_gpcio_trigger_R']
		owner['sensor']['speed'] = {}

		owner['sensor']['speed']['distance'] = row['w_distance']
		owner['sensor']['speed']['low'] = row['w_speed_L']
		owner['sensor']['speed']['high'] = row['w_speed_H']

		owner['count'] = {}
		owner['count']['capacity'] = {}
		owner['count']['capacity']['A'] = row['w_capacity_A']
		owner['count']['direction'] = {}
		owner['count']['direction']['AX'] = row['w_direction_AX']
		owner['count']['direction']['XA'] = row['w_direction_XA']

		owner['position'] = {}
		owner['position']['internal'] = {}
		owner['position']['internal']['AX'] = row['w_internal_AX']
		owner['position']['internal']['XA'] = row['w_internal_XA']
		owner['position']['external'] = {}
		owner['position']['external']['AX'] = row['w_external_AX']
		owner['position']['external']['XA'] = row['w_external_XA']
		
		## Audio Information (Audio Name and Length)
		owner['audio'] = {}
		if row['wr_2'] and row['wr_3']:
			owner['audio']['name'] = row['wr_2']
			owner['audio']['length'] = float(row['wr_3'])

		owner['server'] = {}
		## 릴레이 출력단에 이벤트 정보 전송(GPIO ID, 시간)
		owner['server']['relay'] = {}
		if row['w_alert_Port'] and row['w_alert_Value']:
			owner['server']['relay']['id'] = int(row['w_alert_Port'])
			owner['server']['relay']['time'] = float(row['w_alert_Value'])
		## 모니터링 시스템으로 이벤트 정보 전송(IP, Port)
		owner['server']['ims'] = []
		if row['w_host_Addr1'] and row['w_host_Port1']:
			owner['server']['ims'].append({ "addr":row['w_host_Addr1'], "port":row['w_host_Port1'] })
		if row['w_host_Addr2'] and row['w_host_Port2']:
			owner['server']['ims'].append({ "addr":row['w_host_Addr2'], "port":row['w_host_Port2'] })
		## Target URL에 이벤트에 따른 Request 전송(user, password, url, htmldigest)
		owner['server']['request']= []
		if row['wr_4']:
			newRequest = requestParse(row['wr_4'])
			if newRequest: 
				owner['server']['request'].append(newRequest)
			else:
				print "Error Check Request 1"
				continue
		if row['wr_5']:
			newRequest = requestParse(row['wr_5'])
			if newRequest: 
				owner['server']['request'].append(newRequest)
			else:
				print "Error Check Request 2"
				continue

		# newRequest = requestParse(row['wr_6'])
		# if newRequest: 
		# 	owner['server']['request'].append(newRequest)
		# newRequest = requestParse(row['wr_7'])
		# if newRequest: 
		# 	owner['server']['request'].append(newRequest)
		
		## Target IP에 필요한 시스템으로 소켓 이벤트 정보(IP, Port)
		owner['server']['socket'] = []
		if row['wr_8']:
			newIpPort = ipPortParse(row['wr_8'])
			if newIpPort: 
				owner['server']['socket'].append(newIpPort)
			else:
				print "Error Check Socket 1"
				continue
		if row['wr_9']:
			newIpPort = ipPortParse(row['wr_9'])
			if newIpPort: 
				owner['server']['socket'].append(newIpPort)
			else:
				print "Error Check Socket 2"
				continue

		###############################################
		## 파일 config.json내용 저장
		cfgJson = share["path"]["gpcio"]+'/gpcio_'+str(owner['interface']['port_in'])+'.json'
		saveConfig(owner,cfgJson) ## 저장
		
		print(kill_demon_GPCIO(cfgJson))
		make_GPCIO_map()
		print(run_demon_GPCIO(cfgJson))		
	exit()	