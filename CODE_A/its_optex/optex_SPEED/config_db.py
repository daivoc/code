#!/usr/bin/python
# -*- coding: utf-8 -*-

# mysql
db_host = "localhost"
db_user = "its"
db_pass = "GXnLRNT9H50yKQ3G"
db_name = "its_web" # 기본 데이터베이스 

ITS_web_path = "/var/www/html/its_web" # 웹페이지 폴더명

# 센서 환경설정 테이블 명
ITS_sensor_log_table = "w_log_sensor" # 로그파일 테이블명의 PreFix로 사용
ITS_sensor_cfg_table = "w_cfg_sensor" # 웹에서는 실제 사용하지 않음
ITS_sensor_blk_table = "w_block_event" # 예약차단 테이블

# ITS_w_cfg_sensor_TTY = "g5_write_g100t100" # ITS_WEB에서 생성된 테이블 
# ITS_w_cfg_sensor_RELAY = "g5_write_g100t160" # ITS_WEB에서 생성된 테이블 
# ITS_w_cfg_sensor_BSS = "g5_write_g200t100" # ITS_WEB에서 생성된 테이블 Optex Microwave
# ITS_w_cfg_sensor_BSS_R = "g5_write_g200t110" # ITS_WEB에서 생성된 테이블 Optex Microwave
# ITS_w_cfg_sensor_SPEED = "g5_write_g200t120" # ITS_WEB에서 생성된 테이블 Optex Microwave
# ITS_w_cfg_sensor_RLS = "g5_write_g200t200" # ITS_WEB에서 생성된 테이블 Optex Laser
# ITS_w_cfg_sensor_GPIO = "g5_write_g300t100" # ITS_WEB에서 생성된 테이블 

ITS_log_data = ITS_web_path+"/data/log/" # Log File 저장 위치
ITS_img_data = ITS_web_path+"/data/image/" # Log File 저장 위치

ECOS_table_prefix = "g5_write_"
ECOS_table_SERIAL = "g100t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_BSS = "g200t100" # ITS_WEB에서 생성된 테이블 
ECOS_table_BSS_R = "g200t110" # ITS_WEB에서 생성된 테이블 
ECOS_table_SPEED = "g200t120" # ITS_WEB에서 생성된 테이블 
ECOS_table_RLS = "g200t200" # ITS_WEB에서 생성된 테이블 
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
