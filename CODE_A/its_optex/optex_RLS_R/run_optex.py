#!/usr/bin/env python
# -*- coding: utf-8 -*-  

######################################################################
# 본 소스코드는 OPTEX Laser Sensor Model: RLS 용 프로그램 입니다.
######################################################################

from module import *

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
err_max = ERROR_check_cnt_max


if __name__ == '__main__':

	# 파이선 데몬 제거
	kill_demon_check_RLS_R()
		
	# 노드JS 데몬 제거
	kill_demon_realtime_RLS_R()
	
	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(30) ## 데이터베이스가 준비된 상태가 아니면 주기(30초)적인 재시도
			err_max=err_max-1
			if not err_max: exit('Time out')
			
	w_cfg_sensor_list_ID = read_table_w_cfg_sensorID() # table_RLS = c.ECOS_table_prefix+c.ECOS_table_RLS_R
	countOfDevice = len(w_cfg_sensor_list_ID)
	totalOfDevice = countOfDevice
	if w_cfg_sensor_list_ID:
		for row in w_cfg_sensor_list_ID:
			myTableID = str(row["wr_id"])
			sensor_IP = row["w_sensor_Addr"]
			sensor_Subject = row["wr_subject"]
			sensor_Serial = row["w_sensor_serial"]
			
			sensor_allowZone = row["w_sensor_allowZone"]
			sensor_ignoreZone = row["w_sensor_ignoreZone"]
			
			set_reload_w_cfg_reload(myTableID) # 재시동 필드를 회복시킨다.

			if sensor_IP:
				while True: # 센서 아이피 확인
					if check_sensor(sensor_IP):
						print(R+"*** ERROR ***\n\tPlease check sensor's IP address. It must be %s. Waiting[%s] ..." % (sensor_IP, err_max)+W)
						time.sleep(30) ## 센서가 준비된 상태가 아니면 주기(30초)적인 재시도
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
						
						## JS Code를 위한 JSON 형식의 환경파일 생성
						com_cfg = '/home/pi/common/config.json'
						own_cfg = '/home/pi/optex_RLS_R/config_'+str(nodeIn)+'.json'
						if os.path.isfile(own_cfg):
							pass
						else:
							share = readConfig(com_cfg)
							share["masking"] = {}
							share["masking"]["allowGroup"] = {}
							share["masking"]["denyGroup"] = {}
							share["maskCoord"] = {}
							share["maskCoord"]["allowGroup"] = {}
							share["maskCoord"]["denyGroup"] = {}

							if sensor_allowZone:
								zoneGroup = [x.strip() for x in sensor_allowZone.split(',')]
								
								for allowZone in zoneGroup:
									try:
										name, value = allowZone.split("|") # 1_253_155|229:438_5320:4611
										aZS, aZE = value.split('_')
										aZsX, aZsY = aZS.split(':')
										aZeX, aZeY = aZE.split(':')
										azW = int(aZeX)-int(aZsX)
										azH = int(aZeY)-int(aZsY)
										azMask = "M%s,%s l%s,0 0,%s -%s,0 0,-%s z" % (aZsX, aZsY, azW, azH, azW, azH)
										share["maskCoord"]["allowGroup"][name] = [int(aZsX), int(aZsY), int(aZeX), int(aZeY)]
										share["masking"]["allowGroup"][name] = azMask
									except:
										continue

							if sensor_ignoreZone:
								zoneGroup = [x.strip() for x in sensor_ignoreZone.split(',')]

								for ignoreZone in zoneGroup:
									try:
										name, value = ignoreZone.split("|") # 1_253_155|229:438_5320:4611
										iZS, iZE = value.split('_')
										iZsX, iZsY = iZS.split(':')
										iZeX, iZeY = iZE.split(':')
										izW = int(iZeX)-int(iZsX)
										izH = int(iZeY)-int(iZsY)
										izMask = "M%s,%s l%s,0 0,%s -%s,0 0,-%s z" % (iZsX, iZsY, izW, izH, izW, izH)
										share["maskCoord"]["denyGroup"][name] = [int(iZsX), int(iZsY), int(iZeX), int(iZeY)]
										share["masking"]["denyGroup"][name] = izMask
									except:
										continue
										
							share["interface"] = {}
							share["interface"]["portIn"] = nodeIn
							share["interface"]["portOut"] = nodeOut
							
							share["sensor"] = {}
							share["sensor"]["tableID"] = myTableID
							share["sensor"]["sensorIP"] = sensor_IP
							share["sensor"]["subject"] = sensor_Subject
							share["sensor"]["serial"] = sensor_Serial

							saveConfig(share,own_cfg)
						
						active, ip, port = MASQUERADE(row["w_opt94"],sensor_IP,int(row["w_sensor_Port"]) + int(row["w_sensor_serial"][-4:]))
						if active:
							print ("MASQUERADE On, Access Port:%s"%port)
						else:
							print ("MASQUERADE Off")
							
						## 파이선 데몬 실행
						run_demon_check_RLS_R(myTableID) # 이전라인의 kill_demon_realtime_RLS_R 시간 주기위해 
						time.sleep(4) # run_demon_check_RLS_R에서 realtime_RLS_R_nodeID.html 파일이 생성될 시간을 준다.
						
						countOfDevice -= 1
						break
			else:
				print(R+"*** ERROR ***\n\tSensor [%s] ID:%s."% (sensor_Subject,sensor_Serial)+W)
	else:
		print ("Error from read_table_w_cfg_sensorID(), Check Sensor's Config...")
	
	print ("Device\n Total: %s Error: %s" % (totalOfDevice, (countOfDevice)))
	
	exit()