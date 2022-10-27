#!/usr/bin/env python
# -*- coding: utf-8 -*-  

######################################################################
# 본 소스코드는 OPTEX Laser Sensor Model: RLS 용 프로그램 입니다.
######################################################################

from module import *

err_max = 10 # ERROR_check_cnt_max

if __name__ == '__main__':
	while True: # 데이터베이스 확인
		if database_test(): 
			print("*** PASS ***\n\tDatabase connected.") # 데이터베이스 쿼리 오류
			break
		else:
			print("*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ...") # 데이터베이스 쿼리 오류
			time.sleep(30) ## 데이터베이스가 준비된 상태가 아니면 주기(30초)적인 재시도
			err_max=err_max-1
			if not err_max: exit('Time out')
			
	w_cfg_sensor_list_ID = read_table_w_cfg_sensorID() # table_RLS = c.ECOS_table_prefix+c.ECOS_table_RLS_R
	if w_cfg_sensor_list_ID:

		for row in w_cfg_sensor_list_ID:
			cfg = readConfig('/home/pi/optex_VEHICLE/config.json')
			cfg["db"] = {}

			## 파이선 데몬 제거
			kill_demon_check_VEHICLE()

			## 노드JS 데몬 제거
			kill_demon_realtime_VEHICLE()

			tmpID = str(row["wr_id"])
			tmpSensAddr = row["w_sensor_Addr"]
			tmpSenSerial = row["w_sensor_serial"]
			tmpSenSubj = row["wr_subject"]

			# 설정시 재시동 요청시된 Check field 값 Reset 
			set_reload_w_cfg_reload(tmpID) # 재시동 요청 필드를 회복시킨다.
			
			if tmpSensAddr:
				while True: # 센서와 연결된 아이피 확인
					if check_sensor(tmpSensAddr):
						print("*** ERROR ***\n\tPlease check sensor's IP address. It must be %s. Waiting[%s] ..." % (tmpSensAddr, err_max))
						time.sleep(30) ## 센서가 준비된 상태가 아니면 주기(30초)적인 재시도
						err_max = err_max-1
						if not err_max:
							err_max = ERROR_check_cnt_max
							print('Time out')
							break
					else:
						cfg["db"]["wr_id"] = row["wr_id"]
						cfg["db"]["wr_subject"] = row["wr_subject"]
						cfg["db"]["wr_1"] = row["wr_1"]
						cfg["db"]["wr_2"] = row["wr_2"]
						cfg["db"]["wr_3"] = row["wr_3"]
						cfg["db"]["wr_4"] = row["wr_4"]
						cfg["db"]["wr_5"] = row["wr_5"]
						cfg["db"]["wr_6"] = row["wr_6"]
						cfg["db"]["wr_7"] = row["wr_7"]

						cfg["db"]["wr_8"] = row["wr_8"]
						cfg["db"]["wr_9"] = row["wr_9"]
						cfg["custom"] = {}
						if row["wr_8"]:
							opt1s = []
							opt2s = []
							var1, var2, host, port, opt1, opt2 = row["wr_8"].split('||') 
							opts = opt1.split(',')
							for opt in opts:
								opt1s.append(opt)
							opts = opt2.split(',')
							for opt in opts:
								opt2s.append(opt)
							cfg["custom"]["cust01"] = {"var1":var1,"var2":var2,"host":host,"port":int(port),"opt1s":opt1s,"opt2s":opt2s}

						if row["wr_9"]:
							opt1s = []
							opt2s = []
							var1, var2, host, port, opt1, opt2 = row["wr_9"].split('||') 
							opts = opt1.split(',')
							for opt in opts:
								opt1s.append(opt)
							opts = opt2.split(',')
							for opt in opts:
								opt2s.append(opt)
							cfg["custom"]["cust02"] = {"var1":var1,"var2":var2,"host":host,"port":int(port),"opt1s":opt1s,"opt2s":opt2s}

						cfg["db"]["wr_10"] = row["wr_10"]
						cfg["db"]["cpu_id"] = row["w_cpu_id"]
						cfg["db"]["license"] = row["w_license"]
						cfg["db"]["device_id"] = row["w_device_id"]
						cfg["db"]["sensor_serial"] = row["w_sensor_serial"]
						cfg["db"]["sensor_model"] = row["w_sensor_model"]
						cfg["db"]["sensor_face"] = row["w_sensor_face"]
						cfg["db"]["sensor_angle"] = row["w_sensor_angle"]
						cfg["db"]["sensor_lat_s"] = row["w_sensor_lat_s"]
						cfg["db"]["sensor_lng_s"] = row["w_sensor_lng_s"]
						cfg["db"]["sensor_lat_e"] = row["w_sensor_lat_e"]
						cfg["db"]["sensor_lng_e"] = row["w_sensor_lng_e"]
						cfg["db"]["sensor_ignoreS"] = row["w_sensor_ignoreS"]
						cfg["db"]["sensor_ignoreE"] = row["w_sensor_ignoreE"]
						cfg["db"]["sensor_noOfZone"] = row["w_sensor_noOfZone"]
						cfg["db"]["sensor_stepOfZone"] = row["w_sensor_stepOfZone"]
						cfg["db"]["sensor_offset"] = row["w_sensor_offset"]
						cfg["db"]["sensor_allowZone"] = row["w_sensor_allowZone"]
						cfg["db"]["sensor_ignoreZone"] = row["w_sensor_ignoreZone"]
						cfg["db"]["sensor_scheduleS"] = row["w_sensor_scheduleS"]
						cfg["db"]["sensor_scheduleE"] = row["w_sensor_scheduleE"]
						cfg["db"]["sensor_scheduleZone"] = row["w_sensor_scheduleZone"]
						cfg["db"]["sensor_week"] = row["w_sensor_week"]
						cfg["db"]["sensor_time"] = row["w_sensor_time"]
						cfg["db"]["sensor_disable"] = row["w_sensor_disable"]
						cfg["db"]["sensor_stop"] = row["w_sensor_stop"]
						cfg["db"]["sensor_reload"] = row["w_sensor_reload"]
						cfg["db"]["event_pickTime"] = row["w_event_pickTime"]
						cfg["db"]["event_holdTime"] = row["w_event_holdTime"]
						cfg["db"]["event_keepHole"] = row["w_event_keepHole"]
						cfg["db"]["event_syncDist"] = row["w_event_syncDist"]
						cfg["db"]["alarm_disable"] = row["w_alarm_disable"]
						cfg["db"]["alarm_level"] = row["w_alarm_level"]
						cfg["db"]["system_ip"] = row["w_system_ip"]
						cfg["db"]["system_port"] = row["w_system_port"]
						cfg["db"]["master_Addr"] = row["w_master_Addr"]
						cfg["db"]["master_Port"] = row["w_master_Port"]
						cfg["db"]["virtual_Addr"] = row["w_virtual_Addr"]
						cfg["db"]["virtual_Port"] = row["w_virtual_Port"]
						cfg["db"]["sensor_Addr"] = row["w_sensor_Addr"]
						cfg["db"]["sensor_Port"] = row["w_sensor_Port"]
						cfg["db"]["table_PortIn"] = row["w_table_PortIn"]
						cfg["db"]["table_PortOut"] = row["w_table_PortOut"]
						cfg["db"]["host_Addr"] = row["w_host_Addr"]
						cfg["db"]["host_Port"] = row["w_host_Port"]
						cfg["db"]["host_Addr2"] = row["w_host_Addr2"]
						cfg["db"]["host_Port2"] = row["w_host_Port2"]
						cfg["db"]["tcp_Addr"] = row["w_tcp_Addr"]
						cfg["db"]["tcp_Port"] = row["w_tcp_Port"]
						cfg["db"]["tcp_Addr2"] = row["w_tcp_Addr2"]
						cfg["db"]["tcp_Port2"] = row["w_tcp_Port2"]
						cfg["db"]["url1"] = row["w_url1"]
						cfg["db"]["url2"] = row["w_url2"]
						cfg["db"]["url3"] = row["w_url3"]
						cfg["db"]["url4"] = row["w_url4"]
						cfg["db"]["alert_Port"] = row["w_alert_Port"]
						cfg["db"]["alert_Value"] = row["w_alert_Value"]
						cfg["db"]["alert2_Port"] = row["w_alert2_Port"]
						cfg["db"]["alert2_Value"] = row["w_alert2_Value"]
						cfg["db"]["alert3_Port"] = row["w_alert3_Port"]
						cfg["db"]["alert3_Value"] = row["w_alert3_Value"]
						cfg["db"]["alert4_Port"] = row["w_alert4_Port"]
						cfg["db"]["alert4_Value"] = row["w_alert4_Value"]
						cfg["db"]["opt11"] = row["w_opt11"]
						cfg["db"]["opt12"] = row["w_opt12"]
						cfg["db"]["opt13"] = row["w_opt13"]
						cfg["db"]["opt14"] = row["w_opt14"]
						cfg["db"]["opt21"] = row["w_opt21"]
						cfg["db"]["opt22"] = row["w_opt22"]
						cfg["db"]["opt23"] = row["w_opt23"]
						cfg["db"]["opt24"] = row["w_opt24"]
						cfg["db"]["opt91"] = row["w_opt91"]
						cfg["db"]["opt92"] = row["w_opt92"]
						cfg["db"]["opt93"] = row["w_opt93"]
						cfg["db"]["opt94"] = row["w_opt94"]
						cfg["db"]["output1_relay"] = row["w_output1_relay"]
						cfg["db"]["output1_value"] = row["w_output1_value"]
						cfg["db"]["output1_group"] = row["w_output1_group"]
						cfg["db"]["output2_relay"] = row["w_output2_relay"]
						cfg["db"]["output2_value"] = row["w_output2_value"]
						cfg["db"]["output2_group"] = row["w_output2_group"]
						cfg["db"]["output3_relay"] = row["w_output3_relay"]
						cfg["db"]["output3_value"] = row["w_output3_value"]
						cfg["db"]["output3_group"] = row["w_output3_group"]
						cfg["db"]["output4_relay"] = row["w_output4_relay"]
						cfg["db"]["output4_value"] = row["w_output4_value"]
						cfg["db"]["output4_group"] = row["w_output4_group"]
						cfg["audioName"] = []
						cfg["audioTime"] = []
						cfg["audioVolume"] = []
						cfg["audioName"].append(row["w_audio1_name"])
						cfg["audioName"].append(row["w_audio2_name"])
						cfg["audioName"].append(row["w_audio3_name"])
						cfg["audioName"].append(row["w_audio4_name"])
						cfg["audioTime"].append(row["w_audio1_time"])
						cfg["audioTime"].append(row["w_audio2_time"])
						cfg["audioTime"].append(row["w_audio3_time"])
						cfg["audioTime"].append(row["w_audio4_time"])
						cfg["audioVolume"].append(row["w_audio1_volume"])
						cfg["audioVolume"].append(row["w_audio2_volume"])
						cfg["audioVolume"].append(row["w_audio3_volume"])
						cfg["audioVolume"].append(row["w_audio4_volume"])						

						cfg["masking"] = {}
						cfg["masking"]["allowGroup"] = {}
						cfg["masking"]["denyGroup"] = {}
						cfg["maskCoord"] = {}
						cfg["maskCoord"]["allowGroup"] = {}
						cfg["maskCoord"]["denyGroup"] = {}

						if row["w_sensor_allowZone"]:
							zoneGroup = [x.strip() for x in row["w_sensor_allowZone"].split(',')]
							
							for allowZone in zoneGroup:
								try:
									name, value = allowZone.split("|") # 1_253_155|229:438_5320:4611
									aZS, aZE = value.split('_')
									aZsX, aZsY = aZS.split(':')
									aZeX, aZeY = aZE.split(':')
									azW = int(aZeX)-int(aZsX)
									azH = int(aZeY)-int(aZsY)
									azMask = "M%s,%s l%s,0 0,%s -%s,0 0,-%s z" % (aZsX, aZsY, azW, azH, azW, azH)
									cfg["maskCoord"]["allowGroup"][name] = [int(aZsX), int(aZsY), int(aZeX), int(aZeY)]
									cfg["masking"]["allowGroup"][name] = azMask
								except:
									continue

						if row["w_sensor_ignoreZone"]:
							zoneGroup = [x.strip() for x in row["w_sensor_ignoreZone"].split(',')]

							for ignoreZone in zoneGroup:
								try:
									name, value = ignoreZone.split("|") # 1_253_155|229:438_5320:4611
									iZS, iZE = value.split('_')
									iZsX, iZsY = iZS.split(':')
									iZeX, iZeY = iZE.split(':')
									izW = int(iZeX)-int(iZsX)
									izH = int(iZeY)-int(iZsY)
									izMask = "M%s,%s l%s,0 0,%s -%s,0 0,-%s z" % (iZsX, iZsY, izW, izH, izW, izH)
									cfg["maskCoord"]["denyGroup"][name] = [int(iZsX), int(iZsY), int(iZeX), int(iZeY)]
									cfg["masking"]["denyGroup"][name] = izMask
								except:
									continue

						cfg["sensor"]["serial"] = row["w_sensor_serial"]
						cfg["sensor"]["subject"] = row["wr_subject"]
						cfg["sensor"]["tableID"] = row["wr_id"]
										
						cfg["interface"] = {}
						cfg["interface"]["portIn"] = row["w_table_PortIn"]+cfg["sensor"]["sensorPort"] # 8225 + 5001
						cfg["interface"]["portOut"] = row["w_table_PortOut"]+cfg["sensor"]["sensorPort"] # 9225 + 5001

						own_cfg = '/home/pi/optex_VEHICLE/config_'+str(cfg["interface"]["portIn"])+'.json'
						saveConfig(cfg,own_cfg)
						
						## 파이선 데몬 실행
						run_demon_check_VEHICLE(cfg["interface"]["portIn"]) # 이전라인의 kill_demon_realtime_VEHICLE 시간 주기위해 
						# time.sleep(4) # run_demon_check_VEHICLE에서 realtime_VEHICLE_nodeID.html 파일이 생성될 시간을 준다.
						
						break
			else:
				print("*** ERROR ***\n\tSensor [%s] ID:%s."% (tmpSenSubj,tmpSenSerial))
	else:
		print "Error - No sensorID(), Check Sensor's Config..."
	
	exit()