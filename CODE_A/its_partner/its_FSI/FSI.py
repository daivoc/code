#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import datetime
import subprocess 
import re
import struct
import socket
# import xml.etree.ElementTree as ET
import xmltodict, json
import threading
import requests

import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

import os
import logging
import logging.handlers
	
## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)

def kill_demon_FDX(): 
	cmd = "pkill -9 -ef FDX.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def sendPing(conn, deviceName):
	return conn.send('<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName>{0}</DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>'.format(deviceName)) # 센서의 접속 요청이 오면 핑

def sendNrecvPing(conn, deviceName):
	conn.send('<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName>{0}</DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>'.format(deviceName))
	buffer = 1024
	isPart = 0 # part Counter
	isFull = 0 # bucket Full
	bucket = b'' # bucket
	fLine = b'' # 이전 페킷의 시작 라인 저장
	lLine = b'' # 이전 페킷의 마지막 라인 저장
	while True:
		try:
			data = conn.recv(buffer)
		except:
			if cfg["user"]["debug"]: logger.info("<--- Error receive data, will retry --->")
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

		# 파트의 묶음이 완성됨
		if isFull:
			return bucket
	conn.close()

def parserXML(data): # 
	try:
		dict_type = xmltodict.parse(data)
		json_type = json.dumps(dict_type, indent=4, sort_keys=True)
		if cfg["user"]["debug"]: logger.info("<--- json data --|{0}|-->".format(json_type))
		return json.loads(json_type)
	except:
		response = {}
		response['error'] = data
		return response

def sendCommandZone(host,port,command):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
	try: 
		s.connect((host,port))
		s.send(command) 
		s.close() 
		return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		s.close()

