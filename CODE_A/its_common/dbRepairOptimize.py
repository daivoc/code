#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import json
import subprocess

'''
* 터미널에서 복구 방법 (MYSQL)
	+ Check
		$ mysqlcheck -uits -pGXnLRNT9H50yKQ3G --check its_web

	+ Repair
		$ mysqlcheck -uits -pGXnLRNT9H50yKQ3G --auto-repair its_web

	+ Optimize
		$ mysqlcheck -uits -pGXnLRNT9H50yKQ3G --optimize its_web
'''

## 환경설정 파일(JSON) 읽기
def readConfig():
	with open('/home/pi/common/config.json') as json_file:
		return json.load(json_file)

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

def main():
	cfg = readConfig()
	print("""
	본 프로그램은 
	데이터베이스 테이블 최적화 프로그램.
	실행중 프로그램이 종료때 까지 기다려야 함.
	""")
	confirm = raw_input('confirm? (Y/n)')
	if confirm == "Y":
		cmd = "mysqlcheck -u{0} -p{1} --auto-repair {2}".format(cfg["mysql"]["user"], cfg["mysql"]["pass"], cfg["mysql"]["name"])
		print(str(cmd_proc_Popen(cmd)).strip())
		print("waiting ...")
		cmd = "mysqlcheck -u{0} -p{1} --optimize {2}".format(cfg["mysql"]["user"], cfg["mysql"]["pass"], cfg["mysql"]["name"])
		print(str(cmd_proc_Popen(cmd)).strip())

		confirm = raw_input('Reboot System? (Y/n)')
		if confirm == "Y":
			cmd_proc_Popen("sudo reboot")

if __name__ == '__main__':
	main()
