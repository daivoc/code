#!/usr/bin/env python
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
	return str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()

# ## 자신의 아이피 확인
# def get_ip_address():
# 	ifname = get_interface()
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	return socket.inet_ntoa(fcntl.ioctl(
# 		s.fileno(),
# 		0x8915,  # SIOCGIFADDR
# 		struct.pack('256s', ifname[:15])
# 	)[20:24])

# 자신 아이피 확인 
def get_ip_address(): # get_ip_address("eth0")
	ifname = get_interface()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915, # SIOCGIFADDR
			struct.pack("256s", ifname[:15])
		)[20:24])
	except:
		return 'localhost'

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
	curIP = get_ip_address()
	if iface and curIP:
		curNM = str(cmd_proc_Popen("ifconfig "+iface+" | grep 'inet' -m1 | awk -F' ' '{print $4}' 2>/dev/null")).strip()
		curGW = str(cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $2}' 2>/dev/null")).strip()
		
		setIP = str(cmd_proc_Popen("grep '^address' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null")).strip()
		setNM = str(cmd_proc_Popen("grep '^netmask' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null")).strip()
		setGW = str(cmd_proc_Popen("grep '^gateway' /etc/network/interfaces -m1 | cut -d' ' -f2 2>/dev/null")).strip()

		if newIP and setIP and setIP != newIP:
			cmd = "sudo sed -i -e 's/%s/%s/g' /etc/network/interfaces" % (setIP, newIP)
			print ("\tSystem newIP:{}".format(newIP))
			os.system(cmd)

			# 실시간 네트워크 환경 적용
			if curIP != newIP: # sudo ifconfig eth0 192.168.0.80 netmask 255.255.255.0 up
				cmd = "sudo ifconfig %s %s" % (iface, newIP)
				os.system(cmd)

		if newNM and setNM and setNM != newNM:
			cmd = "sudo sed -i -e 's/%s/%s/g' /etc/network/interfaces" % (setNM, newNM)
			print ("\tSystem newNM:{}".format(newNM))
			os.system(cmd)

			# 실시간 네트워크 환경 적용
			if curNM != newNM: # sudo ifconfig eth0 192.168.0.80 netmask 255.255.255.0 up
				cmd = "sudo ifconfig %s netmask %s" % (iface, newNM)
				os.system(cmd)

		if newGW and setGW and setGW != newGW:
			cmd = "sudo sed -i -e 's/%s/%s/g' /etc/network/interfaces" % (setGW, newGW)
			print ("\tSystem newGW:{}".format(newGW))
			os.system(cmd)
			
			# 실시간 네트워크 환경 적용
			if curGW != newGW:
				cmd = "sudo route add default gw %s" % (newGW)
				os.system(cmd)

		return ('IP:{} NM:{} GW:{}'.format(curIP, curNM, curGW))
	else:
		return ('No Network Connected')

