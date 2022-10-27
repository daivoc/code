#!/usr/bin/env python
# -*- coding: utf-8 -*-  

'''
- 라스터(이미지)데이터 배경에 백터(요소:펜스,카메라,)데이터를 사용한다.
- 추천하는 백터에디터는 [잉크스케이브] 또는 크롬기반의 [Your Graphic Designer]를 권한다.
- 주화면
	- 상단에 전 이벤트의 타임라인
	- 배경에 지도 표시
	- 전체 이벤트 로그 표시
- 이밴트 발생시 
	- 관련 카메라를 표시
	- 관련 백터 색변환
	- 상태로그 목록표시
- 펜스, 카메라
	- 선택시 관련정보 표시 : 1시간
	- 팬스 선택시 관련 카메라 표시
	- 카메라 선택시 정보표시 및 팝업 표시
	- 펜스별 24시간 타임라인 차트
- 로그
	- 데이터베이스 이벤트 로그 : 알람이벤트 만
	- event 파일로그 : IMS로 들어오는 모든 로그
		- /var/www/html/its_web/data/log/IMS/event/월일.event
	- 텍스트 파일로그 : 명령문 로그
		- /var/www/html/its_web/data/log/IMS/IMS.log
- 카메라뷰
	- PTZ 카메라인 경우 키보드조작에 따른 화면제어가능
	- 상,하,좌,우 키 화면이동
	- +,- 키 줌인 줌아웃
-  팝업이미지
	- 아이티에스로 부터 저장된 이미지 링크를 받아 표시됨
	- 화면 표시는 최대 32개이며
	- 32개 이후의 이미지는 과거 이미지를 밀어내며 32이미지를 유지
'''

import os
import time
import subprocess
import json
import MySQLdb
import logging
import logging.handlers
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

import socket
import fcntl
import struct

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

