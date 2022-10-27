#!/usr/bin/env python
# -*- coding: utf-8 -*-  

###################################################
## COUNTER Control and Managment
## Ref: https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
## Ref: http://112.187.234.55/optex_web/bbs/board.php?bo_table=g100t100&wr_id=96
###################################################

from module import *

if __name__ == '__main__':
	while True: # 데이터베이스 확인
		if database_test(): 
			print(c.G+"*** PASS ***\n\tDatabase connected."+c.W) # 데이터베이스
			break
		else:
			print(c.R+"*** ERROR ***\n\tDatabase connected error. Retry ..."+c.W) # 데이터베이스
			time.sleep(1)
			c.db_connection_limit -= 1
			if not c.db_connection_limit: exit('Time out')

	kill_demon_COUNTER_table()
	kill_demon_COUNTER()

	w_cfg_sensor_list_COUNTER = read_table_w_cfg_sensorID_COUNTER()

	for row in w_cfg_sensor_list_COUNTER:
		COUNTER_minDist = int(row["w_sensor_ignoreS"]) # 감지 시작 영역
		COUNTER_maxDist = int(row["w_sensor_ignoreE"]) # 감지 종료 영역
		COUNTER_validZone_S = int(row["w_sensor_scheduleS"]) # 감지 확정 영역
		COUNTER_validZone_E = int(row["w_sensor_scheduleE"]) # 감지 확정 영역
		COUNTER_table_PortIn = row["w_table_PortIn"]
		COUNTER_table_PortOut = row["w_table_PortOut"]
		
		make_its_M_map(COUNTER_minDist,COUNTER_maxDist,COUNTER_validZone_S,COUNTER_validZone_E) 

		print('Running Table: %s \n' % run_demon_COUNTER_table("%s %s"%(COUNTER_table_PortIn, COUNTER_table_PortOut)))		
		
		# ECOS_exeName = "%s" % row["wr_id"]
		# print('Running COUNTER: %s \n' % run_COUNTER(ECOS_exeName))
		print('Running COUNTER: %s \n' % run_COUNTER("%s" % row["wr_id"]))
		
	exit()