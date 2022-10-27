#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from module import *

def main():
	# 사용자 요청에 따른 시리얼 디바이스 선택  
	if not len(sys.argv) == 2: sys.exit('need argv') ##### exit #####
	
	myTableID = sys.argv[1]

	for row in read_table_w_cfg_sensor_COUNTER(myTableID): # 로깅을 위한 파일명으로 사용할 시리얼 번호를 가지고 온다.
		mySensorID = row["w_sensor_serial"]
	
	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418

	if not os.path.exists(c.ITS_log_data): # c.ITS_log_data 폴더 생성
		os.makedirs(c.ITS_log_data)
	logger = logging.getLogger(mySensorID) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = c.ITS_log_data+mySensorID+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
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
	if not os.path.exists(c.ITS_img_data): # c.ITS_img_data 폴더 생성
		os.makedirs(c.ITS_img_data)
	# 센서 이벤트 스크린샷 이미지 저장 폴더명
	targetPath = c.ITS_img_data + mySensorID + "/"
	if not os.path.exists(targetPath): # c.ITS_img_data 내의 서브 사진 폴더 생성
		os.makedirs(targetPath)
	############ Images ################

	# 테이블 생성
	returnMsg = create_table_w_log_sensor_COUNTER(mySensorID) # 테이블 생성 - 반환값

	set_reload_w_cfg_sensor_COUNTER(myTableID) ## reload reset
	w_cfg_sensor_list = read_table_w_cfg_sensor_COUNTER(myTableID) # 변수에 아이디를 넣어 하나의 센서 정보만 가지고 온다.
	for row in w_cfg_sensor_list:
		CNT_subject = row["wr_subject"]
		# CNT_id = row["w_id"]
		# CNT_cpu_id = row["w_cpu_id"]
		CNT_keycode = row["w_keycode"]
		# CNT_device_id = row["w_device_id"]
		CNT_sensor_serial = row["w_sensor_serial"] #
		# CNT_sensor_model = row["w_sensor_model"]
		# CNT_sensor_face = row["w_sensor_face"]
		# CNT_sensor_angle = row["w_sensor_angle"]
		# CNT_sensor_lat_s = row["w_sensor_lat_s"]
		# CNT_sensor_lng_s = row["w_sensor_lng_s"]
		# CNT_sensor_lat_e = row["w_sensor_lat_e"]
		# CNT_sensor_lng_e = row["w_sensor_lng_e"]
		CNT_minDist = int(row["w_sensor_ignoreS"]) # 감지 시작 영역
		CNT_maxDist = int(row["w_sensor_ignoreE"]) # 감지 종료 영역
		# CNT_sensor_ignoreZone = row["w_sensor_ignoreZone"] # 감지 확정 영역
		CNT_validZone_S = int(row["w_sensor_scheduleS"])
		CNT_validZone_E = int(row["w_sensor_scheduleE"])
		# CNT_sensor_scheduleZone = row["w_sensor_scheduleZone"]
		CNT_oneway = row["w_sensor_noOfZone"] #
		# CNT_sensor_stepOfZone = row["w_sensor_stepOfZone"] #
		CNT_sensor_offset = int(row["w_sensor_offset"]) #
		CNT_sensor_sensor_week = row["w_sensor_week"]
		# BSS_sensor_sensor_time = row["w_sensor_time"]
		CNT_sensor_disable = row["w_sensor_disable"]
		CNT_sensor_stop = row["w_sensor_stop"] #
		CNT_sensor_reload = row["w_sensor_reload"] #
		CNT_pickCycle = float(row["w_event_pickTime"]) # 노이즈 임계 값
		CNT_holdTime= float(row["w_event_holdTime"]) # 이벤트 그룹 크기 
		CNT_event_keepHole = row["w_event_keepHole"] #
		CNT_event_syncDist = row["w_event_syncDist"] #
		CNT_alarm_disable = row["w_alarm_disable"] #
		# CNT_alarm_level = row["w_alarm_level"] #
		CNT_system_ip = row["w_system_ip"]
		CNT_system_port = row["w_system_port"]
		# CNT_systemBF_ip = row["w_systemBF_ip"]
		# CNT_systemBF_port = row["w_systemBF_port"]
		# CNT_systemAF_ip = row["w_systemAF_ip"]
		# CNT_systemAF_port = row["w_systemAF_port"]
		# CNT_master_Addr = row["w_master_Addr"]
		# CNT_master_Port = row["w_master_Port"]
		# CNT_virtual_Addr = row["w_virtual_Addr"] #
		# CNT_virtual_Port = row["w_virtual_Port"] #
		# CNT_sensor_Addr = row["w_sensor_Addr"] #
		# CNT_sensor_Port = row["w_sensor_Port"]
		CNT_host_addr = row["w_host_Addr"]
		CNT_host_port = row["w_host_Port"]
		CNT_host_addr2 = row["w_host_Addr2"]
		CNT_host_port2 = row["w_host_Port2"]
		# CNT_tcp_Addr = row["w_tcp_Addr"]
		# CNT_tcp_Port = row["w_tcp_Port"]
		# CNT_tcp_Addr2 = row["w_tcp_Addr2"]
		# CNT_tcp_Port2 = row["w_tcp_Port2"]
		CNT_url = row["w_url1"] #
		# CNT_url2 = row["w_url2"]
		CNT_alert_port = int(row["w_alert_Port"])
		CNT_alert_value = float(row["w_alert_Value"])
		# CNT_stamp = row["w_stamp"] #
		
		# Node Js를 통한 실시간 모니터링 입력 포트 http://localhost:myPortIn
		CNT_table_PortIn = row["w_table_PortIn"]

	# 알람 정보가 등록되어있으면 [출력]포트 초기화
	if CNT_alert_port and CNT_alert_value:
		try: # COUNTER 포트 초기화
			GPIO.setmode(GPIO.BCM)	# Set's COUNTER pins to BCM COUNTER numbering
			GPIO.setup(CNT_alert_port, GPIO.OUT)
			GPIO.output(CNT_alert_port, GPIO.HIGH)
		except:
			logger.info('%s Error Alert port Init' % CNT_alert_port)
	######################################################

	CNT_minIgnore = CNT_minDist/10 # mm -> cm 감지 시작 영역
	CNT_maxIgnore = CNT_maxDist/10 # mm -> cm 감지 시작 영역
	CNT_minLimit = CNT_validZone_S/10 # mm -> cm 감지 종료 영역
	CNT_maxLimit = CNT_validZone_E/10 # mm -> cm 감지 종료 영역
	
	SENSOR_min = 19 # 센서 특성 최소 감지거리
	SENSOR_max = 499 # 센서 특성 최대 감지거리

	logger.info(">>>> Start <<<<")
	# logger.info("CNT_subject")
	# logger.info("minIgnore %s cm"%CNT_minIgnore)
	# logger.info("maxIgnore %s cm"%CNT_maxIgnore)
	# logger.info("minLimit %s cm"%CNT_minLimit)
	# logger.info("maxLimit %s cm"%CNT_maxLimit)
	# logger.info("Cycle Time %s sec"%CNT_pickCycle)
	# logger.info("Manual Delay %s"%CNT_holdTime) ## 센서 특성에 따른 사용자 강제 딜레이
	# logger.info("Log Print %s"%CNT_alarm_disable) ## Logger Output
	# logger.info("Dual Event %s"%CNT_event_keepHole) ## 최초에 두센서가 동시에 발생한(CNT_event_keepHole) 이벤트 허용
	# logger.info("Limit Over %s"%CNT_event_syncDist) ## 최대 허용거리(CNT_maxIgnore)를 초과하는 이벤트를 유효이밴트로 처리한다.
	# logger.info("Oneway %s"%CNT_oneway) ## Oneway
	# logger.info("Pause %s"%CNT_sensor_stop) ## Pause
	
	initPortGPIO(c.L_TRIG, c.L_ECHO)
	initPortGPIO(c.R_TRIG, c.R_ECHO)

	moveIN = '' ## Start Name
	moveOUT = '' ## End Name

	doubleIN = 0 ## Double Start
	doubleOUT = 0 ## Double End
	
	imgPath = '' ## 스넵샷 이미지 경로
	
	eventOn = 0
	heartBeat = 0
	
	dirLeft = 'left'
	dirRight = 'right'
	dirBoth = 'both'
	
	while(1):
		## 센서 특성에 따른 사용자 강제 딜레이 - Manual Delay
		if CNT_holdTime:
			time.sleep(CNT_holdTime)
	
		if not CNT_sensor_stop: ## 일시정지 CNT_sensor_stop
			dist_L = getEventGPIO(c.L_TRIG, c.L_ECHO)
			dist_R = getEventGPIO(c.R_TRIG, c.R_ECHO)

		## 거리고정허용(CNT_event_syncDist) 값에 따라 
		## 센서 최대 허용거리(SENSOR_max)를 초과하는 이벤트를 유효이밴트로 처리한다.
		if CNT_event_syncDist:
			if dist_L>CNT_maxIgnore: dist_L = SENSOR_min
			if dist_R>CNT_maxIgnore: dist_R = SENSOR_min

		insert_socket_monitor_COUNTER(CNT_system_ip, CNT_table_PortIn, CNT_sensor_serial, CNT_subject, "dist_L", dist_L, eventOn)
		insert_socket_monitor_COUNTER(CNT_system_ip, CNT_table_PortIn, CNT_sensor_serial, CNT_subject, "dist_R", dist_R, eventOn)
		
		if dist_L > CNT_minLimit and dist_R > CNT_minLimit: ## 허용거리에 접근한 이벤트가 없는경우
			if moveIN and moveOUT and moveIN is not moveOUT: ## 단일입장 단일퇴장 조건 만족
				eventOn = 1
			elif doubleIN and moveOUT: ## 동시입장 단일퇴장 조건 만족
				eventOn = 2
			elif moveIN and doubleOUT: ## 단일입장 동시퇴장 조건 만족
				eventOn = 3
			elif doubleOUT and doubleIN: ## 동시 입장, 퇴장
				eventOn = 4
			elif moveIN and moveOUT and moveIN is moveOUT: ## 단일입장 단일퇴장 조건 만족
				eventOn = 5
			else: 
				if moveIN or moveOUT or doubleIN or doubleOUT:
					eventOn = 9
				heartBeat += 1 ## 
				
		elif dist_L < CNT_minLimit and dist_R < CNT_minLimit: ## 허용거리에 접근한 이벤트가 모두 있는경우
			## 최초에 두센서가 동시에 발생한(CNT_event_keepHole) 이벤트 허용
			## 최대 허용거리(CNT_maxIgnore)를 초과하는 이벤트를 유효이밴트로 처리한다.
			if CNT_event_keepHole:
				if moveIN or doubleIN: ## 최종 이벤트 - 출구방향 선언
					doubleOUT = 1
					moveOUT = '' ## Single Out 리셋
				else: ## 최초 이벤트 -입구방향 선언
					doubleIN = 1
			continue # 속도와 연관있음 
			
		else: ## 허용거리에 접근한 이벤트가 하나인 경우
			if moveIN or doubleIN: ## 최종 이벤트 - 출구방향 선언
				if dist_L < dist_R:
					moveOUT = dirLeft
				else:
					moveOUT = dirRight
				doubleOUT = 0 ## Double Out 리셋
			else: ## 최초 이벤트 -입구방향 선언
				if dist_L < dist_R:
					moveIN = dirLeft
				else:
					moveIN = dirRight
			continue # 속도와 연관있음 
		
		if eventOn: ## 상태 전송
			## 방향 확인
			if eventOn == 1 or eventOn == 3:
				dirStat = moveIN
				msg = "Single -> 1:Single or 3:Both"
			elif eventOn == 2:
				if moveOUT == dirLeft:
					dirStat = dirRight
				else:
					dirStat = dirLeft
				msg = "Both -> Single"
			elif eventOn == 4:
				dirStat = dirBoth
				msg = "Both -> Both"
			elif eventOn == 5:
				dirStat = "return"
				msg = "Return to Enterence"
			elif eventOn == 9: ## eventOn가 9인경우
				dirStat = "error"
				msg = "ERROR"
			
			if CNT_alarm_disable: 
				if eventOn == 9:
					logger.warning("%s in, Type: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, Msg:%s" % (dirStat.upper(), eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg))
					print "%s%s%s:\tType: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, \tMsg:%s" % (c.R,dirStat.upper(),c.W, eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg)
				elif eventOn == 5:
					logger.info("%s in, Type: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, Msg:%s" % (dirStat.upper(), eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg))
					print "%s%s%s:\tType: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, \tMsg:%s" % (c.P,dirStat.upper(),c.W, eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg)
				elif eventOn == 4:
					logger.warning("%s in, Type: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, Msg:%s" % (dirStat.upper(), eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg))
					print "%s%s%s:\tType: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, \tMsg:%s" % (c.O,dirStat.upper(),c.W, eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg)
				else:
					logger.info("%s in, Type: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, Msg:%s" % (dirStat.upper(), eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg))
					print "%s%s%s:\tType: %s, mIN:%s, mOUT:%s, dIN:%s, dOUT:%s, \tMsg:%s" % (c.G,dirStat.upper(),c.W, eventOn, moveIN, moveOUT, doubleIN, doubleOUT, msg)

			## 데이터 베이스 등록
			# if CNT_oneway: ## 일방통행
			insert_event_log_COUNTER(mySensorID, eventOn, dirStat)
			insert_socket_monitor_COUNTER(CNT_system_ip, CNT_table_PortIn, CNT_sensor_serial, CNT_subject, dirStat, CNT_minLimit, eventOn)
			if CNT_url: imgPath = "%s%s" % (CNT_system_ip,getSnapshot(CNT_url,targetPath)[13:]) # image를 가지고온후 머리부분 /var/www/html을 제거
			if CNT_host_addr and CNT_host_port: insert_socket_for_IMS(CNT_host_addr, CNT_host_port, CNT_sensor_serial, CNT_subject, 1, 0, 0, 0, 0, shot=imgPath, msg='')
			if CNT_host_addr2 and CNT_host_port2: insert_socket_for_IMS(CNT_host_addr2, CNT_host_port2, CNT_sensor_serial, CNT_subject, 1, 0, 0, 0, 0, shot=imgPath, msg='')
	
		else: ## 데이터 베이스 확인
			if heartBeat > c.db_reload_cycle: ## 기본 10회
				heartBeat = 0 ##  카운터 리셋
				## 하트비트 전송
				if CNT_alarm_disable: logger.info('heartBeat Current Max_L:%scm, Max_R:%scm'%(dist_L, dist_R))
				if CNT_host_addr and CNT_host_port: insert_socket_for_IMS(CNT_host_addr, CNT_host_port, CNT_sensor_serial, CNT_subject)
				if CNT_host_addr2 and CNT_host_port2: insert_socket_for_IMS(CNT_host_addr2, CNT_host_port2, CNT_sensor_serial, CNT_subject)
				
				for row in read_table_w_cfg_sensor_COUNTER(myTableID): # 로깅을 위한 파일명으로 사용할 시리얼 번호를 가지고 온다.
					## 사용자의 설정변경값을 적용
					if row["w_sensor_reload"]: # visReload:
						CNT_subject = row["wr_subject"]
						CNT_minDist = int(row["w_sensor_ignoreS"]) # 감지 시작 영역
						CNT_maxDist = int(row["w_sensor_ignoreE"]) # 감지 종료 영역
						CNT_validZone_S = int(row["w_sensor_scheduleS"]) # 감지 임계값
						CNT_validZone_E = int(row["w_sensor_scheduleE"]) # 감지 임계값
						CNT_pickCycle = float(row["w_event_pickTime"]) # 픽업주기 
						CNT_holdTime= float(row["w_event_holdTime"]) ## 센서 특성에 따른 사용자 강제 딜레이
						
						CNT_sensor_disable = row["w_sensor_disable"] # 사용정지
						CNT_sensor_stop = row["w_sensor_stop"] # 일시정지
						CNT_alarm_disable = row["w_alarm_disable"] # 로그 출력 허용
						CNT_event_keepHole = row["w_event_keepHole"] ## 최초에 두센서가 동시에 발생한(CNT_event_keepHole) 이벤트 허용
						CNT_event_syncDist = row["w_event_syncDist"] ## 최대 허용거리(CNT_maxIgnore)를 초과하는 이벤트를 유효이밴트로 처리한다.
						CNT_oneway = row["w_sensor_noOfZone"] #

						CNT_table_PortIn = row["w_table_PortIn"]
						CNT_table_PortOut = row["w_table_PortOut"]

						CNT_minIgnore = CNT_minDist/10 # mm -> cm 감지 시작 영역
						CNT_maxIgnore = CNT_maxDist/10 # mm -> cm 감지 시작 영역
						CNT_minLimit = CNT_validZone_S/10 # mm -> cm 감지 종료 영역
						CNT_maxLimit = CNT_validZone_E/10 # mm -> cm 감지 종료 영역
						
						logger.info(">>>> Restart <<<<")
						logger.info("CNT_subject")
						logger.info("minIgnore %s cm"%CNT_minIgnore)
						logger.info("maxIgnore %s cm"%CNT_maxIgnore)
						logger.info("minLimit %s cm"%CNT_minLimit)
						logger.info("maxLimit %s cm"%CNT_maxLimit)
						logger.info("Cycle Time %s sec"%CNT_pickCycle)
						logger.info("Manual Delay %s"%CNT_holdTime) ## 센서 특성에 따른 사용자 강제 딜레이
						logger.info("Log Print %s"%CNT_alarm_disable) ## Logger Output
						logger.info("Dual Event %s"%CNT_event_keepHole) ## 최초에 두센서가 동시에 발생한(CNT_event_keepHole) 이벤트 허용
						logger.info("Limit Over %s"%CNT_event_syncDist) ## 최대 허용거리(CNT_maxIgnore)를 초과하는 이벤트를 유효이밴트로 처리한다.
						logger.info("Oneway %s"%CNT_oneway) ## Oneway
						logger.info("Pause %s"%CNT_sensor_stop) ## Pause
						
						kill_demon_COUNTER_table() ## Kill Node Daemon
						make_its_M_map(CNT_minDist,CNT_maxDist,CNT_validZone_S,CNT_validZone_E) ## Remake HTML
						run_demon_COUNTER_table("%s %s"%(CNT_table_PortIn, CNT_table_PortOut)) ## Exec Node Daemon
						logger.info('Running Node Daemon')	

						set_reload_w_cfg_sensor_COUNTER(myTableID) ## reload reset
				
		eventOn = 0
		moveIN = ''
		moveOUT = ''
		doubleIN = 0
		doubleOUT = 0

		time.sleep(CNT_pickCycle) # wait 10 miliseconds
	# Reset GPIO settings
	GPIO.cleanup()

	
# Run the main function when the script is executed
if __name__ == "__main__":
    main()	