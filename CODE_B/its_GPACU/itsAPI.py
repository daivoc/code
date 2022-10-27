#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import re
import sys
import json
import subprocess
import requests
import socket
import struct
import fcntl
import RPi.GPIO as GPIO
import threading

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)

def validate_url(s):
	# print(re.match(regex, "http://www.example.com") is not None) # True
	# print(re.match(regex, "example.com") is not None)            # False
	regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if re.match(regex, s):
		return True
	return False

def validate_ip(s):
	a = s.split('.')
	if len(a) != 4:
		return False
	for x in a:
		if not x.isdigit():
			return False
		i = int(x)
		if i < 0 or i > 255:
			return False
	return True

def findITS(host):
	ipGroup = []
	classIP = '.'.join(host.split(".")[0:3]) # 192.168.0
	port = share["port"]["gpwio"]["portIn"] # 8040
	# print classIP, port
	for ips in range(2,255):  
		ip = '%s.%s'%(classIP,ips)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.01)
		result = sock.connect_ex((ip, port))
		sock.close()
		if result == 0:
			ipGroup.append(ip)
	return ipGroup # if success return 0


def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

def get_ip_address():
	ifname = str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def timerTurnOff(id):
	if id in common["gpioPw"]:
		GPIO.output(common["gpioPw"][id], GPIO.LOW)
	if id in common["gpioOut"]:
		GPIO.output(common["gpioOut"][id], GPIO.LOW)

