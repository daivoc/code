#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import re
import fcntl
import struct
import shutil
import time
import json
import uuid
import socket
import subprocess
from datetime import datetime
from hashlib import sha256
import pymysql
# import MySQLdb
from warnings import filterwarnings

filterwarnings('ignore', category = pymysql.Warning)

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(share,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(share, json_file, sort_keys=True, indent=4)

## 핼스서버로 자료 전송
def reportToWdSrv(ip, port, envData):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	try: 
		sock.connect((ip,int(port)))
		# print >>sys.stderr, 'sending "%s"' % envData
		# return sock.send(envData) 
		return sock.sendall(envData) 
	except socket.error:
		# print >>sys.stderr, 'socket.error'
		return 0
	except socket.timeout:
		# print >>sys.stderr, 'socket.timeout'
		return 0
	finally:
		sock.close() 

## 자신의 IP Address를 추출한다.
def get_ip_address():
	ifname = str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try: 
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])
	except:
		return 0

def get_mac_address():
	return hex(uuid.getnode())

def get_cpu_serial():
	cpuserial = ""
	f = open("/proc/cpuinfo","r")
	for line in f:
		if line[0:6]=="Serial":
			cpuserial = line[10:26]
	f.close()
	return cpuserial

def get_deviceModel():
	with open("/proc/device-tree/model", "r") as f:
		lines = f.read()[:-1] ##Assume the sample file has 3 lines
	return lines
	# return str(cmd_proc_Popen("cat /proc/device-tree/model")).strip()

def get_diskSize():
	disk = subprocess.check_output ('df -h --output=size,used,avail,pcent / | tail -1', shell=True)
	dT = re.sub(' +',',',disk.strip()).split(',') #  15G  2.8G   11G  21%
	return dT

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

def itsMemberConfig(field, id): # table 
	# cursor = None
	# conn = None
	query = "SELECT " + field + " FROM g5_member WHERE mb_id = '" + id + "'" 
	# mb_4 - system ip address
	try:
		conn = pymysql.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchone() # 커서의 fetchall()는 모두, fetchone()은 하나의 Row, fetchone(n)은 n개 만큼
	except pymysql.Error as error:
		return 0
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()

def itsSystemConfig(field): # 시스템 설정 값 반환 cf_title
	# cursor = None
	# conn = None
	query = "SELECT " + field + " FROM g5_config"
	# mb_4 - system ip address
	try:
		conn = pymysql.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchone() # 커서의 fetchall()는 모두, fetchone()은 하나의 Row, fetchone(n)은 n개 만큼
	except pymysql.Error as error:
		return 0
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()

