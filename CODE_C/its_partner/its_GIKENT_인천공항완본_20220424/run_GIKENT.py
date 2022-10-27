#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import time
import MySQLdb
import subprocess 
import json
from hashlib import sha256

def kill_demon_GIKENT():
	# 아래 grep에서 스페이스를 포함해야 자신(run_GIKENT.pyc)을 죽이지 않는다
	# cmd = "pkill -9 -ef $(ps aux | grep '/gikent_' | awk '{print $2}')"
	cmd = "pkill -9 -ef GIKENT/GIKENT 2>&1" ## 주의) 직전에 실행된 프로세서를 죽이는 오류 발생 가능
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "kill_demon_GIKENT"

def MASQUERADE(active,port):
	if active:
		# 연결 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination 192.168.168.30:80;
		'''%port
	else:
		# 차단 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		sudo iptables -D FORWARD -i eth0 -j ACCEPT
		sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE
		sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination 192.168.168.30:80;
		'''%port
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

def run_demon_GIKENT_PY(cfgJson): 
	cmd = "python %s/GIKENT.pyc %s 2>&1 & " % (share['path']['gikent'],cfgJson)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName): # 
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
		
def acuParse(content):
	## content = 'IP||Port||ID||Zone||Time||enc'
	try:
		elements = content.split('||') 
		acuInfo = {
			'ip':elements[0],
			'port':int(elements[1]),
			'id':int(elements[2]),
			'zone':int(elements[3]),
			'time':float(elements[4]),
			'enc':int(elements[5])
		}
		return acuInfo
	except:
		return 0

def read_table_w_cfg_gikent(): ## 사용자 환경 변수 로딩
	query = "SELECT * FROM " + share['table']['gikent'] + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
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
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
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