def gpioAction(status, id, hold, msg):
	response = {}
	if status == "0" and id in common["gpioOut"]:
		GPIO.output(common["gpioOut"][id], GPIO.LOW)
		response[id] = GPIO.input(common["gpioOut"][id])
		return response
	elif status == "1" and id in common["gpioOut"]:
		GPIO.output(common["gpioOut"][id], GPIO.HIGH)
		response[id] = GPIO.input(common["gpioOut"][id])
		# hold 값이 있으면 시간 이후 timerTurnOff()
		try: # 문자를 숫자화 할떄 모류 제거
			if float(hold):
				hold = abs(float(hold))
				# https://stackoverflow.com/questions/16578652/threading-timer
				t = threading.Timer(hold, timerTurnOff, [id])
				t.start() # after hold seconds, run timerTurnOff
		except ValueError:
			pass
		return response
	elif status == "0" and id in common["gpioPw"]:
		GPIO.output(common["gpioPw"][id], GPIO.LOW)
		response[id] = GPIO.input(common["gpioPw"][id])
		return response
	elif status == "1" and id in common["gpioPw"]:
		GPIO.output(common["gpioPw"][id], GPIO.HIGH)
		response[id] = GPIO.input(common["gpioPw"][id])
		# hold 값이 있으면 시간 이후 timerTurnOff()
		try: # 문자를 숫자화 할떄 모류 제거
			if float(hold):
				hold = abs(float(hold))
				# https://stackoverflow.com/questions/16578652/threading-timer
				t = threading.Timer(hold, timerTurnOff, [id])
				t.start() # after hold seconds, run timerTurnOff
		except ValueError:
			pass
		return response
	elif status == "3":
		if id in common["gpioIn"]:
			response[id] = GPIO.input(common["gpioIn"][id])
		elif id in common["gpioOut"]:
			response[id] = GPIO.input(common["gpioOut"][id])
		elif id in common["gpioPw"]:
			response[id] = GPIO.input(common["gpioPw"][id])
		return response
	elif status == "6": # Power
		for key, value in common["gpioPw"].iteritems():
			response[key] = GPIO.input(value)
		return response
	elif status == "7": # Relay
		for key, value in common["gpioOut"].iteritems():
			response[key] = GPIO.input(value)
		return response
	elif status == "8": # Sensor
		for key, value in common["gpioIn"].iteritems():
			response[key] = GPIO.input(value)
		return response
	elif status == "9": # All
		for key, value in common["gpioIn"].iteritems():
			response[key] = GPIO.input(value)
		for key, value in common["gpioOut"].iteritems():
			response[key] = GPIO.input(value)
		for key, value in common["gpioPw"].iteritems():
			response[key] = GPIO.input(value)
		return response
	else:
		return
	'''
echo '[{ "gpio": { "status": "9", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "8", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "7", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "6", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "3", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "0", "id": "", "hold": "", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0

echo '[{ "gpio": { "status": "0", "id": "R15", "hold": "0", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R15", "hold": "2", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0

echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""}, "debug":1 }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""}, "debug":1 }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""}, "debug":1 }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""}, "debug":1 }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""}, "debug":1 }]' | nc 192.168.0.60 54001 -q 0
echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "2", "msg": ""}, "debug":1 }]' | nc 192.168.0.60 54001 -q 0

echo '[{ "audio": { "source": "1", "target": "192.168.0.60", "volume": "100", "command": "0", "loop": "3" }, "debug":true }]' | nc 192.168.0.60 54001 -q 0 &
echo '[{ "audio": { "source": "1", "target": "192.168.0.101", "volume": "80", "command": "0", "loop": "1" }, "debug":true }]' | nc 192.168.0.60 54001 -q 0 &
echo '[{ "audio": { "source": "1", "target": "192.168.0.101", "volume": "80", "command": "0", "loop": "3" }, "debug":true }]' | nc 192.168.0.60 54001 -q 0 &
echo '[{ "gpio": { "status": "1", "id": "R09", "hold": "3", "msg": ""},  "gpio": { "status": "1", "id": "R10", "hold": "4", "msg": ""}, "debug":true }]' | nc 192.168.0.60 54001 -q 0 &

echo '[{ "audio": { "source": "1", "target": "192.168.0.101", "volume": "80", "command": "0", "loop": "3" }, "debug":true },{ "gpio": { "status": "1", "id": "R01", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R02", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R03", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R04", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R05", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R06", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R07", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R08", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R09", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R10", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R11", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R12", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R13", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R14", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R15", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R16", "hold": "3", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0

echo '[{ "gpio": { "status": "1", "id": "R01", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R02", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R03", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R04", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R05", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R06", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R07", "hold": "3", "msg": ""} },{ "gpio": { "status": "1", "id": "R08", "hold": "3", "msg": ""} }]' | nc 192.168.0.60 54001 -q 0

echo '[
{ "gpio": { "status": "1", "id": "R01", "hold": "0.01", "msg": ""} },
{ "gpio": { "status": "1", "id": "R02", "hold": "0.02", "msg": ""} },
{ "gpio": { "status": "1", "id": "R03", "hold": "0.03", "msg": ""} },
{ "gpio": { "status": "1", "id": "R04", "hold": "0.04", "msg": ""} },
{ "gpio": { "status": "1", "id": "R05", "hold": "0.05", "msg": ""} },
{ "gpio": { "status": "1", "id": "R06", "hold": "0.06", "msg": ""} },
{ "gpio": { "status": "1", "id": "R07", "hold": "0.07", "msg": ""} },
{ "gpio": { "status": "1", "id": "R08", "hold": "0.08", "msg": ""} },
{ "gpio": { "status": "1", "id": "R09", "hold": "0.09", "msg": ""} },
{ "gpio": { "status": "1", "id": "R10", "hold": "0.10", "msg": ""} },
{ "gpio": { "status": "1", "id": "R11", "hold": "0.11", "msg": ""} },
{ "gpio": { "status": "1", "id": "R12", "hold": "0.12", "msg": ""} },
{ "gpio": { "status": "1", "id": "R13", "hold": "0.13", "msg": ""} },
{ "gpio": { "status": "1", "id": "R14", "hold": "0.14", "msg": ""} },
{ "gpio": { "status": "1", "id": "R15", "hold": "0.15", "msg": ""} },
{ "gpio": { "status": "1", "id": "R16", "hold": "0.16", "msg": ""} }
]' | nc 192.168.0.60 54001 -q 0

echo '[
{ "gpio": { "status": "1", "id": "R01", "hold": "3.01", "msg": ""} },
{ "gpio": { "status": "1", "id": "R02", "hold": "3.02", "msg": ""} },
{ "gpio": { "status": "1", "id": "R03", "hold": "3.03", "msg": ""} },
{ "gpio": { "status": "1", "id": "R04", "hold": "3.04", "msg": ""} },
{ "gpio": { "status": "1", "id": "R05", "hold": "3.05", "msg": ""} },
{ "gpio": { "status": "1", "id": "R06", "hold": "3.06", "msg": ""} },
{ "gpio": { "status": "1", "id": "R07", "hold": "3.07", "msg": ""} },
{ "gpio": { "status": "1", "id": "R08", "hold": "3.08", "msg": ""} },
{ "gpio": { "status": "1", "id": "R09", "hold": "3.09", "msg": ""} },
{ "gpio": { "status": "1", "id": "R10", "hold": "3.10", "msg": ""} },
{ "gpio": { "status": "1", "id": "R11", "hold": "3.11", "msg": ""} },
{ "gpio": { "status": "1", "id": "R12", "hold": "3.12", "msg": ""} },
{ "gpio": { "status": "1", "id": "R13", "hold": "3.13", "msg": ""} },
{ "gpio": { "status": "1", "id": "R14", "hold": "3.14", "msg": ""} },
{ "gpio": { "status": "1", "id": "R15", "hold": "3.15", "msg": ""} },
{ "gpio": { "status": "1", "id": "R16", "hold": "3.16", "msg": ""} }
]' | nc 192.168.0.60 54001 -q 0
	'''


