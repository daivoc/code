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

	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(1)
			err_max=err_max-1
			if not err_max: exit('Time out')
			
	w_cfg_sensor_list_ID = read_table_w_cfg_sensorID() # table_RLS = c.ECOS_table_prefix+c.ECOS_table_RLS
	countOfDevice = len(w_cfg_sensor_list_ID)
	totalOfDevice = countOfDevice
	if w_cfg_sensor_list_ID:
		for row in w_cfg_sensor_list_ID:
			myTableID = str(row["wr_id"])
			sensor_IP = row["w_sensor_Addr"]
			sensor_Subject = row["wr_subject"]
			sensor_Serial = row["w_sensor_serial"]

			set_reload_w_cfg_reload(myTableID) # 재시동 필드를 회복시킨다.
			kill_demon_check_RLS(myTableID)
			
			if sensor_IP:
				while True: # 센서 아이피 확인
					if check_sensor(sensor_IP):
						print(R+"*** ERROR ***\n\tPlease check sensor's IP address. It must be %s. Waiting[%s] ..." % (sensor_IP, err_max)+W)
						time.sleep(1)
						err_max=err_max-1
						if not err_max:
							err_max = ERROR_check_cnt_max
							print('Time out')
							break
					else:
						print(O+"*** PASS ***\n\tSensor [%s] ID:%s IP:%s."% (sensor_Subject,sensor_Serial,sensor_IP)+W)

						varPort = int(sensor_IP.split('.')[2]) + int(sensor_IP.split('.')[3])
						nodeIn = 50000 + varPort # sensor_IP = '192.168.168.30' -> 50198
						nodeOut = 51000 + varPort # sensor_IP = '192.168.168.30' -> 51198
						
						argv_realtime_RLS = '%s %s' % (nodeIn, nodeOut)
						kill_demon_realtime_RLS(argv_realtime_RLS)
						
						run_demon_check_RLS(myTableID) # 이전라인의 kill_demon_realtime_RLS 시간 주기위해 
						time.sleep(4) # run_demon_check_RLS에서 realtime_RLS_nodeID.html 파일이 생성될 시간을 준다.
						
						run_demon_realtime_RLS(argv_realtime_RLS) # /its_web/theme/ecos-its_optex/utility/nodeJs_table/realtime_RLS_templet.html, realtime_RLS_templet_Area.html, realtime_RLS_nodeID.html
						countOfDevice -= 1
						break
			else:
				print(R+"*** ERROR ***\n\tSensor [%s] ID:%s."% (sensor_Subject,sensor_Serial)+W)
	else:
		print "Error from read_table_w_cfg_sensorID(), Check Sensor's Config..."
		
	print "Device\n Total: %s Error: %s" % (totalOfDevice, (countOfDevice))

	exit()