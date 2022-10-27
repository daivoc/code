#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import datetime
import re
import struct
import socket
import xml.etree.ElementTree as ET
import xmltodict, json
import threading
import requests

import os
import logging
import logging.handlers
	
## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def sendPing(conn, deviceName):
	return conn.send('<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName>{0}</DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>'.format(deviceName)) # 센서의 접속 요청이 오면 핑

def parserXML(data): # 
	try:
		dict_type = xmltodict.parse(data)
		json_type = json.dumps(dict_type, indent=4, sort_keys=True)
		if cfg["site"]["debug"]: logger.info("<--- json data --|{0}|-->".format(json_type))
		return json.loads(json_type)
	except:
		response = {}
		response['error'] = data
		return response

def postCommandMessage(addr, port, deviceName, status):
	# deviceName(APU) : FD525R-109545

	if deviceName and detectionEvent: # TCP 포트 전송
		response = apiCustom(addr, port,'{ "deviceName":deviceName, "status":status }')
	else:
		response = "Unknown Event"

	return deviceName, status, response

def postDeviceDetectionReport(addr, port, deviceName, detectionEvent):
	# deviceName(ZONE) : FD525R-109545.HZONE-1.ZONE-001
	# detectionEvent : Intrusion, Fault, Tamper

	# ## 웹 리퀴스트 전송
	# if deviceName and detectionEvent:
	# 	data = { "deviceName":deviceName, "detectionEvent":detectionEvent }
	# 	response = web_request(method_name='POST', url=cfg["site"]["server"]["1st"]["url"], dict_data=data)
	# else:
	# 	response = "Unknown Event"

	# TCP 포트 전송
	if deviceName and detectionEvent:
		response = apiCustom(addr, port,'{ "deviceName":deviceName, "detectionEvent":detectionEvent }')
	else:
		response = "Unknown Event"

	# if detectionEvent == "Intrusion":
	# 	response = apiJson(addr, port,'{ "gpio": { "status": "1", "id": "R09", "hold": "5", "msg": ""}, "debug":true }]')
	# elif detectionEvent == "Fault":
	# 	response = apiJson(addr, port,'[{ "gpio": { "status": "1", "id": "R10", "hold": "5", "msg": ""}, "debug":true }]')
	# elif detectionEvent == "Tamper":
	# 	response = apiJson(addr, port,'[{ "gpio": { "status": "1", "id": "R11", "hold": "5", "msg": ""}, "debug":true }]')
	# else:
	# 	response = "Unknown Event"

	if cfg["site"]["debug"]: logger.info("<--- itsAPI's response --|{0}|-->".format(response))
	return deviceName, detectionEvent, response

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