def audioAction(source, target, volume, command, loop):
	localS = 0 # 예약된 음원
	audio = ""
	errorMsg = ""
	if source.isdigit(): # 목록에 있는 음원을 사용한다.
		if len(sourceList) < int(source): # 리스트 목록에 없는 번호
			errorMsg = "Out of list"
		else:
			audio = audioFolder + sourceList[int(source)-1]
			localS = 1
	else:
		if os.path.isfile(source):
			audio = source
		elif validate_url(source):
			url = source
			name = "/tmp/audioSource" 
			try:
				# print (url, name)
				# 해당 URL에 송신 및 response 성공 시 파일 저장 
				r = requests.get(url, allow_redirects=True)
				open(name, 'wb').write(r.content)
			# 잘못된 URL 입력 시 예외 처리
			except Exception as e:
				errorMsg = "Audio Download error"
			else:
				audio = name
		else:
			errorMsg = "Unknown audio path or url"
	
	if target == "localhost":
		target = host
	else:
		if validate_ip(target):
			pass
		else:
			errorMsg = "Target IP format error"

	if volume.isdigit():
		volume = abs(int(volume))
		if volume > 0 and volume <= 100:
			pass
		else: # 기본 소리 크기값 사용
			volume = share["mPlayer"]["mplayer"]["volume"]
	else:
		errorMsg = "Volume value error"

	if command.isdigit():
		command = abs(int(command))
		if command == 1:
			errorMsg = json.dumps(os.listdir(audioFolder))
			pass
	else:
		errorMsg = "Command value error"

	if loop.isdigit():
		loop = abs(int(loop))
		if loop > 0:
			pass
		else:
			loop = 1
	else:
		errorMsg = "Loop value error"

	# print (audio, target, volume, command, loop)
	if errorMsg:
		return errorMsg
	else:
		# 오디오 원격 전송시 Loop 기능은 적용이 않된다.
		# Loop 기능은 Local Audio Play 시에만 적용 된다.
		# chkProc = sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "pidof mplayer"
		if target == host: # 원격 아이피가 자기 자신이면 직접 실행
			# cmd ="if ! pidof mplayer /dev/null 2>&1; then mplayer -cache 1024 -volume %s -loop %s %s &>/dev/null; fi &" % (volume, loop, audio)
			cmd ="if ! pidof mplayer /dev/null 2>&1; then mplayer -cache 1024 -volume %s -loop %s %s >/dev/null 2>&1; fi &" % (volume, loop, audio)
		elif localS: # 속도를 위해 오디오가 공용 파일이면 원격에 있는 자체 파일을 출력한다.
			# cmd = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer /dev/null 2>&1; then cat %s | mplayer -cache 1024 -volume %s - &>/dev/null; else echo 'busy'; fi' &" % (target, audio, volume)
			# cmd = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer /dev/null 2>&1; then cat %s | mplayer -cache 1024 -volume %s -loop %s - &>/dev/null; fi' &" % (target, audio, volume, loop)
			# cmd = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer /dev/null 2>&1; then mplayer -cache 1024 -volume %s -loop %s %s &>/dev/null; fi' &" % (target, volume, loop, audio)
			cmd = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer /dev/null 2>&1; then mplayer -cache 1024 -volume %s -loop %s %s >/dev/null 2>&1; fi' &" % (target, volume, loop, audio)
		else: # 오디오 전송 기능에서는 Loop적용이 않된다.
			# cmd = "cat %s | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer /dev/null 2>&1; then cat - | mplayer -cache 1024 -volume %s - &>/dev/null; else echo 'busy'; fi' &" % (audio, target, volume)
			cmd = "cat %s | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer /dev/null 2>&1; then cat - | mplayer -cache 1024 -volume %s - &>/dev/null; fi' &" % (audio, target, volume) # 오디오 원격 전송시 Loop 기능은 적용이 않된다.

		## https://soooprmx.com/archives/5932 Popen vs call
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		# p = subprocess.call(cmd, shell=True)
		# result = "Sent audio %s"%p
		return

def imageAction(source, target, volume, command, loop):
	pass

def systemAction(source, target, volume, command, loop):
	pass

