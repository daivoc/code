#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from config_db import *
from config_sensor import *
from module_for_optex import *
from module_for_mysql import *


######################################################
# - 패킥 대기 모드 루프
# - 감지된 패킷을 읽어 들인다.
# - 하트비트(16 Byte)만 존재하면 루틴을 종료하고 대기모드로 전환
# - 감지 데이터가 존재하면 하트비트를 제거한 데이터만 취합한다.
# - 취합한 데이터의 오류가 있으면 처리후 다시 대기모드로 전환 하고 
# - 오류가 없으면 감지데이터를 통해 정보를 취합한다.
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
	j = struct.unpack("<H", struct.pack(">H", i))[0] # -> x00e0 -> d224
	return hex(j).split('x')[1] # -> 224 -> 0xe0
	
def blockSize(packet): # 데이터 수 - 2 Byte 
	i = int(binascii.hexlify(packet[2:4]).decode(), 16) # -> 10 00
	return struct.unpack("<H", struct.pack(">H", i))[0] # -> 0x0010 -> 0d16

######################################################
## 거리 데이터전문
######################################################
def slaveID(packet): # 슬레이브기판ID D0 : 1-255
	return binascii.hexlify(packet[0:1]).decode()

def deviceID(packet): # 기기식별코드 D1 : Ascii
	return binascii.hexlify(packet[1:2]).decode()

def distant(packet): # 거리 D2 D3 D4 D5 : 1 ~ 999999 - 4 Byte
	i = int(binascii.hexlify(packet[2:6]).decode(), 16)
	tmpDist = struct.unpack("<I", struct.pack(">I", i))[0]
	if tmpDist < 4294967295:
		return float(tmpDist)
	else:
		return 0

# 자립형에서 100미터가 넘을 경우
def overDist(distant): # 거리 D2 D3 D4 D5 : 1 ~ 999999 - 4 Byte
	if distant > 159999: # 159 미터 이상이면 한번의 이밴트에 알림전송
		return 1
	elif distant > 139999: # 139 미터 이상 한번의 이밴트에 알림전송
		return 1
	elif distant > 119999: # 119 미터 이상 두번의 이밴트에 알림전송
		return 2
	elif distant > 99999: # 99 미터 이상 세번의 이밴트에 알림전송
		return 3
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
 	i = int(binascii.hexlify(packet[10:12]).decode(), 16)
	return struct.unpack("<I", struct.pack(">I", i))[0]

##### 데이터 검증 ##################################
def isItNormalDate():
	weekNo = datetime.datetime.today().weekday() # 현재의 주일번호 확인 Monday is 0 and Sunday is 6.
	# print BSS_sensor_sensor_week
	if str(weekNo) in BSS_sensor_sensor_week: # BSS_sensor_sensor_week를 어레이로 변환후 오늘의 주번호와 일치하는지 확인
		isScWeek = check_scheduledWeek_BSS(myTableID, weekNo) # 주간 예약인지 확인
		if isScWeek['cnt'] > 0:
			# print isScWeek, "isScWeek"
			return 0 # 지금은 예약된 일시 입니다.
			
	# 현재날짜와 시간이 예약된 날자인지 확인(일치하는 필드 갯수)한다.
	isScDate = check_scheduledDate_BSS(myTableID)
	if isScDate['cnt'] > 0:
		# print isScDate, "isScDate"
		return 0 # 지금은 예약된 일시 입니다.
	else:
		return 1 # 예약 안된 일시 입니다.




		
def isVaildZone(dist, BSS_sensor_ignoreS, BSS_sensor_ignoreE, BSS_sensor_ignoreZone, BSS_sensor_stepOfZone):
	# if BSS_alarm_disable: print(dist, BSS_sensor_ignoreS, BSS_sensor_ignoreE, BSS_sensor_ignoreZone, BSS_sensor_stepOfZone)
	isVaildZone = 1
	if dist < BSS_sensor_ignoreS:
		return 0
	if dist > BSS_sensor_ignoreE:
		return 0
	
	if BSS_sensor_ignoreZone: # 비활성 지역 이 있으면 
		zones = BSS_sensor_ignoreZone.rstrip(',')
		ignoreZone = zones.split(',')
		for i in ignoreZone:
			zoneS = BSS_sensor_stepOfZone * float(i)
			zoneE = zoneS + BSS_sensor_stepOfZone + 1
			if zoneS <= dist and dist < zoneE:
				# if BSS_alarm_disable: print(zoneS, dist, zoneE)
				return 0
	return isVaildZone
	
def isVaildLevel(tmp_peaklevel): # 0 ~ 6, 0:레벨 비출력
	# 1 => '감도 1 이상, 거리 무시',
	# 2 => '감도 2 이상, 거리 무시',
	# 3 => '감도 3 이상, 거리 무시',
	# 4 => '감도 4 이상, 거리 무시',
	# 5 => '감도 5 이상, 거리 무시',
	# 6 => '감도 6 이상, 거리 무시',
	isVaildLevel = 1
	if tmp_peaklevel < BSS_alarm_level:
		return 0
	return isVaildLevel

