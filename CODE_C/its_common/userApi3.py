#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# 본 기능은 ITS에서 실행되는 프로그램의 환경값을 
# 외부 특히 IMS에서 원격의 ITS내 프로그램 설정값(1 ~ 5)을 재설정하는 역할을 한다.
# its_M_map_templet.html(setRunLevel) -> its_M_map.js(userCmd) -> bash(nc command) -> this_program(port: 32001) -> ITS DB Update -> Run Program
# 테스트 = echo '{"runLevel":{"name":"gpio","table":"g300t100","id":"1","run":"0"}}' | nc 192.168.0.80 32001 -q 0 &

import time
import json
import subprocess
import socket
import struct
import fcntl
import pymysql

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)

# def validate_url(s):
# 	# print(re.match(regex, "http://www.example.com") is not None) # True
# 	# print(re.match(regex, "example.com") is not None)            # False
# 	regex = re.compile(
# 		r'^(?:http|ftp)s?://' # http:// or https://
# 		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
# 		r'localhost|' #localhost...
# 		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
# 		r'(?::\d+)?' # optional port
# 		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
# 	if re.match(regex, s):
# 		return True
# 	return False

# def validate_ip(s):
# 	a = s.split('.')
# 	if len(a) != 4:
# 		return False
# 	for x in a:
# 		if not x.isdigit():
# 			return False
# 		i = int(x)
# 		if i < 0 or i > 255:
# 			return False
# 	return True

# def audioOut(source, remote, volume): # 
# 	# cmd = "cat /var/www/html/its_web/data/audio/A_museum.mp3 | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume 100 - &>/dev/null; fi' "
# 	if cfg.localSource: # 속도를 위해 오디오가 공용 파일이면 원격에 있는 자체 파일을 출력한다.
# 		cmd = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer &>/dev/null; then cat %s | mplayer -cache 1024 -volume %s - &>/dev/null; fi' &" % (remote, source, volume)
# 	else:
# 		cmd = "cat %s | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume %s - &>/dev/null; fi' &" % (source, remote, volume)
# 	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
# 	# print(cmd)

def send_data_socket(host, port, data, isJson=True): # 요청된 명령문 전송
	try: 
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((host, int(port))) 
		if isJson:
			client_socket.send(json.dumps({"data":data}).encode('utf-8')) 
		else:
			client_socket.send(data) 
		# print(client_socket.recv(1024)) ## 응답이 올때까지 기다린다. (수신서버에서 응답코드가 없으면 socket.error 발생 또는 무한대기함)
		client_socket.close() 
		return 1
	except: # 수신측에서 준비가 않되어 있으면 오류
		return 0

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

# 자신 아이피 확인 
# 자신 아이피 확인 
def get_ip_address(iface): # get_ip_address("eth0")
	return cmd_proc_Popen("ifconfig "+iface+" | grep 'inet ' | cut -d: -f2 | awk '{print $2}'").strip().decode()

# def insert_table_ITS(table, field, data): 
# 	query = "INSERT INTO "+table+" (w_ax_cnt,w_xa_cnt) VALUES(%s,%s)"
# 	args = (data[0],data[1])
# 	try:
# 		conn = pymysql.connect(host=cfg['mysql']['host'], user=cfg['mysql']['user'], passwd=cfg['mysql']['pass'], db=cfg['mysql']['name'], charset='utf8', use_unicode=True) 
# 		cursor = conn.cursor()
# 		cursor.execute(query, args)
# 		conn.commit()
# 		conn.close()
# 		return cursor.lastrowid
# 	except pymysql.Error as error:
# 		return 0
# 	finally:
# 		if cursor:
# 			cursor.close()
# 		if conn:
# 			conn.close()

def get_table_value(table, id, field): # 시스템 설정 값 반환 cf_title
	query = "SELECT {} FROM {} WHERE wr_id = '{}'".format(field, table, id)
	# print(query)
	try:
		conn = pymysql.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
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

