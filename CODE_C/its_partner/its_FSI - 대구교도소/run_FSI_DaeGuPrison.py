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
	cmd = "kill -9 $(ps aux | grep ' FSI.pyc' | awk '{print $2}')"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

def run_demon_FSI(): 
	cmd = "cd %s; python FSI.pyc 2>&1 & " % (share['path']['fsi'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

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

def masquerade(masq):
	# 아이피 라우팅 기능으로 내부 환경설정의 
	# MASQUERADE -> action 상태에 따라 실행 된다.
	# 삭제시 리스트를 통해 총 수를 확인한 후 일괄 삭제한다. 
	if masq["active"]:
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
	cfg = {}

	cfg["device"] = {}
	cfg["device"]["name"] = ""
	cfg["device"]["addr"] = "192.168.168.30"
	cfg["device"]["port"] = 10001 # 52101

	cfg["local"] = {}
	cfg["local"]["host"] = "192.168.168.10"
	cfg["local"]["port"] = 52001 # 52001

	cfg["pathLog"] = share["path"]["log"]

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

	cfg["site"] = local.copy() # 
	saveConfig(cfg,"./FSI.json")
	
	openning()
	print(("Running Mode: %s"%mode))		

	masquerade(cfg["site"]["masquerade"])

	run_demon_FSI()

if __name__ == "__main__":
	kill_demon_FSI()

	share = readConfig("/home/pi/common/config.json")
	local = readConfig("/home/pi/FSI/config.json")
	main()
	exit()	
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