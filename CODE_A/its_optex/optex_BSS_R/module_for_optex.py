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


# multiprocessing 라이브러리를 이용해서 일정시간(druation)동안 알람을 발생 시킨다.
# Using - Process(target=alarmOut, args=(2,7)).start()
# http://mydb.tistory.com/245
# http://studymake.tistory.com/498
# def alertOut(port, druation): # GPIO Port No. , Action Due
	# # GPIO.setup(port, GPIO.OUT)
	# # GPIO.output(port, GPIO.HIGH)
	# iteracion = 0
	# print port, druation, "-------------------------"
	# while iteracion < druation:
		# GPIO.output(port, False)
		# time.sleep(1) ## Wait one second
		# iteracion = iteracion + 1
	# GPIO.output(port, True)
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

# # MYSQL 실행 확인 
# def check_mysql():
	# # cmd = "ps -fU mysql | grep mysqld.sock | wc -l"
	# cmd = "ps -fU mysql | grep mysqld | wc -l"
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	# return p.communicate()
    # # return os.system("pgrep mysql | wc -l") # IF RETURN 0 THAT Network Active ELSE Network Error

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BSS01(): 
	# cmd = "kill $(ps aux | grep '[p]ython -u -W ignore /home/pi/optex_BSS_R/optex_BSS01.pyc' | awk '{print $2}')" 
	cmd = "kill $(ps aux | grep '[p]ython /home/pi/optex_BSS_R/optex_BSS01.pyc' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()

	
# 확인된 변수로 데몬을 실행 한다
def run_demon_BSS01(arg): 
	# cmd = "python -u -W ignore /home/pi/optex_BSS_R/optex_BSS01.pyc %s 2>&1 & " % arg
	# -W ignore : 콘솔 출력 GPIO.setwarnings(False) to disable warnings
	cmd = "python /home/pi/optex_BSS_R/optex_BSS01.pyc %s 2>&1 & " % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# # 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
# def kill_demon_UNION_table(): 
	# cmd = "kill $(ps aux | grep '[n]ode table_union.js' | awk '{print $2}')"
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	# time.sleep(1)
	
# # 확인된 변수로 데몬을 실행 한다
# def run_demon_UNION_table(arg): 
	# path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	# cmd = "cd /var/www/html/its_web/%s; node table_union.js %s 2>&1 & " % (path, arg)
	# p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BSS01_table(): 
	cmd = "kill $(ps aux | grep '[n]ode table_BSS_R.js' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_BSS01_table(arg): 
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node table_BSS_R.js %s 2>&1 & " % (path, arg)
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
# 모니터링을 위한 지도파일을 생성한다.
def make_table_map_html(source, target, content):
	__script_jquery_js__ = '/home/pi/common/jquery/jquery-3.1.1.min.js'
	__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	__script_jquery_ui_js__ = '/home/pi/common/jquery/ui/jquery-ui.js'
	__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	__style_jquery_ui_css__ = '/home/pi/common/jquery/ui/jquery-ui.css'
	__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	
	# __svg_pan_zoom__ = '/home/pi/common/svg-pan-zoom/svg-pan-zoom.js'
	# __svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'
	__smoothiecharts__ = '/home/pi/common/smoothiecharts/smoothie.js'
	__smoothiecharts__ = '<script>'+open(__smoothiecharts__, 'r').read()+'</script>'
	
	# __svg_content__ = open(content, 'r').read()
	
	# print __style_jquery_ui_css__
	with open(source, 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
		# tmp_its_tmp = tmp_its_tmp.replace('__svg_pan_zoom__', __svg_pan_zoom__)
		tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
		# tmp_its_tmp = tmp_its_tmp.replace('__svg_content__', __svg_content__)
		with open(target, 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()
	
# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_BSS01_map(): 
	cmd = "kill $(ps aux | grep '[n]ode table_BSS_map.js' | awk '{print $2}')" 
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	# p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()
	
# 확인된 변수로 데몬을 실행 한다
def run_demon_BSS01_map(arg): 
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node table_BSS_map.js %s 2>&1 & " % (path, arg)
	## run it ##
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def restart_BSS():
	# print(sys.executable, sys.executable, " ", sys.argv)
	os.execl(sys.executable, sys.executable, *sys.argv)

# 원격 카메라 이미지 다운로드
# ex: /usr/bin/wget http://121.154.205.28:8001/snapshot/1/snapshot.jpg -O /var/www/html/its_web/tmp/ITS_%s.jpg  -q -o /dev/null
def run_wget_image(source, target): 
	cmd = "/usr/bin/wget %s -O %s -q -o /dev/null" % (source, target)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 프로그램 오류 발생 또는 설정 변경후 다시 자신의 프로그램을 다시 시작 한다.
def restart_myself():
	# os.execv(__file__, sys.argv)
	print sys.executable, " ", sys.argv
	# os.execv(sys.executable, [sys.executable] + sys.argv)
	os.execv(__file__, sys.argv)

# 프로그램 오류 발생시 부모프로그램 다시 실행 한다.
def restart_wits(): 
	## command to run - tcp only ##
	cmd = "python /home/pi/optex_BSS_R/run_optex.pyc"
	# cmd = "python demon.pyc %s 2>&1 & " % arg 
	print(cmd)
	## run it ##
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

	# 프로그램 오류 발생시 시스템 다시 시작 한다.
def reboot_wits():
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
	dist_zone = tmp_distant / MAX_stepOfZone
	lat_s_n = lat_s + (unit_coord_lat * dist_zone)
	lng_s_n = lng_s + (unit_coord_lng * dist_zone)
	lat_e_n = lat_s_n + unit_coord_lat
	lng_e_n = lng_s_n + unit_coord_lat

	# print lat_s_n,lng_s_n,tmp_distant
	coordinate = []
	coordinate = [lat_s_n,lng_s_n,lat_e_n,lng_e_n,dist_zone]
	
	return coordinate
	
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
