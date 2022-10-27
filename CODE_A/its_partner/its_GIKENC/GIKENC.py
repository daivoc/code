#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import socket 
import time
import datetime

import pymysql
import subprocess 
import json

import logging
import logging.handlers

import threading

from shutil import copyfile

from warnings import filterwarnings
filterwarnings('ignore', category = pymysql.Warning)

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
		
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName): # 
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def run_demon_GIKENC_JS(): 
	cmd = "node {}/GIKENC.js 2>&1 & ".format(cfg['path']['gikenc'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

def reset_sensor_time(time): 
	'''
	４－４－１ 시각설정 커맨드
		컬럼    내용    Size
		1       버전        2   "50"
		2       커맨드      3   "001" ：시각설정
		3       기기번호    8   시리얼번호
		4       데이터길이  8   "00000014"
		5       일시        14  "yyyymmddHHMMSS" (UTC)

	４－４－２ 시각설정 리스폰스
		컬럼    내용        Size
		1       버전        2 "50"
		2       커맨드      3 "001" ：시각설정
		3       에러코드    3 "000"：정상
		4       데이터길이  8 "00000000"

	echo "500010030373900000014BUFFERCLEAR00200" | nc 192.168.168.30 50001
	'''
	command = '001'
	length = '00000014'
	msg = "%s%s%s%s%s"%(cfg['sensor']['version'],command,cfg['sensor']['serial'],length,time)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((cfg['sensor']['ip'], cfg['sensor']['port']))
		sock.send(msg) 
		while True:
			data = sock.recv(16)
			if data[5:8] == "000":
				return 1
			else:
				return 0
			return data.decode()
	except socket.error:
		print("Error by reset_sensor_time")
		return 0
	except socket.timeout:
		print("Timeout by reset_sensor_time")
		return 0
	finally:
		sock.close() 

def reset_sensor_data():
	'''
	４－２－１ 계수데이터 클리어 커맨드
		컬럼    내용        Size
		1       버전        2   "50"
		2       커맨드      3   "200" ：카운트데이터 클리어
		3       기기번호    8   시리얼번호
		4       데이터길이  8   "00000016"
		5       고정문자열  16  "BUFFERCLEAR00200"

	４－２－２ 계수데이터 클리어 리스폰스
		컬럼    내용        Size
		1       버전        2   "50"
		2       커맨드      3   "200" ：카운트데이터 클리어
		3       에러코드    3   "000"：정상
		4       데이터길이  8   "00000000"

	echo "502000030373900000016BUFFERCLEAR00200" | nc 192.168.168.30 50001
	'''
	command = '200'
	length = '00000016'
	msg = "%s%s%s%s%s"%(cfg['sensor']['version'],command,cfg['sensor']['serial'],length,"BUFFERCLEAR00200") # 502000030373900000016BUFFERCLEAR00200
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((cfg['sensor']['ip'], cfg['sensor']['port']))
		sock.send(msg) 
		while True:
			data = sock.recv(16)
			if data[5:8] == "000":
				return 1
			else:
				return 0
	except socket.error:
		print("Error by reset_sensor_data")
		return 0
	except socket.timeout:
		print("Timeout by reset_sensor_data")
		return 0
	finally:
		sock.close() 

## 기켄센서 화상데이터 요구
def get_sensor_image(): 
	'''
	４－５ 화상데이터 요구
		・ 센서 유닛의 카메라화상을 요구할 때에 사용한다.
		・ 커맨드의 요구를 받은 시점의 화상데이터를 바이너리형식으로 회신한다.
		・ 현 버전에서는 320×240 의 JPEG 형식으로만 대응한다.
		・ 현 버전의 화상데이터의 최대사이즈는 32K 바이트가 된다.
	４－５－１ 화상데이터 요구 커맨드
		컬럼 내용 Size
		1 버전 2 “50”
		2 커맨드 3 “100” ：계수데이터
		3 기기번호 8 시리얼번호
		4 데이터길이 8 “00000002”
		5 화상타입 1 “0” ：현재의 화상(320×240 컬러)
		6 화상형식 1 “0” ：JPEG 파일 이미지
	４－５－２ 화상데이터 요구 리스폰스
		컬럼 내용 Size
		1 버전 2 “50”
		2 커맨드 3 “100”：계수데이터
		3 에러코드 3 “000”：정상
		4 데이터길이 8 “00000000”～
		“00000000”시는 화상없음
		5 화상데이터 변경가능 바이너리 데이터
	４－５－３ 커맨드 사용방법
		커맨드 송신시점의 현재화상데이터를 취득한다.
		취득한 화상데이터 부분을 무변환으로 파일에 덮어쓰기를 하면, JPEG 이미지파일로서 사용할수 있다.
		연속 화상을 취득하고 싶은 경우에는, 최하 1 초이상의 커맨드 송신시간의 간격이 필요하다.
		화상데이터에는 날짜・시각 등의 부가정보가 존재하지 않기 때문에, 매시간의 화상파일이
		필요할 경우에는 수집 어플리케이션 측의 파일명칭을 변경하는 등의 고려가 필요하다.

		50 100 000 00011301
		50 100 000 00011243
	'''
	version = cfg['sensor']['version']
	command = '100'
	serial = cfg['sensor']['serial']
	length = '00000002'
	imgType = '0' # 현재의 화상(320×240 컬러)
	imgStyle = '0' # JPEG 파일 이미지
	# 501000030373900000000200
	msg = "%s%s%s%s%s%s"%(version,command,serial,length,imgType,imgStyle)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((cfg['sensor']['ip'], cfg['sensor']['port']))
	sock.settimeout(1)
	## https://walkinpcm.blogspot.com/2016/05/python-python-opencv-tcp-socket-image.html
	try: 
		sock.send(msg) 
		count = int(sock.recv(16)[8:16])
		buf = b''
		while count:
			newbuf = sock.recv(count)
			if not newbuf: return None
			buf += newbuf
			count -= len(newbuf)
		return buf
	except socket.error:
		print("Error by get_sensor_image")
		return None
	except socket.timeout:
		print("Timeout by get_sensor_image")
		return None
	finally:
		sock.close() 

def read_sensor_count(dateS, dateE): 
	'''
	４－３－１ 카운트데이터 요구커맨드
		컬럼    내용            Size
		1       버전             2   "50"
		2       커맨드           3   "201" ：계수데이터
		3       기기번호         8   시리얼번호
		4       데이터길이       8   "00000032"
		5       검색시작 일시   12   "yyyymmddHHMM", "000000000000"로 가장 오래된 데이터
		6       검색종료 일시   12   "yyyymmddHHMM", "999999999999"로 최신 데이터※1
		7       카운트           1   출력지정 1 "0"~"1" ※2
		8       카운트           2   출력지정 1 "0"~"1" ※2
		9       카운트           3   출력지정 1 "0"~"1" ※2
		10      카운트           4   출력지정 1 "0"~"1" ※2
		11      예비영역         4   "0000"

		※1 최신데이터를 요구한 경우, 리스폰스의 제일 마지막 레코드에 미확정 데이터를 부가한다.
		1 분 이내의 간격으로 속보수치가 필요할 경우에 사용한다.
		※2 "0"＝출력없음, "1"＝출력있음

	４－３－２ 카운트 데이터 요구 리스폰스
		컬럼    내용            Size
		1       버전            2   "50"
		2       커맨드          3   "201"：계수데이터
		3       에러코드        3   "000"：정상
		4       데이터길이      8   "00000030" ~ 30＋레코드수×레코드사이즈
		5       미송신데이터    12 "000000000000" ※1
				선두일시
		6       레코드 수       8   "00000000"~
		7       레코드 사이즈   8   "00000000"~
		8       개행            2   CR(0x0D)＋LF(0x0A)
		9       카운트 데이터       레코드수×레코드사이즈

		※1 현시점의 센서 유닛 사양으로는 미송신 데이터는 발생하지 않기 때문에, 항상 0 이 설정됨.

		echo "50201003037390000003200000000000099999999999911110000" | nc 192.168.168.30 50001
	'''
	command = '201'
	length = '00000032'
	count = '1111'
	reserve = '0000'
	msg = "%s%s%s%s%s%s%s%s"%(cfg['sensor']['version'],command,cfg['sensor']['serial'],length,dateS,dateE,count,reserve)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((cfg['sensor']['ip'], cfg['sensor']['port']))
		sock.send(msg) 
		while True:
			data = sock.recv(128)
			return data.decode()
	except socket.error:
		print("Error by read_sensor_count")
		return 0
	except socket.timeout:
		print("Timeout by read_sensor_count")
		return 0
	finally:
		sock.close() 

## 백그라운드 포트 감지
## https://stackoverflow.com/questions/22648765/how-to-run-a-background-procedure-while-constantly-checking-for-input-threadin
def process_port_PY_in():
	try:
		sock = socket.socket()
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ## 파이썬 : 바인딩 소켓 :“이미 사용중인 주소” 방지
		sock.bind(("localhost",cfg['interface']['port_PY_in']))
		sock.listen(1)
		print ("\tWaiting on connection %s"%cfg['interface']['port_PY_in'])
		conn = sock.accept()
		logger.info("> Client connected Recv. Port{}".format(cfg['interface']['port_PY_in']))
	except socket.error as msg:
		print ("\tError bind - (Kill Processor.) PY")
		logger.info("> Error Connect to Recv. Port:{}".format(cfg['interface']['port_PY_in']))

	while True:
		try:
			data = conn[0].recv(1024)
			if data:
				try: # json 확인
					jData = json.loads(data) ## json.loads 실행시 오류가 없으면 진행
					if 'timer_set' in jData:
						cfg['eventTimer'] = jData['timer_set']
						logger.info('Event Timer Set: {}'.format(cfg['eventTimer']))
						print(cfg['eventTimer'])
					elif 'gChkBox' in jData:
						cfg['gChkBox'] = jData['gChkBox'] # 실시간 변수값 설정
						logger.info('CheckBox Set: {}'.format(cfg['gChkBox']))
						# print(cfg['gChkBox'])
				except ValueError as e: ## 상단의 json.loads 실행시 오류가 발생하면
					if data == 'event_group':
						messageToClient('eventGroup', cfg['eventGroup']) # 뷰어측 브라우저에 상태 전송
						messageToClient('eventTimer', cfg['eventTimer']) # 뷰어측 브라우저에 타이머 설정 정보 전송 
					elif data == 'event_reset':
						cfg['trigger'] = [0,0,0,0,0,0,0,0]
						cfg['newData'] = [0,0,0,0,0,0,0,0]
						cfg['gapEvent'] = [0,0,0,0,0,0,0,0]
						cfg['sumEvent'] = [0,0,0,0,0,0,0,0]
						# cfg['newData'] = [0,0,0,0,0,0,0,0]
						# cfg['oldData'] = [0,0,0,0,0,0,0,0]
						cfg['eventGroup'] = {"trigger":cfg['trigger'],"newEvent":cfg['newEvent'],"gapEvent":cfg['gapEvent'],"sumEvent":cfg['sumEvent']}
						messageToClient("eventGroup", cfg['eventGroup']) # 뷰어측 브라우저에 상태 등록
				else:
					continue

				# saveConfig(cfg,cfg['file']['conf_gikenc']) ## 저장
		except:
			continue

	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

# 모니터링을 위한 지도파일을 생성한다.
def make_GIKENC_map():
	jquery = '%s/jquery/jquery-3.1.1.min.js' % cfg['path']['common']
	__script_jquery_js__ = '<script>'+open(jquery, 'r').read()+'</script>'

	bootstrap_js = '%s/bootstrap/js/bootstrap.min.js' % cfg['path']['common']
	__style_bootstrap_js__ = '<script>'+open(bootstrap_js, 'r').read()+'</script>'
	bootstrap_css = '%s/bootstrap/css/bootstrap.min.css' % cfg['path']['common']
	__style_bootstrap_css__ = '<style>'+open(bootstrap_css, 'r').read()+'</style>'
	
	__realtime_image__ = '''
	function reflashImage() {
		document.getElementById("liveImage").src = "http://%s/theme/ecos-its_optex/user/image/gikenC/live.jpg?rand=" + Math.random();
	}
	''' % (cfg['its']['bo_ip'])
	__roomID__ = '''{}'''.format(cfg['its']['description'].encode('utf8')) # .decode('unicode_escape')
	with open(cfg['file']['html_source'], 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_js__', __style_bootstrap_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css__', __style_bootstrap_css__)

		tmp_its_tmp = tmp_its_tmp.replace('__roomID__', __roomID__)
		tmp_its_tmp = tmp_its_tmp.replace('__realtime_image__', __realtime_image__.encode('utf8'))
		
		with open(cfg['file']['html_target'], 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()

# 이벤트 시점의 스넵샷 이나 Touch file 용 폴더 생성
def create_image_folder(root):
	UTC = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # UTC+9
	jDate = [UTC[0:4],UTC[4:6],UTC[6:8],UTC[8:10]]

	f_year = root + '/{}'.format(jDate[0])
	if not os.path.isdir(f_year):
		os.makedirs(f_year)
		os.chmod(f_year, 0o707)
		traffic[jDate[0]] = {}

	f_month = root + '/{}/{}'.format(jDate[0],jDate[1])
	if not os.path.isdir(f_month):
		os.makedirs(f_month)
		os.chmod(f_month, 0o707)
		traffic[jDate[0]][jDate[1]] = {}

	f_day = root + '/{}/{}/{}'.format(jDate[0],jDate[1],jDate[2])
	if not os.path.isdir(f_day):
		os.makedirs(f_day)
		os.chmod(f_day, 0o707)
		traffic[jDate[0]][jDate[1]][jDate[2]] = {}

	f_hour = root + '/{}/{}/{}/{}'.format(jDate[0],jDate[1],jDate[2],jDate[3])
	if not os.path.isdir(f_hour):
		os.makedirs(f_hour)
		os.chmod(f_hour, 0o707)
		traffic[jDate[0]][jDate[1]][jDate[2]][jDate[3]] = 0

	saveConfig(traffic,cfg['file']['log_traffic']) ## 저장
	# print ("1111 %s"%traffic)

	# f_hour = root + '/{}/{}/{}/{}'.format(jDate[0],jDate[1],jDate[2],jDate[3])
	# if os.path.isdir(f_hour):
	# 	return
	# else:
	# 	os.makedirs(f_hour)
	# 	os.chmod(f_hour, 0o707)
	# 	traffic[jDate[0]][jDate[1]][jDate[2]][jDate[3]] = {}

	# f_day = root + '/{}/{}/{}'.format(jDate[0],jDate[1],jDate[2])
	# if os.path.isdir(f_day):
	# 	return
	# else:
	# 	os.makedirs(f_day)
	# 	os.chmod(f_day, 0o707)
	# 	traffic[jDate[0]][jDate[1]][jDate[2]] = {}

	# f_month = root + '/{}/{}'.format(jDate[0],jDate[1])
	# if os.path.isdir(f_month):
	# 	return
	# else:
	# 	os.makedirs(f_month)
	# 	os.chmod(f_month, 0o707)
	# 	traffic[jDate[0]][jDate[1]] = {}

	# f_year = root + '/{}'.format(jDate[0])
	# if os.path.isdir(f_year):
	# 	return
	# else:
	# 	os.makedirs(f_year)
	# 	os.chmod(f_year, 0o707)
	# 	traffic[jDate[0]] = {}

def file_counter(folder): # 생성된 스넵샷 갯수 확인
	for base, dirs, files in os.walk(folder):
		# print('Looking in : ',base)
		noOfFiles = 0
		noOfDir = 0
		for directories in dirs:
			noOfDir += 1
		for Files in files:
			noOfFiles += 1

		if noOfFiles: 
			print('file_counter - {}/{}'.format(base[-13:], noOfFiles)) # 2021/11/12/08 25

	# print('Number of files',noOfFiles)
	# print('Number of Directories',noOfDir)
	# print('Total:',(noOfDir + noOfFiles))

###################################
## apiCustom
###################################
def apiCustom(addr, port, data):
	## Data는 List내에 Dict.로 국성되어야 한다. - [{},{},..] 로 구성 되어야 한다.
	## data는 평문임으로 json.loads 명령으로 변환한후
	## 필요한 작업을 수행한 후 결과를 반환한다.
	## 반환시 dict(json)를 json.dumps 명령으로 변환후 전송한다.
	try:
		arrJson = json.loads(data)
	except:
		logger.warning('category:unknown msg:JSON format error - {}'.format(data))
		return('category:unknown msg:JSON format error - {}'.format(data))

	if isinstance(arrJson, list): # 인스턴스가 데이터 타입과 일치할 경우에는 True
		pass
	else:
		logger.warning('JSON Array not JSON Objects. {}'.format(arrJson))
		return('JSON Array not JSON Objects. {}'.format(arrJson))

	for i in range(len(arrJson)):
		args = arrJson[i]

		if '__LG__' in args:
			dataIs = args
		elif '__command__' in args:
			dataIs = args
		else: # ITS API로 전송을 의미한다.
			dataIs = [args]

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
		try: 
			sock.connect((addr, port))
			result = sock.sendall(json.dumps(dataIs))
			if not result:
				logger.info("Success {} {} {}".format(addr, port, dataIs)) 
		except socket.error:
			logger.warning("Socket Error {0}".format(addr)) 
		except socket.timeout:
			logger.warning("Timeout Error {0}".format(addr)) 
		finally:
			sock.close() 

	# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# sock.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	# try: 
	# 	sock.connect((addr, port))
	# 	return sock.sendall(data) 
	# 	# sock.send(data)
	# 	# recv = sock.recv(1024) 
	# 	# sock.close() 
	# 	# return recv
	# except socket.error:
	# 	return "Socket Error {0}".format(addr)
	# except socket.timeout:
	# 	return "Timeout Error {0}".format(addr)
	# finally:
	# 	sock.close() 
		
###################################
## 활성화된 모니터링서버(IMS)에 데이터 전송
###################################
def insert_socket_IMS(ip,port,data): 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((ip, port)) # sock.connect((ip,port))
		return sock.sendall(data) 
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

###################################
## 활성화된 브라우저에 데이터 전송
###################################
def insert_socket_GIKEN(data): 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect(('localhost', cfg['interface']['port_JS_in'])) # sock.connect((ip,port))
		return sock.sendall(data) 
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

###################################
## JSON 메세지 전송
###################################
def messageToClient(key, value):
	jsonData = {}
	jsonData[key] = value
	json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
	insert_socket_GIKEN(json_dump)

## Database Table
def create_table_w_log_giken(table):
	try:
		conn = pymysql.connect(host=cfg['mysql']['host'], user=cfg['mysql']['user'], passwd=cfg['mysql']['pass'], db=cfg['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		tbl_w_log_sensor_sql = """
			CREATE TABLE IF NOT EXISTS %s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_ax_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xa_cnt` int(11) NOT NULL DEFAULT '0',
			`w_bx_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xb_cnt` int(11) NOT NULL DEFAULT '0',
			`w_cx_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xc_cnt` int(11) NOT NULL DEFAULT '0',
			`w_dx_cnt` int(11) NOT NULL DEFAULT '0',
			`w_xd_cnt` int(11) NOT NULL DEFAULT '0',
			`w_opt_01` int(11) NOT NULL DEFAULT '0',
			`w_opt_02` int(11) NOT NULL DEFAULT '0',
			`w_opt_03` int(11) NOT NULL DEFAULT '0',
			`w_ymdhm` varchar(12) DEFAULT NULL,
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % table
		cursor.execute(tbl_w_log_sensor_sql) # create table
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except pymysql.Error as error:
		logger.info('SQL Server Error {}'.format(error))
 	except pymysql.Warning as warning:
		pass
	# finally:
	# 	cursor.close()
	# 	conn.close()

def insert_table_w_log_giken(table, data): 
	query = "INSERT IGNORE INTO "+table+"(w_ax_cnt,w_xa_cnt,w_bx_cnt,w_xb_cnt,w_cx_cnt,w_xc_cnt,w_dx_cnt,w_xd_cnt,w_opt_01,w_opt_02,w_opt_03,w_ymdhm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	# args = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11].ljust(12, '0'))
	args = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11])
	try:
		conn = pymysql.connect(host=cfg['mysql']['host'], user=cfg['mysql']['user'], passwd=cfg['mysql']['pass'], db=cfg['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except pymysql.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def main ():
	## 기켄센서 정검
	if reset_sensor_data():
		print("Cleared Sensor Buffer")
	else:
		print("Error - Clear Sensor Buffer")
		os._exit(0)
	
	dateTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") # UTC - 센서 요청시간대
	if reset_sensor_time(dateTime):
		print "Set Sensor Time: %s" % datetime.datetime.now()
	else:
		print("Error - Set Sensor Time")
		os._exit(0)
	
	# 기켄센서 정검이후 GIKENC_JS 실행
	run_demon_GIKENC_JS()
	logger.info('> run_demon_GIKENC_JS')

	## Create html_target(index.html)
	make_GIKENC_map()

	# 데이타베이스 이벤트 테이블 생성
	create_table_w_log_giken(cfg['log_table']['tbl_live']) 
	# create_table_w_log_giken(cfg['log_table']['tbl_min']) 
	# create_table_w_log_giken(cfg['log_table']['tbl_hour']) 
	# create_table_w_log_giken(cfg['log_table']['tbl_day']) 
	# create_table_w_log_giken(cfg['log_table']['tbl_week']) 
	# create_table_w_log_giken(cfg['log_table']['tbl_month']) 
	# create_table_w_log_giken(cfg['log_table']['tbl_sum']) 

	dateS = dateTime[:-2] # 센서 시간 설정후 시작시간 설정
	dateE = '999999999999'
	saveDate = 'dateS'

	create_image_folder(cfg['file']['image_counting']) # 시간대별 image folder 생성
	
	## 백그라운드 포트 감지 - NodeJS에서 보내는 데이터 파싱과 실행
	thread = threading.Thread(target=process_port_PY_in)
	thread.daemon = True
	thread.start()

	while True:
		data = read_sensor_count(dateS, dateE)
		# print data
		if data is 0: # 페킷 읽기 오류
			continue

		for line in data.splitlines()[1:]:
			# dateS = int(line[8:20]) # 신규 픽업시간 저장
			dateS = line[8:20] # 신규 픽업시간 저장
			dataIs = line[22:] # 신규데이터 저장
			if len(dataIs) is not 32: # print len(dataIs)
				continue

			if dateS > saveDate: # 분이 바뀌면 집계 - 데이터베이스 연계
				create_image_folder(cfg['file']['image_counting']) # 시간대별 image folder 생성
			
			# print int(dataIs)

			for i in range(8): # 4byte 단위로 구분한 후 8새의 변수 newData[i]에 등록한다.
				cfg['newData'][i] = int(dataIs[i*4:(i*4)+4])

			for i in range(8):
				if cfg['newData'][i] > cfg['oldData'][i]: # 새로운 이벤트(cfg['newData'])값은 1분 주기로 리셋된다.
					cfg['newEvent'][i] = cfg['newData'][i] - cfg['oldData'][i] # 새로 발생한 이벤트수 추출
					cfg['sumEvent'][i] += cfg['newEvent'][i] # 발생한 이벤트 합계
					cfg['oldData'][i] = cfg['newData'][i] # 발생한 이벤트 저장
					cfg['trigger'][i] = 1 # 트리거 플레그 온
				else:
					cfg['newEvent'][i] = 0
					cfg['trigger'][i] = 0

			if 1 in cfg['trigger']: # 만약 트리거가 발생 했으면
				for i in range(8): # 홀수(Out), 짝수(In) 구분 후 잔여 인원 저장
					if i % 2: # 1 3 5 7
						cfg['gapEvent'][i] = cfg['sumEvent'][i] - cfg['sumEvent'][i-1]
					else: # 0 2 4 6
						cfg['gapEvent'][i] = cfg['sumEvent'][i] - cfg['sumEvent'][i+1]

						if cfg['gChkBox']['adjustment']: ## adjustment
							## 오류로 인해 들어간 입장 보다 퇴장이 많을시 초기화 히는 기능: in < out
							if cfg['gapEvent'][i] < 0:
								cfg['gapEvent'][i] = 0
								cfg['sumEvent'][i] = cfg['sumEvent'][i+1] 

				tableID = insert_table_w_log_giken(cfg['log_table']['tbl_live'], cfg['newEvent'] + [0,0,0,dateS])
				# print("id:{}, cfg['trigger']:{}, cfg['newEvent']:{}, cfg['gapEvent']:{}, cfg['sumEvent']:{}".format(tableID, cfg['trigger'], cfg['newEvent'], cfg['gapEvent'], cfg['sumEvent']))

				# 모니터링(상태값 실시간 전송) : 실시간 모든 방향의 합계를 활성화된 브라우저로 전송
				cfg['eventGroup'] = {"trigger":cfg['trigger'],"newEvent":cfg['newEvent'],"gapEvent":cfg['gapEvent'],"sumEvent":cfg['sumEvent']}
				messageToClient("eventGroup", cfg['eventGroup']) # 뷰어측 브라우저에 상태 등록
				cfg['trigger'] = [0,0,0,0,0,0,0,0]

				###################################
				## Protocol에 따른 Event 전송 <<<<<<
				###################################

				## IMS Monitoring
				if cfg['server']['ims']['flag']['P']:
					imsValue = 'id='+cfg['its']['serial']+',name='+cfg['its']['subject']+',beep=1,status=1,shot=,video=,count=1,block=0,msg=Inner'
					result = insert_socket_IMS(cfg['server']['ims']['P']['addr'],cfg['server']['ims']['P']['port'],imsValue)
					logger.info("IMS P:{0}, {1}, {2}, {3}".format(result, cfg['server']['ims']['P']['addr'], cfg['server']['ims']['P']['port'], imsValue))
				if cfg['server']['ims']['flag']['S']:
					imsValue = 'id='+cfg['its']['serial']+',name='+cfg['its']['subject']+',beep=1,status=1,shot=,video=,count=1,block=0,msg=Inner'
					result = insert_socket_IMS(cfg['server']['ims']['S']['addr'],cfg['server']['ims']['S']['port'],imsValue)
					logger.info("IMS S:{0}, {1}, {2}, {3}".format(result, cfg['server']['ims']['S']['addr'], cfg['server']['ims']['S']['port'], imsValue))

				## socketIO API 사용자 연동 기능
				if cfg['server']['socket']['flag']['P']:
					# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], cfg['server']['socket']['P']['value'])
					dataIs = cfg['server']['socket']['P']['value']
					logger.info("Request_P:{0}, {1}, {2}".format(cfg['server']['socket']['P']['addr'], cfg['server']['socket']['P']['port'], dataIs.encode('utf-8')))
					result = apiCustom(cfg['server']['socket']['P']['addr'], cfg['server']['socket']['P']['port'], dataIs)
				if cfg['server']['socket']['flag']['S']:
					# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], cfg['server']['socket']['S']['value'])
					dataIs = cfg['server']['socket']['S']['value']
					logger.info("Request_S:{0}, {1}, {2}".format(cfg['server']['socket']['S']['addr'], cfg['server']['socket']['S']['port'], dataIs.encode('utf-8')))
					result = apiCustom(cfg['server']['socket']['S']['addr'], cfg['server']['socket']['S']['port'], dataIs)

				## 스넵샷 저장
				data = get_sensor_image()
				if data:
					try: # 스넵샷 백업
						with open(cfg['file']['image_live'], 'w') as f:
							f.write(data)
						dateT = datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f") # UTC - 센서 요청시간대
						jDate = [dateT[0:4],dateT[4:6],dateT[6:8],dateT[8:10],dateT[10:]]
						fileT = '{}/{}/{}/{}/{}/{}.jpg'.format(cfg['file']['image_counting'],jDate[0],jDate[1],jDate[2],jDate[3],jDate[4])
						
						if cfg['gChkBox']['snapshut']:
							copyfile(cfg['file']['image_live'], fileT) # 이미지 백업
						else:
							open(fileT,'a').close() # Touch 파일 생성

						traffic[jDate[0]][jDate[1]][jDate[2]][jDate[3]] += 1
					except:
						logger.info('Not Found Snapshot Folder')

				###################################
				## Protocol에 따른 Event 전송 >>>>>>
				###################################


			if dateS > saveDate: # 분이 바뀌면 집계 - 데이터베이스 연계
				# read_minute_sum() # 분 집계 등록
				cfg['oldData'] = [0,0,0,0,0,0,0,0] # 초기화 - cfg['newData'] 값은 1분 주기로 센서에서 자동 리셋되기 때문에 oldData도 리셋시킴
				# file_counter(cfg['file']['image_counting'])

				if dateS[0:10] > saveDate[0:10]: # 시간이 바뀌면
					pass

					if dateS[0:8] > saveDate[0:8]: # 날짜가 바뀌면
						# 어제의 합계를 JSON형식으로 날자방에 저장 -> JS에 요청 한다.
						messageToClient('today_total', '{}/{}/{}.json'.format(int(saveDate[0:4]),int(saveDate[4:6]),int(saveDate[6:8]))) # 어제 날짜 통계요청
						pass

						if datetime.datetime(int(dateS[0:4]),int(dateS[4:6]),int(dateS[6:8])).weekday() == 0: # 한주의 시작이면
							pass

						if dateS[0:6] > saveDate[0:6]: # 월이 바뀌면
							pass

							if dateS[0:4] > saveDate[0:4]: # 해가 바뀌면
								pass

			saveDate = dateS # 이전 픽업시간 저장

		time.sleep(0.1) # 1초에 한번 이상 확인하기 위함
		
if __name__ == '__main__':

	cfg = readConfig('./gikenc.json')
	# Global ################## <<<
	cfg['eventGroup'] = {}
	cfg['eventTimer'] = [0,0,0,0,0,0,0,0] 
	cfg['eventUTime'] = [0,0,0,0,0,0,0,0] # unix time
	cfg['trigger'] = [0,0,0,0,0,0,0,0]
	cfg['newEvent'] = [0,0,0,0,0,0,0,0]
	cfg['gapEvent'] = [0,0,0,0,0,0,0,0]
	cfg['sumEvent'] = [0,0,0,0,0,0,0,0]
	cfg['newData'] = [0,0,0,0,0,0,0,0]
	cfg['oldData'] = [0,0,0,0,0,0,0,0]
	# ######################### >>>
	print '\nip:{}, port:{}, version:{}, serial:{}'.format(cfg['sensor']['ip'], cfg['sensor']['port'], cfg['sensor']['version'], cfg['sensor']['serial'])

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	logger = logging.getLogger('mylogger') # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = cfg['file']['log_gikenc']
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	os.chmod(filename,0o777)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info('> START')
	# logger.debug('===========================')
	# logger.info('TEST START')
	# logger.warning('파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.')
	# logger.debug('디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.')
	# logger.critical('치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!')
	# logger.debug('===========================')
	# logger.info('TEST END!')
	print('Log Path: {}'.format(cfg['file']['log_gikenc']))
	############ logging ################

	# run_demon_GIKENC_JS()
	# logger.info('> run_demon_GIKENC_JS')

	try:
		traffic = readConfig(cfg['file']['log_traffic']) # 통행량
	except:
		traffic = {}

	main()