def update_table_ITS(table, id, field, value): # 예(gpio): gpio, 1, w_event_holdTime, 2
	query = "UPDATE {} SET {} = '{}' WHERE wr_id = '{}';".format(table, field, value, id)
	# print(query)
	try:
		conn = pymysql.connect(host=cfg['mysql']['host'], user=cfg['mysql']['user'], passwd=cfg['mysql']['pass'], db=cfg['mysql']['name'], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		# return cursor.fetchone() # 커서의 fetchall()는 모두, fetchone()은 하나의 Row, fetchone(n)은 n개 만큼
		return cursor.rowcount
	except pymysql.Error as error:
		print("Failed to update table record: {}".format(error))
		return 0
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()


def main():
	# 예약된 포트를 사용하는 존비 프로세서를 제거 한다.
	# cmd_proc_Popen('sudo fuser -k -n tcp {}'.format(port))
	cmd_proc_Popen('sudo kill -9 $(lsof -t -i:{}) 2>/dev/null'.format(port))
	time.sleep(1) # Second

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
	s.bind((host, port)) # <------- 소켓을 주소로 바인딩
	s.listen(1) # <------ listening 시작. 최대 클라이언트 연결 수 5개
	buffer = 1024  # Normally 1024, but we want fast response
	while True:
		sock, addr = s.accept()
		while True: # <-------- 클라이언트 연결이 오면 루프로 들어가서 데이터가 수신을 기다림
			data = sock.recv (buffer)
			if not data:
				break
			else:
				if len(data) < buffer:
					pass
				else:
					while True: 
						part = sock.recv (buffer)
						data += part
						if len(part) < buffer:
							break

			try:
				arrJson = json.loads(data)
			except:
				break

			# print(send_data_socket(addr[0], port, data, isJson=True))
			# print('Connected from:{}'.format(addr), arrJson)
			if 'runLevel' in arrJson:
				if 'name' in arrJson['runLevel']:
					prog_name = arrJson['runLevel']['name']
				else:
					break

				if 'table' in arrJson['runLevel']:
					prog_tbl = arrJson['runLevel']['table']
				else:
					break

				if 'id' in arrJson['runLevel']:
					prog_id = arrJson['runLevel']['id']
				else:
					break

				if 'run' in arrJson['runLevel']:
					prog_level = arrJson['runLevel']['run']
				else:
					break

				if prog_name in cfg['path']: # Key, Value 점검
					prog_path = cfg['path'][prog_name] # 실행 명령어 경로
				else:
					break
				
				if prog_name in cfg['runTable']: # Key, Value 점검
					prog_cmds = cfg['runTable'][prog_name]['command'] # 실행 명령어 이름
				else:
					break

				prog_exec = 'cd {0}; python {0}/{1} 2>&1 &'.format(prog_path, prog_cmds)

				# Database 설정
				# 사전에 설정된 환경값(Level 1/2/3)으로 데이터베이스 값 변경한다.
				# arrJson['runLevel']['sensor_serial'] 값 분석(Parse)에 따른 테이블내 레코드 수정
				# 테스트 = echo '{"runLevel":{"name":"gpio","table":"g300t100","id":"1","run":"0"}}' | nc 192.168.0.80 32001 -q 0 &
				# 예: gpio
					# wr_6  w_event_pickTime:1-60
					# wr_7  w_event_holdTime:0-10
					# $write['wr_6'] = "w_1_pickTime,1,1,1,1,1";
					# $write['wr_7'] = "w_1_holdTime,0,0,0,0,0";

				# Program 재실행
				# 확인된 프로그램을 모두 제거하고 1초간 대기후
				# 관련프로그램을 재실행 한다.
				if prog_name == 'gpio':
					# 레빌값 읽기 - get_table_value: pickTime, holdTime)
					# 변수값 추출 - pickTime[int(prog_level)], holdTime[int(prog_level)]
					# 변수값 저장 - update_table_ITS: w_event_pickTime, w_event_holdTime
					# 레벨값 저장 - update_table_ITS: wr_6 pickTime[0], wr_7 holdTime[0]
					# 프로그램 중지 - prog_kill
					# 프로그램 재실행 - prog_exec
					g5_table = cfg['table'][prog_name]
					pickTime = get_table_value(g5_table, prog_id, 'wr_6')['wr_6'].split(',')
					holdTime = get_table_value(g5_table, prog_id, 'wr_7')['wr_7'].split(',')
					
					if pickTime and holdTime: # 2021-12-28 02:06:45
						if int(prog_level) < 1 or int(prog_level) >= len(pickTime): # 런레벨값을 1 ~ 5 까지로 제한
							print("Out of Run Level: {}".format(prog_level)) # 요청된 실행 등급이 목록테이블과 불일치 - 2021-12-28 00:28:43
							break

						w_event_pickTime = pickTime[int(prog_level)]
						if w_event_pickTime: # 실행 등급 적용
							update_table_ITS(g5_table, prog_id, 'w_event_pickTime', w_event_pickTime)
							# print(g5_table, prog_id, 'w_event_pickTime', w_event_pickTime)
							pickTime[0] = "w_{}_pickTime".format(prog_level)
							update_table_ITS(g5_table, prog_id, 'wr_6', ','.join(pickTime))
							# print(g5_table, prog_id, 'wr_6', ','.join(pickTime))

						w_event_holdTime = holdTime[int(prog_level)]
						if w_event_holdTime: # 실행 등급 적용
							update_table_ITS(g5_table, prog_id, 'w_event_holdTime', w_event_holdTime)
							# print(g5_table, prog_id, 'w_event_holdTime', w_event_holdTime)
							holdTime[0] = "w_{}_holdTime".format(prog_level)
							update_table_ITS(g5_table, prog_id, 'wr_7', ','.join(holdTime))
							# print(g5_table, prog_id, 'wr_7', ','.join(holdTime))

						# 실행되고 있는 GPIO 데몬을 재거 한후 신규 실행등급을 적용을 위한 프로그램 재실행
						# prog_kill = 'sudo pkill -9 -ef GPIO 2>&1' ## 주의) 직전에 실행된 프로세서를 죽이는 오류 발생 가능
						prog_kill = "sudo kill -9 $(ps aux | grep 'GPIO' | awk '{print $2}')" # '{스페이스} itsAPI.pyc, itsAPI.js 포함' 중요함
						subprocess.Popen(prog_kill, shell=True, stderr=subprocess.PIPE)
						time.sleep(1) # Second
						# print(prog_kill)
						subprocess.Popen(prog_exec, shell=True, stderr=subprocess.PIPE)
						# print(prog_exec)
					else:
						print("Not Found Run Level Values") # 요청된 실행 등급이 목록테이블과 불일치 - 2021-12-28 01:31:11

				elif prog_name == '':
					pass
				else:
					pass

			## 작업 완료
			print('Connected from:{}'.format(addr), prog_name, prog_tbl, prog_id, prog_level, prog_path, prog_cmds, prog_exec)
			break # 작업후 While 종료

			# sock.send(data) # <------ 데이터가 있으면 ctime()값과 data를 송신
		sock.close() # <------ 클라이언트 세션 종료
	s.close() # <------- 위 루프가 끝나지 않으므로 이 라인은 실행되지 않는다. just a remainder of close() 
	
if __name__ == '__main__':
	cfg = readConfig('/home/pi/common/config.json')

	myIface = cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null").strip().decode()

	host = get_ip_address(myIface).strip() # '192.168.0.80'
	port = cfg['port']['userApi'] # 32001

	print('userApi {} {}'.format(host, port))

	main()
