#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import subprocess 
import json

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(cfg,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(cfg, json_file, sort_keys=True, indent=4)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_itsAPI(): 
	cmd = "kill $(ps aux | grep ' itsAPI.pyc' | awk '{print $2}')" # '{스페이스} itsAPI.pyc' 중요함
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
def run_demon_itsAPI(): 
	cmd = "cd %s; python itsAPI.pyc 2>&1 & " % (share['path']['gpacu'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def main():
	cfg = {}
	cfg["category"] = {}
	cfg["category"]["gpio"] = { "status":"", "id":"", "hold":"", "msg":"" }
	cfg["category"]["audio"] = { "source":"", "target":"", "volume":"", "command":"", "loop":"" }
	cfg["category"]["camera"] = {}
	cfg["category"]["system"] = {}
	cfg["category"]["maria"] = {}
	cfg["category"]["custom"] = {}
	cfg["category"]["debug"] = True

	if len(sys.argv) == 1: # its
		mode = "ACU API"
		cfg["gpioIn"] = {}
		cfg["gpioOut"] = {}
		for key, value in share["ioBoard"]["acu"]["setIO"].iteritems():
			# print key, value
			if value: # Relay
				id = "R"+key[2:4]
				cfg["gpioOut"][id] = share["ioBoard"]["acu"]["gpio"][key]
			else: # Sensor
				id = "S"+key[2:4]
				cfg["gpioIn"][id] = share["ioBoard"]["acu"]["gpio"][key]
		# cfg["gpioOut"]["P01"] = 12
		# cfg["gpioOut"]["P02"] = 8
		# cfg["gpioOut"]["R01"] = 19
		# cfg["gpioOut"]["R02"] = 13
		# cfg["gpioOut"]["R03"] = 6
		# cfg["gpioOut"]["R04"] = 5
		# cfg["gpioOut"]["R05"] = 22
		# cfg["gpioOut"]["R06"] = 27
		# cfg["gpioOut"]["R07"] = 17
		# cfg["gpioOut"]["R08"] = 4
		# cfg["gpioOut"]["R09"] = 26
		# cfg["gpioOut"]["R10"] = 21
		# cfg["gpioOut"]["R11"] = 20
		# cfg["gpioOut"]["R12"] = 16
		# cfg["gpioOut"]["R13"] = 7
		# cfg["gpioOut"]["R14"] = 25
		# cfg["gpioOut"]["R15"] = 24
		# cfg["gpioOut"]["R16"] = 23

		cfg["gpioPw"] = {}
		for key, value in share["ioBoard"]["acu"]["setPW"].iteritems():
			id = "P"+key[2:4]
			cfg["gpioPw"][id] = share["ioBoard"]["acu"]["gppw"][key]
			# # print key, value
			# if value: # Relay
			# 	id = "P"+key[2:4]
			# 	cfg["gpioPw"][id] = share["ioBoard"]["acu"]["gppw"][key]
			# else: # Sensor
			# 	id = "P"+key[2:4]
			# 	cfg["gpioPw"][id] = share["ioBoard"]["acu"]["gppw"][key]
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

	saveConfig(cfg,"./itsAPI.json")

	run_demon_itsAPI()
	print('Running %s:'%mode)		



if __name__ == '__main__':
	share = readConfig('/home/pi/common/config.json')
	kill_demon_itsAPI()
	main()
	exit()	