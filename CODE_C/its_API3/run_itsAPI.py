#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import os
import time
import subprocess 
import json
import socket
import struct
import fcntl
import pymysql

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(cfg,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(cfg, json_file, sort_keys=True, indent=4)


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

def get_interface(): # return 'eth0'
	return cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null").strip().decode()
	 
# 자신 아이피 확인 
def get_ip_address(iface): # get_ip_address("eth0")
	return cmd_proc_Popen("ifconfig "+iface+" | grep 'inet ' | cut -d: -f2 | awk '{print $2}'").strip().decode()
	# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# try:
	# 	return socket.inet_ntoa(fcntl.ioctl(
	# 		s.fileno(),
	# 		0x8915, # SIOCGIFADDR
	# 		struct.pack("256s", iface[:15])
	# 	)[20:24])
	# except:
	# 	return 'localhost'

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

def setSystemIP(newIP, newNM, newGW): # IP, NETMASK, GATEWAY 설정
	# IP, NETMASK설정은 ifconfig명령으로~
	# # ifconfig eth0 192.168.1.123 netmask 255.255.255.0 up
	# GATEWAY설정은 route명령으로~
	# # route add default gw 192.168.1.1

	iface = get_interface()
	if iface:
		curIP = get_ip_address(iface)
		curNM = cmd_proc_Popen("ifconfig "+iface+" | grep 'inet' -m1 | awk -F' ' '{print $4}' 2>/dev/null").strip().decode()
		curGW = cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $2}' 2>/dev/null").strip().decode()
		
		setIP = cmd_proc_Popen("grep '^address' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null").strip().decode()
		setNM = cmd_proc_Popen("grep '^netmask' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null").strip().decode()
		setGW = cmd_proc_Popen("grep '^gateway' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null").strip().decode()

		if newIP and setIP and setIP != newIP and newIP != "127.0.0.1":
			cmd = "sudo sed -i -e 's/{}/{}/g' /etc/network/interfaces".format(setIP, newIP)
			print ("\tSystem newIP:{}".format(newIP))
			os.system(cmd)

			# 실시간 네트워크 환경 적용
			if curIP != newIP: # sudo ifconfig eth0 192.168.0.80 netmask 255.255.255.0 up
				cmd = "sudo ifconfig {} {}".format(iface, newIP)
				os.system(cmd)

		if newNM and setNM and setNM != newNM:
			cmd = "sudo sed -i -e 's/{}/{}/g' /etc/network/interfaces".format(setNM, newNM)
			print ("\tSystem newNM:{}".format(newNM))
			os.system(cmd)

			# 실시간 네트워크 환경 적용
			if curNM != newNM: # sudo ifconfig eth0 192.168.0.80 netmask 255.255.255.0 up
				cmd = "sudo ifconfig {} netmask {}".format(iface, newNM)
				os.system(cmd)

		if newGW and setGW and setGW != newGW:
			cmd = "sudo sed -i -e 's/{}/{}/g' /etc/network/interfaces".format(setGW, newGW)
			print ("\tSystem newGW:{}".format(newGW))
			os.system(cmd)
			
			# 실시간 네트워크 환경 적용
			if curGW != newGW:
				cmd = "sudo route add default gw {}".format(newGW)
				os.system(cmd)

		print ('IP:{} NM:{} GW:{}'.format(curIP, curNM, curGW))
		return 1
	else:
		print ('No Network Connected')
		return 0

# 실행하고 있는 오디오 데몬을 모두 종료 시킨다.
def kill_demon_mplayer(player): 
	cmd = "sudo killall -s 9 {}".format(player) # '{스페이스} itsAPI.pyc' 중요함
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	cmd = "sudo killall -s 9 {}".format("arecord oggenc sshpass mplayer") # Talk 기능이 살아있을 때를 감안해서 프로세서를 확인차 죽인다.
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_media_player"

