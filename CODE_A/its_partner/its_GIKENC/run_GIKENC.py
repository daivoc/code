#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import time
import pymysql
import subprocess 
import json
import datetime

def kill_demon_GIKENC():
	# 아래 grep에서 스페이스를 포함해야 자신(run_GIKENC.pyc)을 죽이지 않는다
	# cmd = "pkill -9 -ef $(ps aux | grep '/gikenc_' | awk '{print $2}')"
	cmd = "pkill -9 -ef GIKENC/GIKENC 2>&1" ## 주의) 직전에 실행된 프로세서를 죽이는 오류 발생 가능
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "kill_demon_GIKENC"


def run_demon_GIKENC_PY(): 
	cmd = "python {}/GIKENC.pyc 2>&1 & ".format(share['path']['gikenc'])
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

def read_table_w_cfg_gikenc(): ## 사용자 환경 변수 로딩
	query = "SELECT * FROM " + share['table']['gikenc'] + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = pymysql.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except pymysql.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()


def create_image_folder(root):
	UTC = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # UTC+9
	jDate = [UTC[0:4],UTC[4:6],UTC[6:8],UTC[8:10]]

	f_year = root + '/{}'.format(jDate[0])
	if not os.path.isdir(f_year):
		os.makedirs(f_year)
		os.chmod(f_year, 0o707)
		# traffic[jDate[0]] = {}

	f_month = root + '/{}/{}'.format(jDate[0],jDate[1])
	if not os.path.isdir(f_month):
		os.makedirs(f_month)
		os.chmod(f_month, 0o707)
		# traffic[jDate[0]][jDate[1]] = {}

	f_day = root + '/{}/{}/{}'.format(jDate[0],jDate[1],jDate[2])
	if not os.path.isdir(f_day):
		os.makedirs(f_day)
		os.chmod(f_day, 0o707)
		# traffic[jDate[0]][jDate[1]][jDate[2]] = {}

	f_hour = root + '/{}/{}/{}/{}'.format(jDate[0],jDate[1],jDate[2],jDate[3])
	if not os.path.isdir(f_hour):
		os.makedirs(f_hour)
		os.chmod(f_hour, 0o707)
		# traffic[jDate[0]][jDate[1]][jDate[2]][jDate[3]] = 0

	# saveConfig(traffic,cfg['file']['log_traffic']) ## 저장

