#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# from module import *

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
	response = os.system("ping -c 1 {} > /dev/null".format(ip))
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
	# cmd = "kill -9 $(ps aux | grep 'spotter.js' | awk '{print $2}' | head -n 1)"
	cmd = "pkill -9 -ef spotter.js 2>&1" 
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
	# print(license, key)
	serial = ''
	f = open('/proc/cpuinfo','r')
	for line in f:
		if line[0:6]=='Serial':
			serial = line[10:26]
	f.close()

	# print(sha256(serial + key).hexdigest(), license)
	if sha256(serial + key).hexdigest() == license:
		return 1
	else:
		return 0


def main ():
	try:
		# 모니터링을 위한 HTML 파일 생성한다.
		__script_jquery_js__ = '%s/jquery/jquery-3.1.1.min.js' % cfg["path"]["common"]
		__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
		__script_jquery_ui_js__ = '%s/jquery/ui/jquery-ui.js' % cfg["path"]["common"]
		__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
		__style_jquery_ui_css__ = '%s/jquery/ui/jquery-ui.css' % cfg["path"]["common"]
		__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'

		__svg_pan_zoom__ = '%s/svg-pan-zoom/svg-pan-zoom.js' % cfg["path"]["common"]
		__svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'
		__smoothiecharts__ = '%s/smoothiecharts/smoothie.js' % cfg["path"]["common"]
		__smoothiecharts__ = '<script>'+open(__smoothiecharts__, 'r').read()+'</script>'
		
		bootstrap_js = '%s/bootstrap/js/bootstrap.min.js' % cfg["path"]["common"]
		__script_bootstrap_js__ = '<script>'+open(bootstrap_js, 'r').read()+'</script>'
		
		bootstrap_css = '%s/bootstrap/css/bootstrap.min.css' % cfg["path"]["common"]
		__style_bootstrap_css__ = '<style>'+open(bootstrap_css, 'r').read()+'</style>'
		
		canvas_gauges_js = '%s/node_modules/canvas-gauges/gauge.min.js' % cfg["path"]["common"]
		__script_canvas_gauges_js__ = '<script>'+open(canvas_gauges_js, 'r').read()+'</script>'

		__company_logo_path__ = cfg["path"]["img"]+cfg["file"]["img_logo_main"]
		
		__camera_live_url__ = "http://%s/%s"%(cfg["camera"]["addr"], cfg["camera"]["video"])
		
		## 바탕 이미지를 위한 SVG 
		if os.path.exists("www/image"+cfg["file"]["html_bg"]):
			__svg_background__ = open("www/image"+cfg["file"]["html_bg"], 'r').read()
		else:
			__svg_background__ = ''
			
		# print __svg_background__
		
		# print(cfg["file"]["html_src"])
		with open(cfg["path"]["spotter"]+cfg["file"]["html_src"], 'r') as templet_file:
			tmp_its_tmp = templet_file.read()
			templet_file.close()
			tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
			tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
			tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
			tmp_its_tmp = tmp_its_tmp.replace('__svg_pan_zoom__', __svg_pan_zoom__)
			tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
			tmp_its_tmp = tmp_its_tmp.replace('__script_bootstrap_js__', __script_bootstrap_js__)
			tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css__', __style_bootstrap_css__)
			tmp_its_tmp = tmp_its_tmp.replace('__script_canvas_gauges_js__', __script_canvas_gauges_js__)
			tmp_its_tmp = tmp_its_tmp.replace('__company_logo_path__', __company_logo_path__)
			tmp_its_tmp = tmp_its_tmp.replace('__camera_live_url__', __camera_live_url__)
			tmp_its_tmp = tmp_its_tmp.replace('__svg_background__', __svg_background__)

			with open(cfg["path"]["spotter"]+cfg["file"]["html_dst"], 'w') as tmp_its_file:
				tmp_its_file.write(tmp_its_tmp)
				tmp_its_file.close()
		# 모니터링을 위한 HTML 파일 생성 종료
		logger.info("Created HTML File for Client %s"%cfg["path"]["spotter"]+cfg["file"]["html_dst"])
		print ("\n\tCreated HTML File for Client.")
	except:
		logger.critical("Error Making HTML File for Client %s"%cfg["path"]["spotter"]+cfg["file"]["html_dst"])
		print ("\n\tError Making HTML File for Client %s"%cfg["path"]["spotter"]+cfg["file"]["html_dst"])
		exit()
		
	run_its_spotter(cfg["path"]["spotter"], cfg["interface"]["portOut"])
	