# 실행하고 있는 카메라 데몬을 모두 종료 시킨다.
def kill_demon_streaming(): 
	cmd = "sudo kill -9 $(ps aux | grep ' streaming' | awk '{print $2}')" # '{스페이스} itsAPI.pyc, itsAPI.js 포함' 중요함
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_streaming"

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_itsAPI(): 
	cmd = "sudo kill -9 $(ps aux | grep ' itsAPI' | awk '{print $2}')" # '{스페이스} itsAPI.pyc, itsAPI.js 포함' 중요함
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_itsAPI"

def run_demon_streaming(): 
	cmd = "cd %s; python3 streaming.pyc 2>&1 & " % (share["path"]["api3"])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_streaming"
		
def run_demon_itsAPI(): 
	cmd = "cd %s; python3 itsAPI.pyc 2>&1 & " % (share["path"]["api3"])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_itsAPI"

def set_userPath_permission(path): 
	if os.path.isfile(path):
		pass
	else:
		# cmd = 'mkdir /var/www/html/its_web{} 2>&1 & '.format(path)
		cmd = 'mkdir {} 2>&1 & '.format(path)
		response = cmd_proc_Popen(cmd)
	cmd = "sudo chmod -R 777 {} 2>&1 & ".format(path)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_itsAPI"
		
