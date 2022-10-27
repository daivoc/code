#!/usr/bin/python
# -*- coding: utf-8 -*-

# mysql
db_host = "localhost"
db_user = "its"
db_pass = "GXnLRNT9H50yKQ3G"
db_name = "its_web" # 기본 데이터베이스 

web_name = "its_web" # 웹페이지 폴더명
theme_name = "ecos-its_optex" # Optex Theme

ITS_common_path = "/home/pi/common"
ITS_utility_path = "/home/pi/utility"

# 센서 환경설정 테이블 명
ITS_sensor_log_table = "w_log_sensor" # 로그파일 테이블명의 PreFix로 사용
ITS_sensor_cfg_table = "w_cfg_sensor" # 웹에서는 실제 사용하지 않음
ITS_sensor_blk_table = "w_block_event" # 예약차단 테이블

ITS_w_cfg_sensor_TTY = "g5_write_g100t100" # ITS_WEB에서 생성된 테이블 
ITS_w_cfg_sensor_RELAY = "g5_write_g100t160" # ITS_WEB에서 생성된 테이블 
ITS_w_cfg_sensor_BSS = "g5_write_g200t100" # ITS_WEB에서 생성된 테이블 Optex Microwave
ITS_w_cfg_sensor_BSS_R = "g5_write_g200t110" # ITS_WEB에서 생성된 테이블 Optex Microwave
ITS_w_cfg_sensor_SPEED = "g5_write_g200t120" # ITS_WEB에서 생성된 테이블 Optex Microwave
ITS_w_cfg_sensor_RLS = "g5_write_g200t200" # ITS_WEB에서 생성된 테이블 Optex Laser
ITS_w_cfg_sensor_GPIO = "g5_write_g300t100" # ITS_WEB에서 생성된 테이블 

ITS_log_data = "/var/www/html/"+web_name+"/data/log/" # Log File 저장 위치
ITS_img_data = "/var/www/html/"+web_name+"/data/image/" # Log File 저장 위치

ITS_map_content = "/var/www/html/"+web_name+"/data/table_monitoring_map.svg"
ITS_map_source = "/var/www/html/"+web_name+"/theme/"+theme_name+"/utility/nodeJs_table/table_templet_map.html" 
ITS_map_target = "/var/www/html/"+web_name+"/theme/"+theme_name+"/utility/nodeJs_table/table_BSS_map.html" 

ITS_host_gate = web_name+"/utility/sensorMgr/collectEvent.php" # w_host_enable 되어있으면 host_ip를 통해 각각의 센서에서 발생이벤트를 w_collect_event 테이블에 자료 등록

ECOS_table_prefix = "g5_write_"
ECOS_table_SERIAL = "g100t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_BSS = "g200t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_BSS_R = "g200t110" # ITS_WEB에서 생성된 테이블 
ECOS_table_SPEED = "g200t120" # ITS_WEB에서 생성된 테이블 
ECOS_table_RLS = "g200t200" # ITS_WEB에서 생성된 테이블 
ECOS_table_RLS_R = "g200t210" # ITS_WEB에서 생성된 테이블 
ECOS_table_PARKING = "g200t220" # ITS_WEB에서 생성된 테이블 
ECOS_table_GPIO = "g300t100" # ITS_WEB에서 생성된 테이블 

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

date_of_old = 30 # 일수

######################## 사용자 설정 
ERROR_socket_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
ERROR_socketRecv_cnt = 8
ERROR_connect_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
ERROR_sleep_cnt = 2 # 초
ERROR_recv_timeout = 16 #절대 10초(센서의 하느비트 주기가 10초임으로) 이하면 않됩 초
ERROR_check_cnt_max = 8 # 최초실행시 디비와 센서체크 오류 횟수

# //// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
# E:\Development\raspberryPi\Programs\optex\config_db.py
MAX_event_holdTime = 100 # 최대 이밴트 허용 횟수 : 1회 =~ 0.1초
MAX_event_pickTime = 3000 # mSec 
MAX_event_allowSameCount = 512 # 동일한 거리 레벨이 연속적이면 문제 제기

Event_type = {}
Event_type['init']	= 0
Event_type['active']	= 1
Event_type['idle']	= 2
Event_type['post']	= 3
Event_type['shot']	= 4 # 사진
Event_type['alarm']	= 5
Event_type['block']	= 6
Event_type['reload']	= 7
Event_type['start']	= 8
Event_type['error']	= 9

Event_desc = {}
Event_desc[0] = 'Init. System'
Event_desc[1] = 'Active Event'
Event_desc[2] = 'Idle Event'
Event_desc[3] = 'Post Event'
Event_desc[4] = 'Snapshot'
Event_desc[5] = 'Alarm Light'
Event_desc[6] = 'Block/Schedule'
Event_desc[7] = 'Reload Program'
Event_desc[8] = 'Start Program'
Event_desc[9] = 'Error Event'
if __name__ == '__main__':
	pass
