#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

# requirement:  
# pip3 install PyMySQL
# pip3 install RPi.GPIO
# pip3 install python-telegram-bot
# pip3 install mutagen

import os
import re
import sys
import time
import datetime
import json
import subprocess
import requests
import socket
import RPi.GPIO as GPIO
import threading
import telegram
import smtplib
from email.mime.text import MIMEText
import logging
import logging.handlers
# import mutagen # 오디오파일 정보
from mutagen.mp3 import MP3 # MP3오디오파일 정보 : pip3 install mutagen

## 환경설정 파일(JSON)읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)

## 환경설정 파일(JSON) 저장
def saveConfig(cfg,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(cfg, json_file, sort_keys=True, indent=4)

def validate_url(s):
	# print(re.match(regex, 'http://www.example.com') is not None) # True
	# print(re.match(regex, 'example.com') is not None)            # False
	regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if re.match(regex, s):
		return True
	return False

def validate_ip(s):
	a = s.split('.')
	if len(a) != 4:
		return False
	for x in a:
		if not x.isdigit():
			return False
		i = int(x)
		if i < 0 or i > 255:
			return False
	return True

def is_json_key_present(json, key):
	try:
		buf = json[key]
	except KeyError:
		return False
	return True	

def cmd_proc_run_status(cmd):
	## Is command exist in remote system?
	# command = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'command -v arecord'"
	p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# print( 'status:', p.returncode )
	# print( 'stdout:', p.stdout.decode() )
	# print( 'stderr:', p.stderr.decode() )

	# if p.returncode == 0:
	# 	print("command is success")
	# elif p.returncode == 1:
	# 	print("command is error")
	# else:
	# 	print("command is unknown")
	return p.returncode

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	# out == '' 이면 작업 성공, out != ''이면 실패
	# 복합명령인 경우 확인이 불가능 하므로 err는 무시하고 out만 확인 한다.
	return out 

def cmd_proc_Popen_status(cmd): # 2022-07-25 04:44:52
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	# if p.returncode == 0:
	# 	print("command is success")
	# elif p.returncode == 1:
	# 	print("command is error")
	# else:
	# 	print("command is unknown")
	return p.returncode
	
def timerTurnOff(id):
	if id in cfg['setBD']['gppw']:
		GPIO.output(cfg['setBD']['gppw'][id], GPIO.LOW)
	if id in cfg['setBD']['gpio']:
		GPIO.output(cfg['setBD']['gpio'][id], GPIO.LOW)
	sendDataToJsPort('gpioID', id) # 릴레이 ID 전송 -> itsAPI.js

def timerTurnOn(id):
	if id in cfg['setBD']['gppw']:
		GPIO.output(cfg['setBD']['gppw'][id], GPIO.HIGH)
	if id in cfg['setBD']['gpio']:
		GPIO.output(cfg['setBD']['gpio'][id], GPIO.HIGH)
	sendDataToJsPort('gpioID', id) # 릴레이 ID 전송 -> itsAPI.js

def timerTurnToggle(id):
	if id in cfg['setBD']['gppw']:
		if GPIO.input(cfg['setBD']['gppw'][id]):
			GPIO.output(cfg['setBD']['gppw'][id], GPIO.LOW)
		else:
			GPIO.output(cfg['setBD']['gppw'][id], GPIO.HIGH)

	if id in cfg['setBD']['gpio']:
		if GPIO.input(cfg['setBD']['gpio'][id]):
			GPIO.output(cfg['setBD']['gpio'][id], GPIO.LOW)
		else:
			GPIO.output(cfg['setBD']['gpio'][id], GPIO.HIGH)
	sendDataToJsPort('gpioID', id) # 릴레이 ID 전송 -> itsAPI.js

def Nop(id):
	gpioTimer[id] = None
	# print("{} end timer".format(id))
	return 0

# GPIO ID 단위의 다중 타이머 설정 
# 타이머 종료시 종료를 확인 하기 위해 gpioTimer[id]를 None으로 설정
def setGpioTimer(id, time):
	if gpioTimer[id] == None: # or gpioTimer[id].is_alive() == False:
		gpioTimer[id] = threading.Timer(time, Nop, [id])
		gpioTimer[id].start()
		return True # 
	else:
		return False


def actNop(id):
	actTimer[id] = None
	# print("{} end timer".format(id))
	return 0

# 이벤트 ID 단위의 다중 타이머 설정 
# 타이머 종료시 종료를 확인 하기 위해 actTimer[id]를 None으로 설정
def setThreadingTimer(id, time):
	if actTimer[id] == None:
		actTimer[id] = threading.Timer(time, actNop, [id])
		actTimer[id].start()
		return True 
	else:
		return False

def gpioAction(status, id, hold):
	response = {}

	isPortIO = None # isPortPW = None

	# cfg['setBD']['gpio'] || cfg['setBD']['gppw']
	# cfg['setBD']['setIO'] || cfg['setBD']'[setPW']

	# 릴레이 실행 플래그 상태 확인
	# if cfg['execution'][id]:
	if id in cfg['execution']:
		pass
	else:
		return 

	if status in ['0','1','2','3']: # 상태확인
		if id in cfg['setBD']['setIO']:
			if cfg['setBD']['setIO'][id]: # True -> 릴레이
				isPortIO = True
			else: # False -> 센서
				response[id] = GPIO.input(cfg['setBD']['gpio'][id])
				return response
		elif id in cfg['setBD']['setPW']:
			if cfg['setBD']['setPW'][id]: # True -> 릴레이
				isPortIO = False
			else: # False -> 센서
				response[id] = GPIO.input(cfg['setBD']['gppw'][id])
				return response
		else:
			return

	if status == '0': ##### Set OFF
		if isPortIO:
			GPIO.output(cfg['setBD']['gpio'][id], GPIO.LOW)
			response[id] = GPIO.input(cfg['setBD']['gpio'][id])
		else:
			GPIO.output(cfg['setBD']['gppw'][id], GPIO.LOW)
			response[id] = GPIO.input(cfg['setBD']['gppw'][id])
		# hold 값이 있으면 시간 이후 timerTurnOff() / timerTurnOn()
		try: # 문자를 숫자화 할떄 모류 제거
			if float(hold):
				hold = abs(float(hold))
				# https://stackoverflow.com/questions/16578652/threading-timer
				t = threading.Timer(hold, timerTurnOn, [id])
				t.start() # after hold seconds, run timerTurnOff
		except ValueError:
			pass
		sendDataToJsPort('gpioID', id) # 릴레이 ID 전송 -> itsAPI.js
	elif status == '1': ##### Set ON
		if isPortIO:
			GPIO.output(cfg['setBD']['gpio'][id], GPIO.HIGH)
			response[id] = GPIO.input(cfg['setBD']['gpio'][id])
		else:
			GPIO.output(cfg['setBD']['gppw'][id], GPIO.HIGH)
			response[id] = GPIO.input(cfg['setBD']['gppw'][id])
		# hold 값이 있으면 시간 이후 timerTurnOff() / timerTurnOn()
		try: # 문자를 숫자화 할떄 모류 제거
			if float(hold):
				hold = abs(float(hold))
				# https://stackoverflow.com/questions/16578652/threading-timer
				t = threading.Timer(hold, timerTurnOff, [id])
				t.start() # after hold seconds, run timerTurnOff
		except ValueError:
			pass
		sendDataToJsPort('gpioID', id) # 릴레이 ID 전송 -> itsAPI.js
	elif status == '2': ##### Set Toggle
		if isPortIO:
			if GPIO.input(cfg['setBD']['gpio'][id]):
				GPIO.output(cfg['setBD']['gpio'][id], GPIO.LOW)
			else:
				GPIO.output(cfg['setBD']['gpio'][id], GPIO.HIGH)
			response[id] = GPIO.input(cfg['setBD']['gpio'][id])
		else:
			if GPIO.input(cfg['setBD']['gppw'][id]):
				GPIO.output(cfg['setBD']['gppw'][id], GPIO.LOW)
			else:
				GPIO.output(cfg['setBD']['gppw'][id], GPIO.HIGH)
			response[id] = GPIO.input(cfg['setBD']['gppw'][id])
		# hold 값이 있으면 시간 이후 timerTurnOff() / timerTurnOn()
		try: # 문자를 숫자화 할떄 모류 제거
			if float(hold):
				hold = abs(float(hold))
				# https://stackoverflow.com/questions/16578652/threading-timer
				t = threading.Timer(hold, timerTurnToggle, [id])
				t.start() # after hold seconds, run timerTurnToggle
		except ValueError:
			pass
		sendDataToJsPort('gpioID', id) # 릴레이 ID 전송 -> itsAPI.js
	elif status == '3': ##### Status Each
		if isPortIO:
			response[id] = GPIO.input(cfg['setBD']['gpio'][id])
		else:
			response[id] = GPIO.input(cfg['setBD']['gppw'][id])
	elif status == '7': ##### Status Power
		for key, value in cfg['setBD']['gppw'].items():
			response[key] = GPIO.input(value)
	elif status == '8': ##### Status Sensor and Relay
		for key, value in cfg['setBD']['gpio'].items():
			response[key] = GPIO.input(value)
	elif status == '9': ##### Status All
		for key, value in cfg['setBD']['gpio'].items():
			response[key] = GPIO.input(value)
		for key, value in cfg['setBD']['gppw'].items():
			response[key] = GPIO.input(value)
	else:
		return

	# for key, value in response.items():
	# 	keyDesc = cfg['description'][key]
	# 	if keyDesc:
	# 		response[keyDesc] = response.pop(key)

	return response

def audioName(source):
	if source.isdigit(): # 목록에 있는 음원을 사용한다.
		if len(sourceList) < int(source): # 리스트 목록에 없는 번호
			return 0 # 'Out of list'
		else:
			audio = audioFolderAPI + '/' + sourceList[int(source)-1]
			if os.path.isfile(audio):
				pass
			else:
				return 0 # 'File not Found'
	else:
		if validate_url(source):
			url = source
			audio = '/tmp/audioSource_{}' .format(source.split('/')[-1]) # audioSource_ + url의 마지막 파일명 첨부
			if not os.path.exists(audio):
				try:
					# print(url, name)
					# 해당 URL에 송신 및 response 성공 시 파일 저장 
					response = requests.get(url, allow_redirects=True)
					open(audio, 'wb').write(response.content)
				# 잘못된 URL 입력 시 예외 처리
				except Exception as e:
					logger.warning('Audio Download error, {}'.format(audio))
					return 0 # 'Audio Download error'
		elif os.path.isfile(audioFolderDownload + '/' + source): # 로컬내 파일
			audio = audioFolderDownload + '/' + source
		elif os.path.isfile(audioFolderBeep + '/' + source): # 로컬내 파일
			audio = audioFolderBeep + '/' + source
		else:
			return 0 # 'Unknown audio path or url'
	return audio

def audioAction(audio, volume, loop):
	if cfg["audio"]["player"] == 'mplayer': # mplayer를 기본 재생기로 한다. defaultPlayer
		defaultPlayer = True
	elif cfg["audio"]["player"] == 'omxplayer.bin': # 오류 있음 
		defaultPlayer = False
	else:
		return 'Unknown Player'

	if volume.isdigit():
		volume = abs(int(volume))
		if volume > 0 and volume <= 100:
			pass
		else: # 기본 소리 크기값 사용
			volume = 50 # 중간크기

		if defaultPlayer: # mplayer 0 ~ 100
			pass
		else: # omxplayer.bin -3000 ~ +3000
			volume = (volume - 50) * 60 
	else:
		return 'Volume value error'

	if loop.isdigit():
		loop = abs(int(loop))
		if loop > 0:
			pass
		else:
			loop = 1
	else:
		return 'Loop value error'

	# print(audio, target, volume, command, loop)
	# mplayer -nolirc -cache 1024 -volume 100 -loop 0 /var/www/html/its_web/theme/ecos-its_optex/user/audio/api/Industrial.mp3
	# pidof : 프로세서 아이디 확인후 실행
	if defaultPlayer: # mplayer
		cmd ='if ! pidof {0} /dev/null 2>&1; then {0} -nolirc -cache 1024 -volume {1} -loop {2} {3} >/dev/null 2>&1; fi &'.format(cfg["audio"]["player"],volume, loop, audio)
	else: # omxplayer.bin
		cmd ='if ! pidof {0} /dev/null 2>&1; then {0} --vol {1} {2} >/dev/null 2>&1; fi &'.format(cfg["audio"]["player"], volume, audio)

	return cmd_proc_Popen(cmd)

def disconnectPipe():
	cmd_proc_Popen('sudo killall -s 9 {} 2>/dev/null'.format("arecord oggenc sshpass mplayer")) # killall -s 9 arecord oggenc sshpass ssh mplayer
	sendDataToJsPort('btn_status_talk', {'id':'disconnect', 'status':False}) # 사용중
	sendDataToJsPort('btn_status_talk', {'id':'speaking', 'status':True}) # 대기중
	sendDataToJsPort('btn_status_talk', {'id':'listening', 'status':True}) # 대기중

def talkAction(command, remoteIP, description=""):
	## talk 기능은 마이크를 통한 음성을 원격으로 실시간 전송하는 기능이다.
	## 서버 클라이언트간 파이프라인을 연결하는 방식으로 1:n은 불가능하다.
	## [speaking]과 [listening]을 개별 및 동시실행이 가능하다
	## 동시에 실행하는 경우 상대방과의 실시간 대화가 가능하게 된다.
	## [speaking]은 마이크를 통한 자신의 음성을 원격으로 송신하는 방식이다.
	## [listening]은 원격의 마이크를 구동시켜 음성을 수신하는 방식이다.
	## [disconnect]는 실행되고 있는 [speaking] 또는 [listening]프로세서를 죽인다.
	## 구동되는 processor 종류는 arecord, oggenc, sshpass, mplayer 이다.
	## 종료는 threading기능을 이용해 버퍼링시간(3~4초)을 대기한 후 관련프로세서를 죽인다.
	## Shell Command는 대기 현상을 피하기위해 Background로 실행한다.
	## http://ip_address/api.php?api=[{"talk":{"command":"speaking","remoteIP":"192.168.0.2"},"debug":true}]
	## http://ip_address/api.php?api=[{"talk":{"command":"listening","remoteIP":"192.168.0.2"},"debug":true}]
	## http://ip_address/api.php?api=[{"talk":{"command":"disconnect","remoteIP":"192.168.0.2"},"debug":true}]

	## 마이크 확인
	## $ arecord -l
	## 	**** List of CAPTURE Hardware Devices ****
	## 	card 1: Device [Usb Audio Device], device 0: USB Audio [USB Audio]
	## 	Subdevices: 1/1
	## 	Subdevice #0: subdevice #0
	## -->  -D plughw:Card_No,Devide_No
	## -->  -D plughw:1,0


	if command == 'speaking': # 예 {"talk":{"command":"speaking","remoteIP":$('#talkDestIP').val()}}
		# Local의 마이크를 활성화하고 Remote 스피커로 출력 - kill: arecord, oggenc, sshpass
		result = cmd_proc_Popen("arecord -f cd -D plughw:1,0 -t raw | oggenc - -r | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@{} 'cat - | mplayer -volume {} -' >/dev/null 2>&1 &".format(remoteIP, cfg["talk"]["speaking"]["volume"]))
		sendDataToJsPort('btn_status_talk', {'id':'speaking', 'status':False}) # 사용중
		sendDataToJsPort('btn_status_talk', {'id':'disconnect', 'status':True}) # 대기중
		logger.info("talkAction speaking - {}".format(result))
		return "talkAction speaking {}".format(result)
	elif command == 'listening':
		# Remote의 마이크를 활성화하고 Local 스피커로 출력 - kill: sshpass, mplayer
		result = cmd_proc_Popen("sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@{} 'arecord -f cd -D plughw:1,0 -t raw | oggenc - -r ' | mplayer -volume {} - >/dev/null 2>&1 &".format(remoteIP, cfg["talk"]["listening"]["volume"]))
		sendDataToJsPort('btn_status_talk', {'id':'listening', 'status':False}) # 사용중
		sendDataToJsPort('btn_status_talk', {'id':'disconnect', 'status':True}) # 대기중
		logger.info("talkAction listening - {}".format(result))
		return "talkAction listening {}".format(result)
	elif command == 'disconnect':
		# 전송지연시간을 감안한 시간이후 연결끈기를 실행 한다.
		# cfg["talk"]["closingHold"] 시간 이후 disconnectPipe() 실행
		disconnect = threading.Timer(cfg["talk"]["closingHold"], disconnectPipe)
		disconnect.start() # after hold seconds, run timerTurnOff
		logger.info("talkAction disconnect")
		return 'talkAction disconnect'

	## 본 기능은 JS 에서 구연 하는것이 정상적인 방법임
	## 추후에 작업 요망 2022-07-25 06:50:25
	# elif command == 'appendAllowIP': # 예약 2022-07-25 01:48:11
	# 	# http://192.168.0.50/api.php?api=[{"talk":{"command":"appendAllowIP","remoteIP":"192.168.0.10"},"debug":true}]
	# 	# if remoteIP not in cfg["talk"]["allowIP"]:
	# 	# 	cfg["talk"]["allowIP"].append(remoteIP)		
	# 	# 	return "talkAction added IP"
	# 	# else:
	# 	# 	return "talkAction already exists IP"

	# 	if validate_ip(remoteIP):
	# 		cfg["talk"]["allowIP"][remoteIP] = description
	# 		share["talk"]["allowIP"][remoteIP] = description
	# 		saveConfig(share,'./config.json')
	# 		return "talkAction added IP"
	# 	else:
	# 		return "talkAction invalid IP format"

	# elif command == 'removeAllowIP': # 예약 2022-07-25 01:48:21
	# 	# if remoteIP in cfg["talk"]["allowIP"]:
	# 	# 	cfg["talk"]["allowIP"].remove(remoteIP)		
	# 	# 	return "talkAction removed IP"
	# 	# else:
	# 	# 	return "talkAction not exists IP"
	# 	if remoteIP in share["talk"]["allowIP"].keys():
	# 		cfg["talk"]["allowIP"].pop(remoteIP)
	# 		share["talk"]["allowIP"].pop(remoteIP)
	# 		saveConfig(share,'./config.json')
	# 		return "talkAction removed IP"
	# 	else:
	# 		return "talkAction not exists IP"

	else:
		return "Unknown Talk Command ..."

def systemAction(command, value):
	if command == 'stop_audio': # 예 { "system": { "command": "stop_audio", "value": "" },"debug":true} - 오디오 출력 강제 정지
		result = cmd_proc_Popen('sudo killall -s 9 {} 2>/dev/null'.format(cfg["audio"]["player"]))
		if result: # Success Killall
			return 'Error stop_audio'
		else:
			# 클라이언트에 오디오 종료 이벤트 전송
			sendDataToJsPort('btn_status_audio', {'length':0, 'path':'Stop Audio Out', 'volume':0, 'loop':0}) # 오디오 정지
			return 'Success stop_audio'

	elif command == 'list_audio': 
		return sourceList

	elif command == 'enable_audio': 
		sendDataToJsPort('enable_audio') # itsAPI.js 측 변수 변경 요청 한다.
		cfg['audio']['enable'] = 1 
		return 'Now audio is enabled'

	elif command == 'disable_audio': 
		sendDataToJsPort('disable_audio') # itsAPI.js 측 변수 변경 요청 한다.
		cfg['audio']['enable'] = 0 
		return 'Now audio is disabled'

	elif command == 'saved_mDVR':  # 예 { "system": { "command": "saved_mDVR", "value": "20220506_101420" },"debug":true}
		# 필요에 따라 저장된 폴더위치를 IMS로 전송 할수 있다.
		sendDataToJsPort('btn_status_mDVR', {'ip':'localhost', 'time':value, 'activation':0}) # mDVR의 저장 결과
		return 'Saved footprint'

	elif command == 'sleep': # 예 { "system": { "command": "sleep", "value": "5.0" },"debug":true} - 시간지연 Float
		time.sleep(float(value))
		return 'sleep {}sec'.format(value)

	elif command == 'get_name': 
		return cfg['location']

	elif command == 'set_name': # 예약
		if value:
			sendDataToJsPort('set_name', value) # itsAPI.js 측 변수 변경 요청 한다.
			cfg['location'] = value 
			return 'New location name is {}'.format(value)
		else:
			return 'Unknown location name'

	elif command == 'get_time': 
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	elif command == 'set_time': 
		# Remote Sync Time : rTime=`sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.5 "date '+%Y-%m-%d %H:%M:%S.%N'"` && sudo date -s "$rTime"
		# $command_is = "sudo /bin/date -s '".$_POST["now_dateTime"]."'";
		# return datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

		if value:
			setTime = 'sudo /bin/date -s "{}" 2>/dev/null'.format(value)
			result = cmd_proc_Popen(setTime) # value="2021-10-18 10:11:45"
		else:
			## 적용하려면 value 값 없이 set_time 요청하면 됨
			## Remote 시간과 Local 시간 동기화 - IF ssh Timeout THEN Done.
			remoteTimeServer = '119.207.126.79'
			setTime = '''rTime=`sshpass -pits_iot ssh -o StrictHostKeyChecking=no -o ConnectTimeout=1 pi@{} "date '+%Y-%m-%d %H:%M:%S.%N'" 2>/dev/null `  && sudo date -s "$rTime"'''.format(remoteTimeServer)
			result = cmd_proc_Popen(setTime) # value="2021-10-18 10:11:45"

		if result: # Success Killall
			# 클라이언트에 오디오 종료 이벤트 전송
			sendDataToJsPort('btn_status_set_time', {'now':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) # 오디오 정지
			return 'Success set_time {}'.format(result)
		else:
			return 'Error set_time {}'.format(result)

	elif command == 'health_check':
		# if value == cfg['permission']['accessKey']['keyCode']:
		# 	health = {}
		# 	watchdog = readConfig('../.config/watchdog.json')
		# 	health['cpuPcent'] = watchdog['cpuPcent'].copy()
		# 	health['cpuTemp'] = watchdog['cpuTemp']
		# 	health['diskGb'] = watchdog['diskGb'].copy()
		# 	health['fixed'] = watchdog['fixed'].copy()
		# 	health['memUseKb'] = watchdog['memUseKb'].copy()
		# 	del health['fixed']['deviceModel']
		# 	del health['fixed']['license']
		# 	return health
		# else:
		# 	return 'Security Block: Unmatched License Key'
		health = {}
		watchdog = readConfig('../.config/watchdog.json')
		health['cpuPcent'] = watchdog['cpuPcent'].copy()
		health['cpuTemp'] = watchdog['cpuTemp']
		health['diskGb'] = watchdog['diskGb'].copy()
		health['fixed'] = watchdog['fixed'].copy()
		health['memUseKb'] = watchdog['memUseKb'].copy()
		del health['fixed']['deviceModel']
		del health['fixed']['license']
		return health

	elif command == 'enable_io': 
		if value and is_json_key_present(cfg['execution'], value):
			sendDataToJsPort('enable_io', value) # itsAPI.js 측 변수 변경 요청 한다.
			cfg['execution'][value] = 1 
			return 'Now {} is enabled'.format(value)
		else:
			return 'Unknown IO Port ID {}'.format(value)

	elif command == 'disable_io': 
		if value and is_json_key_present(cfg['execution'], value):
			sendDataToJsPort('disable_io', value) # itsAPI.js 측 변수 변경 요청 한다.
			cfg['execution'][value] = 0
			return 'Now {} is disabled'.format(value)
		else:
			return 'Unknown IO Port ID {}'.format(value)

	elif command == 'trigger_io': # 예 { "system": { "command": "trigger_io", "value": "io01" },"debug":true} 
		sendDataToJsPort('trigger_io', value)
		return 'trigger {}'.format(value)

	elif command == 'restart': # 예약
		# # 정상 적으로 자기 자신을 재실행하는 것은 불가능 하므로
		# # itsAPI.js에 재실행을 요청 한다.
		sendDataToJsPort('restart_self', value)
		exit("Restart ITS API Program ...") 

	elif command == 'reboot': # 예약
		result = cmd_proc_Popen("sudo reboot")
		exit("Reboot ITS API System ...") 

	elif command == 'alarm_job': # 예 { "system": { "command": "alarm_job", "value": "" },"debug":true}
		# 정보 https://tecadmin.net/crontab-in-linux-with-20-examples-of-cron-schedule/
		result = cmd_proc_Popen('crontab -l 2>/dev/null')
		if result: # Success alarm
			return 'Success Alarm Job {}'.format(result)
		else:
			# 클라이언트에 클론 정보 전송
			# 예정 - sendDataToJsPort('btn_status_alarm', {'length':0, 'path':'Stop Audio Out', 'volume':0, 'loop':0}) # 오디오 정지
			return 'Error Read Alarm Job'

	else:
		return 'Unknown Command ...'

def mariaAction(source, target, volume, command, loop):
	pass

def mailReport(sender, receivers, subject, message):
	# sender = 'doNotReply@ecos.com'
	# receivers = ['daivoc@gmail.com']
	# # receivers = ['daivoc@gmail.com', 'daivoc.kim@gmail.com']
	# # content = MIMEText("""body""")
	content = MIMEText(message)
	content['Subject'] = subject
	content['From'] = sender
	content['To'] = ", ".join(receivers)
	try:
		smtpObj = smtplib.SMTP('localhost')
		# smtpObj.set_debuglevel(1)
		smtpObj.sendmail(sender, receivers, content.as_string())  
		return('Successfully sent')
	except smtplib.SMTPException:
		return('Unable to send')

def run_demon_API(): 
	cmd = 'cd %s; node itsAPI.js 2>&1 & ' % (share['path']['api3'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return '\nrun_demon_API'

def sendDataToCustomTcp(host, port, data, isJson=True): # 요청된 명령문 전송
	try: 
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((host, int(port))) 
		if isJson:
			client_socket.send(json.dumps({"data":data}).encode('utf-8')) 
		else:
			client_socket.send(data) 
		logger.info('Success custom->tcp_socket {} {}'.format(host, port))
		# print(client_socket.recv(1024)) ## 응답이 올때까지 기다린다. (수신서버에서 응답코드가 없으면 socket.error 발생 또는 무한대기함)
		client_socket.close() 
		return 1
	except: # 수신측에서 준비가 않되어 있으면 오류
		logger.warning('Error, Check Receiver custom->tcp_socket, {} {}'.format(host, port))
		return 0
	# except socket.error:
	# 	print('socket.error')
	# 	return 0
	# except socket.timeout:
	# 	print('socket.timeout')
	# 	return 0

def sendDataToJsPort(name, value=None): # 요청된 명령문 또는 릴레이 ID 전송 -> itsAPI.js -> itsAPI.html
	try: # itsAPI.js에 요청된 명령문 전송
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
		client_socket.connect((cfg['tcpIpPort']['staticAddress'], cfg['tcpIpPort']['portIn'])) 
		client_socket.send(json.dumps({"name":name,"value":value}).encode('utf-8')) 
		# print(client_socket.recv(1024)) ## 응답이 올때까지 기다린다. (수신서버에서 응답코드가 없으면 무한대기함)
		client_socket.close() 
		return 1
	except:
		return 0

def sock_send(sock, data): # 클라이언트 측에 응답한다.
	try:
		sock.send(json.dumps(data).encode()) # json.dumps(data).encode()
		# sendDataToJsPort('push_gLog', data) # 로그 전송 -> itsAPI.js -> itsAPI.html
	except:
		# 디버그모드에서 클라이언트의 응답이 느릴때 발생 한다.
		logger.warning('Timeout warning: turnoff debug mode, {}'.format(data))
		sendDataToJsPort('push_gLog','Timeout warning: turnoff debug mode')

def telegram_log(to, text): # 텔레그램 체널 또는 그룹으로 메세지 전송 기능 - telegram_log("bot", text)
	if cfg['telegram']['bot01']['token'] and text:
		bot = telegram.Bot(token = cfg['telegram']['bot01']['token'])
	else:
		return None
	text =  text + "\n\n<b>{}</b>\n<code>Device: {}</code>".format(cfg['watchdog']['ioBoard'], cfg['watchdog']['serialKey'])
	if to == "bot" and cfg['telegram']['bot01']['run'] and cfg['telegram']['bot01']['chatID']:
		chat_id = cfg['telegram']['bot01']['chatID']
	elif to == "group" and cfg['telegram']['group01']['run'] and cfg['telegram']['group01']['chatID']:
		chat_id = cfg['telegram']['group01']['chatID']
	elif to == "channel" and cfg['telegram']['channel01']['run'] and cfg['telegram']['channel01']['chatID']:
		chat_id = cfg['telegram']['channel01']['chatID']
	else:
		return None

	return bot.send_message(chat_id = chat_id, parse_mode='HTML', text = text) 

# 모니터링을 위한 페이지 생성
def make_API_map():
	jquery = '%s/jquery/jquery-3.1.1.min.js' % share['path']['common']
	__script_jquery_js__ = '<script>'+open(jquery, 'r').read()+'</script>'

	jquery_ui = '%s/jquery/ui/jquery-ui.js' % share['path']['common']
	__script_jquery_ui_js__ = '<script>'+open(jquery_ui, 'r').read()+'</script>'
	jquery_css = '%s/jquery/ui/jquery-ui.css' % share['path']['common']
	__script_jquery_ui_css__ = '<style>'+open(jquery_css, 'r').read()+'</style>'

	bootstrap_js = '%s/bootstrap4/js/bootstrap.min.js' % share['path']['common']
	__style_bootstrap_js__ = '<script>'+open(bootstrap_js, 'r').read()+'</script>'
	bootstrap_css = '%s/bootstrap4/css/bootstrap.min.css' % share['path']['common']
	__style_bootstrap_css__ = '<style>'+open(bootstrap_css, 'r').read()+'</style>'

	# bootstrap_js_map = '%s/bootstrap4/js/bootstrap.min.js.map' % share['path']['common']
	# __style_bootstrap_js_map__ = '<script>'+open(bootstrap_js_map, 'r').read()+'</script>'
	# bootstrap_css_map = '%s/bootstrap4/css/bootstrap.min.css.map' % share['path']['common']
	# __style_bootstrap_css_map__ = '<style>'+open(bootstrap_css_map, 'r').read()+'</style>'
	
	# bootstrap4_toggle_js = '%s/bootstrap4-toggle/js/bootstrap4-toggle.min.js' % share['path']['common']
	# __style_bootstrap4_toggle_js__ = '<script>'+open(bootstrap4_toggle_js, 'r').read()+'</script>'
	# bootstrap4_toggle_css = '%s/bootstrap4-toggle/css/bootstrap4-toggle.min.css' % share['path']['common']
	# __style_bootstrap4_toggle_css__ = '<style>'+open(bootstrap4_toggle_css, 'r').read()+'</style>'
	
	__html_sensor_button__ = ''
	__html_relay_button__ = ''
	__html_alarm_button__ = ''
	__html_timer_button__ = ''

	## 질의 응답이 있으면 
	# if os.path.isfile('./QnA.jpg'):
	# 	data_qna = open('./QnA.jpg', 'rb').read().encode('base64').replace('\n', '')
	# 	__html_QnA__ = '<img src="data:image/png;base64,{0}">'.format(data_qna)
	# else:

	__html_QnA__ = ''
	# download = '<a href="http://'+cfg['tcpIpPort']['staticAddress']+'/api_qna.pdf'+'" style="position: absolute;bottom: 1vh;right: 1vw;color: gray;font-size: 6pt;">Download QnA</a>'
	if os.path.isfile(cfg['userPath']['webPath']+'/api_readme.pdf'): # 
		__html_QnA__ = '<a href="http://'+cfg['tcpIpPort']['staticAddress']+'/api_readme.pdf'+'" style="position: fixed;bottom: 0vh;right: 60px;color: gray;font-size: 6pt;">READ ME</a>'
	# if os.path.isfile(cfg['userPath']['webPath']+'/api_qna.pdf'): # 
	# 	__html_QnA__ += '<a href="http://'+cfg['tcpIpPort']['staticAddress']+'/api_qna.pdf'+'" style="position: fixed;bottom: 0vh;right: 30px;color: gray;font-size: 6pt;">QnA</a>'
	# if os.path.isfile(cfg['userPath']['webPath']+'/api_quickGuide.pdf'): # 
	# 	__html_QnA__ += '<a href="http://'+cfg['tcpIpPort']['staticAddress']+'/api_quickGuide.pdf'+'" style="position: fixed;bottom: 0vh;right: 60px;color: gray;font-size: 6pt;">Quick Guide</a>'

	for key, value in sorted(cfg['setBD']['setIO'].items()):
		if value:
			__html_relay_button__ += """
			<div class='group'>
			<button id='{0}' type='button' class='btn btn-outline-success relay' data-toggle='button' title='Relay{1}'>{2}</button>
			<input id='des_{0}' type='text' class='desc' readonly='readonly' disabled='disabled' value='{2}'>
			<button id='exe_{0}' type='button' class='btn btn-outline-danger exec' readonly='readonly' disabled='disabled' data-toggle='button'></button>
			</div>""".format(key,key[-2:],cfg['description'][key])
		else:
			__html_sensor_button__ += """
			<div class='group_R'>
			<button id='{0}' type='button' class='btn btn-outline-primary sensor' title='Sensor{1}'>{2}</button>
			<input id='des_{0}' type='text' class='desc' readonly='readonly' disabled='disabled' value='{2}'>
			<input id='cmd_{0}' type='text' class='cmds' readonly='readonly' disabled='disabled' value='{3}' placeholder='Json Only'>
			<button id='trg_{0}' type='button' class='btn btn-warning trgr' readonly='readonly' disabled='disabled' data-toggle='button'></button>
			<button id='exe_{0}' type='button' class='btn btn-outline-danger exec' readonly='readonly' disabled='disabled' data-toggle='button'></button>
			<button id='add_{0}' type='button' class='btn btn-outline-info gpio' readonly='readonly' disabled='disabled'>R</button>
			</div>""".format(key,key[-2:],cfg['description'][key],key,cfg['command'][key])

	## 알람 시스템 클론탭
	for key in sorted(cfg['alarmCmds']): # 순서 정렬
		if cfg['alarmCmds'][key]['enable']:
			__html_alarm_button__ += """
			<div class='group_A'>
			<button id='{0}' type='button' class='btn btn-outline-info alarm' title='Alarm{1}'>{2}</button>
			<input id='desc_A_{0}' type='text' class='desc' readonly='readonly' disabled='disabled' value=''>
			<input id='cmds_A_{0}' type='text' class='cmds' readonly='readonly' disabled='disabled' value='' placeholder='Json Only'>
			<input id='time_A_{0}' type='text' class='time' readonly='readonly' disabled='disabled' value='' placeholder='m h d M w'>
			</div>""".format(key,key[-2:],cfg['alarmCmds'][key]['desc'])

	for key in cfg['timerCmds']: 
		if cfg['timerCmds'][key]['enable']:
			__html_timer_button__ += """
			<div class='group_A'>
			<button id='{0}' type='button' class='btn btn-outline-warning timer' title='Timer{1}'>{2}</button>
			<input id='desc_T_{0}' type='text' class='desc' readonly='readonly' disabled='disabled' value=''>
			<input id='cmds_T_{0}' type='text' class='cmds' readonly='readonly' disabled='disabled' value='' placeholder='Json Only'>
			<input id='time_T_{0}' type='text' class='time' readonly='readonly' disabled='disabled' value='' placeholder='Second'>
			</div>""".format(key,key[-2:],cfg['timerCmds'][key]['desc'])

	__html_power_button__ = ''
	for key, value in sorted(cfg['setBD']['setPW'].items()):
		if value:
			__html_power_button__ += """
			<div class='group'>
			<button id='{0}' type='button' class='btn btn-outline-warning power' data-toggle='button' title='Power{1}'>{2}</button>
			<input id='des_{0}' type='text' class='desc' readonly disabled value='{2}'>
			<button id='exe_{0}' type='button' class='btn btn-outline-danger exec' readonly='readonly' disabled='disabled' data-toggle='button'></button>
			</div>""".format(key,key[-2:],cfg['description'][key])
		else:
			__html_power_button__ += ''

	__html_audio_button__ = """
		<div class='group'>
		<button id='audio_stop' type='button' class='btn btn-outline-info audio_stop'>🔊</button>
		<input id='audio_name' type='text' class='audioName' readonly='readonly' value='' placeholder='Audio Info'>
		<button id='audio_exec' type='button' class='btn btn-outline-danger exec' readonly='readonly' disabled='disabled' data-toggle='button' value=''></button>
		</div>"""

	__html_talk_button__ = """
		<div class='group'>
		<button id='speaking' type='button' class='btn btn-outline-info speaking'>speaking</button>
		<button id='listening' type='button' class='btn btn-outline-info listening'>listening</button>
		<button id='disconnect' type='button' class='btn btn-outline-info disconnect' disabled='disabled'>disconnect</button>
		<input id='talkDestIP' type='text' class='talkName' value='' placeholder='Target IP'>
		<button id='talk_exec' type='button' class='btn btn-outline-danger exec' readonly='readonly' disabled='disabled' data-toggle='button' value=''></button>
		</div>"""
		
	if cfg['camera']['name']: # mDVR이 실행중이라 판단 되면
		__html_mDVR_button__ = """
			<div class='group'>
			<button id='mDVR_stop' type='button' class='btn btn btn-outline-primary mDVR_stop'>🎦</button>
			<div id='mDVR_name' class='mDVRName'></div>
			<button id='mDVR_exec' type='button' class='btn btn-outline-danger exec' readonly='readonly' disabled='disabled' data-toggle='button' value=''></button>
			</div>"""
	else:
		__html_mDVR_button__ = ''

	with open(cfg['file']['html_source'], 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_css__', __script_jquery_ui_css__)
		
		# # 클라이언트 측 글로번 변수 사전 선언 
		# tmp_its_tmp = tmp_its_tmp.replace('__script_global_var__', json.dumps(cfg).encode('utf-8'))

		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_js__', __style_bootstrap_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css__', __style_bootstrap_css__)
		# tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_js_map__', __style_bootstrap_js_map__)
		# tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css_map__', __style_bootstrap_css_map__)
		
		# tmp_its_tmp = tmp_its_tmp.replace('__html_title__', cfg['title'].encode('utf8'))
		tmp_its_tmp = tmp_its_tmp.replace('__url_server_home__', cfg['tcpIpPort']['staticAddress'])

		tmp_its_tmp = tmp_its_tmp.replace('__html_relay_button__', __html_relay_button__)
		tmp_its_tmp = tmp_its_tmp.replace('__html_sensor_button__', __html_sensor_button__)
		tmp_its_tmp = tmp_its_tmp.replace('__html_power_button__', __html_power_button__)
		tmp_its_tmp = tmp_its_tmp.replace('__html_audio_button__', __html_audio_button__)
		tmp_its_tmp = tmp_its_tmp.replace('__html_talk_button__', __html_talk_button__)
		tmp_its_tmp = tmp_its_tmp.replace('__html_mDVR_button__', __html_mDVR_button__)
		tmp_its_tmp = tmp_its_tmp.replace('__html_alarm_button__', __html_alarm_button__ + __html_timer_button__)
		# tmp_its_tmp = tmp_its_tmp.replace('__html_timer_button__', __html_timer_button__)

		tmp_its_tmp = tmp_its_tmp.replace('__html_QnA__', __html_QnA__)
		
		with open(cfg['file']['html_target'], 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()

# 타이머 그룹 실행 <<<
# 콘솔 윈도 내에 타이머 설정을 실행 한다.
# 최소 분단위의 알람설정과 달리 초단위 설정이 가능 하다.
# 타이머 갯수는 config.json -> timerCmds 내 항목 추가로 가능 하다.

class myThread (threading.Thread):
	def __init__(self, name, command, delay):
		threading.Thread.__init__(self)
		# self.threadID = threadID
		self.name = name
		self.command = command
		self.delay = delay
	def run(self):
		print("\tStarting {} {} {}".format(self.name, json.dumps(self.command), self.delay))
		threadAction(self.name, self.command, self.delay)

def threadAction(name, command, delay): # 반복 구간
	while True:
		time.sleep(delay)

		if name == 'Heartbeat': # 하트비트 전송 
			sendDataToJsPort('heartbeat', delay)
		
		if command:
			if command['host']:
				host = command['host']
			else:
				host = cfg['tcpIpPort']['staticAddress']
			if command['port']:
				port = int(command['port'])
			else:
				port = cfg['portAPI']

			sendDataToCustomTcp(host, port, json.dumps(command['data']).encode(), False) # 요청된 명령문 전송

# >>> 타이머 그룹 실행

def main():
	message = ''
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # <--- 아직 검증안됨 "Address already in use" 무시
		s.bind((cfg['tcpIpPort']['staticAddress'], cfg['portAPI'])) # <------- 소켓을 주소로 바인딩
		s.listen(1) # <------ listening 시작. 최대 클라이언트 연결 수 5개
		logger.info('Daemon of API {0}:{1}'.format(cfg['tcpIpPort']['staticAddress'],cfg['portAPI']))
		message += 'Daemon of API {0}:{1}\n'.format(cfg['tcpIpPort']['staticAddress'],cfg['portAPI'])
	except:
		logger.warning('SOCKET Error {0}:{1}'.format(cfg['tcpIpPort']['staticAddress'],cfg['portAPI']))
		sys.exit('SOCKET Error {0}:{1}'.format(cfg['tcpIpPort']['staticAddress'],cfg['portAPI']))

	print(run_demon_API())
	print('Log : {}'.format(filename))
	print('Local Audio List:')
	for i in range(len(sourceList)):
		print('\t{}: {}'.format(i+1,sourceList[i]))

	## 메일 전송 <<<
	message += 'ITS API 실행 :{}'.format(time.ctime())
	snd = cfg['reportMail']['sender']
	rcv = cfg['reportMail']['receiver'].split(",")
	sbj = cfg['reportMail']['subject'].encode('utf-8')
	sgn = '\n\n--\n{}'.format(cfg['reportMail']['signature'].encode('utf-8'))
	frq = int(cfg['reportMail']['frequency'])
	# print(snd, rcv, sbj, sgn, frq)
	message += sgn # 서명란 붙임 
	## print(mailReport(snd, rcv, sbj, message))
	# >>> 메일 전송

	# 타이머 그룹 실행 <<<
	print('Timer Job:')
	for key in cfg['timerCmds']:
		if cfg['timerCmds'][key]['time']: # 시간값이 있을때 실행한다.

			try: # json 확인
				timeCmds = json.loads(cfg['timerCmds'][key]['cmd'])
			except ValueError as e:
				timeCmds = ''

			timeDue = float(cfg['timerCmds'][key]['time'])
			timeDesc = cfg['timerCmds'][key]['desc'].encode('utf-8')

			if timeDue and cfg['timerCmds'][key]['enable']:
				# print(timeDue, timeCmds, timeDesc, time_host, time_port)
				myThread(timeDesc, timeCmds, timeDue).start()

	# >>> 타이머 그룹 실행

	while True:
		sock, sender_API = s.accept()
		# print('From:', sender_API[0])

		###################
		## 아이피 필터링 <<
		###################
		if sender_API[0] == cfg['tcpIpPort']['staticAddress']:
			pass # 자신의 아이피는 통과시킨다.
		else:
			# filter(None) -> 비어있는 값 삭제
			allow = list(filter(None,cfg['permission']['filterIP']['allow'].split(',')))
			deny = list(filter(None,cfg['permission']['filterIP']['deny'].split(',')))
			if len(allow) and sender_API[0] not in allow:
				print("IP allow {} {}".format(sender_API[0],allow))
				continue

			if len(deny) and sender_API[0] in deny:
				print("IP deny {} {}".format(sender_API[0],deny))
				continue
		###################
		## >> 아이피 필터링
		###################

		while True: # <-------- 클라이언트 연결이 오면 루프로 들어가서 데이터가 수신을 기다림
			# data = sock.recv(buffer*8)
			# if not data:
			# 	break

			data = sock.recv (buffer)
			if not data:
				break
			else:
				if len(data) < buffer:
					pass
				else:
					while True: 
						part = sock.recv (buffer)
						data += part
						if len(part) < buffer:
							break
			# print("debug - port read: {}".format(data))
			# data -> [{"gpio":{"status":"0","id":"io09","hold":"0.1","interval":"1","count":"4","actID":"io01"}}]
			try:
				arrJson = json.loads(data)
			except:
				sock_send(sock,{'ip':sender_API[0], 'category':'unknown', 'msg':'JSON format error'})
				logger.info('category:unknown msg:JSON format error - {} {}'.format(sender_API[0], data))
				break

			# if isinstance(arrJson, dict):
			if isinstance(arrJson, list): # 인스턴스가 데이터 타입과 일치할 경우에는 True
				sendDataToJsPort('push_gLog', 'From: {} {}'.format(sender_API[0], data)) # 클라이언트 모니터링(브라우저)에 현재의 명령문(Log) 전송
			else: # From 
				# http://192.168.0.50/api.php?api=[{"trigger":{"id":"io02"}}]
				if 'trigger' in arrJson: # 외부포트로부터 직접 명령을 접수한후 배열을 선언한다.
					# print("TRIGGER {}".format(cfg['command'][arrJson['trigger']['id']]))
					if arrJson['trigger']['id'] in cfg['command']: # 센서 아이디 (io01 ~ io08)
						# Thread 타이머를 구현하기 위해 유니크한 키값을 생성하기 위한 작업
						if cfg['command'][arrJson['trigger']['id']]:
							logger.info("category:trigger from {}, cmd ID {}".format(sender_API[0], arrJson['trigger']['id']))
							cmdIS = json.loads(cfg['command'][arrJson['trigger']['id']])
							for i in range(len(cmdIS['data'])):
								args = cmdIS['data'][i]
								if 'custom' in args:
									cmdIS['data'][i]['custom']['actID'] = arrJson['trigger']['id']
							arrJson = cmdIS['data'] # cfg['command'][트리거ID]내 명령을 접수함
						else:
							break

						# if cfg['command'][arrJson['trigger']['id']]:
						# 	cmdIS = json.loads(cfg['command'][arrJson['trigger']['id']])
						# 	arrJson = cmdIS['data'] # cfg['command'][트리거ID]내 명령을 접수함
						# else:
						# 	break
					else:
						sock_send(sock,{'ip':sender_API[0], 'category':'trigger', 'msg':'Mismatch trigger value'})
						logger.warning('category:unknown, msg:Mismatch trigger value {}'.format(arrJson['trigger']['id']))
						break
					# print(arrJson)
				else:
					sock_send(sock,{'ip':sender_API[0], 'category':'unknown', 'msg':'Data should be JSON Array'})
					logger.info('JSON Array not JSON Objects. {}'.format(arrJson))
					break
			
			# 접수되는 모든 정상이벤트를 로그에 저장함
			# logger.info('from:{} {}'.format(sender_API[0], arrJson))

			for i in range(len(arrJson)):
				args = arrJson[i]
				# print(args)
				
				# 카테고리는 내용을 포함 해서 필수 이다.
				if all (k in cfg['category'].keys() for k in args):
					pass
				else:
					sock_send(sock,{'ip':sender_API[0], 'category':'unknown', 'msg':'Missing category value'})
					logger.warning('category:unknown, msg:Missing category value {}'.format(i))
					continue # Complex Command 인경우 관련 명령만 제외하고 다음 명령을 수행 한다.

				# keySource 값이 존재하면 키 검증을 한다.
				# ECOS -> At77NUjFJOwbEdsXPT+utXW3Czt3e7sqN0Gp1mmHvnA= "keyCode":"At77NUjFJOwbEdsXPT+utXW3Czt3e7sqN0Gp1mmHvnA="
				# http://192.168.0.80/api.php?api=[{"gpio":{"status":"2","id":"io11","hold":"3.16","msg":"},"debug":true,"keyCode":"02defb3548c524ec1b11db173d3faeb575b70b3b777bbb2a3741a9d66987be70"}]
				# http://192.168.0.80/api.php?api=[{"gpio":{"status":"2","id":"io11","hold":"3.16","msg":"},"debug":true]
				if cfg['permission']['accessKey']['keySource']: 
					if 'keyCode' in args:
						if args['keyCode'] == cfg['permission']['accessKey']['keyCode']:
							pass
						else:
							sock_send(sock,{'ip':sender_API[0], 'category':'keyCode', 'msg':'Mismatch keyCode value'})
							logger.warning('category:unknown, msg:Mismatch KeyCode value {}'.format(args))
							continue
					else:
						sock_send(sock,{'ip':sender_API[0], 'category':'keyCode', 'msg':'Missing keyCode value'})
						logger.warning('category:unknown, msg:Missing KeyCode value {}'.format(args))
						continue

				# 디버그 모드 상태에 따라 오류 메시지 출력 결정
				if args and 'debug' not in args:
					args['debug'] = False
				else: # 내용이 없다고 무시하면 않됨
					pass

				if 'gpio' in args:
					# http://192.168.0.80/api.php?api=[{"gpio":{"status":"2","id":"io12","hold":"0.1","interval":"5"},"debug":true}]
					# http://192.168.0.80/api.php?api=[{"gpio":{"status":"2","id":"io12","hold":"0.1","interval":"5"},"debug":true}]
					if all (k in args['gpio'] for k in cfg['category']['gpio'].keys()):
						if args['gpio']['status'] not in ('0', '1', '2', '3', '6', '7', '8', '9'):
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'gpio', 'status':args['gpio']['status'], 'msg':'Missing status value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing status value'))
						elif args['gpio']['status'] in ('0', '1', '2', '3') and not args['gpio']['id']: # 0, 1, 2, 3인 경우 id값이 있어야 한다.
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'gpio', 'status':args['gpio']['status'], 'msg':'Missing id value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing id value'))
						else:
							# gpioAction(status, id, hold)
							# 같은 센서에서 인터벌 시간내에 발생하는 이벤트는 무시한다.
							if 'count' in args['gpio']:
								if args['gpio']['count']:
									count = int(args['gpio']['count'])
							else:
								count = 0

							if 'interval' in args['gpio']:
								if args['gpio']['interval']:
									interval = float(args['gpio']['interval'])
							else:
								interval = 0

							if count and interval:
								# 타이머 시간이내 카운터 횟수 이상이면 알람발생
								# 타이머가 종료 되면 카운터 초기화
								# print('A', count, gpioCount[args['gpio']['id']], interval)
								if setGpioTimer(args['gpio']['id'], interval): # 타이머가 > 0 이고 카운터도 > 0 이면
									gpioCount[args['gpio']['id']] = 1 # 초기화 : 최초 이벤트를 유효처리 한다.
								else:
									gpioCount[args['gpio']['id']] += 1

								if gpioCount[args['gpio']['id']] >= count:
									response = gpioAction(args['gpio']['status'], args['gpio']['id'], args['gpio']['hold'])
									# print('AAA')

							elif count == 0 and interval:
								# print('B', count, gpioCount[args['gpio']['id']], interval)
								if setGpioTimer(args['gpio']['id'], interval): # 타이머가 > 0 이고 카운터도 0 이면
									response = gpioAction(args['gpio']['status'], args['gpio']['id'], args['gpio']['hold'])
									# print('BBB')

							elif count and interval == 0: # 타이머가 0 이고 카운터도 > 0 이면
								# print('C', count, gpioCount[args['gpio']['id']], interval)
								gpioCount[args['gpio']['id']] += 1
								if gpioCount[args['gpio']['id']] >= count:
									response = gpioAction(args['gpio']['status'], args['gpio']['id'], args['gpio']['hold'])
									gpioCount[args['gpio']['id']] = 0
									# print('CCC')

							else: # count == 0 and interval == 0 : # 타이머가 0 이고 카운터도 0 이면
								# print('D', count, gpioCount[args['gpio']['id']], interval)
								response = gpioAction(args['gpio']['status'], args['gpio']['id'], args['gpio']['hold']) 
								# print('DDD')

						if args['debug']:
							if response: # Success
								sock_send(sock,{'ip':sender_API[0], 'category':'gpio', 'status':args['gpio']['status'], 'response':response})
							else: # Error
								sock_send(sock,{'ip':sender_API[0], 'category':'gpio', 'status':args['gpio']['status'], 'msg':'No action'})
								logger.warning('from:{} {}'.format(sender_API[0], 'No action'))
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'gpio', 'status':args['gpio']['status'], 'msg':'Missing args'})

					continue # <-- 현 Loop 종료

				if 'audio' in args and cfg['audio']['enable']: # 
					# {"host": "","port": "","data": [{"system":{"command":"stop_audio","value":""}},{"audio": {"source": "inspiring-cinematic-background-music-for-videos-5717.mp3","volume": "20","loop": "0"}}]}
					if all (k in args['audio'] for k in cfg['category']['audio'].keys()):
						if not args['audio']['source']:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Missing source value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing source value'))
						# elif not args['audio']['target']:
						# 	if args['debug']:
						# 		sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Missing target value'}))
						elif not args['audio']['volume']:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Missing volume value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing volume value'))
						# elif not args['audio']['command']:
						# 	if args['debug']:
						# 		sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Missing command value'}))
						elif not args['audio']['loop']:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Missing loop value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing loop value'))
						else:
							# 오디오 전송
							audioPath = audioName(args['audio']['source'])
							# audioAction(source, target, volume, command, loop)
							# print(audioPath)
							if audioPath:
								# 오디오 출력
								response = audioAction(audioPath, args['audio']['volume'], args['audio']['loop'])
								telegram_log("group", "🔊 <b>Audio Alarm</b>\nfrom {} - {}".format(cfg['location'], cfg['tcpIpPort']['staticAddress'])) # 텔레그램 메세지 전송 요청
								if response: # Busy or Error
									if args['debug']:
										sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':response })
										logger.warning('from:{} {}'.format(sender_API[0], 'Busy Audio Port'))
								else: # Success
									if args['debug']:
										sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'response':{'sent':args['audio']['source']}})

									try: # 클라이언트에 오디오 사용 상태를 전송(길이 및 오디오명)
										audioInfo = MP3(audioPath) # 오디오파일의 실행시간을 가지고 온다(초)
										# audioInfo = sox.file_info.duration(audioPath)
										# print("2022-06-24 03:44:08", audioInfo.info.length, audioPath)
										sendDataToJsPort('btn_status_audio', {'length':audioInfo.info.length, 'path':audioPath.split('/')[-1], 'volume':args['audio']['volume'], 'loop':args['audio']['loop']})
									except Exception as e:
										# print(e,audioPath)
										sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'It is not MP3 or bad format' })
										logger.warning('from:{} {}'.format(sender_API[0], 'MP3 Format error'))
							else:
								sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Audio File Not Found'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Audio File Not Found'))
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'audio', 'msg':'Missing args or Disable Audio Out'})
							logger.warning('from:{} {}'.format(sender_API[0], 'Missing audio args or Disable Audio Out'))

					# result = audioIPOut(source, target, volume, command, loop) ## mplayer를 통해 오디오 출력

					continue # <-- 현 Loop 종료

				if 'talk' in args and cfg['talk']['enable']:
					## http://ip_address/api.php?api=[{"talk":{"command":"speaking","remoteIP":"192.168.0.2"},"debug":true}]
					## http://ip_address/api.php?api=[{"talk":{"command":"listening","remoteIP":"192.168.0.2"},"debug":true}]
					## http://ip_address/api.php?api=[{"talk":{"command":"disconnect","remoteIP":"192.168.0.2"},"debug":true}]
					if all (k in args['talk'] for k in cfg['category']['talk'].keys()):
						if not args['talk']['command']:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'talk', 'msg':'Missing command value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing command value'))
						else:
							## 원격아이피 형식확인(validate_ip)과 수용가능(cfg['talk']['allowIP'])한지 획인함 args['talk']['remoteIP'] in share["talk"]["allowIP"].keys()
							if validate_ip(args['talk']['remoteIP']) and args['talk']['remoteIP'] in cfg['talk']['allowIP'].keys():
								logger.info('from:{} {} {}'.format(sender_API[0], args['talk']['command'], args['talk']['remoteIP']))
								response = talkAction(args['talk']['command'], args['talk']['remoteIP'])
								if args['debug']:
									sock_send(sock,{'ip':sender_API[0], 'category':'talk', 'command':args['talk']['command'], 'msg':response })
							else:
								sock_send(sock,{'ip':sender_API[0], 'category':'talk', 'msg':'Invalid or unallowable target IP', 'target':args['talk']['remoteIP']})
								sendDataToJsPort('push_gLog', 'Invalid or unallowable target IP') # 로그 전송 -> itsAPI.js -> itsAPI.html
								logger.warning('Invalid or unallowable target IP {}'.format(args['talk']['remoteIP']))
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'talk', 'msg':'Missing args'})
							logger.warning('from:{} {}'.format(sender_API[0], 'Missing talk args'))

					continue # <-- 현 Loop 종료

				if 'camera' in args: # still_shot, motion_shot, list_shot, download_shot, footprint
					if all (k in args['camera'] for k in cfg['category']['camera'].keys()):
						if not args['camera']['command']:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'camera', 'msg':'Missing command value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing command value'))
						elif args['camera']['command'] == 'footprint':
							# 임시 폴더 명 dirOn 가 생성 되면 동시에 날짜와 시간폴더로 전환되며 그 시점의 이미지를 저장 한다.
							# cmd = 'mkdir {}{}/camera/dirOn 2>/dev/null'.format(share['path']['its_web'],share['path']['user']['image'])

							# if cfg['camera']['config'] and cfg['camera']['name']: # 변수 mDVR를 통해 실행여부 확인
							if 'enable' in cfg['mDVR'] and 'dirOn' in cfg['mDVR']: # 변수 mDVR를 통해 실행여부 확인
								cmd = 'mkdir {} 2>/dev/null'.format(cfg['mDVR']['dirOn'])
								response = cmd_proc_Popen(cmd)
								# eventAt = time.strftime('%Y%m%d_%H%M%S', time.localtime()) # 저장할 경로 + 펄더명
								eventAt = time.strftime('%Y%m%d_%H%M%S', time.localtime()) # 저장할 경로 + 펄더명

								if args['debug']:
									if response: # Error
										sock_send(sock,{'ip':sender_API[0], 'category':'camera', 'command':args['camera']['command'], 'msg':response })
									else: # Success
										sock_send(sock,{'ip':sender_API[0], 'category':'camera', 'response':{'sent':args['camera']['command']}})
										sendDataToJsPort('btn_status_mDVR', {'ip':sender_API[0], 'time':eventAt, 'activation':1}) # mDVR에 저장 요청
							else:
								sock_send(sock,{'ip':sender_API[0], 'category':'camera', 'command':args['camera']['command'], 'msg':'Not Running mDVR' })

						elif args['camera']['command'] == 'still_shot':
							pass
						elif args['camera']['command'] == 'motion_shot':
							pass
						elif args['camera']['command'] == 'list_shot':
							pass
						else:
							sock_send(sock,{'ip':sender_API[0], 'category':'camera', 'command':args['camera']['command'], 'msg':'Unknown Command' })
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'camera', 'msg':'Missing args'})
							logger.warning('from:{} {}'.format(sender_API[0], 'Missing camera args'))

					continue # <-- 현 Loop 종료

				if 'system' in args: 
					if all (k in args['system'] for k in cfg['category']['system'].keys()):
						if not args['system']['command']:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'command', 'msg':'Missing command value'})
								logger.warning('from:{} {}'.format(sender_API[0], 'Missing command value'))
						else:
							logger.info('from:{} {} {}'.format(sender_API[0], args['system']['command'], args['system']['value']))
							response = systemAction(args['system']['command'], args['system']['value'])
							# print ("2022-06-24 03:37:46", response)
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'category':'system', 'command':args['system']['command'], 'msg':response })
								# if response: # Error
								# 	sock_send(sock,{'ip':sender_API[0], 'category':'system', 'command':args['system']['command'], 'msg':response })
								# else: # Success
								# 	sock_send(sock,{'ip':sender_API[0], 'category':'system', 'response':{'sent':args['system']['command']}})
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'system', 'msg':'Missing args'})
							logger.warning('from:{} {}'.format(sender_API[0], 'Missing system args'))

					continue # <-- 현 Loop 종료

				if 'maria' in args:
					pass
					continue # <-- 현 Loop 종료

				if 'messenger' in args:
					# {"host": "","port": "","data": [{"messenger": {"sendMessage": "tcp_socket"},"debug":true}]}
					# {"host": "","port": "","data": [{"messenger": {"sendMessage": "from ip 10"},"server": {"host": "192.168.0.80","port": "34001"}}]}
					# http://192.168.0.80/api.php?api=[{"messenger": {"sendMessage": "tcp_socket"},"debug":true}]
					# http://192.168.0.10/api.php?api=[{"messenger": {"sendMessage": "from ip 10"},"server": {"host": "192.168.0.80","port": "34001"}}]
					# echo '[{"messenger": {"sendMessage": "tcp_socket"},"debug":true}]' | nc 192.168.0.80 34001 -q 0
					# echo '[{"messenger": {"sendMessage": "from ip 10"},"server": {"host": "192.168.0.80","port": "34001"}}]' | nc 192.168.0.10 34001 -q 0
					# https://api.telegram.org/bot<TOKEN>/getUpdates
					# https://api.telegram.org/bot5579880570:AAHZD3f6_6EL-qFl0PzxdRrRy6VkiYpmxqo/getUpdates
					
					
					# print(cfg['category']['messenger'].keys())
					if all (k in args['messenger'] for k in cfg['category']['messenger'].keys()):
						if args['messenger']['sendMessage']:
							response = telegram_log("bot", args['messenger']['sendMessage'])
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'response': str(response) })
						else:
							if args['debug']:
								sock_send(sock,{'ip':sender_API[0], 'response': "no message" })

						# # print(bot.get_me())
						# # print(bot.get_updates())
						# if 'getUpdates' in args['messenger']:
						# 	if args['messenger']['getUpdates'] == True:
						# 		bot = telegram.Bot(token = cfg['telegram']['bot01']['token'])
						# 		response = bot.get_updates()
						# 		if args['debug']:
						# 			sock_send(sock,{'ip':sender_API[0], 'response': str(response) })
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'messenger', 'msg':'Missing args'})
							logger.warning('from:{} {}'.format(sender_API[0], 'Missing messenger args'))

					continue # <-- 현 Loop 종료

				if 'custom' in args:
					# {"host": "","port": "","data": [{"custom": {"method": "tcp_socket","isJson": true,"data": {"id_01": "name_01","id_02": "name_02","id_03": "name_03","id_04": "name_04"},"count": "3","interval": "3"},"server": {"host": "192.168.0.90","port": "33001"},"debug": true}]}
					# {"host":"","port":"","data":[{"custom":{"method":"tcp_socket", "data":"AAA", "isJson":false, "count":4, "interval":2},"server":{"host":"192.168.0.80","port":"54321"},"debug": true}]}

					if all (k in args['custom'] for k in cfg['category']['custom'].keys()):
						if 'count' in args['custom']:
							if args['custom']['count']:
								count = int(args['custom']['count'])
						else:
							count = 0

						if 'interval' in args['custom']:
							if args['custom']['interval']:
								interval = float(args['custom']['interval'])
						else:
							interval = 0

						if 'actID' in args['custom']:
							actID = args['custom']['actID']
						else:
							actID = 'usr04'

						# print("debug - Count:{}, Interval:{}, actID:{}".format(count,interval,actID),actCount[actID],actTimer[actID])
						if args['custom']['method'] == 'tcp_socket':
							host = args['server']['host']
							port = args['server']['port']

							if count and interval:
								# 타이머 시간이내 카운터 횟수 이상이면 알람발생
								# 타이머가 종료 되면 카운터 초기화
								if setThreadingTimer(actID, interval): # 타이머가 > 0 이고 카운터도 > 0 이면
									actCount[actID] = 1 # 초기화 : 최초 이벤트를 유효처리 한다.
								else:
									actCount[actID] += 1

								if actCount[actID] >= count:
									sendDataToCustomTcp(host, port, args['custom']['data'], args['custom']['isJson']) # 요청된 명령문 전송

							elif count == 0 and interval:
								if setThreadingTimer(actID, interval): # 타이머가 > 0 이고 카운터도 0 이면
									sendDataToCustomTcp(host, port, args['custom']['data'], args['custom']['isJson']) # 요청된 명령문 전송

							elif count and interval == 0: # 타이머가 0 이고 카운터도 > 0 이면
								actCount[actID] += 1
								if actCount[actID] >= count:
									sendDataToCustomTcp(host, port, args['custom']['data'], args['custom']['isJson']) # 요청된 명령문 전송
									actCount[actID] = 0

							else: # count == 0 and interval == 0 : # 타이머가 0 이고 카운터도 0 이면
								sendDataToCustomTcp(host, port, args['custom']['data'], args['custom']['isJson']) # 요청된 명령문 전송 

							# sendDataToCustomTcp(host, port, args['custom']['data'], args['custom']['isJson']) # 요청된 명령문 전송

						elif args['custom']['method'] == 'http_get':
							'''
							try:
								# http authentication 
								# https://requests.readthedocs.io/en/latest/user/authentication/
								if args['server']['username'] and args['server']['password']:
									url = args['server']['url']
									username = args['server']['username']
									password = args['server']['password']
									# from requests.auth import HTTPBasicAuth
									# basic = HTTPBasicAuth(username, password)
									# response = response = requests.get(url, auth=basic, params = args['custom']['data'])
									response = response = requests.get(url, auth=(username, password), params = args['custom']['data'])
								else:
									response = requests.get(url = args['server']['url'], params = args['custom']['data'])
								logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_get {}'.format(args['server']['url'])))
							except Exception as e:
								logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_get {} {}'.format(args['server']['url'], e)))
							'''
							if 'username' in args['server'] and  'password' in args['server']:
								username = args['server']['username']
								password = args['server']['password']
								basicAuth = True
							else:
								basicAuth = False

							url = args['server']['url']

							if count and interval:
								# 타이머 시간이내 카운터 횟수 이상이면 알람발생
								# 타이머가 종료 되면 카운터 초기화
								if setThreadingTimer(actID, interval): # 타이머가 > 0 이고 카운터도 > 0 이면
									actCount[actID] = 1 # 초기화 : 최초 이벤트를 유효처리 한다.
								else:
									actCount[actID] += 1

								if actCount[actID] >= count:
									try:
										if basicAuth:
											response = requests.get(url, auth=(username, password), params = args['custom']['data'])
										else:
											response = requests.get(url, params = args['custom']['data'])
										# requests.get(url = args['server']['url'], params = args['custom']['data'])
										logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_get {}, auth:{}'.format(args['server']['url'],basicAuth)))
									except Exception as e:
										logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_get {} {}'.format(args['server']['url'], e)))

							elif count == 0 and interval:
								if setThreadingTimer(actID, interval): # 타이머가 > 0 이고 카운터도 0 이면
									try:
										if basicAuth:
											response = requests.get(url, auth=(username, password), params = args['custom']['data'])
										else:
											response = requests.get(url, params = args['custom']['data'])
										# requests.get(url = args['server']['url'], params = args['custom']['data'])
										logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_get {}, auth:{}'.format(args['server']['url'],basicAuth)))
									except Exception as e:
										logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_get {} {}'.format(args['server']['url'], e)))

							elif count and interval == 0: # 타이머가 0 이고 카운터도 > 0 이면
								actCount[actID] += 1
								if actCount[actID] >= count:
									try:
										if basicAuth:
											response = requests.get(url, auth=(username, password), params = args['custom']['data'])
										else:
											response = requests.get(url, params = args['custom']['data'])
										# requests.get(url = args['server']['url'], params = args['custom']['data'])
										logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_get {}, auth:{}'.format(args['server']['url'],basicAuth)))
									except Exception as e:
										logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_get {} {}'.format(args['server']['url'], e)))

									actCount[actID] = 0

							else: # count == 0 and interval == 0 : # 타이머가 0 이고 카운터도 0 이면
								try:
									if basicAuth:
										response = requests.get(url, auth=(username, password), params = args['custom']['data'])
									else:
										response = requests.get(url, params = args['custom']['data'])
									# requests.get(url = args['server']['url'], params = args['custom']['data'])
									logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_get {}, auth:{}'.format(args['server']['url'],basicAuth)))
								except Exception as e:
									logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_get {} {}'.format(args['server']['url'], e)))

							# try:
							# 	requests.get(url = args['server']['url'], params = args['custom']['data'])
							# 	logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_get {}'.format(args['server']['url'])))
							# except Exception as e:
							# 	logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_get {} {}'.format(args['server']['url'], e)))

						elif args['custom']['method'] == 'http_post':
							'''
							try:
								# http authentication 
								# https://requests.readthedocs.io/en/latest/user/authentication/
								if args['server']['user'] and args['server']['password']:
									url = args['server']['url']
									username = args['server']['username']
									password = args['server']['password']
									# from requests.auth import HTTPBasicAuth
									# basic = HTTPBasicAuth(username, password)
									# response = requests.post(url, auth=basic, params = args['custom']['data'])
									response = requests.post(url, auth=(username, password), params = args['custom']['data'])
								else:
									response = requests.post(url = args['server']['url'], params = args['custom']['data'])
								logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_post {}, auth:{}'.format(args['server']['url'],basicAuth)))
							except Exception as e:
								logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_post {} {}'.format(args['server']['url'], e)))
							'''
							if 'username' in args['server'] and  'password' in args['server']:
								username = args['server']['username']
								password = args['server']['password']
								basicAuth = True
							else:
								basicAuth = False

							url = args['server']['url']

							if count and interval:
								# 타이머 시간이내 카운터 횟수 이상이면 알람발생
								# 타이머가 종료 되면 카운터 초기화
								if setThreadingTimer(actID, interval): # 타이머가 > 0 이고 카운터도 > 0 이면
									actCount[actID] = 1 # 초기화 : 최초 이벤트를 유효처리 한다.
								else:
									actCount[actID] += 1

								if actCount[actID] >= count:
									try:
										if basicAuth:
											requests.post(url, auth=(username, password), params = args['custom']['data'])
										else:
											requests.post(url, params = args['custom']['data'])
										# requests.post(url = args['server']['url'], data = args['custom']['data'])
										logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_post {}, auth:{}'.format(args['server']['url'],basicAuth)))
									except Exception as e:
										logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_post {} {}'.format(args['server']['url'], e)))

							elif count == 0 and interval:
								if setThreadingTimer(actID, interval): # 타이머가 > 0 이고 카운터도 0 이면
									try:
										if basicAuth:
											requests.post(url, auth=(username, password), params = args['custom']['data'])
										else:
											requests.post(url, params = args['custom']['data'])
										# requests.post(url = args['server']['url'], data = args['custom']['data'])
										logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_post {}, auth:{}'.format(args['server']['url'],basicAuth)))
									except Exception as e:
										logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_post {} {}'.format(args['server']['url'], e)))

							elif count and interval == 0: # 타이머가 0 이고 카운터도 > 0 이면
								actCount[actID] += 1
								if actCount[actID] >= count:
									try:
										if basicAuth:
											requests.post(url, auth=(username, password), params = args['custom']['data'])
										else:
											requests.post(url, params = args['custom']['data'])
										# requests.post(url = args['server']['url'], data = args['custom']['data'])
										logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_post {}, auth:{}'.format(args['server']['url'],basicAuth)))
									except Exception as e:
										logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_post {} {}'.format(args['server']['url'], e)))

									actCount[actID] = 0

							else: # count == 0 and interval == 0 : # 타이머가 0 이고 카운터도 0 이면
								try:
									if basicAuth:
										requests.post(url, auth=(username, password), params = args['custom']['data'])
									else:
										requests.post(url, params = args['custom']['data'])
									# requests.post(url = args['server']['url'], data = args['custom']['data'])
									logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_post {}, auth:{}'.format(args['server']['url'],basicAuth)))
								except Exception as e:
									logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_post {} {}'.format(args['server']['url'], e)))

							# try:
							# 	requests.post(url = args['server']['url'], data = args['custom']['data'])
							# 	logger.info('from:{} {}'.format(sender_API[0], 'Success custom->http_post {}, auth:{}'.format(args['server']['url'],basicAuth)))
							# except Exception as e:
							# 	logger.info('from:{} {}'.format(sender_API[0], 'Error custom->http_post {} {}'.format(args['server']['url'], e)))
						else:
							sock_send(sock,{'ip':sender_API[0], 'category':'custom', 'msg':'Unknown Command'})
					else:
						if args['debug']:
							sock_send(sock,{'ip':sender_API[0], 'category':'custom', 'msg':'Missing args'})
							logger.warning('from:{} {}'.format(sender_API[0], 'Missing custom args'))

					continue # <-- 현 Loop 종료

				if 'global_var' in args: # 크라이언트(itsAPI.html)에서 변경된 변수 실시간 적용
					cfgNew = args['global_var']
					for key in cfgNew:
						cfg[key] = cfgNew[key]
						# print key
					# print(json.dumps(cfgNew, indent=4, sort_keys=True))

					continue # <-- 현 Loop 종료

			break # <-- 중요함 : 크라이언트에서 세션 종료 유무와 무관하게 자체에서 센션종료함
			
		sock.close() # <------ 클라이언트 세션 종료
	s.close() # <------- 위 루프가 끝나지 않으므로 이 라인은 실행되지 않는다.

