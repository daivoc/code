#!/usr/bin/env python
# -*- coding: utf-8 -*-  

######################################################################
# 본 소스코드는 OPTEX Laser Sensor Model: RLS 용 프로그램 입니다.
######################################################################

from config_sensor import *
from module_for_optex import *
from module_for_mysql import *

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
err_max = ERROR_check_cnt_max

if __name__ == '__main__':

	# 초기 화면 내용 삭제 
	# clear_screen()

	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(1)
			err_max=err_max-1
			if not err_max: exit('Time out')
			
	kill_demon_PARKING_table()
	kill_demon_RLS()
	w_cfg_sensor_list_ID = read_table_w_cfg_sensorID()
	if w_cfg_sensor_list_ID:
		for row in w_cfg_sensor_list_ID:
			ECOS_myID = row["wr_id"] 
			ECOS_capacity_max = row["w_capacity_max"]
			
			ECOS_loc_lat_s = row["w_sensor_lat_s"]
			ECOS_loc_lng_s = row["w_sensor_lng_s"]
			ECOS_loc_lat_e = row["w_sensor_lat_e"]
			ECOS_loc_lng_e = row["w_sensor_lng_e"]

			ECOS_system_port = row["w_system_port"]
			ECOS_system_portOut = ECOS_system_port + 2

			ECOS_virtual_Addr = row["w_virtual_Addr"]
			ECOS_sensor_Addr = row["w_sensor_Addr"]
			ECOS_sensor_Addr2 = row["w_sensor_Addr2"]

			ECOS_table_PortIn = row["w_table_PortIn"]
			ECOS_table_PortOut = row["w_table_PortOut"]

			if ECOS_myID:
				if check_sensor(ECOS_virtual_Addr):
					exit(R+"*** Ping Test ERROR ***\n\tPlease check virtual IP(%s) address" % ECOS_virtual_Addr+W)
				else:
					print(G+"*** Ping Test PASS ***\n\tConfirmed virtual IP(%s) existence." % ECOS_virtual_Addr+W)
				
				if ECOS_sensor_Addr:
					if check_sensor(ECOS_sensor_Addr):
						exit(R+"*** Ping Test ERROR ***\n\tPlease check sensor's IP(%s) address." % ECOS_sensor_Addr+W)
					else:
						print(G+"*** Ping Test PASS ***\n\tConfirmed sensor IP(%s) existence." % ECOS_sensor_Addr+W)
				
				if ECOS_sensor_Addr2:
					if check_sensor(ECOS_sensor_Addr2): # 두번째 센서는 선택 사항이며 등록된 아이피 테스트 오류가 발생 하면 아이피 값을 0으로 설정 
						print(R+"*** Disable 2nd Sensor ***\n\tPlease check sensor's IP(%s) address." % ECOS_sensor_Addr2+W)
						ECOS_sensor_Addr2 = 0 # 0 값은 센서가 없음을 의미 한다.
					else:
						print(G+"*** Ping Test PASS ***\n\tConfirmed sensor IP(%s) existence." % ECOS_sensor_Addr2+W)
						
				ECOS_javaName = '%s %s' % (ECOS_table_PortIn, ECOS_table_PortOut)
				print('Running nodeJs: %s' % run_demon_PARKING_table(ECOS_javaName))

				ECOS_exeName = 'optex_PARKING.pyc %s' % ECOS_myID # python -u /home/pi/optex/optex_PARKING.pyc 7
				print('Running optex_PARKING: %s \n' % run_demon_RLS(ECOS_myID))
				
	else:
		print "Error from read_table_w_cfg_sensorID(), Check Sensor's Config..."
		
	exit()