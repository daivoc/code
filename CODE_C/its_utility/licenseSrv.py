#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import json

## 환경설정 파일(JSON) 읽기
def readConfig():
	with open(configJson) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(config):
	with open(configJson, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def main():
	cfg = readConfig()
	print("""
	본 프로그램은 
	라이센스서버의 아이피(주소) 변경 용도로 사용.
	필요에 따라 포트번호가 포함된 주소등록 가능.
	예) 119.207.126.79
	""")
	print("기존의 IP - {}".format(cfg["license"]["server_addr"]))
	newIP = raw_input('새로운 IP - ')
	if newIP:
		confirm = raw_input('기존 IP {}을(를) IP {}(으)로 변경합니다. (Y/n) : '.format(cfg["license"]["server_addr"],newIP))
		if confirm == "Y":
			cfg["license"]["server_url"] = cfg["license"]["server_url"].replace(cfg["license"]["server_addr"], newIP)
			cfg["license"]["server_addr"] = newIP
			print("변경 되었습니다.")
		else:
			print("취소 되었습니다.")
	else:
		print("취소 되었습니다.")

	saveConfig(cfg)

if __name__ == '__main__':
	configJson = "/home/pi/common/config.json"
	exit("Terminated")
	main()