def main():

	serialKey = get_cpu_serial()
	if not serialKey: # ITS가 아니 장비인 경우 MAC Address 를 사용한다.
		serialKey = get_mac_address()
	systemTitle = str(itsSystemConfig("cf_title")["cf_title"]).strip() # 시스템 타이틀을 키로 사용 함
	noLicense = (60 * 60 * 24 * share["license"]["trial_limit_due"])  # 30일간의 초 

	# 암호 생성 -> hash(시리얼키 + hash(시스템키))
	hash = sha256(serialKey + sha256(systemTitle).hexdigest()).hexdigest()

	wdSrvAddr = share["usrCfg"]["wdServer"] ## 
	wdSrvPort = share["port"]["watchdog"]["portIO"] # 53000
	actionDue = share["port"]["watchdog"]["interval"] # 생성주기 초

	myIpAddr = get_ip_address()
	# myIpAddr = share["usrCfg"]["myAddress"] # 2021-12-24 15:07:27

	if myIpAddr:
		pass
	else:
		print("Error Network Interface from watchdog {}".format(myIpAddr))
		# exit("Error Network Interface:{}".format(myIpAddr))

	print("watchdog {} {} {}".format(myIpAddr, wdSrvPort, actionDue))

	deviceModel = get_deviceModel().strip()
	diskSize = get_diskSize()[0]

	data = {}
	data["fixed"] = {}
	data["fixed"]["lastStart"] = cmd_proc_Popen("uptime -s").strip() # 마지막 부팅한 시각
	data["fixed"]["ipAddr"] = myIpAddr # 자신의 아이피
	data["fixed"]["macAddr"] = get_mac_address() # 맥주소
	data["fixed"]["serialKey"] = serialKey # H/W 키, RPI:cpu serial, Ubuntu: Mac Address
	data["fixed"]["systemTitle"] = systemTitle # config->key_system
	data["fixed"]["noLicense"] = noLicense # No License Lifetime
	data["fixed"]["deviceModel"] = deviceModel # deviceModel
	data["fixed"]["diskSize"] = diskSize # deviceModel

	data["fixed"]["run"] = "" # 사용중인 프로그램 목록 취합
	for key, value in share["run"].items():
		data["fixed"]["run"] += str(key) + " "
	data["fixed"]["run"] = data["fixed"]["run"].strip().upper()

	if share["usrCfg"]["ioBoard"]: # 릴레이 보드 형식 
		data["fixed"]["ioBoard"] = "ITS " + share["usrCfg"]["ioBoard"].upper()
	else:
		data["fixed"]["ioBoard"] = "ITS STD"

	if wdSrvAddr and wdSrvPort: # 진단 및 검진(mb_3)에 아이피가 있으면
		data["fixed"]["wdSrvUrl"] = ("{}:{}".format(wdSrvAddr,wdSrvPort))

	while True:
		# 날짜, 시간, 아이피, 메모리, 디스크, 온도, 실행시간 정보
		its_time = datetime.now()
		data["fixed"]["dateTime"] = str(its_time)

		with open('/proc/uptime') as second:
			curSec = second.read().split(' ')[0] # 338572.21(부팅후 지금까지 초) 1086929.08(idle uptime)
		liveTime = curSec
		# liveTime = subprocess.check_output('uptime -p', shell=True)
		data["fixed"]["liveTime"] = liveTime.strip()

		# 디스크 사용량
		# disk = subprocess.check_output ('df -h --output=size,used,avail,pcent / | tail -1', shell=True)
		# dT = re.sub(' +',',',disk.strip()).split(',')
		dT = get_diskSize()
		data["diskGb"] = {}
		data["diskGb"]["size"] = dT[0]
		data["diskGb"]["used"] = dT[1]
		data["diskGb"]["avail"] = dT[2]
		data["diskGb"]["pcent"] = dT[3]
		# diskUse = "T:%s U:%s(%s) A:%s"%(dT[0], dT[1], dT[3], dT[2]) # ' +' : 연속적인 스페이스, .split(',')


		topInfo = subprocess.check_output ('top -b -n 1 | sed -n 2,5p', shell=True)
		topList = topInfo.split('\n')
		# print topList[0] # 프로세서 실행정보
		# print topList[1] # CPU 점유정보
		# print topList[2] # 메모리 사용량
		# print topList[3] # 스왑 사용량

		# 프로세서 실행정보
		# Tasks: 117 total,   1 running, 116 sleeping,   0 stopped,   0 zombie
		pT = topList[0].strip().split(',')
		data["procCont"] = {}
		data["procCont"]["total"] = pT[0].strip().split(' ')[-2]
		data["procCont"]["running"] = pT[1].strip().split(' ')[-2]
		data["procCont"]["sleeping"] = pT[2].strip().split(' ')[-2]
		data["procCont"]["stopped"] = pT[3].strip().split(' ')[-2]
		data["procCont"]["zombie"] = pT[4].strip().split(' ')[-2]

		# CPU 점유정보
		# %Cpu(s):  1.4 us,  2.8 sy,  0.0 ni, 95.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
		cT = topList[1].strip().split(',')
		data["cpuPcent"] = {}
		data["cpuPcent"]["user"] = cT[0].strip().split(' ')[-2]
		data["cpuPcent"]["system"] = cT[1].strip().split(' ')[-2]
		# data["cpuPcent"]["ni"] = cT[2].strip().split(' ')[-2]
		data["cpuPcent"]["idle"] = cT[3].strip().split(' ')[-2]

		# 메모리 사용량
		# MiB Mem :   1939.4 total,   1520.2 free,    168.6 used,    250.7 buff/cache
		mT = topList[2].strip().split(',')
		data["memUseKb"] = {}
		data["memUseKb"]["total"] = mT[0].strip().split(' ')[-2]
		data["memUseKb"]["free"] = mT[1].strip().split(' ')[-2]
		# data["memUseKb"]["used"] = mT[2].strip().split(' ')[-2]

		# 스왑 사용량
		# MiB Swap:    100.0 total,    100.0 free,      0.0 used.   1694.9 avail Mem
		sT = topList[3].strip().split(',')
		data["swapUseKb"] = {}
		data["swapUseKb"]["total"] = sT[0].strip().split(' ')[-2]
		data["swapUseKb"]["free"] = sT[1].strip().split(' ')[-2]

		with open('/sys/class/thermal/thermal_zone0/temp') as temp:
			curCtemp = float(temp.read()) / 1000
			curFtemp = ((curCtemp / 5) * 9) + 32
		data["cpuTemp"] = curCtemp

		data["usePort"] = {}
		for port in service.keys():
			if myIpAddr: # 네트워크 모드이면
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(1)
				portOpen = sock.connect_ex((myIpAddr, port))
				sock.close()
				if portOpen:
					data["usePort"][service[port]] = 0 # 비실행
				else:
					data["usePort"][service[port]] = 1 # 실행중

		###########################
		## 시스템 라이센스 확인 - 시작
		## mb_1의 라이센스 키와 config 폴더 내에 파일명이 동일한지 확인 
		## 불일치시 GUI 화면 아래 메시지가 출력된다.

		licenseKey = str(itsMemberConfig('mb_1','manager')["mb_1"]).strip() # 라이브 등록
		data["fixed"]["license"] = licenseKey
		if licenseKey == hash: # 라이센스키 비교
			data["fixed"]["licenseStatus"] = "Approved"
			htmlMsg = """<div id="license" style="cursor:pointer;position:absolute;top:0;left:0;background:#258feac9;color:#fff;padding: 0 4px;z-index: 1;">Licensed</div>"""
		else:
			data["fixed"]["licenseStatus"] = "Illegal"
			htmlMsg = """<div id="license" style="cursor:pointer;position:absolute;top:0;left:0;background:#ff003cc9;color:#fff;padding: 0 4px;z-index: 1;">Required ITS License</div>"""

			## 라이센스 없이 일정시간을 넘게 사용한 경우
			## common/config.json을 이동한후 재부팅 한다.
			if float(data["fixed"]["liveTime"]) > float(noLicense):
				shutil.move("{0}/config.json".format(share["path"]["common"]), "{0}/config.json".format(share["path"]["config"]))
				os.system("sudo reboot")

		# 사용코드 - G:\Development\ecos_ITS\its_web\theme\ecos-its_optex\tail.php
		# systemMsg = ("{0}/systemMsg.htm".format(share["path"]["log"]))
		# with open(systemMsg, 'w') as f:
		# 	f.write(htmlMsg)
		systemMsg = ("{0}/systemMsg.htm".format(share["path"]["config"]))
		with open(systemMsg, 'w') as f:
			f.write(htmlMsg)
		## 시스템 라이센스 확인 - 종료
		###########################

		data["fixed"]["execTime"] = str(datetime.now() - its_time) ## 전체 실행에 소요된 시간

		# 파일 생성 - share["path"]["config"]/watchdog.json
		watchdogJson = ("{0}/watchdog.json".format(share["path"]["config"]))
		try:
			with open(watchdogJson, 'w') as outfile:
				json.dump(data, outfile, indent=4, sort_keys=True)
		except:
			print("Error Create watchdog.json")

		# 모니터링 서버에 헬스정보 전송
		if wdSrvAddr and wdSrvPort: # 진단 및 검진(mb_3)에 아이피가 있으면
			result = reportToWdSrv(wdSrvAddr, wdSrvPort, json.dumps(data))
			# if result: # Return error : 0, success : 0 < number
			# 	pass
			# else:
			# 	print("Error No IMS Reponse") # IP:%s port:%s, Check manager > Config > Watchdog IP "%(wdSrvAddr, wdSrvPort))

		if actionDue: 
			time.sleep(actionDue) # Second
		else:
			exit("No Watchdog Interval")
		
