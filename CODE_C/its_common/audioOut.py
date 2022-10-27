#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# 본 프로그램은 오디오 출력을 단일 프로세서로 통합하는 기능으로
# 통합 변수사용이 불가능 함으로 특정파일의 존재를 변수값으로 사용한다.
# open('/home/pi/common/audioOut', 'a').close()
# python audioOutVolume /usr/share/sounds/alsa/Front_Center.wav 2.301 500

# 작동 구조
# /home/pi/common 내에 audioOut 이란 플래그 파일의 존재여부에 따라 
# 실행중인지의 여부를 판단한다.
# 프로그램이 실행되면 
# 변수 audioOut(/home/pi/common/audioOut) 파일명 audioOut을 생성한다.
# 오디오파일의 출력이 종료되면 
# /home/pi/common 내에 audioOut을 삭제후 졸료한다.

import os
import re
import sys
import json
import subprocess
import requests
import socket
import struct
import fcntl

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

def audioOut(source, target, volume): # 
	# cmd = "cat /var/www/html/its_web/data/audio/A_museum.mp3 | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume 100 - &>/dev/null; fi' "
	# print target, get_ip_address()
	if target == get_ip_address(): # 자신에게 있는 음원파일 이면
		cmd = "sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer &>/dev/null; then cat %s | mplayer -cache 1024 -volume %s - &>/dev/null; fi' &" % (target, source, volume)
	else:
		cmd = "cat %s | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@%s 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume %s - &>/dev/null; fi' &" % (source, target, volume)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def main():
	audioOut(source, target, volume) ## mplayer 통해 mp3 오디오 출력
	quit()
	
if __name__ == '__main__':
	cfg = readConfig('/home/pi/common/config.json')

	# commonPath = cfg["path"]["user"]["audio"] + "/common"
	commonPath = cfg["path"]["its_web"] + cfg["path"]["user"]["audio"] + "/api"
	sourceList = os.listdir(commonPath)
	sourceList.sort()
	# print commonPath+"/"+sourceList
	# print sourceList

	if len(sys.argv) == 4: 
		if sys.argv[1].isdigit(): # 목록에 있는 음원을 시용한다.
			if len(sourceList) < int(sys.argv[1]): # 리스트 목록에 없는 번호
				print "\t Unknown No. of list"
				quit()
			else:
				source = commonPath + "/" + sourceList[int(sys.argv[1])-1]
		else:
			if os.path.isfile(sys.argv[1]):
				source = sys.argv[1]
			elif validate_url(sys.argv[1]):
				url = sys.argv[1]
				name = "/tmp/audioSource" 
				try:
					# print (url, name)
					# 해당 URL에 송신 및 response 성공 시 파일 저장 
					r = requests.get(url, allow_redirects=True)
					open(name, 'wb').write(r.content)
				# 잘못된 URL 입력 시 예외 처리
				except Exception as e:
					print "\t Download failed"
					quit()
				else:
					source = name
			else:
				print "\t Unknown source path or url"
				quit()
		if validate_ip(sys.argv[2]):
			target = sys.argv[2]
		else:
			target = "localhost"

		if sys.argv[3].isdigit():
			volume = int(sys.argv[3])
		else: # 기본 소리 크기값 사용
			volume = cfg["mPlayer"]["mplayer"]["volume"]
		# print source, target, volume
	else:
		print "Example(File Time Volume):\n\tpython %s /usr/share/sounds/alsa/Front_Center.wav 192.168.0.20 80"%sys.argv[0]
		print "\tpython %s source [ip address] [volume(1~100)]"%sys.argv[0]
		i = 0
		for source in sourceList:
			i = i + 1
			print "\t", i, source

		quit()

	main()



# ## 로컬 오디오를 로컬 스피커로
# 	if ! pidof mplayer &>/dev/null; then mplayer /var/www/html/its_web/data/audio/A_museum.mp3; fi

# ## 원격 오디오를 로컬 스피커로
# 	# 원격에서
# 		# SSH를 통해 미디어파일을 가지고 온다.
# 	# 로컬에서
# 		# 현재 실행되는 스트리밍이 없으면 전송받은 스트리밍을 출력한다.
	
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /var/www/html/its_web/data/audio/A_museum.mp3" | if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume 100 - &>/dev/null; fi &

# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /var/www/html/its_web/data/audio/A_museum.mp3" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/freedesktop/stereo/*" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/ubuntu/stereo/*" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/ubuntu/ringtones/*" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/ubuntu/notifications/*" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/speech-dispatcher/*" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/Yaru/stereo/*" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/sound-icons/xylofon.wav" | mplayer -cache 1024 -volume 100 -
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 "cat /usr/share/sounds/alsa/Front_Right.wav" | mplayer -cache 1024 -volume 100 -

# ## 로컬 오디오 파일을 원격 스피커로 
# 	# 로컬에서
# 		# 자신에게 있는 오디오 파일을 열고 SSH를 통해 원격으로 전송한다
# 	# 원격에서
# 		# 현재 실행되는 스트리밍이 없으면 전송받은 스트리밍을 출력한다.
	
# 	cat /var/www/html/its_web/data/audio/A_museum.mp3 | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume 100 - &>/dev/null; fi' &
# 	cat /usr/share/sounds/freedesktop/stereo/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume 100 - &>/dev/null; fi' &
# 	cat /usr/share/sounds/ubuntu/stereo/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'if ! pidof mplayer &>/dev/null; then cat - | mplayer -cache 1024 -volume 100 - &>/dev/null; fi' &

# 	cat /var/www/html/its_web/data/audio/A_museum.mp3 | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/freedesktop/stereo/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/ubuntu/stereo/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/ubuntu/ringtones/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/ubuntu/notifications/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/speech-dispatcher/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/Yaru/stereo/* | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/sound-icons/xylofon.wav | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
# 	cat /usr/share/sounds/alsa/Front_Right.wav | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'

# ## 원격 마이크를 로컬 스피커로 - 아직 테스트 않됨
# 	sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.8 'arecord -f cd -t raw | oggenc - -r ' | mplayer -cache 1024 -volume -

# ## 로컬 마이크을 원격 스피커로
# 	arecord -f cd -t raw | oggenc - -r | sshpass -pits_iot ssh -o StrictHostKeyChecking=no pi@192.168.0.20 'cat - | mplayer -cache 1024 -volume 100 -'
