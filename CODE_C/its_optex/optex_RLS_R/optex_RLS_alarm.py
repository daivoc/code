#!/usr/bin/env python
# -*- coding: utf-8 -*-

## RLS 센서에 출력 릴레이 구현
from module import *

### Packet field access ###
def all(packet):
	return binascii.hexlify(packet).decode()

def main ():
	
	setAlertTime1 = 0 ##  얼랏 발생시 타이머 적용
	setAlertTime2 = 0 ##  얼랏 발생시 타이머 적용
	setAlertTime3 = 0 ##  얼랏 발생시 타이머 적용
	setAlertTime4 = 0 ##  얼랏 발생시 타이머 적용

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((db_virtual_Addr, db_virtual_Port)) # 'localhost'를 뜻함
	except:
		print "IP(%s) and Port(%s) are Busy.\nCheck Processor."%(db_virtual_Addr, db_virtual_Port)
		exit()
		
	s.listen(1)

			
	##########################################################
	## # GPIO 포트 초기화
	if db_out1_relay and db_out1_value:
		print "Init. GPIO ID 1:",insert_socket_GPWIO(id=db_out1_relay, status=1, msg='init')
			
	if db_out2_relay and db_out2_value:
		print "Init. GPIO ID 2:",insert_socket_GPWIO(id=db_out2_relay, status=1, msg='init')
			
	if db_out3_relay and db_out3_value:
		print "Init. GPIO ID 3:",insert_socket_GPWIO(id=db_out3_relay, status=1, msg='init')
			
	if db_out4_relay and db_out4_value:
		print "Init. GPIO ID 4:",insert_socket_GPWIO(id=db_out4_relay, status=1, msg='init')

	while True:
	
		conn, addr = s.accept()
		while True:
			data = conn.recv(1024)
			if not data: break

			##########################################################
			## 알람아웃
			## A1 A2 B1 B2 AM AR SO DQ TR TA HB		11111111110
			## db_out1_relay = int(row["w_output1_relay"])
			## db_out1_value = float(row["w_output1_value"])
			## db_out1_group = row["w_output1_group"]

			RLS_size = len(data)
			if RLS_size is 27: # 2020 or 3060
				# w_md = data[0:3].strip()	# 3 Model
				# w_id = data[3:6].strip()	# 3 ID Number
				# w_ma = data[6:8].strip()	# 2 Master Alarm
				w_la = data[8:10].strip()	## 2 The Latest Area
				# w_ca = data[10:12].strip()	# 2 Combination of Areas
				# w_cc = data[12:14].strip()	# 2 Multiple Areas
				w_dq = ('1' if(data[14:16].strip()) else '0')	# 2 Disqualification	
				w_ar = ('1' if(data[16:18].strip()) else '0')	# 2 Anti-rotation
				w_am = ('1' if(data[18:20].strip()) else '0')	# 2 Anti-masking
				w_tr = ('1' if(data[20:22].strip()) else '0')	# 2 Internal Error
				w_so = ('1' if(data[22:24].strip()) else '0')	# 2 Soiling
				w_ta = ('1' if(data[24:26].strip()) else '0')	# 2 Tamper or Device Monitoring
				# RLS_zone_max = 4 # zone 4
			elif RLS_size is 28: # 3060
				# w_md = data[0:3].strip()	# 3 Model
				# w_id = data[3:6].strip()	# 3 ID Number
				# w_ma = data[6:8].strip()	# 2 Master Alarm
				w_la = data[8:11][:-1].strip()	## 두자로 바꾼자. 3 The Latest Area
				# w_ca = data[11:13].strip()	# 2 Combination of Areas
				# w_cc = data[13:15].strip()	# 2 Multiple Areas
				w_dq = ('1' if(data[15:17].strip()) else '0')	# 2 Disqualification
				w_ar = ('1' if(data[17:19].strip()) else '0')	# 2 Anti-rotation
				w_am = ('1' if(data[19:21].strip()) else '0')	# 2 Anti-masking
				w_tr = ('1' if(data[21:23].strip()) else '0')	# 2 Internal Error
				w_so = ('1' if(data[23:25].strip()) else '0')	# 2 Soiling
				w_ta = ('1' if(data[25:27].strip()) else '0')	# 2 Tamper or Device Monitoring
				# RLS_zone_max = 8 # zone 8
			
			
			w_hb = '0' # 하트비트 초기화
			if (w_la == 'A1'):
				w_la = '1000'
			elif (w_la == 'A2'):
				w_la = '0100'
			elif (w_la == 'B1'):
				w_la = '0010'
			elif (w_la == 'B2'):
				w_la = '0001'
			else:
				w_la = '0000'
				w_hb = '1'
				
			eventValue = ("%s%s%s%s%s%s%s%s" % (w_la,w_am,w_ar,w_so,w_dq,w_tr,w_ta,w_hb))
			# print data, eventValue, db_out1_group
			# print "E:%s, A1:%s, A2:%s, A3:%s, A4:%s"%(eventValue, db_out1_group, db_out2_group, db_out3_group, db_out4_group)
			## 감지한 이벤트 값과 설정값이 동시에 엑테브('1') 상테이면 릴레이를 동작시키고 브레이크 한다.
			if(len(db_out1_group)):
				for i in range(0, len(eventValue)):
					if(eventValue[i] == db_out1_group[i] == '1'):
						if db_out1_relay and db_out1_value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( db_alert_Value:)
							if setAlertTime1:
								## 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
								pass
							else:
								setAlertTime1 = datetime.datetime.now()
								Process(target=alertOut, args=(db_out1_relay,db_out1_value)).start()
						break
			if(len(db_out2_group)):
				for i in range(0, len(eventValue)):
					if (eventValue[i] == db_out2_group[i] == '1'):
						if db_out2_relay and db_out2_value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( db_alert_Value:)
							if setAlertTime2:
								## 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
								pass
							else:
								setAlertTime2 = datetime.datetime.now()
								Process(target=alertOut, args=(db_out2_relay,db_out2_value)).start()
						break
			if(len(db_out3_group)):
				for i in range(0, len(eventValue)):
					if (eventValue[i] == db_out3_group[i] == '1'):
						if db_out3_relay and db_out3_value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( db_alert_Value:)
							if setAlertTime3:
								## 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
								pass
							else:
								setAlertTime3 = datetime.datetime.now()
								Process(target=alertOut, args=(db_out3_relay,db_out3_value)).start()
						break
			if(len(db_out4_group)):
				for i in range(0, len(eventValue)):
					if (eventValue[i] == db_out4_group[i] == '1'):
						if db_out4_relay and db_out4_value: # 알람 발생 알림 포트(BSS_alert_Port) 출력지속시간:초( db_alert_Value:)
							if setAlertTime4:
								## 경보발생 시간 이내에 발생하는 이벤트는 그 시간이 끝날떄 까지 무시 한다.
								pass
							else:
								setAlertTime4 = datetime.datetime.now()
								Process(target=alertOut, args=(db_out4_relay,db_out4_value)).start()
						break
						
			## 알람아웃
			##########################################################			
			
			# print "%s\t%s"%(addr,data) ## 자료가 바이너리이면 all(data)
			
			## 실시간 알람 접점신호 발생 ##
			## 시간차(0:00:10.558780)를 초로 변환(total_seconds()) > 설정된 지속시간값(초)
			if db_out1_value and setAlertTime1:
				if (datetime.datetime.now() - setAlertTime1).total_seconds() > db_out1_value:
					setAlertTime1 = 0
			if db_out2_value and setAlertTime2:
				if (datetime.datetime.now() - setAlertTime2).total_seconds() > db_out2_value:
					setAlertTime2 = 0
			if db_out3_value and setAlertTime3:
				if (datetime.datetime.now() - setAlertTime3).total_seconds() > db_out3_value:
					setAlertTime3 = 0
			if db_out4_value and setAlertTime4:
				if (datetime.datetime.now() - setAlertTime4).total_seconds() > db_out4_value:
					setAlertTime4 = 0
					
		conn.close()
	s.close()

if __name__ == '__main__':
	if len(sys.argv) > 1: 
		myTableID = sys.argv[1]
	else:
		exit("No database Information, Check Sensor's Config...")
		
	w_cfg_sensor_list_All = read_table_w_cfg_sensor_all(myTableID)
	for row in w_cfg_sensor_list_All:
		db_virtual_Addr = row["w_virtual_Addr"]
		db_virtual_Port = row["w_virtual_Port"]
		db_out1_relay = int(row["w_output1_relay"])
		db_out1_value = float(row["w_output1_value"])
		db_out1_group = row["w_output1_group"]
		db_out2_relay = int(row["w_output2_relay"])
		db_out2_value = float(row["w_output2_value"])
		db_out2_group = row["w_output2_group"]
		db_out3_relay = int(row["w_output3_relay"])
		db_out3_value = float(row["w_output3_value"])
		db_out3_group = row["w_output3_group"]
		db_out4_relay = int(row["w_output4_relay"])
		db_out4_value = float(row["w_output4_value"])
		db_out4_group = row["w_output4_group"]
		
	print("Runing Background Alarm ...")
	
	main()