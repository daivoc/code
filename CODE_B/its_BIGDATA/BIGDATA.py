#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from module import *

## 이벤트 로그 필드정보 초기화
w_cfg_id = 0 # int(11)
w_eventId = 0 # tinyint(4) No 0
w_eventDesc = '' # varchar(32) utf8_general_ci
w_eventValue = 0 # float No 0
w_eventStatus = '' # varchar(128) utf8_general_ci
w_eventShotURL = '' # 스넵샷 주소

if __name__ == '__main__':
	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print share["file"]["html_src"]
	## 예: print share["mysql"]["db_host"]
	share = readConfig('/home/pi/common/config.json')
	owner = readConfig('/home/pi/BIGDATA/config.json') 


	# 사용자 요청에 따른 시리얼 디바이스 선택  
	if not len(sys.argv) == 2: sys.exit('need argv') ##### exit #####
	myTableID = sys.argv[1]
	for row in read_field_w_cfg_sensor_BIGDATA(myTableID): # 로깅을 위한 파일명으로 사용할 시리얼 번호를 가지고 온다.
		mySensorID = row["w_sensor_serial"]
	
	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	if not os.path.exists(ECOS_log_data): # ECOS_log_data 폴더 생성
		os.makedirs(ECOS_log_data)
	logger = logging.getLogger(mySensorID) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = ECOS_log_data+mySensorID+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info("- START -")
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
	if not os.path.exists(ECOS_img_data): # ECOS_img_data 폴더 생성
		os.makedirs(ECOS_img_data)
	# 센서 이벤트 스크린샷 이미지 저장 폴더명
	img_data_sub = ECOS_img_data + mySensorID + "/"
	if not os.path.exists(img_data_sub): # ECOS_img_data 내의 서브 사진 폴더 생성
		os.makedirs(img_data_sub)
	############ Images ################

	# 테이블 생성
	returnMsg = create_table_w_log_sensor_BIGDATA(mySensorID) # 테이블 생성 - 반환값

	w_cfg_sensor_list = read_table_w_cfg_sensor_BIGDATA(myTableID) # 변수에 아이디를 넣어 하나의 센서 정보만 가지고 온다.
	for row in w_cfg_sensor_list:
		BIGDATA_subject = row["wr_subject"]
		# BIGDATA_id = row["w_id"]
		# BIGDATA_cpu_id = row["w_cpu_id"]
		BIGDATA_keycode = row["w_keycode"]
		BIGDATA_device_id = row["w_device_id"]
		BIGDATA_sensor_serial = row["w_sensor_serial"] #
		BIGDATA_sensor_model = row["w_sensor_model"]
		BIGDATA_sensor_face = row["w_sensor_face"]
		BIGDATA_sensor_angle = row["w_sensor_angle"]
		BIGDATA_sensor_lat_s = row["w_sensor_lat_s"]
		BIGDATA_sensor_lng_s = row["w_sensor_lng_s"]
		BIGDATA_sensor_lat_e = row["w_sensor_lat_e"]
		BIGDATA_sensor_lng_e = row["w_sensor_lng_e"]
		# BIGDATA_sensor_ignoreS = row["w_sensor_ignoreS"] #
		# BIGDATA_sensor_ignoreE = row["w_sensor_ignoreE"] #
		# BIGDATA_sensor_noOfZone = row["w_sensor_noOfZone"] #
		# BIGDATA_sensor_stepOfZone = row["w_sensor_stepOfZone"] #
		# BIGDATA_sensor_ignoreZone = row["w_sensor_ignoreZone"] #
		# BIGDATA_sensor_scheduleS = row["w_sensor_scheduleS"]
		# BIGDATA_sensor_scheduleE = row["w_sensor_scheduleE"]
		# BIGDATA_sensor_scheduleZone = row["w_sensor_scheduleZone"]
		BIGDATA_sensor_sensor_week = row["w_sensor_week"]
		# BIGDATA_sensor_sensor_time = row["w_sensor_time"]
		# BIGDATA_sensor_disable = row["w_sensor_disable"]
		# BIGDATA_sensor_stop = row["w_sensor_stop"] #
		# BIGDATA_sensor_reload = row["w_sensor_reload"] #
		BIGDATA_event_pickTime = row["w_event_pickTime"]
		BIGDATA_event_holdTime = row["w_event_holdTime"] # 
		BIGDATA_event_keepHole = row["w_event_keepHole"] #
		# BIGDATA_event_syncDist = row["w_event_syncDist"] #
		BIGDATA_alarm_disable = row["w_alarm_disable"] #
		BIGDATA_alarm_level = row["w_alarm_level"] #
		BIGDATA_system_ip = row["w_system_ip"]
		BIGDATA_system_port = row["w_system_port"]
		# BIGDATA_systemBF_ip = row["w_systemBF_ip"]
		# BIGDATA_systemBF_port = row["w_systemBF_port"]
		# BIGDATA_systemAF_ip = row["w_systemAF_ip"]
		# BIGDATA_systemAF_port = row["w_systemAF_port"]
		# BIGDATA_master_Addr = row["w_master_Addr"]
		# BIGDATA_master_Port = row["w_master_Port"]
		# BIGDATA_virtual_Addr = row["w_virtual_Addr"] #
		# BIGDATA_virtual_Port = row["w_virtual_Port"] #
		# BIGDATA_sensor_Addr = row["w_sensor_Addr"] #
		# BIGDATA_sensor_Port = row["w_sensor_Port"]
		BIGDATA_host_Addr = row["w_host_Addr"]
		BIGDATA_host_Port = row["w_host_Port"]
		BIGDATA_host_Addr2 = row["w_host_Addr2"]
		BIGDATA_host_Port2 = row["w_host_Port2"]
		# BIGDATA_tcp_Addr = row["w_tcp_Addr"]
		# BIGDATA_tcp_Port = row["w_tcp_Port"]
		# BIGDATA_tcp_Addr2 = row["w_tcp_Addr2"]
		# BIGDATA_tcp_Port2 = row["w_tcp_Port2"]
		
		BIGDATA_audio_name = row["wr_2"] ## Audio Filename
		BIGDATA_audio_time = float(row["wr_3"]) ## Audio Length
		BIGDATA_wr_4_URL = row["wr_4"] ## Preset
		BIGDATA_wr_5_ENC = row["wr_5"] ## Preset
		BIGDATA_wr_6_ID = row["wr_6"] ## Preset
		BIGDATA_wr_7_URL = row["wr_7"] ## Preset
		BIGDATA_wr_8_ENC = row["wr_8"] ## Preset
		BIGDATA_wr_9_ID = row["wr_9"] ## Preset

		BIGDATA_url1 = row["w_url1"] ## 스냅샷
		BIGDATA_url2 = row["w_url2"] ## 스트리밍
		BIGDATA_url3 = row["w_url3"] ## URL1
		BIGDATA_url4 = row["w_url4"] ## URL2
		BIGDATA_alert_Port = int(row["w_alert_Port"])
		BIGDATA_alert_Value = float(row["w_alert_Value"])
		
		BIGDATA_opt22 = row["w_opt22"]
		BIGDATA_opt91 = row["w_opt91"]
		BIGDATA_opt92 = row["w_opt92"]
		BIGDATA_opt93 = row["w_opt93"]
		BIGDATA_opt94 = row["w_opt94"]
		
		# Node Js를 통한 실시간 모니터링 입력 포트 http://localhost:myPortIn
		BIGDATA_table_PortIn = row["w_table_PortIn"]

	# 알람 정보가 등록되어있으면 [출력]포트 초기화
	if BIGDATA_alert_Port and BIGDATA_alert_Value:
		try: # BIGDATA 포트 초기화
			# BIGDATA.setmode(BIGDATA.BCM)	# Set's BIGDATA pins to BCM BIGDATA numbering
			# BIGDATA.setup(BIGDATA_alert_Port, BIGDATA.OUT)
			# BIGDATA.output(BIGDATA_alert_Port, BIGDATA.HIGH)
			insert_socket_GPWIO(id=BIGDATA_alert_Port, status=1, msg='init')
		except:
			pass

	# [입력]포트 초기화
	try: # BIGDATA 포트 초기화
		BIGDATA.setmode(BIGDATA.BCM)	# Set's BIGDATA pins to BCM BIGDATA numbering
		BIGDATA_ID = int(BIGDATA_device_id)
		BIGDATA.setup(BIGDATA_ID, BIGDATA.IN, pull_up_down = BIGDATA.PUD_UP)
	except:
		logger.info('%s Error BIGDATA port Init... WITS will restart' % BIGDATA_subject)
		w_cfg_id = 1 # Error Event
		w_eventId = Event_type['init']
		w_eventDesc = Event_desc[w_eventId]
		w_eventStatus = '%s Error BIGDATA port Init' % BIGDATA_subject
		insertLogId = insert_event_log_BIGDATA(mySensorID, w_cfg_id, w_eventId, w_eventDesc, w_eventValue, w_eventStatus) # 반환값은 성공시 데이터베이스 인댁스 ID
		logger.info(w_eventStatus)
		time.sleep(3) # delays for 5 seconds
		restart_myself() # 프로그램 재 시작
		
	w_eventId = Event_type['start']
	w_eventDesc = Event_desc[w_eventId]
	w_eventStatus = 'Normal start'
	insertLogId = insert_event_log_BIGDATA(mySensorID, w_cfg_id, w_eventId, w_eventDesc, w_eventValue, w_eventStatus) # 이벤트 로그
	logger.info(w_eventStatus)

	######################################################
	sec_per_times = 10.0	# float
	sleep_cycle = 1.0 / sec_per_times	# 데이터 픽업 주기 초
	heart_limit = 10	# 하트비트 시간 주기 초
	active_limit = int(BIGDATA_event_pickTime / sleep_cycle)	# 감지 대기 시간 10초
	error_limit = active_limit * 2 # 감지대기(BIGDATA_event_pickTime)에 두배 시간을 초과하면 오류 발생(초)
	event_hold = int(BIGDATA_event_holdTime) # 감지횟수
	
	count_sub = 0		# 이벤트 카운터
	count_rise = 0		# 이벤트 업 카운터
	event_curr = 0		# 지금 이벤트
	event_last = 0		# 과거 이벤트
	heart_event = 0		# 하트비트 이벤트
	rise_event = 0		# 업 이벤트
	error_event = 0		# 오류 이벤트
	block_event = 0
	
	setAlertTime = 0 ##  얼랏 발생시 타이머 적용
	setAudioTime = 0 ##  얼랏 발생시 타이머 적용
	
	count_shut = 0 ## 스넵샷 횟수 요청 - BIGDATA_opt22
	
	while True:
		# event_curr = BIGDATA.input(BIGDATA_ID) # 현재 릴레이 상태를 읽어들인다.
		## 사용자 설정(BIGDATA_alarm_level)값(NC 또는 NO)에 따라 event_curr 값을 선언 한다. 
		if BIGDATA_alarm_level: ## NO: Normal Open
			if BIGDATA.input(BIGDATA_ID): # 현재 릴레이 상태를 읽어들인다.
				event_curr = 0 
			else: 
				event_curr = 1 
		else: ## NO: Normal Close
			if BIGDATA.input(BIGDATA_ID): # 현재 릴레이 상태를 읽어들인다.
				event_curr = 1 
			else: 
				event_curr = 0 

		rise_event = 0 ## 리셋 업 이벤트
		send_event = 0 ## 이벤트 전송 변수 초기화
		
		if event_last is event_curr: ## 이전과 현재이벤트와 같은 값이면 
			count_sub += 1 ## 이벤트지속 카운트업
		else: ## 이벤트가 바뀌면
			count_sub = 0 ## 이벤트지속 리셋
			
			## 연속적으로 동일한 이밴트란 가정에서 
			## 이벤트현재 값이 업이벤트 면
			if event_curr: # 업 이벤트로 바뀠으면
				rise_event = 1
				count_rise += 1 ## 업 이벤트 카운터 추가
				if BIGDATA_event_keepHole: ## 이밴트 횟수 주기 유지
					if (count_rise % event_hold) is 0: ## 허용횟수 배수이면 send_event 설정 
						send_event = 1
				else: ## 최초 허용횟수를 넘는 이벤트 부터 연속적으로  send_event 설정 
					if count_rise >= event_hold:
						send_event = 1
			
		heart_event = 0
		error_event = 0
		
		if event_curr:
			# 감지 상태이며 count_sub 가 error_limit 의 배수이면 센서오류 이밴트 발생
			if count_sub and count_sub > error_limit: # 샌서 단선 또는 전원 오류
				error_event = 1
		else:
			# 비감지 상태이며 count_sub가 heart_limit의 배수이면 하트비트 이밴트 발생
			if count_sub and (count_sub % heart_limit) is 0: # 정상 동작으로 주기에 따른 하트비트 발생
				heart_event = 1
				
			if count_sub and active_limit and (count_sub % active_limit) is 0: # 감지 대기 시간에 따른 이벤트 활성상황 종료
				count_rise = 0 # 리셋 업 카운터
				# logger.info('Reset by active_limit: %s %s' % (count_sub, active_limit))

		event_last = event_curr

		############################################################################################
		############################################################################################
		############################################################################################
		
		# 예약확인
		
		if rise_event: # 
			weekNo = datetime.datetime.today().weekday() # 현재의 주일번호 확인 Monday is 0 and Sunday is 6.
			if str(weekNo): # in BIGDATA_sensor_sensor_week: # BIGDATA_sensor_sensor_week를 어레이로 변환후 오늘의 주번호와 일치하는지 확인
				scheduleWeek = check_scheduledWeek_BIGDATA(myTableID, weekNo) # 주간 예약인지 확인
				block_event = scheduleWeek['cnt']
			if not block_event: # 주간 예약을 우선하고 아닌경우 일간 예약 확인
				scheduleDate = check_scheduledDate_BIGDATA(myTableID) # 일간 예약인지 확인
				block_event = scheduleDate['cnt']
		else:
			block_event = 0 ## 리셋
		
		if heart_event: # 하트 비트
			status=Event_type['idle']
			msg=Event_desc[status]
		elif rise_event: # 이벤트 비트 업
			if block_event: # 이벤트 비트 업
				status=Event_type['block']
				msg=Event_desc[status]
			else:
				status=Event_type['active']
				msg=Event_desc[status]
		elif error_event: # 오류 비트
			status=Event_type['error']
			msg=Event_desc[status]
		else:
			status=Event_type['init']
			msg=''
			
		if rise_event:
			# 예약에 의한 블럭 상태
			logger.info('%s # %s' % (msg, count_rise))
			if block_event:
				insertLogId = insert_event_log_BIGDATA(mySensorID,w_cfg_id,status,msg,w_eventValue,Event_desc[1]) # 이벤트 로그
		if status:
			insert_socket_status_UNION(BIGDATA_sensor_serial, BIGDATA_subject, BIGDATA_system_ip, BIGDATA_system_port, model=BIGDATA_sensor_model, board=ECOS_table_BIGDATA, tableID=myTableID, status=status, msg=msg)  # 소켓 유니온 전송
		
		###############################################
		## 조건에 따른 관제에 이벤트 전송, 스넵샛, 알람
		if send_event: # 이벤트 비트 업

			####### 실시간 모니터링을 위한 이벤트 전송 #######
			if BIGDATA_system_ip and BIGDATA_table_PortIn:
				returnValue = insert_socket_monitor_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, BIGDATA_sensor_lat_s, BIGDATA_sensor_lng_s, BIGDATA_sensor_lat_e, BIGDATA_sensor_lng_e, BIGDATA_system_ip, BIGDATA_table_PortIn)
						
			####### 실시간 알람 접점신호 발생 #######
			if BIGDATA_alert_Port and BIGDATA_alert_Value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( BIGDATA_alert_Value:)
				if setAlertTime:
					# 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
					pass
				else:
					setAlertTime = datetime.datetime.now()
					Process(target=alertOut, args=(BIGDATA_alert_Port,BIGDATA_alert_Value)).start()
					w_eventStatus = "Alarm out %s Seconds to port %s." % (BIGDATA_alert_Value,BIGDATA_alert_Port)
					logger.info(w_eventStatus)
										
			####### 오디오 경고방송 #######
			if BIGDATA_audio_name and BIGDATA_audio_time: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( BIGDATA_audio_time:)
				## audioOutTime -> audioFile audioTime (파일명, 시간)
				# audio_name_mp3 = "%s/%s %s"%(share["path"]["audio"],BIGDATA_audio_name, BIGDATA_audio_time)
				# Process(target=audioOutTime, args=(audio_name_mp3,)).start() # 참고 https://stackoverflow.com/questions/22997802/multiprocessing-typeerror
				
				## audioOut -> audioVolume audioFile (볼륨, 파일명)
				audio_name_mp3 = "%s %s/%s"%(share["mPlayer"]["omxplayer"]["volume"],share["path"]["audio"],BIGDATA_audio_name)
				if setAudioTime:
					## 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
					pass
				else:
					logger.info("Audio Warning.. %s"%BIGDATA_audio_name)
					setAudioTime = datetime.datetime.now()
					Process(target=audioOut, args=(audio_name_mp3,)).start() # 참고 https://stackoverflow.com/questions/22997802/multiprocessing-typeerror
			####### 오디오 경고방송 #######

			####### 스냅샷 실행 #######
			if BIGDATA_url1:
				w_cfg_id = 0 # 0: No error, 1: Error
				
				count_shut = BIGDATA_opt22
					
				### Background PROCESS with HTTPDigestAuth
				### 고급 카메라인 경우 HTTPDigestAuth기능이 적용되며 
				### 저속인경우 HTTPDigestAuth와 워터마크 기능이 불가능 하다. 
				
				eventName = getImgPath(img_data_sub) # image가 저장될 경로를 가지고 온다
				imageInfo = "Sensor ID:%s %s"%(BIGDATA_sensor_serial, eventName[-22:]) # 한글 지원 않됨
				try:
					# ## 저속 장비인경우 HTTPDigestAuth와 워터마크 기능이 불가능 하다.
					# result = getSnapshot(BIGDATA_url1, eventName)
					## 고속 고급 장비인경우 HTTPDigestAuth와 워터마크 기능이 가능함
					result = authRequest.download_image_n_wmark(BIGDATA_url1, eventName, imageInfo, BIGDATA_opt91)
				except:
					result = "Snapshot or Watermark Error %s"%BIGDATA_url1
					
				logger.info(result)  # get the return value from your function.
				tmp_path = eventName[21:] # 머리부분 /var/www/html/its_web을 제거
				tmp_name = eventName[-22:]
				w_eventShotURL = "%s%s"%(BIGDATA_system_ip,tmp_path)
				w_eventStatus = "<a href=%s target=_blank>%s</a>" % (tmp_path,tmp_name) 
				### Background PROCESS with HTTPDigestAuth

				logger.info(w_eventStatus)
				
			###################################
			## 관제시스템에 이벤트 로그를 전송 한다.
			###################################
			## Http Request
			if BIGDATA_url3: ## Send _get
				payload = {'info': '1'} ## payload = {'key1': 'value1', 'key2': 'value2'}
				r = authRequest.requests_get(BIGDATA_url3, BIGDATA_opt93, payload) 
				logger.info("requests_get %s"%r.status_code)
			if BIGDATA_url4: ## Send _post
				payload = {'query': 'limit'} ## payload = {'key1': 'value1', 'key2': 'value2'}
				r = authRequest.requests_post(BIGDATA_url4, BIGDATA_opt94, payload) 
				logger.info("requests_post %s"%r.status_code)

			###################################
			## PTZ 카메라에 프리셋 전송 한다.
			###################################
			if BIGDATA_wr_4_URL and BIGDATA_wr_6_ID: # 카메라 연동 프리셋 전송
				result = send_camera_PRESET(BIGDATA_wr_4_URL, BIGDATA_wr_5_ENC, BIGDATA_wr_6_ID)
				if result:
					logger.info("sent Preset to %s %s"%(BIGDATA_wr_4_URL, result))
				else:
					logger.warning("Error, Check URL %s"%(BIGDATA_wr_4_URL))
					
			if BIGDATA_wr_7_URL and BIGDATA_wr_9_ID: # 카메라 연동 프리셋 전송
				result = send_camera_PRESET(BIGDATA_wr_7_URL, BIGDATA_wr_8_ENC, BIGDATA_wr_9_ID)
				if result:
					logger.info("sent Preset to %s %s"%(BIGDATA_wr_7_URL, result))
				else:
					logger.warning("Error, Check URL %s"%(BIGDATA_wr_4_URL))
									
			####### 관제시스템에 이벤트 로그를 전송 #######
			if BIGDATA_host_Addr and BIGDATA_host_Port:
				returnValue = insert_socket_log_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, BIGDATA_sensor_lat_s, BIGDATA_sensor_lng_s, BIGDATA_sensor_lat_e, BIGDATA_sensor_lng_e, BIGDATA_host_Addr, BIGDATA_host_Port, count_rise, block_event, status, msg, w_eventShotURL, BIGDATA_url2)
				w_eventId = Event_type['post']
				w_eventDesc = Event_desc[w_eventId]
				if(returnValue == 0):
					w_cfg_id = 1 # 0: No error, 1: Error
					w_eventStatus = 'Connection or Timeout Error %s:%s' % (BIGDATA_host_Addr,BIGDATA_host_Port)
				else: # 로그 소켓 전송 결과 값
					w_cfg_id = 0 # 0: No error, 1: Error
					w_eventStatus = 'Sent to %s:%s' % (BIGDATA_host_Addr,BIGDATA_host_Port)
				logger.info(w_eventStatus)
				insertLogId = insert_event_log_BIGDATA(mySensorID,w_cfg_id,w_eventId,w_eventDesc,w_eventValue,w_eventStatus) # 이벤트 로그
			####### 관제시스템에 이벤트 로그를 전송 #######
			if BIGDATA_host_Addr2 and BIGDATA_host_Port2:
				returnValue = insert_socket_log_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, BIGDATA_sensor_lat_s, BIGDATA_sensor_lng_s, BIGDATA_sensor_lat_e, BIGDATA_sensor_lng_e, BIGDATA_host_Addr2, BIGDATA_host_Port2, count_rise, block_event, status, msg, w_eventShotURL, BIGDATA_url2)
				w_eventId = Event_type['post']
				w_eventDesc = Event_desc[w_eventId]
				if(returnValue == 0):
					w_cfg_id = 1 # 0: No error, 1: Error
					w_eventStatus = 'Connection or Timeout Error %s:%s' % (BIGDATA_host_Addr2,BIGDATA_host_Port2)
				else: # 로그 소켓 전송 결과 값
					w_cfg_id = 0 # 0: No error, 1: Error
					w_eventStatus = 'Sent to %s:%s' % (BIGDATA_host_Addr2,BIGDATA_host_Port2)
				logger.info(w_eventStatus)
				insertLogId = insert_event_log_BIGDATA(mySensorID,w_cfg_id,w_eventId,w_eventDesc,w_eventValue,w_eventStatus) # 이벤트 로그
			
			###########################	
		else:
			###########################	
			## 이벤트발생에 따른 추가사진 생성루틴
			## 기본적으로 이밴트 발생후 사용자 요청에 따른 추가 스넵샷을 찍는 루틴
			if(count_shut):
				count_shut -= 1
				eventName = getImgPath(img_data_sub) # image가 저장될 경로를 가지고 온다
				imageInfo = "Sensor ID:%s %s"%(BIGDATA_sensor_serial, eventName[-22:]) # 한글 지원 않됨
				try:
					# ## 저속 장비인경우 HTTPDigestAuth와 워터마크 기능이 불가능 하다.
					# result = getSnapshot(BIGDATA_url1, eventName)
					## 고속 고급 장비인경우 HTTPDigestAuth와 워터마크 기능이 가능함
					result = authRequest.download_image_n_wmark(BIGDATA_url1, eventName, imageInfo, BIGDATA_opt91)
				except:
					result = "Snapshot or Watermark Error %s"%BIGDATA_url1
					
				tmp_path = eventName[21:] # 머리부분 /var/www/html/its_web을 제거
				tmp_name = eventName[-22:]
				w_eventShotURL = "%s%s"%(BIGDATA_system_ip,tmp_path)
				w_eventStatus = "<a href=%s target=_blank>%s</a>" % (tmp_path,tmp_name)
				
				####### 관제시스템에 이벤트 로그를 전송 #######
				if BIGDATA_host_Addr and BIGDATA_host_Port:
					returnValue = insert_socket_log_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, 0, 0, 0, 0, BIGDATA_host_Addr, BIGDATA_host_Port, count_rise, block_event, 1, msg, w_eventShotURL, BIGDATA_url2)
				####### 관제시스템에 이벤트 로그를 전송 #######
				if BIGDATA_host_Addr2 and BIGDATA_host_Port2:
					returnValue = insert_socket_log_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, 0, 0, 0, 0, BIGDATA_host_Addr2, BIGDATA_host_Port2, count_rise, block_event, 1, msg, w_eventShotURL, BIGDATA_url2)
			###########################	

		## 실시간 알람 접점신호 발생 ##
		## 시간차(0:00:10.558780)를 초로 변환(total_seconds()) > 설정된 지속시간값(초)
		if BIGDATA_alert_Value and setAlertTime:
			if (datetime.datetime.now() - setAlertTime).total_seconds() > BIGDATA_alert_Value:
				setAlertTime = 0
		if BIGDATA_audio_time and setAudioTime:
			if (datetime.datetime.now() - setAudioTime).total_seconds() > BIGDATA_audio_time:
				setAudioTime = 0
			
		# 사용자 환경 변경 값을 실시간 적용을 위한 기능으로 변경된 데이터베이스 값을 기반으로 하며
		# 연속되는 이밴트로 전환되는 시점에 한번 값을 읽어들인다.
		if count_sub and active_limit and (count_sub % active_limit) is 0:
			# w_eventStatus = 'Idle sensor:%s' % (int(count_sub) + 1)
			# logger.info(w_eventStatus)
			if(error_event):
				logger.critical('Critical Error: Check Sensor or Cable')
			else:
				logger.info('Idle : %s' % conv_sec_2_time(count_sub/sec_per_times))

			if BIGDATA_host_Addr and BIGDATA_host_Port: # 하트비트 전송
				returnValue = insert_socket_log_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, BIGDATA_sensor_lat_s, BIGDATA_sensor_lng_s, BIGDATA_sensor_lat_e, BIGDATA_sensor_lng_e, BIGDATA_host_Addr, BIGDATA_host_Port, count_rise, block_event, status, msg)
			if BIGDATA_host_Addr2 and BIGDATA_host_Port2: # 하트비트 전송
				returnValue = insert_socket_log_BIGDATA(BIGDATA_sensor_serial, BIGDATA_subject, BIGDATA_sensor_lat_s, BIGDATA_sensor_lng_s, BIGDATA_sensor_lat_e, BIGDATA_sensor_lng_e, BIGDATA_host_Addr2, BIGDATA_host_Port2, count_rise, block_event, status, msg)
			
			instant_set = read_field_w_cfg_sensor_BIGDATA(myTableID) # 임시정지 모드 이면 1 
			for row in instant_set:
				BIGDATA_sensor_reload = row["w_sensor_reload"]	# `w_instant_reload` TINYINT(1) - 프로그램 재시동

				if BIGDATA_sensor_reload: # 설정값 변경 실시간 적용
					set_reload_w_cfg_sensor_BIGDATA(myTableID) # w_sensor_reload 값을 회복시킨다.
					logger.info('Restart Program by user command')
					#### 재 시작 상태값 저장
					w_eventId = Event_type['reload']
					w_eventDesc = Event_desc[w_eventId]
					w_eventStatus = 'Reload sensor'

					insertLogId = insert_event_log_BIGDATA(mySensorID, w_cfg_id, w_eventId, w_eventDesc, w_eventValue, w_eventStatus) # 이벤트 로그
					logger.info(w_eventStatus)
					###################
					restart_myself() # 프로그램 재 시작
				

		time.sleep(sleep_cycle)