def main():

	cfg["category"] = {} # 카탈로그 내 키값 이외의 요청은 거부
	cfg["category"]["gpio"] = { 'status':'', 'id':'', 'hold':'' }
	cfg["category"]["audio"] = { 'source':'', 'volume':'', 'loop':'' }
	cfg["category"]["talk"] = { 'command':'', 'remoteIP':'' }
	cfg["category"]["camera"] = { 'command':'', 'value':'' }
	cfg["category"]["system"] = { 'command':'', 'value':'' }
	cfg["category"]["trigger"] = { 'id':'' }
	cfg["category"]["maria"] = {}
	cfg["category"]["messenger"] = { 'sendMessage':'' }
	cfg["category"]["custom"] = { 'method':'', 'data':''}
	cfg["category"]["server"] = { 'host':'', 'port':'', 'url':'' }
	cfg["category"]["keyCode"] = ''
	cfg["category"]["global_var"] = None
	cfg["category"]["debug"] = True

	cfg["status"] = share["status"].copy()
	cfg["userPath"] = share["path"]["user"].copy()
	cfg["userPath"]["webPath"] = share["path"]["its_web"] # share["path"]["its_web"] path its_web

	cfg["userPath"]["fullAudio"] = cfg["userPath"]["webPath"]+cfg["userPath"]["audio"]+'/api'
	set_userPath_permission(cfg["userPath"]["fullAudio"]) ## API 내부 음원경로 권한
	print('Audio : {}'.format(cfg['userPath']['fullAudio']))

	if cfg["mDVR"]["enable"]:
		## streaming 정보 - Kill Daemon에 문제로 ITS가 죽음(독립적으로 실행 함)
		if cfg["camera"]["name"]:
			cfg["userPath"]["fullCamera"] = cfg["userPath"]["webPath"]+cfg["userPath"]["image"]+'/'+cfg["camera"]["name"]
			cfg["mDVR"]["dirRoot"] = cfg["userPath"]["fullCamera"]
			cfg["mDVR"]["dirCur"] = cfg["mDVR"]["dirRoot"] + '/dirCur' # 스넵샷 실시간 저장 폴더
			cfg["mDVR"]["dirTmp"] = cfg["mDVR"]["dirRoot"] + '/dirTmp' # 스넵샷의 임시폴더
			cfg["mDVR"]["dirOn"] = cfg["mDVR"]["dirRoot"] + '/dirOn' # 스넵샷의 임시폴더
			cfg["mDVR"]["imgLast"] = cfg["mDVR"]["dirRoot"] + '/last.png'
			set_userPath_permission(cfg["userPath"]["fullCamera"]) ## Stream File 경로 권한
			print('Camera : {}'.format(cfg['userPath']['fullCamera']))
			print(run_demon_streaming())
		else:
			print('No Selected Camera, Setup -> Camera > mDVR config')
	else:
		print('Disabled Local Stramming')

	cfg["portAPI"] = share["port"]["api"]

	ioB = cfg["ioBoard"]["set"]
	if ioB == 'acu': # 사전설정 GPIO 7,8 : sudo raspi-config -> 3 Interface Options -> P4 SPI -> Select No(Disable)
		mode = 'ACU API'
		cfg["ioMode"] = 'acu'
		cfg["setBD"] = share["ioBoard"]["acu"].copy()

	elif ioB == 'psw':
		mode = 'Power Switch'
		cfg["ioMode"] = 'psw'
		cfg["setBD"] = share["ioBoard"]["psw"].copy()

	else: # ITS
		mode = 'STD API'
		cfg["ioMode"] = 'std'
		cfg["setBD"] = share["ioBoard"]["std"].copy()

	## 시스템 네트워크 설정 IP, Netmask, Gateway
	if setSystemIP(cfg["tcpIpPort"]["staticAddress"], cfg["tcpIpPort"]["staticNetMask"], cfg["tcpIpPort"]["staticGateway"]): # 아이피정보를 재설정한다.
		iface = get_interface()
		if iface:
			cfg["tcpIpPort"]["staticAddress"] = get_ip_address(iface)
			cfg["tcpIpPort"]["staticNetMask"] = cmd_proc_Popen("ifconfig "+iface+" | grep 'inet' -m1 | awk -F' ' '{print $4}' 2>/dev/null").strip().decode()
			cfg["tcpIpPort"]["staticGateway"] = cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $2}' 2>/dev/null").strip().decode()
	else:
		cfg["tcpIpPort"]["staticAddress"] = "localhost"
	# 	cfg["tcpIpPort"]["staticAddress"] = "192.168.0.10"
	# 	cfg["tcpIpPort"]["staticNetMask"] = "255.255.255.0"
	# 	cfg["tcpIpPort"]["staticGateway"] = "192.168.0.1"
	
	print('Allow IP:\n\t{}\nDeny IP:\n\t{}'.format(cfg["permission"]["filterIP"]["allow"], cfg["permission"]["filterIP"]["deny"]))
	cmd_proc_Popen('cp {} {}'.format('{}/itsAPI.php'.format(share["path"]["api3"]), '{}/api.php'.format(cfg["userPath"]["webPath"])))
	saveConfig(cfg,'./itsAPI.json')

	# Start -  도움말 파일 관련
	if os.path.isfile('./example.html'):
		source_help = './example.html'
		target_help = '{}/api_example.html'.format(cfg["userPath"]["webPath"])

		#input file
		fin = open(source_help, "rt")
		#output file to write the result to
		fout = open(target_help, "wt")
		#for each line in the input file
		for line in fin:
			#read replace the string and write to output file
			fout.write(line.replace('my_IP', cfg["tcpIpPort"]["staticAddress"]))
			# print('my_ip_address', cfg["tcpIpPort"]["staticAddress"])
		#close input and output files
		fin.close()
		fout.close()

		cmd_proc_Popen('cp {} {}'.format('./readme.pdf', '{}/api_readme.pdf'.format(cfg["userPath"]["webPath"])))
		# cmd_proc_Popen('cp {} {}'.format('./QnA.pdf', '{}/api_qna.pdf'.format(cfg["userPath"]["webPath"])))
		# cmd_proc_Popen('cp {} {}'.format('./quickGuide.pdf', '{}/api_quickGuide.pdf'.format(cfg["userPath"]["webPath"])))
		# cmd_proc_Popen('cp {} {}'.format('./example.html', '{}/api_example.html'.format(cfg["userPath"]["webPath"])))

		# shutil.copyfile('./QnA.pdf', '{}/api_qna.pdf'.format(cfg["userPath"]["webPath"])) #copy src to dst
	# End - Start -  도움말 파일 관련

	# Start - 크론텝 관리 및 등록
	# 예외규정 예제: https://www.unix.com/unix-for-advanced-and-expert-users/199211-run-job-cron-specific-day-excluding-holidays.html
	f = open('cron_tab.txt', 'w')
	print('Alarm List:')
	for key in sorted(cfg["alarmCmds"]):
		if cfg["alarmCmds"][key]["cmd"] and cfg["alarmCmds"][key]["enable"]:
			alarm = json.loads(cfg["alarmCmds"][key]["cmd"])
			if alarm["host"]:
				cron_host = alarm["host"]
			else:
				cron_host = cfg["tcpIpPort"]["staticAddress"]
			if alarm["port"]:
				cron_port = int(alarm["port"])
			else:
				cron_port = cfg["portAPI"]

			cron_chars = " 0123456789*/" # 시간 변수에 허용되는 문자 그룹
			cron_valid = cfg["alarmCmds"][key]["time"]
			for c in cron_chars:
				cron_valid = cron_valid.replace(c, '')

			cron_count = len(cfg["alarmCmds"][key]["time"].strip().split(' '))
			if cron_count == 5 and cron_valid == '':
				# 시간과 명령문이 있으면 파일에 등록한다.
				f.write("{} echo '{}' | nc {} {} -q 0 > /dev/null 2>&1 \n".format(cfg["alarmCmds"][key]["time"].strip(), json.dumps(alarm["data"]), cron_host, cron_port))
				# print('\t{} {}'.format(cfg["alarmCmds"][key]["time"].strip(), json.dumps(alarm["data"])))[:80]+' ...' # 긴 문단을 잘라냄
				print('\t{} {}'.format(cfg["alarmCmds"][key]["time"].strip(), json.dumps(alarm["data"])[:80]+' ...')) # 긴 문단을 잘라냄
			else:
				print('\tError Alarm Command: {} {}').format(cfg["alarmCmds"][key]["time"].strip(), json.dumps(alarm["data"]))[:80]+' ...'
			# print(cfg["alarmCmds"][key]["time"], cron_count, cron_valid)
	f.close()
	# (crontab -r ; cat cron_tab.txt | crontab -
	cmd_proc_Popen('(crontab -r ; cat cron_tab.txt) | crontab -')
	# End - 크론텝 관리 및 등록

	print(run_demon_itsAPI())
	print(('Running %s:'%mode))		

