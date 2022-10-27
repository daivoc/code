#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from config_db import *
from config_sensor import *
from module_for_optex import *
from module_for_mysql import *

import io
######################################################
# - 패킥 대기 모드 루프
# - 감지된 패킷을 읽어 들인다.
# - 하트비트(16 Byte)만 존재하면 루틴을 종료하고 대기모드로 전환
# - 감지 데이터가 존재하면 하트비트를 제거한 데이터만 취합한다.
# - 취합한 데이터의 오류가 있으면 처리후 다시 대기모드로 전환 하고 
# - 오류가 없으면 감지데이터를 통해 정보를 취합한다.
# - https://docs.python.org/3/library/struct.html
######################################################

### Packet field access ###
def all(packet):
	return binascii.hexlify(packet).decode()

def hartbeat(packet):
	return binascii.hexlify(packet[0:16]).decode()

def payload(packet):
	return binascii.hexlify(packet[16:]).decode()

######################################################
## 블록 데이터 식별 아이디
######################################################
def blockType(packet): # 블록 형식 0x00E0 - 2 Byte
	i = int(binascii.hexlify(packet[0:2]).decode(), 16) # -> e0 00
	j = struct.unpack("<H", struct.pack(">H", i))[0] # -> x00e0 -> d224, H: unsigned short integer 2 Byte
	return hex(j).split('x')[1] # -> 224 -> 0xe0
	
def blockSize(packet): # 데이터 수 - 2 Byte 
	i = int(binascii.hexlify(packet[2:4]).decode(), 16) # -> 10 00
	return struct.unpack("<H", struct.pack(">H", i))[0] # -> 0x0010 -> 0d16, H: unsigned short integer 2 Byte

######################################################
## 거리 데이터전문
######################################################
def slaveID(packet): # 슬레이브기판ID D0 : 1-255
	return binascii.hexlify(packet[0:1]).decode()

def deviceID(packet): # 기기식별코드 D1 : Ascii
	return binascii.hexlify(packet[1:2]).decode()

def distant(packet): # 거리 D2 D3 D4 D5 : 1 ~ 999999 - 4 Byte
	i = int(binascii.hexlify(packet[2:6]).decode(), 16)
	tmpDist = struct.unpack("<I", struct.pack(">I", i))[0] # I: unsigned integer 4Byte
	if tmpDist < 4294967295:
		return float(tmpDist)
	else:
		return 0

# ※1 이상 코드
# 1：이상 없음			
# 4: 근거리 위험 표시 거리 미만			
# 5: A/D치 포화시			
# bit4:의사 거리 출력 플래그			
def errorCode(packet): # 이상코드 D6 : 0 ~ 255 ※1
	# return binascii.hexlify(packet[6:7]).decode()
	i = binascii.hexlify(packet[6:7]).decode()
	return int(i, 16)

# ※ 2 피크 레벨
# 0: 레벨 비 출력
# 1：레벨 0~1999
# 2：레벨 2000~3999
# 3：레벨 4000~5999
# 4：레벨 6000~7999
# 5：레벨 8000~9999
# 6：레벨 10000 이상
def peakLevel(packet): # 피크레벨 D7 : 0 ~ 6 ※2 예: 0x06 -> 6 으로 변환
	# return binascii.hexlify(packet[7:8]).decode()
	i = binascii.hexlify(packet[7:8]).decode()
	return int(i, 16)
  
# ※3 경보출력 - 출력 커넥터 사양
# bit0：경보A 출력(감지=1)
# bit1：경보B 출력(감지=1)
# bit2：감시중 출력(정상=1)
# bit3：탬퍼 출력(리개 개방=1)
# bit4：점검 입력(쇼트=1)
# bit5：예비 입력A(쇼트=1)
# bit6：예비 입력B(쇼트=1)
# bit7：탬퍼 입력(리개 개방=1)
def alarmOut(packet): # 경보출력 D8 : bit0-7 ※3
	# return binascii.hexlify(packet[8:9]).decode()
	i = binascii.hexlify(packet[8:9]).decode() # 05
	return  bin(int(i, 16))[2:].zfill(8) # 05 -> 00000101


# ※4 대향형/자립형 플래그
# 0：대향형 모드 채용중
# 1：자립형 모드 채용중
def sensorType(packet): # 대향형/자립형 플래그 D9 : 0/1 ※4 - tmp_sensorType
	# return binascii.hexlify(packet[9:10]).decode()
	i = binascii.hexlify(packet[9:10]).decode()
	return int(i, 16)

