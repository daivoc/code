#!/usr/bin/env python
# -*- coding: utf-8 -*-  

######################################################################
# 본 소스코드는 OPTEX Microwave Sensor Model: SPEED 용 프로그램 입니다.
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

	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(1)
			err_max=err_max-1
			if not err_max: exit('Time out')
			
	kill_demon_SPEED_table()
	kill_demon_SPEED()
	w_cfg_sensor_list_BSS = read_table_w_cfg_sensorID_BSS()
	if w_cfg_sensor_list_BSS:
		for row in w_cfg_sensor_list_BSS:
			ECOS_myID = row["wr_id"]
			ECOS_sensor_noOfZone = row["w_sensor_noOfZone"]
			
			ECOS_loc_lat_s = row["w_sensor_lat_s"]
			ECOS_loc_lng_s = row["w_sensor_lng_s"]
			ECOS_loc_lat_e = row["w_sensor_lat_e"]
			ECOS_loc_lng_e = row["w_sensor_lng_e"]

			ECOS_system_port = row["w_system_port"]
			ECOS_system_portOut = ECOS_system_port + 2

			ECOS_virtual_Addr = row["w_virtual_Addr"]
			ECOS_sensor_Addr = row["w_sensor_Addr"]

			ECOS_table_PortIn = row["w_table_PortIn"]
			ECOS_table_PortOut = row["w_table_PortOut"]

			if ECOS_myID:
				while True: # 가상 아이피 확인
					if check_sensor(ECOS_virtual_Addr):
						print(R+"*** ERROR ***\n\tPlease check Wits's virtual IP address. It must be %s. Waiting ..." % ECOS_virtual_Addr+W)
						time.sleep(1)
						err_max=err_max-1
						if not err_max: exit('Time out')
					else:
						print(G+"*** PASS ***\n\tConfirmed virtual IP %s existence." % ECOS_virtual_Addr+W)
						break
					
				while True: # 센서 아이피 확인
					if check_sensor(ECOS_sensor_Addr):
						print(R+"*** ERROR ***\n\tPlease check sensor's IP address. It must be %s. Waiting ..." % ECOS_sensor_Addr+W)
						time.sleep(1)
						err_max=err_max-1
						if not err_max: exit('Time out')
					else:
						print(G+"*** PASS ***\n\tConfirmed sensor %s existence." % ECOS_sensor_Addr+W)
						break

				ECOS_javaName = '%s %s %s 1 %s %s %s %s' % (ECOS_table_PortIn, ECOS_table_PortOut, ECOS_sensor_noOfZone, ECOS_loc_lat_s, ECOS_loc_lng_s, ECOS_loc_lat_e, ECOS_loc_lng_e)
				print('Running nodeJs: %s' % run_demon_SPEED_table(ECOS_javaName))

				ECOS_exeName = 'optex_SPEED.pyc %s' % ECOS_myID # python -u /home/pi/optex/optex_speed.pyc 7
				print('Running optex_SPEED: %s \n' % run_demon_SPEED(ECOS_myID))
				
	else:
		print "Error from read_table_w_cfg_sensorID_BSS()"
		
	exit()