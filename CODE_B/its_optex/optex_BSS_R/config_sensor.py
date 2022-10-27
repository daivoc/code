#!/usr/bin/env python
# -*- coding: utf-8 -*-  

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

######################## 사용자 설정 
ERROR_socket_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
ERROR_socketRecv_cnt = 8
ERROR_connect_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
ERROR_sleep_cnt = 2 # 초
ERROR_recv_timeout = 16 #절대 10초(센서의 하느비트 주기가 10초임으로) 이하면 않됩 초
ERROR_check_cnt_max = 20 # 최초실행시 디비와 센서체크 오류 횟수

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
