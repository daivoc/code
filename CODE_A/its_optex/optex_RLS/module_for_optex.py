#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import datetime
import subprocess 
# 파일로 로그를 남기는 경우 파일이 너무 커지면 자동으로 새로운 파일
import logging
import logging.handlers

import struct
import binascii
import socket

import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO

from multiprocessing import Process

### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
reload(sys)
sys.setdefaultencoding('utf-8')

def alertOut(port, druation): # GPIO Port No. , Action Due
	if(GPIO.input(port)):
		GPIO.output(port, False)
		time.sleep(druation)
		GPIO.output(port, True)
	else:
		pass
def alertOn(port): # GPIO Port No. , Action Due
	GPIO.output(port, False)
def alertOff(port): # GPIO Port No. , Action Due
	GPIO.output(port, True)

# 센서 아이피 확인 
def check_sensor(sensorIP):
    return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error
	
	
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_check_RLS(arg): 
	cmd = "kill $(ps aux | grep '[p]ython /home/pi/optex_RLS/optex_RLS.pyc %s' | awk '{print $2}')"  % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_check_RLS(arg): # python -W ignore
	cmd = "python /home/pi/optex_RLS/optex_RLS.pyc %s 2>&1 & " % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_realtime_RLS(arg): 
	cmd = "kill $(ps aux | grep '[n]ode realtime_RLS.js %s' | awk '{print $2}')" % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_realtime_RLS(arg): 
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node realtime_RLS.js %s 2>&1 & " % (path, arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 원격 카메라 이미지 다운로드
# ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/wits_%s.jpg  -q -o /dev/null
def run_wget_image(source, target): 
	cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (source, target)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 프로그램 오류 발생시 부모프로그램 다시 실행 한다.
def restart_its(): 
	cmd = "python /home/pi/optex_RLS/run_optex.pyc"
	print(cmd)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 프로그램 오류 발생시 시스템 다시 시작 한다.
def reboot_its():
	# os.system('/sbin/shutdown -r now')
	print "reboot ###################"
	return
	os.system('sudo reboot')

# 오래된 파일 삭제
def run_remove_old_file(path, day):
	if (path and day):
		cmd = "find %s -type f -ctime %s -exec rm -rf {} \;" % (path, day) # day 이후 모두 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		cmd = "find %s -type d -empty -delete" % (path)	 # 비어있는 폴더 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	
# 라즈베리 CPU Serial Code
def get_serial(): # 라즈베리 전용 코드
	# Extract serial from cpuinfo file
	cpuserial = "0000000000000000"
	try:
		f = open('/proc/cpuinfo','r')
		for line in f:
			if line[0:6]=='Serial':
				cpuserial = line[10:26]
		f.close()
	except:
		cpuserial = "ERROR000000000"
	return cpuserial
	
# 초단위를 시간차이값 형태로 변환 예: 2초 -> 0:00:02.000000
def conv_sec_2_time(second):
	return datetime.timedelta(seconds=second)

# 시간을 초로 반환한다.
def conv_time_2_sec(times):
	return times.total_seconds()

# 화면내용 삭제
def clear_screen(): # 초기 화면 내용 삭제 
	subprocess.call('clear',shell=True)

# 화면버퍼 출력
def print_buff(string): 
	sys.stdout.write(string)

screen_put = os.fdopen(sys.stdout.fileno(), 'w', 0)
def dot_out(str='.'):
	screen_put.write(str)