def main():
	tableRow = read_table_w_cfg_gikent()
	if not tableRow: # 데이터베이스 유/무 확인
		exit('No database')

	for row in tableRow:
		owner = {}
		owner['mysql'] = share['mysql'].copy()
		owner['port'] = share['port'].copy()
	
		if not row['w_giken_serial']:
			print "Need Sensor Serial Info(%s)" % row['w_device_id']
			continue

		owner['user_table'] = {}
		owner['user_table']['board']    = share['table']['gikent']
		owner['user_table']['wr_id']    = row['wr_id']

		owner['interface'] = {}
		owner['interface']['port_MQ']      = row['w_giken_ip'].split('.')[2] + row['w_giken_ip'].split('.')[3] # 원격접속을 위한 포트훠어딩 표트 번호 (센서아이피 후미 두개의 클레스) 16830
		owner['interface']['port_JS_in']   = share['port']['gikent']['portIn'] + int(row['w_device_id'].split('.')[-2])
		owner['interface']['port_JS_out']  = share['port']['gikent']['portOut'] + int(row['w_device_id'].split('.')[-2])
		owner['interface']['port_PY_in']   = share['port']['gikent']['portIn'] + int(row['w_device_id'].split('.')[-2]) + 1
		owner['interface']['port_PY_out']  = share['port']['gikent']['portOut'] + int(row['w_device_id'].split('.')[-2]) + 1
		owner['interface']['ip']           = row['w_device_id'].split('_')[1]

		owner['file'] = {}
		owner['file']['conf_common']    = '/home/pi/common/config.json'
		owner['file']['html_source']    = share['path']['gikent']+'/GIKENT.html'
		owner['file']['html_target']    = share['path']['gikent']+'/index_'+str(owner['interface']['port_JS_in'])+'.html'
		owner['file']['conf_gikent']    = share['path']['gikent']+'/gikent_'+str(owner['interface']['port_JS_in'])+'.json'

		owner['file']['log_gikent']     = share['path']['log']+'/'+row['w_sensor_serial']+'.log'

		owner['file']['image_folder']   = share['path']['img']+'/gikenT_'+row['w_sensor_serial']
		# owner['file']['image_NIR']      = share['path']['img']+'/gikenT_'+row['w_sensor_serial']+'/NIR'
		owner['file']['image_tailing']  = share['path']['img']+'/gikenT_'+row['w_sensor_serial']+'/tailing'
		owner['file']['image_manual']   = share['path']['img']+'/gikenT_'+row['w_sensor_serial']+'/manual'
		owner['file']['image_unknown']  = share['path']['img']+'/gikenT_'+row['w_sensor_serial']+'/unknown'
		owner['file']['image_final']    = share['path']['img']+'/gikenT_'+row['w_sensor_serial']+'/final'
		owner['file']['image_base']     = '0_img.png'
		owner['file']['image_live']     = '1_img.png'
		owner['file']['image_sync']     = '9_img.png'

		try:
			os.makedirs(owner['file']['image_folder'])
			os.chmod(owner['file']['image_folder'], 0o707)
		except:
			pass # directory already exists

		# try:
		# 	os.makedirs(owner['file']['image_NIR'])
		# 	os.chmod(owner['file']['image_NIR'], 0o707)
		# except:
		# 	pass # directory already exists

		try:
			os.makedirs(owner['file']['image_tailing'])
			os.chmod(owner['file']['image_tailing'], 0o707)
		except:
			pass # directory already exists

		try:
			os.makedirs(owner['file']['image_manual'])
			os.chmod(owner['file']['image_manual'], 0o707)
		except:
			pass # directory already exists

		try:
			os.makedirs(owner['file']['image_unknown'])
			os.chmod(owner['file']['image_unknown'], 0o707)
		except:
			pass # directory already exists

		try:
			os.makedirs(owner['file']['image_final'])
			os.chmod(owner['file']['image_final'], 0o707)
		except:
			pass # directory already exists

		owner['its'] = {}
		owner['its']['bo_ip']           = '.'.join(row['w_sensor_serial'].split('_')[1:5]) # IP 추출
		owner['its']['bo_table']        = row['w_sensor_serial'].split('_')[0] # 데이터베이스 테이블명
		owner['its']['bo_id']           = int(row['w_sensor_serial'].split('_')[-1]) # 테이블 ID명
		owner['its']['cpu_id']          = row['w_cpu_id']
		owner['its']['serial']          = row['w_sensor_serial']
		owner['its']['device']          = row['w_device_id']
		owner['its']['disabled']        = row['w_sensor_disable']
		owner['its']['description']     = row['w_sensor_desc']
		owner['its']['subject']         = row['wr_subject']
		owner['its']['level']           = row['w_group_level']

		owner['sensor'] = {}
		owner['sensor']['ip']           = row['w_giken_ip']
		owner['sensor']['port']         = 50001 # 센서 설정에서 변경 가능
		owner['sensor']['cgi']          = '/cgi-bin/information.cgi'
		owner['sensor']['device_id']    = row['w_device_id']
		owner['sensor']['version']      = row['w_giken_verson']
		owner['sensor']['serial']       = row['w_giken_serial']
		owner['sensor']['size_x']       = 320
		owner['sensor']['size_y']       = 240

		owner['opencv'] = {}
		owner['opencv']['crop_w']       = row['w_opencv_crop_w']
		owner['opencv']['crop_h']       = row['w_opencv_crop_h']
		owner['opencv']['crop_x']       = row['w_opencv_crop_x']
		owner['opencv']['crop_y']       = row['w_opencv_crop_y']

		owner['opencv']['mask_w']       = row['w_opencv_mask_w']
		owner['opencv']['mask_h']       = row['w_opencv_mask_h']
		owner['opencv']['mask_x']       = row['w_opencv_mask_x']
		owner['opencv']['mask_y']       = row['w_opencv_mask_y']
		if row['w_opencv_mask_w'] and row['w_opencv_mask_h']: # 폭과 높이 값이 존재하면
			owner['opencv']['mask_enable'] = 1
		else:
			owner['opencv']['mask_enable'] = 0

		owner['opencv']['mask2_w']       = row['w_opencv_mask2_w']
		owner['opencv']['mask2_h']       = row['w_opencv_mask2_h']
		owner['opencv']['mask2_x']       = row['w_opencv_mask2_x']
		owner['opencv']['mask2_y']       = row['w_opencv_mask2_y']
		if row['w_opencv_mask2_w'] and row['w_opencv_mask2_h']: # 폭과 높이 값이 존재하면
			owner['opencv']['mask2_enable'] = 1
		else:
			owner['opencv']['mask2_enable'] = 0

		owner['opencv']['mask3_w']       = row['w_opencv_mask3_w']
		owner['opencv']['mask3_h']       = row['w_opencv_mask3_h']
		owner['opencv']['mask3_x']       = row['w_opencv_mask3_x']
		owner['opencv']['mask3_y']       = row['w_opencv_mask3_y']
		if row['w_opencv_mask3_w'] and row['w_opencv_mask3_h']: # 폭과 높이 값이 존재하면
			owner['opencv']['mask3_enable'] = 1
		else:
			owner['opencv']['mask3_enable'] = 0

		# Anti Tailing Function
		owner['opencv']['tail_w']       = 200 # row['w_opencv_tail_w']
		owner['opencv']['tail_h']       = 100 # row['w_opencv_tail_h']
		owner['opencv']['tail_x']       = 100 # row['w_opencv_tail_x']
		owner['opencv']['tail_y']       = 30 # row['w_opencv_tail_y']

		if owner['opencv']['tail_w'] and owner['opencv']['tail_h']: # 폭과 높이 값이 존재하면
			owner['opencv']['tail_enable'] = 1
		else:
			owner['opencv']['tail_enable'] = 0

		owner['opencv']['object_w']     = row['w_opencv_object_w']
		owner['opencv']['object_h']     = row['w_opencv_object_h']
		owner['opencv']['object_p']     = row['w_opencv_object_p']

		if row['w_opencv_grayLv']: # 정전관련 밝기 강도
			owner['opencv']['grayLv'] = row['w_opencv_grayLv'] * 2.55 # % 값을 255레벨로 변경함
		else:
			owner['opencv']['grayLv'] = 0

		owner['opencv']['threshold']    = row['w_opencv_threshold']
		owner['opencv']['gBlur']        = row['w_opencv_gBlur']
		owner['opencv']['canny']        = row['w_opencv_canny']
		owner['opencv']['kernel']       = row['w_opencv_kernel']
		owner['opencv']['img_filter']   = row['w_opencv_filter']
		owner['opencv']['tuner_mode']   = row['w_opencv_tuner']
		owner['opencv']['mask_mode']    = row['w_opencv_mask']
		owner['opencv']['iLog_mode']    = row['w_opencv_iLog'] # 최종이미지 저장

		owner['opencv']['live_url']     = row['w_giken_live_url']

		owner['log_table'] = {}
		owner['log_table']['tbl_log']  = 'w_log_sensor_'+row['w_sensor_serial']
		
		owner['log_table']['tbl_live']  = 'w_log_gikenT_live_'+row['w_giken_serial']
		owner['log_table']['tbl_min']   = 'w_log_gikenT_min_'+row['w_giken_serial']
		owner['log_table']['tbl_hour']  = 'w_log_gikenT_hour_'+row['w_giken_serial']
		owner['log_table']['tbl_day']   = 'w_log_gikenT_day_'+row['w_giken_serial']
		owner['log_table']['tbl_week']  = 'w_log_gikenT_week_'+row['w_giken_serial']
		owner['log_table']['tbl_month'] = 'w_log_gikenT_month_'+row['w_giken_serial']
		owner['log_table']['tbl_sum']   = 'w_log_gikenT_sum_'+row['w_giken_serial']
		owner['log_table']['tbl_life']  = 30 # days 이후 삭제

		owner['log_pmt'] = {}
		owner['log_pmt']['tbl_live']  = 'w_log_permit_live_'+row['w_giken_serial']
		owner['log_pmt']['tbl_min']   = 'w_log_permit_min_'+row['w_giken_serial']
		owner['log_pmt']['tbl_hour']  = 'w_log_permit_hour_'+row['w_giken_serial']
		owner['log_pmt']['tbl_day']   = 'w_log_permit_day_'+row['w_giken_serial']
		owner['log_pmt']['tbl_week']  = 'w_log_permit_week_'+row['w_giken_serial']
		owner['log_pmt']['tbl_month'] = 'w_log_permit_month_'+row['w_giken_serial']
		owner['log_pmt']['tbl_life']  = 30 # days 이후 삭제

		owner['area'] = {}
		owner['area']['face'] = {}
		owner['area']['face']['A'] = row['w_face_direction_A']
		owner['area']['face']['B'] = row['w_face_direction_B']
		owner['area']['face']['C'] = row['w_face_direction_C']
		owner['area']['face']['D'] = row['w_face_direction_D']

		owner['area']['alarm'] = {}
		owner['area']['alarm']['permit']    = row['w_allow_permit'] # 허가 모드 (카드키, 지문)
		owner['area']['alarm']['security']  = row['w_security_mode'] # 보안 모드

		owner['gpio'] = {}
		owner['gpio']['reset_interval'] = float(row['w_reset_interval'])

		owner['gpio']['in_id'] = {}
		owner['gpio']['in_id']['0'] = 19
		owner['gpio']['in_id']['1'] = 13
		owner['gpio']['in_id']['2'] = 6
		owner['gpio']['in_id']['3'] = 5
		owner['gpio']['in_id']['4'] = 22
		owner['gpio']['in_id']['5'] = 27
		owner['gpio']['in_id']['6'] = 17
		owner['gpio']['in_id']['7'] = 4

		owner['gpio']['outStatus'] = {}
		owner['gpio']['outStatus']['0'] = int(row['w_gpio_out'][0])
		owner['gpio']['outStatus']['1'] = int(row['w_gpio_out'][1])
		owner['gpio']['outStatus']['2'] = int(row['w_gpio_out'][2])
		owner['gpio']['outStatus']['3'] = int(row['w_gpio_out'][3])
		owner['gpio']['outStatus']['4'] = int(row['w_gpio_out'][4])
		owner['gpio']['outStatus']['5'] = int(row['w_gpio_out'][5])
		owner['gpio']['outStatus']['6'] = int(row['w_gpio_out'][6])
		owner['gpio']['outStatus']['7'] = int(row['w_gpio_out'][7])

		owner['gpio']['inTypeNC'] = []
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][0]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][1]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][2]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][3]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][4]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][5]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][6]))
		owner['gpio']['inTypeNC'].append(int(row['w_gpio_in'][7]))

		## 릴레이 출력단에 이벤트 정보 전송(GPIO ID, 시간)
		owner['gpio']['out_id'] = {}
		owner['gpio']['out_id']['0'] = int(row['w_alert_Port1'])
		owner['gpio']['out_id']['1'] = int(row['w_alert_Port2'])
		owner['gpio']['out_id']['2'] = int(row['w_alert_Port3'])
		owner['gpio']['out_id']['3'] = int(row['w_alert_Port4'])

		owner['gpio']['out_time'] = {}
		owner['gpio']['out_time']['0'] = float(row['w_alert_Value1'])
		owner['gpio']['out_time']['1'] = float(row['w_alert_Value2'])
		owner['gpio']['out_time']['2'] = float(row['w_alert_Value3'])
		owner['gpio']['out_time']['3'] = float(row['w_alert_Value4'])

		if row['w_bounce_time']:
			owner['gpio']['bounce'] = row['w_bounce_time']
		else:
			owner['gpio']['bounce'] = 200

		## Port Forward : 외부 접속 허용 및 차단
		MASQUERADE(owner['opencv']['tuner_mode'],owner['interface']['port_MQ'])

		## Audio Information (Audio Name and Length)
		owner['audio'] = {}
		if row['wr_2'] and row['wr_3']:
			owner['audio']['name'] = row['wr_2']
			owner['audio']['length'] = float(row['wr_3'])

		owner['server'] = {}

		## 외부 접근가능한 아이피
		owner['server']['accessible'] = []
		if row['w_remote_accessible']:
			owner['server']['accessible'] = row['w_remote_accessible'].split(',')

		## 모니터링 시스템으로 이벤트 정보 전송(IP, Port)
		owner['server']['ims'] = []
		if row['w_host_Addr1'] and row['w_host_Port1']:
			owner['server']['ims'].append({ "addr":row['w_host_Addr1'], "port":row['w_host_Port1'] })
		if row['w_host_Addr2'] and row['w_host_Port2']:
			owner['server']['ims'].append({ "addr":row['w_host_Addr2'], "port":row['w_host_Port2'] })

		## 이벤트 서버 데이터베이스 접속 정보(IP, Port)
		owner['server']['event'] = []
		if row['w_event_Addr1'] and row['w_event_Port1']:
			owner['server']['event'].append({ "addr":row['w_event_Addr1'], "port":row['w_event_Port1'], "user":share['mysql']['user'], "pass":share['mysql']['pass'], "name":share['mysql']['name'] })
		if row['w_event_Addr2'] and row['w_event_Port2']:
			owner['server']['event'].append({ "addr":row['w_event_Addr2'], "port":row['w_event_Port2'], "user":share['mysql']['user'], "pass":share['mysql']['pass'], "name":share['mysql']['name'] })

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

		## 원격 GPWIO 정보
		owner['server']['acu'] = [] # {} 단일 요소 조합, [] 병렬 요소 조합,
		if row['wr_10']:
			newAcu = acuParse(row['wr_10'])
			if newAcu: 
				owner['server']['acu'].append(newAcu)
			else:
				print "Error Check ACU"
				continue

		## Live Control 설정
		owner['control'] = {}
		owner['control']['setLock'] = 0
		owner['control']['setOpen'] = 0
		owner['control']['release'] = 1
		owner['control']['antiDenial'] = row['w_allow_multiple']
		owner['control']['antiTailing'] = 0

		## 파일 config.json 저장
		# owner['sensor']['ip'] = '192.168.0.249' ######################
		saveConfig(owner,owner['file']['conf_gikent']) ## 저장

		# 메인 프로그램 실행
		run_demon_GIKENT_PY(owner['file']['conf_gikent'])

if __name__ == '__main__':

	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print share['file']['html_src']
	## 예: print share['mysql']['db_host']
	share = readConfig('/home/pi/common/config.json')
	print "\t",kill_demon_GIKENT()
	# print "\t",kill_demon_MOTION()

	# ###########################
	# ## 시스템 라이센스 확인 - 시작
	# # /tmp/license_hash가 manager의 mb_1의 값과 일치하는지 확인 한다.
	# license = str(itsMemberConfig('mb_1')['mb_1']).strip() # 라이센스 확인
	# if os.path.isfile('/tmp/'+license):
	# 	print("\tPass ITS License")
	# else:
	# 	print("\nNot Found ITS License\n\tPlease Call to Service Provider!!")
	# 	exit() 
	# ## 시스템 라이센스 확인 - 종료
	# ###########################

	main()
