#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import subprocess 
import json
import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(cfg,name):
	with open(name, "w") as json_file: ## 저장
		json.dump(cfg, json_file, sort_keys=True, indent=4)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_FSI(): 
	cmd = "sudo kill -9 $(ps aux | grep ' FSI' | awk '{print $2}')"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

def kill_demon_FDX(): 
	cmd = "pkill -9 -ef FDX.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

def run_demon_FSI(): 
	cmd = "cd %s; python FSI.pyc 2>&1 & " % (share['path']['fsi'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def run_demon_FDX(k, v):
	cmd = "cd %s; python FDX.pyc %s %s 2>&1 & " % (share['path']['fsi'], k, v)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def read_table_w_cfg_fsi(): ## 사용자 환경 변수 로딩
	query = "SELECT * FROM " + share['table']['fsi'] + " WHERE w_sensor_disable = 0" + " ORDER BY wr_id DESC LIMIT 1" # 최종 등록된 1의 레코드 추출
	try:
		conn = MySQLdb.connect(host=share["mysql"]['host'], user=share["mysql"]['user'], passwd=share["mysql"]['pass'], db=share["mysql"]['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchone()
	except MySQLdb.Error as error:
		print(error)
		return '' ## 오류발생시 
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_fsi_fd(): ## 사용자 환경 변수 로딩
	query = "SELECT * FROM " + share['table']['fsi_fd'] + " WHERE w_sensor_disable = 0"
	try:
		conn = MySQLdb.connect(host=share["mysql"]['host'], user=share["mysql"]['user'], passwd=share["mysql"]['pass'], db=share["mysql"]['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		print(error)
		return '' ## 오류발생시 
	finally:
		cursor.close()
		conn.close()

def create_table_w_log_fsi_data(logTable):
	query = """
		CREATE TABLE IF NOT EXISTS %s (
		`w_id` int(11) NOT NULL AUTO_INCREMENT,
		`w_zone` tinyint(4) NOT NULL DEFAULT '0',
		`w_eventID` tinyint(4) NOT NULL DEFAULT '0',
		`w_eventName` varchar(16) NULL DEFAULT '',
		`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`w_id`)
		) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
		""" % (logTable)
	try:
		conn = MySQLdb.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query) # create table
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
	except MySQLdb.Warning as warning:
		pass
	finally:
		cursor.close()
		conn.close()

def itsMemberConfig(id, field): # table
	cursor = None
	conn = None
	query = "SELECT " + field + " FROM g5_member WHERE mb_id = '" + id + "'" 
	try:
		conn = MySQLdb.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchone() # 커서의 fetchall()는 모두, fetchone()은 하나의 Row, fetchone(n)은 n개 만큼
	except MySQLdb.Error as error:
		return 0
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()

def configZone(zone,row):
	global cfg

	cfg["action"][zone] = {}

	cfg["action"][zone]["info"] = {}
	cfg["action"][zone]["info"]["subject"] = row["wr_subject"]
	cfg["action"][zone]["info"]["serial"] = row["w_device_serial"]

	cfg["action"][zone]["flag"] = {}

	## START #########################################
	# audioOut - 오디오 출력
	cfg["action"][zone]["audioOut"] = {}
	cfg["action"][zone]["flag"]["audioOut"] = False
	if row["wr_2"] and row["wr_3"]:
		cfg["action"][zone]["audioOut"] = {
			"path":row["wr_2"],
			"length":float(row["wr_3"])
		}
		cfg["action"][zone]["flag"]["audioOut"] = True

	# httpRequest - GET/POST
	cfg["action"][zone]["httpRequest"] = {}
	cfg["action"][zone]["flag"]["httpRequest"] = {}
	try:
		cfg["action"][zone]["flag"]["httpRequest"]["P"] = False
		elements = row["wr_4"].split('||') 
		addr = elements[0]
		data = elements[1]
		if elements[2]:
			enc = "POST"
		else:
			enc = "GET"
		xml = elements[3]
		if addr and data:
			cfg["action"][zone]["httpRequest"]["P"] = {
				"addr":addr,
				"data":data,
				"enc":enc,
				"xml":xml
			}
			cfg["action"][zone]["flag"]["httpRequest"]["P"] = True
	except:
		pass

	try:
		cfg["action"][zone]["flag"]["httpRequest"]["S"] = False
		elements = row["wr_5"].split('||') 
		addr = elements[0]
		data = elements[1]
		if elements[2]:
			enc = "POST"
		else:
			enc = "GET"
		xml = elements[3]
		if addr and data:
			cfg["action"][zone]["httpRequest"]["S"] = {
				"addr":addr,
				"data":data,
				"enc":enc,
				"xml":xml
			}
			cfg["action"][zone]["flag"]["httpRequest"]["S"] = True
	except:
		pass

	# ims - 모니터링 서버 접속
	cfg["action"][zone]["ims"] = {}
	cfg["action"][zone]["flag"]["ims"] = {}
	cfg["action"][zone]["flag"]["ims"]["P"] = False
	if row["w_ims_address_P"] and row["w_ims_port_P"]:
		cfg["action"][zone]["ims"]["P"] = {
			"addr":row["w_ims_address_P"],
			"port":row["w_ims_port_P"]
		}
		cfg["action"][zone]["flag"]["ims"]["P"] = True

	cfg["action"][zone]["flag"]["ims"]["S"] = False
	if row["w_ims_address_S"] and row["w_ims_port_S"]:
		cfg["action"][zone]["ims"]["S"] = {
			"addr":row["w_ims_address_S"],
			"port":row["w_ims_port_S"]
		}
		cfg["action"][zone]["flag"]["ims"]["S"] = True


	# itsACU - 원격 릴레이 컨트롤
	cfg["action"][zone]["itsACU"] = {}
	cfg["action"][zone]["flag"]["itsACU"] = False
	try:
		acuIP, acuPort, acuID, acuZone, acuTime, acuEnc = row["wr_10"].split('||') 
		if acuIP and acuPort and acuID and acuTime:
			cfg["action"][zone]["itsACU"] = {
				"addr":acuIP,
				"port":acuPort,
				"id":acuID,
				"zone":acuZone,
				"time":acuTime,
				"enc":acuEnc
			}
			cfg["action"][zone]["flag"]["itsACU"] = True
	except:
		pass

	# relayOut - 로컬 릴레이 컨트롤
	cfg["action"][zone]["relayOut"] = {}
	cfg["action"][zone]["flag"]["relayOut"] = False
	if row["w_alert_port"] and row["w_alert_value"]:
		cfg["action"][zone]["relayOut"] = {
			"port":row["w_alert_port"],
			"hold":row["w_alert_value"]
		}
		cfg["action"][zone]["flag"]["relayOut"] = True

	# snapshot - CCTV 사진 저장
	cfg["action"][zone]["snapshot"] = {}
	cfg["action"][zone]["flag"]["snapshot"] = False
	if row["w_snapshot_url"] and row["w_snapshot_qty"]:
		cfg["action"][zone]["snapshot"] = {
			"url":row["w_snapshot_url"],
			"qty":row["w_snapshot_qty"],
			"enc":row["w_snapshot_enc"]
		}
		cfg["action"][zone]["flag"]["snapshot"] = True

	# streaming - CCTV 스트리밍 링크
	cfg["action"][zone]["streaming"] = {}
	cfg["action"][zone]["flag"]["streaming"] = False
	if row["w_streaming_url"]:
		cfg["action"][zone]["streaming"] = {
			"url":row["w_streaming_url"],
			"enc":row["w_streaming_enc"]
		}
		cfg["action"][zone]["flag"]["streaming"] = True

	# socketIO - TCP 포트 통신
	cfg["action"][zone]["socketIO"] = {}
	cfg["action"][zone]["flag"]["socketIO"] = {}
	try:
		cfg["action"][zone]["flag"]["socketIO"]["P"] = False
		elements = row["wr_8"].split('||') 
		addr = elements[0]
		port = int(elements[1])
		value = elements[2]
		if addr and port and value:
			cfg["action"][zone]["socketIO"]["P"] = {
				"addr":addr,
				"port":port,
				"value":value
			}
			cfg["action"][zone]["flag"]["socketIO"]["P"] = True
	except:
		pass

	try:
		cfg["action"][zone]["flag"]["socketIO"]["S"] = False
		elements = row["wr_9"].split('||') 
		addr = elements[0]
		port = int(elements[1])
		value = elements[2]
		if addr and port and value:
			cfg["action"][zone]["socketIO"]["S"] = {
				"addr":addr,
				"port":port,
				"value":value
			}
			cfg["action"][zone]["flag"]["socketIO"]["S"] = True
	except:
		pass
	## END #########################################	

def masquerade(masq):
	# 아이피 라우팅 기능으로 내부 환경설정의 
	# MASQUERADE -> action 상태에 따라 실행 된다.
	# 삭제시 리스트를 통해 총 수를 확인한 후 일괄 삭제한다. 
	if masq["masq"]:
		# Pre/Post Routing
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(masq["port"], masq["addr"])
		# sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		# sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		# sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport 10001 -j DNAT --to-destination 192.168.168.30:80;
	else:
		# Pre/Post Routing 일괄 삭제
		cmd = '''
		line_num=$(sudo iptables --line-numbers --list PREROUTING -t nat | awk '$9 ~ /to:192.168.16..30/ { print $1 }' | wc -l); 
		for i in `seq 1 $line_num`; do sudo iptables -t nat -D PREROUTING 1; done;
		line_num=$(sudo iptables --line-numbers --list POSTROUTING -t nat | awk '$2 ~ /MASQUERADE/ { print $1 }' | wc -l); 
		for i in `seq 1 $line_num`; do sudo iptables -t nat -D POSTROUTING 1; done;
		'''
		# cmd = '''
		# sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		# sudo iptables -D FORWARD -i eth0 -j ACCEPT;
		# sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE;
		# sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		# '''%(masq["port"], masq["addr"])

		# sudo iptables -D FORWARD -i eth0 -j ACCEPT;
		# sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE;
		# sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport 10001 -j DNAT --to-destination 192.168.168.30:80;
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return masq

def openning():
	################
	# Openning Color
	################
	print("\n")
	for i in range(0, 16):
		for j in range(0, 16):
			code = str(i * 16 + j)
			sys.stdout.write("\\u001b[38;5;{0}m {1}".format(code,code.ljust(4)).decode("unicode-escape"))
		print(("\\u001b[0m".decode("unicode-escape")))
	print("\n")

	for i in range(0, 16):
		for j in range(0, 16):
			code = str(i * 16 + j)
			sys.stdout.write("\\u001b[48;5;{0}m {1}".format(code,code.ljust(4)).decode("unicode-escape"))
		print(("\\u001b[0m".decode("unicode-escape")))
	print("\n")
	
	print("""
 ███████╗ ██████╗ ██████╗ ███████╗
 ██╔════╝██╔════╝██╔═══██╗██╔════╝
 █████╗  ██║     ██║   ██║███████╗
 ██╔══╝  ██║     ██║   ██║╚════██║
 ███████╗╚██████╗╚██████╔╝███████║
 ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝
 
 FFFFFFFFFFFFFFFFFFFFFF    SSSSSSSSSSSSSS   IIIIIIIIII
 F::::::::::::::::::::F  SS:::::::::::::::S I::::::::I
 F::::::::::::::::::::F S::::::SSSSS::::::S I::::::::I
 FF::::::FFFFFFFFF::::F S:::::S      SSSSSS II::::::II
   F:::::F       FFFFFF S:::::S               I::::I  
   F:::::F              S:::::S               I::::I  
   F::::::FFFFFFFFFF     S:::::SSS            I::::I  
   F:::::::::::::::F      SS::::::SSSSS       I::::I  
   F:::::::::::::::F        SSS::::::::SS     I::::I  
   F::::::FFFFFFFFFF           SSSSS:::::S    I::::I  
   F:::::F                          S:::::S   I::::I  
   F:::::F                          S:::::S   I::::I  
 FF:::::::FF            SSSSSS      S:::::S II::::::II
 F::::::::FF            S::::::SSSSS::::::S I::::::::I
 F::::::::FF            S:::::::::::::::SS  I::::::::I
 FFFFFFFFFFF              SSSSSSSSSSSSSS    IIIIIIIIII
	""")

def main():
	global cfg

	row = read_table_w_cfg_fsi()
	if not row: # 데이터베이스 유/무 확인
		exit('No database')

	cfg["user"] = readConfig("{}/config.json".format(share["path"]["fsi"]))

	cfg["status"] = share["status"].copy()
	cfg["mysql"] = share["mysql"].copy()
	# 로그 테이블 생성
	logTable = "w_log_sensor_"+row["w_device_serial"]
	create_table_w_log_fsi_data(logTable)
	cfg["mysql"]["logTable"] = logTable

	cfg["device"] = {}
	cfg["device"]["id"] = row["w_device_id"] # ETH1_192.168.168.10
	cfg["device"]["name"] = row["w_device_name"]
	cfg["device"]["model"] = cfg["user"]["model"][row["w_device_model"]]
	cfg["device"]["serial"] = row["w_device_serial"]
	cfg["device"]["addr"] = row["w_device_ip"] # "192.168.168.30"
	cfg["device"]["port"] = row["w_device_port"] # 10001 # 52101 
	cfg["device"]["masq"] = row["w_device_masq"] # w_device_masq

	# print row["w_event_id"]
	try:
		elements = row["w_event_id"].split('||')
	except:
		pass
	if len(elements) < 25:
		elements = [None] * 25
	cfg["device"]["zoneName"] = {
		"CHA":elements[0] if elements[0] else "001",
		"CHB":elements[1] if elements[1] else "002",
		"ZONE-001":elements[0] if elements[0] else "001",
		"ZONE-002":elements[1] if elements[1] else "002",
		"ZONE-003":elements[2] if elements[2] else "003",
		"ZONE-004":elements[3] if elements[3] else "004",
		"ZONE-005":elements[4] if elements[4] else "005",
		"ZONE-006":elements[5] if elements[5] else "006",
		"ZONE-007":elements[6] if elements[6] else "007",
		"ZONE-008":elements[7] if elements[7] else "008",
		"ZONE-009":elements[8] if elements[8] else "009",
		"ZONE-010":elements[9] if elements[9] else "010",
		"ZONE-011":elements[10] if elements[10] else "011",
		"ZONE-012":elements[11] if elements[11] else "012",
		"ZONE-013":elements[12] if elements[12] else "013",
		"ZONE-014":elements[13] if elements[13] else "014",
		"ZONE-015":elements[14] if elements[14] else "015",
		"ZONE-016":elements[15] if elements[15] else "016",
		"ZONE-017":elements[16] if elements[16] else "017",
		"ZONE-018":elements[17] if elements[17] else "018",
		"ZONE-019":elements[18] if elements[18] else "019",
		"ZONE-020":elements[19] if elements[19] else "020",
		"ZONE-021":elements[20] if elements[20] else "021",
		"ZONE-022":elements[21] if elements[21] else "022",
		"ZONE-023":elements[22] if elements[22] else "023",
		"ZONE-024":elements[23] if elements[23] else "024",
		"ZONE-025":elements[24] if elements[24] else "025"
	}
	cfg["device"]["zoneID"] = {
		"CHA":"1",
		"CHB":"2",
		"ZONE-001":"1",
		"ZONE-002":"2",
		"ZONE-003":"3",
		"ZONE-004":"4",
		"ZONE-005":"5",
		"ZONE-006":"6",
		"ZONE-007":"7",
		"ZONE-008":"8",
		"ZONE-009":"9",
		"ZONE-010":"10",
		"ZONE-011":"11",
		"ZONE-012":"12",
		"ZONE-013":"13",
		"ZONE-014":"14",
		"ZONE-015":"15",
		"ZONE-016":"16",
		"ZONE-017":"17",
		"ZONE-018":"18",
		"ZONE-019":"19",
		"ZONE-020":"20",
		"ZONE-021":"21",
		"ZONE-022":"22",
		"ZONE-023":"23",
		"ZONE-024":"24",
		"ZONE-025":"25"
	}

	try:
		elements = row["w_event_value"].split('||') 
	except:
		pass
	if len(elements) < 5:
		elements = [None] * 5
	cfg["device"]["value"] = { # common -> config.json -> status
		"Intrusion":int(elements[0]) if elements[0] else 1,
		"Fault":int(elements[1]) if elements[1] else 9,
		"Tamper":int(elements[2]) if elements[2] else 8,
		"Other":int(elements[3]) if elements[3] else 0,
		"OK":int(elements[4]) if elements[4] else 2
	}

	try:
		elements = row["w_event_type"].split('||') 
	except:
		pass
	if len(elements) < 5:
		elements = [None] * 5
	cfg["device"]["type"] = {
		"Intrusion":elements[0] if elements[0] else "Intrusion",
		"Fault":elements[1] if elements[1] else "Fault",
		"Tamper":elements[2] if elements[2] else "Tamper",
		"Other":elements[3] if elements[3] else "Other",
		"OK":elements[4] if elements[4] else "Ping"
	}

	cfg["action"] = {}
	# "0"은 자체 디바이스를 의미 한다.
	# 그외 1 부터 25 까지의 존이 설정된다.
	# configZone("0",row) # cfg["action"]["0"] 생성 및 관련 변수 선언

	# # 사용자 요청 유무
	# cfg["action"]["0"]["user"] = {}
	# cfg["action"]["0"]["user"]["httpRequest"] = False
	# if cfg["user"]["interface"]["httpRequest"]["url"] and cfg["user"]["interface"]["httpRequest"]["method"]:
	# 	cfg["action"]["0"]["user"]["httpRequest"] = True

	# cfg["action"]["0"]["user"]["apiCustom"] = False
	# if cfg["user"]["interface"]["apiCustom"]["addr"] and cfg["user"]["interface"]["apiCustom"]["port"]:
	# 	cfg["action"]["0"]["user"]["apiCustom"] = True

	cfg["local"] = {}
	cfg["local"]["host"] = row["w_device_id"].split('_')[-1] # "192.168.168.10"
	cfg["local"]["port_from_fsi"] = share["port"]["fsi"] # 52001 
	cfg["local"]["port_from_other"] = share["port"]["fsi"] # 동일한 포트를 사용처에 따른 이름을 달리함 + 2 # 52003
	cfg["local"]["zone"] = {}
	# cfg["local"]["zone"]["0"] = share["port"]["fsi"]+99 # FSI 센서 자신

	# 1 부터 25 까지의 존이 설정.
	rowZone = read_table_w_cfg_fsi_fd()
	for row_fd in rowZone: # cfg["action"]["1 ~ 25"] 생성 및 관련 변수 선언
		configZone(str(row_fd["w_zone_id"]),row_fd)
		# Zone단위 데몬 Port -> zone_id + 52001 + 99
		cfg["local"]["zone"][row_fd["w_zone_id"]] = row_fd["w_zone_id"]+share["port"]["fsi"]+99

	cfg["nodejs"] = {}
	cfg["nodejs"]["port_py_to_js"] = share["port"]["fsi"]+10
	cfg["nodejs"]["port_js_to_html"] = share["port"]["fsi"]+12
	cfg["nodejs"]["js_code"] = "{}/FSI.js".format(share["path"]["fsi"])
	cfg["nodejs"]["html_source"] = "{}/FSI.html".format(share["path"]["fsi"])
	cfg["nodejs"]["html_target"] = "{}/index.html".format(share["path"]["fsi"])

	cfg["pathLog"] = share["path"]["log"]
	cfg["pathCommon"] = share["path"]["common"]
	# user command folder
	cfg["pathUserCmd"] = share["path"]["its_web"]+share["path"]["user"]["note"]+"/fsi_command"
	if not os.path.exists(cfg["pathUserCmd"]): # audioFolderBeep 폴더 생성
		os.makedirs(cfg["pathUserCmd"])
	os.chmod(cfg["pathUserCmd"],0o777)

	ioB = str(itsMemberConfig('its','mb_4')['mb_4']).strip() # 인터페이스 IO 보드 확인 ITS/ACU
	if ioB == "acu":
		mode = "ACU API"
		cfg["gpioIn"] = {}
		cfg["gpioOut"] = {}
		# for key, value in list(share["ioBoard"]["acu"]["setIO"].items()):
		for key, value in share["ioBoard"]["acu"]["setIO"].iteritems():
			# print key, value
			if value: # Relay
				id = "R"+key[2:4]
				cfg["gpioOut"][id] = share["ioBoard"]["acu"]["gpio"][key]
			else: # Sensor
				id = "S"+key[2:4]
				cfg["gpioIn"][id] = share["ioBoard"]["acu"]["gpio"][key]
		cfg["gpioPw"] = {}
		# for key, value in list(share["ioBoard"]["acu"]["setPW"].items()):
		for key, value in share["ioBoard"]["acu"]["setPW"].iteritems():
			id = "P"+key[2:4]
			cfg["gpioPw"][id] = share["ioBoard"]["acu"]["gppw"][key]
	else: # ITS
		mode = "ITS API"
		cfg["gpioIn"] = {}
		cfg["gpioIn"]["S01"] = 19
		cfg["gpioIn"]["S02"] = 13
		cfg["gpioIn"]["S03"] = 6
		cfg["gpioIn"]["S04"] = 5
		cfg["gpioIn"]["S05"] = 22
		cfg["gpioIn"]["S06"] = 27
		cfg["gpioIn"]["S07"] = 17
		cfg["gpioIn"]["S08"] = 4
		
		cfg["gpioOut"] = {}
		cfg["gpioOut"]["R01"] = 18
		cfg["gpioOut"]["R02"] = 23
		cfg["gpioOut"]["R03"] = 24
		cfg["gpioOut"]["R04"] = 25

		cfg["gpioPw"] = {}
		cfg["gpioPw"]["P01"] = 12

	saveConfig(cfg,"./FSI.json")

	openning()
	print(("Running Mode: %s"%mode))		

	masquerade(cfg["device"])

	# # 개별 존 데몬 실행
	for (k, v) in cfg["local"]["zone"].items():
		run_demon_FDX(k, v)

	
	run_demon_FSI()

if __name__ == "__main__":
	kill_demon_FSI()
	kill_demon_FDX()

	cfg = {} # 전역 변수
	share = readConfig("/home/pi/common/config.json")

	src_node = "{}/node_modules".format(share["path"]["common"])
	tar_node = "{}/node_modules".format(share["path"]["fsi"])
	if os.path.isdir(tar_node):
		pass
	else:
		os.symlink(src_node, tar_node)

	main()

"""
FD322 설정
	Connect Mode
		Passive Connection:
			Accept Incoming:	Yes
			Password Required:	No
		Active Connection:
			Active Connect:		Auto Start
			Password:	

	Endpoint Configuration:
		Local Port:		10001
		Auto increment for active connect: Check
		Remote Port:	52001
		Remote Host:	192.168.168.10
"""