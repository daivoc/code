#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import fcntl
import struct
import socket
import subprocess 
import json
import pymysql
# import MySQLdb

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)

# 멤버 아이디(its)에 선택필드(mb_1 ~ 9)
def database_test(): # Optex Microwave
	try:
		conn = pymysql.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset="utf8", use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		return 1
	except:
		return 0

def create_folder(path):
	if not os.path.exists(path): 
		os.makedirs(path)
	# 모드수정을 해야만 Other Group에서 접근가능 함
	os.chmod(path, 0o707)
	
# 자신 아이피 확인 
def get_ip_address(ifname): # get_ip_address("eth0")
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915, # SIOCGIFADDR
			struct.pack("256s", ifname[:15])
		)[20:24])
	except:
		return

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

# 시스템 헬스체크 데몬 실행
def run_demon_watchdog():
	print(kill_demon_watchdog())
	cmd = "python %s/watchdog.pyc 2>&1 & " % (share["path"]["common"])
	# stdout=subprocess.PIPE, stderr=subprocess.PIPE 인경우 서브프로세서로 실행시 오류를 알수가 없다.
	p = subprocess.Popen(cmd, shell=True)
	return p
def kill_demon_watchdog():
	cmd = "pkill -9 -ef watchdog.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_watchdog"

# 시스템 데몬 메니저 실행
def run_demon_userApi():
	print(kill_demon_userApi())
	cmd = "python %s/userApi.pyc 2>&1 & " % (share["path"]["common"])
	# stdout=subprocess.PIPE, stderr=subprocess.PIPE 인경우 서브프로세서로 실행시 오류를 알수가 없다.
	p = subprocess.Popen(cmd, shell=True)
	return p
def kill_demon_userApi():
	cmd = "pkill -9 -ef userApi.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_userApi"

# def check_ipaddress(address):
# 	try:
# 		network = ipaddress.IPv4Network(address)
# 		return network
# 	except ValueError:
# 		return ("address/netmask is invalid for IPv4:", address)

def setNTP(ntpSrv):
	cfg = "/etc/chrony/chrony.conf" ## chrony 설치 확인 용도임
	if os.path.exists(cfg): ## chrony 설치 확인 
		# cmd = "sudo chronyc add server %s" % (ntpSrv) ## NTP 서버 추가
		# result = os.system(cmd)
		# return "Run NTP Sync to %s : %s" % (ntpSrv, result)
		server = ntpSrv.split("||")
		for addr in server:
			cmd = "sudo chronyc add server %s" % (addr) ## NTP 서버 추가
			result = os.system(cmd)
		return "Run NTP Sync to %s : %s" % (ntpSrv, result)
	else:
		return "Not installed Chrony"
		
def setVIP(virtualIP): ## 가상아이피 설정
	cmd = "sudo ifconfig %s:0 %s up" % (its_iface, virtualIP)
	result = os.system(cmd)
		
def setIP(newIP, newNM, newGW):
	# IP, NETMASK설정은 ifconfig명령으로~
	# # ifconfig eth0 192.168.1.123 netmask 255.255.255.0 up
	# GATEWAY설정은 route명령으로~
	# # route add default gw 192.168.1.1
	# # route add default gw 62.210.123.1

	curIP = its_ipAddr
	curNM = str(cmd_proc_Popen("ifconfig "+its_iface+" | grep 'inet' -m1 | awk -F' ' '{print $4}' 2>/dev/null")).strip()
	curGW = str(cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $2}' 2>/dev/null")).strip()
	
	setIP = str(cmd_proc_Popen("grep '^address' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null")).strip()
	setNM = str(cmd_proc_Popen("grep '^netmask' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null")).strip()
	setGW = str(cmd_proc_Popen("grep '^gateway' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null")).strip()

	if newIP and setIP and setIP != newIP:
		cmd = "sudo sed -i -e 's/%s/%s/g' /etc/network/interfaces" % (setIP, newIP)
		result = os.system(cmd)
		print ("\tSystem newIP:{}".format(newIP))

		# sudo ifconfig eth0 192.168.0.80 netmask 255.255.255.0 up
		if curIP != newIP:
			# cmd = "sudo ifconfig %s %s" % (its_iface, newIP)
			# result = os.system(cmd)
			cmd = "sudo reboot"
			result = os.system(cmd)

	if newNM and setNM and setNM != newNM:
		cmd = "sudo sed -i -e 's/%s/%s/g' /etc/network/interfaces" % (setNM, newNM)
		result = os.system(cmd)
		print ("\tSystem newNM:{}".format(newNM))

		# sudo ifconfig eth0 192.168.0.80 netmask 255.255.255.0 up
		if curNM != newNM:
			cmd = "sudo ifconfig %s netmask %s" % (its_iface, newNM)
			result = os.system(cmd)

	if newGW and setGW and setGW != newGW:
		cmd = "sudo sed -i -e 's/%s/%s/g' /etc/network/interfaces" % (setGW, newGW)
		result = os.system(cmd)
		print ("\tSystem newGW:{}".format(newGW))
		
		if curGW != newGW:
			cmd = "sudo route add default gw %s" % (newGW)
			result = os.system(cmd)