# 모니터링을 위한 지도파일을 생성한다.
def make_its_M_map():
	__script_jquery_js__ = '<script>'+open('%s/jquery/jquery-3.1.1.min.js' % cfg["path"]["common"], 'r').read()+'</script>'
	__script_jquery_ui_js__ = '<script>'+open('%s/jquery/ui/jquery-ui.js' % cfg["path"]["common"], 'r').read()+'</script>'
	__style_jquery_ui_css__ = '<style>'+open('%s/jquery/ui/jquery-ui.css' % cfg["path"]["common"], 'r').read()+'</style>'
	__svg_pan_zoom__ = '<script>'+open('%s/svg-pan-zoom/svg-pan-zoom.js' % cfg["path"]["common"], 'r').read()+'</script>'
	__smoothiecharts__ = '<script>'+open('%s/smoothiecharts/smoothie.js' % cfg["path"]["common"], 'r').read()+'</script>'
	
	## 보안상 차단한다.
	# __global_variables_ims__ = '<script>var cfg = ' + json.dumps(cfg) + ';</script>'
	__global_variables_ims__ = '<script>var ims = ' + json.dumps(ims) + ';</script>'
	__global_variables_icc__ = '<script>var icc = ' + json.dumps(icc) + ';</script>'
	
	## 실시간 센서 마지막 이벤트 테이블  
	__tbl_sensor__ = tbl_sensor(ims["sensor"]).encode('utf-8')
	
	## 카메라 테이블  
	__tbl_camera__ = tbl_camera(ims["camera"]).encode('utf-8')
	
	## 진단 테이블  
	if 'its' in ims['online']:
		__tbl_health__ = tbl_health(ims["online"]["its"]).encode('utf-8')
	else:
		__tbl_health__ = ""
		
	## IMS 자가진단 테이블 
	__tbl_health_ims__ = tbl_health_ims().encode('utf-8')
	# print __tbl_health_ims__

	## 바탕 이미지를 위한 SVG 
	svg_content = "%s%s"%(cfg["path"]["img"],cfg["file"]["svg_content"])
	if os.path.exists(svg_content):
		__svg_content__ = open(svg_content, 'r').read()
	else: # 기본 바탕 이미지
		__svg_content__ = '<svg x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve"> <path style="fill:#C7CFE2;" d="M503.129,291.485h-26.614c-5.804,0-10.947,12.562-14.178,31.96 c-2.098,12.592-13.095,21.779-25.856,22.134l-288.201,8.005v35.485l288.201,8.005c12.761,0.355,23.758,9.541,25.856,22.134 c3.232,19.398,8.374,31.96,14.178,31.96h26.614c4.899,0,8.871-3.972,8.871-8.871v-141.94 C512,295.457,508.028,291.485,503.129,291.485z"/> <rect x="148.283" y="300.358" style="fill:#C7CFE2;" width="53.227" height="44.356"/> <path style="fill:#C7CFE2;" d="M0.112,89.861L14.51,247.934c0.416,4.569,4.247,8.066,8.835,8.066h303.162 c4.589,0,8.42-3.5,8.835-8.069l14.343-158.079c1.414-15.583-10.857-29.019-26.505-29.019H26.616 C10.965,60.833-1.308,74.274,0.112,89.861z"/> <path style="fill:#E4EAF6;" d="M290.253,309.227H59.601c-9.799,0-17.742-7.943-17.742-17.742V114.06 c0-9.799,7.943-17.742,17.742-17.742h230.652c9.799,0,17.742,7.943,17.742,17.742v177.425 C307.996,301.284,300.052,309.227,290.253,309.227z"/> <path style="fill:#5B5D6E;" d="M245.863,256H103.992c-4.899,0-8.871-3.972-8.871-8.871v-88.712c0-4.899,3.972-8.871,8.871-8.871 h141.87c4.899,0,8.871,3.972,8.871,8.871v88.712C254.734,252.029,250.762,256,245.863,256z"/> <circle style="fill:#464655;" cx="174.93" cy="202.775" r="44.356"/> <path style="fill:#E4EAF6;" d="M476.515,291.485c-9.798,0-17.742,35.746-17.742,79.841c0,44.094,7.944,79.841,17.742,79.841h26.614 c4.899,0,8.871-3.972,8.871-8.871v-141.94c0-4.899-3.972-8.871-8.871-8.871H476.515z"/> <circle style="fill:#5B5D6E;" cx="174.93" cy="202.775" r="26.614"/> <circle style="fill:#FFFFFF;" cx="174.93" cy="202.775" r="8.871"/> <circle style="fill:#D7DEED;" cx="201.51" cy="176.161" r="17.742"/> <path style="fill:#FFFFFF;" d="M199.86,193.735c-2.687-7.405-8.519-13.226-15.927-15.905C184.734,186.283,191.403,192.944,199.86,193.735z"/> <path style="fill:#FFFFFF;" d="M201.507,158.416c-3.785,0-7.276,1.205-10.155,3.225c11.243,4.494,20.183,13.418,24.691,24.652 c2.01-2.876,3.207-6.36,3.207-10.134C219.249,166.359,211.305,158.416,201.507,158.416z"/> <path style="fill:#E4EAF6;" d="M174.893,415.682L174.893,415.682c-19.598,0-35.485-15.887-35.485-35.485v-35.485 c0-4.899,3.972-8.871,8.871-8.871h53.227c4.899,0,8.871,3.972,8.871,8.871v35.485C210.378,399.795,194.491,415.682,174.893,415.682z "/></svg>'
	
	with open(cfg["file"]["html_source"], 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()

		## 언어 설정 적용 - 예) "delete":["Delete","削除","삭제"],
		## 메모리 부담을 줄이기 위해 먼저 수행한다.
		## LANGUAGE Json 파일내의 표시될 이름 앞뒤를 '__'로 감싼다.
		for key in lan.keys():
			# print(key, ":", lan[key][0])
			tmp_its_tmp = tmp_its_tmp.decode("utf-8").replace('__%s__'%key,lan[key][cfg["language"]["selected"]]).encode("utf-8")

		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
		tmp_its_tmp = tmp_its_tmp.replace('__svg_pan_zoom__', __svg_pan_zoom__)
		tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
		tmp_its_tmp = tmp_its_tmp.replace('__global_variables_ims__', __global_variables_ims__)
		tmp_its_tmp = tmp_its_tmp.replace('__global_variables_icc__', __global_variables_icc__)
		tmp_its_tmp = tmp_its_tmp.replace('__tbl_sensor__', __tbl_sensor__)
		tmp_its_tmp = tmp_its_tmp.replace('__tbl_camera__', __tbl_camera__)
		tmp_its_tmp = tmp_its_tmp.replace('__tbl_health__', __tbl_health__)
		tmp_its_tmp = tmp_its_tmp.replace('__tbl_health_ims__', __tbl_health_ims__)
		tmp_its_tmp = tmp_its_tmp.replace('__svg_content__', __svg_content__)

		with open(cfg["file"]["html_target"], 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()
			
def kill_its_M_map(): 
	cmd = "pkill -9 -ef its_M_map 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return p
	
def kill_procOnvif(): 
	cmd = "pkill -9 -ef procOnvif 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return p
	
def kill_ipCamView(): 
	cmd = "pkill -9 -ef ipCamView 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return p
	
## 확인된 변수로 데몬을 실행 한다
def run_its_M_map(): 
	cmd = "node %s/its_M_map.js 2>&1 & " % (cfg["path"]["monitor"])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

## 확인된 변수로 데몬을 실행 한다
def run_procOnvif(camID): 
	cmd = "node %s/procOnvif.js %s 2>&1 & " % (cfg["path"]["monitor"], camID)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p
	
def run_ipCamView(): 
	cmd = "node %s/ipCamView.js 2>&1 & " % (cfg["path"]["monitor"])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p
	
## 확인된 변수로 데몬을 실행 한다
def run_ipCamInfo(): 
	cmd = "node %s/ipCamInfo.js 2>&1 & " % (cfg["path"]["monitor"])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p

## 환경설정 파일(JSON) 읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(cfg,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(cfg, json_file, sort_keys=True, indent=4)

## 데이터베이스 관련
def create_table_w_log_IMS_data():
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		query = """
			CREATE TABLE IF NOT EXISTS %s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_gr` int(11) NOT NULL DEFAULT '0',
			`w_ca` int(11) NOT NULL DEFAULT '0',
			`w_sensorId` varchar(64) NULL DEFAULT '',
			`w_sensorName` varchar(64) NULL DEFAULT '',
			`w_userName` varchar(32) NULL DEFAULT '',
			`w_shot` varchar(255) NULL DEFAULT '', 
			`w_action` tinyint(4) NOT NULL DEFAULT '0',
			`w_description` varchar(64) NULL DEFAULT '', 
			`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (`w_id`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % cfg["table"]["imsData"]
		cursor.execute(query) # create table
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
 	except MySQLdb.Warning as warning:
		pass
	finally:
		cursor.close()
		conn.close()
		
def create_table_w_log_IMS_key():
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		query = """
			CREATE TABLE IF NOT EXISTS %s (
			`w_id` int(11) NOT NULL AUTO_INCREMENT,
			`w_sensorId` varchar(64) NULL DEFAULT '',
			PRIMARY KEY (`w_id`), UNIQUE (`w_sensorId`)
			) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
			""" % cfg["table"]["imsKey"]
		cursor.execute(query) # create table
		conn.commit()
		return cursor.lastrowid
	except MySQLdb.Error as error:
		print(error)
 	except MySQLdb.Warning as warning:
		pass
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_imsKey(): ##
	query = "SELECT * FROM " + cfg["table"]["imsKey"] 
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()

def read_table_w_cfg_cameraID(): ##
	query = "SELECT * FROM " + cfg["table"]["camera"] + " WHERE w_camera_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def read_table_w_cfg_zoneID(): ##
	query = "SELECT * FROM " + cfg["table"]["zone"] + " WHERE w_zone_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def read_table_w_cfg_boxID(): ##
	query = "SELECT * FROM " + cfg["table"]["box"] + " WHERE w_box_disable = 0" + " ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return '' ## 오류발생시 
		print(error)
	finally:
		cursor.close()
		conn.close()
		
def itsMemberConfig(field, id): ## 사용자 its의 특정필드 내용 확인
	query = "SELECT " + field + " FROM g5_member WHERE mb_id = '" + id + "'" 
	try:
		conn = MySQLdb.connect(host=cfg["mysql"]["host"], user=cfg["mysql"]["user"], passwd=cfg["mysql"]["pass"], db=cfg["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchone() 
	except MySQLdb.Error as error:
		return 0
	finally:
		cursor.close()
		conn.close()

def tbl_sensor(sns):
	result = ''
	for key in sns: # key는 센서 시리얼
		# result += "<table> <tr> <td colspan=4>%s</td> </tr> <tr> <td colspan=4>BBB</td> </tr> <tr> <td>A</td> <td>B</td> <td>C</td> <td>D</td> </tr> </table>" % sns[key]['subj']
		result += "<div class='group' id='tbl_"+key+"'> <div class='title'>%s</div> <div class='model'>%s</div> <div class='times'>-</div> <div class='event'> <span class='a'>A</span> <span class='b'>H</span> <span class='c'>E</span> <span class='d'>e</span> </div> </div>" % (sns[key]['subj'], sns[key]['model'])
	return result
	
def tbl_camera(cam):
	result = ''
	for key in cam: # key는 카메라 시리얼
		# result += "<table> <tr> <td colspan=4>%s</td> </tr> <tr> <td colspan=4>BBB</td> </tr> <tr> <td>A</td> <td>B</td> <td>C</td> <td>D</td> </tr> </table>" % cam[key]['subj']
		result += "<div class='group' id='tbl_"+key+"'> <div class='title'>%s</div> <div class='model'>%s</div> <div class='times'>-</div> <div class='event'> <span class='a'>A</span> <span class='b'>B</span> <span class='c'>C</span> <span class='d'>D</span> </div> </div>" % (cam[key]['subj'], cam[key]['model'])
	return result

def tbl_health(its):
	result = ''
	event = '''
<div class="wdWrap">
	<div class="wdName">cpu</div>
	<div class="wdStatus">
	<hr class="idle" style="width:80%;background-color:orangered;" title="">
	<hr class="idleOv wdLeftover" title="">
	</div>
</div>
<div class="wdWrap">
	<div class="wdName">disk</div>
	<div class="wdStatus">
	<hr class="disk" style="width:80%;background-color:darkorange;" title="">
	<hr class="diskOv wdLeftover" title="">
	</div>
</div>
<div class="wdWrap">
	<div class="wdName">mem</div>
	<div class="wdStatus">
	<hr class="mem" style="width:80%;background-color:blueviolet;" title="">
	<hr class="memOv wdLeftover" title="">
	</div>
</div>
<div class="wdWrap">
	<div class="wdName">swap</div>
	<div class="wdStatus">
	<hr class="swap" style="width:80%;background-color:deepskyblue;" title="">
	<hr class="swapOv wdLeftover" title="">
	</div>
</div>
<div class="wdWrap">
	<div class="wdName">temp</div>
	<div class="wdStatus">
	<hr class="temp" style="width:80%;background-color:forestgreen;" title="">
	<hr class="tempOv wdLeftover" title="">
	</div>
</div>

'''	
	for key in its: # key는 아이티에스 IP Addr임
		keyID = "wd_%s"%key.replace(".", "_")
		# result += "<table> <tr> <td colspan=4>%s</td> </tr> <tr> <td colspan=4>BBB</td> </tr> <tr> <td>A</td> <td>B</td> <td>C</td> <td>D</td> </tr> </table>" % cam[key]['subj']
		result += "<div class='group' id='"+keyID+"'> <div class='title'>"+key+"</div> <div class='model'>-</div> <div class='times'>-</div> <div class='event'>"+event+"</div> </div>"
	return result

def tbl_health_ims():
	if ims['guiConfig']['wdServer'] == ims['imsIP']:
		event = '''
			<div class="wdWrap">
				<div class="wdName">cpu</div>
				<div class="wdStatus">
				<hr class="idle" style="width:80%;background-color:orangered;" title="">
				<hr class="idleOv wdLeftover" title="">
				</div>
			</div>
			<div class="wdWrap">
				<div class="wdName">disk</div>
				<div class="wdStatus">
				<hr class="disk" style="width:80%;background-color:darkorange;" title="">
				<hr class="diskOv wdLeftover" title="">
				</div>
			</div>
			<div class="wdWrap">
				<div class="wdName">mem</div>
				<div class="wdStatus">
				<hr class="mem" style="width:80%;background-color:blueviolet;" title="">
				<hr class="memOv wdLeftover" title="">
				</div>
			</div>
			<div class="wdWrap">
				<div class="wdName">swap</div>
				<div class="wdStatus">
				<hr class="swap" style="width:80%;background-color:deepskyblue;" title="">
				<hr class="swapOv wdLeftover" title="">
				</div>
			</div>
			<div class="wdWrap">
				<div class="wdName">temp</div>
				<div class="wdStatus">
				<hr class="temp" style="width:80%;background-color:forestgreen;" title="">
				<hr class="tempOv wdLeftover" title="">
				</div>
			</div>
			<div class="wdWrap">
				<div class="wdName">live</div>
				<div class="wdStatus times"></div>
			</div>
		'''	
		keyID = "wd_%s"%ims['guiConfig']['wdServer'].replace(".", "_")
		result = "<div class='tbl_health_ims' id='"+keyID+"'>"+event+"</div>"
	else:
		result = ""

	return result

def ipPortParse(content):
	## content = 'root||password||192.168.0.10||1234||Opt1||Opt2'
	try:
		elements = content.split('||') 
		connectInfo = {
				'user':elements[0],
				'pass':elements[1],
				'host':elements[2],
				'port':int(elements[3]),
				'opt1':elements[4],
				'opt2':elements[5]
			}
		return connectInfo
	except:
		# return "requests.get Error: %s" % url
		return 0

def serNameParse(content):
	## content = 'g500t300_192_168_0_103_0002'
	try:
		elements = content.split('_') 
		connectInfo = {
				'table':elements[0],
				'ipAddr':"%s.%s.%s.%s"%(elements[1],elements[2],elements[3],elements[4]),
				'record':elements[5]
			}
		return connectInfo
	except:
		return 0
			
if __name__ == '__main__':
	## 확인된 변수로 데몬을 실행 한다
	kill_procOnvif()
	kill_its_M_map()
	kill_ipCamView()
	###############################################
	## 파일 config.json내용을 사용자 변수로 선언
	## 예: print cfg["file"]["html_src"]
	## 예: print cfg["mysql"]["db_host"]
	cfg = readConfig('/home/pi/MONITOR/config.json') # '/home/pi/MONITOR/%s.json'
	icc = readConfig('/home/pi/MONITOR/camera.json')
	lan = readConfig('/home/pi/MONITOR/language.json')
	
	############ logging ################
	# 로그 파일 초기화 참고:  http://gyus.me/?p=418
	if not os.path.exists(cfg["path"]["log"]): # /var/www/html/its_web/data/log
		os.makedirs(cfg["path"]["log"])
		os.chmod(cfg["path"]["log"],0o777)
	if not os.path.exists(cfg["path"]["log"]+cfg["path"]["home"]): # /var/www/html/its_web/data/log/ims
		os.makedirs(cfg["path"]["log"]+cfg["path"]["home"])
		os.chmod(cfg["path"]["log"]+cfg["path"]["home"],0o777)
	if not os.path.exists(cfg["path"]["log"]+cfg["path"]["event"]): # /var/www/html/its_web/data/log/ims/event
		os.makedirs(cfg["path"]["log"]+cfg["path"]["event"])
		os.chmod(cfg["path"]["log"]+cfg["path"]["event"],0o777)
	logger = logging.getLogger(cfg["path"]["home"][1:]) # 로거 인스턴스를 만든다
	fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s') # 포매터를 만든다
	loggerLevel = logging.DEBUG
	filename = cfg["path"]["log"]+cfg["path"]["home"]+cfg["path"]["home"]+'.log'
	fileMaxByte = 1024 * 1024 * 10 # 10MB - 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
	fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=fileMaxByte, backupCount=10) # fileMaxByte(10M) 10개 까지
	streamHandler = logging.StreamHandler()
	fileHandler.setFormatter(fomatter) # 각 핸들러에 포매터를 지정한다.
	streamHandler.setFormatter(fomatter)
	os.chmod(filename,0o777)
	logger.addHandler(fileHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# logger.addHandler(streamHandler) # 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
	# 로거 인스턴스 로그 예
	logger.setLevel(loggerLevel)
	logger.info("START")
	# logger.debug("===========================")
	# logger.info("TEST START")
	# logger.warning("파일 명과 로깅 레벨을 각각 환경마다 다르게 남도록 했어요.")
	# logger.debug("디버그 로그는 테스트 환경과 로컬 피씨에서남 남는 답니다.")
	# logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
	# logger.debug("===========================")
	# logger.info("TEST END!")
	############ logging ################
	
	## 로그테이블 생성
	create_table_w_log_IMS_data()
	# create_table_w_log_IMS_key(); ## w_optex_FENCE에서 사전에 생성 한다.
	
	ims = {} ## 전역변수
	
	ims['file'] = cfg['file'].copy() # 
	ims['systemCmd'] = cfg['systemCmd'].copy() # 
	ims['userCmd'] = cfg['userCmd'].copy() # 
	ims['runProgram'] = cfg['runProgram'].copy()
	ims['groupLayer'] = cfg['groupLayer'].copy()
	ims['guiScreen'] = cfg['guiScreen'].copy()
	ims['itsApi'] = cfg['itsApi'].copy() # 

	ims['guiConfig'] = {}
	ims["guiConfig"]["wdServer"] = itsMemberConfig('mb_3','manager')['mb_3']

	# IMS IP - 자신의 실제 아이피
	# its_iface = str(cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $8}' 2>/dev/null")).strip()
	its_iface = str(cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null")).strip()
	ims['imsIP'] = get_ip_address(its_iface).strip()

	if ims['imsIP']:
		print ("\nSystem IP:{}".format(ims['imsIP']))
	else:
		exit("Error Network Interface:{}".format(ims['imsIP']))

	## 커스텀 로고가 없으면 옵텍스 로고로 대치한다.
	image_dir = "%s/data/image"%(cfg["path"]["its_web"])
	if not os.path.exists(image_dir): # /var/www/html/its_web/data/image
		os.makedirs(image_dir)
		os.chmod(image_dir,0o707)
	
	image_ims_dir = "%s/data/image/ims"%(cfg["path"]["its_web"])
	if not os.path.exists(image_ims_dir): # /var/www/html/its_web/data/image/ims
		os.makedirs(image_ims_dir)
		os.chmod(image_ims_dir,0o707)
	
	img_customLogo = "%s%s"%(cfg["path"]["its_web"],cfg["file"]["img_customLogo"])
	if os.path.exists(img_customLogo):
		ims["file"]["img_currentLogo"] = cfg["file"]["img_customLogo"]
	else:
		ims["file"]["img_currentLogo"] = cfg["file"]["img_optexLogo"]

	## 센서 관련 정보 수집
	ims['sensor'] = {} ## sensor group
	## 카메라 관련 정보 수집
	ims['camera'] = {} ## camera group
	## 존 관련 정보 수집
	ims['zone'] = {} ## zone group
	## 함체 관련 정보 수집
	ims['box'] = {} ## box group
	## 맵 관련 정보 수집
	ims['map'] = {} ## map group
	## Online Test 관련 정보 수집
	ims['online'] = {} ## online group
	
	audioName = itsMemberConfig('mb_2', 'its')
	audioTime = itsMemberConfig('mb_3', 'its')

	## 오디오 출력파일 정보(Global)
	ims['audioName'] = audioName['mb_2']
	if audioTime['mb_3']:
		ims['audioTime'] = float(audioTime['mb_3'])
	else:
		ims['audioTime'] = 0

	relayAddr = itsMemberConfig('mb_5', 'its')
	relayPort = itsMemberConfig('mb_6', 'its')
	relayNumber = itsMemberConfig('mb_7', 'its')

	ims['relayAddr'] = relayAddr['mb_5']
	
	## 릴레이 출력파일 정보(Global) - 경광등 ..
	if relayPort['mb_6']:	
		ims['relayPort'] = int(relayPort['mb_6'])
	else:
		ims['relayPort'] = 0
	
	if relayNumber['mb_7']:	
		ims['relayNumber'] = int(relayNumber['mb_7'])
	else:
		ims['relayNumber'] = 0

	## Sensor 정보 수집
	for row in read_table_w_cfg_zoneID():
		if row['w_sns_0']: ## Zone에 링크된 센서아이디값이 존재 하면
			sensorID = row['w_sns_0']
			if not sensorID in ims['sensor']:
				ims['sensor'][sensorID] = {}
			ims['sensor'][sensorID]['group'] = row['wr_id']
			ims['sensor'][sensorID]['cate'] = int(sensorID[1:4]+sensorID[5:8])
			ims['sensor'][sensorID]['subj'] = row['wr_subject']
			ims['sensor'][sensorID]['desc'] = row['w_zone_desc']
			ims['sensor'][sensorID]['model'] = row['w_zone_model']
			ims['sensor'][sensorID]['mapID'] = row['w_map_id']
			ims['sensor'][sensorID]['boxID'] = row['w_box_id']
			ims['sensor'][sensorID]['zoneID'] = row['w_zone_serial']
			ims['sensor'][sensorID]['iFrame'] = row['w_iFrame']
			
			if row['wr_2'] and row['wr_3']: ## 선언한 오디오 파일이 없으면 공용오디오로 대치함
				ims['sensor'][sensorID]['audioName'] = row['wr_2']
				ims['sensor'][sensorID]['audioTime'] = float(row['wr_3'])
			elif ims['audioName'] and ims['audioTime']:
				ims['sensor'][sensorID]['audioName'] = ims['audioName']
				ims['sensor'][sensorID]['audioTime'] = ims['audioTime']
			else:
				ims['sensor'][sensorID]['audioName'] = ""
				ims['sensor'][sensorID]['audioTime'] = 0
			
			if row['wr_5'] and row['wr_6'] and row['wr_7']:
				ims['sensor'][sensorID]['relayAddr'] = row['wr_5']
				ims['sensor'][sensorID]['relayPort'] = int(row['wr_6'])
				ims['sensor'][sensorID]['relayNumber'] = int(row['wr_7'])
			elif ims['relayAddr'] and ims['relayPort'] and ims['relayNumber']:
				ims['sensor'][sensorID]['relayAddr'] = ims['relayAddr']
				ims['sensor'][sensorID]['relayPort'] = ims['relayPort']
				ims['sensor'][sensorID]['relayNumber'] = ims['relayNumber']
			else:
				ims['sensor'][sensorID]['relayAddr'] = ""
				ims['sensor'][sensorID]['relayPort'] = 0
				ims['sensor'][sensorID]['relayNumber'] = 0

			ims['sensor'][sensorID]['preset'] = {}
			ims['sensor'][sensorID]['camera'] = []
			for j in range(4): ## ims['camera']내에 값입력
				if row['w_cam_'+str(j)]: ## 센서 아이디 값이 존재 하면
					ims['sensor'][sensorID]['camera'].append(row['w_cam_'+str(j)])
					
					if row['w_ptz_'+str(j)]: ## 센서 프리셋 값이 존재 하면
						ims['sensor'][sensorID]['preset'][row['w_cam_'+str(j)]] = row['w_ptz_'+str(j)]
	
	# ## Zone 정보 수집
	# for row in read_table_w_cfg_zoneID():
		zoneID = row['w_zone_serial']
		if not zoneID in ims['zone']:
			ims['zone'][zoneID] = {}
			
		ims['zone'][zoneID]['group'] = row['wr_id']
		ims['zone'][zoneID]['cate'] = int(zoneID[1:4]+zoneID[5:8]) ## 500200 <-- g500t200_192_168_0_103_0020
		ims['zone'][zoneID]['subj'] = row['wr_subject']
		ims['zone'][zoneID]['desc'] = row['w_zone_desc']
		ims['zone'][zoneID]['mapID'] = row['w_map_id']
		ims['zone'][zoneID]['boxID'] = row['w_box_id']

		if row['wr_2'] and row['wr_3']: ## 선언한 오디오 파일이 없으면 공용오디오로 대치함
			ims['zone'][zoneID]['audioName'] = row['wr_2']
			ims['zone'][zoneID]['audioTime'] = float(row['wr_3'])
		elif ims['audioName'] and ims['audioTime']:
			ims['zone'][zoneID]['audioName'] = ims['audioName']
			ims['zone'][zoneID]['audioTime'] = ims['audioTime']
		else:
			ims['zone'][zoneID]['audioName'] = ""
			ims['zone'][zoneID]['audioTime'] = 0
		
		if row['wr_5'] and row['wr_6'] and row['wr_7']:
			ims['zone'][zoneID]['relayAddr'] = row['wr_5']
			ims['zone'][zoneID]['relayPort'] = int(row['wr_6'])
			ims['zone'][zoneID]['relayNumber'] = int(row['wr_7'])
		elif ims['relayAddr'] and ims['relayPort'] and ims['relayNumber']:
			ims['zone'][zoneID]['relayAddr'] = ims['relayAddr']
			ims['zone'][zoneID]['relayPort'] = ims['relayPort']
			ims['zone'][zoneID]['relayNumber'] = ims['relayNumber']
		else:
			ims['zone'][zoneID]['relayAddr'] = ""
			ims['zone'][zoneID]['relayPort'] = 0
			ims['zone'][zoneID]['relayNumber'] = 0

		ims['zone'][zoneID]['preset'] = {}
		ims['zone'][zoneID]['pSetOn'] = {}
		ims['zone'][zoneID]['camera'] = []
		for j in range(4): ## ims['camera']내에 값입력
			if row['w_cam_'+str(j)]: ## 센서 아이디 값이 존재 하면
				ims['zone'][zoneID]['camera'].append(row['w_cam_'+str(j)])
				
				if row['w_ptz_'+str(j)]: ## 센서 프리셋 값이 존재 하면
					ims['zone'][zoneID]['preset'][row['w_cam_'+str(j)]] = row['w_ptz_'+str(j)]
					ims['zone'][zoneID]['pSetOn'][row['w_cam_'+str(j)]] = row['w_ptzOn_'+str(j)]
					
		if not row['w_map_id'] in ims['map']:
			ims['map'][row['w_map_id']] = {}
		ims['map'][row['w_map_id']]['group'] = 'zone'
		ims['map'][row['w_map_id']]['imsId'] = row['w_zone_serial']
		ims['map'][row['w_map_id']]['itsId'] = row['w_sns_0']
	
	# ## Online 정보 수집
	# 가독성 관계로 위의 센서정보 수집과 분리함
	# for row in read_table_w_cfg_zoneID():
		if row['w_sns_0']: ## Zone에 링크된 센서아이디값이 존재 하면
			onlineID = serNameParse(row['w_sns_0'])['ipAddr']
			if not 'its' in ims['online']:
				ims['online']['its'] = {}
				
			if not onlineID in ims['online']['its']:
				ims['online']['its'][onlineID] = {}
			
			ims['online']['its'][onlineID]['port'] = 80
				
			## 함체(박스)
			if row['w_box_id']:
				ims['online']['its'][onlineID]['boxID'] = row['w_box_id']
				
			## 센서
			if not 'senID' in ims['online']['its'][onlineID]:
				ims['online']['its'][onlineID]['senID'] = [] ## 아이피에 관계된 Zone ID Group 
			if row['w_sns_0']:
				ims['online']['its'][onlineID]['senID'].append(row['w_sns_0']) 
			
			## 지역(Zone)
			if not 'zoneID' in ims['online']['its'][onlineID]:
				ims['online']['its'][onlineID]['zoneID'] = [] ## 아이피에 관계된 Zone ID Group 
			if row['w_zone_serial']:
				ims['online']['its'][onlineID]['zoneID'].append(row['w_zone_serial']) 
						
			## 카메라
			if not 'camID' in ims['online']['its'][onlineID]:
				ims['online']['its'][onlineID]['camID'] = [] ## 아이피에 관계된 Camera Group
			if row['w_cam_0']:
				ims['online']['its'][onlineID]['camID'].append(row['w_cam_0']) 
			if row['w_cam_1']:
				ims['online']['its'][onlineID]['camID'].append(row['w_cam_1']) 
			if row['w_cam_2']:
				ims['online']['its'][onlineID]['camID'].append(row['w_cam_2']) 
			if row['w_cam_3']:
				ims['online']['its'][onlineID]['camID'].append(row['w_cam_3']) 				
	
	## 함체 정보 수집
	for row in read_table_w_cfg_boxID():
		boxID = row['w_box_serial']
		if not boxID in ims['box']:
			ims['box'][boxID] = {}
			
		ims['box'][boxID]['group'] = row['wr_id']
		ims['box'][boxID]['cate'] = int(boxID[1:4]+boxID[5:8])
		ims['box'][boxID]['subj'] = row['wr_subject']
		ims['box'][boxID]['desc'] = row['w_box_desc']
		ims['box'][boxID]['mapID'] = row['w_map_id']
		ims['box'][boxID]['iFrame'] = row['w_iFrame']

		if row['wr_2'] and row['wr_3']: ## 선언한 오디오 파일이 없으면 공용오디오로 대치함
			ims['box'][boxID]['audioName'] = row['wr_2']
			ims['box'][boxID]['audioTime'] = float(row['wr_3'])
		elif ims['audioName'] and ims['audioTime']:
			ims['box'][boxID]['audioName'] = ims['audioName']
			ims['box'][boxID]['audioTime'] = ims['audioTime']
		else:
			ims['box'][boxID]['audioName'] = ""
			ims['box'][boxID]['audioTime'] = 0
		
		if row['wr_5'] and row['wr_6'] and row['wr_7']:
			ims['box'][boxID]['relayAddr'] = row['wr_5']
			ims['box'][boxID]['relayPort'] = int(row['wr_6'])
			ims['box'][boxID]['relayNumber'] = int(row['wr_7'])
		elif ims['relayAddr'] and ims['relayPort'] and ims['relayNumber']:
			ims['box'][boxID]['relayAddr'] = ims['relayAddr']
			ims['box'][boxID]['relayPort'] = ims['relayPort']
			ims['box'][boxID]['relayNumber'] = ims['relayNumber']
		else:
			ims['box'][boxID]['relayAddr'] = ""
			ims['box'][boxID]['relayPort'] = 0
			ims['box'][boxID]['relayNumber'] = 0
		
		## Target IP에 필요한 시스템으로 이벤트 정보(IP, Port)
		ims['box'][boxID]['customIpPort'] = []
		newIpPort = ipPortParse(row['wr_8'])
		if newIpPort: 
			ims['box'][boxID]['customIpPort'].append(newIpPort)
		newIpPort = ipPortParse(row['wr_9'])
		if newIpPort: 
			ims['box'][boxID]['customIpPort'].append(newIpPort)

		ims['box'][boxID]['preset'] = {}
		ims['box'][boxID]['camera'] = []
		for j in range(4): ## ims['camera']내에 값입력
			if row['w_cam_'+str(j)]: ## 센서 아이디 값이 존재 하면
				ims['box'][boxID]['camera'].append(row['w_cam_'+str(j)])
				
				if row['w_ptz_'+str(j)]: ## 센서 프리셋 값이 존재 하면
					ims['box'][boxID]['preset'][row['w_cam_'+str(j)]] = row['w_ptz_'+str(j)]
					
		if not row['w_map_id'] in ims['map']:
			ims['map'][row['w_map_id']] = {}
		ims['map'][row['w_map_id']]['group'] = 'box'
		ims['map'][row['w_map_id']]['imsId'] = row['w_box_serial']
		ims['map'][row['w_map_id']]['itsId'] = ''

	## 카메라 정보 수집
	for row in read_table_w_cfg_cameraID():
		ims['camera'][row['w_camera_serial']] = {}
		ims['camera'][row['w_camera_serial']]['subj'] = row['wr_subject']
		ims['camera'][row['w_camera_serial']]['desc'] = row['w_camera_desc']
		ims['camera'][row['w_camera_serial']]['model'] = row['w_camera_model']
		ims['camera'][row['w_camera_serial']]['mapID'] = row['w_map_id']
		ims['camera'][row['w_camera_serial']]['boxID'] = row['w_box_id']
		ims['camera'][row['w_camera_serial']]['user'] = row['w_camera_user']
		ims['camera'][row['w_camera_serial']]['pass'] = row['w_camera_pass']
		ims['camera'][row['w_camera_serial']]['addr'] = row['w_camera_addr']
		ims['camera'][row['w_camera_serial']]['port'] = row['w_camera_port']
		ims['camera'][row['w_camera_serial']]['hash'] = row['w_camera_hash']
		
		ims['camera'][row['w_camera_serial']]['camPort'] = cfg["interface"]["camPort"] + row['wr_id']

		if row['w_url1']:
			## 이미지 스크린 샷.
			image_link = "http://"+row['w_camera_addr']+row['w_url1']
		elif row['w_url3']:	
			image_link = row['w_url3']
		else:
			image_link = ""
		ims['camera'][row['w_camera_serial']]['image'] = image_link
		
		if row['w_url2']:
			## 라이브 비디오
			video_link = "http://"+row['w_camera_addr']+row['w_url2']
		elif row['w_url4']:	
			video_link = row['w_url4']
		else:	
			video_link = ""
		ims['camera'][row['w_camera_serial']]['video'] = video_link
		
		ims['camera'][row['w_camera_serial']]['resolution'] = {}
		ims['camera'][row['w_camera_serial']]['resolution']['x'] = row['w_camera_px_X']
		ims['camera'][row['w_camera_serial']]['resolution']['y'] = row['w_camera_px_Y']

		if not row['w_map_id'] in ims['map']:
			ims['map'][row['w_map_id']] = {}
		ims['map'][row['w_map_id']]['group'] = 'camera'
		ims['map'][row['w_map_id']]['imsId'] = row['w_camera_serial']
		ims['map'][row['w_map_id']]['itsId'] = ''

	
	# ## Online 정보 수집
	# for row in read_table_w_cfg_cameraID():
		if row['w_camera_addr']: ## 카메라 IP 값이 존재 하면
			onlineID = row['w_camera_addr']
			if not 'cam' in ims['online']:
				ims['online']['cam'] = {}
			if not onlineID in ims['online']:
				ims['online']['cam'][onlineID] = {}
			if row['w_camera_port']:
				ims['online']['cam'][onlineID]['port'] = row['w_camera_port']
			else:
				ims['online']['cam'][onlineID]['port'] = 80

	###############################################
	## 파일 config.json내용 저장
	saveConfig(ims,cfg["path"]["monitor"]+'/cfgIms.json') ## 저장
	
	make_its_M_map() # index.html 생성후 SVG 파일 적용
	
	run_its_M_map() # IMS 구동
	
	## 플러그인
	if(cfg["runProgram"]["procOnvif"]): # 카메라 수만큼의 온비프 인터페이스 프로그램을 실행
		for camID in ims['camera'].keys():
			if icc[ims['camera'][camID]['model']]['isPTZ']: # 카메라 목록에서 PTZ 기능인 확인
				print("ID:{} IP:{} Model:{}".format(camID, ims['camera'][camID]['addr'], ims['camera'][camID]['model']))
				run_procOnvif(camID)
				
	if(cfg["runProgram"]["ipCamInfo"]): # Onvif 정보 생산을 위해 등록된 카메라정보(camera.json: Account Info) 읽어들임
		run_ipCamInfo()
		print('Running run_ipCamInfo')
		
	if(cfg["runProgram"]["ipCamView"]): # 지역정보(Zone) 등록시 카메라 PTZ 값을 읽어드리는 기능
		run_ipCamView()
		print('Running run_ipCamView')

	# print('Running nodeJs')
	exit()