#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import requests
import traceback, os
import json

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

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(share,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(share, json_file, sort_keys=True, indent=4)

def yes_or_no(question):
	while "the answer is invalid":
		reply = str(raw_input(question+' (y/n): ')).lower().strip()
		if reply:
			if reply[0] == 'y':
				return True
			if reply[0] == 'n':
				return False

def httpRequest(method_name, url, dict_data, is_urlencoded=True):
	"""Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
	"""
	url  = 'http://192.168.0.80:9991' # 접속할 사이트주소 또는 IP주소를 입력한다 
	data = {'uid':'Happy','pid':'Birth','sid':'Day'}         # 요청할 데이터
	response = httpRequest(method_name='GET/POST', url=url, dict_data=data)

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
	try:
		if method_name == 'GET': # GET방식인 경우
			response = requests.get(url=url, params=dict_data)
		elif method_name == 'POST': # POST방식인 경우
			if is_urlencoded is True:
				response = requests.post(url=url, data=dict_data, timeout=1, headers={'Content-Type': 'application/x-www-form-urlencoded'})
			else:
				response = requests.post(url=url, data=json.dumps(dict_data), timeout=1, headers={'Content-Type': 'application/json'})
		# return response
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

	## 프로그램 선택 및 실행 순서
	print("Select Program")
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
			reponse = httpRequest("POST", share["license"]["server_url"]+"/licenseSrvAdd.php", watch["fixed"])
			print ("\t{} - {}".format(share["license"]["server_addr"], reponse))
			break
		else:
			continue

if __name__ == '__main__':
	configJson = "/home/pi/common/config.json"

	# 환경설정 파일이 없으면 바로 종료
	if os.path.isfile(configJson):
		share = readConfig(configJson)
	else: 
		exit("Expired License, Call administrator")

	# watchdog의 실행 이력이 없으면 종료	
	watchdog = share["path"]["config"]+"/watchdog.json"
	if os.path.isfile(watchdog):
		watch = readConfig(watchdog)
	else: 
		exit("Watchdog is Not Running, Call administrator")

	run = share["runTable"]


	try:
		main()
	except KeyboardInterrupt:
		print ("\nCanceled")
	except Exception as e:
		print (str(e))
		traceback.print_exc()
		os._exit(1)