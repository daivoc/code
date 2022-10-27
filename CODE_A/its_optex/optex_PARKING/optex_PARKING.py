#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from config_db import *
from config_sensor import *
from module_for_optex import *
from module_for_mysql import *

##### 데이터 검증 ##################################
def isItScheduleDate(): # 주단위 예약이 우선이다.
	weekNo = datetime.datetime.today().weekday() # 현재의 주일번호 확인 Monday is 0 and Sunday is 6.
	# print db_sensor_sensor_week, weekNo # 예 : 6,1,2,4,5
	if str(weekNo) in db_sensor_sensor_week: # db_sensor_sensor_week를 어레이로 변환후 오늘의 주번호와 일치하는지 확인
		isScWeek = check_scheduledWeek(myTableID, weekNo) # 주간 예약인지 확인
		if isScWeek['cnt'] > 0:
			# print isScWeek, "isScWeek"
			return 2 # 지금은 주간 예약된 일시 입니다.
			
	# 현재날짜와 시간이 예약된 날자인지 확인(일치하는 필드 갯수)한다.
	isScDate = check_scheduledDate(myTableID)
	if isScDate['cnt'] > 0:
		# print isScDate, "isScDate"
		return 1 # 지금은 일간 예약된 일시 입니다.
	else:
		return 0 # 예약 안된 일시 입니다.

def lsIgnoreZone(zone, w_event_schedule):
	# print zone, w_event_schedule, db_sensor_scheduleZone, db_sensor_ignoreZone
	if not zone: return 0 # 지역 정보가 없으면 무시 한다.
	
	if w_event_schedule: # 1:일간예약, 2:주간예약
		zones = db_sensor_scheduleZone.rstrip(',') # 
	else: # 예약 정보가 없으면 기존 무시지역을 적용한다.
		zones = db_sensor_ignoreZone.rstrip(',')
	if not zones: return 0 # 지역 정보가 없으면 무시 한다.
	
	ignoreZone = zones.split(',')
	# print ignoreZone
	for i in ignoreZone: # 
		j = RLS_map_LA[zone]
		if j and float(j) == float(i):
			# print float(j), ignoreZone, zone, "is Blocked"
			return 1 # 차단된 지역
	return 0 # 적용사항 없음

def getAlarmSet(w_rls_ma,w_rls_la,w_rls_ca,w_rls_cc,w_rls_dq,w_rls_ar,w_rls_am,w_rls_tr,w_rls_so,w_rls_ta,tmp_ignore):
	getAlarmSet = ''
	if w_rls_ma == 'MO':
		getAlarmSet += '1' 
	else:
		getAlarmSet += '0' 
	if len(w_rls_la) == 3: 
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_ca == '':
		getAlarmSet += '1' 
	else:
		getAlarmSet += '0' 
	if w_rls_cc == 'CC':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_dq == 'DQ':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_ar == 'AR':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_am == 'AM':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_tr == 'TR':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_so == 'SO':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_ta == 'TA':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if w_rls_ta == 'DM':
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
	if tmp_ignore:
		getAlarmSet += '1' 
	else: 
		getAlarmSet += '0' 
		
	return getAlarmSet
	
def getEventStatus(db_sensor_face, curEVT, preEVT): # 현재 센서의 위치 파악
	if db_sensor_face: # 0 => 'Side In', 1 => 'Side Out'
		curTYPE = Type_event_out[curEVT]
		preTYPE = Type_event_out[preEVT]
	else:
		curTYPE = Type_event_in[curEVT]
		preTYPE = Type_event_in[preEVT]

	if (curTYPE - preTYPE) > 0: return 0 # 음수는 접근 양수는 후퇴
	
	return curTYPE


def getSnapshot(w_url1): 
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
	# tmpName = time.strftime('%M_%S-URL_01') + ".jpg"
	millis = int(round(time.time() * 100))
	# tmpName = time.strftime('%M_%S_') + str(millis) + ".jpg" # '%d/%m/%y %H:%M:%S.%f'
	tmpName = time.strftime('%M_%S_') + str(millis) + ".jpg" # '%d/%m/%y %H:%M:%S.%f'
	
	thisImgName = tmpFullPath + tmpName
	run_wget_image(w_url1, thisImgName) # Ontime Screenshot
	return thisImgName

