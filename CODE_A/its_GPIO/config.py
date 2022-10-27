#!/usr/bin/python
# -*- coding: utf-8 -*-

db_host = "localhost"
db_user = "its"
db_pass = "GXnLRNT9H50yKQ3G"
db_name = "its_web" # 기본 데이터베이스 

op_pass = 'optex5971'

date_of_old = 30 # 일수

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # Red
G  = '\033[32m' # Green
Y  = '\033[33m' # Yellow
B  = '\033[34m' # Blue
P  = '\033[35m' # Purple
C  = '\033[36m' # Cyan# Cyan

ITS_common_path = "/home/pi/common"
ITS_gpio_path = "/home/pi/GPIO"
ITS_web_path = "/var/www/html/its_web" # 웹페이지 전체경로
ITS_audio_flag = "/tmp/audioOut"

ITS_web = "its_web" # 웹페이지 폴더명

ECOS_log_data = ITS_web_path+"/data/log/" # Log File 저장 위치
ECOS_img_data = ITS_web_path+"/data/image/" # Log File 저장 위치

ECOS_table_prefix = "g5_write_"
ECOS_table_GPIO = "g300t100" # ITS_WEB에서 생성된 테이블 

# 센서 환경설정 테이블 명
ECOS_sensor_log_table = "w_log_sensor" # 로그파일 테이블명의 PreFix로 사용
ECOS_sensor_blk_table = "w_block_event" # 예약차단 테이블

# Sun Mon Tue Wed Thu Fri Sat 
#  1   2   3   4   5   6   7  
#  6   0   1   2   3   4   5  
ECOS_week_map = {
	0 : "2017-01-02", # 월요일
	1 : "2017-01-03", # 화요일
	2 : "2017-01-04",
	3 : "2017-01-05",
	4 : "2017-01-06",
	5 : "2017-01-07",
	6 : "2017-01-01", # 일요일
}

########################################################
GPOUT = { 1:18, 2:23, 3:24, 4:25, 5:6, 6:7, 7:8, 8:9 } # GPIO 논리:실제, 출력: 1 ~ 4, 예약포트: 5 ~ 8
GPIN = { 1:19, 2:13, 3:6, 4:5, 5:22, 6:27, 7:17, 8:4 } # GPIO 입력: 1 ~ 8 예) GPIN[3] -> 6

Event_type = {
	'init':0,
	'active':1,
	'idle':2,
	'post':3,
	'shot':4, # 사진
	'alarm':5,
	'block':6,
	'reload':7,
	'start':8,
	'error':9
}

Event_desc = {
	0:'Init._System',
	1:'Active_Event',
	2:'Idle_Event',
	3:'Post_Event',
	4:'Snapshot',
	5:'Alarm_Light',
	6:'Block_Schedule',
	7:'Reload_Program',
	8:'Start_Program',
	9:'Error_Event'
}

if __name__ == '__main__':
	pass