if __name__ == '__main__':
	share = readConfig('/home/pi/common/config.json')
	wdog = readConfig('/home/pi/.config/watchdog.json') 
	cfg = readConfig('/home/pi/API3/config.json')

	# Log file path
	if not os.path.exists(share['path']['log']): # /var/www/html/its_web/data/log
		os.makedirs(share['path']['log'])
		os.chmod(share['path']['log'],0o777)
	if not os.path.exists(share['path']['log']+'/API3'): # /var/www/html/its_web/data/log/API3
		os.makedirs(share['path']['log']+'/API3')
		os.chmod(share['path']['log']+'/API3',0o777)
	cfg['loggerPath'] = share['path']['log']+'/API3/API3.log'
	cfg["watchdog"] = {}
	cfg["watchdog"] = wdog["fixed"].copy()


	print(kill_demon_mplayer(cfg["audio"]["player"]))
	print(kill_demon_itsAPI())

	cfg["userConfig"] = {} 

	# { 일반정보 2021-12-24 23:25:22

	# 라이센스 키
	cfg["userConfig"]["itsLicense"] = ""
	
	# 와치도그 서버 주소
	cfg["userConfig"]["wdServer"] = ""
	cfg["userConfig"]["myAddress"] = ""
	cfg["userConfig"]["myNetmask"] = ""
	cfg["userConfig"]["myGateway"] = ""
	cfg["userConfig"]["myLanguage"] = ""
	cfg["userConfig"]["ntpServer"] = ""
	cfg["userConfig"]["ipVirtual"] = ""

	# 오디오 소스
	cfg["userConfig"]["audioName"] = ""
	cfg["userConfig"]["audioTime"] = ""

	# I/O 보드 종류 (STD/ACU)
	cfg["userConfig"]["ioBoard"] = ""

	# 릴레이 경보
	cfg["userConfig"]["relayAddr"] = ""
	cfg["userConfig"]["relayPort"] = ""
	cfg["userConfig"]["relayNumber"] = ""

	# } 일반정보 2021-12-24 23:25:22

	main()