##### 데이터 검증 ##################################
	
if __name__ == '__main__':

	myTableID = sys.argv[1]
	
	for row in read_field_w_cfg_serial(myTableID): # 로깅을 위한 파일명으로 사용할 시리얼 번호를 가지고 온다.
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
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
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

	############ Table ################
	# 테이블 생성
	returnMsg = create_table_w_log_RLS(mySensorID) # 테이블 생성 - 반환값
		
	# 테이블 읽기
	w_cfg_sensor_list_All = read_table_w_cfg_sensor_all(myTableID)
	for row in w_cfg_sensor_list_All:
		db_subject = row["wr_subject"]
		# db_id = row["w_id"]
		# db_cpu_id = row["w_cpu_id"]
		# db_license = row["w_license"]
		# db_device_id = row["w_device_id"]
		
		db_sensor_serial = row["w_sensor_serial"] #
		db_sensor_model = row["w_sensor_model"]
		db_sensor_face = row["w_sensor_face"] # 0 => 'Side In', 1 => 'Side Out'
		
		# db_sensor_angle = row["w_sensor_angle"]
		
		db_sensor_lat_s = row["w_sensor_lat_s"]
		db_sensor_lng_s = row["w_sensor_lng_s"]
		db_sensor_lat_e = row["w_sensor_lat_e"]
		db_sensor_lng_e = row["w_sensor_lng_e"]
		
		# db_sensor_ignoreS = row["w_sensor_ignoreS"] #
		# db_sensor_ignoreE = row["w_sensor_ignoreE"] #
		# db_sensor_noOfZone = row["w_sensor_noOfZone"] #
		# db_sensor_stepOfZone = row["w_sensor_stepOfZone"] # 
		# db_sensor_offset = row["w_sensor_offset"] #
		
		db_sensor_ignoreZone = row["w_sensor_ignoreZone"] #
		
		# db_sensor_scheduleS = row["w_sensor_scheduleS"]
		# db_sensor_scheduleE = row["w_sensor_scheduleE"]
		
		db_sensor_scheduleZone = row["w_sensor_scheduleZone"]
		db_sensor_sensor_week = row["w_sensor_week"]
		
		# db_sensor_sensor_time = row["w_sensor_time"]
		# db_sensor_disable = row["w_sensor_disable"]
		# db_sensor_stop = row["w_sensor_stop"] #
		db_sensor_reload = row["w_sensor_reload"] #
		# db_event_pickTime = row["w_event_pickTime"]
		# db_event_holdTime = row["w_event_holdTime"] # 
		# db_event_keepHole = row["w_event_keepHole"] #
		db_event_syncDist = row["w_event_syncDist"] #
		db_alarm_disable = row["w_alarm_disable"] #
		# db_alarm_level = row["w_alarm_level"] #
		db_system_ip = row["w_system_ip"]
		db_system_port = row["w_system_port"]
		
		# db_systemBF_ip = row["w_systemBF_ip"]
		# db_systemBF_port = row["w_systemBF_port"]
		# db_systemAF_ip = row["w_systemAF_ip"]
		# db_systemAF_port = row["w_systemAF_port"]
		# db_master_Addr = row["w_master_Addr"]
		# db_master_Port = row["w_master_Port"]
		
		db_virtual_Addr = row["w_virtual_Addr"] #
		db_virtual_Port = row["w_virtual_Port"] #
		db_sensor_Addr = row["w_sensor_Addr"] #
		db_sensor_Port = row["w_sensor_Port"]
		db_sensor_Addr2 = row["w_sensor_Addr2"] #
		db_sensor_Port2 = row["w_sensor_Port2"]
		
		db_email_Addr = row["w_email_Addr"]
		db_email_Time = row["w_email_Time"]
		
		db_table_PortIn = row["w_table_PortIn"]
		db_table_PortOut = row["w_table_PortOut"]
		db_host_Addr = row["w_host_Addr"]
		db_host_Port = row["w_host_Port"]
		
		# db_host_Addr2 = row["w_host_Addr2"]
		# db_host_Port2 = row["w_host_Port2"]
		# db_tcp_Addr = row["w_tcp_Addr"]
		# db_tcp_Port = row["w_tcp_Port"]
		# db_tcp_Addr2 = row["w_tcp_Addr2"]
		# db_tcp_Port2 = row["w_tcp_Port2"]
		
		db_url = row["w_url1"] #
		# db_url2 = row["w_url2"]
		db_neighbors_ip = row["w_neighbors_ip"]
		db_capacity_max = int(row["w_capacity_max"])
		db_capacity_cur = int(row["w_capacity_cur"])
		db_alert_Port = int(row["w_alert_Port"])
		db_alert_Value = float(row["w_alert_Value"])
		# db_alert2_Port = int(row["w_alert2_Port"])
		# db_alert2_Value = float(row["w_alert2_Value"])
		# db_keycode = row["w_keycode"]
		# db_stamp = row["w_stamp"] #
	############ Table ################
		
	############ GPIO ################
	# GPIO 포트 초기화
	if db_alert_Port:
		try: # GPIO 포트 초기화
			GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
			GPIO.setup(db_alert_Port, GPIO.OUT)
			GPIO.output(db_alert_Port, GPIO.HIGH)
			if db_alarm_disable: print "Enable GPIO", db_alert_Port
		# except KeyboardInterrupt:
			# GPIO.cleanup()
		except:
			pass
	############ GPIO ################

	returnIndex = insert_event_log_RLS(tableName=mySensorID,w_event_desc='Start Program')
	if returnIndex:
		logger.info('Start Programs ID - %s' % returnIndex)
	else:
		logger.critical('Error, insert_event_log_RLS')

	# 최초 실행시 사인보드에 현재 상황 전송
	for row in read_field_w_capacity_cur(myTableID): # 현재 수용량의 변화를 재 설정 한다..
		db_capacity_max = row["w_capacity_max"]
		db_capacity_cur = row["w_capacity_cur"]
			
	insert_socket_SIGN_BOARD(db_sensor_serial, db_subject, db_system_ip, db_table_PortIn, db_capacity_max, db_capacity_cur, beep=1)
					
	#################################################################
	# 환경변수
	#################################################################
	if db_sensor_face: # 0 => 'Side In', 1 => 'Side Out'
		statTch = 'B2'
		# statApp = 'B1'
		# statAtt = 'A1'
		statFin = 'A2'
	else:
		statTch = 'A2'
		# statApp = 'A1'
		# statAtt = 'B1'
		statFin = 'B2'

	curEvent = ''	
	curStatus = 0	
	preEvent = '' 
	preStatus = 0 
	
	traceEvent = 0 # 시작 이벤트 발생
	traceDirection = 'eventOn'
	moveIn = 1
	moveOut = -1
	
	# blockGate = '' #  == 'MO'
	gateOpen = 0
	gateClose = 0
	countAdd = 0

	tmpEventCount = 0
	tmpEventLevel = 0 # 감지된 이벤트의 지역(Zone)수
	tmpEventType = ''
	set_w_rls_ca = 0
	pre_w_rls_ca = ''
	
	socket.setdefaulttimeout(RLS_limit_time_delta) # socket.timeout 오류시간 설정
	try:
		tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
		tcpSerSock.bind((db_virtual_Addr, db_virtual_Port)) # <------- 소켓을 주소로 바인딩
		tcpSerSock.listen(1) # <------ listening 시작. 최대 클라이언트 (연결 수)
		logger.info("Connected and Listen IP:%s PORT:%s" % (db_virtual_Addr, db_virtual_Port))
	except:
		tcpSerSock.close() # 오류를 발생시킴으로 재 실행을 유도 한다.
		logger.critical('Error, At Creating Socket. Check Socket IP(%s) And Port(%s)' % (db_virtual_Addr, db_virtual_Port))
		print reboot_wits() # send mail to manager
	
	while True:
		try:
			tcpCliSock, addr = tcpSerSock.accept()
		except socket.timeout: # RLS_limit_time_delta 값 이상의 시간이 흐르면 오류 발생
			logger.critical(RLS_limit_time_delta_msg) # Waiting Heartbit over
			continue # 오류발생시 반복문 재실행.
		
		if addr[0] == db_sensor_Addr or addr[0] == db_sensor_Addr2: # 약속된 센서 아이피만 수용한다.
			pass
		else:
			logger.critical('Error, Sensor IP %s and config IP %s are must be match.' % (addr[0], db_sensor_Addr))
			continue # 조건에 맞지 않는 경우 맨 처음으로 돌아가기
		
		while True:
			data = tcpCliSock.recv(Buffer_size)
			if not data: 
				break # 현재의 반복문을 빠저나간다.
			
			RLS_size = len(data)
			if RLS_size is 27: # 2020 or 3060
				w_rls_md = data[0:3].strip()	# Model
				w_rls_id = data[3:6].strip()	# ID Number
				w_rls_ma = data[6:8].strip()	# Master Alarm
				w_rls_la = data[8:10].strip()	# The Latest Area
				w_rls_ca = data[10:12].strip()	# Combination of Areas
				w_rls_cc = data[12:14].strip()	# Multiple Areas
				w_rls_dq = data[14:16].strip()	# Disqualification	
				w_rls_ar = data[16:18].strip()	# Anti-rotation
				w_rls_am = data[18:20].strip()	# Anti-masking
				w_rls_tr = data[20:22].strip()	# Internal Error
				w_rls_so = data[22:24].strip()	# Soiling
				w_rls_ta = data[24:26].strip()	# Tamper or Device Monitoring
			elif RLS_size is 28: # 3060
				w_rls_md = data[0:3].strip()	# Model
				w_rls_id = data[3:6].strip()	# ID Number
				w_rls_ma = data[6:8].strip()	# Master Alarm
				w_rls_la = data[8:11].strip()	# The Latest Area
				w_rls_ca = data[11:13].strip()	# Combination of Areas
				w_rls_cc = data[13:15].strip()	# Multiple Areas
				w_rls_dq = data[15:17].strip()	# Disqualification
				w_rls_ar = data[17:19].strip()	# Anti-rotation
				w_rls_am = data[19:21].strip()	# Anti-masking
				w_rls_tr = data[21:23].strip()	# Internal Error
				w_rls_so = data[23:25].strip()	# Soiling
				w_rls_ta = data[25:27].strip()	# Tamper or Device Monitoring
			else:
				pass
			
			# Event Reset
			w_zone_a1 = 0
			w_zone_a2 = 0
			w_zone_b1 = 0
			w_zone_b2 = 0
			
			w_event_sent = 0
			w_event_shot = 0
			w_event_mail = 0
			w_event_alert = 0

			if tmpEventType == w_rls_ma: # 마스터 알람 플레그를 저장한후 다음 이벤트와 비교
				tmpEventCount += 1
			else: # 이전 이벤트 전환시점
				tmpEventCount = 1
			
			if w_rls_ca: # Combination of Area
				tmpEventLevel = RLS_map_CA[w_rls_ca].count(",")+1 # 감지지역 수
				w_map_CA = RLS_map_CA[w_rls_ca].split(",")
				for i in w_map_CA: # 복합영역의 값을 영역필드에 적용. 참조:RLS_map_CA[]
					locals()['w_zone_{0}'.format(i)] = 1
				w_event_desc = RLS_desc_CA[w_rls_ca]
			elif w_rls_la: # Latest Area
				tmpEventLevel = 1
				# 예) w_rls_la값: B21 -> b21 -> b2 -> w_zone_b2 결과값
				if len(w_rls_la) is 3: # ex) B21, RLS_size is 28
					locals()['w_zone_{0}'.format(w_rls_la.lower()[:-1])] = 1
				else: # ex) B2, RLS_size is 27
					locals()['w_zone_{0}'.format(w_rls_la.lower())] = 1
				w_event_desc = RLS_desc_LA[w_rls_la]
			elif w_rls_ma: # Master Alarm
				tmpEventLevel = 0
				w_event_desc = RLS_desc_MA[w_rls_ma]
			else: # MO : Master Alarm - 하트비트
				tmpEventLevel = 0
				w_event_desc = Event_desc[2] # 'Idle Event'
							
			w_event_cnt = tmpEventCount # 연속되는 이벤트 증가값 저장
			w_event_schedule = 0 # isItScheduleDate() # 주단위 예약이 우선이다. 예약일(1:일간, 2:주간)인지 아니지 
			w_event_ignore = 0 # lsIgnoreZone(w_rls_la, w_event_schedule) # 예약일이면 scheduleZone 참조 아니면 ignoreZone 참조
			
			##################################################
			## Analiging #####################################
			# - 마스터이벤트(w_rls_ma)값이 [MO]가 아니면([CL]이거나 None)
			
			if w_rls_ma == 'MO':

				# 복합 이벤트인 경우 센서에 가까운 위치값을 최근값에 선언한다.
				if w_rls_ca: 
					curEvent = Event_CA[w_rls_ca]
				else:
					curEvent = w_rls_la

				curStatus = getEventStatus(db_sensor_face, curEvent, preEvent)
				
				if curStatus != preStatus and curStatus: # 동일한 위치가 연속적이면 이베트 무시
					preStatus = curStatus
					# w_event_sent = 1
				
				# 최초 이벤트값이 시작이나 끝이면 추적 시작
				# 시작시 값을 종료때에도 유지 한다.
				if traceEvent:
					if set_w_rls_ca and w_rls_ca == '':
						set_update_w_capacity_cur(myTableID, traceEvent)
						w_event_sent = 1
						
					if w_rls_ca == 'BA':
						pre_w_rls_ca = 'BA'
					else:
						pre_w_rls_ca = ''
						
					if pre_w_rls_ca == 'BA' and w_rls_ca == 'BA':
						set_w_rls_ca = 1
					else:
						set_w_rls_ca = 0
				else:
					if curEvent == statTch:
						traceEvent = moveIn # traceValue = 1 # 가산
						traceDirection = 'moveIn'
					elif curEvent == statFin:
						traceEvent = moveOut # traceValue = -1 # 감산
						traceDirection = 'moveOut'
					else:
						traceDirection = 'eventOn'
						traceEvent = 0 
						curEvent = ''	
						curStatus = 0	
						preEvent = '' 
						preStatus = 0

				position = Status_event[curStatus]
				preEvent = curEvent
					
			else: # if w_rls_ma == 'CL':
				# if traceEvent :
				# 시작이 들어오면서 종료가 나가는것이거나 그 반대인 경우
				if traceEvent == moveIn and curEvent == statFin or traceEvent == moveOut and curEvent == statTch:
					set_update_w_capacity_cur(myTableID, traceEvent) # w_capacity_cur에 변화된 값을 재 설정 한다.
					w_event_sent = 1
				
					# print "trace:%s msg:%s gateOpen:%s gateClose:%s countAdd:%s curE:%s preE:%s curS:%s preS:%s" % (traceEvent, w_rls_ma, gateOpen, gateClose, countAdd, curEvent, preEvent, curStatus, preStatus)
					
				# 리셋 플래그
				traceEvent = 0 
				curEvent = ''	
				curStatus = 0	
				preEvent = '' 
				preStatus = 0
					
			## Analiging #####################################
			##################################################

			# Error or worning
			# Sensor Condition
			condition_error = 0
			if w_rls_dq: # Disqualification
				w_event_desc = RLS_desc_DQ[w_rls_dq] + " " + w_event_desc
				logger.warning(RLS_desc_DQ[w_rls_dq])
				condition_error = 9
			if w_rls_ar: # Anti-rotation
				w_event_desc = RLS_desc_AR[w_rls_ar] + " " + w_event_desc
				logger.warning(RLS_desc_AR[w_rls_ar])
				condition_error = 9
			if w_rls_am: # Anti-masking
				w_event_desc = RLS_desc_AM[w_rls_am] + " " + w_event_desc
				logger.warning(RLS_desc_AM[w_rls_am])
				condition_error = 9
			if w_rls_tr: # Internal Error
				w_event_desc = RLS_desc_TR[w_rls_tr] + " " + w_event_desc
				logger.critical(RLS_desc_TR[w_rls_tr])
				condition_error = 9
			if w_rls_so: # Soiling
				w_event_desc = RLS_desc_SO[w_rls_so] + " " + w_event_desc
				logger.warning(RLS_desc_SO[w_rls_so])
				condition_error = 9
			if w_rls_ta: # Tamper, Device Monitoring
				if w_rls_ta == "DM":
					w_event_desc = RLS_desc_TA[w_rls_ta] + " " + w_event_desc
					pass
				else:
					w_event_desc = RLS_desc_TA[w_rls_ta] + " " + w_event_desc
					logger.warning(RLS_desc_TA[w_rls_ta])
					condition_error = 9
			
			tmp_lat_s = db_sensor_lat_s
			tmp_lng_s = db_sensor_lng_s
			tmp_lat_e = db_sensor_lat_e
			tmp_lng_e = db_sensor_lng_e
			tmp_ignore = w_event_ignore
			tmp_area = w_rls_la.lower()[:-1]
			if len(w_rls_la) is 3: # ex) B21, RLS_size is 28
				tmp_area = w_rls_la.lower()[:-1]
			else: # ex) B2, RLS_size is 27
				tmp_area = w_rls_la.lower()
			tmp_zone = RLS_map_LA[w_rls_la] # w_rls_la값이 없으면 -1을 반환 한다.

			tmp_alarmOut = getAlarmSet(w_rls_ma,w_rls_la,w_rls_ca,w_rls_cc,w_rls_dq,w_rls_ar,w_rls_am,w_rls_tr,w_rls_so,w_rls_ta,tmp_ignore)

			# 매번 데이터 베이스 접속을 방지 하기 위해 방금 전의 이밴트가 알람 크리어된 상테인경우 설정을 확인 한후 실행
			# 현제의 이벤트가 CL 이며 이전 이벤트가 하트비트 이면 설정갑을 확인후 제실행 한다.
			# if not w_rls_ma and tmpEventType == 'CL': 
			# if w_rls_ma == 'MO' and tmpEventType == 'CL': 
			if w_rls_ma == '' and tmpEventType == '': 
				# 실시간 설정 변동 값을 휴간상황때 데이터베이스 접속 확인
				for row in read_field_w_cfg_status(myTableID):
					# db_sensor_stop = row["w_sensor_stop"]		# `w_sensor_stop` TINYINT(1) - 일시정지
					db_sensor_reload = row["w_sensor_reload"] 	# `w_sensor_reload` TINYINT(1) - 재시동
					db_sensor_disable = row["w_sensor_disable"]	# `w_sensor_disable` TINYINT(1) -알람중지
					
				if db_sensor_disable: # 종료
					logger.info('Stop Program.')

					tcpCliSock.close()
					tcpSerSock.close()
					returnIndex = insert_event_log_RLS(tableName=mySensorID,w_event_desc='Stop Program')
					if returnIndex:
						logger.info('Stop Programs ID - %s' % returnIndex)
					else:
						logger.critical('Error, insert_event_log_RLS')
					exit()
				
				if db_sensor_reload: # 재시동
					logger.info('Restart Program.')
					set_reload_w_cfg_reload(myTableID) # 재시동 필드를 회복시킨다.

					tcpCliSock.close()
					tcpSerSock.close()
					returnIndex = insert_event_log_RLS(tableName=mySensorID,w_event_desc='Restart Program')
					if returnIndex:
						logger.info('Restart Programs ID - %s' % returnIndex)
					else:
						logger.critical('Error, insert_event_log_RLS')
					restart_wits()
					exit()

				# 하트비트 전송
				if (w_event_cnt % Heartbit_cycle) == 0:
					# status = Event_type['idle']
					# msg = Event_desc[status]
					if condition_error:
						status = condition_error
					else:
						status = Event_type['idle']

					msg = w_event_desc
					
					insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=db_sensor_model, board=ECOS_table_PARKING, tableID=myTableID, status=status, msg=msg)
					
					insert_socket_SIGN_BOARD(db_sensor_serial, db_subject, db_system_ip, db_table_PortIn, db_capacity_max, db_capacity_cur, beep=0)
					
					if db_host_Addr and db_host_Port: # 호스트정보가 있으면 정보 전송
						returnValue = insert_socket_log(db_sensor_serial, db_subject, tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, db_sensor_face, db_host_Addr, db_host_Port, db_capacity_max, db_capacity_cur, status, msg)
						if returnValue: #
							# 대상 호스트 포트 프로그램이 실행 되지 않으면 오류 발생
							logger.warning("%s - Check Host:Port Socket or Monitoring." % returnValue)
						else:
							# # 정상적인 결과인경우 로그전송을 하지 않는다.
							# logger.info('Sent to Socket ID - %s' % returnValue)
							pass
					else:
						logger.warning("Need Host Info.")
					
			tmpEventType = w_rls_ma

			##///////////////////////////////////////////////////////////////
			# 결과에 따른 기능 수행
			##///////////////////////////////////////////////////////////////
			if db_alarm_disable: # and not tmp_ignore: # 유효한 이벤트 발생시 관제에 상태 전송 후 스넵샷
				pass
			else:
				# 관제시스템에 이벤트 로그를 전송 한다.
				if w_event_sent:
					if w_event_schedule:
						status=Event_type['block']
						msg = position
					else:	
						status=Event_type['active']
						msg = position
						
					# print "trace:%s msg:%s gateOpen:%s gateClose:%s countAdd:%s curE:%s preE:%s curS:%s preS:%s" % (traceEvent, w_event_desc, gateOpen, gateClose, countAdd, curEvent, preEvent, curStatus, preStatus)

					for row in read_field_w_capacity_cur(myTableID): # 현재 수용량의 변화를 재 설정 한다..
						db_capacity_max = row["w_capacity_max"]
						db_capacity_cur = row["w_capacity_cur"]

					w_event_desc = '%s %i/%i' % (traceDirection, db_capacity_cur, db_capacity_max)
					insert_socket_status_UNION(db_sensor_serial, db_subject, db_system_ip, db_system_port, model=db_sensor_model, board=ECOS_table_PARKING, tableID=myTableID, status=status, msg=w_event_desc)  # 소켓 유니온 전송
							
					# 사인보드에 상황 전송
					insert_socket_SIGN_BOARD(db_sensor_serial, db_subject, db_system_ip, db_table_PortIn, db_capacity_max, db_capacity_cur, beep=1)
							
					if db_host_Addr and db_host_Port: # 호스트정보가 있으면 정보 전송
						returnValue = insert_socket_log(db_sensor_serial, db_subject, tmp_lat_s, tmp_lng_s, tmp_lat_e, tmp_lng_e, db_sensor_face, db_host_Addr, db_host_Port, db_capacity_max, db_capacity_cur, status, w_event_desc)
						if returnValue: #
							# 대상 포트 프로그램이 실행 되지 않으면 오류 발생
							logger.warning("Socket Error(insert_socket_log %s)" % returnValue)
						else:
							# # 정상적인 결과인경우 로그전송을 하지 않는다.
							# logger.info('Sent to Socket ID - %s' % returnValue)
							pass
					else:
						logger.warning("Need Host Info.")
			
					# 스넵삿
					# http://myserver/axis-cgi/jpg/image.cgi
					if db_url: # 스넵삿이 가능한 BSS_url 값이 있으면 
						eventName = getSnapshot(db_url)

					# 실시간 알람 접점신호 발생
					if w_event_alert:
						if db_alert_Port and db_alert_Value: # 알람 발생 알림 포트(db_alert_Port) 출력지속시간:초( db_alert_Value:)
							Process(target=alertOut, args=(db_alert_Port,db_alert_Value)).start()
						else:
							pass
							# logger.warning("Need Alert Info.")
					
			# # 유효 이벤트 발생시 정보 데이터베이스 업데이트
			if w_event_sent: # 적용 이벤트가 발생하면 데이터베이스에 등록 한다.
				returnIndex = insert_event_log_RLS(tableName=mySensorID,w_rls_md=w_rls_md,w_rls_id=w_rls_id,w_rls_ma=w_rls_ma,w_rls_la=w_rls_la,w_rls_ca=w_rls_ca,w_rls_cc=w_rls_cc,w_rls_dq=w_rls_dq,w_rls_ar=w_rls_ar,w_rls_am=w_rls_am,w_rls_tr=w_rls_tr,w_rls_so=w_rls_so,w_rls_ta=w_rls_ta,w_zone_a1=w_zone_a1,w_zone_a2=w_zone_a2,w_zone_b1=w_zone_b1,w_zone_b2=w_zone_b2,w_event_cnt=w_event_cnt,w_event_ignore=w_event_ignore,w_event_schedule=w_event_schedule,w_event_sent=w_event_sent,w_event_shot=w_event_shot,w_event_mail=w_event_mail,w_event_alert=w_event_alert,w_event_desc=w_event_desc)
				logger.info('Update Event ID - %s %s' % (returnIndex,w_event_desc))
				
		tcpCliSock.close()
	tcpSerSock.close()			