if __name__ == '__main__':
	share = readConfig('/home/pi/common/config.json')
	cfg = readConfig('/home/pi/API3/itsAPI.json')

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	# api3 = 'API3'
	# if not os.path.exists(share['path']['log']): # /var/www/html/its_web/data/log
	# 	os.makedirs(share['path']['log'])
	# 	os.chmod(share['path']['log'],0o777)
	# if not os.path.exists(share['path']['log']+'/'+api3): # /var/www/html/its_web/data/log/API3
	# 	os.makedirs(share['path']['log']+'/'+api3)
	# 	os.chmod(share['path']['log']+'/'+api3,0o777)
	logger = logging.getLogger('API3') # 로거 인스턴스를 만든다
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = cfg['loggerPath']
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(formatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(formatter)
	os.chmod(filename,0o777)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info('START')
	# logger.debug('===========================')
	# logger.info('TEST START')
	# logger.warning('파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.')
	# logger.debug('디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.')
	# logger.critical('치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!')
	# logger.debug('===========================')
	# logger.info('TEST END!')
	############ logging ################

	# host = cfg['tcpIpPort']['staticAddress']
	# port = cfg['portAPI']
	# port_N = cfg['tcpIpPort']['portIn']
	buffer = 1024  # Normally 1024, but we want fast response

	gpioTimer = {} # 센서별 타이머
	gpioCount = {} # 센서별 횟수제한
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
	for key, value in cfg['setBD']['setIO'].items():
		if value:
			GPIO.setup(cfg['setBD']['gpio'][key], GPIO.OUT) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
		else:
			GPIO.setup(cfg['setBD']['gpio'][key], GPIO.IN) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
		gpioTimer[key] = None
		gpioCount[key] = 0
	for key, value in cfg['setBD']['setPW'].items():
		if value:
			GPIO.setup(cfg['setBD']['gppw'][key], GPIO.OUT) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
		else:
			GPIO.setup(cfg['setBD']['gppw'][key], GPIO.IN) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
		gpioTimer[key] = None
		gpioCount[key] = 0
	# # 주의: cleanup을 하면 종료를 의미 하며 GPWIO Node가 죽는다.
	# GPIO.cleanup()

	# 
	actTimer = {} # 액션이벤트별 타이머
	actCount = {} # 액션이벤트별 횟수제한
	for key, value in cfg['alarmCmds'].items():
		actTimer[key] = None
		actCount[key] = 0
	for key, value in cfg['timerCmds'].items():
		actTimer[key] = None
		actCount[key] = 0
	for key, value in cfg['command'].items():
		actTimer[key] = None
		actCount[key] = 0
	for key, value in cfg['userCmds'].items():
		actTimer[key] = None
		actCount[key] = 0

	# print(actTimer)

	## audioFolderDownload
	audioFolderDownload = share['path']['its_web'] + share['path']['user']['audio'] + '/download'
	if not os.path.exists(audioFolderDownload): # audioFolderDownload 폴더 생성
		os.makedirs(audioFolderDownload)
	os.chmod(audioFolderDownload,0o777)
	## audioFolderBeep
	audioFolderBeep = share['path']['its_web'] + share['path']['user']['audio'] + '/beep'
	if not os.path.exists(audioFolderBeep): # audioFolderBeep 폴더 생성
		os.makedirs(audioFolderBeep)
	os.chmod(audioFolderBeep,0o777)

	## audioFolderAPI
	audioFolderAPI = share['path']['its_web'] + share['path']['user']['audio'] + '/api'
	if not os.path.exists(audioFolderAPI): # audioFolderAPI 폴더 생성
		os.makedirs(audioFolderAPI)
	os.chmod(audioFolderAPI,0o777)
	sourceList = os.listdir(audioFolderAPI)
	sourceList.sort()

	make_API_map()
	# print(run_demon_API())		
	# print("Log : {}".format(filename))
	# print("Audio : {}".format(audioFolderAPI))
	main()
