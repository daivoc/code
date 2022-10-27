#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sys
import time
import subprocess 
import pymysql
import os
import json

# from warnings import filterwarnings
# filterwarnings('ignore', category = pymysql.Warning)

# ### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
# reload(sys)
# sys.setdefaultencoding('utf-8')

# mysql
db_host = "localhost"
db_user = "its"
db_pass = "GXnLRNT9H50yKQ3G"
db_name = "its_web" # 기본 데이터베이스

ECOS_table = "g5_write_g200t230"
ERROR_check_cnt_max = 8 # 최초실행시 디비와 센서체크 오류 횟수

def database_test(): # Optex Microwave
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		return 1
	except:
		return 0

# 센서 아이피 확인 
def check_sensor(sensorIP):
    return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)

## 환경설정 파일(JSON) 저장
def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def kill_demon_check_RLS_V(): 
	cmd = "pkill -9 -ef optex_RLS_V.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def run_demon_check_RLS_V(arg): # python -W ignore
	# cmd = "python /home/pi/optex_RLS_V/optex_RLS_V.pyc %s 2>&1 & " % arg
	cmd = "python3 /home/pi/optex_RLS_V/getSensorInfo.pyc && python /home/pi/optex_RLS_V/optex_RLS_V.pyc %s 2>&1 & " % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def kill_demon_realtime_RLS_V(): 
	cmd = "pkill -9 -ef realtime_RLS.js 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return p

def MASQUERADE(active,ip,port):
	if active:
		# 연결 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(port,ip)
	else:
		# 차단 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		sudo iptables -D FORWARD -i eth0 -j ACCEPT
		sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE
		sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(port,ip)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return (active,ip,port)

def read_table_w_cfg_sensorID(): ###################### Optex REDSCAN
	query = "SELECT * FROM " + ECOS_table + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

def set_reload_w_cfg_reload(wr_id=''): 
	query = "UPDATE " + ECOS_table + " SET w_sensor_reload = '0' WHERE wr_id = " + wr_id
	try:
		conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except pymysql.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

err_max = ERROR_check_cnt_max

if __name__ == '__main__':
	# 파이선 데몬 제거
	kill_demon_check_RLS_V()
	# 노드JS 데몬 제거
	kill_demon_realtime_RLS_V()

	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(30) ## 데이터베이스가 준비된 상태가 아니면 주기(30초)적인 재시도
			err_max=err_max-1
			if not err_max: exit('Time out')

	# print(json.dumps(read_table_w_cfg_sensorID(), indent = 4, sort_keys = True, default = str))

	w_cfg_sensor_list_ID = read_table_w_cfg_sensorID()
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
						own_cfg = '/home/pi/optex_RLS_V/config_'+str(nodeIn)+'.json'
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
						run_demon_check_RLS_V(myTableID) # 이전라인의 kill_demon_realtime_RLS_V 시간 주기위해 
						time.sleep(4) # run_demon_check_RLS_V에서 realtime_RLS_V_nodeID.html 파일이 생성될 시간을 준다.
						
						countOfDevice -= 1
						break
			else:
				print(R+"*** ERROR ***\n\tSensor [%s] ID:%s."% (sensor_Subject,sensor_Serial)+W)
	else:
		print ("Error from read_table_w_cfg_sensorID(), Check Sensor's Config...")

	print ("Device\n Total: %s Error: %s" % (totalOfDevice, (countOfDevice)))
	exit()