# ※5 속도
# + : 접근　- : 이반 방향
def speed(packet): # 속도 (Km/h) D10 D11 : -999 ~ +999 ※5
 	i = int(binascii.hexlify(packet[10:12]).decode(), 16) # -> 10 00
	j = struct.unpack("<H", struct.pack(">H", i))[0] # -> 0x0010 -> 0d16, H: unsigned short integer 2 Byte
	
	if j > 32768:
		j = int(j - 65535) # 소수점
	return j

def getSnapshot(BSS_url, tmp_speed): 
	# 이벤트 스크린샷
	# print time.strftime('%Y/%m/%d')
	tmpYear = img_data_sub+time.strftime('%Y/') # 년도 방
	if not os.path.exists(tmpYear): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpYear)
		os.chmod(tmpYear, 0o777)
	tmpMonth = tmpYear+time.strftime('%m/') # 월별 방
	if not os.path.exists(tmpMonth): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpMonth)
		os.chmod(tmpMonth, 0o777)
	tmpDay = tmpMonth+time.strftime('%d/') # 일별 방
	if not os.path.exists(tmpDay): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpDay)
		os.chmod(tmpDay, 0o777)
	tmpFullPath = tmpDay+time.strftime('%H/') # 시간별 방
	if not os.path.exists(tmpFullPath): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpFullPath)
		os.chmod(tmpFullPath, 0o777)
	# tmpName = time.strftime('%M_%S-URL_01') + ".jpg"
	millis = int(round(time.time() * 100))
	# tmpName = time.strftime('%M_%S_') + str(millis) + ".jpg" # '%d/%m/%y %H:%M:%S.%f'
	tmpName = time.strftime('%M_%S_') + str(millis) + "_" + str(tmp_speed) + ".jpg" # '%d/%m/%y %H:%M:%S.%f'
	
	thisImgName = tmpFullPath + tmpName
	run_wget_image(BSS_url, thisImgName) # Ontime Screenshot
	os.chmod(thisImgName, 0o777)
	return thisImgName
			
##### 데이터 검증 ##################################
	
