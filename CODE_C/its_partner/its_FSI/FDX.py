#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import socket
import json
import requests

import os
import logging
import logging.handlers

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)

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

##########################################
## 활성화된 모니터링서버(IMS)에 데이터 전송
def insertSocketIMS(ip,port,data): 
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

def replaceRule(zoneID, zoneName, eventKey, data):
	## Key : __zone__, __value__, __type__, __name__, __serial__, __ip__, __time__
	__zone__ = cfg["device"]["zoneName"][zoneName] # __zone__ 이벤트 형태 : "Fault", "Intrusion", "OK", "Other", "Tamper"
	__value__ = cfg["device"]["value"][eventKey] # __value__ 이벤트 값(정수) : "9", "1", "2", "0", "8"
	__type__ = cfg["device"]["type"][eventKey] # __type__ 이벤트 형태 : "Fault", "Intrusion", "OK", "Other", "Tamper"
	__name__ = cfg["action"][zoneID]["info"]["subject"] # __name__ 존 사용자명
	__serial__ = cfg["action"][zoneID]["info"]["serial"] # __serial__ 존 시리얼

	dataRule = data
	dataRule = dataRule.replace('__zone__', __zone__)
	dataRule = dataRule.replace('__value__', __value__)
	dataRule = dataRule.replace('__type__', __type__)
	dataRule = dataRule.replace('__name__', __name__)
	dataRule = dataRule.replace('__serial__', __serial__)

	print("{0} {1}, {2}, {3}, {4}".format(__zone__, __value__, __type__, __name__, __serial__))
	print(dataRule)
	
	return data

def doAction(zoneID, dataJson):
	## dataJson = {"command": "DeviceDetectionReport", "deviceName":curDeviceName, "detectionEvent":curDetectionEvent}
	#########################################################
	## For IMS
	status = 0 
	if dataJson["command"] == "CommandMessage":
		status = 2 # Heartbeat
	elif dataJson["command"] == "DeviceDetectionReport":
		if dataJson["detectionEvent"] == "Intrusion":
			status = 1
		elif dataJson["detectionEvent"] == "Tamper":
			status = 8
		elif dataJson["detectionEvent"] == "Fault":
			status = 9

		zoneName = dataJson["deviceName"].split('.')[-1] ## "ZONE-001", "CHA" ...
			
	logger.info("<--- Status (Cmd:{0}, status={1}) --->".format(dataJson["command"], cfg["status"][str(status)]))


	#########################################################
	## For ims
	beep = 1
	if status == 2: beep = 0 
	msg = cfg["status"][str(status)]
	shot = ""
	if cfg["action"][zoneID]["flag"]["ims"]["P"]:
		imsValue=("id={0},name={1},beep={2},status={3},shot={4},msg={5}".format(cfg["action"][zoneID]["info"]["serial"],cfg["action"][zoneID]["info"]["subject"].encode("utf-8"),beep,status,shot,msg))
		result = insertSocketIMS(cfg["action"][zoneID]["ims"]["P"]["addr"],cfg["action"][zoneID]["ims"]["P"]["port"],imsValue)
		if cfg["user"]["debug"]: 
			logger.info("<--- Info (ims:{0}, {1}, {2}, {3}) --->".format(result, cfg["action"][zoneID]["ims"]["P"]["addr"],cfg["action"][zoneID]["ims"]["P"]["port"],imsValue))

	if cfg["action"][zoneID]["flag"]["ims"]["S"]:
		imsValue=("id={0},name={1},beep={2},status={3},shot={4},msg={5}".format(cfg["action"][zoneID]["info"]["serial"],cfg["action"][zoneID]["info"]["subject"].encode("utf-8"),beep,status,shot,msg))
		result = insertSocketIMS(cfg["action"][zoneID]["ims"]["S"]["addr"],cfg["action"][zoneID]["ims"]["S"]["port"],imsValue)
		if cfg["user"]["debug"]: 
			logger.info("<--- Info (ims:{0}, {1}, {2}, {3}) --->".format(result, cfg["action"][zoneID]["ims"]["S"]["addr"],cfg["action"][zoneID]["ims"]["S"]["port"],imsValue))

	#########################################################
	## 하트비트(CommandMessage)인경우 다음기능은 무시(Return) 한다.
	if dataJson["command"] == "CommandMessage": 
		# print("Heartbeat Zone ID:{}".format(zoneID))
		return

	#########################################################
	## For audioOut
	if cfg["action"][zoneID]["flag"]["audioOut"] and dataJson["command"] == "DeviceDetectionReport":
		pass
		# print("audioOut")

	#########################################################
	## For httpRequest
	if cfg["action"][zoneID]["flag"]["httpRequest"]["P"] and dataJson["command"] == "DeviceDetectionReport":
		# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], cfg["action"][zoneID]["httpRequest"]["P"]["data"])
		dataIs = cfg["action"][zoneID]["httpRequest"]["P"]["data"]
		result = httpRequest(cfg["action"][zoneID]["httpRequest"]["P"]["enc"], cfg["action"][zoneID]["httpRequest"]["P"]["addr"], dataIs)
		if cfg["user"]["debug"]: 
			logger.info("<--- Info (httpRequest_P:{0}, {1}, {2}, {3}) --->".format(result, cfg["action"][zoneID]["httpRequest"]["P"]["enc"], cfg["action"][zoneID]["httpRequest"]["P"]["addr"], dataIs.encode("utf-8")))

	if cfg["action"][zoneID]["flag"]["httpRequest"]["S"] and dataJson["command"] == "DeviceDetectionReport":
		# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], cfg["action"][zoneID]["httpRequest"]["S"]["data"])
		dataIs = cfg["action"][zoneID]["httpRequest"]["S"]["data"]
		result = httpRequest(cfg["action"][zoneID]["httpRequest"]["S"]["enc"], cfg["action"][zoneID]["httpRequest"]["S"]["addr"], dataIs)
		if cfg["user"]["debug"]: 
			logger.info("<--- Info (httpRequest_S:{0}, {1}, {2}, {3}) --->".format(result, cfg["action"][zoneID]["httpRequest"]["S"]["enc"], cfg["action"][zoneID]["httpRequest"]["S"]["addr"], dataIs.encode("utf-8")))

	#########################################################
	## For itsACU
	if cfg["action"][zoneID]["flag"]["itsACU"] and dataJson["command"] == "DeviceDetectionReport":
		pass
		# print("itsACU")

	#########################################################
	## For relayOut
	if cfg["action"][zoneID]["flag"]["relayOut"] and dataJson["command"] == "DeviceDetectionReport":
		pass
		# print("relayOut")

	#########################################################
	## For snapshot
	if cfg["action"][zoneID]["flag"]["snapshot"] and dataJson["command"] == "DeviceDetectionReport":
		pass
		# print("snapshot")

	#########################################################
	## For socketIO
	if cfg["action"][zoneID]["flag"]["socketIO"]["P"] and dataJson["command"] == "DeviceDetectionReport":
		# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], cfg["action"][zoneID]["socketIO"]["P"]["value"])
		dataIs = cfg["action"][zoneID]["socketIO"]["P"]["value"]
		result = apiCustom(cfg["action"][zoneID]["socketIO"]["P"]["addr"], cfg["action"][zoneID]["socketIO"]["P"]["port"], dataIs)
		if cfg["user"]["debug"]: 
			logger.info("<--- Info (socketIO_P:{0}, {1}, {2}, {3}) --->".format(result, cfg["action"][zoneID]["socketIO"]["P"]["addr"], cfg["action"][zoneID]["socketIO"]["P"]["port"], dataIs.encode("utf-8")))
	if cfg["action"][zoneID]["flag"]["socketIO"]["S"] and dataJson["command"] == "DeviceDetectionReport":
		# dataIs = replaceRule(zoneID, zoneName, dataJson["detectionEvent"], cfg["action"][zoneID]["socketIO"]["S"]["value"])
		dataIs = cfg["action"][zoneID]["socketIO"]["S"]["value"]
		result = apiCustom(cfg["action"][zoneID]["socketIO"]["S"]["addr"], cfg["action"][zoneID]["socketIO"]["S"]["port"], dataIs)
		if cfg["user"]["debug"]: 
			logger.info("<--- Info (socketIO_S:{0}, {1}, {2}, {3}) --->".format(result, cfg["action"][zoneID]["socketIO"]["S"]["addr"], cfg["action"][zoneID]["socketIO"]["S"]["port"], dataIs.encode("utf-8")))

	#########################################################
	## For streaming
	if cfg["action"][zoneID]["flag"]["streaming"] and dataJson["command"] == "DeviceDetectionReport":
		pass
		# print("streaming")