def mariaAction(source, target, volume, command, loop):
	pass

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # <------ tcp 서버소켓 할당. 객체생성
	s.bind((host, port)) # <------- 소켓을 주소로 바인딩
	s.listen(1) # <------ listening 시작. 최대 클라이언트 연결 수 5개
	print 'Daemon of API Parser'

	while True:
		sock, senderIP = s.accept()
		print 'From:', senderIP[0]
		while True: # <-------- 클라이언트 연결이 오면 이 dialog 루프로 들어가서 데이터가 수신을 기다림
			data = sock.recv(buffer)
			if not data:
				break

			try:
				arrJson = json.loads(data)
			except:
				sock.send(json.dumps({"ip":senderIP[0], "category":"unknown", "msg":"JSON format error"},sort_keys=True)) 
				print "category:unknown", "msg:JSON format error", data
				break

			# if isinstance(arrJson, dict):
			if isinstance(arrJson, list):
				pass
			else:
				sock.send(json.dumps({"ip":senderIP[0], "category":"unknown", "msg":"Data should be JSON Array"},sort_keys=True)) 
				print "Data should be JSON Array not JSON Objects. Ex:[{}] or [{},{},,,]"
				break
			
			print len(arrJson), arrJson
			for i in range(len(arrJson)):
				args = arrJson[i]
				# print args
				# 카테고리는 내용을 포함 해서 필수 이다.
				if all (k in common["category"].keys() for k in args):
					pass
				else:
					sock.send(json.dumps({"ip":senderIP[0], "category":"unknown", "msg":"Missing category value"},sort_keys=True)) 
					print "category:unknown", "msg:Missing category value", i
					# break

				# 디버그 모드 상태에 따라 오류 메시지 출력 결정
				if "debug" not in args:
					args["debug"] = False

				if "gpio" in args:
					if all (k in args["gpio"] for k in common["category"]["gpio"].keys()):
						if args["gpio"]["status"] not in ("0", "1", "3", "6", "7", "8", "9"):
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"gpio", "msg":"Missing status value"},sort_keys=True)) 
						elif args["gpio"]["status"] in ("0", "1", "3") and not args["gpio"]["id"]:
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"gpio", "msg":"Missing id value"},sort_keys=True))
						else:
							response = gpioAction(args["gpio"]["status"], args["gpio"]["id"], args["gpio"]["hold"], args["gpio"]["msg"]) 
							if response: # Success
								sock.send(json.dumps({"ip":senderIP[0], "category":"gpio", "response":response},sort_keys=True))
							else: # Error
								if args["debug"]:
									sock.send(json.dumps({"ip":senderIP[0], "category":"gpio", "msg":"No action"},sort_keys=True))
					else:
						if args["debug"]:
							sock.send(json.dumps({"ip":senderIP[0], "category":"gpio", "msg":"Missing args"},sort_keys=True))
				if "audio" in args:
					if all (k in args["audio"] for k in common["category"]["audio"].keys()):
						if not args["audio"]["source"]:
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":"Missing source value"},sort_keys=True)) 
						elif not args["audio"]["target"]:
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":"Missing target value"},sort_keys=True)) 
						elif not args["audio"]["volume"]:
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":"Missing volume value"},sort_keys=True)) 
						elif not args["audio"]["command"]:
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":"Missing command value"},sort_keys=True)) 
						elif not args["audio"]["loop"]:
							if args["debug"]:
								sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":"Missing loop value"},sort_keys=True)) 
						else:
							# 오디오 전송
							response = audioAction(args["audio"]["source"], args["audio"]["target"], args["audio"]["volume"], args["audio"]["command"], args["audio"]["loop"]) 
							if response: # Error
								if args["debug"]:
									sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":response },sort_keys=True))
							else: # Success
									sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "response":{"sent":args["audio"]["target"]}},sort_keys=True))
					else:
						if args["debug"]:
							sock.send(json.dumps({"ip":senderIP[0], "category":"audio", "msg":"Missing args"},sort_keys=True))

					# result = audioIPOut(source, target, volume, command, loop) ## mplayer를 통해 오디오 출력
				if "image" in args:
					pass
				if "system" in args:
					pass
				if "maria" in args:
					pass
				if "custom" in args:
					pass
				
			break # <-- 크라이언트에서 세션 종료 유무와 무관하게 자체에서 센션종료함
			
		sock.close() # <------ 클라이언트 세션 종료
	s.close() # <------- 위 루프가 끝나지 않으므로 이 라인은 실행되지 않는다. just a remainder of close() 

if __name__ == '__main__':
	share = readConfig('/home/pi/common/config.json')
	
	host = get_ip_address()
	port = share["port"]["its"]
	buffer = 4096  # Normally 1024, but we want fast response

	common = readConfig("./itsAPI.json")

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)	# Set's GPIO pins to BCM GPIO numbering
	for key, value in common["gpioIn"].iteritems():
		GPIO.setup(value, GPIO.IN) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
	for key, value in common["gpioOut"].iteritems():
		GPIO.setup(value, GPIO.OUT) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
	for key, value in common["gpioPw"].iteritems():
		GPIO.setup(value, GPIO.OUT) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
	# # 주의: cleanup을 하면 종료를 의미 하며 GPWIO Node가 죽는다.
	# GPIO.cleanup()

	## audio
	audioFolder = share["path"]["audio"] + "/common/"
	sourceList = os.listdir(audioFolder)
	sourceList.sort()
	# print sourceList

	# itsList = findITS(host)
	# print itsList

	main()
