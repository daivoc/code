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
date_of_old = 30 # 일수

MAX_event_allowSameCount = 512; # 동일한 거리 레벨이 연속적이면 문제 제기

ERROR_socket_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
ERROR_socketRecv_cnt = 8
ERROR_connect_cnt = 16 # 소켓 접속 오류 제한 횟수, 초과시 프로그램 종료
ERROR_sleep_cnt = 2 # 초
ERROR_recv_timeout = 16 # 초
ERROR_check_cnt_max = 8 # 최초실행시 디비와 센서체크 오류 횟수

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

########################################################
RLS_limit_time_delta = 10 # Sec, RLS_time_delta_limit 이상 이벤트 발생이 없으면 오류 발생
RLS_limit_time_delta_msg = "Waiting Heartbit over %s Secs. May disconnected sensor." % RLS_limit_time_delta

# Master Alarm
RLS_desc_MA = {}
RLS_desc_MA['MO'] = "감지"
RLS_desc_MA['CL'] = "감지 상태 종료"

# The Latest Area
# RLS-2020: A1/A2/B1/B2, RLS-3060: A1/A2/B1/B2 or A11/A12/A21/A22/B11/B12/B21/B22
RLS_desc_LA = {}
RLS_desc_LA['A1'] =  "A1 감지"
RLS_desc_LA['A2'] =  "A2 감지"
RLS_desc_LA['B1'] =  "B1 감지"
RLS_desc_LA['B2'] =  "B2 감지"
RLS_desc_LA['A11'] = "A11 감지"
RLS_desc_LA['A12'] = "A12 감지"
RLS_desc_LA['A21'] = "A21 감지"
RLS_desc_LA['A22'] = "A22 감지"
RLS_desc_LA['B11'] = "B11 감지"
RLS_desc_LA['B12'] = "B12 감지"
RLS_desc_LA['B21'] = "B21 감지"
RLS_desc_LA['B22'] = "B22 감지"

# Combination of Areas - The code shows multiple areas where objects are detected. 
RLS_desc_CA = {}
RLS_desc_CA['AA'] = "__,__,A1,A2 감지"
RLS_desc_CA['BB'] = "B2,B1,__,__ 감지"
RLS_desc_CA['BA'] = "B2,__,__,A2 감지"
RLS_desc_CA['Ba'] = "B2,__,A1,__ 감지"
RLS_desc_CA['bA'] = "__,B1,__,A2 감지"
RLS_desc_CA['ba'] = "__,B1,A1,__ 감지"
RLS_desc_CA['EA'] = "B2,B1,A1,__ 감지"
RLS_desc_CA['Ea'] = "B2,B1,__,A2 감지"
RLS_desc_CA['Eb'] = "B2,__,A1,A2 감지"
RLS_desc_CA['EB'] = "__,B1,A1,A2 감지"
RLS_desc_CA['AL'] = "B2,B1,A1,A2 감지"

# Multiple Areas - "CC" means that objects are detected in multiple areas.
RLS_desc_CC = {}
RLS_desc_CC['CC'] = "복수영역 감지"

# Disqualification - "DQ" means disqualification status. "dq" means that disqualification status is cleared.
RLS_desc_DQ = {}
RLS_desc_DQ['DQ'] = "날씨 환경이 열악한 상태" 
RLS_desc_DQ['dq'] = "상황(날씨 환경이 열악한 상태) 종료됨"

# Anti-rotation - "AR" means that the unit is rotated. "ar" means that the rotation is recovered.
RLS_desc_AR = {}
RLS_desc_AR['AR'] = "센서 틀어진 상태"
RLS_desc_AR['ar'] = "상황(센서 틀어진 상태) 종료됨"

# Anti-masking - "AM" means that the unit is masked. "am" means that the mask is recovered.
RLS_desc_AM = {}
RLS_desc_AM['AM'] = "센서시계 차단(Masked) 상태"
RLS_desc_AM['am'] = "상황(센서시계 차단 상태) 종료됨"

# Internal Error - "TR" means that internal error occurred. "tr" means that the error is recovered.
RLS_desc_TR = {}
RLS_desc_TR['TR'] = "센서 내부 오류발생"
RLS_desc_TR['tr'] = "상황(센서 내부오류) 종료됨"

# Soiling - "SO" means that laser window has dirt. "so" means that the dirt is removed.
RLS_desc_SO = {}
RLS_desc_SO['SO'] = "창이 더러운 상태"
RLS_desc_SO['so'] = "상황(창이 더러운 상태) 종료됨"

# Tamper or Device Monitoring - Cover is opened, or the unit is removed from the wall. "ta" means that the trouble is recovered. 
# If device monitoring is enabled, "DM" is stored in this section and sent repeatedly. "DM" is supported by RLS-2020.
RLS_desc_TA = {}
RLS_desc_TA['TA'] = "센서커버 열림 또는 벽에서 분리됨"
RLS_desc_TA['ta'] = "상황(센서의 커버가 열렸거나 벽에서 분리됨) 종료됨"
RLS_desc_TA['DM'] = "섹션이 저장(RLS-2020 기능)"


# Combination of Areas - The code shows multiple areas where objects are detected. 
RLS_map_CA = {}
RLS_map_CA['AA'] = "a1,a2"
RLS_map_CA['BB'] = "b2,b1"
RLS_map_CA['BA'] = "b2,a2"
RLS_map_CA['Ba'] = "b2,a1"
RLS_map_CA['bA'] = "b1,a2"
RLS_map_CA['ba'] = "b1,a1"
RLS_map_CA['EA'] = "b2,b1,a1"
RLS_map_CA['Ea'] = "b2,b1,a2"
RLS_map_CA['Eb'] = "b2,a1,a2"
RLS_map_CA['EB'] = "b1,a1,a2"
RLS_map_CA['AL'] = "b2,b1,a1,a2"

# 센서 지역을 수치로 변환
# RLS-2020: A1/A2/B1/B2, RLS-3060: A1/A2/B1/B2 or A11/A12/A21/A22/B11/B12/B21/B22
RLS_map_LA = {}
RLS_map_LA[''] =  -1
RLS_map_LA['A1'] =  2
RLS_map_LA['A2'] =  3
RLS_map_LA['B1'] =  1
RLS_map_LA['B2'] =  0
RLS_map_LA['A11'] = 4
RLS_map_LA['A12'] = 5
RLS_map_LA['A21'] = 6
RLS_map_LA['A22'] = 7
RLS_map_LA['B11'] = 3
RLS_map_LA['B12'] = 2
RLS_map_LA['B21'] = 1
RLS_map_LA['B22'] = 0

if __name__ == '__main__':
	pass