def main():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
		s.bind((host, port)) # <------- 소켓을 주소로 바인딩
		s.listen(1) # <------ listening 시작. 최대 클라이언트 연결 수 5개
		print('Daemon of API Parser {0}:{1}'.format(host,port))
	except:
		exit('Address already in use {0}:{1}'.format(host,port))

	while True:
		sock, senderIP = s.accept()
		# print('From:{}'.format(port))
		while True: # <-------- 클라이언트 연결이 오면 이 dialog 루프로 들어가서 데이터가 수신을 기다림
			# command = json.dumps({"command": "CommandMessage", "status":"OK"}) 
			# command = json.dumps({"command": "DeviceDetectionReport", "deviceName":curDeviceName, "detectionEvent":curDetectionEvent}) 

			data = sock.recv(buffer)
			if not data: break

			try:
				dataJson = json.loads(data)
			except:
				# sock.send(json.dumps({"ip":senderIP[0], "command":"unknown", "msg":"JSON format error"},sort_keys=True)) 
				logger.critical("<--- Error (JSON format error - {}) --->".format(data))
				print("msg:JSON format error - {}".format(data))
				break

			doAction(zoneID, dataJson)

if __name__ == "__main__":
	cfg = readConfig("/home/pi/FSI/FSI.json")

	if not len(sys.argv) == 3: sys.exit('need argv') ##### exit #####
	zoneID = sys.argv[1]

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	if not os.path.exists(cfg["pathLog"]): # /var/www/html/its_web/data/log
		os.makedirs(cfg["pathLog"])
		os.chmod(cfg["pathLog"],0o777)
	# if not os.path.exists(cfg["pathLog"] + "/FSI"): # /var/www/html/its_web/data/log
	# 	os.makedirs(cfg["pathLog"] + "/FSI")
	# 	os.chmod(cfg["pathLog"] + "/FSI",0o777)
	logger = logging.getLogger('mylogger') # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	# filename = cfg["pathLog"] + "/FSI/" + zoneID + ".log"
	filename = cfg["pathLog"] + "/" + cfg["action"][zoneID]["info"]["serial"] + ".log"
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

	host = 'localhost'
	port = int(sys.argv[2])
	buffer = 4096  # Normally 1024, but we want fast response

	main()
