#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import datetime
import subprocess 
import fcntl
# 파일로 로그를 남기는 경우 파일이 너무 커지면 자동으로 새로운 파일
import logging
import logging.handlers

import struct
import binascii
import socket

import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO

from multiprocessing import Process

# http://www.thecodingcouple.com/watermark-images-python-pillow-pil/
# 이미지 처리 프로그램
# $ sudo apt-get install python-pip
# $ sudo apt-get install libjpeg-dev
# $ sudo pip install Pillow
from PIL import Image, ImageDraw, ImageFont

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

# 자신 아이피 확인 
def get_ip_address(ifname): # get_ip_address('eth0')  # '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])
# 센서 아이피 확인 
def check_sensor(sensorIP):
    return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_SPEED(): 
	cmd = "kill $(ps aux | grep '[p]ython -u -W ignore /home/pi/optex_SPEED/optex_SPEED.pyc' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()

	
# 확인된 변수로 데몬을 실행 한다
def run_demon_SPEED(arg): 
	cmd = "python -u -W ignore /home/pi/optex_SPEED/optex_SPEED.pyc %s 2>&1 & " % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_SPEED_table(): 
	cmd = "kill $(ps aux | grep '[n]ode table_SPEED.js' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_SPEED_table(arg): 
	ITS_web_path = "/var/www/html/its_web" # 웹페이지 폴더명 /var/www/html/its_web/theme/ecos-its_optex/utility/nodeJs_table/
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd %s/%s; node table_SPEED.js %s 2>&1 & " % (ITS_web_path, path, arg)
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 원격 카메라 이미지 다운로드
# ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/ITS_%s.jpg  -q -o /dev/null
def run_wget_image(source, target): 
	cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (source, target)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def run_msg_on_image(path, msg):
	cmd = "python /home/pi/common/msg_on_image.pyc %s %s 2>&1 & " % (path, msg)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out
	# image = Image.open(open('/var/www/html/its_web/data/image/BSS_SP_ETH1_19216816810/2017/09/26/16/31_11_150641107139.jpg', 'rb'))
	# draw = ImageDraw.Draw(image)
	# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",30)
	# text = "2017-09-26 16:15:36.351617 4m 10Km/h\n 2017-09-26 16:15:36.574791 3m 9Km/h\n 2017-09-26 16:15:36.808844 6m 6Km/h\n 2017-09-26 16:15:36.922885 9m 4Km/h\n "
	# draw.text((1260, 860), text, font=font)
	# image.save('/var/www/html/its_web/data/image/BSS_SP_ETH1_19216816810/2017/09/26/16/31_11_150641107139.jpg',optimize=True,quality=90)

# 오래된 파일 삭제
def run_remove_old_file(path, day):
	if (path and day):
		cmd = "find %s -type f -ctime %s -exec rm -rf {} \;" % (path, day) # day 이후 모두 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
		cmd = "find %s -type d -empty -delete" % (path)	 # 비어있는 폴더 삭제
		p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
# 프로그램 오류 발생 또는 설정 변경후 다시 자신의 프로그램을 다시 시작 한다.
def restart_myself():
	# os.execv(__file__, sys.argv)
	print sys.executable, " ", sys.argv
	# os.execv(sys.executable, [sys.executable] + sys.argv)
	os.execv(__file__, sys.argv)

# 프로그램 오류 발생시 부모프로그램 다시 실행 한다.
def restart_its(): 
	## command to run - tcp only ##
	cmd = "python /home/pi/optex_SPEED/run_optex.pyc"
	# cmd = "python demon.pyc %s 2>&1 & " % arg 
	print(cmd)
	## run it ##
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 프로그램 오류 발생시 시스템 다시 시작 한다.
def reboot_its():
	# os.system('/sbin/shutdown -r now')
	os.system('sudo reboot')
	
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

def get_current_location_BSS(lat_s,lng_s,lat_e,lng_e, tmp_distant, MAX_stepOfZone, MAX_numberOfZone): # 좌표와 좌표 특정한 중간점의 좌표
	# print lat_s,lng_s,lat_e,lng_e, tmp_distant, MAX_stepOfZone, MAX_numberOfZone
	# 37.486487358 127.10386268 37.48644736 127.106177675 18304.0 1000.0 200
	# 37.486487358 127.10386268 37.48644736 127.106177675 17473.0 1000.0 200
	# 37.486487358 127.10386268 37.48644736 127.106177675 15811.0 1000.0 200
	# 37.486487358 127.10386268 37.48644736 127.106177675 24121.0 1000.0 200
	# 37.486447360 127.10617767
	
	unit_coord_lat = (lat_e - lat_s) / MAX_numberOfZone
	unit_coord_lng = (lng_e - lng_s) / MAX_numberOfZone
	# if tmp_distant is 0: tmp_distant = 1
	dist_zone = tmp_distant / MAX_stepOfZone
	lat_s_n = lat_s + (unit_coord_lat * dist_zone)
	lng_s_n = lng_s + (unit_coord_lng * dist_zone)
	lat_e_n = lat_s_n + unit_coord_lat
	lng_e_n = lng_s_n + unit_coord_lat

	# print lat_s_n,lng_s_n,tmp_distant
	coordinate = []
	coordinate = [lat_s_n,lng_s_n,lat_e_n,lng_e_n,dist_zone]
	
	return coordinate

def get_light_level(sT, sV, eT, eV):
	cT = datetime.datetime.now().strftime("%H%M") # 현재 시:분
	# print sT, sV, eT, eV, cT
	if ((sT < cT) and (eT > cT)):
		return sV
	else:
		return eV

	
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
