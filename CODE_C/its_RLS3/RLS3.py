#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
# Request Ex. (JavaScript)
# https://www.js-tutorials.com/nodejs-tutorial/simple-websocket-example-with-nodejs/
# ws = new WebSocket("ws://192.168.168.30/detection");
# ws.send(JSON.stringify({"ctrl":"start","maxObject":50,"withCandidate":false}));

rtsp://root:RLS-3060V@192.168.168.30/stream/0
'''
## 2022-10-06 13:05:24
## python3.7 -m pip install flask
## python3.7 -m pip install flask_socketio
## python3.7 -m pip install websockets
## python3 -m pip install --upgrade onvif_zeep
## python3.7 -m pip install gevent-websocket
## 여기까지 검증

import random ## temp
import os
import time
import ast
import datetime
import json
import socket 
import threading 
import subprocess
import requests
from requests.auth import HTTPDigestAuth
import pymysql
import asyncio
import websockets
import logging
import logging.handlers

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)

def run_demon(): 
	cmd = "node ./realtime_RLS.js 2>&1 &"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# cmd = "python3 ./setup.pyc 2>&1 & "
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	# out == '' 이면 작업 성공, out != ''이면 실패
	# 복합명령인 경우 확인이 불가능 하므로 err는 무시하고 out만 확인 한다.
	return out

def insert_event_RLS_V(tableName, kind="", initialPosX=0, initialPosY=0, currentPosX=0, currentPosY=0, distance=0, step=0, size=0, zone="", level=0, count=0): 
	query = "INSERT INTO `"+tableName+"` (`kind`, `initialPosX`, `initialPosY`, `currentPosX`, `currentPosY`, `distance`, `step`, `size`, `zone`, `level`, `count`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	args = (kind, initialPosX, initialPosY, currentPosX, currentPosY, distance, step, size, zone, level, count)
	try:
		conn = pymysql.connect(host=config["mysql"]["host"], user=config["mysql"]["user"], passwd=config["mysql"]["pass"], db=config["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query, args)
		conn.commit()
		return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
 	# except pymysql.Warning as warning:
	else:
		pass
	finally:
		cursor.close()
		conn.close()


def actNop(id, resetDue): ## 타이머가 끝나는 순간 실행되며 ID와 관련된 요소를 삭제한다.
	# 이벤트 ID 단위의 다중 타이머 설정 
	# 타이머 종료시 종료를 확인 하기 위해 actTimer[id]를 None으로 설정
	# config["actTimer"] = {}
	# config["actCount"] = {}
	print("\tReset {} {}".format(id, time.time() - config["actCycle"][id] - resetDue))
	try:
		del config["actTimer"][id]
		del config["actCount"][id]
		del config["actCycle"][id]
	except:
		pass

	if config["recordOn"] and not len(config["actTimer"]): # True and 0 : 이벤트 발생후 평상 상태로 복귀 - End
		config["recordOn"] = False
		print("<<<<<<<<<<<<<<<<<<<<<<")
	return
		

def setThreadingTimer(id, resetDue):
	## 만약 이벤트 아이디가 config["actTimer"]에 존재하면 실행중을 뜻하며
	## 시간을 설정값으로 재 연장하고 실행카운트를 증가시킨다.
	## 그와 반대인 경우 카운트를 초기화 하고 타이머를 실행 시킨다.
	## 반환값은 현재의 카운터 값이다.
	if id in config["actTimer"]: # 시간 연장
		config["actCount"][id] += 1
		config["actTimer"][id].cancel()
		config["actTimer"][id] = threading.Timer(resetDue, actNop, [id, resetDue])
		config["actTimer"][id].start()
	else: # 시작
		config["actTimer"][id] = threading.Timer(resetDue, actNop, [id, resetDue])
		config["actTimer"][id].start()
		config["actCount"][id] = 1
		config["actCycle"][id] = time.time()
	return config["actCount"][id] 

def realtime_html(ip,port,data):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	reponse = 0
	# print(json.dumps(data).encode('utf-8'))
	try: 
		s.connect((ip,port))
		s.send(json.dumps(data).encode('utf-8'))
	except socket.error:
		reponse = 1
	except socket.timeout:
		reponse = 2
	finally:
		s.close() 

	return reponse

def realtime_IMS(data):
	##########################################
	## 활성화된 모니터링서버(IMS)에 데이터 전송
	## "id={0},name={1},beep={2},status={3},shot={4},msg={5}"
	## - status == 1 : 이벤트 발생 - [A] color: 'red'
	## - status == 2 : 하트비트 - [H] color: 'green' 
	##	addr = config["server"]["ims1st"]["addr"]
	##	port = config["server"]["ims1st"]["port"]
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	reponse = [0,0]
	if config["server"]["ims1st"]["addr"]:
		try:
			sock.connect((config["server"]["ims1st"]["addr"], config["server"]["ims1st"]["port"])) # sock.connect((addr,port))
			sock.sendall(data.encode('utf-8'))
		except socket.error:
			reponse[0] = 1
		except socket.timeout:
			reponse[0] = 2
		finally:
			sock.close()
	if config["server"]["ims2nd"]["addr"]:
		try:
			sock.connect((config["server"]["ims2nd"]["addr"], config["server"]["ims2nd"]["port"])) # sock.connect((addr,port))
			sock.sendall(data.encode('utf-8'))
		except socket.error:
			reponse[1] = 1
		except socket.timeout:
			reponse[1] = 2
		finally:
			sock.close()
	return reponse

###################################
## apiCustom
###################################
def trigger_API3(addr, port, data):
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
		dataIs = arrJson[i] # .encode('utf-8')

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1) # 타임아웃 값, 1초까지만 기다린다.
		try: 
			sock.connect((addr, port))
			result = sock.sendall(json.dumps(dataIs).encode('utf-8'))
			if not result:
				logger.info("Success {} {} {}".format(addr, port, dataIs)) 
		except socket.error:
			logger.warning("Socket Error {0}".format(addr)) 
		except socket.timeout:
			logger.warning("Timeout Error {0}".format(addr)) 
		finally:
			sock.close() 



def requestApi(address, command, id, password, method):
	try:
		if method == "get":
			# response = requests.get(command.format(address), auth=HTTPDigestAuth(id, password))
			response = requests.get("http://{}{}".format(address,command), auth=HTTPDigestAuth(id, password))
		elif method == "post":
			# response = requests.post(command.format(address), auth=HTTPDigestAuth(id, password))
			response = requests.post("http://{}{}".format(address,command), auth=HTTPDigestAuth(id, password))
		else:
			return 2, "Unknow Methode"

		if response.status_code == 200:
			return 0, response.json()
		else:
			return 1, response.status_code
	except:
		return 3, "Unknow Error"

async def webSocketApi(command, data):
	try:
		async with websockets.connect("ws://{}{}".format(config["sensor"]["addr"],command)) as ws:
			await ws.send(json.dumps(data))
			try:
				response = await ws.recv()
				return 0, json.loads(response)
			except:
				return 1, "Except: recv"
	except:
		return 2, "Except: websockets.connect"


#####################################
## IMS 하트비트, 통신오류 전송
#####################################
def heartBeat(): # 
	status, desc = requestApi(config["sensor"]["addr"], config["sensor"]["cmd"]["gInfoStatus"], config["sensor"]["user"], config["sensor"]["pass"], "get")
	id = "{}_{}_{}".format(config["sensor"]["prefix"], config["server"]["localhost"]["addr"].replace(".", "_" ), config["sensor"]["heartBeatKey"])
	if status: # IMS 오류 전송
		imsValue=(f"id={id},name={'gInfoStatus'},beep={1},status={9},shot={''},msg={''}")
		# print (f"Error Getting internal status - {status}")
	else: # IMS 하트비트 전송
		imsValue=(f"id={id},name={'heartbeat'},beep={0},status={2},shot={''},msg={'heartbeat'}")
		# print (f"Pass Getting internal status - {desc}")

	# ## 사용자 서버 데이터 전송 - ITS API3
	# if config["server"]["user2nd"]["addr"] and config["server"]["user2nd"]["port"] == config["port"]["forAPI3"] and config["server"]["user2nd"]["method"] =="api3" and config["server"]["user2nd"]["command"]:
	# 	print(realtime_html(config["server"]["user2nd"]["addr"],config["server"]["user2nd"]["port"],ast.literal_eval(config["server"]["user2nd"]["command"])))

	# print(imsValue)
	realtime_IMS(imsValue)
	# threading.Timer(6.0, heartBeat).start() # called every minute
	threading.Timer(config["sensor"]["heartBeatDue"], heartBeat).start() # called every minute

def main():
	## 마스킹 영역
	# print(config["filter"]["maskCoord"])
	stampsWas = time.time()
	statusWas = None
	desc = ["normal state ...", "err communication ...", "err connection ..."]
	data = {"ctrl":"start","maxObject":50,"withCandidate":False}

	## 영역제한(areaFilter) 사전정의
	## 영역제한은 거부(denyGroup)그룹이 우선 적용된다.
	if len(config["filter"]["maskCoord"]["denyGroup"]):
		areaFilter = "denyGroup"
	elif len(config["filter"]["maskCoord"]["allowGroup"]):
		areaFilter = "allowGroup"
	else:
		areaFilter = "ignoreGroup"
		
	# ## 크기제한(sizeFilter) 사전정의
	# ## 최소크기 또는 최대크기 조건 제한
	# if config["filter"]["size"]["min"] and config["filter"]["size"]["max"]:
	# 	sizeFilter = "both"
	# elif config["filter"]["size"]["min"]:
	# 	sizeFilter = "min"
	# elif config["filter"]["size"]["max"]:
	# 	sizeFilter = "max"
	# else:
	# 	sizeFilter = "none"

	levelSize = {} # {'0': 'max', '1': 'max', '2': 'max', '3': 'max', '4': 'both'}
	for k, v in config["level"].items():	
		if v["size"]["min"] and v["size"]["max"]:
			levelSize[k] = "both"
		elif v["size"]["min"]:
			levelSize[k] = "min"
		elif v["size"]["max"]:
			levelSize[k] = "max"
		else:
			levelSize[k] = "none"

	heartBeat() # Heartbeat 발생

	while True:
		statusIs, events = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectObj"], data))
		## 통신 오류(센서상태확인)를 검사를 위해 현상태의 지속시간을 측정 한다.
		## STATUS: 0 - 정상상태, 1 - 통신오류, 2 - 접속오류 

		if statusWas == statusIs: # 직전과 같은 상태
			pass
		else:
			stampsIs = time.time()
			timeGap = stampsIs - stampsWas
			stampsWas = stampsIs
			statusWas = statusIs
			logger.debug("{}s -> [{}] {}".format(int(timeGap), datetime.datetime.now(), desc[statusWas]))

		if statusWas: # 오류상태이면 Pass
			pass
		else: # STATUS: 0 - 정상상태

			# #############################################
			# ## Test Event
			# ## events: {'id': 0, 'kind': 'detected', 'initialPos': {'x': 0, 'y': 0}, 'currentPos': {'x': -2440, 'y': 3651}, 'distance': 0, 'step': 0, 'size': 76}
			# xIs = random.randrange(-30000,30000)
			# yIs = random.randrange(0,30000)
			# size = random.randrange(1000,5000)
			# events = {"objects": [{"id": 0, "kind": "detected", "initialPos": {"x": xIs, "y": yIs}, "currentPos": {"x": xIs, "y": yIs}, "distance": 0, "step": 0, "size": size}]}

			# # filteredID = "101Z0_000000_000000"
			# ## Test Event
			# #############################################

			## 각각의 이벤트가 설정 조건에 적합한지 검사
			for event in events["objects"]:
				## events: {'id': 0, 'kind': 'candidate', 'initialPos': {'x': -2440, 'y': 3651}, 'currentPos': {'x': -2440, 'y': 3651}, 'distance': 4392, 'step': 515, 'size': 76}
				## 설명: 'initialPos': {'x': 2844, 'y': 3706}, 'currentPos': {'x': 2838, 'y': 3733}, 'distance': 4690, 'step': 231, 'size': 572
				## 'initialPos': 시작 {X,Y}, 'currentPos': 현재 {X,Y}, 'distance': 직선거리(mm), 'step': 스켄번호, 'size': 크기(mm)

				## SVG 실시간 표현을 위한 이벤트 전송 
				response = realtime_html("localhost",config["port"]["forZone"],event)
				# print("From Nodejs {}".format(response))

				## Filtering - Kind : detected or candidate
				if event["kind"] == "detected":
					pass
				else:
					continue

				## 필터 아이디는 allowGroup인 경우 사용자 Zone과 Level이 설정 되며
				## denyGroup영역이 아닌 모든 이벤트는 존은 A이고 레벨은 0(Normal)으로 설정 한다.
				filteredID = "" # 이벤트 내부 아이디 : A0_000000_000000
				## Filtering - Area
				## 무시영역(denyGroup)은 허용영역보다 우선처리 된다.
				## 무시영역을 제외한 모든 이벤트를 허용한다.
				if areaFilter == "denyGroup": # 거부우선
					tempStat = False
					for k, v in config["filter"]["maskCoord"]["denyGroup"].items():
						if v[0] <= event["currentPos"]["x"] <= v[2] and v[1] <= event["currentPos"]["y"] <= v[3]:
							# print("denyGroup", event["currentPos"]["x"], event["currentPos"]["y"], k)
							tempStat = True
							filteredID = k
							break
					if tempStat:
						continue
					else:
						pass
				
				## 허용영역(allowGroup)은 허용영역보다 우선처리 된다.
				## 허용영역을 제외한 모든 이벤트를 무시한다.
				if areaFilter == "allowGroup": # 허용우선
					tempStat = False
					for k, v in config["filter"]["maskCoord"]["allowGroup"].items():
						if v[0] <= event["currentPos"]["x"] <= v[2] and v[1] <= event["currentPos"]["y"] <= v[3]:
							# print("allowGroup", event["currentPos"]["x"], event["currentPos"]["y"], k)
							tempStat = True
							filteredID = k
							break
					if tempStat:
						pass
					else:
						continue
				
				if areaFilter == "ignoreGroup": # 모두 수용
					pass
				
				## Action Code Here
				if filteredID: ## 레벨과 존에 따른 조건이 있으면
					pass
				else:
					## 허용영역(allowGroup)이 아닌 모든 이벤트의 존은 999이고 레벨은 0(Normal)로 설정 한다.
					filteredID = "999Z0_000000_000000"
					continue

				zoneID = filteredID[0:3] ## 필터아이디의 존등급 (101, 201, ~ 989)
				trigger = f"T{filteredID[0:1]}" ## 필터아이디의 존등급 (101, 201, ~ 989)
				levelID = filteredID[4:5] ## 필터아이디의 두번째 문자 - 레벨등급 (normal, alert, ...)

				# print("Current Event", filteredID, levelSize[levelID], zoneID, levelID, trigger)

				## 이벤트 크기 검사
				## Filtering - Size
				# print("Size Filter:{} Min:{} Max:{}".format(levelSize[levelID], config["level"][levelID]["size"]["min"], config["level"][levelID]["size"]["max"]))
				if levelSize[levelID] == "both": # Min 필터보다 크거나 Max 필터보다 작은 이벤트
					if config["level"][levelID]["size"]["min"] < event["size"] < config["level"][levelID]["size"]["max"]:
						pass
					else:
						continue
				elif levelSize[levelID] == "min": # Min 필터보다 크면
					if config["level"][levelID]["size"]["min"] < event["size"]:
						pass
					else:
						continue
				elif levelSize[levelID] == "max": # Max 필터보다 작으면
					if event["size"] < config["level"][levelID]["size"]["max"]:
						pass
					else:
						continue
				else:
					pass


				# print("{} {}".format(filteredID, event))
				tmpID = "{}-{}".format(event["initialPos"]["y"],event["initialPos"]["x"])
				tmpCnt = setThreadingTimer(tmpID, config["level"][levelID]["reset"])
				if config["level"][levelID]["hold"]["cont"] == 0: # 횟수제한 없이 출력
					# print("No Keep ID:{} {}mm {}th".format(tmpID, event["size"], tmpCnt))
					pass
				else: # 설정횟수 제한 (Count)
					if tmpCnt < config["level"][levelID]["hold"]["cont"]: # 설정횟수 이하이면
						continue
					else: # 
						if config["level"][levelID]["hold"]["keep"]: # 설정횟수 고정(Keep)
							config["actCount"][tmpID] = 0

						# print("Cont. ID:{} {}mm {}th".format(tmpID, event["size"], tmpCnt))

				#####################################
				## 이벤트 전송 #######################
				#####################################

				#####################################
				## logger 등록
				logger.info(f'Level:{config["level"][levelID]["name"]} ID:{tmpID} key:{filteredID} Size:{event["size"]}mm Keep:{config["level"][levelID]["hold"]["keep"]} Set#:{config["level"][levelID]["hold"]["cont"]} Cur#:{tmpCnt}th')

				#####################################
				## 데이터베이스 등록
				# [INFO|RLS3.py:167] 2022-09-13 17:48:50,656 > {'id': 0, 'kind': 'candidate', 'initialPos': {'x': -3668, 'y': 7277}, 'currentPos': {'x': -3674, 'y': 7290}, 'distance': 8164, 'step': 487, 'size': 106}
				insert_event_RLS_V(config["mysql"]["table"]["log"], event["kind"], event["initialPos"]["y"], event["initialPos"]["x"], event["currentPos"]["y"], event["currentPos"]["x"], event["distance"], event["step"], event["size"], zoneID, levelID, tmpCnt)

				#####################################
				## IMS 등록 string.replace(".", "_" )
				id = "{}_{}_{}".format(config["mysql"]["table"]["rls_v"], config["server"]["localhost"]["addr"].replace(".", "_" ), filteredID.split('-', 1)[0])
				name = "name"
				beep = 1
				status = 1
				# 스넵이미지 URL
				shot = config["camera"]["liveShot"].replace("http://", "" ) #config["sensor"]["cmd"]["shot"] + config["sensor"]["cmd"]["shot"]
				msg = "msg"
				imsValue=("id={0},name={1},beep={2},status={3},shot={4},msg={5}".format(id,name,beep,status,shot,msg))
				# print(imsValue)
				reponse = realtime_IMS(imsValue)

				#####################################
				## API3 데이터 전송 - ITS API3
				if config["server"]["user1st"]["addr"] and config["server"]["user1st"]["port"] == config["port"]["forAPI3"] and config["server"]["user1st"]["method"] =="api3" and config["server"]["user1st"]["command"]:
					trigger_API3(config["server"]["user1st"]["addr"], config["port"]["forAPI3"], config["server"]["user1st"]["command"])
				if config["server"]["user2nd"]["addr"] and config["server"]["user2nd"]["port"] == config["port"]["forAPI3"] and config["server"]["user2nd"]["method"] =="api3" and config["server"]["user2nd"]["command"]:
					trigger_API3(config["server"]["user2nd"]["addr"], config["port"]["forAPI3"], config["server"]["user2nd"]["command"])

				#####################################
				## API3 트리거링 전송 - ITS API3
				# print(config["trigger"][trigger])
				if config["trigger"][trigger]: # config["trigger"]["T1"] == True
					trigger_API3(config["server"]["localhost"]["addr"], config["port"]["forAPI3"], config["trigger_command"][trigger])

		if not config["recordOn"] and len(config["actTimer"]): # False and 0< : 이벤트 발생중인 상태 - Start
			config["recordOn"] = True 
			print(">>>>>>>>>>>>>>>>>>>>>>")
		elif config["recordOn"] and not len(config["actTimer"]): # True and 0 : 이벤트 발생후 평상 상태로 복귀 - End
			config["recordOn"] = False
			print("<<<<<<<<<<<<<<<<<<<<<<")
		else: # 이벤트가 없는 상태
			# print(config["recordOn"], len(config["actTimer"]))
			pass

		time.sleep(config["sensor"]["pickupDue"]) # Keep Sensor Load

if __name__ == "__main__":
	config = readConfig("./config_RLS3.json")

	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	logger = logging.getLogger("RLS") # 로거 인스턴스를 만든다
	formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s") # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = config["path"]["logger"]
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(formatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(formatter)
	os.chmod(filename,0o777)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	logger.setLevel(loggerLevel)
	# 로거 인스턴스 로그 예
	logger.info("START")
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	############ logging ################

	run_demon()

	main()