def main():
	tableRow = read_table_w_cfg_gikenc() # GIKEN Counter GUI
	if not tableRow: # 데이터베이스 유/무 확인
		exit('No database')

	for row in tableRow:
		cfg['mysql'] = share['mysql'].copy()
		# cfg['port'] = share['port'].copy()
	
		if not row['w_giken_serial']:
			print ("Need Sensor Serial Info(%s)" % row['w_device_id'])
			continue

		cfg['path'] = {}
		cfg['path']['gikenc'] 			= share['path']['gikenc']
		cfg['path']['common']    		= '/home/pi/common'
		
		# cfg['user_table'] = {}
		# cfg['user_table']['board']    = share['table']['gikenc']
		# cfg['user_table']['wr_id']    = row['wr_id']

		cfg['interface'] = {}
		cfg['interface']['port_MQ']      = row['w_giken_ip'].split('.')[2] + row['w_giken_ip'].split('.')[3] # 원격접속을 위한 포트훠어딩 표트 번호 (센서아이피 후미 두개의 클레스) 16830
		cfg['interface']['port_JS_in']   = share['port']['gikenc']['portIn'] + int(row['w_device_id'].split('.')[-2])
		cfg['interface']['port_JS_out']  = share['port']['gikenc']['portOut'] + int(row['w_device_id'].split('.')[-2])
		cfg['interface']['port_PY_in']   = share['port']['gikenc']['portIn'] + int(row['w_device_id'].split('.')[-2]) + 1
		cfg['interface']['port_PY_out']  = share['port']['gikenc']['portOut'] + int(row['w_device_id'].split('.')[-2]) + 1
		cfg['interface']['ip']           = row['w_device_id'].split('_')[1]

		cfg['file'] = {}
		cfg['file']['conf_common']	= cfg['path']['common']+'/config.json'
		cfg['file']['conf_gikenc']	= cfg['path']['gikenc']+'/gikenc.json'
		cfg['file']['html_source']	= cfg['path']['gikenc']+'/GIKENC.html'
		cfg['file']['html_target']	= cfg['path']['gikenc']+'/index.html'
		cfg['file']['log_gikenc']	= share['path']['log']+'/'+row['w_sensor_serial']+'.log'
		
		if not os.path.exists(share['path']['log']): # /var/www/html/its_web/data/log
			os.makedirs(share['path']['log'])
			os.chmod(share['path']['log'],0o777)
		else:
			os.chmod(share['path']['log'],0o777)
		
		imageFolder = share['path']['its_web']+share['path']['user']['image']
		if not os.path.exists(imageFolder): # /var/www/html/its_web/theme/ecos-its_optex/user/image/
			os.makedirs(imageFolder)
			os.chmod(imageFolder,0o777)
		else:
			os.chmod(imageFolder,0o777)

		## 스넵샷 이미지 폴더 생성 - 년월일시 <<<<<<
		cfg['file']['image_folder']   = share['path']['its_web']+share['path']['user']['image']+'/gikenC'
		try: # /var/www/html/its_web/theme/ecos-its_optex/user/image/gikenC
			os.makedirs(cfg['file']['image_folder'])
			os.chmod(cfg['file']['image_folder'], 0o707)
		except:
			os.chmod(cfg['file']['image_folder'], 0o707) # directory already exists

		cfg['file']['image_counting']  = cfg['file']['image_folder']+'/counting'
		try: # /var/www/html/its_web/theme/ecos-its_optex/user/image/gikenC/counting
			os.makedirs(cfg['file']['image_counting'])
			os.chmod(cfg['file']['image_counting'], 0o707)
		except:
			os.chmod(cfg['file']['image_counting'], 0o707) # directory already exists

		## 트레픽 통계 JSON
		cfg['file']['log_traffic']	= cfg['file']['image_folder']+'/traffic.json'

		## 라이브 이미지
		cfg['file']['image_live']     = cfg['file']['image_folder']+'/live.jpg'

		## 스넵샷 이미지 폴더 생성 - 년월일시 >>>>>>

		cfg['its'] = {}
		cfg['its']['bo_ip']           = '.'.join(row['w_sensor_serial'].split('_')[1:5]) # IP 추출
		cfg['its']['bo_table']        = row['w_sensor_serial'].split('_')[0] # 데이터베이스 테이블명
		cfg['its']['bo_id']           = int(row['w_sensor_serial'].split('_')[-1]) # 테이블 ID명
		cfg['its']['cpu_id']          = row['w_cpu_id']
		cfg['its']['serial']          = row['w_sensor_serial']
		cfg['its']['device']          = row['w_device_id']
		cfg['its']['disabled']        = row['w_sensor_disable']
		cfg['its']['description']     = row['w_sensor_desc']
		cfg['its']['subject']         = row['wr_subject']
		cfg['its']['userURL']         = 'http://'+cfg['its']['bo_ip']+share['path']['user']['home']

		cfg['sensor'] = {}
		cfg['sensor']['ip']           = row['w_giken_ip']
		cfg['sensor']['port']         = 50001 # 센서 설정에서 변경 가능
		cfg['sensor']['cgi']          = '/cgi-bin/information.cgi'
		cfg['sensor']['version']      = row['w_giken_verson']
		cfg['sensor']['serial']       = row['w_giken_serial']

		cfg['log_table'] = {}
		cfg['log_table']['tbl_live']  = 'w_log_gikenC_live_'+row['w_giken_serial']

		## 모니터링 시스템으로 이벤트 정보 전송(IP, Port)
		# cfg['server'] = {} # 자체 config.json 정보 사용
		cfg['server']['ims'] = {}
		cfg['server']['ims']['flag'] = {}
		cfg['server']['ims']['flag']['P'] = False # 주
		cfg['server']['ims']['flag']['S'] = False # 부
		if row['w_host_Addr1'] and row['w_host_Port1']:
			cfg['server']['ims']['P'] = { "addr":row['w_host_Addr1'], "port":row['w_host_Port1'] }
			cfg['server']['ims']['flag']['P'] = True # 주
		if row['w_host_Addr2'] and row['w_host_Port2']:
			cfg['server']['ims']['S'] = { "addr":row['w_host_Addr2'], "port":row['w_host_Port2'] }
			cfg['server']['ims']['flag']['S'] = True # 주

		## socketIO - TCP 포트 통신 <<<
		cfg['server']['socket'] = {}
		cfg['server']['socket']['flag'] = {}
		cfg['server']['socket']['flag']['P'] = False # 주
		cfg['server']['socket']['flag']['S'] = False # 부
		try:
			elements = row["wr_8"].split('||') 
			addr = elements[0]
			port = int(elements[1])
			value = elements[2]
			if addr and port and value:
				cfg['server']['socket']['P'] = {
					"addr":addr,
					"port":port,
					"value":value
				}
				cfg['server']['socket']['flag']['P'] = True
		except:
			pass

		try:
			elements = row["wr_9"].split('||') 
			addr = elements[0]
			port = int(elements[1])
			value = elements[2]
			if addr and port and value:
				cfg['server']['socket']['S'] = {
					"addr":addr,
					"port":port,
					"value":value
				}
				cfg['server']['socket']['flag']['S'] = True
		except:
			pass

		# create_image_folder(cfg['file']['image_counting']) ## 이벤트 시점의 스넵샷 이나 Touch file 용 폴더 생성

		## 파일 config.json 저장
		saveConfig(cfg,cfg['file']['conf_gikenc']) ## 저장

		# 메인 프로그램 실행
		run_demon_GIKENC_PY()

if __name__ == '__main__':
	cfg = readConfig('/home/pi/GIKENC/config.json') 
	share = readConfig('/home/pi/common/config.json')
	print (kill_demon_GIKENC())
	main()
