#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from module import *
			
def main():
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ## 기존에 진행하는 포트가 살아있어도 진행요구. Error [Errno 98] Address already in use
			s.bind(('', cfg["interface"]["portIn"])) ## 'localhost'로 선언하면 외부 아이피에서 접근불가능 - 블랭크 ''로 하면 외부접근 가능
			s.listen(10)
			# conn, addr = s.accept()
			# print ('\n\tOpened Py Port Main: %s')%cfg["interface"]["portIn"]
			logger.info("Socket connected Py Port Main: %s"%cfg["interface"]["portIn"]) # 데이터베이스 쿼리 오류
		except:
			s.close()
			print ("\n\tCaught exception socket.error : %s" % exc)
			print ("\tSocket connect error. %s times left. Waiting ..."%err_max) # 데이터베이스 쿼리 오류
			logger.critical("Socket connect error. %s times left. Waiting ..."%err_max) # 데이터베이스 쿼리 오류
			err_max=err_max-1
			if not err_max:
				exit('Time out')

		recvBuffer = 1024 ## 1024  ## Normally 1024, but we want fast response
		conn, addr = s.accept()
		
		## 클라이언트에서 지속적으로 보내는 데이터가 버퍼에 싸이게 되는데
		## 본 프로그램 실행시 과거자료를 삭제함으로서 오류를 방지 한다.
		## 완벽하다고 볼수 없는 기능임
		# print clearBuffer(conn, recvBuffer) ## 기존의 버퍼를 비운다.
		clearBuffer(conn, recvBuffer) ## 기존의 버퍼를 비운다.

		while True:
			data = conn.recv(recvBuffer)
			if not data: break
			# print data

			try:
				dataList = data.split('&')
				clientIP = dataList[0:1] ## IP 추출
				queryCmd = dataList[1:] ## 명령문 추출
				
				if queryCmd[0] == "cmd=camRestart": ## 재실행 요청 수용
					logger.info('Command Action: %s %s'%(clientIP[0],queryCmd[0]))
				else: ## 카메라 명령
					# print clientIP, queryCmd
					## 카메라로 명령문 전송후 리턴값을 받아온다.
					## queryCmd = queryCmd.replace(clientIP, '') ## 왜 아이피가 붙어서 나오는지 이유를 아직 모름 (강제 삭제)
					retuenValue = camera.cameraPTZ(queryCmd, 1, cfg["camera"]["addr"], cfg["camera"]["user"], cfg["camera"]["pass"])
					## 기본으로 받은 값에 클라이언트 정보와 요청 명령 정보를 추가 한후 명령 conn.send을 통해 CAM.js로 전송한다 
					retuenValue['reqFrom'] = clientIP[0] ## 관련정보 요청 클라이엄트
					
					if queryCmd[0] == "query=position": ## 매초 단위로 position을 요청함으로 제외
						pass 
					else:
						logger.info('Camera Action: %s %s'%(retuenValue['reqFrom'],queryCmd))
			except:
				logger.warning('Camera Communication Error')
				break

			## 카메라로 부터 받은 자료(retuenValue)를 
			## JSON 형식으로 변환후 클라이언트(CAM.js)에 정보값 리턴(conn.send)
			try: 
				for pair in queryCmd: ## queryCmd는 리스트 형식이어서 이를 푼다음 각각 등록 한다. query=position => "query": "position"
					x,y = pair.split("=")
					retuenValue[x] = y
					data_dump = json.dumps(retuenValue) ## JSON 형식 변환 
				# print data_dump
				conn.send(data_dump)  # echo
			except:
				break
		conn.close()
	s.close()
	###### 제어 포트(cfg["interface"]["portIn"])로 접수된 명령 해석 및 실행 ######