def web_request(method_name, url, dict_data, is_urlencoded=True):
	"""Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
	"""
	url  = 'http://192.168.0.80:9991' # 접속할 사이트주소 또는 IP주소를 입력한다 
	data = {'uid':'Happy','pid':'Birth','sid':'Day'}         # 요청할 데이터
	response = web_request(method_name='GET/POST', url=url, dict_data=data)
	"""

	# if method_name == 'GET': # GET방식인 경우
	# 	response = requests.get(url=url, params=dict_data)
	# elif method_name == 'POST': # POST방식인 경우
	# 	if is_urlencoded is True:
	# 		response = requests.post(url=url, data=dict_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
	# 	else:
	# 		response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})

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

# 에스원 고객 전용임
def postCommand_S1(url, deviceName, status):
	# deviceName(APU) : FD525R-109545
	if deviceName in cfg["site"]["convert"]["name"] and status in cfg["site"]["convert"]["value"]:
		typeIs = cfg["site"]["convert"]["value"][status]
		# descIs = cfg["site"]["convert"]["description"][status]
		timeIs = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
		idIs = cfg["site"]["convert"]["name"][deviceName] # 0 인경우 시스템을 뜻함
		# data = '<EventMessage><Type>{0}</Type><Desc>{1}</Desc><Time>{2}</Time><ID>{3}</ID></EventMessage>'.format(typeIs, descIs, timeIs, idIs)
		data = '<EventMessage><Type>{0}</Type><AlarmGroup>9</AlarmGroup><ID>{1}</ID><AlarmTime>{2}</AlarmTime></EventMessage>'.format(typeIs, idIs, timeIs)
		## 웹 리퀴스트 전송
		response = web_request(method_name='POST', url=url, dict_data=data)
	else:
		response = "Unmatched Event"

	return deviceName, status, response

# 에스원 고객 전용임 2021-03-04 15:50:31수정
def postDetectSite_S1(url, deviceName, detectionEvent):
	## http://115.139.183.226:8000/optex_web/bbs/board.php?bo_table=g100t100&wr_id=512
	# deviceName(ZONE) : FD525R-109545.HZONE-1.ZONE-001
	# detectionEvent : Intrusion, Fault, Tamper
	if deviceName in cfg["site"]["convert"]["name"] and detectionEvent in cfg["site"]["convert"]["value"]:
		typeIs = cfg["site"]["convert"]["value"][detectionEvent]
		# descIs = cfg["site"]["convert"]["description"][detectionEvent]
		timeIs = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
		idIs = cfg["site"]["convert"]["name"][deviceName]
		# data = '<EventMessage><Type>{0}</Type><Desc>{1}</Desc><Time>{2}</Time><ID>{3}</ID></EventMessage>'.format(typeIs, descIs, timeIs, idIs)
		data = '<EventMessage><Type>{0}</Type><AlarmGroup>9</AlarmGroup><ID>{1}</ID><AlarmTime>{2}</AlarmTime></EventMessage>'.format(typeIs, idIs, timeIs)
		## 웹 리퀴스트 전송
		response = web_request(method_name='POST', url=url, dict_data=data)
	else:
	 	response = "Unmatched Event"
		
	return deviceName, detectionEvent, response

def main ():

	###########################
	# Receiving Server Binding
	###########################
	for count in reversed(list(range(retry_cnt))):
		if count:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(10) ## 설정시 변화를 알수 없음, 1초로 하면 접속오류 발생
				s.bind((cfg["local"]["host"], cfg["local"]["port"])) # 'localhost'를 뜻함
				print("Local Binding OK {0}:{1}".format(cfg["local"]["host"], cfg["local"]["port"]))
				logger.info("Local Binding OK {0}:{1}".format(cfg["local"]["host"], cfg["local"]["port"]))
				break
			except:
				print("Local Binding Error, Retry After 5s({0}) ...".format(count))
				logger.info("Local Binding Error, Retry After 5s({0}) ...".format(count))
				time.sleep(5)
				continue
		else:
			logger.info("Binding Error : Over Count")
			exit("Binding Error : Over Count")
	s.listen(1)

	while True:
		###########################
		# 디바이스명 확인 후 저장
		###########################
		print("Listening from {0}:{1} ...".format(cfg["device"]["addr"],cfg["device"]["port"]))
		logger.info("Listening from {0}:{1} ...".format(cfg["device"]["addr"],cfg["device"]["port"]))
		for count in reversed(list(range(retry_cnt))):
			try:
				conn, addr = s.accept()
				print("Connection address:{0}".format(addr))
				logger.info("Connection address:{0}".format(addr))
			except:
				print("Connection Error, Retry After 5s({0}) ...".format(count))
				logger.info("Connection Error, Retry After 5s({0}) ...".format(count))
				time.sleep(5)
				if count:
					continue
				else:
					logger.info("Check Sensor of {0}:{1} and Retry later.".format(cfg["device"]["addr"],cfg["device"]["port"]))
					exit("Check Sensor of {0}:{1} and Retry later.".format(cfg["device"]["addr"],cfg["device"]["port"]))
			if count:
				try:
					sendPing(conn, '') # 1st Ping Request
					data = conn.recv(1024) # Receive CommandMessage
					if cfg["site"]["debug"]: logger.info("<--- 1st Ping data --|{0}|-->".format(data))
					cmdMsg = parserXML(data.split("\n",1)[1]) # Parser CommandMessage
					if cfg["site"]["debug"]: logger.info("<--- 1st cmdMsg --|{0}|-->".format(cmdMsg))
					deviceName = cmdMsg["CommandMessage"]["DeviceIdentification"]["DeviceName"] # Get deviceName
					if cfg["site"]["debug"]: logger.info("<--- get deviceName --|{0}|-->".format(deviceName))

					print("Device name is {0}".format(deviceName))
					logger.info("Device name is {0}".format(deviceName))

					sendPing(conn, deviceName) # 2nd Ping Request with deviceName
					data = conn.recv(1024) # Receive CommandMessage
					if cfg["site"]["debug"]: logger.info("<--- 2nd Ping data --|{0}|-->".format(data))
					cmdMsg = parserXML(data.split("\n",1)[1]) # Parser CommandMessage
					if cfg["site"]["debug"]: logger.info("<--- 2nd cmdMsg --|{0}|-->".format(cmdMsg))
					status = cmdMsg["CommandMessage"]["@Status"] # Get deviceName
					if cfg["site"]["debug"]: logger.info("<--- status --|{0}|-->".format(status))

					if status == 'OK':
						print("Handshake with {0}".format(deviceName))
						logger.info("Handshake with {0}".format(deviceName))
						break
					else:
						print("Handshake Error, Retry After 5s({0}) ...".format(count))
						logger.info("Handshake Error, Retry After 5s({0}) ...".format(count))
						time.sleep(5)
						conn.close()
						continue
				except:
					print("Parser Error, Retry After 5s({0}) ...".format(count))
					logger.info("Parser Error, Retry After 5s({0}) ...".format(count))
					time.sleep(5)
					conn.close()
					continue
			else:
				conn.close()
				s.close()
				print("Handshake Error : Over Count")
				logger.info("Handshake Error : Over Count")
				main() # 정상 적인 네트워크 확인(바인드) 후 오류발생시 처음부터 재시작:

		## 최대 130초 내에 handshake를 해야만 접속이 유지 된다.
		## 120초 간격으로 디바이스에 접속유지 요청을 하는 기능
		def handshake():
			threading.Timer(120.0, handshake).start()
			response = sendPing(conn, deviceName) # 핑 요청
			if cfg["site"]["debug"]: logger.info("<--- handshake --|{0}|-->".format(response))
		handshake()

		# 특징
		# 페킷이 크기 구분 없이 연속해서 들어온다
		# XML의 시작 패킷의 첫번째 라인은 엔터키로 시작된다. (최초저장)
		# 중간 라인은 네이스팅 룰에 의해 시작을 스페이스로 채운다. (첨부저장)
		# 마지막 라인은 네이스팅 룰에 의해 시작이 </ 로 시작하고 >로 끝난다. (마지막 저장)
		# 마지막 저장이 실행되면 이어서 파싱작업을 한다.
		buffer = 4096
		isPart = 0 # part Counter
		isFull = 0 # bucket Full
		bucket = b'' # bucket
		fLine = b'' # 이전 페킷의 시작 라인 저장
		lLine = b'' # 이전 페킷의 마지막 라인 저장

		url = cfg["site"]["server"]["1st"]["url"]
		addr = cfg["site"]["server"]["1st"]["addr"]
		port = cfg["site"]["server"]["1st"]["port"]
		while True:

			try:
				data = conn.recv(buffer)
			except:
				if cfg["site"]["debug"]: logger.info("<--- Error receive data, will retry --->")
				break
			
			if not data: break # 정상인경우 발셍 하지 않는 오류를 뜻한다. # Re-Connection address: ('192.168.168.30', 10001)
			
			sLine = data.splitlines()[0] # 받은 파트의 첫라인
			eLine = data.splitlines()[-1] # 받은 파트의 마지막 라인
			# 시작과 끝이 완전한 파트
			if re.match(r'^\n<', sLine) and re.match(r'^<\/.*>', eLine): # 엔터키이후 <가 나오면 시작점임
				bucket = data # 시작 점, 버텟에 채운다.
				isFull = 1
				isPart = 1
			# 시작점이 있으나 완전치 않은 파트
			elif re.match(r'^\n<', sLine): # 엔터키이후 <가 나오면 시작점임
				bucket = data # 시작 점, 버텟에 채운다.
				isFull = 0
				isPart = 1
				fLine = sLine
			# 마지막 점이 있거나 이전의 마지막과 결합후 완성 된 경우
			elif re.match(r'^<\/.*>', eLine) or re.match(r'^<\/.*>', lLine+eLine):
				bucket += data # 마지막 점, 버텟에 추가한다.
				isFull = 1
				isPart += 1
				# 마지막점 인지를 확인후 추가 기능 실행
				# 마지막 라인이 '</단어>' 로 끝나거나
				# '어>' 로 끝날시 이전 마지막 단어 '<단' 랑 결합후 조건 '</단어>'이 완성 되면
			# 시작도 마지막도 아닌 경우
			else:
				bucket += data # 중간 점, 버텟에 추가한다.
				isFull = 0
				isPart += 1
				lLine = eLine

			if cfg["site"]["debug"]: logger.info("<--- received raw data ({0}) --|{1}|-->".format(isPart,data))

			# 파트의 묶음이 완성됨
			if isFull:
				rootGrps = bucket.split("\n",1)[1] # 최초 엔터를 기준으로 공백인 첫째라인 제거
				rootGrps = bucket.split(rootGrps.splitlines()[0])[1:] # XML Head를 기준으로 배열화 
				for idx,group in enumerate(rootGrps): # 하나 또는 그 이상인 배열을 반복문에 적용
					if cfg["site"]["debug"]: logger.info("<--- cooked data ({0}/{1}) --|{2}|-->".format(idx+1,len(rootGrps),group))
					
					pData = parserXML(group) # XML -> JSON -> Dict 적용
					
					# 분석요청
					if "CommandMessage" in pData: # 접속 유무 확인 및 하트비트로 활용됨
						# response = postCommandMessage(addr, port, pData["CommandMessage"]["DeviceIdentification"]["DeviceName"], pData["CommandMessage"]["@Status"])

						# 에스원 고객 전용임
						try:
							response = postCommand_S1(url, pData["CommandMessage"]["DeviceIdentification"]["DeviceName"], pData["CommandMessage"]["@Status"])
						except:
							pass
						### logger.info("\\u001b[31;1m >>>>> CommandMessage <<<<< \\u001b[0m {0}".format(response).decode("unicode-escape"))

					elif "DeviceDetectionReport" in pData: #
						# response = postDeviceDetectionReport(addr, port, pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["DeviceIdentification"]["DeviceName"], pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["Detection"]["DetectionEvent"])

						# 에스원 고객 전용임
						try:
							response = postDetectSite_S1(url, pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["DeviceIdentification"]["DeviceName"],pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["Detection"]["DetectionEvent"])
						except:
							pass
						### if cfg["site"]["debug"]: logger.info("<--- HTTP Reauest --|{0}|-->".format(response))

						### logger.info("\\u001b[32;1m >>>>> DeviceDetectionReport <<<<< {0}".format(response).decode("unicode-escape"))
						### if cfg["site"]["debug"]: logger.info('<--- sent alarm --|{0}|-->'.format(pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["Detection"]["ID"]))

					elif "DeviceStatusReport" in pData:
						pass
						### logger.info ("\u001b[33;1m >>>>> DeviceStatusReport <<<<< {0}".format(pData).decode("unicode-escape"))

					elif "DeviceConfiguration" in pData:
						pass
						 ###logger.info ("\u001b[34;1m >>>>> DeviceConfiguration <<<<< {0}".format(pData).decode("unicode-escape"))

					elif "PlatformStatusReport" in pData: # Timeover 130sec
						### logger.info ("\u001b[35;1m >>>>> PlatformStatusReport <<<<< {0}".format(pData).decode("unicode-escape"))
						if pData["PlatformStatusReport"]["PlatformStatusReport"]["DeviceStatusReport"]["Status"]["DeviceState"] == "Secure":
							sendPing(conn, deviceName) # Nenewal Ping Request with deviceName
							### if cfg["site"]["debug"]: logger.info("<--- sent ping --->")

					else:
						pass
						### logger.info("\\u001b[36;1m >>>>> Unknown <<<<< {0}".format(pData).decode("unicode-escape"))

					### logger.info("\\u001b[0m".decode("unicode-escape")) #### COLOR Off ###

				bucket = b"" # 종료 점, 버텟을 비운다.
				isFull = 0
				isPart = 0
		conn.close()
	s.close()

if __name__ == "__main__":
	cfg = readConfig("/home/pi/FSI/FSI.json")
	retry_cnt = 16

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	if not os.path.exists(cfg["pathLog"]): # /var/www/html/its_web/data/log
		os.makedirs(cfg["pathLog"])
		os.chmod(cfg["pathLog"],0o777)
	logger = logging.getLogger('mylogger') # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = cfg["pathLog"] + "/FSI.log"
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

	main()

	##  Raw Data Receiver - Line Command
	# echo '<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName>FD525R-109545</DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>' | nc 192.168.168.30 10001 | tee -a /tmp/10001.log

	# echo '<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName>E105894</DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>' | nc 192.168.168.30 10001 | tee -a /tmp/10001.log