if __name__ == '__main__':
	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print cfg["file"]["html_src"]
	cfg = readConfig() ## 환경변수 읽기

	## Working license Check
	# cfg["license"]["passed"] = 1
	if check_system_license(cfg["license"]["key"], cfg["license"]["op_code"]):
		cfg["license"]["passed"] = 1
	else:
		cfg["license"]["passed"] = 0
		print("You need license key for %s - %s"%(cfg["sensor"]["name"],cfg["sensor"]["model"]))
		
	homePath = cfg["path"]["webRoot"]+cfg["path"]["home"]
	logPath = cfg["path"]["webRoot"]+cfg["path"]["log"]
	imgPath = cfg["path"]["webRoot"]+cfg["path"]["img"]
	jsonPath = cfg["path"]["webRoot"]+cfg["path"]["json"]
	configPath = cfg["path"]["webRoot"]+cfg["path"]["config"]
	
	try:
		## 폴더 생성
		if not os.path.exists(homePath): # homePath 폴더 생성
			os.makedirs(homePath)
		if not os.path.exists(logPath): # logPath 폴더 생성
			os.makedirs(logPath)
		if not os.path.exists(imgPath): # imgPath 폴더 생성
			os.makedirs(imgPath)
		if not os.path.exists(jsonPath): # jsonPath 폴더 생성
			os.makedirs(jsonPath)
		if not os.path.exists(configPath): # configPath 폴더 생성
			os.makedirs(configPath)
			os.chmod(configPath, 0o757)
		
		## Index 링크 URL PHP 파일 생성
		shutil.copy("www/index.php", cfg["path"]["webRoot"])
		
		## Upload JSON PHP 파일 생성
		shutil.copy("www/upload.php", homePath)
		
		## PHP Reset 파일 복사
		shutil.copy("www/reset.php", homePath)
		
		## Http Request 응답 테스트
		shutil.copy("www/get_post_receiver.php", homePath)
		
		## Restart System 1초후에 리부팅
		shutil.copy("www/restart.php", homePath)
		
		## SpotterRF 로고파일 복사
		shutil.copy("www/image"+cfg["file"]["img_logo_home"], imgPath)
		## 웹에서 업로드시 쓰기 오류 예방 차원에서 쓰기허용
		os.chmod(imgPath+cfg["file"]["img_logo_home"], 0o646)
		
		## Optex 로고파일 복사
		shutil.copy("www/image"+cfg["file"]["img_logo_main"], imgPath)
		## 웹에서 업로드시 쓰기 오류 예방 차원에서 쓰기허용
		os.chmod(imgPath+cfg["file"]["img_logo_main"], 0o646)
		
		## 설정(config.json)파일 복사
		if os.path.exists(configPath+cfg["file"]["config"]):
			cfg = readConfig(configPath) ## 사용자 환경변수가 있으면 기존변수를 사용자 변수로 변경
		else:
			shutil.copy("."+cfg["file"]["config"], configPath)
			## 웹에서 업로드시 쓰기 오류 예방 차원에서 쓰기허용
			os.chmod(configPath+cfg["file"]["config"], 0o646)
		# shutil.copy("."+cfg["file"]["config"], configPath)
		# ## 웹에서 업로드시 쓰기 오류 예방 차원에서 쓰기허용
		# os.chmod(configPath+cfg["file"]["config"], 0o646)
		
	except:
		exit("Access permission error %s"%cfg["path"]["webRoot"])
		
	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	logger = logging.getLogger(cfg["sensor"]["name"]) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = logPath+'/'+cfg["sensor"]["name"]+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info("START") 
	# logger.debug("===========================")
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	# logger.debug("===========================")
	# logger.info("TEST END!")
	############ logging ################
	
	###############################################
	## 이전에 실행되고 있는 프로그램 제거
	kill_its_spotter(cfg["interface"]["portOut"])
	
	## actionLog 내용 지우기
	del cfg["actionLog"][:]
	
	## USB to Ethernet Interface Check
	print ("\n\tInterface Check %s"%cfg["interface"]["portAddr"])
	if check_ping(cfg["interface"]["portAddr"]): ## 센서 
		logger.info("Pass Interface Check(%s)."%cfg["interface"]["portAddr"])
		print ("\n\tPass Interface Check")
		cfg["actionLog"].append( "%s Pass Interface Check."%str(time.time()) )
	else:
		logger.warning("Error Interface Check(%s)."%cfg["interface"]["portAddr"])
		print ("\n\tError Interface Check")
		cfg["actionLog"].append( "%s Error Interface Check."%str(time.time()) )
	
	## Sensor Connection Test
	print ("\n\tSensor Connection Check %s"%cfg["sensor"]["addr"])
	if check_ping(cfg["sensor"]["addr"]): ## 센서 테스트 결과 값
		logger.info("Pass Sensor Connection Check(%s)."%cfg["sensor"]["addr"])
		print ("\n\tPass Sensor Connection Check")
		cfg["actionLog"].append( "%s Pass Sensor Connection Check."%str(time.time()) )
		
		###############################################
		## 사용자 비번 포함된 센서 URL 생성
		if cfg["sensor"]["user"]:
			sensor_url = "http://%s:%s@%s"%(cfg["sensor"]["user"],cfg["sensor"]["pass"],cfg["sensor"]["addr"])
		else:
			sensor_url = "http://%s"%(cfg["sensor"]["addr"])
		
		###############################################
		## 관리자(admin) 비밀번호 설정 User:admin, Pass:its_iot
		if set_admin_pass(sensor_url): 
			print ("\n\tSet admin's password.")
			cfg["actionLog"].append( "%s Set admin's password."%str(time.time()) )
		
		###############################################
		## geolocation 설정
		payload = { "latitude":0, "longitude":0, "altitude":0, "declination":0, "acquireGpsOnBoot":False, "bearing":0, "acquireOrientationOnBoot":False }
		if set_geolocation(sensor_url,payload): 
			print ("\n\tSet geolocation informations.")
			cfg["actionLog"].append( "%s Set geolocation informations."%str(time.time()) )
		
		###############################################
		## push notifications(tracks) 설정
		payload = { "protocol":"tcp:", "hostname":cfg["interface"]["portAddr"], "port":cfg["interface"]["portIn"] } ## 기본네트워트 아이피 활성
		if set_push_tracks(sensor_url,payload): 
			print ("\n\tSet push notifications(tracks).")
			cfg["actionLog"].append( "%s Set push notifications(tracks)."%str(time.time()) )

	else: ## 센서확인 않됨
		logger.warning("Error Sensor Connection Check(%s)."%cfg["sensor"]["addr"])
		print ("\n\tError Sensor Connection Check")
		cfg["actionLog"].append( "%s Error Sensor Connection Check."%str(time.time()) )
	
	# ## 로컬 영영의 카메라 찾기
	# print ("\n\tFind Camera in Local Network")
	# cameraList = check_opened_port('CAMERA')
	# if len(cameraList):
		# cfg["camera"]["addr"] = cameraList[0]
		# print ("\n\tSet Camera's IP %s"%cfg["camera"]["addr"])
		# logger.info("Set Camera's IP %s"%cfg["camera"]["addr"])
		# cfg["actionLog"].append( "%s Set Camera's IP %s."%(str(time.time()),cfg["camera"]["addr"]) )
	# else:
		# ## 실패하면 기본 카메라 주소를 유지 한다.
		# # cfg["camera"]["addr"] = ""
		# print ("\n\tNot Found Camera in Local Area")
		# logger.warning("Not Found Camera in Local Area")
		# cfg["actionLog"].append( "%s Not Found Camera in Local Area."%str(time.time()) )
		
	###############################################
	
	saveConfig(cfg) ## 환경변수 저장
	
		
	
	main()