def isVaildZoneSchedule(dist, BSS_sensor_scheduleS, BSS_sensor_scheduleE, BSS_sensor_scheduleZone, BSS_sensor_stepOfZone):
	# if BSS_alarm_disable: print(dist, BSS_sensor_scheduleS, BSS_sensor_scheduleE, BSS_sensor_scheduleZone, BSS_sensor_stepOfZone)
	isVaildZoneSchedule = 1
	if dist < BSS_sensor_scheduleS:
		return 0
	if dist > BSS_sensor_scheduleE:
		return 0
	
	if BSS_sensor_scheduleZone: # 비활성 지역 이 있으면 
		zones = BSS_sensor_scheduleZone.rstrip(',')
		ignoreZoneSchedule = zones.split(',')
		for i in ignoreZoneSchedule:
			zoneS = BSS_sensor_stepOfZone * float(i)
			zoneE = zoneS + BSS_sensor_stepOfZone + 1
			if zoneS <= dist and dist < zoneE:
				# if BSS_alarm_disable: print(zoneS, dist, zoneE)
				return 0
	return isVaildZoneSchedule

def getSnapshot(BSS_url): 
	# 이벤트 스크린샷
	# print time.strftime('%Y/%m/%d')
	tmpYear = img_data_sub+time.strftime('%Y/') # 년도 방
	if not os.path.exists(tmpYear): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpYear)
	tmpMonth = tmpYear+time.strftime('%m/') # 월별 방
	if not os.path.exists(tmpMonth): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpMonth)
	tmpDay = tmpMonth+time.strftime('%d/') # 일별 방
	if not os.path.exists(tmpDay): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpDay)
	tmpFullPath = tmpDay+time.strftime('%H/') # 시간별 방
	if not os.path.exists(tmpFullPath): # ITS_image_data 내의 서브 사진 폴더 생성
		os.makedirs(tmpFullPath)
	tmpName = time.strftime('%M_%S-URL_01') + ".jpg"
	
	thisImgName = tmpFullPath + tmpName
	run_wget_image(BSS_url, thisImgName) # Ontime Screenshot
	return thisImgName
	# return "getSnapshot"
			
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

	insert_event_log_BSS(mySensorID, w_cfg_id=1, w_bss_slave='-', w_bss_device='-', w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='Reboot System', w_event_desc='/_/ START /_/', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')

	errorCntCreate = 0 # 소켓 생성 오류 횟수
	errorCntConnect = 0 # 소켓 접속 오류 횟수
	errorCntRecv = 0 # 페킷 받은 오류 횟수
	
	eventHeartBit = 0
	notChangedVaildEventCnt = 0
	
	commndFlag = 0 # 메세지 출력시 사용자 요청에 의함인지 확인
	
	eventTimeIs = datetime.datetime.now() # 이벤트 발생 시간 임시 저장
	eventHeartBitDue = eventTimeIs # 이벤트 발생 시간 임시 저장
	notChangedVaildEventCntDue = eventTimeIs # 이벤트 발생 시간 임시 저장

	notChangedAllEventCnt = 0 # 변화 없이 연속된 이벤트 횟수
		
	while True:
		w_cfg_sensor_list_BSS = read_table_w_cfg_sensor_BSS(myTableID)
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
			BSS_sensor_ignoreZone = row["w_sensor_ignoreZone"] #
			BSS_sensor_scheduleS = row["w_sensor_scheduleS"]
			BSS_sensor_scheduleE = row["w_sensor_scheduleE"]
			BSS_sensor_scheduleZone = row["w_sensor_scheduleZone"]
			BSS_sensor_sensor_week = row["w_sensor_week"]
			# BSS_sensor_sensor_time = row["w_sensor_time"]
			# BSS_sensor_disable = row["w_sensor_disable"]
			BSS_sensor_stop = row["w_sensor_stop"] #
			BSS_sensor_reload = row["w_sensor_reload"] #
			# BSS_event_pickTime = row["w_event_pickTime"]
			BSS_event_holdTime = row["w_event_holdTime"] # 
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
			BSS_keycode = row["w_keycode"]
			BSS_stamp = row["w_stamp"] #

		try: # GPIO 포트 초기화
			GPIO.setwarnings(False) # to disable warnings
			GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
			GPIO.setup(BSS_alert_Port, GPIO.OUT)
			GPIO.output(BSS_alert_Port, GPIO.HIGH)
		except:
			pass
		
		BUFSIZ = 1024
		preEventDist = 0
		preEventLevel = 0
				
		if commndFlag: # 사용자 요청
			statusInfo = "User Command"
		else:
			statusInfo = "System Command"
		# 시작정보 로그입력
		insert_event_log_BSS(mySensorID, w_cfg_id=1, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat=statusInfo, w_event_desc='Start Program', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
		
		try:
			tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
			tcpSerSock.bind((BSS_virtual_Addr, BSS_virtual_Port)) # <------- 소켓을 주소로 바인딩
			tcpSerSock.listen(2) # <------ listening 시작. 최대 클라이언트 (연결 수)
			tcpSerSock.settimeout(2) #  <------- 타임아웃 에러 (초)
			logger.info("Connected and Listen IP:%s PORT:%s" % (BSS_virtual_Addr, BSS_virtual_Port))
						
			if commndFlag: # 사용자 요청
				logger.info('Re-Created Server Socket')
			else:
				logger.info('Created Server Socket')
			try:
				tcpCliSock, addr = tcpSerSock.accept()
				tcpCliSock.settimeout(ERROR_recv_timeout)
				if commndFlag: # 사용자 요청
					logger.info('Re-Connected Client Socket')
				else:
					logger.info('Connected Client Socket')

				while True:
					if addr[0] != BSS_sensor_Addr: # 약속된 센서 아이피만 수용한다.
						logger.critical('Error Unmatched Sensor\'s IP. WITS Wait From %s. Please Check Config Table.' % BSS_sensor_Addr)
						logger.critical('Or Please Check Sensor\'s IP %s.' % addr[0])
						continue # 조건에 맞지 않는 경우 맨 처음으로 돌아가기

					try:
						data = tcpCliSock.recv(BUFSIZ)
					except:
						errorCntCreate = 0
						errorCntConnect = 0
						eventHeartBit = 0
						errorCntRecv += 1
						tcpCliSock.close()
						if (errorCntRecv % ERROR_socketRecv_cnt) == 0: # 5번 이상 오류가 발생 한경우
							logger.critical('Error Receiving Event. Please Check Connecting Condition. # %s' % errorCntRecv)
						else:
							if commndFlag: # 사용자 요청
								logger.info('Waiting ...')
							else:
								logger.critical('Error Receiving Timeout. Close Socket And Retry Connect. # %s' % errorCntRecv)
						# 매우 심각한 오류 발생시
						if BSS_host_Addr and BSS_host_Port: # 호스트정보가 있으면 정보 전송
							tmp_subject = BSS_subject + " >>> Error Receiving Event. Please Check Connecting Condition"
							insert_socket_alert_BSS(BSS_sensor_serial, tmp_subject, BSS_host_Addr, BSS_host_Port)
							if BSS_host_Addr2 and BSS_host_Port2: # 호스트정보가 있으면 정보 전송
								insert_socket_alert_BSS(BSS_sensor_serial, tmp_subject, BSS_host_Addr2, BSS_host_Port2)
						raise
					else:
						##################################################################################
						if BSS_sensor_stop: # 일시 정지 - 모든 이벤트를 Idle 로 바꾼다.
							data = ''
						if len(data) > 16: # 하트비트를 포함한 이밴트 데이터 
							eventData = data[16:] # 하트비트 이후의 자료 저장
							typeOfBlock = blockType(eventData) # 명령문 해석 ex: e0는 거리데이터, e1은 센서 설정갑 변동 응답(?)
							sizeOfBlock = blockSize(eventData)
							if BSS_alarm_disable: 
								print "typeOfBlock, sizeOfBlock"
								print typeOfBlock, sizeOfBlock
							if typeOfBlock == 'e0': # 거리 데이터
								if sizeOfBlock == 16: # 거리 데이터 이며 거리정보가 존재 하면 
									distData = eventData[4:]
									##### 순수한 이벤트 정보(거리, 속도, 감도, 릴레이 상태 및 센서 정보) ##########################
									if len(distData) == 16:
										notChangedVaildEventCnt += 1
										notChangedAllEventCnt += 1
										eventHeartBit = 0
										
										tmp_cfg_id = 0
										tmp_slaveID = slaveID(distData)
										tmp_deviceID = deviceID(distData) # 센서아이디
										# tmp_distant = "{0:>8}m".format(round(float(distant(distData))/1000, 3)) # 소수점 3자리 mm 으로 표시
										tmp_distant = distant(distData) # 거리, 소수점 3자리 mm 으로 표시
										if BSS_alarm_disable: 
											print "tmp_slaveID, tmp_deviceID, tmp_distant"
											print tmp_slaveID, tmp_deviceID, tmp_distant
										
										if tmp_distant:
											if BSS_sensor_offset: # 시작점에서 센서위치와 감지할 시점의 거리 - 사전에 상쇄할 
												offset = BSS_sensor_offset * 10 # 오프셋값 센치미터를 미리미터로 변환
												if tmp_distant > offset:
													tmp_distant = tmp_distant - offset
												else: # 오프셋값 보다 작은거리값이면 
													tmp_distant = 1 # 음수인경우 시작위치라고 가정함
													
											# 이전 거리와 비교 1m = 1000 MAX_event_syncDist이내는 동일거리로 간주
											spot_offset = BSS_sensor_spot * 10 # 범주 오프셋값 센치미터를 미리미터로 변환
											if abs(preEventDist - tmp_distant) < spot_offset: # MAX_event_syncDist: 
												tmp_delta = 1 #  허용범주내의 유효 데이터 
												# print spot_offset
											else:
												tmp_delta = 0
												# 허용범주를 넘은 값은 무효 데이터 
												notChangedAllEventCnt = 0
											
											# 거리값에 오프셋값을 적용 이동거리와 속도 방향을 계산을 위한 값 저장한다.
											if notChangedAllEventCnt == 1: # 최초발생 이벤트 이면
												startEventDist = tmp_distant
												startEventTime = datetime.datetime.now()
											else: # 연소발생 이벤트 이면
												stopEventDist = tmp_distant
												stopEventTime = datetime.datetime.now()
										else: # 대항형이면
											notChangedAllEventCnt = 0
											tmp_delta = 0
											
										tmp_errorCode = errorCode(distData) # 오류코드
										tmp_peaklevel = peakLevel(distData) # 이벤트레벨
										tmp_alarmOut = alarmOut(distData) # 알람상태
										tmp_sensorType = sensorType(distData) # 센서타입
										tmp_speed = speed(distData) # 속도
										tmp_cnt = notChangedVaildEventCnt
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
										tmp_cntError = 0
										
										if BSS_alarm_disable: 
											print "tmp_errorCode, tmp_peaklevel, tmp_alarmOut, tmp_speed, tmp_cnt"
											print tmp_errorCode, tmp_peaklevel, tmp_alarmOut, tmp_speed, tmp_cnt

										# # 이전 거리와 비교 1m = 1000 MAX_event_syncDist이내는 동일거리로 간주
										# if abs(preEventDist - tmp_distant) < MAX_event_syncDist: 
											# tmp_delta = 1 #  허용범주내의 유효 데이터 
										# else:
											# tmp_delta = 0
										if tmp_sensorType: #### 자립형 #########################################
											new_coord = get_current_location_BSS(BSS_sensor_lat_s, BSS_sensor_lng_s, BSS_sensor_lat_e, BSS_sensor_lng_e, tmp_distant, BSS_sensor_stepOfZone, BSS_sensor_noOfZone)
											tmp_lat_s = new_coord[0]
											tmp_lng_s = new_coord[1]
											tmp_lat_e = new_coord[2]
											tmp_lng_e = new_coord[3]
											tmp_zone = int(new_coord[4])
										else:
											tmp_lat_s = BSS_sensor_lat_s
											tmp_lng_s = BSS_sensor_lng_s
											tmp_lat_e = BSS_sensor_lat_e
											tmp_lng_e = BSS_sensor_lng_e
											tmp_zone = 0
											
										if BSS_alarm_disable: 
											print "tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, tmp_zone"
											print tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, tmp_zone
										
										############ 조건에 따른 관제 알람 ###########################
										# print tmp_distant, "=", BSS_sensor_ignoreS, " ", BSS_sensor_ignoreE, " ",BSS_sensor_ignoreZone, " ",BSS_sensor_stepOfZone
										# print BSS_sensor_sensor_week
										if tmp_sensorType: #### 자립형 #########################################
											if BSS_alarm_disable: print "YES-isAreaType" #
											# 거리 값이 0인지 확인
											if tmp_distant > 0: # 거리정보 값이 있으면
												if BSS_alarm_disable: print "YES-isVaildDist - ", tmp_distant # \a 비프음 출력
												# 자립형에서 100미터가 넘는 거리이면
												tmp_overDist = overDist(tmp_distant)
											else: # 거리정보 값이 0 이면
												if BSS_alarm_disable: print "NO-isVaildDist"
												tmp_zeroDist += 1 # tmp_zeroDist 값은 자립형만 적용된다.
											
											# 감지 및 비감지 지역인지 확인
											if isItNormalDate(): # 예약일인지 확인
												if BSS_alarm_disable: print "YES-isItNormalDate"
												if isVaildZone(tmp_distant, BSS_sensor_ignoreS, BSS_sensor_ignoreE, BSS_sensor_ignoreZone, BSS_sensor_stepOfZone): # 감지허용 지역이면 
													if BSS_alarm_disable: print "YES-isVaildZone"
												else: # 감지무시 지역이면 
													if BSS_alarm_disable: print "NO-isVaildZone"
													tmp_ignore += 1
											else: # 예약일인 경우 예약지역을 확인 한다.
												if BSS_alarm_disable: print "YES-isItScheduledDate"
												if isVaildZoneSchedule(tmp_distant, BSS_sensor_scheduleS, BSS_sensor_scheduleE, BSS_sensor_scheduleZone, BSS_sensor_stepOfZone): # 감지허용 지역이면 
													if BSS_alarm_disable: print "YES-isVaildZone"
												else: # 감지무시 지역이면 
													if BSS_alarm_disable: print "NO-isVaildZone"
													tmp_ignore += 1
												tmp_schedule += 1
										#### 자립형 #########################################
										
										else: #### 대항형 ##############################
											if BSS_alarm_disable: print "YES-isLineType" # 거리 및 감지지역을 모두 수용한다.
											if isItNormalDate(): # 예약일인지 확인
												if BSS_alarm_disable: print "YES-isItNormalDate"
											else:
												if BSS_alarm_disable: print "YES-isItScheduledDate"
												tmp_schedule += 1
												# tmp_ignore += 1 # 대항형은 제한구역의 의미가 없다.
										#### 대항형 #########################################
										
										# 감지감도의 허용기준 확인
										# if tmp_peaklevel > 0: # 감지감도가 기준감도 보다 크거나 같으면
											# if BSS_alarm_disable: print "YES-isVaildLevel"
										# else: # 감지감도가 기준감도 보다 작으면
											# if BSS_alarm_disable: print "NO-isVaildLevel"
											# tmp_outLevel += 1
											
										# 감지감도의 허용기준 확인
										if isVaildLevel(tmp_peaklevel): # 감지감도가 기준감도 보다 크거나 같으면
											if BSS_alarm_disable: print "YES-isVaildLevel"
										else: # 감지감도가 기준감도 보다 작으면
											if BSS_alarm_disable: print "NO-isVaildLevel"
											tmp_outLevel += 1
										
										# 유효한 이밴트 이면
										if tmp_zeroDist == 0 and tmp_ignore == 0 and tmp_outLevel == 0: # 거리가 있고 그 거리가 허용 지역이며 허용레벨이면 
											if BSS_alarm_disable: print "YES-isVaildEVENT"
										else:
											if BSS_alarm_disable: print "NO-isVaildEVENT"
											notChangedVaildEventCnt = 0
											tmp_cnt = 0

										# 현재거리 및 감도가 이전과 다르면. notChangedAllEventCnt > MAX_event_allowSameCount
										# if not preEventDist == tmp_distant and not preEventLevel == tmp_peaklevel:
										if tmp_delta: #  and not preEventLevel == tmp_peaklevel: # 현재거리와 이전거리가 다르며 
											# notChangedAllEventCnt += 1
											if notChangedAllEventCnt > MAX_event_allowSameCount and tmp_zeroDist: # tmp_zeroDist 값은 자립형만 적용된다.
												tmp_cntError += 1
										else: # 거리가 않변한경우 그 연속성이 특정 한계(MAX_event_allowSameCount = 128)를 넘으면 오류를 발생 시킨다.
											# notChangedAllEventCnt = 0
											if BSS_event_syncDist: # 동일거리 동기 설정이면
												tmp_cnt = 0
												notChangedVaildEventCnt = tmp_cnt
												
										# 유효한 이벤트의 연속횟수가 요구(Hold) 조건을 만족 하는지 확인
										tmp_cnt_save = tmp_cnt
										if tmp_cnt < BSS_event_holdTime:
											if BSS_alarm_disable: print "NO-isVaildCount"
										else:
											##### 모든 조건이 만족한 상태 #########################
											if BSS_alarm_disable: print "YES-isVaildCount"
											# 동일거리고정 값만 허용하는 기준
											if BSS_event_syncDist: # 거리 동기 설정값 확인
												# if preEventDist == tmp_distant: # 동일한 거리및 레벨이 연속적이면 and preEventLevel == tmp_peaklevel:
												if tmp_delta: # 동일한 거리및 레벨이 연속적이면 and preEventLevel == tmp_peaklevel:
													tmp_sent += 1 # 알람을 호스트에 전송
													tmp_shot += 1 # 검증샷 확인
													tmp_outCount += 1 # 전송및 검증샷 확인
												else:
													tmp_cnt = 0
											else: # 거리가 연속적이지 아니어도 거리및 레벨이 허용값 이면
												tmp_sent += 1 # 알람을 호스트에 전송
												tmp_shot += 1 # 검증샷 확인
												tmp_outCount += 1 # 전송및 검증샷 확인
												
											# 허용회수 리셋, 아니면 최초 허용회수 이후 이밴트를 지속적으로 발생 한다
											if BSS_event_keepHole: # 기준값이상이면 무조건 출력됨을 막기 위해 반복되는 조건을 위해 리셋
												notChangedVaildEventCnt = 0
												tmp_cnt = 0
												##### 모든 조건이 만족한 상태 #########################
										
										# if BSS_alarm_disable: # 알람이 차단된 디버그 모드이면 원 데이터와 시간 출력
											# print "slaveID:", tmp_slaveID, "deviceID:", tmp_deviceID, "distant:", tmp_distant, "status:", tmp_errorCode, "peaklevel:",tmp_peaklevel, "alarmOut:", tmp_alarmOut, "type:", tmp_sensorType, "speed:", tmp_speed, "count:", tmp_cnt
											
										# # tmp_overDist 값이 양수이면 자립형이며 거리가 100미터를 넘는 값이며 감도 레벨이 1 이상이란 의미
										# # 값에 따라 다른 조건은 나중에 보완 한다.
										# # 사전의 조건을 다 무시 한다.
										# if tmp_overDist and tmp_ignore == 0:
											# if tmp_cnt % tmp_overDist == 0: # 현재의 카운터와 오버카운트 허용수가 같거나 배수이면 출력
												# tmp_sent += 1 # 알람을 호스트에 전송
												# tmp_shot += 1 # 검증샷 확인
												# tmp_outCount += 1 # 전송및 검증샷 확인
												
												# notChangedVaildEventCnt = 0
												# tmp_cnt = 0
												
												# if BSS_alarm_disable: print "YES-isOverDistent"
										
										##############################
										# 이벤트 전송및 스넵샷
										##############################
										if tmp_cntError: # 센서의 설정상에 문제 가능성이 매우 높다. 동일한 신호가 최대횟수(MAX_event_allowSameCount)를 넘은 경우 발생 한다.
											tmp_error += 1
											tmp_stat = "Overflow Count."
											tmp_desc = "Reboot System"
											logger.warning("Wits Will Reboot.")
											insert_event_log_BSS(mySensorID, w_cfg_id=2, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=1, w_event_stat=tmp_stat, w_event_desc=tmp_desc, w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=notChangedAllEventCnt, w_opt_4='', w_opt_5='')

											reboot_wits() # send mail to manager
										else:											
											# 스넵삿
											if tmp_shot and not BSS_alarm_disable:
												if BSS_url: # 스넵삿이 가능한 BSS_url 값이 있으면 
													tmp_desc = getSnapshot(BSS_url)
													tmp_desc = "<a href=%s target=_blank>Snapshot</a>" % tmp_desc[21:] # 머리부분 /var/www/html을 제거
												else:
													tmp_desc = "Need Snapshot URL."
													logger.warning("Need Host IP And Port Infomation.")
													tmp_error += 1
												
											# 관제시스템에 이벤트 로그를 전송
											if tmp_sent and not BSS_alarm_disable: 
												# 거리값에 오프셋값을 적용 이동거리와 속도 방향을 계산을 위한 값
												obj_length = stopEventDist - startEventDist
												diff = stopEventTime - startEventTime
												obj_time = diff.total_seconds()
												obj_speed = abs((obj_length / 1000000) / (obj_time / 3600))
												if obj_length > 0:
													obj_move = "Out"
												elif obj_length < 0:
													obj_move = "In"
												else:
													obj_move = "Standing"
												
												obj_level = tmp_peaklevel
												
												# logger.info("<<< Cnt:%s Start:%sm Stop:%sm %s >>>" % (notChangedAllEventCnt, round((startEventDist/1000),2), round((stopEventDist/1000),2), tmp_stat))
												# 관제시스템에 이벤트 로그를 전송 한다.
												if BSS_host_Addr and BSS_host_Port: # 호스트정보가 있으면 정보 전송
													returnValue = insert_socket_log_BSS_OBJ(BSS_sensor_serial, BSS_subject, '%.20f' % tmp_lat_s, '%.20f' % tmp_lng_s, '%.20f' % tmp_lat_e, '%.20f' % tmp_lng_e, BSS_sensor_face, BSS_host_Addr, BSS_host_Port, tmp_distant, tmp_zone, obj_length, obj_time, obj_speed, obj_move, obj_level)
													if BSS_host_Addr2 and BSS_host_Port2: # 호스트정보가 있으면 정보 전송
														returnValue2 = insert_socket_log_BSS_OBJ(BSS_sensor_serial, BSS_subject, '%.20f' % tmp_lat_s, '%.20f' % tmp_lng_s, '%.20f' % tmp_lat_e, '%.20f' % tmp_lng_e, BSS_sensor_face, BSS_host_Addr2, BSS_host_Port2, tmp_distant, tmp_zone, obj_length, obj_time, obj_speed, obj_move, obj_level)
												else:
													tmp_stat = "Need Host Info."
													logger.warning("Need Host IP And Port Infomation.")
													tmp_error += 1
												
												# 실시간 관제 서비스를 위한 이벤트 전송
												# table_BSS.js와 연동되어 움직인다.
												if BSS_system_ip: # 												
													# node.js로 실시간 GUI관제 서비스를 위해 위트 IP(BSS_system_ip)와 port 8000 으로 강제 촐력
													returnValue = insert_socket_monitor_BSS_OBJ(BSS_sensor_serial, BSS_subject, tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, BSS_system_ip, BSS_table_PortIn, tmp_distant, tmp_alarmOut, tmp_sensorType, tmp_zone, obj_length, obj_time, obj_speed, obj_move, obj_level)
												# else: # 거리와 위치를 -1 값으로 한후 릴레이 값만 전송 한다.
													# insert_socket_monitor_BSS(BSS_sensor_serial, BSS_subject, tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, BSS_system_ip, BSS_table_PortIn, -1, tmp_alarmOut, tmp_sensorType, -1)

												# 알람 발생
												if BSS_alert_Port and BSS_alert_Value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( BSS_alert_Value:)
													Process(target=alertOut, args=(BSS_alert_Port,BSS_alert_Value)).start()

												# 데이터베이스에 계산된 사물의 속도를 저장한다.
												tmp_speed = obj_speed
												tmp_stat = "Speed:%skm Length:%sm Time:%ssec Move:%s " % (round(obj_speed,2), round((obj_length/1000),2), round(obj_time,2), obj_move)
												
										# 임시 상태값 출력
										if BSS_alarm_disable: 
											print "slvID:", tmp_slaveID, "devID:", tmp_deviceID, "dist:", tmp_distant, "stat:", tmp_errorCode, "peaklv:",tmp_peaklevel, "alarmOut:", tmp_alarmOut, "type:", tmp_sensorType, "speed:", tmp_speed, "tmpCnt:", tmp_cnt_save, "zeroDist:", tmp_zeroDist, "outLv:", tmp_outLevel, "outCnt:", tmp_outCount, "ignore:", tmp_ignore, "schedule:",tmp_schedule, "sent:", tmp_sent, "shot:", tmp_shot, "error:", tmp_error, "cntErr:", tmp_cntError, "allEvCnt:", notChangedAllEventCnt, "vaildEvtCnt:", notChangedVaildEventCnt, "\n------------ End of Event ------------"
										
										##############################
										# 이벤트 데이터베이스 업데이트
										##############################
										# try:
										if tmp_outCount: # 유효한 이벤트만 데이터베이스에 등록
											if tmp_schedule:
												status=Event_type['block']
												msg=Event_desc[status]
											else:	
												status=Event_type['active']
												msg=Event_desc[status]
												
											# table_union.js와 연동되어 움직인다.
											insert_socket_status_UNION(BSS_sensor_serial, BSS_subject, BSS_system_ip, BSS_system_port, model=BSS_sensor_model, board=ECOS_table_BSS_R, tableID=myTableID, status=status, msg=msg)  # 소켓 유니온 전송
											
											tableID = insert_event_log_BSS(mySensorID, w_cfg_id=tmp_cfg_id, w_bss_slave=tmp_slaveID, w_bss_device=tmp_deviceID, w_bss_distent=tmp_distant, w_bss_error=tmp_errorCode, w_bss_level=tmp_peaklevel, w_bss_alarm=tmp_alarmOut, w_bss_type=tmp_sensorType, w_bss_speed=tmp_speed, w_event_cnt=tmp_cnt_save, w_event_zeroDist=tmp_zeroDist, w_event_outLevel=tmp_outLevel, w_event_outCount=tmp_outCount, w_event_ignore=tmp_ignore, w_event_schedule=tmp_schedule, w_event_sent=tmp_sent, w_event_shot=tmp_shot, w_event_error=tmp_error, w_event_stat=tmp_stat, w_event_desc=tmp_desc, w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=notChangedAllEventCnt, w_opt_4='', w_opt_5='') # 반환값은 성공시 데이터베이스 인댁스 ID	
										else:
											tableID = 0
										# except:
											# logger.critical('Error @ database update - insert_event_log_BSS')
										##############################
										# 이벤트 로그파일 업데이트
										##############################
										logger.info("slvID:%s devID:%s dist:%8s stat:%s level:%s alarm:%s type:%s speed:%s cnt:%s schedule:%s sent:%s shot:%s ignore:%s zone:%s notChanged:%s tblID %s" % (tmp_slaveID,tmp_deviceID,tmp_distant,tmp_errorCode,tmp_peaklevel,tmp_alarmOut,tmp_sensorType,tmp_speed,tmp_cnt_save,tmp_schedule,tmp_sent,tmp_shot,tmp_ignore,tmp_zone,notChangedAllEventCnt,tableID)) # 로그출력
										if tmp_sent: logger.info("<<< ID:%s %s Start:%sm Stop:%sm>>>" % (tableID, tmp_stat, round((startEventDist/1000),2), round((stopEventDist/1000),2)))
										
										# 이전 이벤트와 비교를 위한 임시 저장
										preEventDist = tmp_distant
										preEventTime = datetime.datetime.now()
										preEventLevel = tmp_peaklevel

										############ 조건에 따른 관제 알람 ###########################
									else: # 오류
										logger.info("Recv. Data But No Dist. Info -> %s" % all(distData)) # 거리정보가 없음
										# 기존 필타링 값을 리셋
										notChangedVaildEventCnt = 0
										notChangedAllEventCnt = 0

									##### 순수한 이벤트 정보(거리, 속도, 감도, 릴레이 상태 및 센서 정보) ##########################
								else: # 오류
									logger.info("No Data Info -> if sizeOfBlock == 16:")
							elif typeOfBlock == 'e1': # 설정 확인
								logger.info("Updated Sensor Parameter From [Parameter Setting Tools]")
								insert_event_log_BSS(mySensorID, w_cfg_id=6, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='Setup Tools', w_event_desc='Updated Sensor Parameter', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
							else:
								logger.info("Unknow Event data")
						else: # 하트비트
							##### idle ######################
							# 사용자 요청 확인 및 적용
							eventHeartBit += 1
							notChangedVaildEventCnt = 0
							commndFlag = 0 # 메세지 출력시 사용자 요청에 의함인지 확인
							
							# 실시간 관제 서비스를 위한 이벤트 전송
							if BSS_host_Addr and BSS_host_Port: # 호스트정보가 있으면 정보 전송
								insert_socket_log_BSS(BSS_sensor_serial, BSS_subject, -1, -1, -1, -1, -1, BSS_host_Addr, BSS_host_Port, -1, -1)
							if BSS_host_Addr2 and BSS_host_Port2: # 호스트정보가 있으면 정보 전송
								insert_socket_log_BSS(BSS_sensor_serial, BSS_subject, -1, -1, -1, -1, -1, BSS_host_Addr2, BSS_host_Port2, -1, -1)
							# table_BSS.js와 연동되어 움직인다.
							insert_socket_monitor_BSS(BSS_sensor_serial, BSS_subject, 0, 0, 0, 0, BSS_system_ip, BSS_table_PortIn, -1, -1, -1, -1)
							# table_union.js와 연동되어 움직인다.
							insert_socket_status_UNION(BSS_sensor_serial, BSS_subject, BSS_system_ip, BSS_system_port, model=BSS_sensor_model, board=ECOS_table_BSS_R, tableID=myTableID, status=Event_type['idle'], msg=Event_desc[Event_type['idle']])  # 소켓 유니온 전송

							# 실시간 설정 변동 값을 휴간상황때 데이터베이스 접속 확인
							for row in read_field_w_cfg_status_BSS(myTableID):
								BSS_sensor_stop = row["w_sensor_stop"]		# `w_sensor_stop` TINYINT(1) - 일시정지
								BSS_sensor_reload = row["w_sensor_reload"] 	# `w_sensor_reload` TINYINT(1) - 재시동
								BSS_alarm_disable = row["w_alarm_disable"]	# `w_alarm_disable` TINYINT(1) -알람중지
							
							if BSS_alarm_disable: # 알람이 차단된 경우 디버그 모드로 원 데이터와 시간 출력
								print " stop:", BSS_sensor_stop, " reload:", BSS_sensor_reload, " alarm:", BSS_alarm_disable, " hold:", BSS_event_holdTime, " count:", eventHeartBit,  " data len:", len(data)," data contents:", all(data)
								
							if (eventHeartBit % BSS_event_holdTime) == 0: # 센서가 살아있음을 알림 - 대략 10초 * BSS_event_holdTime
								logger.info('Idle #: %s' % (eventHeartBit))
								
							if BSS_sensor_reload: # 재시동, 
								commndFlag = 1
								logger.info('Reload Program.')
								set_reload_w_cfg_reload_BSS(myTableID) # 재시동 필드를 회복시킨다.
								insert_event_log_BSS(mySensorID, w_cfg_id=3, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=0, w_event_stat='User Request', w_event_desc='Reload Program', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
								
								tcpSerSock.shutdown(socket.SHUT_RDWR) # 소켓 셧다운 - 재 생성시 오류를 막기 위함
								tcpCliSock.close() # 오류를 발생시킴으로 재 실행을 유도 한다.
							##### idle ######################
						##################################################################################
			except:
				status=Event_type['error']
				msg=Event_desc[status]
				# table_union.js와 연동되어 움직인다.
				insert_socket_status_UNION(BSS_sensor_serial, BSS_subject, BSS_system_ip, BSS_system_port, model=BSS_sensor_model, board=ECOS_table_BSS_R, tableID=myTableID, status=status, msg=msg)  # 소켓 유니온 전송
				errorCntConnect += 1
				if BSS_alarm_disable:
					print('Error#(%s) At After Socket Bind:IP(%s) Port(%s). Please Check 1)Cable Langth And Connector Or Wiring. 2)Data Signal Level.' % (errorCntConnect, BSS_virtual_Addr, BSS_virtual_Port))
					
				tcpCliSock.shutdown(socket.SHUT_RDWR) # 소켓 셧다운 - 재 생성시 오류를 막기 위함
				tcpCliSock.close() # 오류를 발생시킴으로 재 실행을 유도 한다.

				if errorCntConnect > ERROR_connect_cnt: # 오류 허용 한계를 넘으면 
					logger.critical('Error#(%s) At After Socket Bind:IP(%s) Port(%s). Please Check 1)Cable Langth And Connector Or Wiring. 2)Data Signal Level.' % (errorCntConnect, BSS_virtual_Addr, BSS_virtual_Port))
					# exit(1) # send mail to manager
					insert_event_log_BSS(mySensorID, w_cfg_id=2, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=1, w_event_stat='Over Count of Socket Bind', w_event_desc='Reboot System', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
					reboot_wits() # send mail to manager
				else:
					logger.critical('Error Connect # %s' % errorCntConnect)
				time.sleep(ERROR_sleep_cnt) # delays for 2 seconds
		except:
			status=Event_type['error']
			msg=Event_desc[status]
			# table_union.js와 연동되어 움직인다.
			insert_socket_status_UNION(BSS_sensor_serial, BSS_subject, BSS_system_ip, BSS_system_port, model=BSS_sensor_model, board=ECOS_table_BSS_R, tableID=myTableID, status=status, msg=msg)  # 소켓 유니온 전송
			errorCntCreate += 1
			if BSS_alarm_disable:
				print('Error#(%s) At Creating Socket. Please Check Socket IP(%s) Address And Port(%s) Number' % (errorCntCreate, BSS_virtual_Addr, BSS_virtual_Port))
					
			tcpSerSock.close() # 오류를 발생시킴으로 재 실행을 유도 한다.

			if errorCntCreate > ERROR_socket_cnt: # 오류 허용 한계를 넘으면
				logger.critical('Error#(%s) At Creating Socket. Please Check Socket IP(%s) Address And Port(%s) Number' % (errorCntCreate, BSS_virtual_Addr, BSS_virtual_Port))
				insert_event_log_BSS(mySensorID, w_cfg_id=2, w_bss_slave='-', w_bss_device=BSS_sensor_model, w_bss_distent=0, w_bss_error=0, w_bss_level=0, w_bss_alarm='-', w_bss_type='-', w_bss_speed=0, w_event_cnt=0, w_event_zeroDist=0, w_event_outLevel=0, w_event_outCount=0, w_event_ignore=0, w_event_schedule=0, w_event_sent=0, w_event_shot=0, w_event_error=1, w_event_stat='Over Count of Creating Socket', w_event_desc='Reboot System', w_opt_0=0, w_opt_1=0, w_opt_2=0, w_opt_3=0, w_opt_4='', w_opt_5='')
				# restart_BSS() # send mail to manager
				reboot_wits() # send mail to manager
			else:
				logger.critical('Error Creating Socket # %s' % errorCntCreate)
			time.sleep(ERROR_sleep_cnt) # delays for 2 seconds

			