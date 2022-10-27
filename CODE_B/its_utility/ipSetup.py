#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import traceback, os
import MySQLdb
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
	
def itsSetMember(key, value, member): # table
	cursor = None
	conn = None
	query = "UPDATE g5_member SET " + key + " = '" + value + "' WHERE mb_id = '" + member + "' " 
	# print query

	try:
		conn = MySQLdb.connect(host=share['mysql']['host'], user=share['mysql']['user'], passwd=share['mysql']['pass'], db=share['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		return cursor.rowcount
	except MySQLdb.Error as error:
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

def main():

	ap_addr = raw_input(Y+"Enter address : "+W)
	ap_netm = raw_input(Y+"Enter netmask : "+W)
	ap_gate = raw_input(Y+"Enter gateway : "+W)
	ap_WDIP = raw_input(Y+"Enter watchdog : "+W)
	ap_NTPD = raw_input(Y+"Enter ntp srv : "+W)

	itsSetMember("mb_4", ap_addr, "manager") # IP 등록
	itsSetMember("mb_5", ap_netm, "manager") # IP 등록
	itsSetMember("mb_6", ap_gate, "manager") # IP 등록
	itsSetMember("mb_3", ap_WDIP, "manager") # IP 등록
	itsSetMember("mb_8", ap_NTPD, "manager") # IP 등록
	
if __name__ == '__main__':

	configJson = "/home/pi/common/config.json"

	# 환경설정 파일이 없으면 바로 종료
	if os.path.isfile(configJson):
		share = readConfig(configJson)
	else: 
		exit("No Common Config, Call administrator")

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCanceled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)