if __name__ == '__main__':

	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	cfg = readConfig()
						
	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	if not os.path.exists(cfg["path"]["log"]): # cfg["path"]["log"] 폴더 생성
		os.makedirs(cfg["path"]["log"])
	if not os.path.exists(cfg["path"]["log"]+cfg["path"]["home"]): # cfg["path"]["log"] 폴더 생성
		os.makedirs(cfg["path"]["log"]+cfg["path"]["home"])
	logger = logging.getLogger(cfg["path"]["home"][1:]) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = cfg["path"]["log"]+cfg["path"]["home"]+cfg["path"]["home"]+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info("START")
	# logger.debug("===========================")
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	# logger.debug("===========================")
	# logger.info("TEST END!")
	############ logging ################
		
	cfg["system"]["ip"] = get_ip_address('eth0') ## 변수 선언

	# ###### 시스템 라이센스 확인 ######
	# ## /tmp/license_hash가 manager의 mb_1의 값과 일치하는지 확인 한다.
	# if os.path.isfile('/tmp/'+cfg["license"]["manager_key"]):
	# 	license = 1
	# 	logger.info('Pass ICC Manager License')
	# 	print("\n\tPass ICC Manager License")
	# else:
	# 	license = 0
	# 	logger.warning('Not Found ICC Manager License')
	# 	print("\n\tNot Found ICC Manager License")
	# 	# exit() 
	# ###### 시스템 라이센스 확인 ######
	
	
	###### 로컬 영영의 카메라 찾기 ######
	# print ("\n\tFind Camera in Local Network")
	# cameraList = check_opened_port('CAMERA')
	# cameraList = ''
	# if len(cameraList):
	# 	cfg["camera"]["addr"] = cameraList[0]
	# 	print ("\n\tSet Camera's IP %s"%cfg["camera"]["addr"])
	# 	logger.info("Set Camera's IP %s"%cfg["camera"]["addr"])
	# else:
	# 	## 실패하면 기본 카메라 주소를 유지 한다.
	# 	if not cfg["camera"]["addr"]: 
	# 		cfg["camera"]["addr"] = '' ## 변수 선언
	# 	print ("\n\tNot Found Camera in Local Area")
	# 	logger.warning("Not Found Camera in Local Area")
	cfg["camera"]["addr"] = '192.168.0.113'
	###### 로컬 영영의 카메라 찾기 ######

	# ###### PTZ IP 카메라 확인 ######

	###### 브랜드별 카메라 프로그램 불러오기 ######
	camera = __import__('model.%s'%cfg["camera"]["api"], fromlist=['model.%s'%cfg["camera"]["api"]]) # ex) => from model.AXIS_VAPIX_V3 import *
	###### 브랜드별 카메라 프로그램 불러오기 ######

	###### 카매라 테스트 겸 이미지 해상도 읽고 index.html(cfg["file"]["html_dst"]) 생성 ######
	## http://192.168.0.38/axis-cgi/imagesize.cgi?camera=1 -> image width = 1920, image height = 1080
	try:
		retuenValue = camera.cameraIMAGESIZE(1, cfg["camera"]["addr"], cfg["camera"]["user"], cfg["camera"]["pass"])
		cfg["camera"]["resolution"]["x"] = retuenValue['image width'] ## 가로  ## 변수 선언
		cfg["camera"]["resolution"]["y"] = retuenValue['image height'] ## 세로  ## 변수 선언
		###### Node.js index.html 생성을 위한 바탕 이미지 와 비데오 링크 ######
		# imageURL = 'http://%s%s'%(cfg["camera"]["addr"],cfg["camera"]["camImage"]) # /axis-cgi/jpg/image.cgi"
		videoURL = 'http://%s%s'%(cfg["camera"]["addr"],cfg["camera"]["camVideo"]) # /axis-cgi/mjpg/video.cgi
		###### Node.js index.html 생성을 위한 바탕 이미지 와 비데오 링크 ######
		logger.info('Success connect camera. %s'%videoURL)
	except:
		cfg["camera"]["resolution"]["x"] = 0
		cfg["camera"]["resolution"]["y"] = 0
		videoURL = 'http://'+cfg["system"]["ip"]+'/theme/ecos-its_optex/img/ptzCamera.png'
		logger.warning('False connect camera. %s'%videoURL)
		
	## index.html 생성후 SVG 파일 적용	
	make_table_CAM(cfg["file"]["html_src"], cfg["file"]["html_dst"], videoURL, cfg["camera"]["resolution"]["x"], cfg["camera"]["resolution"]["y"], cfg["path"]["common"])
	###### 카매라 이미지 해상도 읽기 ######
	
	###############################################
	## 파일 config.json내용 저장
	saveConfig(cfg) ## 저장

	############ 이미지 파일 폴더 초기화 data/images ################
	if not os.path.exists(cfg["path"]["img"]): # cfg["path"]["img"] 폴더 생성
		os.makedirs(cfg["path"]["img"])
	# 센서 이벤트 스크린샷 이미지 저장 폴더명
	img_data_sub = cfg["path"]["img"] + "/" + cfg["camera"]["serial"]
	if not os.path.exists(img_data_sub): # cfg["path"]["img"] 내의 서브 사진 폴더 생성
		os.makedirs(img_data_sub)
	############ 이미지 파일 폴더 초기화 data/images ################

	# ############ Create Transaction Log 테이블 생성################
	# returnMsg = create_table_w_log_camera_CAM(cfg["camera"]["serial"]) # 테이블 생성 - 반환값
	# # print returnMsg
	# ############ Create Transaction Log 테이블 생성################

	############ 카메라 모니터링을 위한 독립 프로그램 ############
	###### Nodejs 주 프로그램 실행 ######
	result = run_demon_CAM_js(cfg["camera"]["addr"])
	logger.info('Running CAM Node: %s' % result)
	############ 카메라 모니터링을 위한 독립 프로그램 ############

	main()