if __name__ == '__main__':

	myTableID = sys.argv[1]
	
	for row in read_field_w_cfg_serial_BSS(myTableID): # 로깅을 위한 파일명으로 사용할 시리얼 번호를 가지고 온다.
		mySensorID = row["w_sensor_serial"]
	
	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418

	if not os.path.exists(ITS_log_data): # ITS_log_data 폴더 생성
		os.makedirs(ITS_log_data)
	logger = logging.getLogger(mySensorID) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = ITS_log_data+mySensorID+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info("/_/_/ START /_/_/")
	# logger.debug("===========================")
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	# logger.debug("===========================")
	# logger.info("TEST END!")
	############ logging ################
	
	############ Images ################
	# 이미지 파일 초기화 
	if not os.path.exists(ITS_img_data): # ITS_img_data 폴더 생성
		os.makedirs(ITS_img_data)
	# 센서 이벤트 스크린샷 이미지 저장 폴더명
	img_data_sub = ITS_img_data + mySensorID + "/"
	if not os.path.exists(img_data_sub): # ITS_img_data 내의 서브 사진 폴더 생성
		os.makedirs(img_data_sub)
	############ Images ################

	# 테이블 생성
	returnMsg = create_table_w_log_BSS(mySensorID) # 테이블 생성 - 반환값

	w_cfg_sensor_list_BSS = read_table_w_cfg_sensor_BSS(myTableID)
	set_reload_w_cfg_reload_BSS(myTableID) # 설정값을 읽은 후(read_table_w_cfg_sensor_BSS) 재시동 필드를 회복시킨다.
	for row in w_cfg_sensor_list_BSS:
		BSS_subject = row["wr_subject"]
		# BSS_id = row["w_id"]
		# BSS_cpu_id = row["w_cpu_id"]
		BSS_license = row["w_license"]
		BSS_device_id = row["w_device_id"]
		BSS_sensor_serial = row["w_sensor_serial"] #
		BSS_sensor_model = row["w_sensor_model"]
		BSS_sensor_face = row["w_sensor_face"]
		BSS_sensor_angle = row["w_sensor_angle"]
		BSS_sensor_lat_s = row["w_sensor_lat_s"]
		BSS_sensor_lng_s = row["w_sensor_lng_s"]
		BSS_sensor_lat_e = row["w_sensor_lat_e"]
		BSS_sensor_lng_e = row["w_sensor_lng_e"]
		BSS_sensor_ignoreS = row["w_sensor_ignoreS"] #
		BSS_sensor_ignoreE = row["w_sensor_ignoreE"] #
		BSS_sensor_noOfZone = row["w_sensor_noOfZone"] #
		BSS_sensor_stepOfZone = row["w_sensor_stepOfZone"] # 
		BSS_sensor_spot = row["w_sensor_spot"] #
		BSS_sensor_offset = row["w_sensor_offset"] #
		BSS_sensor_speedLimit = row["w_sensor_ignoreZone"] #
		BSS_sensor_distMin = row["w_sensor_scheduleS"] # 감지시작
		BSS_sensor_distMax = row["w_sensor_scheduleE"] # 감지종료
		BSS_sensor_scheduleZone = row["w_sensor_scheduleZone"]
		BSS_sensor_sensor_week = row["w_sensor_week"]
		# BSS_sensor_sensor_time = row["w_sensor_time"]
		# BSS_sensor_disable = row["w_sensor_disable"]
		BSS_sensor_stop = row["w_sensor_stop"] #
		BSS_sensor_reload = row["w_sensor_reload"] #
		BSS_event_noise = int(row["w_event_pickTime"])
		BSS_event_maxShut = row["w_event_holdTime"] # 스넵샷 허용횟수 
		BSS_event_keepHole = row["w_event_keepHole"] #
		BSS_event_syncDist = row["w_event_syncDist"] #
		BSS_alarm_disable = row["w_alarm_disable"] #
		BSS_alarm_level = row["w_alarm_level"] #
		BSS_system_ip = row["w_system_ip"]
		BSS_system_port = row["w_system_port"]
		# BSS_systemBF_ip = row["w_systemBF_ip"]
		# BSS_systemBF_port = row["w_systemBF_port"]
		# BSS_systemAF_ip = row["w_systemAF_ip"]
		# BSS_systemAF_port = row["w_systemAF_port"]
		# BSS_master_Addr = row["w_master_Addr"]
		# BSS_master_Port = row["w_master_Port"]
		BSS_virtual_Addr = row["w_virtual_Addr"] #
		BSS_virtual_Port = row["w_virtual_Port"] #
		BSS_sensor_Addr = row["w_sensor_Addr"] #
		BSS_sensor_Port = row["w_sensor_Port"]
		BSS_email_Addr = row["w_email_Addr"]
		BSS_email_Time = row["w_email_Time"]
		BSS_table_PortIn = row["w_table_PortIn"]
		BSS_table_PortOut = row["w_table_PortOut"]
		BSS_host_Addr = row["w_host_Addr"]
		BSS_host_Port = row["w_host_Port"]
		BSS_host_Addr2 = row["w_host_Addr2"]
		BSS_host_Port2 = row["w_host_Port2"]
		# BSS_tcp_Addr = row["w_tcp_Addr"]
		# BSS_tcp_Port = row["w_tcp_Port"]
		# BSS_tcp_Addr2 = row["w_tcp_Addr2"]
		# BSS_tcp_Port2 = row["w_tcp_Port2"]
		BSS_url = row["w_url1"] #
		# BSS_url2 = row["w_url2"]
		BSS_alert_Port = int(row["w_alert_Port"])
		BSS_alert_Value = float(row["w_alert_Value"])
		# BSS_alert2_Port = int(row["w_alert2_Port"])
		# BSS_alert2_Value = float(row["w_alert2_Value"])
		BSS_opt11 = row["w_opt11"].replace(":", "")[0:4] # 14:12 -> 1412 로 변경후 4자만 취합
		BSS_opt12 = row["w_opt12"]
		BSS_opt21 = row["w_opt21"].replace(":", "")[0:4]
		BSS_opt22 = row["w_opt22"]
		BSS_keycode = row["w_keycode"]
		BSS_stamp = row["w_stamp"] #

	try: # GPIO 포트 초기화
		GPIO.setwarnings(False) # to disable warnings
		GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
		GPIO.setup(BSS_alert_Port, GPIO.OUT)
		GPIO.output(BSS_alert_Port, GPIO.HIGH)
	except:
		pass
	
	myIP = get_ip_address('eth0')
	BUFSIZ = 1024
	
	eventDataBit = 0
	eventHeartBit = 0
	eventOverSpeed = 0
	eventName = ''

	errorCntCreate = 0 # 소켓 생성 오류 횟수
	errorCntConnect = 0 # 소켓 접속 오류 횟수
	
	reloadCheck = 0 # 프로그램 재 구동
	
	# 시작정보 로그입력
	insert_event_log_BSS(mySensorID, w_cfg_id=1, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='System Boot', w_event_desc='Start Program', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
	
	try:
		tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
		tcpSerSock.bind((BSS_virtual_Addr, BSS_virtual_Port)) # <------- 소켓을 주소로 바인딩
		tcpSerSock.listen(2) # <------ listening 시작. 최대 클라이언트 (연결 수)
		# tcpSerSock.settimeout(2) #  <------- 타임아웃 에러 (초)
		
		logger.info("Connected and Listen IP:%s PORT:%s" % (BSS_virtual_Addr, BSS_virtual_Port))
	except:
		logger.critical('Error#(%s) At Creating Socket. Please Check Socket IP(%s) Address And Port(%s) Number' % (errorCntCreate, BSS_virtual_Addr, BSS_virtual_Port))
		insert_event_log_BSS(mySensorID, w_cfg_id=2, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=1, w_event_stat='Over Count of Creating Socket', w_event_desc='Reboot System', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
		logger.critical('Error Creating Socket # %s' % errorCntCreate)
		reboot_its() # send mail to manager

	while True:
		try:
			tcpCliSock, addr = tcpSerSock.accept()
			tcpCliSock.settimeout(ERROR_recv_timeout)
				
			if addr[0] == BSS_sensor_Addr: # 약속된 센서 아이피만 수용한다.
				logger.info('Connected Client Socket')
			else:
				logger.critical('Error Unmatched Sensor\'s IP. WITS Wait From %s. Please Check Config Table.' % BSS_sensor_Addr)
				logger.critical('Or Please Check Sensor IP %s.' % addr[0])
				raise
		except: 
			logger.critical('Error#(%s) At After Socket Bind:IP(%s) Port(%s). Please Check 1)Cable Langth And Connector Or Wiring. 2)Data Signal Level.' % (errorCntConnect, BSS_virtual_Addr, BSS_virtual_Port))
			# exit(1) # send mail to manager
			insert_event_log_BSS(mySensorID, w_cfg_id=2, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=1, w_event_stat='Over Count of Socket Bind', w_event_desc='Reboot System', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
			logger.critical('Error Connect # %s' % errorCntConnect)
			reboot_its() # send mail to manager
			
		while True:
			data = tcpCliSock.recv(BUFSIZ) # 0b001500150010000000000000000000
			## print len(data), all(data)
			if len(data) > 16: # 하트비트를 포함한 이밴트 데이터 
				eventData = data[16:] # 하트비트 이후의 자료 저장
				typeOfBlock = blockType(eventData) # 명령문 해석 ex: e0는 거리데이터, e1은 센서 설정갑 변동 응답(?), 0b는 하트비트
				sizeOfBlock = blockSize(eventData)
				if typeOfBlock == 'e0' and sizeOfBlock == 16: # 거리 데이터
					distData = eventData[4:]
					#####################################################
					## 아래 기능으로 접근하거나 멀이지는 이벤트를 구분가능 하다.
					## if len(distData) == 16 and speed(distData) > 0: # 센서로 접근하는 이벤트 무시
					#####################################################
					if len(distData) == 16 and speed(distData) < 0: ## 센서로부터 멀어지는 이벤트 무시
						continue ## 역주행
					else: ## 정주행
						pass
				else: # 예외데이터
					continue
			elif len(data) == 16: # 하트비트
				# continue
				reloadCheck = 1
			else:
				continue

			if reloadCheck:
				########################################################
				## 하트비트 감지 시 다음 실행
				## 데이터베이스 접속 확인
				## 실시간 설정 변동 값을 휴간상황때 데이터베이스 접속 확인
				########################################################
				
				for row in read_field_w_cfg_status_BSS(myTableID):
					BSS_sensor_stop = row["w_sensor_stop"]		# `w_sensor_stop` TINYINT(1) - 일시정지
					BSS_sensor_reload = row["w_sensor_reload"] 	# `w_sensor_reload` TINYINT(1) - 재시동
					BSS_alarm_disable = row["w_alarm_disable"]	# `w_alarm_disable` TINYINT(1) -알람중지
					
				if BSS_sensor_reload: # 재시동
					logger.info('Reload Program.')
					set_reload_w_cfg_reload_BSS(myTableID) # 재시동 필드를 회복시킨다.
					insert_event_log_BSS(mySensorID, w_cfg_id=3, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='User Request', w_event_desc='Reload Program', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
					
					## 재시동
					set_reload_w_cfg_reload_BSS(myTableID) # 설정값을 읽은 후 재시동 필드를 회복시킨다.
					for row in read_field_w_cfg_setup_BSS(myTableID):
						BSS_sensor_speedLimit = row["w_sensor_ignoreZone"] 
						BSS_sensor_distMin = row["w_sensor_scheduleS"]
						BSS_sensor_distMax = row["w_sensor_scheduleE"]
						BSS_event_maxShut = row["w_event_holdTime"]
						BSS_event_noise = int(row["w_event_pickTime"])
						BSS_opt11 = row["w_opt11"].replace(":", "")[0:4] # 14:12 -> 1412 로 변경후 4자만 취합
						BSS_opt12 = row["w_opt12"]
						BSS_opt21 = row["w_opt21"].replace(":", "")[0:4]
						BSS_opt22 = row["w_opt22"]

					if BSS_alarm_disable: print 'Reload Program.'
					
				reloadCheck = 0 # 재시작 초기화 
					
				curStatus = Event_type['idle'];
				# logger.info(Event_desc[curStatus])
				
				################################################################
				## 관제실로 하트비트 이벤트 전송 (BSS_host_Addr, BSS_host_Port)
				################################################################
				# if BSS_host_Addr and BSS_host_Port: # 호스트정보가 있으면 정보 전송
					# insert_socket_log_BSS_SPEED(BSS_sensor_serial, BSS_subject, BSS_host_Addr, BSS_host_Port, 0, 0)
					# if BSS_host_Addr2 and BSS_host_Port2: # 호스트정보가 있으면 정보 전송
						# insert_socket_log_BSS_SPEED(BSS_sensor_serial, BSS_subject, BSS_host_Addr2, BSS_host_Port2, 0, 0)
				
				# 실시간 속도계 서비스를 위한 이벤트 전송 
				# table_SPEED.js와 연동되어 움직인다.
				insert_socket_monitor_BSS_OBJ(BSS_sensor_serial, BSS_subject, 0, 0, 0, 0, BSS_system_ip, BSS_table_PortIn, 0, 0, 0, 0, 0, 0, 0, '', 0)
					
				# STSTUS 전송 table_union.js와 연동되어 움직인다.
				insert_socket_status_UNION(BSS_sensor_serial, BSS_subject, BSS_system_ip, BSS_system_port, model=BSS_sensor_model, board=ECOS_table_SPEED, tableID=myTableID, status=curStatus, msg=Event_desc[curStatus])  # 소켓 유니온 전송
				continue

				
			##### 순수한 이벤트 정보(거리, 속도, 감도, 릴레이 상태 및 센서 정보) ##########################
			if len(distData) == 16:
				tmp_cfg_id = 0
				tmp_slaveID = slaveID(distData)
				tmp_deviceID = deviceID(distData) # 센서아이디
				tmp_distant = distant(distData) # 거리, 소수점 3자리 mm 으로 표시
				tmp_errorCode = errorCode(distData) # 오류코드
				tmp_peaklevel = peakLevel(distData) # 이벤트레벨
				tmp_alarmOut = alarmOut(distData) # 알람상태
				tmp_sensorType = sensorType(distData) # 센서타입
				tmp_speed = speed(distData) # 속도
				tmp_zeroDist = 0 # 거리가 0인 이벤트는 1로 셋
				tmp_overDist = 0 # 기준거리 이상인경우 자료제한 요소를 해소하기 위함 - 100m:1, 120m:2, 140m:3, 160m:4 이상
				tmp_outLevel = 0 # 기준 레벨을 넘은 이벤트
				tmp_outCount = 0 # 기준 횟수를 넘은 이벤트
				tmp_ignore = 0 # 무시영역 인 이벤트
				tmp_schedule = 0 # 예정된 무시영역 인 이벤트
				tmp_sent = 0 # 관제에 이벤트 전송
				tmp_shot = 0 # 사진
				tmp_error = 0 # 이밴트 오류
				tmp_stat = ''
				tmp_desc = ''
				new_coord = get_current_location_BSS(BSS_sensor_lat_s, BSS_sensor_lng_s, BSS_sensor_lat_e, BSS_sensor_lng_e, tmp_distant, BSS_sensor_stepOfZone, BSS_sensor_noOfZone)
				tmp_lat_s = new_coord[0]
				tmp_lng_s = new_coord[1]
				tmp_lat_e = new_coord[2]
				tmp_lng_e = new_coord[3]
				tmp_zone = int(new_coord[4])
				
				tmp_cnt = 0

				##################################################################################################################
				## 물체의 연속성을 결정 하는 중요한 코드
				## 속도는 없어도 거리와 레벨은 출력가능 하다.
				## 예를 들어 tmp_speed, tmp_peaklevel, tmp_distant 
				## tmp_speed > BSS_sensor_speedLimit - ## 속도 초과한 이밴트만 필터링 한다.(노이즈제거 효과) 
				## int(BSS_sensor_distMin) < int(tmp_distant) and int(BSS_sensor_distMax) > int(tmp_distant) - ## 요구하는 지역내에서 발생한 이밴트
				##################################################################################################################
				if tmp_speed > BSS_event_noise and tmp_peaklevel: # and tmp_distant  
					tmp_cnt = eventHeartBit ## 최초 이벤트 등록을 위한 유효이벤트 실행 횟수 저장
					eventHeartBit = 0
					tmp_heart_cnt = 0
					eventDataBit += 1
					tmp_data_cnt = eventDataBit
				else: ## 유효 이벤트 횟수 리셋
					tmp_cnt = eventDataBit ## 최초 이벤트 등록을 위한 유효이벤트 실행 횟수 저장
					eventDataBit = 0
					tmp_data_cnt = 0
					eventHeartBit += 1
					tmp_heart_cnt = eventHeartBit
				
				if (eventHeartBit%100) == 0: reloadCheck = 2 ## 하트비트 100번 주기로 설정 확인
				
				if BSS_alarm_disable: logger.info("NoiseSP %s\t Data# %s\t Heart %s\t Speed %s\t Dist %s\t Level %s\t"%(BSS_event_noise, tmp_data_cnt, tmp_heart_cnt, tmp_speed, tmp_distant, tmp_peaklevel))
				
				## tmp_time = datetime.datetime.now() # 이벤트 발생 시간 임시 저장	
				tmp_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")						
				tmp_path = ''
				tmp_name = ''
				tmp_imageURL = ''
			else:
				continue
				
			if tmp_data_cnt:
				##### Data ######################
				# if tmp_data_cnt == 1: #BSS_sensor_speedLimit
				# 최초 이밴트속도가 제한속도보다 크면 실행
				if abs(tmp_speed) > int(BSS_sensor_speedLimit): 
					eventOverSpeed = 1
				else:
					eventOverSpeed = 0

				# 최초 이벤트 속도가 초과 했을 때에 만 유효한 이벤트로 간주 한다.
				# 대기모드에서 최초로 이벤트 발생시
				# (tmp_data_cnt % 2) == 1 # 두번에 한장
				# tmp_data_cnt <= BSS_event_maxShut # 최초 3장
				if tmp_data_cnt <= BSS_event_maxShut and eventOverSpeed:

					# 알람
					if BSS_alert_Port and BSS_alert_Value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( BSS_alert_Value:)
						Process(target=alertOut, args=(BSS_alert_Port,BSS_alert_Value)).start()
					
					# 촬영 범위에 이동체가 존재하는지 확인
					if int(BSS_sensor_distMin) < int(tmp_distant) and int(BSS_sensor_distMax) > int(tmp_distant):
						logger.info('D:%s S:%s Z:%s ~ %s' % (tmp_distant, tmp_speed, BSS_sensor_distMin, BSS_sensor_distMax))
						
					# 스넵삿
					# http://myserver/axis-cgi/jpg/image.cgi
					if BSS_url: # 스넵삿이 가능한 BSS_url 값이 있으면 
						eventName = getSnapshot(BSS_url, tmp_speed)
						# tmp_path = eventName[13:] # 머리부분 /var/www/html을 제거
						tmp_path = eventName[21:] # 머리부분 /var/www/html/its_web을 제거
						tmp_name = eventName[-22:]
						tmp_desc = "<a href=%s target=_blank>%s</a>" % (tmp_path,tmp_name) # 머리부분 /var/www/html을 제거
						tmp_imageURL = "http://%s%s"%(myIP,tmp_path)
						logger.info(tmp_desc)
						
					# 이미지 워터마크
					# message = "%s,%s,%skm/h" % (tmp_time, mySensorID, tmp_speed)
					# run_msg_on_image(eventName, message)

					## 오래된 파일 삭제
					run_remove_old_file(img_data_sub, date_of_old) # 

					insert_event_log_BSS(mySensorID, w_cfg_id=tmp_cfg_id, w_bss_slave=tmp_slaveID, w_bss_device=tmp_deviceID, w_bss_distent=tmp_distant, w_bss_error=tmp_errorCode, w_bss_level=tmp_peaklevel, w_bss_alarm=tmp_alarmOut, w_bss_type=tmp_sensorType, w_bss_speed=tmp_speed, w_event_cnt=tmp_data_cnt, w_event_zeroDist=tmp_zeroDist, w_event_outLevel=tmp_outLevel, w_event_outCount=tmp_outCount, w_event_ignore=tmp_ignore, w_event_schedule=tmp_schedule, w_event_sent=tmp_sent, w_event_shot=tmp_shot, w_event_error=tmp_error, w_event_stat=tmp_stat, w_event_desc=tmp_desc, w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
						
					logger.info('Over Speed: %skm/h #%s' % (tmp_speed,tmp_data_cnt))
				else:
					if eventOverSpeed:
						logger.info('Over Speed: %skm/h #%s' % (tmp_speed,tmp_data_cnt))
					else:
						logger.info('Normal Speed: %skm/h #%s' % (tmp_speed,tmp_data_cnt))
				
				################################################################
				## 오버스피드 일때만 관제실로 이벤트 전송 (BSS_host_Addr, BSS_host_Port)
				## BSS_host_Addr: LPR, 
				## BSS_host_Addr2: Display
				## BSS_host_Addr 오버스피드인 경우에 만 이벤트 전송
				## BSS_host_Addr2 10Km이상 이면 이벤트 전송
				################################################################
				
				# print BSS_opt11, BSS_opt12, BSS_opt21, BSS_opt22, datetime.datetime.now().strftime("%H%M")
				lightLV = get_light_level(BSS_opt11, BSS_opt12, BSS_opt21, BSS_opt22)
				print lightLV
				if eventOverSpeed:
					if tmp_path: # Host1 LPR로 전송
						if BSS_host_Addr and BSS_host_Port: # 호스트정보가 있으면 정보 전송
							insert_socket_log_BSS_SPEED(BSS_sensor_serial, BSS_subject, BSS_host_Addr, BSS_host_Port, tmp_speed, eventOverSpeed, tmp_imageURL, lightLV)
				if tmp_speed > 10: #
					if BSS_host_Addr2 and BSS_host_Port2: # 호스트정보가 있으면 정보 전송
						insert_socket_log_BSS_SPEED(BSS_sensor_serial, BSS_subject, BSS_host_Addr2, BSS_host_Port2, tmp_speed, eventOverSpeed, tmp_imageURL, lightLV)
				
				################################################################
				## 관제실로 이벤트 전송 (BSS_host_Addr, BSS_host_Port)
				################################################################
				# 실시간 모니터 관제 서비스를 위한 이벤트 전송 
				# table_SPEED.js와 연동되어 움직인다.
				insert_socket_monitor_BSS_OBJ(BSS_sensor_serial, BSS_subject, tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, BSS_system_ip, BSS_table_PortIn, tmp_distant, tmp_alarmOut, tmp_sensorType, tmp_zone, eventOverSpeed, tmp_time, tmp_speed, '', tmp_peaklevel)

				# table_union.js와 연동되어 움직인다.
				msg='S:%s D:%s' % (tmp_speed, tmp_distant)
				insert_socket_status_UNION(BSS_sensor_serial, BSS_subject, BSS_system_ip, BSS_system_port, model=BSS_sensor_model, board=ECOS_table_SPEED, tableID=myTableID, status=Event_type['active'], msg=msg)  
		tcpCliSock.close()
	tcpSerSock.close()			