# 실행하고 있는 오디오 데몬을 모두 종료 시킨다.
def kill_demon_mplayer(player): 
	cmd = "sudo killall -s 9 {}".format(player) # '{스페이스} itsAPI.pyc' 중요함
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
	cmd = "cd %s; python streaming.pyc 2>&1 & " % (share['path']['api'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_streaming"
		
def run_demon_itsAPI(): 
	cmd = "cd %s; python itsAPI.pyc 2>&1 & " % (share['path']['api'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_itsAPI"

def set_userPath_permission(path): 
	if os.path.isfile(path):
		pass
	else:
		cmd = 'mkdir /var/www/html/its_web{} 2>&1 & '.format(path)
		response = str(cmd_proc_Popen(cmd)).strip()
	cmd = "sudo chmod -R 777 /var/www/html/its_web{} 2>&1 & ".format(path)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_itsAPI"
		
def main():
	iface = get_interface()
	cfg['tcpIpPort']['staticAddress'] = get_ip_address()
	cfg['tcpIpPort']['staticNetMask'] = str(cmd_proc_Popen("ifconfig "+iface+" | grep 'inet' -m1 | awk -F' ' '{print $4}' 2>/dev/null")).strip()
	cfg['tcpIpPort']['staticGateway'] = str(cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $2}' 2>/dev/null")).strip()

	cfg['category'] = {} # 카탈로그 내 키값 이외의 요청은 거부
	cfg['category']['gpio'] = { 'status':'', 'id':'', 'hold':'' }
	cfg['category']['audio'] = { 'source':'', 'volume':'', 'loop':'' }
	cfg['category']['camera'] = { 'command':'', 'value':'' }
	cfg['category']['system'] = { 'command':'', 'value':'' }
	cfg['category']['maria'] = {}
	cfg['category']['custom'] = { 'method':'', 'data':''} #, 'type':'', 'interval':''} # 'method':'tcp_socket/http_get/http_post', 'type':'query/json/xml', 'data':'data', 'interval':'sec'
	cfg['category']['server'] = { 'host':'', 'port':'', 'url':'' }
	cfg['category']['keyCode'] = ''
	cfg['category']['global_var'] = None
	cfg['category']['debug'] = True

	cfg['status'] = share['status'].copy()
	cfg['userPath'] = share['path']['user'].copy()
	cfg['userPath']['webPath'] = '/var/www/html/its_web'
	cfg['userPath']['fullAudio'] = cfg['userPath']['webPath']+cfg['userPath']['audio']+'/api'
	cfg['userPath']['fullCamera'] = cfg['userPath']['webPath']+cfg['userPath']['image']+'/camera'

	set_userPath_permission(cfg['userPath']['audio']+'/api') ## API 내부 음원경로 권한
	set_userPath_permission(cfg['userPath']['image']+'/camera') ## Stream File 경로 권한
	set_userPath_permission('/theme/ecos-its_optex/utility/ubergallery/resources/cache') ## ubergallery 경로 권한 http://192.168.0.80/theme/ecos-its_optex/utility/ubergallery/

	cfg['portAPI'] = share['port']['api']

	ioB = cfg['ioBoard']['set']
	if ioB == 'acu': # 사전설정 GPIO 7,8 : sudo raspi-config -> 3 Interface Options -> P4 SPI -> Select No(Disable)
		mode = 'ACU API'
		cfg['ioMode'] = 'acu'
		cfg['setBD'] = share['ioBoard']['acu'].copy()

	elif ioB == 'psw':
		mode = 'Power Switch'
		cfg['ioMode'] = 'psw'
		cfg['setBD'] = share['ioBoard']['psw'].copy()

	else: # ITS
		mode = 'STD API'
		cfg['ioMode'] = 'std'
		cfg['setBD'] = share['ioBoard']['std'].copy()

	## 시스템 네트워크 설정 IP, Netmask, Gateway
	print(setSystemIP(cfg['tcpIpPort']['staticAddress'], cfg['tcpIpPort']['staticNetMask'], cfg['tcpIpPort']['staticGateway']))
	print('Allow IP:\n\t{}\nDeny IP:\n\t{}'.format(cfg['permission']['filterIP']['allow'], cfg['permission']['filterIP']['deny']))

	cmd_proc_Popen('cp {} {}'.format('{}/itsAPI.php'.format(share['path']['api']), '{}/api.php'.format(share['path']['its_web'])))

	if cfg['mDVR']['enable']:
		## streaming 정보 - Kill Daemon에 문제로 ITS가 죽음(독립적으로 실행 함)
		print(run_demon_streaming())
	else:
		print('Disabled Local Stramming')

	cfg['mDVR']['dirRoot'] = cfg['userPath']['fullCamera']
	cfg['mDVR']['dirCur'] = cfg['mDVR']['dirRoot'] + '/dirCur'
	cfg['mDVR']['dirTmp'] = cfg['mDVR']['dirRoot'] + '/dirTmp'
	cfg['mDVR']['imgLast'] = cfg['mDVR']['dirRoot'] + '/last.png'

	saveConfig(cfg,'./itsAPI.json')

	# Start -  도움말 파일 관련
	if os.path.isfile('./example.html'):
		source_help = './example.html'
		target_help = '{}/api_example.html'.format(cfg['userPath']['webPath'])

		#input file
		fin = open(source_help, "rt")
		#output file to write the result to
		fout = open(target_help, "wt")
		#for each line in the input file
		for line in fin:
			#read replace the string and write to output file
			fout.write(line.replace('my_IP', cfg['tcpIpPort']['staticAddress']))
			# print('my_ip_address', cfg['tcpIpPort']['staticAddress'])
		#close input and output files
		fin.close()
		fout.close()

		cmd_proc_Popen('cp {} {}'.format('./QnA.pdf', '{}/api_qna.pdf'.format(cfg['userPath']['webPath'])))
		cmd_proc_Popen('cp {} {}'.format('./quickGuide.pdf', '{}/api_quickGuide.pdf'.format(cfg['userPath']['webPath'])))
		# cmd_proc_Popen('cp {} {}'.format('./example.html', '{}/api_example.html'.format(cfg['userPath']['webPath'])))

		# shutil.copyfile('./QnA.pdf', '{}/api_qna.pdf'.format(cfg['userPath']['webPath'])) #copy src to dst
	# End - Start -  도움말 파일 관련

	# Start - 크론텝 관리 및 등록
	# 예외규정 예제: https://www.unix.com/unix-for-advanced-and-expert-users/199211-run-job-cron-specific-day-excluding-holidays.html
	f = open('cron_tab.txt', 'w')
	print('Alarm List:')
	for key in sorted(cfg['alarmCmds']):
		if cfg['alarmCmds'][key]['cmd'] and cfg['alarmCmds'][key]['enable']:
			alarm = json.loads(cfg['alarmCmds'][key]['cmd'])
			if alarm['host']:
				cron_host = alarm['host']
			else:
				cron_host = cfg['tcpIpPort']['staticAddress']
			if alarm['port']:
				cron_port = int(alarm['port'])
			else:
				cron_port = cfg['portAPI']

			cron_chars = " 0123456789*/" # 시간 변수에 허용되는 문자 그룹
			cron_valid = cfg['alarmCmds'][key]['time']
			for c in cron_chars:
				cron_valid = cron_valid.replace(c, '')

			cron_count = len(cfg['alarmCmds'][key]['time'].strip().split(' '))
			if cron_count == 5 and cron_valid == '':
				# 시간과 명령문이 있으면 파일에 등록한다.
				f.write("{} echo '{}' | nc {} {} -q 0 > /dev/null 2>&1 \n".format(cfg['alarmCmds'][key]['time'].strip(), json.dumps(alarm['data']), cron_host, cron_port))
				print('\t{} {}'.format(cfg['alarmCmds'][key]['time'].strip(), json.dumps(alarm['data'])))[:80]+' ...' # 긴 문단을 잘라냄
			else:
				print('\tError Alarm Command: {} {}').format(cfg['alarmCmds'][key]['time'].strip(), json.dumps(alarm['data']))[:80]+' ...'
			# print(cfg['alarmCmds'][key]['time'], cron_count, cron_valid)
	f.close()
	# (crontab -r ; cat cron_tab.txt | crontab -
	cmd_proc_Popen('(crontab -r ; cat cron_tab.txt) | crontab -')
	# End - 크론텝 관리 및 등록

	print(run_demon_itsAPI())
	print(('Running %s:'%mode))		

if __name__ == '__main__':
	share = readConfig('/home/pi/common/config.json')
	cfg = readConfig('/home/pi/API/config.json') 
	print(kill_demon_mplayer(cfg['audio']['player']))
	print(kill_demon_itsAPI())

	cfg["userConfig"] = {} 

	# { 일반정보 2021-12-24 23:25:22

	# 라이센스 키
	cfg["userConfig"]["itsLicense"] = str(itsMemberConfig('mb_1','manager')["mb_1"]).strip()
	
	# 와치도그 서버 주소
	cfg["userConfig"]["wdServer"] = str(itsMemberConfig('mb_3','manager')["mb_3"]).strip()
	cfg["userConfig"]["myAddress"] = str(itsMemberConfig('mb_4','manager')["mb_4"]).strip()
	cfg["userConfig"]["myNetmask"] = str(itsMemberConfig('mb_5','manager')["mb_5"]).strip()
	cfg["userConfig"]["myGateway"] = str(itsMemberConfig('mb_6','manager')["mb_6"]).strip()
	cfg["userConfig"]["myLanguage"] = str(itsMemberConfig('mb_7','manager')["mb_7"]).strip()
	cfg["userConfig"]["ntpServer"] = str(itsMemberConfig('mb_8','manager')["mb_8"]).strip()
	cfg["userConfig"]["ipVirtual"] = str(itsMemberConfig('mb_9','manager')["mb_9"]).strip()

	# 오디오 소스
	cfg["userConfig"]["audioName"] = str(itsMemberConfig('mb_2','its')["mb_2"]).strip()
	cfg["userConfig"]["audioTime"] = str(itsMemberConfig('mb_3','its')["mb_3"]).strip()

	# I/O 보드 종류 (STD/ACU)
	cfg["userConfig"]["ioBoard"] = str(itsMemberConfig('mb_4','its')["mb_4"]).strip()

	# 릴레이 경보
	cfg["userConfig"]["relayAddr"] = str(itsMemberConfig('mb_5','its')["mb_5"]).strip()
	cfg["userConfig"]["relayPort"] = str(itsMemberConfig('mb_6','its')["mb_6"]).strip()
	cfg["userConfig"]["relayNumber"] = str(itsMemberConfig('mb_7','its')["mb_7"]).strip()

	# } 일반정보 2021-12-24 23:25:22

	main()