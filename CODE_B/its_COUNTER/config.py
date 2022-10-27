#!/usr/bin/python
# -*- coding: utf-8 -*-

# mysql
db_host = "localhost"
db_user = "its"
db_pass = "GXnLRNT9H50yKQ3G"
db_name = "its_web" # 기본 데이터베이스 

web_name = "its_web" # 웹페이지 폴더명

## 데이터베이스 접속 시도 횟수
db_connection_limit = 10
## 데이터 베이스 확인 주기
db_reload_cycle = 10

## GPIO Info
L_TRIG = 5 # 5 => 'Relay_04'
L_ECHO = 6 # 6 => 'Relay_03'
R_TRIG = 13 # 13 => 'Relay_02'
R_ECHO = 19 # 19 => 'Relay_01'
T_TRIG = 22 # 22 => 'Relay_05'
T_ECHO = 27 # 27 => 'Relay_06'
# 17 => 'Relay_07',
# 4 => 'Relay_08'


ITS_common_path = "/home/pi/common"

# 센서 환경설정 테이블 명
ITS_sensor_log_table = "w_log_sensor" # 로그파일 테이블명의 PreFix로 사용
ITS_sensor_blk_table = "w_block_event" # 예약차단 테이블

ITS_w_cfg_sensor_COUNTER = "g5_write_g300t200" # ITS_WEB에서 생성된 테이블 

ITS_log_data = "/var/www/html/"+web_name+"/data/log/" # Log File 저장 위치
ITS_img_data = "/var/www/html/"+web_name+"/data/image/" # Log File 저장 위치

ITS_M_map_source = "table_COUNTER.html" 
ITS_M_map_target = "index.html" 

ITS_host_gate = web_name+"/utility/sensorMgr/collectEvent.php" # w_host_enable 되어있으면 host_ip를 통해 각각의 센서에서 발생이벤트를 w_collect_event 테이블에 자료 등록

ECOS_table_prefix = "g5_write_"
ECOS_table_SERIAL = "g100t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_BSS = "g200t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_RLS = "g200t200" # ITS_WEB에서 생성된 테이블 
ECOS_table_GPIO = "g300t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_COUNTER = "g300t200" # ITS_WEB에서 생성된 테이블 


W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

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
