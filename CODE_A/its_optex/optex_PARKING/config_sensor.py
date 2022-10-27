#!/usr/bin/env python
# -*- coding: utf-8 -*-  

####################################
## 주차시스템 관련 환경 변수
####################################

Buffer_size = 1024
Sensor_inner = "050" # 센서 아이피 마지막 3자리수로 출력됨
Sensor_outer = "030"
Heartbit_cycle = 10

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

ERROR_check_cnt_max = 20 # 최초실행시 센서체크 오류 횟수

Type_event = {}
Type_event[''] = 0
Type_event['B2'] = 1
Type_event['B1'] = 2
Type_event['A1'] = 3
Type_event['A2'] = 4

Type_event_in = {}
Type_event_in[''] = 0
Type_event_in['B2'] = 1
Type_event_in['B1'] = 2
Type_event_in['A1'] = 3
Type_event_in['A2'] = 4

Type_event_out = {}
Type_event_out[''] = 0
Type_event_out['A2'] = 1
Type_event_out['A1'] = 2
Type_event_out['B1'] = 3
Type_event_out['B2'] = 4

Status_event = {}
Status_event[0] = '0:None'
Status_event[1] = '1:Gate Open'
Status_event[2] = '2:Attached'
Status_event[3] = '3:Approach'
Status_event[4] = '4:Touch'
Status_event[5] = '5:Gate Close'
Status_event[6] = '6:Gate Block'
Status_event[9] = '9:Count UP'

Event_CA = {}
Event_CA['AA'] = "A1"
Event_CA['BB'] = "B2"
Event_CA['BA'] = "B2"
Event_CA['Ba'] = "B2"
Event_CA['bA'] = "B1"
Event_CA['ba'] = "B1"
Event_CA['EA'] = "B2"
Event_CA['Ea'] = "B2"
Event_CA['Eb'] = "B2"
Event_CA['EB'] = "B1"
Event_CA['AL'] = "B2"

Event_type = {}
Event_type['init']	= 0
Event_type['active']= 1
Event_type['idle']	= 2
Event_type['post']	= 3
Event_type['shot']	= 4 # 사진
Event_type['alarm']	= 5
Event_type['block']	= 6
Event_type['reload']= 7
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
RLS_desc_MA['MO'] = "detected(MA)"
RLS_desc_MA['CL'] = "closed(MA)"

# The Latest Area
# RLS-2020: A1/A2/B1/B2, RLS-3060: A1/A2/B1/B2 or A11/A12/A21/A22/B11/B12/B21/B22
RLS_desc_LA = {}
RLS_desc_LA['A1'] =  "A1"
RLS_desc_LA['A2'] =  "A2"
RLS_desc_LA['B1'] =  "B1"
RLS_desc_LA['B2'] =  "B2"
RLS_desc_LA['A11'] = "A11"
RLS_desc_LA['A12'] = "A12"
RLS_desc_LA['A21'] = "A21"
RLS_desc_LA['A22'] = "A22"
RLS_desc_LA['B11'] = "B11"
RLS_desc_LA['B12'] = "B12"
RLS_desc_LA['B21'] = "B21"
RLS_desc_LA['B22'] = "B22"

# Combination of Areas - The code shows multiple areas where objects are detected. 
RLS_desc_CA = {}
RLS_desc_CA['AA'] = "__,__,A1,A2"
RLS_desc_CA['BB'] = "B2,B1,__,__"
RLS_desc_CA['BA'] = "B2,__,__,A2"
RLS_desc_CA['Ba'] = "B2,__,A1,__"
RLS_desc_CA['bA'] = "__,B1,__,A2"
RLS_desc_CA['ba'] = "__,B1,A1,__"
RLS_desc_CA['EA'] = "B2,B1,A1,__"
RLS_desc_CA['Ea'] = "B2,B1,__,A2"
RLS_desc_CA['Eb'] = "B2,__,A1,A2"
RLS_desc_CA['EB'] = "__,B1,A1,A2"
RLS_desc_CA['AL'] = "B2,B1,A1,A2"

# Multiple Areas - "CC" means that objects are detected in multiple areas.
RLS_desc_CC = {}
RLS_desc_CC['CC'] = "multiple areas"

# Disqualification - "DQ" means disqualification status. "dq" means that disqualification status is cleared.
RLS_desc_DQ = {}
RLS_desc_DQ['DQ'] = "disqualification status(DQ)" 
RLS_desc_DQ['dq'] = "trouble(DQ) is recovered"

# Anti-rotation - "AR" means that the unit is rotated. "ar" means that the rotation is recovered.
RLS_desc_AR = {}
RLS_desc_AR['AR'] = "unit is rotated(AR)"
RLS_desc_AR['ar'] = "trouble(AR) is recovered"

# Anti-masking - "AM" means that the unit is masked. "am" means that the mask is recovered.
RLS_desc_AM = {}
RLS_desc_AM['AM'] = "unit is masked(AM)"
RLS_desc_AM['am'] = "trouble(AM) is recovered"

# Internal Error - "TR" means that internal error occurred. "tr" means that the error is recovered.
RLS_desc_TR = {}
RLS_desc_TR['TR'] = "Internal error(TR)"
RLS_desc_TR['tr'] = "trouble(TR) is recovered"

# Soiling - "SO" means that laser window has dirt. "so" means that the dirt is removed.
RLS_desc_SO = {}
RLS_desc_SO['SO'] = "window has dirt(SO)"
RLS_desc_SO['so'] = "trouble(SO) is recovered"

# Tamper or Device Monitoring - Cover is opened, or the unit is removed from the wall. "ta" means that the trouble is recovered. 
# If device monitoring is enabled, "DM" is stored in this section and sent repeatedly. "DM" is supported by RLS-2020.
RLS_desc_TA = {}
RLS_desc_TA['TA'] = "cover is opened(TA)"
RLS_desc_TA['ta'] = "trouble(TA) is recovered"
RLS_desc_TA['DM'] = "monitoring"


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
RLS_map_LA[''] =  0
RLS_map_LA['A1'] =  3
RLS_map_LA['A2'] =  4
RLS_map_LA['B1'] =  2
RLS_map_LA['B2'] =  1
RLS_map_LA['A11'] = 5
RLS_map_LA['A12'] = 6
RLS_map_LA['A21'] = 7
RLS_map_LA['A22'] = 8
RLS_map_LA['B11'] = 4
RLS_map_LA['B12'] = 3
RLS_map_LA['B21'] = 2
RLS_map_LA['B22'] = 1

if __name__ == '__main__':
	pass
