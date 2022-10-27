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

import sys
import time
import os, traceback
import subprocess
import json

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)

def checkFlag(audioFlag): ## audioFlag란 파일이 존재하면 사용중으로 간주, 바로 종료
	if os.path.isfile(audioFlag):
		print('checkFlag Busy %s'%audioFlag)
		quit()

def makeFlag(audioFlag): ## audioFlag 파일을 생성하여 오디오 중복 실행을 방지
	open(audioFlag, 'a').close()
	# print('makeFlag %s'%audioFlag)

def removeFlag(audioFlag): ## audioFlag 파일을 삭재하여 오디오 실행을 허용함
	os.remove(audioFlag)
	# print('removeFlag %s'%audioFlag)

def audioOut(audioName, volume=500): # 
	# volume = cfg["mPlayer"]["omxplayer"]["volume"]
	cmd = "omxplayer -o local --vol %s %s >/dev/null & " % (volume, audioName)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	print('audioOut %s'%cmd)

def main():
	time.sleep(audioTime)
	removeFlag(audioFlag)
	quit()
	
if __name__ == '__main__':
	cfg = readConfig('/home/pi/common/config.json')
	audioFlag = cfg["path"]["common"]+'/audioOut'

	checkFlag(audioFlag) ## audioFlag란 파일이 존재하면 사용중으로 간주, 바로 종료

	## 오디오 파일명과 길이(float) 값이 없으먼 부족
	if len(sys.argv) == 4 and sys.argv[1] and sys.argv[2] and sys.argv[3]:
		audioName = sys.argv[1] # MP3 File name with path
		audioTime = float(sys.argv[2]) # 출력지속시간:초(float)
		audioVolume = int(sys.argv[3]) # 볼륨(int)
	else:
		print "Example(File Time Volume):\n\tpython %s /usr/share/sounds/alsa/Front_Center.wav 2 500"%sys.argv[0]
		quit()
	
	makeFlag(audioFlag) ## audioFlag 파일을 생성하여 오디오 중복 실행을 방지
	
	audioOut(audioName, audioVolume) ## omxplayer를 통해 mp3 오디오 출력

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
		removeFlag(audioFlag)
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)