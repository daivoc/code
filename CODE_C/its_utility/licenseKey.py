#!/usr/bin/env python
import sys
import uuid
import getpass
import time
import subprocess 
import requests
import traceback, os
import pymysql
import json
from hashlib import sha256

import socket
import fcntl
import struct

## https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
bold = '\033[1m' # Bold
uline = '\033[4m' # Underline
Revs = '\033[7m' # Reversed

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # Red
G  = '\033[32m' # Green
Y  = '\033[33m' # Yellow
B  = '\033[34m' # Blue
P  = '\033[35m' # Purple
C  = '\033[36m' # Cyan# Cyan

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(share,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(share, json_file, sort_keys=True, indent=4)

def kill_demon_watchdog():
	# 아래 grep에서 스페이스를 포함해야 자신(run_GIKENT.pyc)을 죽이지 않는다
	cmd = "pkill -9 -ef watchdog.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_watchdog"

def get_cpu_serial():
	cpuserial = ""
	f = open("/proc/cpuinfo","r")
	for line in f:
		if line[0:6]=="Serial":
			cpuserial = line[10:26]
	f.close()
	return cpuserial

def get_mac_address():
	return hex(uuid.getnode())

def itsSetConfig(key, value): # table
	cursor = None
	conn = None
	query = "UPDATE g5_config SET " + key + " = '" + value + "' " 
	# print query

	try:
		conn = pymysql.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		return cursor.rowcount
	except pymysql.Error as error:
		return error
	finally:
		cursor.close()
		conn.close()

def itsSetMember(key, value, member): # table
	cursor = None
	conn = None
	query = "UPDATE g5_member SET " + key + " = '" + value + "' WHERE mb_id = '" + member + "' " 
	# print query

	try:
		conn = pymysql.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		return cursor.rowcount
	except pymysql.Error as error:
		return error
	finally:
		cursor.close()
		conn.close()

def yes_or_no(question):
	while "the answer is invalid":
		reply = str(raw_input(question+' (y/n): ')).lower().strip()
		if reply:
			if reply[0] == 'y':
				return True
			if reply[0] == 'n':
				return False

def httpRequest(method_name, url, dict_data, is_urlencoded=True):
	""" Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 
	D:\code\web_page\its_server\ecosLicense\licenseSrvAdd.php 와 연계
	"""
	"""
	('POST', u'http://119.207.126.79/its_server/ecosLicense/licenseSrvAdd.php', {u'macAddr': 'dc:a6:32:30:06:fe\n', u'run': u'api3 ', u'license': 'c47327a67e01ccc853cdb0dc4b2a9a86169b7e8d747e2ccdff99875ee8103e3f', u'deviceModel': u'Raspberry Pi 4 Model B Rev 1.1', u'execTime': u'0:00:00.273343', u'liveTime': u'1554841.80', u'noLicense': 2592000, u'ipAddr': '192.168.0.70', u'dateTime': u'2022-08-03 13:10:57.804697', u'diskSize': u'59G', u'serialKey': u'10000000fcf3ea29', u'systemTitle': 'ECOS', u'licenseStatus': u'Approved', u'ioBoard': u'ITS STD', u'lastStart': u'2022-07-16 13:16:56'})


	"fixed": {
	    "dateTime": "2021-04-03 13:50:10.962676",
	    "execTime": "0:00:00.262464",
	    "ioBoard": "ITS STD",
	    "ipAddr": "192.168.0.20",
	    "lastStart": "2021-04-02 05:36:32",
	    "license": "7cd0f146d69d991490092ab4524a7fab5289dcf6ff03380f3736dcc26dc1f1fd",
	    "licenseStatus": "Approved",
	    "liveTime": "116018.61",
	    "noLicense": 2592000,
	    "run": "GIKENT FSI GPWIO TABLE GPIO",
	    "serialKey": "10000000204d1eed",
	    "systemTitle": "ECOS"
	},
	"""
	# print(json.dumps(dict_data))
	try:
		if method_name == 'GET': # GET방식인 경우
			response = requests.get(url=url, params=dict_data)
		elif method_name == 'POST': # POST방식인 경우
			if is_urlencoded is True:
				headers = {'Content-Type': 'application/x-www-form-urlencoded'}
				response = requests.post(url=url, data=dict_data, timeout=1, headers=headers)
			else:
				headers = {"Content-Type": "application/json; charset=utf-8"}
				response = requests.post(url=url, data=json.dumps(dict_data), timeout=1, headers=headers)
			# headers = {"Content-Type": "application/json; charset=utf-8"}
			# response = requests.post(url=url, data=json.dumps(dict_data), timeout=1, headers=headers)
		return response.status_code
	except requests.exceptions.Timeout:
		# Maybe set up for a retry, or continue in a retry loop
		return "Timeout Error {0}".format(url)
	except requests.exceptions.TooManyRedirects:
		# Tell the user their URL was bad and try a different one
		return "Bad URL Error {0}".format(url)
	except requests.exceptions.RequestException as e:
		# catastrophic error. bail.
		# raise SystemExit(e)
		return "Request Error {0}".format(url)
	except:
		return "Unknown Error {0}".format(url)


def main():
	###################################
	## 파일 config.json 사용자 변수 선언
	if byManual:
		print("Type Admin Keycode")
		keycode = getpass.getpass(R+"Keycode:\t"+W) # optex5971
		if not keycode:
			exit("No Keycode. Try again.")
		print("Enter or Type ITS Serial")
		serialKey = raw_input(G+"Serial No:\t"+W)
		# print("New IP Address(ex: 192.168.0.20)")
		# ipAddress = raw_input(P+"New IP:\t"+W)
	else:
		keycode = autoKeycode
		serialKey = ""
		# ipAddress = ""

	if not serialKey:	
		serialKey = get_cpu_serial()
		if not serialKey: # ITS가 아니 장비인 경우 MAC Address 를 사용한다.
			serialKey = get_mac_address()

	hash = sha256(serialKey + sha256(keycode).hexdigest()).hexdigest()

	itsSetConfig("cf_title", keycode) # 타이틀 등록
	itsSetMember("mb_1", hash, "manager") # 라이센스 등록
	# itsSetMember("mb_4", ipAddress, "manager") # IP 등록

	# save new system title
	watch["fixed"]["systemTitle"] = keycode
	# save new system licnse
	watch["fixed"]["license"] = hash

	if not byManual:
		watch["fixed"]["licenseStatus"] = "N/A" # 자동등록인 경우 
	# # save new IP
	# if ipAddress:
	# 	pass
	# else:
	# 	its_iface = str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()
	# 	ipAddress = get_ip_address(its_iface).strip()

	its_iface = str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()
	watch["fixed"]["ipAddr"] = get_ip_address(its_iface).strip()

	watch["fixed"]["macAddr"] = cmd_proc_Popen("head -n1 /sys/class/net/{}/address".format(its_iface)).strip()

	## 프로그램 선택 및 실행 순서
	print("Select Program")
	# share["run"] = {} # 
	# watch["fixed"]["run"] = ""
	# for key, value in run.items():
	# 	if yes_or_no(key):
	# 		share["run"][key] = run[key]
	# 		watch["fixed"]["run"] += key + " "
	runList = {}
	orderNo = 0
	showList = ""
	for key in sorted(run):
		orderNo += 1
		runList[orderNo] = key
		if orderNo % 4 is 0:
			enter = "\n"
		else:
			enter = " "
		showList += "{2}{4}{0:>2}{3}:{1:<8}".format(orderNo,key,Y,W,bold) + enter
	print(showList)

	while True:
		share["run"] = {} # 
		watch["fixed"]["run"] = ""
		selected = raw_input("Select number(order) with space: ")
		for key in selected.split():
			try:
				share["run"][runList[int(key)]] = run[runList[int(key)]]
				watch["fixed"]["run"] += runList[int(key)] + " "
			except:
				pass

		if yes_or_no("Selected '{1}{3}{0}{2}', continue?".format(watch["fixed"]["run"],C,W,bold)):
			## 프로그램 선택 및 실행 순서
			saveConfig(share,configJson) ## 저장
			# ITS Server에 자동 등록 192.168.0.8
			reponse = httpRequest("POST", serverUrl, watch["fixed"])

			print ("\t{} - {}".format(share["license"]["server_addr"], reponse))
			print(P+"ITS License:"+Y+" >>>> "+W+hash+Y+" <<<<"+W)
			# print(watch["fixed"])
			break
		else:
			continue

	
if __name__ == '__main__':
	configJson = "/home/pi/common/config.json"
	if len(sys.argv) > 1:
		byManual = 0
		autoKeycode = sys.argv[1]
		autoSrvIP = sys.argv[2]
	else:
		byManual = 1

	# 환경설정 파일이 없으면 바로 종료
	if os.path.isfile(configJson):
		share = readConfig(configJson)
	else: 
		kill_demon_watchdog()
		exit("Expired License, Call administrator")

	# watchdog의 실행 이력이 없으면 종료	
	watchdog = share["path"]["config"]+"/watchdog.json"
	if os.path.isfile(watchdog):
		watch = readConfig(watchdog)
	else: 
		kill_demon_watchdog()
		exit("Watchdog is Not Running, Call administrator")

	if byManual:
		if share["systemCmd"]["execCnt"]:
			share["systemCmd"]["execCnt"] = share["systemCmd"]["execCnt"] - 1
		else:
			exit("Limit Over if Running Count. \nCall administrator")
	else: # setup_its.sh에 의한 실행이면 횟수제한 없음
		share["license"]["server_url"] = share["license"]["server_url"].replace(share["license"]["server_addr"], autoSrvIP)
		share["license"]["server_addr"] = autoSrvIP

	serverUrl = share["license"]["server_url"]+"/licenseSrvAdd.php"

	run = share["runTable"]

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCanceled")
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		os._exit(1)