def itsMemberConfig(field, id): # table
	cursor = None
	conn = None
	query = "SELECT " + field + " FROM g5_member WHERE mb_id = '" + id + "'" # its or manager
	# mb_4 - system ip address
	try:
		conn = pymysql.connect(host=share["mysql"]["host"], user=share["mysql"]["user"], passwd=share["mysql"]["pass"], db=share["mysql"]["name"], charset="utf8", use_unicode=True) 
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
	newIP = str(itsMemberConfig("mb_4", "manager")["mb_4"]).strip()
	newNM = str(itsMemberConfig("mb_5", "manager")["mb_5"]).strip()
	newGW = str(itsMemberConfig("mb_6", "manager")["mb_6"]).strip()
	ntpSrv = str(itsMemberConfig("mb_8", "manager")["mb_8"]).strip()
	virtualIP = str(itsMemberConfig("mb_9", "manager")["mb_9"]).strip()

	## VIP Server
	if(virtualIP):
		print("\t{}".format(setVIP(virtualIP)))
	else:
		print("\tNot in use Virtual IP")

	## NTP Server
	if(ntpSrv):
		print("\t{}".format(setNTP(ntpSrv)))
	else:
		print("\tNot in use NTP server")

	## IP 확인 및 변경
	print("\tSet IP {}".format(setIP(newIP, newNM, newGW)))

	# 모니터링 헬스서버 정보가 있으면 실행
	if is_online:
		run_demon_userApi() # 시스템 관리 실행
		run_demon_watchdog() # 시스템 헬스체크 데몬 실행
	else: # 단독 모드
		run_demon_watchdog() # 시스템 헬스체크 데몬 실행

	# 설정된 프로그램 실행
	for key in share["run"]:
		if key in share["path"]:
			path = share["path"][key]
		else:
			continue
		command = share["run"][key]["command"]
		if path and command:
			# print("\tRun {}".format(key.upper()))
			cmd = "cd {0} && /usr/bin/python {1} > /tmp/{2}.log".format(path,command,key)
			print("\tRun {}".format(cmd))
			# print (subprocess.Popen(cmd, shell=True))
			# print (os.system(cmd))
			subprocess.Popen([cmd], shell=True)

	# ## 헬스체크를 위해 시스템이 구동 되고 있음을 반응하는 포트리스너 <<<<
	# ## 응답만하며 어떤 작업도 하지 않는다.
	# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
	# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # <--- 아직 검증안됨 "Address already in use" 무시
	# sock.bind((its_ipAddr, share["port"]['systemIn'])) # <------- 소켓을 주소로 바인딩
	# sock.listen(5) # <------ listening 시작. 최대 클라이언트 연결 수 5개
	# print('\tDaemon of API {0}:{1}'.format(its_ipAddr,share["port"]['systemIn']))
	
	# while True:
	# 	conn, addr = sock.accept() # print('From:', conn, addr[0])
	# 	# print('From:{} {}'.format(addr[0], addr[1]))
	# 	conn.close() # <------ 클라이언트 세션 종료
	# s.close() # <------- 위 루프가 끝나지 않으므로 이 라인은 실행되지 않는다.
	# ## 헬스체크를 위해 시스템이 구동 되고 있음을 반응하는 포트리스너 >>>>
		
if __name__ == "__main__":
	configJson = "/home/pi/common/config.json"
	if os.path.isfile(configJson):
		share = readConfig(configJson)
	else: # 환경설정 파일이 없으면 바로 종료
		kill_demon_watchdog()
		kill_demon_userApi()
		exit("Call administrator")

	err_max_count = 10 # 10회 시도
	while True: # 데이터베이스 동작 확인
		if database_test(): 
			print("*** PASS ***\n\tDatabase Ready.") # 데이터베이스 실행 대기
			break
		else:
			print("*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ...") # 데이터베이스
			err_max_count = err_max_count - 1
			if not err_max_count: exit("Time out")
		time.sleep(5) # 데이터베이스 준비시간

	create_folder(share["path"]["config"]) # Configuration 폴더 생성 /home/pi/.config
	create_folder(share["path"]["log"]) # Log 폴더 생성 /var/www/html/its_web/data/log

	# USER 폴더 생성 
	create_folder(share["path"]["its_web"]+share["path"]["user"]['home'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['home'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['audio'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['code'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['config'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['image'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['note'])
	create_folder(share["path"]["its_web"]+share["path"]["user"]['video'])

	its_iface = str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()
	its_ipAddr = get_ip_address(its_iface) # .strip()
	# its_ipAddr = str(itsMemberConfig("mb_4", "manager")["mb_4"]).strip() # 2021-12-24 15:10:46

	if its_iface and its_ipAddr:
		print ("\tSystem IP:{}".format(its_ipAddr))
		is_online = 1
	else:
		print ("\tError Network Interface from systemConfig")
		is_online = 0
		# exit ("Error Network Interface")

	print ("\tInterface:{} {}").format(its_iface, its_ipAddr)

	main()
