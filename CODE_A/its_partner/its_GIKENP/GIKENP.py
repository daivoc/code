#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import socket 
import time
import datetime
import json
import MySQLdb
import subprocess 
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
GPIO.setwarnings(False)

import numpy as np
import urllib
import cv2
import threading
import multiprocessing
import shutil
from warnings import filterwarnings

import logging
import logging.handlers

filterwarnings('ignore', category = MySQLdb.Warning)

def run_demon_GIKENP_JS(cfgJson): 
	cmd = "node %s/GIKENP.js %s 2>&1 & " % (share['path']['gikenp'],cfgJson)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

###################################
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName): # 
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

###################################
# GPWIO 이벤트 전송
# relayAction() --> relayOutDueTo() --> insert_socket_GPWIO() --> Port of GPWIO
def insert_socket_GPWIO(id, status, msg): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		# node.connect((ip,port))
		node.connect(('localhost', owner['port']['gpwio']['portIn']))
		msg_data = ('id=%s,status=%s,msg=%s' % (id, status, msg))
		# print msg_data
		return node.send(msg_data) 
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 

def relayOutFixed(port, value): # GPIO Port No. , value 0: on, 1: off
	insert_socket_GPWIO(id=port, status=value, msg='')

def relayOutDueTo(port, druation): # GPIO Port No. , Action Due
	insert_socket_GPWIO(id=port, status=owner['gpio']['swOn'], msg='')
	time.sleep(druation)
	insert_socket_GPWIO(id=port, status=owner['gpio']['swOff'], msg='')

# 아직 적용 안됨
def apiCustom(addr, port, content):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((addr, port))
		s.send(content)
		recv = s.recv(1024) 
		s.close() 
		return recv
	except socket.error:
		return "Socket Error {0}".format(addr)
	except socket.timeout:
		return "Timeout Error {0}".format(addr)
	finally:
		s.close() 

