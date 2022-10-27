#!/usr/bin/env python
# -*- coding: utf-8 -*-  

##################################################
# BIGDATA Control and Managment
##################################################

from module import *

def main():
	# BIGDATA Relay Connection - 센서 설정 보드로 부터 읽은 필요한 값을 변수로 포함하여 실행 한다.
	# 센서 아이디, 센서 타임아웃, 위도, 경도 - w_sensor_id, w_sensor_timeout, w_sensor_lat_s, w_sensor_lng_s
	# 위도 경도는 관제 모니터링을 위한 임시 값으로 사용하기 위함
	w_cfg_sensor_list_BIGDATA = read_table_w_cfg_sensorID_BIGDATA()
	for row in w_cfg_sensor_list_BIGDATA:
	
		###########################
		## 프러덕트 라이센스 확인 - 시작
		license = row["w_license"]
		serial = get_serial()
		device = row["w_device_id"]
		passwd = op_pass
		mixedStr = serial + device + passwd
		hash = sha256(mixedStr).hexdigest()
		if license == hash:
			print("\n%s"%(row["wr_subject"])+Y+" : Pass Product License")
		else:
			print("\n%s"%(row["wr_subject"])+" : No Product License")
			continue 
		# print(Y+"%s : %s : %s"%(row["wr_subject"],row["w_sensor_serial"],row["w_device_id"]))
		## 프러덕트 라이센스 확인 - 종료
		###########################
	
		# Node Js를 통한 실시간 모니터링 입력 포트 http://localhost:myPortIn
		BIGDATA_sensor_noOfZone = row["w_sensor_noOfZone"]
		
		BIGDATA_loc_lat_s = row["w_sensor_lat_s"]
		BIGDATA_loc_lng_s = row["w_sensor_lng_s"]
		BIGDATA_loc_lat_e = row["w_sensor_lat_e"]
		BIGDATA_loc_lng_e = row["w_sensor_lng_e"]

		ECOS_system_port = row["w_system_port"]
		ECOS_system_portOut = ECOS_system_port + 2
		
		BIGDATA_table_PortIn = row["w_table_PortIn"]
		BIGDATA_table_PortOut = row["w_table_PortOut"]

		BIGDATA_node = '%s %s %s 1 %s %s %s %s' % (BIGDATA_table_PortIn, BIGDATA_table_PortOut, BIGDATA_sensor_noOfZone, BIGDATA_loc_lat_s, BIGDATA_loc_lng_s, BIGDATA_loc_lat_e, BIGDATA_loc_lng_e) # node table.js 8008 9008 100 1
		result = run_demon_BIGDATA_table(BIGDATA_node)
		# print('\tRunning Table: %s' % result)		
		
		ECOS_exeName = "%s" % row["wr_id"]
		kill_demon_BIGDATA(ECOS_exeName)
		# time.sleep(1)
		result = run_BIGDATA(ECOS_exeName)
		# print('\tRunning BIGDATA: %s \n' % result)
		
	exit()
	

if __name__ == '__main__':

	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print share["file"]["html_src"]
	## 예: print share["mysql"]["host"]
	share = readConfig('/home/pi/common/config.json')
	owner = readConfig('/home/pi/BIGDATA/config.json') 
	# print share["mysql"]["pass"]
		
	err_max = 20
	while True: # 데이터베이스 확인
		if database_test(share["mysql"]["host"], share["mysql"]["user"], share["mysql"]["pass"], share["mysql"]["name"]): 
			print("*** PASS ***\n\tDatabase connected.") # 데이터베이스 쿼리 오류
			break
		else:
			print("*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ...") # 데이터베이스 쿼리 오류
			time.sleep(1)
			err_max=err_max-1
			if not err_max: exit('Time out')

	kill_demon_BIGDATA_table()


	# ###########################
	# ## 시스템 라이센스 확인 - 시작
	# # /tmp/license_hash가 manager의 mb_1의 값과 일치하는지 확인 한다.
	# license = str(itsMemberConfig('mb_1')['mb_1']).strip() # 라이센스 확인
	# if os.path.isfile('/tmp/'+license):
	# 	print("\nPass ITS License\n")
	# else:
	# 	print("\nNot Found ITS License\n"+"\tPlease Call to Service Provider!!")
	# 	exit() 
	# ## 시스템 라이센스 확인 - 종료
	# ###########################

	
	make_table_BIGDATA(ITS_bigdata_path+"/table_templet.html", ITS_bigdata_path+"/table_BIGDATA.html") # index.html 생성후 SVG 파일 적용

	main()