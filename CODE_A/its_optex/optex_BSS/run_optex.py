#!/usr/bin/env python
# -*- coding: utf-8 -*-  

######################################################################
# 본 소스코드는 OPTEX Microwave Sensor Model: BSS01 용 프로그램 입니다.
######################################################################

# from config_db import *
# from module_for_optex import *
# from module_for_mysql import *

from module import *

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # Cyan# Cyan

err_max = ERROR_check_cnt_max

if __name__ == '__main__':

	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(30) ## 데이터베이스가 준비된 상태가 아니면 주기(30초)적인 재시도
			err_max=err_max-1
			if not err_max: exit('Time out')
			
	kill_demon_BSS01() # python
	kill_demon_BSS01_map() # nodeJs

	# ###########################
	# ## 시스템 라이센스 확인 - 시작
	# # /tmp/license_hash가 manager의 mb_1의 값과 일치하는지 확인 한다.
	# license = str(itsMemberConfig('mb_1')['mb_1']).strip() # 라이센스 확인
	# if os.path.isfile('/tmp/'+license):
	# 	print(C+"\nPass ITS License\n"+W)
	# else:
	# 	print(R+"\nNot Found ITS License\n"+W+"\tPlease Call to Service Provider!!")
	# 	exit() 
	# ## 시스템 라이센스 확인 - 종료
	# ###########################
	
	w_cfg_sensor_list_BSS = read_table_w_cfg_sensorID_BSS()
	countOfDevice = len(w_cfg_sensor_list_BSS)
	totalOfDevice = countOfDevice
	if w_cfg_sensor_list_BSS:
		for row in w_cfg_sensor_list_BSS:
			ECOS_myID = str(row["wr_id"])
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

			set_reload_w_cfg_reload_BSS(ECOS_myID) # 재시동 필드를 회복시킨다.
			
			make_table_map_html(ITS_map_source,ITS_map_target,ITS_map_content) # SVG 파일 적용  ###### - bss map
			while True: # 가상 아이피 확인
				if check_sensor(ECOS_virtual_Addr):
					print(R+"*** ERROR ***\n\tPlease check Wits's virtual IP address. It must be %s. Waiting ..." % ECOS_virtual_Addr+W)
					time.sleep(30) ## 네트워크가 준비된 상태가 아니면 주기(30초)적인 재시도
					err_max=err_max-1
					if not err_max:
						err_max = ERROR_check_cnt_max
						print('Time out')
						break
				else:
					print(G+"*** PASS ***\n\tConfirmed virtual IP %s existence." % ECOS_virtual_Addr+W)
					while True: # 센서 아이피 확인
						if check_sensor(ECOS_sensor_Addr):
							print(R+"*** ERROR ***\n\tPlease check sensor's IP address. It must be %s. Waiting[%s] ..." % (ECOS_sensor_Addr, err_max)+W)
							time.sleep(30) ## 센서가 준비된 상태가 아니면 주기(30초)적인 재시도
							err_max=err_max-1
							if not err_max: 
								err_max = ERROR_check_cnt_max
								print('Time out')
								break
						else:
							print(G+"*** PASS ***\n\tConfirmed sensor %s existence." % ECOS_sensor_Addr+W)
							ECOS_javaName = '%s %s %s 1 %s %s %s %s' % (ECOS_table_PortIn, ECOS_table_PortOut, ECOS_sensor_noOfZone, ECOS_loc_lat_s, ECOS_loc_lng_s, ECOS_loc_lat_e, ECOS_loc_lng_e)
							print('Running nodeJs: %s' % run_demon_BSS01_map(ECOS_javaName)) ###### - bss map
							# print('Running nodeJs: %s' % run_demon_BSS01_table(ECOS_javaName))
							ECOS_exeName = 'optex_BSS01.pyc %s' % ECOS_myID # python -u /home/pi/optex/optex_BSS01.pyc 7
							print('Running optex_BSS01: %s \n' % run_demon_BSS01(ECOS_myID))
							
							countOfDevice -= 1
							break
					break
	else:
		print "Error from read_table_w_cfg_sensorID_BSS()"
		
	print "Device\n Total: %s Error: %s" % (totalOfDevice, (countOfDevice))
	
	exit()