if __name__ == '__main__':
	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print share["file"]["html_src"]
	share = readConfig('/home/pi/common/config.json')
	share["usrCfg"] = {} 

	# 라이센스 키
	share["usrCfg"]["itsLicense"] = str(itsMemberConfig('mb_1','manager')["mb_1"]).strip()
	# 와치도그 서버 주소
	share["usrCfg"]["wdServer"] = str(itsMemberConfig('mb_3','manager')["mb_3"]).strip()
	share["usrCfg"]["myAddress"] = str(itsMemberConfig('mb_4','manager')["mb_4"]).strip()
	share["usrCfg"]["myNetmask"] = str(itsMemberConfig('mb_5','manager')["mb_5"]).strip()
	share["usrCfg"]["myGateway"] = str(itsMemberConfig('mb_6','manager')["mb_6"]).strip()
	share["usrCfg"]["myLanguage"] = str(itsMemberConfig('mb_7','manager')["mb_7"]).strip()
	share["usrCfg"]["ntpServer"] = str(itsMemberConfig('mb_8','manager')["mb_8"]).strip()
	share["usrCfg"]["ipVirtual"] = str(itsMemberConfig('mb_9','manager')["mb_9"]).strip()

	# 오디오 소스
	share["usrCfg"]["audioName"] = str(itsMemberConfig('mb_2','its')["mb_2"]).strip()
	share["usrCfg"]["audioTime"] = str(itsMemberConfig('mb_3','its')["mb_3"]).strip()

	# I/O 보드 종류 (STD/ACU)
	share["usrCfg"]["ioBoard"] = str(itsMemberConfig('mb_4','its')["mb_4"]).strip()

	# 릴레이 경보
	share["usrCfg"]["relayAddr"] = str(itsMemberConfig('mb_5','its')["mb_5"]).strip()
	share["usrCfg"]["relayPort"] = str(itsMemberConfig('mb_6','its')["mb_6"]).strip()
	share["usrCfg"]["relayNumber"] = str(itsMemberConfig('mb_7','its')["mb_7"]).strip()

	###############################################
	## 파일 config.json내용 저장
	saveConfig(share,'/home/pi/common/config.json') ## 저장
	
	# 시스템에 실행중인 프로세서 확인을 위한 포트 집합
	service = {
		4200:"shell", # Shell Box
		8040:"gpwio", # GPWIO.pyc
		8080:"gpwio", # GPWIO.pyc
		9311:"gpio_1", # table_GPIO.js
		9312:"gpio_2", # table_GPIO.js
		9313:"gpio_3", # table_GPIO.js
		9314:"gpio_4", # table_GPIO.js
		9315:"gpio_5", # table_GPIO.js
		9316:"gpio_6", # table_GPIO.js
		9317:"gpio_7", # table_GPIO.js
		9318:"gpio_8", # table_GPIO.js
		18040:"gpacu", # GPACU.pyc
		18080:"gpacu", # GPACU.pyc
		28001:"aoip", # table_GPIO.js
		35168:"giken_R", # GIKENT.js
		35268:"giken_S", # GIKENT.js
		64444:"union_R", # table_union.js
		64446:"union_S", # table_union.js
		38087:"ims_S", # IMS
		38088:"ims_R", # IMS
		53000:"health" # watchdog.pyc
	}

	main()