def insert_fsi_log(tableName, w_zone = 0, w_eventID = 0, w_eventName = ""):
	# `w_zone` tinyint(4) NOT NULL DEFAULT '0',
	# `w_eventID` tinyint(4) NOT NULL DEFAULT '0',
	# `w_eventName` varchar(16) NULL DEFAULT '',
	query = "INSERT INTO "+tableName+" (w_zone, w_eventID, w_eventName) VALUES(%s, %s, %s)"
	args = (w_zone, w_eventID, w_eventName)
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query, args)
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

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
			kill_demon_FDX()
			exit("Binding Error : Over Count")
	s.listen(1)

	while True:
		###########################
		# 디바이스명 확인 후 저장
		###########################
		# print("Listening from {0}:{1} ...".format(cfg["device"]["addr"],cfg["device"]["port"]))
		# logger.info("Listening from {0}:{1} ...".format(cfg["device"]["addr"],cfg["device"]["port"]))
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
					kill_demon_FDX()
					exit("Check Sensor of {0}:{1} and Retry later.".format(cfg["device"]["addr"],cfg["device"]["port"]))
			if count:
				try:
					# sendPing(conn, '') # 1st Ping Request
					data = sendNrecvPing(conn, '') # 1st Ping Request
					if cfg["user"]["debug"]: logger.info("<--- 1st Ping data --|{0}|-->".format(data))
					cmdMsg = parserXML(data.split("\n",1)[1]) # Parser CommandMessage
					if cfg["user"]["debug"]: logger.info("<--- 1st cmdMsg --|{0}|-->".format(cmdMsg))
					deviceName = cmdMsg["CommandMessage"]["DeviceIdentification"]["DeviceName"] # Get deviceName
					if cfg["user"]["debug"]: logger.info("<--- get deviceName --|{0}|-->".format(deviceName))

					print("Device name is {0}".format(deviceName))
					logger.info("Device name is {0}".format(deviceName))

					# sendPing(conn, deviceName) # 2nd Ping Request with deviceName
					data = sendNrecvPing(conn, deviceName) # 2nd Ping Request with deviceName
					if cfg["user"]["debug"]: logger.info("<--- 2nd Ping data --|{0}|-->".format(data))
					cmdMsg = parserXML(data.split("\n",1)[1]) # Parser CommandMessage
					if cfg["user"]["debug"]: logger.info("<--- 2nd cmdMsg --|{0}|-->".format(cmdMsg))
					status = cmdMsg["CommandMessage"]["@Status"] # Get deviceName
					if cfg["user"]["debug"]: logger.info("<--- status --|{0}|-->".format(status))

					if status == 'OK':
						print("Handshake OK with {0}".format(deviceName))
						logger.info("Handshake OK with {0}".format(deviceName))
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

		# ## 최대 130초 내에 handshake를 해야만 접속이 유지 된다.
		# ## 120초 간격으로 디바이스에 접속유지 요청을 하는 기능
		# def handshake():
		# 	threading.Timer(120.0, handshake).start()
		# 	response = sendPing(conn, deviceName) # 핑 요청
		# 	if cfg["user"]["debug"]: logger.info("<--- handshake --|{0}|-->".format(response))
		# handshake()

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

		insert_fsi_log(cfg["mysql"]["logTable"], w_zone = 0, w_eventID = 0, w_eventName = "Start FSI")
		print("Listening event from {0}:{1} ...".format(cfg["device"]["addr"],cfg["device"]["port"]))
		logger.info("Listening event from {0}:{1} ...".format(cfg["device"]["addr"],cfg["device"]["port"]))
		while True:
			try:
				data = conn.recv(buffer)
			except:
				if cfg["user"]["debug"]: logger.info("<--- Error receive data, will retry --->")
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

			## 취합하는 모든 과정을 출력 한다.
			if cfg["user"]["debug"]: logger.info("<--- received raw data ({0}) --|{1}|-->".format(isPart,data))

			# 파트의 묶음이 완성됨
			if isFull:
				rootGrps = bucket.split("\n",1)[1] # 최초 엔터를 기준으로 공백인 첫째라인 제거
				rootGrps = bucket.split(rootGrps.splitlines()[0])[1:] # XML Head를 기준으로 배열화 
				for idx,group in enumerate(rootGrps): # 하나 또는 그 이상인 배열을 반복문에 적용
					## 취합된 XML 자료의 개별 자료 출력
					logger.info("<--- cooked data ({0}/{1})--->".format(idx+1,len(rootGrps)))
					if cfg["user"]["debug"]: logger.info("<--- cooked data ({0}/{1}) --|{2}|-->".format(idx+1,len(rootGrps),group))
					
					pData = parserXML(group) # XML -> JSON -> Dict 적용
					
					# 분석요청
					if "CommandMessage" in pData: # 접속 유무 확인 및 하트비트로 활용됨
						# >>>>> CommandMessage <<<<< {u'CommandMessage': {u'DeviceIdentification': {u'DeviceName': u'E110545'}, u'@MessageType': u'Response', u'Command': {u'SimpleCommand': u'Ping'}, u'@Status': u'OK'}}
						#########################
						## 120초 주기로 실행된다.
						## 하트비트로 사용 가능하다.
						#########################

						# command = json.dumps({"command": "ping"})
						# print sendCommandZone("localhost",cfg["local"]["zone"]["0"],command)
						curStatus = pData["CommandMessage"]["@Status"]
						if curStatus == "OK": # 정상적인 핑의 응답일때만 전체 전송 한다.
							command = json.dumps({"command": "CommandMessage", "status":curStatus}) 

							# 핑 정보는 모든 존에 보낸다.
							# # 개별 존 데몬 실행
							for (key, port) in cfg["local"]["zone"].items():
								sendCommandZone("localhost",port,command) # sendCommandZone(host,port,command)
								# print ("localhost",port,command)

							logger.info("\\u001b[33;1m >>>>> CommandMessage <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))
						else:
							logger.warning("\\u001b[33;1m >>>>> CommandMessage <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))

					elif "DeviceDetectionReport" in pData: 
						# >>>>> DeviceDetectionReport <<<<< {u'DeviceDetectionReport': {u'DeviceDetectionRecord': {u'Detection': {u'UpdateTime': {u'#text': u'2021-03-18T13:10:04.000', u'@Zone': u'GMT'}, u'DetectionEvent': u'Intrusion', u'ID': u'SZ001846'}, u'DeviceIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545.CHB', u'DeviceType': u'FD34x Channel'}}}}
						#########################
						## 이벤트에 따른 사용자 요청 실행
						#########################

						# curDeviceName = pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["DeviceIdentification"]["DeviceName"] # E110545.CHA / FD525R-109545.HZONE-1.ZONE-001
						# curDetectionEvent = pData["DeviceDetectionReport"]["DeviceDetectionRecord"]["Detection"]["DetectionEvent"] # "Intrusion" / "Fault" / "Temper" / "OK"
						# command = json.dumps({"command": "DeviceDetectionReport", "deviceName":curDeviceName, "detectionEvent":curDetectionEvent}) 

						# zoneID = cfg["device"]["zoneID"][curDeviceName.split('.')[-1]] # deviceName : E110545.CHA -> CHA or FD525R-109545.HZONE-1.ZONE-001 -> ZONE-001
						# if zoneID in cfg["local"]["zone"]:
						# 	sendCommandZone("localhost",cfg["local"]["zone"][zoneID],command) # sendCommandZone(host,port,command)
						# else:
						# 	logger.warning("\\u001b[33;1m >>>>> DeviceDetectionReport <<<<< {0}\\u001b[0m".format("No Matched Zone Information.").decode("unicode-escape"))

						# ## 이벤트 로그 등록
						# insert_fsi_log(cfg["mysql"]["logTable"], w_zone = int(zoneID), w_eventID = cfg["device"]["value"][curDetectionEvent], w_eventName = curDetectionEvent)

						# logger.info("\\u001b[33;1m >>>>> DeviceDetectionReport <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))
						try:
							# detectionEvents = []
							if type(pData["DeviceDetectionReport"]["DeviceDetectionRecord"]) is dict:  # True
								detectionEvents = [pData["DeviceDetectionReport"]["DeviceDetectionRecord"]]
							else:
								detectionEvents = pData["DeviceDetectionReport"]["DeviceDetectionRecord"]

							for dEvents in detectionEvents:
								curDeviceName = dEvents["DeviceIdentification"]["DeviceName"] # E110545.CHA / FD525R-109545.HZONE-1.ZONE-001
								curDetectionEvent = dEvents["Detection"]["DetectionEvent"] # "Intrusion" / "Fault" / "Temper" / "OK"
								command = json.dumps({"command": "DeviceDetectionReport", "deviceName":curDeviceName, "detectionEvent":curDetectionEvent}) 

								zoneID = cfg["device"]["zoneID"][curDeviceName.split('.')[-1]] # deviceName : E110545.CHA -> CHA or FD525R-109545.HZONE-1.ZONE-001 -> ZONE-001
								if zoneID in cfg["local"]["zone"]:
									sendCommandZone("localhost",cfg["local"]["zone"][zoneID],command) # sendCommandZone(host,port,command)
								else:
									logger.warning("\\u001b[33;1m >>>>> DeviceDetectionReport <<<<< {0}\\u001b[0m".format("No Matched Zone Information.").decode("unicode-escape"))

								## 이벤트 로그 등록
								insert_fsi_log(cfg["mysql"]["logTable"], w_zone = int(zoneID), w_eventID = cfg["device"]["value"][curDetectionEvent], w_eventName = curDetectionEvent)

								logger.info("\\u001b[33;1m >>>>> DeviceDetectionReport <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))
						except:
							logger.warning("\\u001b[33;1m >>>>> Try Error from DeviceDetectionReport <<<<< \\u001b[0m")

					elif "DeviceStatusReport" in pData:
						# 실시간 단선시 >>>>> DeviceStatusReport <<<<< {u'DeviceStatusReport': {u'DeviceIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545.CHB', u'DeviceType': u'FD34x Channel'}, u'Status': {u'CommunicationState': u'Fail', u'UpdateTime': {u'#text': u'2021-03-18T13:20:54.000', u'@Zone': u'GMT'}, u'DeviceState': u'Fault'}}}
						# 실시간 복구시 >>>>> DeviceStatusReport <<<<< {u'DeviceStatusReport': {u'Detection': {u'UpdateTime': {u'#text': u'2021-03-18T13:20:54.000', u'@Zone': u'GMT'}, u'Details': u'Internal line fault', u'DetectionEvent': u'Other'}, u'DeviceIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545.CHB', u'DeviceType': u'FD34x Channel'}, u'Status': {u'CommunicationState': u'OK', u'UpdateTime': {u'#text': u'2021-03-18T13:20:54.000', u'@Zone': u'GMT'}, u'DeviceState': u'Secure'}}}
						logger.info("\\u001b[33;1m >>>>> DeviceStatusReport <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))

					elif "DeviceConfiguration" in pData:
						# >>>>> DeviceConfiguration <<<<< {u'DeviceConfiguration': {u'ConfigurationOptionBlock': [{u'@Units': u'None', u'@Name': u'Wind Processing', u'ConfigurationOption': [{u'@Selected': u'true', u'@Option': u'Enabled'}, {u'@Selected': u'false', u'@Option': u'Disabled'}]}, {u'@Units': u'None', u'@Name': u'Climb Processing', u'ConfigurationOption': [{u'@Selected': u'true', u'@Option': u'Enabled'}, {u'@Selected': u'false', u'@Option': u'Disabled'}]}, {u'@Units': u'None', u'@Name': u'Cut Processing', u'ConfigurationOption': [{u'@Selected': u'true', u'@Option': u'Enabled'}, {u'@Selected': u'false', u'@Option': u'Disabled'}]}, {u'@Units': u'None', u'@Name': u'Enable Tamper Switch', u'ConfigurationOption': [{u'@Selected': u'false', u'@Option': u'Enabled'}, {u'@Selected': u'true', u'@Option': u'Disabled'}]}], u'@MessageType': u'Report', u'DeviceIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545.CHB', u'DeviceType': u'FD34x Channel'}, u'ConfigurationSetting': [{u'@MaximumValue': u'50', u'@MinimumValue': u'0', u'@CurrentValue': u'14', u'@Name': u'Climb Sensitivity', u'@Units': u'None'}, {u'@MaximumValue': u'600', u'@MinimumValue': u'10', u'@CurrentValue': u'200', u'@Name': u'Climb Low Freq Limit', u'@Units': u'Hz'}, {u'@MaximumValue': u'100', u'@MinimumValue': u'1', u'@CurrentValue': u'1', u'@Name': u'Climb Event Count', u'@Units': u'None'}, {u'@MaximumValue': u'50', u'@MinimumValue': u'0', u'@CurrentValue': u'14', u'@Name': u'Cut Sensitivity', u'@Units': u'None'}, {u'@MaximumValue': u'600', u'@MinimumValue': u'10', u'@CurrentValue': u'300', u'@Name': u'Cut Low Freq Limit', u'@Units': u'Hz'}, {u'@MaximumValue': u'100', u'@MinimumValue': u'1', u'@CurrentValue': u'1', u'@Name': u'Cut Event Count', u'@Units': u'None'}, {u'@MaximumValue': u'80', u'@MinimumValue': u'20', u'@CurrentValue': u'50', u'@Name': u'Wind Reject Factor', u'@Units': u'MilesPerHour'}, {u'@MaximumValue': u'10', u'@MinimumValue': u'1', u'@CurrentValue': u'1', u'@Name': u'Alarm Relay time', u'@Units': u'sec'}]}}
						logger.info("\\u001b[34;1m >>>>> DeviceConfiguration <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))

					elif "PlatformStatusReport" in pData: # Timeover 130sec
						# >>>>> PlatformStatusReport <<<<< {u'PlatformStatusReport': {u'DeviceStatusReport': [{u'DeviceIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545.CHA', u'DeviceType': u'FD34x Channel'}, u'Status': {u'CommunicationState': u'Fail', u'UpdateTime': {u'#text': u'2021-03-18T13:12:04.000', u'@Zone': u'GMT'}, u'DeviceState': u'Fail'}}, {u'DeviceIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545.CHB', u'DeviceType': u'FD34x Channel'}, u'Status': {u'CommunicationState': u'OK', u'UpdateTime': {u'#text': u'2021-03-18T13:12:04.000', u'@Zone': u'GMT'}, u'DeviceState': u'Secure'}}], u'PlatformIdentification': {u'DeviceCategory': u'Sensor', u'DeviceName': u'E110545', u'DeviceType': u'FD34x APU'}}}
						logger.info("\\u001b[35;1m >>>>> PlatformStatusReport <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))
						
						sendPing(conn, deviceName) # Nenewal Ping Request with deviceName
						if cfg["user"]["debug"]: logger.info("<--- sent ping --->")

					else:
						logger.info("\\u001b[36;1m >>>>> Unknown <<<<< {0}\\u001b[0m".format(pData).decode("unicode-escape"))

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
	# if not os.path.exists(cfg["pathLog"] + "/FSI"): # /var/www/html/its_web/data/log
	# 	os.makedirs(cfg["pathLog"] + "/FSI")
	# 	os.chmod(cfg["pathLog"] + "/FSI",0o777)
	logger = logging.getLogger('mylogger') # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	# filename = cfg["pathLog"] + "/FSI/0.log"
	filename = cfg["pathLog"] + "/" + cfg["device"]["serial"] + ".log"
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