# 아직 적용 안됨
def httpRequest(method_name, url, dict_data, is_urlencoded=True):
	"""Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
	"""
	url  = 'http://192.168.0.80:9991' # 접속할 사이트주소 또는 IP주소를 입력한다 
	data = {'uid':'Happy','pid':'Birth','sid':'Day'}         # 요청할 데이터
	response = httpRequest(method_name='GET/POST', url=url, dict_data=data)
	"""

	try:
		if method_name == 'GET': # GET방식인 경우
			response = requests.get(url=url, params=dict_data)
		elif method_name == 'POST': # POST방식인 경우
			if is_urlencoded is True:
				response = requests.post(url=url, data=dict_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
			else:
				response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})
		return response
	except requests.exceptions.Timeout:
		# Maybe set up for a retry, or continue in a retry loop
		return "Timeout Error {0}".format(url)
	except requests.exceptions.TooManyRedirects:
		# Tell the user their URL was bad and try a different one
		return "Bad URL Error {0}".format(url)
	except requests.exceptions.RequestException as e:
		# catastrophic error. bail.
		# raise SystemExit(e)
		return "Request Error {0}".format(url)
	except:
		return "Unknown Error {0}".format(url)
		
###################################
## 활성화된 모니터링서버(IMS)에 데이터 전송
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
def insert_socket_GIKEN(data): 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect(('localhost', owner['interface']['port_JS_in'])) # sock.connect((ip,port))
		return sock.sendall(data) 
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

####### 실시간 알람 접점신호 발생 #######
## 1:Gate, 6:Alarm, 7:Alarm+Camera, 9:Alarm+Camera+Report
## ID:0(gate), 1(Alarm), 2(Camera), 3(Report)
## relayAction() --> relayOutDueTo() --> insert_socket_GPWIO() --> Port of GPWIO
def relayAction(status, flag=0): # 0:초기화, 1:Gate, 6:Alarm, 7:Alarm+Camera, 9:Alarm+Camera+Report
	if status == 1: # Inner
		if owner['gpio']['out_time']['0'] > 0:
			relayOutDueTo(owner['gpio']['out_id']['0'],owner['gpio']['out_time']['0'])
			# multiprocessing.Process(target=relayOutDueTo, args=(owner['gpio']['out_id']['0'],owner['gpio']['out_time']['0'])).start()
	elif status == 2: # Outer
		if owner['gpio']['out_time']['1'] > 0: 
			relayOutDueTo(owner['gpio']['out_id']['1'],owner['gpio']['out_time']['1'])
			# multiprocessing.Process(target=relayOutDueTo, args=(owner['gpio']['out_id']['1'],owner['gpio']['out_time']['1'])).start()
	elif status == 3: # Unknown
		if owner['gpio']['out_time']['2'] > 0: # Unknown
			relayOutDueTo(owner['gpio']['out_id']['2'],owner['gpio']['out_time']['2'])
			# multiprocessing.Process(target=relayOutDueTo, args=(owner['gpio']['out_id']['2'],owner['gpio']['out_time']['2'])).start()
	elif status == 4: # 라이트 - twilight
		if owner['gpio']['out_time']['3']: # Twilight Enable
			relayOutFixed(owner['gpio']['out_id']['3'],flag)
			# multiprocessing.Process(target=relayOutFixed, args=(owner['gpio']['out_id']['3'],flag)).start()


# ####### 실시간 스넵샷 #######
# ## 부정입실시 사진저장
# def unknownShot(path,color): # color:0(gray), 1(color)
# 	dateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") # UTC - 센서 요청시간대
# 	try:
# 		os.makedirs(path+'/'+dateTime[0:10])
# 	except:
# 		pass # directory already exists

# 	try: # putText 한글(유니코드)등록시 오류 발생함
# 		getImage = cv_image_from_url(owner['opencv']['live_url'], color) # 칼라 이미지
# 		cv2.putText(getImage,dateTime,(10,16),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),1,cv2.LINE_AA) # 워터마크
# 		cv2.putText(getImage,owner['its']['subject'],(10,32),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,255),1,cv2.LINE_AA) # 워터마크 description
# 		cv2.imwrite(path+'/'+dateTime[0:10]+'/{}.jpg'.format(dateTime[11:20]), getImage)
# 		return(dateTime[0:10]+'/{}.jpg'.format(dateTime[11:20])) # 최종 저장된 이미지
# 	except:
# 		logger.info("Snapshot Error")
# 		return None

# ####### 테일링 스넵샷 #######
# # Anti Tailing Function
# # 테스트에 의한 기켄의 스넵샷 주기는 평균 0.03초이다.
# # 기켄 자체로드 및 ITS로드를 감안하여 0.05 ~ 0,1초 까지를 안전주기로 가정 한다.
# # 입실시간(카드키 테깅후 출구로 나간 시간)를 평균 2초로 하면
# # 테일링 검증을 위한 스넵샷 수는 2/0.1 ~ 2/0.05 즉 20프레임 ~ 40프레임을 예측 할수 있다.
# # 여기에는 이미지 검증에 필요한 시간을 대략적으로 감안 한것으로 프레임 수는 더 적어질수 있다
# def tailingShot(): # 네트워크 이미지 레코더
# 	dateTime = datetime.datetime.now().strftime("%H:%M:%S.%f") # UTC - 센서 요청시간대
# 	gray = cv_image_from_url(owner['opencv']['live_url'], 0) # 그레이 이미지
# 	crop = gray[owner['opencv']['tail_y']:owner['opencv']['tail_h'], owner['opencv']['tail_x']:owner['opencv']['tail_w']]

# 	# 차등값 추출
# 	diffImage = cv2.subtract(live['tailImg'], crop)

# 	if owner['opencv']['threshold'] > 0:
# 		_,thresh = cv2.threshold(diffImage,owner['opencv']['threshold'],255,cv2.THRESH_BINARY_INV)
# 	else: # 자동 트레솔드
# 		_,thresh = cv2.threshold(diffImage,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 	# 스파클(noise) 제거 및 이미지 반전 https://copycoding.tistory.com/156
# 	if owner['opencv']['img_filter'] > 0:
# 		kernel = np.ones((owner['opencv']['img_filter'], owner['opencv']['img_filter']), np.uint8)
# 		unNoise = cv2.dilate(thresh, kernel, iterations = 1)
# 		# 비트 반전(주변을 검은색으로)
# 		finImage = cv2.bitwise_not(unNoise) 
# 	else:
# 		finImage = cv2.bitwise_not(thresh) 

# 	## 힌색 픽셀 갯수 확인
# 	p = cv2.countNonZero(finImage)
# 	# 오브젝트 위치와 치수
# 	x,y,w,h = cv2.boundingRect(finImage) # left, top, width, height

# 	# if p or x or y or w or h:
# 	live['tailNumpy'] = np.append(live['tailNumpy'], np.array([[p,x,y,w,h]]), axis=0)
	
# 	# if owner['opencv']['iLog_mode']: ## image log 모드이면 저장
# 	# 	cv2.imwrite(owner['file']['image_tailing']+'/'+dateTime+'.jpg', finImage)

# 	# data = get_sensor_image()
# 	# if data:
# 	# 	with open(owner['file']['image_tailing']+'/'+dateTime+'.jpg', 'w') as f:
# 	# 		f.write(data)
# 	# 	return True
# 	# else:
# 	# 	return False

# def statusAntiDenial(): # GPIO IN S/W 3(gpio:6) - 안티 디나이얼
# 	return GPIO.input(6) ## channel == 6: id = 2 ## 안티 디나이얼

## 임시버퍼(live['liveCountIn'])에 저장된 시간이 사용자 선언값(reset_interval)을 초과 하였는지 확인
# def reset_count(): # live['liveCountIn'] 값을 live['liveTimerIn'] 조건에 따라 초기화 한다.
# 	for id in range(8):
# 		if live['liveCountIn'][id]:
# 			timerDelta = (datetime.datetime.now() - live['liveTimerIn'][id]).total_seconds() # Delta 차이깂
# 			if timerDelta > owner['gpio']['reset_interval']: # 사전정의된 시간차
# 				# print 'Reset Count id:{}'.format(id)
# 				logger.info("Reset Timeout Counts")
# 				# 타임아웃 !!
# 				live['liveCountIn'][id] = 0
# 				# 모니터링 : 활성화된 브라우저로 전송
# 				jsonData = {}
# 				jsonData['keyCount'] = {}
# 				jsonData['keyCount'][id] = live['liveCountIn'][id] #
# 				json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 				insert_socket_GIKEN(json_dump)

# 				live['cntDenial'][id]= 0
# 				# 모니터링 : 활성화된 브라우저로 전송
# 				jsonData = {}
# 				jsonData['denialCount'] = {}
# 				jsonData['denialCount'][id] = live['cntDenial'][id] #
# 				json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 				insert_socket_GIKEN(json_dump)

# ## 알람 정보가 등록되어있으면 [출력]포트 초기화
# def init_all_GPIO_out(): ## status 1:HIGH, 0:LOW
# 	tmpLog = 'Init Relay: ' # 
# 	for id in owner['gpio']['out_id']:
# 		gpioID = owner['gpio']['out_id'][id]
# 		try: # GPIO 포트 초기화
# 			GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
# 			GPIO.setup(gpioID, GPIO.OUT)
# 			if owner['gpio']['outStatus'][id]:
# 				GPIO.output(gpioID, GPIO.HIGH)
# 			else:
# 				GPIO.output(gpioID, GPIO.LOW)
# 			tmpLog += "PassID:{}->{}, ".format(id, owner['gpio']['outStatus'][id])
# 		except:
# 			continue
# 			tmpLog += "ErrorID:{}->{}, ".format(id, owner['gpio']['outStatus'][id])
# 	return tmpLog

# ## [입력]포트 초기화
# def init_all_GPIO_in():
# 	bounceTime = owner['gpio']['bounce'] # msec 밀리초

# 	# [입력]포트 초기화
# 	tmpLog = 'Init GPIO_in: '
# 	for id in owner['gpio']['in_id']:
# 		gpioID = owner['gpio']['in_id'][id]
# 		try: # GPIO 포트 초기화
# 			GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering

# 			# GPIO.PUD_UP, GPIO.PUD_DOWN, GPIO.PUD_OFF
# 			GPIO.setup(gpioID, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
# 			# GPIO.add_event_detect, RISING/FALLING/BOTH, bouncetime :튐현상 제거. 1000 = 1초
# 			GPIO.add_event_detect(gpioID, GPIO.BOTH, callback=GPIO_in_handler, bouncetime=bounceTime) 
# 			tmpLog += ' ID:{},#:{},'.format(id,gpioID)
# 		except:
# 			tmpLog += ' Error ID:{},#:{},'.format(id,gpioID)

# 	return tmpLog
	
# # 콜백에 의한 변수로 GPIO ID(BCM)가 channel에 
# # 릴레이 입력이 들어오면 ..
# def GPIO_in_handler(channel): 
# 	if channel == 19:
# 		id = 0 
# 	else:
# 		return
# 	# if channel == 19: id = 0 ## 카드키 나 지문 인식 또는 외부로 부터의 접점이벤트
# 	# if channel == 13: id = 1 ## 예약
# 	# if channel == 6: id = 2 ## 안티 디나이얼
# 	# if channel == 5: id = 3 ## 예약 안티 테일링
# 	# if channel == 22: id = 4 ## 예약
# 	# if channel == 27: id = 5 ## 예약
# 	# if channel == 17: id = 6 ## 예약
# 	# if channel == 4: id = 7 ## 예약

# 	if live['liveCountIn'][id]: # liveCountIn 선별은 혹시 있을 노이즈 제거를 위함임
# 		return

# 	## 사용자 컨트롤 상태에 따른 명령 거부
# 	## 모니터링을 통해 메뉴얼 설정이 가능하다.
# 	## 2021-04-28 13:51:34
# 	if owner['control']['setLock'] or owner['control']['setOpen']:
# 		msg = "User mode Lock:{} Open:{}".format(owner['control']['setLock'], owner['control']['setOpen'])
# 		messageToClient('control', msg)
# 	else:
# 		curStatus = GPIO.input(channel)

# 		# print curStatus, owner['gpio']['inTypeNC'][id]

# 		# 사용자설정(inTypeNC) 조건으로 NC/NO 동작을 유도 한다. 
# 		if curStatus == owner['gpio']['inTypeNC'][id]: ## 현재값 == 설정값
# 			# GPIO 이벤트 발생시 횟수를 취합, 
# 			# 일정시간이 지나면 리셋한다.
# 			# global live['liveTimerIn'], live['liveCountIn']
# 			timerInN = datetime.datetime.now()
# 			timerInD = (timerInN - live['liveTimerIn'][id]).total_seconds() # Delta 차이값
# 			live['liveTimerIn'][id] = timerInN

# 			# OpenCV를 통해 접근자가 한명(isSingle) 인지를 확인하는 변수이다.
# 			# if owner['area']['alarm']['multiple']: #  다수 대기허용
# 			if owner['control']['antiDenial']: # -> if row['w_allow_multiple']
# 				## 복수접근 제어
# 				if statusAntiDenial(): ## 접점 3(2)번의 접지유무에 따라 
# 					#################
# 					## 디나이얼 확인
# 					#################
# 					if owner['opencv']['mask_mode']:
# 						isSingle = cv_multiple_filter() # 영상 테스트(이미지 검수) - 복수의 접근 시도
# 					else:
# 						isSingle = is_multiple_obj() # gikenInfo 테스트 - 복수의 접근 시도
# 				else:
# 					logger.info("Unlocked AntiDenial")
# 					isSingle = 1
# 			else:
# 				## multiple이 허용되면 무조건 1명으로 간주 한다.
# 				isSingle = 1 

# 			if owner['opencv']['mask_mode']:
# 				# cv_multiple_filter 사용시	
# 				if isSingle == 1: # 단수로 확인
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					# 게이트 개방
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					relayAction(1) 
# 					logger.info("Passed AntiDenial")

# 					live['liveCountIn'][id] = 1

# 					# 모니터링 : 활성화된 브라우저로 전송
# 					jsonData = {}
# 					jsonData['keyCount'] = {}
# 					jsonData['keyCount'][id] = live['liveCountIn'][id] #
# 					json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 					insert_socket_GIKEN(json_dump)
# 				elif isSingle == 2: # 다수로 확인
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					# 알람 발생
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					relayAction(6) 
# 					logger.info("Reject(Multiple)")

# 					live['cntDenial'][id] += 1

# 					# 모니터링 : 활성화된 브라우저로 전송
# 					jsonData = {}
# 					jsonData['denialCount'] = {}
# 					jsonData['denialCount'][id] = live['cntDenial'][id] #
# 					json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 					insert_socket_GIKEN(json_dump)
# 				elif isSingle == 3: # 기준이하의 이미지 데이터
# 					logger.info("Low Image Density")
# 				elif isSingle == 4: # 기준이하의 조도 데이터
# 					logger.info("Low Light Source")

# 				else: # 이미지 켑처 오류
# 					## 센서간 통신오류 메세지
# 					logger.info("Image Capture Error")
# 			else:
# 				## is_multiple_obj 사용시	
# 				if isSingle == 1: # 단수로 확인
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					# 게이트 개방
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					relayAction(1) 
# 					logger.info("Passed AntiDenial")

# 					live['liveCountIn'][id] = 1

# 					# 모니터링 : 활성화된 브라우저로 전송
# 					jsonData = {}
# 					jsonData['keyCount'] = {}
# 					jsonData['keyCount'][id] = live['liveCountIn'][id] #
# 					json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 					insert_socket_GIKEN(json_dump)
# 				elif isSingle > 1: # 다수로 확인
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					# 알람 발생
# 					# !!!!!!!!!!!!!!!!!!!!! #
# 					relayAction(6) 
# 					logger.info("Reject(Multiple)")

# 					live['cntDenial'][id] += 1

# 					# 모니터링 : 활성화된 브라우저로 전송
# 					jsonData = {}
# 					jsonData['denialCount'] = {}
# 					jsonData['denialCount'][id] = live['cntDenial'][id] #
# 					json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 					insert_socket_GIKEN(json_dump)
# 				else:
# 					## 센서간 통신오류 메세지
# 					logger.info("No Object")

# 			preStatus = [0,0,0,0,owner['control']['antiDenial']] # 초기화
# 			preStatus[isSingle] = 1
# 			insert_table_w_log_permit(owner['log_pmt']['tbl_live'], preStatus) # 데이터 추가

# 			if isSingle != 1: # 다중 이미지
# 				insert_table_w_log_sensor([0,0,0,1]) # 비허가

# 			# msg = "id:{} action:{}".format(id,isSingle)
# 			logger.info("GPIO Action No:{}, Set:{}, Current:{}".format(id + 1, owner['gpio']['inTypeNC'][id], curStatus))
			
# 		else:
# 			pass

# 		# # 스넵샷 매번 실행
# 		# with open(owner['file']['image_folder']+'/000.jpg', 'w') as f:
# 		# 	f.write(get_sensor_image())
# 	return

# ################################
# ## Live Count Down (Walk in)
# ################################
# def countDown(id,count):
# 	# 인원 및 시간 초과이면 알람
# 	# global live['liveTimerIn'], live['liveCountIn']
# 	msg=""
# 	status = [0,0,0] # [ approvedCount, unknownCount, timeoutCount ]
# 	if live['liveCountIn'][id] > 0: # 키 요청이 있는 경우
# 		timerInN = datetime.datetime.now()
# 		timerInD = (timerInN - live['liveTimerIn'][id]).total_seconds() # Delta 차이깂

# 		if timerInD > owner['gpio']['reset_interval']: # 타임 아웃 이면
# 			status[2] = 1
# 			msg = 'timeoutCount'
# 		else: # 유효한 시간 이내 이면
# 			if count > 1: # 기켄에서 멀티플 감지이면
# 				status[1] = 1
# 				msg = 'unknownCount'
# 			else: # 기켄에서 싱글 감지이면
# 				status[0] = 1
# 				msg = 'approvedCount'

# 		live['liveCountIn'][id] = 0
# 	else: # 승인이 없는 경우
# 		status[1] = 1
# 		msg = 'unknownCount'

# 	jsonData = {}
# 	jsonData[msg] = {}
# 	jsonData[msg][id] = count #
# 	json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
# 	insert_socket_GIKEN(json_dump)

# 	return status,msg # approvedCount, unknownCount, timeoutCount

# 모니터링을 위한 지도파일을 생성한다.
def make_GIKENP_map():
	jquery = '%s/jquery/jquery-3.1.1.min.js' % share['path']['common']
	__script_jquery_js__ = '<script>'+open(jquery, 'r').read()+'</script>'

	bootstrap_js = '%s/bootstrap/js/bootstrap.min.js' % share['path']['common']
	__style_bootstrap_js__ = '<script>'+open(bootstrap_js, 'r').read()+'</script>'
	bootstrap_css = '%s/bootstrap/css/bootstrap.min.css' % share['path']['common']
	__style_bootstrap_css__ = '<style>'+open(bootstrap_css, 'r').read()+'</style>'
	
	bootstrap_toggle_js = '%s/bootstrap/js/bootstrap-toggle.min.js' % share['path']['common']
	__style_bootstrap_toggle_js__ = '<script>'+open(bootstrap_toggle_js, 'r').read()+'</script>'
	bootstrap_toggle_css = '%s/bootstrap/css/bootstrap-toggle.min.css' % share['path']['common']
	__style_bootstrap_toggle_css__ = '<style>'+open(bootstrap_toggle_css, 'r').read()+'</style>'
	
	if owner['opencv']['tuner_mode']:
		# http://192.168.0.102/data/image/gikenP_g400t300_192_168_0_102_0001/1_img.png
		# 분석된 라이브 이미지와 원본 이미지 출력

		## 이미지를 주기적으로 저장한 이미지를 불러오는 기능
		__realtime_image__ = '''
		<div class="tuneComp">
		<img class="gikenComp" id="gikenImage">
		</div>
		<div class="tuneLive">
		<img class="gikenTune" id="liveImage">
		<img class="gikenTune" style="position:absolute;left:0" src="http://%s/data/image/gikenP_%s/%s">
		</div>
		<script>
		setInterval(function() { 
			document.getElementById("gikenImage").src = "http://%s/data/image/gikenP_%s/%s?rand=" + Math.random(); 
			document.getElementById("liveImage").src = "http://%s:%s/cgi-bin/trace.cgi?rand=" + Math.random();
		}, 250); 
		</script>
		''' % (owner['its']['bo_ip'],owner['its']['serial'],owner['file']['image_base'],owner['its']['bo_ip'],owner['its']['serial'],owner['file']['image_live'],owner['its']['bo_ip'],owner['interface']['port_MQ'])
	else:
		__realtime_image__ = '''
		<img class="gikenImage" id="liveImage">
		<script>
		setInterval(function() { 
			document.getElementById("liveImage").src = "http://%s:%s/cgi-bin/trace.cgi?rand=" + Math.random();
		}, 250); 
		</script>
		''' % (owner['its']['bo_ip'],owner['interface']['port_MQ'])

	# __realtime_image__ = '''
	# <img class="gikenImage" id="liveImage">
	# <script>
	# setInterval(function() { 
	# 	document.getElementById("liveImage").src = "http://%s:%s/cgi-bin/trace.cgi?rand=" + Math.random();
	# }, 250); 
	# </script>
	# ''' % (owner['its']['bo_ip'],owner['interface']['port_MQ'])

	with open(owner['file']['html_source'], 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_js__', __style_bootstrap_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css__', __style_bootstrap_css__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_toggle_js__', __style_bootstrap_toggle_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_toggle_css__', __style_bootstrap_toggle_css__)

		tmp_its_tmp = tmp_its_tmp.replace('__realtime_image__', __realtime_image__.encode('utf-8'))
		
		with open(owner['file']['html_target'], 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()

## 기켄센서 시간설정
def reset_sensor_time(time): 
	'''
	４－４－１ 시각설정 커맨드
		컬럼    내용    Size
		1       버전        2   “50”
		2       커맨드      3   “001” ：시각설정
		3       기기번호    8   시리얼번호
		4       데이터길이  8   “00000014”
		5       일시        14  “yyyymmddHHMMSS” (UTC)

	４－４－２ 시각설정 리스폰스
		컬럼    내용        Size
		1       버전        2 “50”
		2       커맨드      3 “001” ：시각설정
		3       에러코드    3 “000”：정상
		4       데이터길이  8 “00000000”
	'''
	command = '001'
	length = '00000014'
	msg = "%s%s%s%s%s"%(owner['sensor']['version'],command,owner['sensor']['serial'],length,time)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((owner['sensor']['ip'], owner['sensor']['port']))
		sock.send(msg) 
		while True:
			data = sock.recv(16)
			if data[5:8] == "000":
				return 1
			else:
				return 0
			return data.decode()
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

## 기켄센서 카운트데이터 클리어
def reset_sensor_data():
	'''
	４－２－１ 계수데이터 클리어 커맨드
		컬럼    내용        Size
		1       버전        2   “50”
		2       커맨드      3   “200” ：카운트데이터 클리어
		3       기기번호    8   시리얼번호
		4       데이터길이  8   “00000016”
		5       고정문자열  16  “BUFFERCLEAR00200”

	４－２－２ 계수데이터 클리어 리스폰스
		컬럼    내용        Size
		1       버전        2   “50”
		2       커맨드      3   “200” ：카운트데이터 클리어
		3       에러코드    3   “000”：정상
		4       데이터길이  8   “00000000”
	'''
	command = '200'
	length = '00000016'
	msg = "%s%s%s%s%s"%(owner['sensor']['version'],command,owner['sensor']['serial'],length,"BUFFERCLEAR00200")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((owner['sensor']['ip'], owner['sensor']['port']))
		sock.send(msg) 
		while True:
			data = sock.recv(16)
			if data[5:8] == "000":
				return 1
			else:
				return 0
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

## 기켄센서 카운트데이터 요구
def read_sensor_count(dateS, dateE): 
	'''
	４－３－１ 카운트데이터 요구커맨드
		컬럼    내용            Size
		1       버전             2   “50”
		2       커맨드           3   “201” ：계수데이터
		3       기기번호         8   시리얼번호
		4       데이터길이       8   “00000032”
		5       검색시작 일시   12   “yyyymmddHHMM”, “000000000000”로 가장 오래된 데이터
		6       검색종료 일시   12   “yyyymmddHHMM”, “999999999999”로 최신 데이터※1
		7       카운트           1   출력지정 1 “0”～”1” ※2
		8       카운트           2   출력지정 1 “0”～”1” ※2
		9       카운트           3   출력지정 1 “0”～”1” ※2
		10      카운트           4   출력지정 1 “0”～”1” ※2
		11      예비영역         4   “0000”

		# 50 201 00314490 00000032 202005120712 999999999999 1111 0000

		※1 최신데이터를 요구한 경우, 리스폰스의 제일 마지막 레코드에 미확정 데이터를 부가한다.
		1 분 이내의 간격으로 속보수치가 필요할 경우에 사용한다.
		※2 ”0”＝출력없음, ”1”＝출력있음

	４－３－２ 카운트 데이터 요구 리스폰스
		컬럼    내용            Size
		1       버전            2   “50”
		2       커맨드          3   “201”：계수데이터
		3       에러코드        3   “000”：정상
		4       데이터길이      8   “00000030” ～ 30＋레코드수×레코드사이즈
		5       미송신데이터    12 “000000000000” ※1
				선두일시
		6       레코드 수       8   “00000000”～
		7       레코드 사이즈   8   “00000000”～
		8       개행            2   CR(0x0D)＋LF(0x0A)
		9       카운트 데이터       레코드수×레코드사이즈

		※1 현시점의 센서 유닛 사양으로는 미송신 데이터는 발생하지 않기 때문에, 항상 0 이 설정됨.
	'''
	version = owner['sensor']['version']
	command = '201'
	serial = owner['sensor']['serial']
	length = '00000032'
	count = '1111'
	reserve = '0000'
	# 50201003037390000003200000000000099999999999911110000
	msg = "%s%s%s%s%s%s%s%s"%(version,command,serial,length,dateS,dateE,count,reserve)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((owner['sensor']['ip'], owner['sensor']['port']))
		sock.send(msg) 
		while True:
			data = sock.recv(128)
			return data.decode()
	except socket.error:
		return None
	except socket.timeout:
		return None
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
	version = owner['sensor']['version']
	command = '100'
	serial = owner['sensor']['serial']
	length = '00000002'
	imgType = '0' # 현재의 화상(320×240 컬러)
	imgStyle = '0' # JPEG 파일 이미지
	# 501000030373900000000200
	msg = "%s%s%s%s%s%s"%(version,command,serial,length,imgType,imgStyle)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((owner['sensor']['ip'], owner['sensor']['port']))
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
		return None
	except socket.timeout:
		return None
	finally:
		sock.close() 

## 데이터베이스 테이블 생성
def create_table_w_log_sensor(): 
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		tbl_w_log_sensor_sql = """
			CREATE TABLE IF NOT EXISTS %s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_approved` int(1) NOT NULL DEFAULT '0',
			`w_unknown` int(1) NOT NULL DEFAULT '0',
			`w_reverse` int(1) NOT NULL DEFAULT '0',
			`w_denial` int(1) NOT NULL DEFAULT '0',
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % owner['log_table']['tbl_log']
		cursor.execute(tbl_w_log_sensor_sql) # create table
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
 	except MySQLdb.Warning as warning:
		pass
	# finally:
	# 	cursor.close()
	# 	conn.close()

def insert_table_w_log_sensor(data): 
	query = "INSERT IGNORE INTO "+owner['log_table']['tbl_log']+"(w_approved,w_unknown,w_reverse,w_denial) VALUES(%s,%s,%s,%s)"
	args = (data[0],data[1],data[2],data[3])
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def create_table_w_log_giken(table): # share['srvHealth']['ip']
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		# conn = MySQLdb.connect(host=share['srvHealth']['ip'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
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
			`w_approved` int(11) NOT NULL DEFAULT '0',
			`w_unknown` int(11) NOT NULL DEFAULT '0',
			`w_timeout` int(11) NOT NULL DEFAULT '0',
			`w_ymdhm` varchar(12) DEFAULT NULL,
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % table
		cursor.execute(tbl_w_log_sensor_sql) # create table
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
 	except MySQLdb.Warning as warning:
		pass
	# finally:
	# 	cursor.close()
	# 	conn.close()

def insert_table_w_log_giken(table, data): 
	# https://stackoverflow.com/questions/14215474/query-to-select-current-and-previous-hour-day-and-month?rq=1
	# https://stackoverflow.com/questions/1945722/selecting-between-two-dates-within-a-datetime-field-sql-server/1945749
	query = "INSERT IGNORE INTO "+table+"(w_ax_cnt,w_xa_cnt,w_bx_cnt,w_xb_cnt,w_cx_cnt,w_xc_cnt,w_dx_cnt,w_xd_cnt,w_approved,w_unknown,w_timeout,w_ymdhm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11].ljust(12, '0'))
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def insert_table_w_log_giken_server(host, port, user, passwd, name, table, data, serial): # w_subject <- owner['its']['subject']
	# https://stackoverflow.com/questions/14215474/query-to-select-current-and-previous-hour-day-and-month?rq=1
	# https://stackoverflow.com/questions/1945722/selecting-between-two-dates-within-a-datetime-field-sql-server/1945749
	# query = "INSERT IGNORE INTO "+table+"(w_ax_cnt,w_xa_cnt,w_bx_cnt,w_xb_cnt,w_cx_cnt,w_xc_cnt,w_dx_cnt,w_xd_cnt,w_approved,w_unknown,w_timeout,w_ymdhm,w_serial) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	# args = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11].ljust(12, '0'),serial)
	query = "INSERT IGNORE INTO "+table+"(w_subject,w_ax_cnt,w_xa_cnt,w_bx_cnt,w_xb_cnt,w_cx_cnt,w_xc_cnt,w_dx_cnt,w_xd_cnt,w_approved,w_unknown,w_timeout,w_ymdhm,w_serial) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (owner['its']['subject'],data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11].ljust(12, '0'),serial)
	try:
		conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('Remote SQL Server Error {} {}'.format(owner['its']['subject'], error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def insert_table_w_log_permit_server(host, port, user, passwd, name, table, data, serial): 
	query = "INSERT IGNORE INTO "+table+"(w_no_image,w_single,w_multiple,w_low_density,w_anti_denial,w_serial) VALUES(%s,%s,%s,%s,%s,%s)"
	args = (data[0],data[1],data[2],data[3],data[4],serial) # no_image,single,multiple,low_density,anti_denial
	try:
		conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('Remote SQL Server Error {} {}'.format(serial, error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def create_table_w_log_permit(table): 
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
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
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % table
		cursor.execute(tbl_w_log_sql) # create table
		conn.commit()
		conn.close()
		return cursor.lastrowid
		
	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
 	except MySQLdb.Warning as warning:
		pass
	# finally:
	# 	cursor.close()
	# 	conn.close()

def insert_table_w_log_permit(table, data): 
	query = "INSERT IGNORE INTO "+table+"(w_no_image,w_single,w_multiple,w_low_density,w_anti_denial) VALUES(%s,%s,%s,%s,%s)"
	args = (data[0],data[1],data[2],data[3],data[4]) # no_image,single,multiple,low_density,anti_denial
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		conn.close()
		return cursor.lastrowid

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def delete_older_days(table, days): 
	## 일정 기간 이후의 자료를 모두 삭제 한다.
	# SELECT * FROM `w_log_gikenP_live_00303739` WHERE `w_stamp` < NOW() -INTERVAL 1 DAY
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		query = "DELETE FROM " + table + " WHERE `w_stamp` < NOW() -INTERVAL " + str(days) + " DAY "
		cursor.execute(query) # create table
		conn.commit()
		# return cursor.lastrowid
		conn.close()
		
	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
 	except MySQLdb.Warning as warning:
		pass
	# finally:
	# 	cursor.close()
	# 	conn.close()

def read_today_sum(): 
	# 오늘의 통계 (approved)
	query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt FROM "+owner['log_table']['tbl_live']+" WHERE DATE(`w_stamp`) = CURDATE() AND `w_approved` > 0 "

	# 오늘의 통계 (unknown)
	query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt FROM "+owner['log_table']['tbl_live']+" WHERE DATE(`w_stamp`) = CURDATE() AND `w_unknown` > 0 "

	# 오늘의 통계 (denial)
	query_denial = "SELECT IFNULL(SUM(w_multiple),0)AS w_multiple FROM "+owner['log_pmt']['tbl_live']+" WHERE DATE(`w_stamp`) = CURDATE() "
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()

		# 정상 통과자 추가분 확인
		cursor.execute(query_approved)
		conn.commit()
		row = cursor.fetchone()
		live['tSum']['todaySumA'] = int(row[0]) # 오늘 들어간 사람 계

		# 부정 통과자 추가분 확인
		cursor.execute(query_unknown)
		conn.commit()
		row = cursor.fetchone()
		live['tSum']['todaySumU'] = int(row[0]) # 오늘 부정 접근한 사람 계
		live['tSum']['todaySumR'] = int(row[1]) # 오늘 나온 사람 계

		# 비승인자 추가분 확인
		cursor.execute(query_denial)
		conn.commit()
		row = cursor.fetchone()
		live['tSum']['todaySumD'] = int(row[0]) # 오늘 들어간 사람 계
		conn.close()
		
	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

def read_minute_sum(): 
	# 이전의 1분간 통계(approved)
	query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 MINUTE, '%Y%m%d%H%i') AS PrevHour FROM "+owner['log_table']['tbl_live']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:00') - INTERVAL 1 MINUTE AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:00') AND `w_approved` > 0 "
	# 이전의 1분간 통계(unknown)
	query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 MINUTE, '%Y%m%d%H%i') AS PrevHour FROM "+owner['log_table']['tbl_live']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:00') - INTERVAL 1 MINUTE AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:00') AND `w_unknown` > 0 "
	# 이전의 1분간 통계(denial)
	query_denial = "SELECT IFNULL(SUM(w_no_image),0)AS w_no_image, IFNULL(SUM(w_single),0)AS w_single, IFNULL(SUM(w_multiple),0)AS w_multiple, IFNULL(SUM(w_low_density),0)AS w_low_density, IFNULL(SUM(w_anti_denial),0)AS w_anti_denial FROM "+owner['log_pmt']['tbl_live']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:00') - INTERVAL 1 MINUTE AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:00') "
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()

		# 승인자 추가분 확인
		cursor.execute(query_approved)
		conn.commit()
		row_approved = cursor.fetchone()
		hasVal_approved = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_approved += int(row_approved[i])
		if hasVal_approved:
			insert_table_w_log_giken(owner['log_table']['tbl_min'], row_approved)

		# 비승인자 추가분 확인
		cursor.execute(query_unknown)
		conn.commit()
		row_unknown = cursor.fetchone()
		hasVal_unknown = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_unknown += int(row_unknown[i])
		if hasVal_unknown:
			insert_table_w_log_giken(owner['log_table']['tbl_min'], row_unknown)

		# 부정접근자 추가분 확인
		cursor.execute(query_denial)
		conn.commit()
		row_denial = cursor.fetchone()
		hasVal_denial = 0
		for i in range(0, 4):
			hasVal_denial += int(row_denial[i])
		if hasVal_denial: # 내용이 있을때만 저장
			insert_table_w_log_permit(owner['log_pmt']['tbl_min'], row_denial)
		conn.close()
		
	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

	##  이벤트 통합 서버로 실시간 데이터 베이스 등록
	if hasVal_approved:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_min", row_approved, int(owner['sensor']['serial']))
				# print row_approved
	if hasVal_unknown:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_min", row_unknown, int(owner['sensor']['serial']))
				# print row_unknown

	if hasVal_denial:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_permit_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_permit_min", row_denial, int(owner['sensor']['serial']))
				# print row_denial

def read_hourly_sum(): 
	# 이전의 한시간 통계
	query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 HOUR, '%Y%m%d%H') AS PrevHour FROM "+owner['log_table']['tbl_min']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') - INTERVAL 1 HOUR AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') AND `w_approved` > 0 "
	query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 HOUR, '%Y%m%d%H') AS PrevHour FROM "+owner['log_table']['tbl_min']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') - INTERVAL 1 HOUR AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') AND `w_unknown` > 0 "
	query_denial = "SELECT IFNULL(SUM(w_no_image),0)AS w_no_image, IFNULL(SUM(w_single),0)AS w_single, IFNULL(SUM(w_multiple),0)AS w_multiple, IFNULL(SUM(w_low_density),0)AS w_low_density, IFNULL(SUM(w_anti_denial),0)AS w_anti_denial FROM "+owner['log_pmt']['tbl_min']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') - INTERVAL 1 HOUR AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') "
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()

		# cursor.execute(query_approved)
		# conn.commit()
		# row = cursor.fetchone()
		# hasValue = 0
		# for i in range(0, 8):
		# 	hasValue += int(row[i])
		# if hasValue:
		# 	insert_table_w_log_giken(owner['log_table']['tbl_hour'], row)

		# cursor.execute(query_unknown)
		# conn.commit()
		# row = cursor.fetchone()
		# hasValue = 0
		# for i in range(0, 8):
		# 	hasValue += int(row[i])
		# if hasValue:
		# 	insert_table_w_log_giken(owner['log_table']['tbl_hour'], row)

		# # 부정접근자 추가분 확인
		# cursor.execute(query_denial)
		# conn.commit()
		# row = cursor.fetchone()
		# hasValue = 0
		# for i in range(0, 4):
		# 	hasValue += int(row[i])
		# if hasValue: # 내용이 있을때만 저장
		# 	insert_table_w_log_permit(owner['log_pmt']['tbl_hour'], row)



		# 승인자 추가분 확인
		cursor.execute(query_approved)
		conn.commit()
		row_approved = cursor.fetchone()
		hasVal_approved = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_approved += int(row_approved[i])
		if hasVal_approved:
			insert_table_w_log_giken(owner['log_table']['tbl_hour'], row_approved)

		# 비승인자 추가분 확인
		cursor.execute(query_unknown)
		conn.commit()
		row_unknown = cursor.fetchone()
		hasVal_unknown = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_unknown += int(row_unknown[i])
		if hasVal_unknown:
			insert_table_w_log_giken(owner['log_table']['tbl_hour'], row_unknown)

		# 부정접근자 추가분 확인
		cursor.execute(query_denial)
		conn.commit()
		row_denial = cursor.fetchone()
		hasVal_denial = 0
		for i in range(0, 4):
			hasVal_denial += int(row_denial[i])
		if hasVal_denial: # 내용이 있을때만 저장
			insert_table_w_log_permit(owner['log_pmt']['tbl_hour'], row_denial)
		conn.close()
		
	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()


	##  이벤트 통합 서버로 실시간 데이터 베이스 등록
	if hasVal_approved:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_hour", row_approved, int(owner['sensor']['serial']))
				# print row_approved
	if hasVal_unknown:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_hour", row_unknown, int(owner['sensor']['serial']))
				# print row_unknown

	if hasVal_denial:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_permit_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_permit_hour", row_denial, int(owner['sensor']['serial']))
				# print row_denial

def read_daily_sum(): 
	# 어제의 통계
	query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 DAY, '%Y%m%d') AS PreviousDate FROM "+owner['log_table']['tbl_hour']+" WHERE `w_stamp` BETWEEN CURDATE() - INTERVAL 1 DAY AND CURDATE() AND `w_approved` > 0 "
	query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 DAY, '%Y%m%d') AS PreviousDate FROM "+owner['log_table']['tbl_hour']+" WHERE `w_stamp` BETWEEN CURDATE() - INTERVAL 1 DAY AND CURDATE() AND `w_unknown` > 0 "
	query_denial = "SELECT IFNULL(SUM(w_no_image),0)AS w_no_image, IFNULL(SUM(w_single),0)AS w_single, IFNULL(SUM(w_multiple),0)AS w_multiple, IFNULL(SUM(w_low_density),0)AS w_low_density, IFNULL(SUM(w_anti_denial),0)AS w_anti_denial FROM "+owner['log_pmt']['tbl_hour']+" WHERE `w_stamp` BETWEEN CURDATE() - INTERVAL 1 DAY AND CURDATE() "
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()

		# cursor.execute(query_approved)
		# conn.commit()
		# row = cursor.fetchone()
		# hasValue = 0
		# for i in range(0, 8):
		# 	hasValue += int(row[i])
		# if hasValue:
		# 	insert_table_w_log_giken(owner['log_table']['tbl_day'], row)
		
		# cursor.execute(query_unknown)
		# conn.commit()
		# row = cursor.fetchone()
		# hasValue = 0
		# for i in range(0, 8):
		# 	hasValue += int(row[i])
		# if hasValue:
		# 	insert_table_w_log_giken(owner['log_table']['tbl_day'], row)

		# # 부정접근자 추가분 확인
		# cursor.execute(query_denial)
		# conn.commit()
		# row = cursor.fetchone()
		# hasValue = 0
		# for i in range(0, 4):
		# 	hasValue += int(row[i])
		# if hasValue: # 내용이 있을때만 저장
		# 	insert_table_w_log_permit(owner['log_pmt']['tbl_day'], row)


		# 승인자 추가분 확인
		cursor.execute(query_approved)
		conn.commit()
		row_approved = cursor.fetchone()
		hasVal_approved = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_approved += int(row_approved[i])
		if hasVal_approved:
			insert_table_w_log_giken(owner['log_table']['tbl_day'], row_approved)

		# 비승인자 추가분 확인
		cursor.execute(query_unknown)
		conn.commit()
		row_unknown = cursor.fetchone()
		hasVal_unknown = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_unknown += int(row_unknown[i])
		if hasVal_unknown:
			insert_table_w_log_giken(owner['log_table']['tbl_day'], row_unknown)

		# 부정접근자 추가분 확인
		cursor.execute(query_denial)
		conn.commit()
		row_denial = cursor.fetchone()
		hasVal_denial = 0
		for i in range(0, 4):
			hasVal_denial += int(row_denial[i])
		if hasVal_denial: # 내용이 있을때만 저장
			insert_table_w_log_permit(owner['log_pmt']['tbl_day'], row_denial)
		conn.close()
		
	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

	##  이벤트 통합 서버로 실시간 데이터 베이스 등록
	if hasVal_approved:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_day", row_approved, int(owner['sensor']['serial']))
				# print row_approved
	if hasVal_unknown:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_day", row_unknown, int(owner['sensor']['serial']))
				# print row_unknown

	if hasVal_denial:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_permit_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_permit_day", row_denial, int(owner['sensor']['serial']))
				# print row_denial

def read_weekly_sum():
	query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 7 DAY, '%Y%m%d') AS PrevWeek FROM "+owner['log_table']['tbl_day']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d 00:00:00') - INTERVAL 7 DAY AND DATE_FORMAT(NOW(), '%Y-%m-%d 00:00:00') AND `w_approved` > 0 "
	query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 7 DAY, '%Y%m%d') AS PrevWeek FROM "+owner['log_table']['tbl_day']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d 00:00:00') - INTERVAL 7 DAY AND DATE_FORMAT(NOW(), '%Y-%m-%d 00:00:00') AND `w_unknown` > 0 "
	query_denial = "SELECT IFNULL(SUM(w_no_image),0)AS w_no_image, IFNULL(SUM(w_single),0)AS w_single, IFNULL(SUM(w_multiple),0)AS w_multiple, IFNULL(SUM(w_low_density),0)AS w_low_density, IFNULL(SUM(w_anti_denial),0)AS w_anti_denial FROM "+owner['log_pmt']['tbl_day']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-%d 00:00:00') - INTERVAL 7 DAY AND DATE_FORMAT(NOW(), '%Y-%m-%d 00:00:00') "
	# CURDATE() - INTERVAL 7 DAY AND CURDATE()
	# DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00') - INTERVAL 7 DAY AND DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00')
	# print query_approved
	# print query_unknown
	# print query_denial

	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()

		# 승인자 추가분 확인
		cursor.execute(query_approved)
		conn.commit()
		row_approved = cursor.fetchone()
		hasVal_approved = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_approved += int(row_approved[i])
		if hasVal_approved:
			insert_table_w_log_giken(owner['log_table']['tbl_week'], row_approved)

		# 비승인자 추가분 확인
		cursor.execute(query_unknown)
		conn.commit()
		row_unknown = cursor.fetchone()
		hasVal_unknown = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_unknown += int(row_unknown[i])
		if hasVal_unknown:
			insert_table_w_log_giken(owner['log_table']['tbl_week'], row_unknown)

		# 부정접근자 추가분 확인
		cursor.execute(query_denial)
		conn.commit()
		row_denial = cursor.fetchone()
		hasVal_denial = 0
		for i in range(0, 4):
			hasVal_denial += int(row_denial[i])
		if hasVal_denial: # 내용이 있을때만 저장
			insert_table_w_log_permit(owner['log_pmt']['tbl_week'], row_denial)
		conn.close()

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

	##  이벤트 통합 서버로 실시간 데이터 베이스 등록
	if hasVal_approved:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_week", row_approved, int(owner['sensor']['serial']))
				# print row_approved
	if hasVal_unknown:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_week", row_unknown, int(owner['sensor']['serial']))
				# print row_unknown

	if hasVal_denial:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_permit_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_permit_week", row_denial, int(owner['sensor']['serial']))
				# print row_denial

def read_monthly_sum(): 
	# 지난달의 통계
	query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y%m') AS PrevMonth FROM "+owner['log_table']['tbl_day']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-01') - INTERVAL 1 MONTH AND DATE_FORMAT(NOW(), '%Y-%m-01') AND `w_approved` > 0 "
	query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS w_ax_cnt,IFNULL(SUM(w_xa_cnt),0)AS w_xa_cnt,IFNULL(SUM(w_bx_cnt),0)AS w_bx_cnt,IFNULL(SUM(w_xb_cnt),0)AS w_xb_cnt,IFNULL(SUM(w_cx_cnt),0)AS w_cx_cnt,IFNULL(SUM(w_xc_cnt),0)AS w_xc_cnt,IFNULL(SUM(w_dx_cnt),0)AS w_dx_cnt,IFNULL(SUM(w_xd_cnt),0)AS w_xd_cnt, IFNULL(SUM(w_approved),0)AS w_approved, IFNULL(SUM(w_unknown),0)AS w_unknown, 0, DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y%m') AS PrevMonth FROM "+owner['log_table']['tbl_day']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-01') - INTERVAL 1 MONTH AND DATE_FORMAT(NOW(), '%Y-%m-01') AND `w_unknown` > 0 "
	query_denial = "SELECT IFNULL(SUM(w_no_image),0)AS w_no_image, IFNULL(SUM(w_single),0)AS w_single, IFNULL(SUM(w_multiple),0)AS w_multiple, IFNULL(SUM(w_low_density),0)AS w_low_density, IFNULL(SUM(w_anti_denial),0)AS w_anti_denial FROM "+owner['log_pmt']['tbl_day']+" WHERE `w_stamp` BETWEEN DATE_FORMAT(NOW(), '%Y-%m-01') - INTERVAL 1 MONTH AND DATE_FORMAT(NOW(), '%Y-%m-01') "
	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()

		# 승인자 추가분 확인
		cursor.execute(query_approved)
		conn.commit()
		row_approved = cursor.fetchone()
		hasVal_approved = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_approved += int(row_approved[i])
		if hasVal_approved:
			insert_table_w_log_giken(owner['log_table']['tbl_month'], row_approved)

		# 비승인자 추가분 확인
		cursor.execute(query_unknown)
		conn.commit()
		row_unknown = cursor.fetchone()
		hasVal_unknown = 0
		for i in range(0, 8): # 최대 8개의 센서 영역의 이벤트를 모두 합한다.
			hasVal_unknown += int(row_unknown[i])
		if hasVal_unknown:
			insert_table_w_log_giken(owner['log_table']['tbl_month'], row_unknown)

		# 부정접근자 추가분 확인
		cursor.execute(query_denial)
		conn.commit()
		row_denial = cursor.fetchone()
		hasVal_denial = 0
		for i in range(0, 4):
			hasVal_denial += int(row_denial[i])
		if hasVal_denial: # 내용이 있을때만 저장
			insert_table_w_log_permit(owner['log_pmt']['tbl_month'], row_denial)
		conn.close()

	except MySQLdb.Error as error:
		logger.info('SQL Server Error {}'.format(error))
	# finally:
	# 	cursor.close()
	# 	conn.close()

	##  이벤트 통합 서버로 실시간 데이터 베이스 등록
	if hasVal_approved:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_month", row_approved, int(owner['sensor']['serial']))
				# print row_approved
	if hasVal_unknown:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_giken_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_giken_month", row_unknown, int(owner['sensor']['serial']))
				# print row_unknown

	if hasVal_denial:
		for evtSrv in owner['server']['event']:
			if evtSrv['addr']:
				insert_table_w_log_permit_server(evtSrv['addr'], evtSrv['port'], evtSrv['user'], evtSrv['pass'], evtSrv['name'], "w_log_permit_month", row_denial, int(owner['sensor']['serial']))
				# print row_denial

## 메세지 전송
def messageToClient(key, value):
	jsonData = {}
	jsonData[key] = value
	json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
	insert_socket_GIKEN(json_dump)

	# ## IMS 서버로 자려 전송
	# ## owner['server']['ims'][0]['address'] and owner['server']['ims'][0]['port']
	# for ims in owner['server']['ims']:
	# 	# print (ims['addr'],ims['port'],json_dump)
	# 	# echo "id=g400t300_192_168_0_20_0001,name=GIKENP,beep=1,status=9,shot=http://192.168.168.30/cgi-bin/trace.cgi,video=,count=1,block=0,msg=Tailing" | nc 192.168.0.4 38087
	# 	insert_socket_IMS(ims['addr'],ims['port'],json_dump)

################################
# METHOD #1: OpenCV, NumPy, and urllib
# URL로부터 이미지 읽어오기
def cv_image_from_url(url, mode): # url = owner['opencv']['live_url'], mode = 0(그레이) 또는 1(칼라)
    # download the image, convert it to a NumPy array, and then read
    # 기켄 이미지 -> 320 X 240
	try:
		resp = urllib.urlopen(url)
	except:
		print('Error read {}'.format(url))
		return None

	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	if mode:
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	else:
		image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
	return image

# ## 기켄센서로부터 정보수집
# ## {u'status': {u'camera': u'G', u'analyser': u'P'}, u'code': 0, u'inside': 0, u'outside': 0, u'setting': {u'areatype': u'N', u'arrow': [[u'B', u'A'], [u'X', u'X'], [u'X', u'X'], [u'X', u'X']]}, u'countdata': [[6, 0], [0, 0], [0, 0], [0, 0]], u'time': u'2021-04-09 21:46:42', u'parameter': {u'interval': 10, u'target': 0, u'very_crowded': 10, u'crowded': 5}}
# def is_multiple_obj():
# 	url = "http://" + owner['sensor']['ip'] + owner['sensor']['cgi']
# 	response = urllib.urlopen(url)
# 	data = json.loads(response.read())
# 	# print data
# 	return data['inside']

def getInformation():
	url = "http://" + owner['sensor']['ip'] + owner['sensor']['cgi']
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	# return data['inside']
	return data

def dueTwilight(due=1): ## 점멸 확인시간을 주기적으로 체크함
	threading.Timer(due, dueTwilight).start()
	getTwilight()

def getTwilight(): # Twilight Enable - 조도값에 따른 라이트 점멸 및 베이스이미지 재 설정
	try:
		initImage = cv_image_from_url(owner['opencv']['live_url'], 0) # 그레이 이미지
		live['liveImgLV'] = np.average(initImage) # 실시간 이미지('liveImgLV') 레벨값 저장
		live['diffImgLV'] = live['baseImgLV'] - live['liveImgLV'] # 실시간 이미지('liveImgLV') 레벨값 저장
		if live['diffImgLV'] > 0:
			if live['flag'] == owner['gpio']['swOn']:
				pass
			else:
				live['flag'] = owner['gpio']['swOn'] # "On Light"
				relayAction(4, live['flag']) # 기준이하 조도 "On Light"
				logger.info("Turn On Light {} Diff:{} Live:{} Base:{}".format(live['flag'],live['diffImgLV'],live['liveImgLV'],live['baseImgLV']))
				if owner['opencv']['tuner_mode']: 
					owner['control']['setLock'] = 1 # 베이스이미지 재 설정을 위한 시간 동안 Unknoen 알람 일시 정지
					# print ("Wait 1 sec for Sensor Ready")
					time.sleep(1)
					logger.info(command_renewal()) # 조도가 바뀌면 베이스이미지 재 설정
					owner['control']['setLock'] = 0 # Unknoen 알람 시작
		else:
			if live['flag'] == owner['gpio']['swOff']:
				pass
			else:
				live['flag'] = owner['gpio']['swOff'] # "Off Light"
				relayAction(4, live['flag']) # 기준이상 조도 "Off Light"
				logger.info("Turn Off Light {} Diff:{} Live:{} Base:{}".format(live['flag'],live['diffImgLV'],live['liveImgLV'],live['baseImgLV'])) 
				if owner['opencv']['tuner_mode']: 
					owner['control']['setLock'] = 1 # 베이스이미지 재 설정을 위한 시간 동안 Unknoen 알람 일시 정지
					# print ("Wait 1 sec for Sensor Ready")
					time.sleep(1)
					logger.info(command_renewal()) # 조도가 바뀌면 베이스이미지 재 설정
					owner['control']['setLock'] = 0 # Unknoen 알람 시작
	except:
		return

## URL을 통해 이미지를 다운로드(cv_image_from_url) 한후 
## 기존의 초기이미지와 비교 한다.
def cv_multiple_filter():
	try:
		initImage = cv_image_from_url(owner['opencv']['live_url'], 0) # 그레이 이미지				
		## 원이미지를 설정된 크기로 잘라낸다. liveImage = initImage[0:200, 50:260]
		liveImage = initImage[owner['opencv']['crop_y']:owner['opencv']['crop_h'], owner['opencv']['crop_x']:owner['opencv']['crop_w']] # [y:h, x:w]
	except:
		return 0 # 이미지 켑쳐 오류

	## 두 이미지간 차이값을 득한다.
	diffImage = cv2.subtract(live['baseImage'], liveImage)

	# 스레솔드 필터 (이미지, 기준값, 변환값, 특성값)
	# _,thresh = cv2.threshold(diffImage,64,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	# _,thresh = cv2.threshold(diffImage,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	# _,thresh = cv2.threshold(diffImage,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	# _,thresh = cv2.threshold(diffImage,192,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	# _,thresh = cv2.threshold(diffImage,owner['opencv']['threshold'],255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	# 트레솔드 필터 (이미지, 기준값, 변환값, 특성값) 
	if owner['opencv']['threshold'] > 0:
		_,thresh = cv2.threshold(diffImage,owner['opencv']['threshold'],255,cv2.THRESH_BINARY_INV)
	else: # 자동 트레솔드
		_,thresh = cv2.threshold(diffImage,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# 스파클(noise) 제거 및 이미지 반전 https://copycoding.tistory.com/156
	if owner['opencv']['img_filter'] > 0:
		kernel = np.ones((owner['opencv']['img_filter'], owner['opencv']['img_filter']), np.uint8)
		unNoise = cv2.dilate(thresh, kernel, iterations = 1)
		# 이미지 반전(주변을 검은색으로)
		finImage = cv2.bitwise_not(unNoise) 
	else:
		finImage = cv2.bitwise_not(thresh) 

	## 힌색 픽셀 갯수 확인
	p = cv2.countNonZero(finImage)

	# 오브젝트 위치와 치수
	x,y,w,h = cv2.boundingRect(finImage) # left, top, width, height

	# dateTime = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S") # UTC - 센서 요청시간대
	dateTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # UTC - 센서 요청시간대
	# 계산된 영역을 박스로 표시
	# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
	cv2.rectangle(liveImage,(x,y),(x+w,y+h),(255,255,255),1)
	cv2.rectangle(finImage,(x,y),(x+w,y+h),(255,255,255),1)
	# 이미지에 정보를 문자 표시 한다.
	# https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html
	font = cv2.FONT_HERSHEY_SIMPLEX # datetime.datetime.now()
	stack = np.hstack((liveImage,finImage)) # 세로로 결합

	# 이미지 정보 쓰기
	cv2.putText(stack,'W:{}({}),H:{}({})'.format(w,owner['opencv']['object_w'],h,owner['opencv']['object_h'],p,owner['opencv']['object_p']),(1,12), font, 0.3,(0,0,0),1,cv2.LINE_AA) ## 그림자
	cv2.putText(stack,'W:{}({}),H:{}({})'.format(w,owner['opencv']['object_w'],h,owner['opencv']['object_h'],p,owner['opencv']['object_p']),(2,13), font, 0.3,(255,255,255),1,cv2.LINE_AA) ## 문자 
	cv2.putText(stack,'Px:{}({})'.format(p,owner['opencv']['object_p']),(1,22), font, 0.3,(0,0,0),1,cv2.LINE_AA) ## 그림자
	cv2.putText(stack,'Px:{}({})'.format(p,owner['opencv']['object_p']),(2,23), font, 0.3,(255,255,255),1,cv2.LINE_AA) ## 문자 
	cv2.putText(stack,'{}'.format(dateTime),(1,32), font, 0.3,(0,0,0),1,cv2.LINE_AA) ## 그림자
	cv2.putText(stack,'{}'.format(dateTime),(2,33), font, 0.3,(255,255,255),1,cv2.LINE_AA) ## 문자 

	cv2.imwrite(owner['file']['image_folder']+'/'+owner['file']['image_live'], stack) # 최종 이미지
	if owner['opencv']['iLog_mode']: ## image log 모드이면 저장
		shutil.copyfile(owner['file']['image_folder']+'/'+owner['file']['image_live'], owner['file']['image_final']+'/{}.png'.format(dateTime)) # 백업 이미지
		## 테스트 가능할때 아래 기능(백업이미지 삭제) 추가.
		# os.chmod(owner['file']['image_final']+'/{}.png'.format(dateTime),0o777)

	# messageToClient('control', 'detect x{}, y{}, w{}, h{}, p{}<br>diff:{}, live:{}, base:{}'.format(x,y,w,h,p,live['diffImgLV'], live['liveImgLV'], live['baseImgLV'])) # 
	messageToClient('statusMsg', '{},{},{},{},{},{},{},{}'.format(x,y,w,h,p,live['diffImgLV'], live['liveImgLV'], live['baseImgLV'])) # 

	return x,y,w,h,p

	# ## 가로(w)와 세로(h) 그리고 공간내 필터링된 픽셀수(p)간의 상관관계
	# ## 
	# if p < owner['opencv']['object_p']: ## 비교 픽셀이 제한값을 넘으면
	# 	logger.info('Less Px: detect x{}, y{}, w{}, h{}, p{}'.format(x,y,w,h,p))
	# 	return 3 # 픽셀 미달
	# elif w > owner['opencv']['object_w'] or h > owner['opencv']['object_h']:
	# 	logger.info('Multiple: detect x{}, y{}, w{}, h{}, p{}'.format(x,y,w,h,p))
	# 	return 2 # 다수 감지
	# else:
	# 	logger.info('Single: detect x{}, y{}, w{}, h{}, p{}'.format(x,y,w,h,p))
	# 	return 1 # 단수 감지

## 관리자의 개방 요청
def command_open(): ## 관리자에 의한 입구 열기
	# # 문을 강제 개방 한다.
	# relayAction(4) 
	# # 관리자 개방 스넵샷 
	# dateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") # UTC - 센서 요청시간대
	# try:
	# 	os.makedirs(owner['file']['image_manual']+'/'+dateTime[0:10])
	# except:
	# 	pass # directory already exists

	# with open(owner['file']['image_manual']+'/'+dateTime[0:10]+'/{}.jpg'.format(dateTime[11:20]), 'w') as f:
	# 	f.write(get_sensor_image())

	# # # 원본(컬러) : 1초 ~= 36프레임
	# # imageColor = cv_image_from_url(owner['opencv']['live_url'], 1) # 컬러 이미지
	# # cv2.imwrite(owner['file']['image_manual']+'/'+dateTime[0:10]+'/{}.jpg'.format(dateTime[11:20]), imageColor)


	# # 키승인 + 부정접근(Anti-Denial)
	# live['liveTimerIn'][0] = datetime.datetime.now() ## 리셋 타이머
	# live['liveCountIn'][0] = 1 ## 기본 승인 횟수 1
	# # 모니터링 : 활성화된 브라우저로 전송
	# jsonData = {}
	# jsonData['keyCount'] = {}
	# jsonData['keyCount'][0] = 1
	# json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
	# insert_socket_GIKEN(json_dump)

	# live['cntDenial'][0] += 1
	# # 모니터링 : 활성화된 브라우저로 전송
	# jsonData = {}
	# jsonData['denialCount'] = {}
	# jsonData['denialCount'][0] = live['cntDenial'][0] #
	# json_dump = json.dumps(jsonData, sort_keys=False, indent=2)
	# insert_socket_GIKEN(json_dump)

	# # if owner['opencv']['mask_mode']:
	# # 	result = cv_multiple_filter()
	# # else:
	# # 	result = is_multiple_obj()

	# # result = cv_multiple_filter()

	# # preStatus = [0,0,0,0,owner['control']['antiDenial']] # 초기화 또는 사용자 개방
	# # insert_table_w_log_permit(owner['log_pmt']['tbl_live'], preStatus) # 데이터 추가

	# insert_table_w_log_sensor([0,0,0,0]) # 센서로그

	return "Light Lv:{0:.2%} Diff:{1:.2%} Base:{2:.2%}".format(live['liveImgLV']/255, live['diffImgLV']/255, live['baseImgLV']/255) # 실시간 이미지 레벨 및 기본 이미지 간 차이값 % 표시(모니터링 폼)

def command_renewal(): 
	try:
		# #####################
		# ## 투명 이미지 생성
		# #####################
		color_white = (255, 255, 255, 255)
		color_white64 = (255, 255, 255, 64)
		color_white16 = (255, 255, 255, 16)
		color_red = (0, 0, 255, 255)
		color_green = (0, 255, 0, 255)
		color_blue = (255, 0, 0, 255)
		color_yellow = (0, 255, 255, 255)
		color_cyan = (255, 255, 0, 255)
		color_orange = (0, 165, 255, 255)

		sX = owner['sensor']['size_x']
		sY = owner['sensor']['size_y']

		## 이미지 생성: np.zeros((img_height, img_width, n_channels), dtype=np.uint8)
		layer = np.zeros((sY, sX, 4))
		font = cv2.FONT_HERSHEY_SIMPLEX
		
		## 투명 이미지에 요소 그리기
		# cv2.line(layer, (170, 170), (340, 340), color_blue, 5)
		# cv2.circle(layer, (255, 255), 100, color_red, 5)
		# cv2.rectangle(layer, (175, 175), (335, 335), color_green, 5)

		# 눈금자 X 그리기
		for i in range(0, sX, 10):
			cv2.line(layer, (i,0), (i,sY), color_white16, 1)
			if not i % 50:
				cv2.line(layer, (i,0), (i,sY), color_white64, 1)
			if not i % 100:
				cv2.line(layer, (i,0), (i,sY), color_white, 1)
				# 눈금자에 치수 쓰기
				cv2.putText(layer, str(i), (i+2,8), font, 0.3, color_white, 1, cv2.LINE_AA)

		# 눈금자 Y 그리기
		for i in range(0, sY, 10):
			cv2.line(layer, (0,i), (sX,i), color_white16, 1)
			if not i % 50:
				cv2.line(layer, (0,i), (sX,i), color_white64, 1)
			if not i % 100:
				cv2.line(layer, (0,i), (sX,i), color_white, 1)
				# 눈금자에 치수 쓰기
				cv2.putText(layer, str(i), (2,i+8), font, 0.3, color_white, 1, cv2.LINE_AA)
	
		x=owner['opencv']['crop_x']
		y=owner['opencv']['crop_y']
		w=owner['opencv']['crop_w']
		h=owner['opencv']['crop_h']

		# 영상분석 영역 그리기
		cv2.rectangle(layer, (x,y), (w,h), color_red, 2)
		cv2.putText(layer,'({} x {})'.format(w-x,h-y), (x,y+h), font, 0.4, color_white, 1, cv2.LINE_AA)

		# ## 다운로드 이미지
		grayImage = cv_image_from_url(owner['opencv']['live_url'], 0) # 그레이 이미지

		# # 마스킹 영역 그리기
		# if owner['opencv']['mask_enable']:
		# 	xM=owner['opencv']['mask_x']
		# 	yM=owner['opencv']['mask_y']
		# 	wM=owner['opencv']['mask_w']
		# 	hM=owner['opencv']['mask_h']
		# 	cv2.rectangle(layer, (xM,yM), (wM,hM), color_yellow, 1)
		# 	# 마스킹 선언
		# 	cv2.rectangle(grayImage, (xM,yM), (wM,hM), (0,0,0), -1)

		# if owner['opencv']['mask2_enable']:
		# 	xM2=owner['opencv']['mask2_x']
		# 	yM2=owner['opencv']['mask2_y']
		# 	wM2=owner['opencv']['mask2_w']
		# 	hM2=owner['opencv']['mask2_h']
		# 	cv2.rectangle(layer, (xM2,yM2), (wM2,hM2), color_cyan, 1)
		# 	# 마스킹 선언
		# 	cv2.rectangle(grayImage, (xM2,yM2), (wM2,hM2), (0,0,0), -1)

		# if owner['opencv']['mask3_enable']:
		# 	xM3=owner['opencv']['mask3_x']
		# 	yM3=owner['opencv']['mask3_y']
		# 	wM3=owner['opencv']['mask3_w']
		# 	hM3=owner['opencv']['mask3_h']
		# 	cv2.rectangle(layer, (xM3,yM3), (wM3,hM3), color_orange, 1)
		# 	# 마스킹 선언
		# 	cv2.rectangle(grayImage, (xM3,yM3), (wM3,hM3), (0,0,0), -1)

		## 분석영역 크롭핑후 베이스이미지로 설정
		live['baseImage'] = grayImage[y:h, x:w] # image[start_x:end_x, start_y:end_y]

		# Anti Tailing Function
		if owner['opencv']['tail_enable']: # 안티테일링 좌표값이 있으면
			xT=owner['opencv']['tail_x']
			yT=owner['opencv']['tail_y']
			wT=owner['opencv']['tail_w']
			hT=owner['opencv']['tail_h']
			cv2.rectangle(layer, (xT,yT), (wT,hT), color_green, 1)
			# 테일링을 위한 초기 이미지 저장
			grayImage = cv_image_from_url(owner['opencv']['live_url'], 0) # 그레이 이미지
			live['tailImg'] = grayImage[owner['opencv']['tail_y']:owner['opencv']['tail_h'], owner['opencv']['tail_x']:owner['opencv']['tail_w']]
			# print live['tailImg']

		## 파일로 저장
		cv2.imwrite(owner['file']['image_folder']+'/'+owner['file']['image_base'], layer)
		# shutil.copyfile(owner['file']['image_folder']+'/'+owner['file']['image_base'], owner['file']['image_folder']+'/'+owner['file']['image_live']) # 백업 이미지

		# logger.info("Base Renewal")
		return "Renewal Base Image"

	except cv2.error as e:
		print('\tError Renewal %s' % e)
		logger.info("Error Renewal")
		return "Error Base Image Renewal"

## 백그라운드 포트 감지
## https://stackoverflow.com/questions/22648765/how-to-run-a-background-procedure-while-constantly-checking-for-input-threadin
def process_port_PY_in():
	try:
		sock = socket.socket()
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ## 파이썬 : 바인딩 소켓 :“이미 사용중인 주소” 방지
		sock.bind(("localhost",owner['interface']['port_PY_in']))
		sock.listen(1)
		# print "\tWaiting on connection %s"%owner['interface']['port_PY_in']
		conn = sock.accept()
		logger.info("> Client connected Recv. Port{}".format(owner['interface']['port_PY_in']))
	except socket.error as msg:
		print ("\tError bind - (Kill Processor.) PY")
		logger.info("> Error Connect to Recv. Port:{}".format(owner['interface']['port_PY_in']))

	while True:
		try:
			msg = conn[0].recv(1024)
			# conn[0].send(msg) ## ECHO Send
			if msg == 'command_open':
				result = command_open()
			elif msg == 'command_renewal':
				result = command_renewal()
			# elif msg == 'command_antiDenial':
			# 	if owner['control']['antiDenial'] == 1:
			# 		owner['control']['antiDenial'] = 0
			# 	else:
			# 		owner['control']['antiDenial'] = 1
			# 	result = "User mode antiDenial:{}".format(owner['control']['antiDenial'])
				
			# elif msg == 'command_antiTailing':
			# 	if owner['control']['antiTailing'] == 1:
			# 		owner['control']['antiTailing'] = 0
			# 	else:
			# 		owner['control']['antiTailing'] = 1
			# 	result = "User mode antiTailing:{}".format(owner['control']['antiTailing'])
			# elif msg == 'command_setLock':
			# 	owner['control']['setLock'] = 1
			# 	owner['control']['setOpen'] = 0
			# 	owner['control']['release'] = 0
			# 	result = "User mode setLock:"
			# elif msg == 'command_setOpen':
			# 	owner['control']['setLock'] = 0
			# 	owner['control']['setOpen'] = 1
			# 	owner['control']['release'] = 0
			# 	result = "User mode setOpen"
			# elif msg == 'command_release':
			# 	owner['control']['setLock'] = 0
			# 	owner['control']['setOpen'] = 0
			# 	owner['control']['release'] = 1
			# 	result = "User mode release All"
			# elif msg == 'command_status':
			# 	messageToClient('statusAll', owner['control']) ## statusReport

			# logger.info(result)
			messageToClient('manualInfo', result) # 
			messageToClient('statusAll', owner['control']) ## statusReport
			saveConfig(owner,owner['file']['conf_gikenp']) ## 저장
		except:
			continue

	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

def linreg(X, Y): # 일련의 숫자에서 기울기와 절편을 반환 한다.
	"""
	https://stackoverflow.com/questions/10048571/python-finding-a-trend-in-a-set-of-numbers
	x = [12, 34, 29, 38, 34, 51, 29, 34, 47, 34, 55, 94, 68, 81]
	a,b = linreg(range(len(x)),x)  //your x,y are switched from standard notation
	반환값 a:기울기 y/x(증가분) - 양수이면 증가 곡선, 음수이면 감소곡선, b:절편값 - x가 0일때 y값
	테스트 : https://www.wolframalpha.com/input/?i=linear+fit+%5B%5D
	"""
	N = len(X)
	Sx = Sy = Sxx = Syy = Sxy = 0.0
	for x, y in zip(X, Y):
		Sx = Sx + x
		Sy = Sy + y
		Sxx = Sxx + x*x
		Syy = Syy + y*y
		Sxy = Sxy + x*y
	det = Sxx * N - Sx * Sx
	return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det

def tailingCheck():
	mP = mW = mH = 0 # 픽셀수 픽셀폭 픽셀높이
	aX = aY = []
	live['tailStatus'] = [0,0,0,0,0,0,0,0] # [ IO(Forward), OI(Backward), RL(Left), LR(Right), ET(Empty), mP(maxPixel), mW(maxX), mH(maxY) ]

	for p,x,y,w,h in live['tailNumpy']: # [p,x,y,w,h]
		if p > mP: # 최대 픽셀수
			live['tailStatus'][5] = p
		if w > mW: # 최대 픽셀폭
			live['tailStatus'][6] = w
		if h > mH: # 최대 픽셀높이
			live['tailStatus'][7] = h
		if x:
			aX.append(x) # 이동 좌표(X:Left, Right)
		if y:
			aY.append(y) # 이동 좌표(Y:Forward, Backward)

	# 방향 분석
	lX = len(aX)
	lY = len(aY)
	if lX > 1: # 수집된 자료가 1 이상이어야 분석 가능함
		a, b = linreg(range(lX),aX)
		if a < 0:
			live['tailStatus'][2] = 1 # RL(Left)
		else:
			live['tailStatus'][3] = 1 # LR(Right)

	if lY > 1: # 수집된 자료가 1 이상이어야 분석 가능함
		a, b = linreg(range(lY),aY)
		if a < 0:
			live['tailStatus'][0] = 1 # 순방향 출입(Forward)
		else:
			live['tailStatus'][1] = 1 # 역방향 출입(Backward)

	if lX == lY == 0: # 데이터가 없는 경우
		live['tailStatus'][4] = 1

	return live['tailStatus']

def apiCustom(addr, port, content):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((addr, port))
		s.send(content)
		recv = s.recv(1024) 
		s.close() 
		return recv
	except socket.error:
		return "Socket Error {0}".format(addr)
	except socket.timeout:
		return "Timeout Error {0}".format(addr)
	finally:
		s.close() 

def main():	
	# ## 최초 이미지 000.jpg로 저장
	# data = get_sensor_image()
	# if data:
	# 	with open(owner['file']['image_folder']+'/000.jpg', 'w') as f:
	# 		f.write(data)
	# 	logger.info('>>>>>>> Created '+owner['file']['image_folder']+'/000.jpg')
	# else:
	# 	logger.info(">>>>>>> Error Connect Sensor(Camera)")
	# 	exit('Error Connect Sensor(Camera)')

	# if owner['control']['antiDenial']:
	# 	print '\tDeny multiple standing.'
	# 	logger.info(">>>>>>>> Deny multiple standing")
	# else:
	# 	print '\tAllow multiple standing.'
	# 	logger.info(">>>>>>>> Allow multiple standing")

	# if owner['opencv']['mask_mode']:
	# 	print '\tOpenCV Denial.'
	# 	logger.info(">>>>>>>> OpenCV Denial")
	# else:
	# 	print '\tSensor Info Denial.'
	# 	logger.info(">>>>>>>> Sensor Info Denial")

	## 라이브데이터 베이스에 등록된 오늘의 이벤트 합계 설정
	read_today_sum() ## todaySumA, todaySumU, todaySumR
	print("\tIN({}) OUT({}) UN({}) DNA({})".format(live['tSum']['todaySumA'],live['tSum']['todaySumR'],live['tSum']['todaySumU'],live['tSum']['todaySumD']))
	logger.info(">>>>> IN({}) OUT({}) UN({}) DNA({})".format(live['tSum']['todaySumA'],live['tSum']['todaySumR'],live['tSum']['todaySumU'],live['tSum']['todaySumD']))

	if owner['opencv']['tuner_mode']: ## 이미지 분석 조건(tuner_mode)
		result = command_renewal()
		print("\tTunner Mode On {}".format(result))
		logger.info(">>>>>> Tunner Mode On {}".format(result))
	else:
		print("\tTunner Mode Off")
		logger.info(">>>>>> Tunner Mode Off")

	if owner['gpio']['out_time']['3']: # Twilight Enable - 조도값에 따른 라이트 점멸
		print("\tTwilight On")
		logger.info(">>>>>>> Twilight On")
		dueTwilight(1)
	else:
		print("\tTwilight Off")
		logger.info(">>>>>>> Twilight Off")

	# dateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # UTC+9
	# dateS = dateTime[:-2] # 센서 시간 설정후 시작시간 설정
	dateS = datetime.datetime.now().strftime("%Y%m%d%H%M") # UTC - 센서 요청시간대
	dateE = '999999999999'
	saveDate = dateS
	# 초기화
	preCnt = [0,0,0,0,0,0,0,0] # 초기화

	preInner = 0 # 최근 내부
	preOuter = 0
	preUnknown = 0
	innerSum = 0
	outerSum = 0
	unknownSum = 0

	actionInner = 0
	actionOuter = 0
	timeInnerS = 0
	timeOuterS = 0

	logger.info(">>>>>>>>> Main Looping..")

	while True:
		# 센서로 부터 정보를 읽어 온다 
		# Http Request 기능으로 1초에 최대 8번 가량 실행이 가능하다
		spot = getInformation()

		# <<<<< 내/외에 존재하는 인원합를 구하기 위한 코드 
		innerSumT = preInner - spot['inside']
		outerSumT = preOuter - spot['outside']

		if owner['area']['timeover']['inner']:
			## print("Inner Start {} {} {} {} {} ".format(innerSumT, preInner, innerSum, spot['inside'], datetime.datetime.now()))
			if innerSumT < 0 and preInner == 0: # 감지유지시간 - 빈 공간에 최초로 사물이 인지되는 시점
				timeInnerS = time.time()
				# print("Start Inner")
			
			if timeInnerS and spot['inside']: # 감지유지시간 -  지속적으로 감지가 되면 유지 시간을 확인 한다.
				timeDue = time.time() - timeInnerS
				if timeDue > owner['area']['timeover']['inner']:
					actionInner = 1
					# print("timeover {} ".format(timeDue))
				else:
					actionInner = 0
					# print("normal {} ".format(timeDue))

			if innerSumT > 0 and not spot['inside']: # 감지유지시간
				actionInner = 0
				timeInnerS = 0 # 초기화
				# print("End Inner")
		else:
			actionInner = spot['inside']

		if owner['area']['timeover']['outer']:
			## print("Outer Start {} {} {} {} {} ".format(outerSumT, preOuter, outerSum, spot['outside'], datetime.datetime.now()))
			if outerSumT < 0 and preOuter == 0: # 감지유지시간 - 빈 공간에 최초로 사물이 인지되는 시점
				timeOuterS = time.time()
				# print("Start Outer")
			
			if timeOuterS and spot['outside']: # 감지유지시간 -  지속적으로 감지가 되면 유지 시간을 확인 한다.
				timeDue = time.time() - timeOuterS
				if timeDue > owner['area']['timeover']['outer']:
					actionOuter = 1
					# print("timeover {} ".format(timeDue))
				else:
					actionOuter = 0
					# print("normal {} ".format(timeDue))

			if outerSumT > 0 and not spot['outside']: # 감지유지시간
				actionOuter = 0
				timeOuterS = 0 # 초기화
				# print("End Outer")
		else:
			actionOuter = spot['outside']


		preInner = spot['inside']
		preOuter = spot['outside']

		if innerSumT > 0:
			innerSum += innerSumT
			spot['innerSum'] = innerSum

		if outerSumT > 0:
			outerSum += outerSumT
			spot['outerSum'] = outerSum

		if actionInner: 
			################################################
			## Relay Out
			relayAction(1) 

			## IMS Monitoring
			for ims in owner['server']['ims']:
				imsValue = 'id='+owner['its']['serial']+',name='+owner['its']['subject']+',beep=1,status=1,shot=,video=,count=1,block=0,msg=Inner'
				insert_socket_IMS(ims['addr'],ims['port'],imsValue)

			## socketIO API 사용자 연동 기능
			if owner['server']['socket']['flag']['P']:
				# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], owner['server']['socket']['P']['value'])
				dataIs = owner['server']['socket']['P']['value']
				result = apiCustom(owner['server']['socket']['P']['addr'], owner['server']['socket']['P']['port'], dataIs)
				logger.info("<--- Info (socketIO_P:{0}, {1}, {2}, {3}) --->".format(result, owner['server']['socket']['P']['addr'], owner['server']['socket']['P']['port'], dataIs.encode("utf-8")))
			if owner['server']['socket']['flag']['S']:
				# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], owner['server']['socket']['S']['value'])
				dataIs = owner['server']['socket']['S']['value']
				result = apiCustom(owner['server']['socket']['S']['addr'], owner['server']['socket']['S']['port'], dataIs)
				logger.info("<--- Info (socketIO_S:{0}, {1}, {2}, {3}) --->".format(result, owner['server']['socket']['S']['addr'], owner['server']['socket']['S']['port'], dataIs.encode("utf-8")))

		if actionOuter: 
			################################################
			## Relay Out
			relayAction(2) 

			# ## IMS Monitoring
			# for ims in owner['server']['ims']:
			# 	imsValue = 'id='+owner['its']['serial']+',name='+owner['its']['subject']+',beep=1,status=1,shot=,video=,count=1,block=0,msg=Outer'
			# 	insert_socket_IMS(ims['addr'],ims['port'],imsValue)

			## socketIO API 사용자 연동 기능
			# if owner['server']['socket']['flag']['P']:
			# 	# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], owner['server']['socket']['P']['value'])
			# 	dataIs = owner['server']['socket']['P']['value']
			# 	result = apiCustom(owner['server']['socket']['P']['addr'], owner['server']['socket']['P']['port'], dataIs)
			# 	logger.info("<--- Info (socketIO_P:{0}, {1}, {2}, {3}) --->".format(result, owner['server']['socket']['P']['addr'], owner['server']['socket']['P']['port'], dataIs.encode("utf-8")))

			# if owner['server']['socket']['flag']['S']:
			# 	# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], owner['server']['socket']['S']['value'])
			# 	dataIs = owner['server']['socket']['S']['value']
			# 	result = apiCustom(owner['server']['socket']['S']['addr'], owner['server']['socket']['S']['port'], dataIs)
			# 	logger.info("<--- Info (socketIO_S:{0}, {1}, {2}, {3}) --->".format(result, owner['server']['socket']['S']['addr'], owner['server']['socket']['S']['port'], dataIs.encode("utf-8")))

		## 이미지 분석 조건(tuner_mode) - Unknown: Relay(3)
		if owner['opencv']['tuner_mode']:
			x,y,w,h,p = cv_multiple_filter()
			if owner['control']['setLock'] == 0: # 조도가 바뀌는 시점인 경우 일정 시간 setLock이 활성화 됨
				# if owner['opencv']['object_p'] and p > owner['opencv']['object_p']:
				# 	spot['unknown'] = 1
				# 	# relayAction(3) # 감지가 불가능한 큰 물체 (예 우산)
				# 	logger.info("Warning: Unknown Objects")
				# else:
				# 	spot['unknown'] = 0
				# 	if owner['opencv']['object_w'] and w > owner['opencv']['object_w'] and owner['opencv']['object_h'] and h > owner['opencv']['object_h']: ## 비교 픽셀이 제한값을 넘으면
				# 		spot['unknown'] = 1
				# 		# relayAction(3) # 감지가 불가능한 큰 물체 (예 우산)
				# 		logger.info("Warning: Unknown Objects")

				if owner['opencv']['object_p'] and p > owner['opencv']['object_p'] and owner['opencv']['object_w'] and w > owner['opencv']['object_w'] and owner['opencv']['object_h'] and h > owner['opencv']['object_h']: ## 비교 픽셀이 제한값을 넘으면
					spot['unknown'] = 1
					# relayAction(3) # 감지가 불가능한 큰 물체 (예 우산)
					logger.info("Warning: Unknown Objects")
				else:
					spot['unknown'] = 0
			else:
				spot['unknown'] = 0
		else: # 일반 모드
			spot['unknown'] = 0
			# print "in:{} out:{} Sum:{} - {}".format(spot['inside'], spot['outside'], spot['countdata'],datetime.datetime.now())
			# 실시간 센서내 4개의 버퍼(IN/OUT Sum) 합계 출력 - 라이브 이미지 좌측 하단
			messageToClient('statusMsg', spot['countdata'])

		unknownSumT = preUnknown - spot['unknown']
		if unknownSumT > 0:
			unknownSum += unknownSumT
			spot['unknownSum'] = unknownSum
		preUnknown = spot['unknown']
		if preUnknown: 
			relayAction(3) 
			## IMS Monitoring
			for ims in owner['server']['ims']:
				imsValue = 'id='+owner['its']['serial']+',name='+owner['its']['subject']+',beep=1,status=1,shot=,video=,count=1,block=0,msg=Oversize'
				insert_socket_IMS(ims['addr'],ims['port'],imsValue)
			## socketIO API 사용자 연동 기능
			if owner['server']['socket']['flag']['P']:
				# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], owner['server']['socket']['P']['value'])
				dataIs = owner['server']['socket']['P']['value']
				result = apiCustom(owner['server']['socket']['P']['addr'], owner['server']['socket']['P']['port'], dataIs)
				logger.info("<--- Info (socketIO_P:{0}, {1}, {2}, {3}) --->".format(result, owner['server']['socket']['P']['addr'], owner['server']['socket']['P']['port'], dataIs.encode("utf-8")))
			if owner['server']['socket']['flag']['S']:
				# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], owner['server']['socket']['S']['value'])
				dataIs = owner['server']['socket']['S']['value']
				result = apiCustom(owner['server']['socket']['S']['addr'], owner['server']['socket']['S']['port'], dataIs)
				logger.info("<--- Info (socketIO_S:{0}, {1}, {2}, {3}) --->".format(result, owner['server']['socket']['S']['addr'], owner['server']['socket']['S']['port'], dataIs.encode("utf-8")))

		# 화면 하단 inside outside Unknown 상태 전송
		messageToClient('objectInfo', spot) 

		# 실시간 모니터링 우측 하단 노랑글 표시 - 현재 감지된 인원 총수
		messageToClient('control', "Area Sum: {}".format(spot['inside'] + spot['outside'] + spot['unknown']) ) #


		################################################
		## 기겐내 버퍼 내용 분석
		data = read_sensor_count(dateS, dateE)
		if not data: # 페킷 읽기 오류
			logger.info("Error: read_sensor_count")
			print("\tError: read_sensor_count - {}".format(datetime.datetime.now()))
			continue
		for line in data.splitlines()[1:]:
			dateS = line[8:20] # 신규 픽업시간 저장(%Y%m%d%H%M)
			newDataIs = line[22:] # 신규데이터 저장
			if len(newDataIs) is not 32: # print len(newDataIs)
				continue

			curCnt = [int(newDataIs[0:4]), int(newDataIs[4:8]), int(newDataIs[8:12]), int(newDataIs[12:16]), int(newDataIs[16:20]), int(newDataIs[20:24]), int(newDataIs[24:28]), int(newDataIs[28:32])]
			tmpStrCnt = ""
			for id in range(8):
				tmpStrCnt += str(curCnt[id]) + " "

			# print " {} {}".format(tmpStrCnt,datetime.datetime.now())

			if dateS > saveDate: # 분이 바뀌면 집계 - 데이터베이스 연계
				################################################
				## 1분 간격으로 하트비트 IMS에 전송 한다.
				for ims in owner['server']['ims']:
					imsValue = 'id='+owner['its']['serial']+',name='+owner['its']['subject']+',beep=0,status=2,shot=,video=,count=1,block=0,msg=Heartbeat'
					insert_socket_IMS(ims['addr'],ims['port'],imsValue)
				## 1분 간격으로 하트비트 또는 오류상태를 IMS에 전송 한다.
				################################################

			saveDate = dateS # 이전 픽업시간 저장

		## 기겐내 버퍼 내용 분석
		################################################

		time.sleep(live['readCycle']) # 1초에 한번 이상 확인하기 위함

		# # Anti Tailing Function
		# # 기켄과 별개로 테일링 검증을 위한 스넵샷 생성
		# # antiTailing 과 tailingFlag 가 1이면 실행
		# if owner['control']['antiTailing'] and owner['opencv']['tail_enable'] and live['tailingFlag']: # 두 변수 조건 만족
		# 	dueSnapDelta = (datetime.datetime.now() - live['setTime']).total_seconds() # Delta 차이깂
		# 	if dueSnapDelta < live['dueTime']: # 픽업가능시간(dueTime) owner['gpio']['reset_interval']
		# 		if live['stTime'] < dueSnapDelta and live['enTime'] > dueSnapDelta: # 사전정의된 시간차
		# 			live['tailCnt'] += 1
		# 			tailingShot() # 포그라운드 실행 - 타이밍에의해 - ~= 8/sec 번
		# 	else:
		# 		live['tailingFlag'] = 0 # 스넵샷 중지
		# 		tailingCheck() # -> live['tailStatus']
		# 		messageToClient('statusMsg', live['tailStatus']) #  
		# 		print ">>>>> Timeout" # 스넵샷 중지 - 시간 만료

		# data = read_sensor_count(dateS, dateE)
		# if not data: # 페킷 읽기 오류
		# 	logger.info("Error: read_sensor_count")
		# 	print("\tError: read_sensor_count - {}".format(datetime.datetime.now()))
		# 	continue

		# for line in data.splitlines()[1:]:
		# 	dateS = line[8:20] # 신규 픽업시간 저장(%Y%m%d%H%M)
		# 	newDataIs = line[22:] # 신규데이터 저장

		# 	if len(newDataIs) is not 32: # print len(newDataIs)
		# 		continue

		# 	# print "####" + newDataIs # 00000000000000000000000000000000

		# 	if dateS > saveDate: # 분이 바뀌면 집계 - 데이터베이스 연계
		# 		read_minute_sum() # 분 집계 등록

		# 		## 1분 간격으로 하트비트 또는 오류상태를 IMS에 전송 한다.
		# 		# 센서 시간 설정은 UTC로 요청 해야 한다. - 리턴 값은 시스템 시간대로 바꿔 보인다.
		# 		# dateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # UTC+9
		# 		dateTimeUTC = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") # UTC - 센서 요청시간대
		# 		if reset_sensor_time(dateTimeUTC):
		# 			beep='0'
		# 			status='2'
		# 			# print "\r\tSet Sensor Time: %s - PY" % datetime.datetime.now()
		# 			# logger.info(">> Set Sensor Time")
		# 		else:
		# 			beep='1'
		# 			status='7'
		# 			# logger.info(">> Error - Set Sensor Time - PY")
		# 			# exit("\r\tError - Check Sensor Interface - PY %s:%s(%s %s)"%(owner['sensor']['ip'], owner['sensor']['port'], owner['sensor']['serial'], owner['sensor']['version']))

		# 		for ims in owner['server']['ims']:
		# 			imsValue = 'id='+owner['its']['serial']+',name='+owner['its']['subject']+',beep='+beep+',status='+status+',shot=,video=,count=1,block=0,msg=Heartbeat'
		# 			insert_socket_IMS(ims['addr'],ims['port'],imsValue)


		# 		if dateS[0:10] > saveDate[0:10]: # 분단위 시간이 바뀌면
		# 			read_hourly_sum() # 시간 집계 등록

		# 			if dateS[0:8] > saveDate[0:8]: # 날짜가 바뀌면
		# 				read_daily_sum() # 오늘 집계 등록

		# 				delete_older_days(owner['log_table']['tbl_live'],owner['log_table']['tbl_life']) # 특정일 이후 자료 삭제
		# 				delete_older_days(owner['log_pmt']['tbl_live'],owner['log_pmt']['tbl_life']) # 특정일 이후 자료 삭제
						
		# 				# # 매일 0시에 센서 시간 동기(오차 수정)
		# 				# dateTimeUTC = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") # UTC - 센서 요청시간대
		# 				# reset_sensor_time(dateTimeUTC)
		# 				# logger.info("Sync Sensor Time")

		# 				live['tSum']['todaySumA'] = 0 # 오늘 들어간 사람 계
		# 				live['tSum']['todaySumU'] = 0 # 오늘 부정 접근한 사람 계
		# 				live['tSum']['todaySumR'] = 0 # 오늘 나온 사람 계
		# 				live['tSum']['todaySumD'] = 0 # 오늘 나온 사람 계

		# 				# 리셋정보 브라우져에 전송
		# 				messageToClient("todaySum", live['tSum'])

		# 				# 한주간 집계 .weekday()의 결과 0인경우 월요일임
		# 				# weekday()의 결과 부터 지난 7일간 집계 함
		# 				if datetime.datetime(int(dateS[0:4]),int(dateS[4:6]),int(dateS[6:8])).weekday() == 0: # 한주의 시작이면
		# 					read_weekly_sum() # 주간 집계 등록
		# 					logger.info("weekly_summary")

		# 				if dateS[0:6] > saveDate[0:6]: # 월이 바뀌면
		# 					read_monthly_sum()
		# 					logger.info("monthly_summary")

		# 					## 월간 단위의 배치프로그램 실행
		# 					## 데이터 베이스, 사진정보등 정리
		# 		preCnt = [0,0,0,0,0,0,0,0] # 초기화
		# 		## 하트비트 전송
		# 		# "its": {
		# 		# 	"bo_id": 1,
		# 		# 	"bo_ip": "192.168.0.10",
		# 		# 	"bo_table": "g400t300",
		# 		# 	"cpu_id": "100000001aef4fc8",
		# 		# 	"description": "DESC",
		# 		# 	"device": "ETH1_192.168.168.10",
		# 		# 	"disabled": 0,
		# 		# 	"serial": "g400t300_192_168_0_10_0001",
		# 		# 	"subject": "AT 01"
		# 		# },
		# 		messageToClient('heartbeat', owner['its'])

		# 	else: 
		# 		# 이벤트 발생시 집계 A(0,1) B(2,3) C(4,5) D(6,7)
		# 		curCnt = [int(newDataIs[0:4]), int(newDataIs[4:8]), int(newDataIs[8:12]), int(newDataIs[12:16]), int(newDataIs[16:20]), int(newDataIs[20:24]), int(newDataIs[24:28]), int(newDataIs[28:32])]

		# 		if int(preCnt == curCnt): # 이전과 현재 전체값을 비교한다.
		# 			pass
		# 		else:

		# 			# Anti Tailing Function
		# 			if owner['control']['antiTailing'] and owner['opencv']['tail_enable'] and live['tailingFlag']: # 두 변수 조건 만족
		# 				live['tailingFlag'] = 0 # 스넵샷 중지
		# 				tailingCheck() # -> live['tailStatus']
		# 				messageToClient('statusMsg', live['tailStatus']) #  
		# 				print ">>>>> By Sensor" # 스넵샷 중지 - 시간 만료

		# 			# 기본적으로 입력되는 방향은 총 8개로 순서대로 변화값을 비교 확인 한다.
		# 			# 스피드게이트에는 단일방향 설정으로 0과 1만(단일구역의 입 출)을 확인함 - range(2)
		# 			for id in range(2): 
		# 				if curCnt[id] > preCnt[id]: # D1: B->L Gate Left 
		# 					liveCount = [0,0,0,0,0,0,0,0] # 초기화

		# 					# liveCount[id] = curCnt[id] - preCnt[id] # 변화값 만 골라낸다.
		# 					# 동시 멀티플은 1명으로 선언(백팩)
		# 					liveCount[id] = 1 # 변화값 만 골라낸다.
							
		# 					preCnt[id] = curCnt[id]

		# 					## 사용자 컨트롤 상태에 따른 명령 거부
		# 					if owner['control']['setLock'] or owner['control']['setOpen']:
		# 						msg = "User mode Lock:{} Open:{}".format(owner['control']['setLock'], owner['control']['setOpen'])
		# 						messageToClient('control', msg)
		# 						continue

		# 					sensorLog = [0,0,0,0] # 센서로그 데이터베이스 등록을 위한 초기값
		# 					status,msg = countDown(id,liveCount[id]) # 리터값 형태 [0,0,0] # [ approvedCount, unknownCount, timeoutCount ]
		# 					# !!!!!!!!!!!!!!!!!!!!! #
		# 					# 알람 발생
		# 					# !!!!!!!!!!!!!!!!!!!!! #
		# 					if status[0]: #### 정상적으로 나가는 이벤트
		# 						# relayAction(1) 
		# 						live['tSum']['todaySumA'] += liveCount[id] # 실시간 들어간 사람 계
		# 						# print "Approved", live['tSum']['todaySumA']
		# 						logger.info("Passed Tailing %s"%live['tSum']['todaySumA'])
		# 						sensorLog[0] = 1 # approvedCount
		# 					elif status[1]: #### 들어오거나 부정으로 나가는 경우
		# 						if (id == 0): #### 부정 접근 나가는 이벤트
		# 							liveImgPath = unknownShot(owner['file']['image_unknown'],1) # 부정 접근 스넵샷
		# 							live['tSum']['todaySumU'] += liveCount[id] # 실시간 부정 접근한 사람 계
		# 							# print "Unknown - Tailing", live['tSum']['todaySumU']
		# 							relayAction(9) 
		# 							logger.info("Unknown Tailing %s"%(live['tSum']['todaySumU']))
		# 							sensorLog[1] = 1 # unknownCount
		# 							# IMS 전송
		# 							# Ex: id=g400t300_192_168_0_20_0001,name=GKT Basic,beep=1,status=1,shot=192.168.0.20/data/image/gikenP_g400t300_192_168_0_20_0001/unknown/2020-10-10/04:35:13.jpg,video=,count=1,block=0,msg=Tailing,subzone=GIKENP,values={"todaySumU": 12, "todaySumD": 0, "todaySumA": 0, "todaySumR": 12}
		# 							for ims in owner['server']['ims']:
		# 								imsShot = owner['its']['bo_ip']+'/data/image/gikenP_'+owner['its']['serial']+'/unknown/'+liveImgPath
		# 								imsValue = 'id='+owner['its']['serial']+',name='+owner['its']['subject']+',beep=1,status=1,shot='+imsShot+',video=,count=1,block=0,msg=Tailing'
		# 								insert_socket_IMS(ims['addr'],ims['port'],imsValue)
		# 						else: #### 들어오는 이벤트는 무시한다.
		# 							live['tSum']['todaySumR'] += liveCount[id] # 실시간 나온 사람 계
		# 							# print "Reverse", live['tSum']['todaySumR']
		# 							logger.info("Reverse %s"%live['tSum']['todaySumR'])
		# 							sensorLog[2] = 1 # reverseCount
		# 					elif status[2]: # timeout - 실제 타임아웃 이전에 카우터 버퍼를 삭제해서 나오지 않음
		# 						relayAction(7) 
		# 						logger.info("Timeout")
		# 					else:
		# 						pass # print msg

		# 					# # 데이터베이스 등록 : 리스트 통합 : liveCount + status + dateS(ymdhm)
		# 					status.append(dateS) # w_ymdhm 항목 추가
		# 					rcvID = insert_table_w_log_giken(owner['log_table']['tbl_live'], liveCount + status)
		# 					# print "\tDatabase ID:%s - %s"%(rcvID, liveCount + status)

		# 					rcvID = insert_table_w_log_sensor(sensorLog)
		# 					# print "\tSensorLog ID:%s - %s"%(rcvID, sensorLog)

		# 					# 모니터링 : 실시간 모든 방향의 합계를 활성화된 브라우저로 전송
		# 					messageToClient("liveCount", liveCount + status)

		# 					# 모니터링 : 오늘의 합계를 활성화된 브라우저로 전송
		# 					messageToClient("todaySum", live['tSum'])

		# 	saveDate = dateS # 이전 픽업시간 저장

		# time.sleep(live['readCycle']) # 1초에 한번 이상 확인하기 위함

		# ## live['liveTimerIn'] 조건(시간초과)에 따라 live['liveCountIn'] 값을 초기화 한다.
		# ## 임시버퍼(live['liveCountIn'])에 저장된 시간이 사용자 선언값(reset_interval)을 초과 하였는지 확인
		# reset_count()

		# print("Pickup Time - Turner:{}, Light:{} - {}".format(owner['opencv']['tuner_mode'], owner['gpio']['out_time']['3'], datetime.datetime.now()))


if __name__ == '__main__':

	###################################
	## 파일 config.json 사용자 변수 선언
	if len(sys.argv) > 1: 
		with open(sys.argv[1]) as json_file:  
			owner = json.load(json_file)
		with open(owner['file']['conf_common']) as json_file: # ~/common/config.json
			share = json.load(json_file)
	else:
		exit("Check Sensor's Config...")	
	## 파일 config.json 사용자 변수 선언

	## 전역변수 선언
	live = {}

	live['baseImage'] = []
	live['baseImgLV'] = owner['opencv']['grayLv'] # 기본값 이미지 조도
	live['liveImgLV'] = 0 # 실시간 이미지 조도
	live['diffImgLV'] = 0 # 이미지간 조도 차이
	live['flag'] = 2 # 현재 라이트 상태 0:on, 1:off, 2:init

	live['tSum'] = {} # 오늘
	live['tSum']['todaySumA'] = 0 # 오늘 들어간 사람 계
	live['tSum']['todaySumU'] = 0 # 오늘 부정 접근한 사람 계
	live['tSum']['todaySumR'] = 0 # 오늘 나온 사람 계
	live['tSum']['todaySumD'] = 0 # 오늘 비 허가인 계

	# live['cntDenial'] = [0,0,0,0,0,0,0,0] # 초기화

	# tN = datetime.datetime.now()
	# live['liveTimerIn'] = [tN,tN,tN,tN,tN,tN,tN,tN] # 초기화
	# live['liveCountIn'] = [0,0,0,0,0,0,0,0] # 초기화

	live['readCycle'] = 0.1 # 0.01 # 반복주기 - 고정 (Second)

	# # Anti Tailing Function
	# live['tailImg'] = [] # 초기값
	# live['tailCnt'] = 0 # 실시간 갯수
	# live['tailNumpy'] = np.empty((0,5), int) # 테일링 이미지 분석값 저장(배열) ex: 1 px:149, x:64, y:60, w:21, h:10
	# live['tailStatus'] = [0,0,0,0,0,0,0,0] # 초기화 - [ IO(Forward), OI(Backward), RL(Left), LR(Right), ET(Empty), mP(maxPixel), mW(maxX), mH(maxY) ]
	# # |----<----------->-----|
	# # |- dueTime ------------|
	# #      < st --- en >
	# live['dueTime'] = owner['gpio']['reset_interval'] # 설정된 시간(초) 동안 스넵샷을 실행한다. 스넵샷 주기는 센서(기켄)에 종속 된다.
	# live['stTime'] = 0 # 0.6 # dueTime 내에 실제 이미지 픽업을 시작하는 시점(초)
	# live['enTime'] = owner['gpio']['reset_interval'] # 1.6 # dueTime 내에 실제 이미지 픽업을 중단하는 시점(초)
	# live['setTime'] = datetime.datetime.now() # 스넵샷이 시작하는 기간 저장
	# # live['maxSnap'] = 100 # 최대 스넵샷
	# # live['cntSnap'] = 0 # 현재 실행된 갯수
	# live['tailingFlag'] = 0 # 초기화 스넵샷 실행 플래그
	# for f in os.listdir(owner['file']['image_tailing']): # 테일링 폴더내 모든 파일 삭제
	# 	os.remove(os.path.join(owner['file']['image_tailing'], f))

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	if not os.path.exists(share['path']['log']): # /var/www/html/its_web/data/log
		os.makedirs(share['path']['log'])
		os.chmod(share['path']['log'],0o777)
	logger = logging.getLogger('mylogger') # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = owner['file']['log_gikenp']
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
	logger.info("> START")
	# logger.debug("===========================")
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	# logger.debug("===========================")
	# logger.info("TEST END!")
	############ logging ################

	## 백그라운드 포트 감지
	thread = threading.Thread(target=process_port_PY_in)
	thread.daemon = True
	thread.start()

	# ## 로그 테이블 생성

	create_table_w_log_sensor() # 센서 일간 로그

	create_table_w_log_giken(owner['log_table']['tbl_live']) # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken(owner['log_table']['tbl_min']) # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken(owner['log_table']['tbl_hour']) # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken(owner['log_table']['tbl_day']) # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken(owner['log_table']['tbl_week']) # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken(owner['log_table']['tbl_month']) # 센서 시리얼 기준의 테이블 생성
	create_table_w_log_giken(owner['log_table']['tbl_sum']) # 센서 시리얼 기준의 테이블 생성

	create_table_w_log_permit(owner['log_pmt']['tbl_live'])
	create_table_w_log_permit(owner['log_pmt']['tbl_min'])
	create_table_w_log_permit(owner['log_pmt']['tbl_hour'])
	create_table_w_log_permit(owner['log_pmt']['tbl_day'])
	create_table_w_log_permit(owner['log_pmt']['tbl_week'])
	create_table_w_log_permit(owner['log_pmt']['tbl_month'])

	## 클라이언트 Html파일 생성
	make_GIKENP_map()

	## 센서 시간 설정은 UTC로 요청 해야 한다. - 리턴 값은 시스템 시간대로 바꿔 보인다.
	# dateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # UTC+9
	dateTimeUTC = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") # UTC - 센서 요청시간대
	if reset_sensor_time(dateTimeUTC):
		print ("\r\tSet Sensor Time: %s - PY" % datetime.datetime.now())
		logger.info(">> Set Sensor Time")
	else:
		logger.info(">> Error - Set Sensor Time - PY")
		exit("\r\tError - Check Sensor Interface - PY %s:%s(%s %s)"%(owner['sensor']['ip'], owner['sensor']['port'], owner['sensor']['serial'], owner['sensor']['version']))

	## 센서 데이터 리셋
	if(reset_sensor_data()):
		print ("\tClear Sensor Buffer - PY")
		logger.info(">>> Clear Sensor Buffer - PY")
	else:
		logger.info(">>> Error - Check Sensor Version and Serial")
		exit("\tError - Check Sensor Version and Serial : %s, %s" % (owner['sensor']['version'], owner['sensor']['serial']))

	# 2021-04-30 13:33:28
	# ## 백그라운드 GPIO 감지
	# result = init_all_GPIO_in() # GPIO
	# logger.info(">>>> "+result)

	# # 초기의 시작값에 따라 릴레이 상태 설정
	# result = init_all_GPIO_out() ## status 1:HIGH, 0:LOW
	# logger.info(">>>>> "+result)

	## 노드js 백그라운드 GIKENP_JS 실행
	result = run_demon_GIKENP_JS(sys.argv[1])
	logger.info(">>>> "+sys.argv[1])
	
	# read_weekly_sum()

	main()