#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
API
pip3 install websockets
'''
# from distutils.command.config import config
import os
import json
import time
import math
from pickle import TRUE
import subprocess
import pymysql
import requests
from requests.auth import HTTPDigestAuth
import asyncio
import websockets

def requestApi(command, method):
	try:
		if method == "get":
			# response = requests.get(command.format(config["sensor"]["addr"]), auth=HTTPDigestAuth(config["sensor"]["user"], config["sensor"]["pass"]))
			response = requests.get("http://{}{}".format(config["sensor"]["addr"],command), auth=HTTPDigestAuth(config["sensor"]["user"], config["sensor"]["pass"]))
		elif method == "post":
			# response = requests.post(command.format(config["sensor"]["addr"]), auth=HTTPDigestAuth(config["sensor"]["user"], config["sensor"]["pass"]))
			response = requests.post("http://{}{}".format(config["sensor"]["addr"],command), auth=HTTPDigestAuth(config["sensor"]["user"], config["sensor"]["pass"]))
		else:
			return 2, "Unknow Methode"

		if response.status_code == 200:
			return 0, response.json()
		else:
			return 1, response.status_code
	except:
		return 3, "Unknow Error"
async def webSocketApi(command, data):
	try:
		async with websockets.connect("ws://{}{}".format(config["sensor"]["addr"],command)) as ws:
			await ws.send(json.dumps(data))
			try:
				response = await ws.recv()
				return 0, json.loads(response)
			except:
				return 1, "Except: recv"
	except:
		return 2, "Except: websockets.connect"

def get_interface(): # return 'eth0'
	return cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null").strip().decode()
	 
# 자신 아이피 확인 
def get_ip_address(iface): # get_ip_address(get_interface())
	return cmd_proc_Popen("ifconfig "+iface+" | grep 'inet ' | cut -d: -f2 | awk '{print $2}'").strip().decode()

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)

def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def kill_demon_JS(): 
	cmd = "pkill -9 -ef ./realtime_RLS.js 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	cmd = "pkill -9 -ef ./setup.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

def kill_demon_RLS3(): 
	cmd = "pkill -9 -ef ./RLS3.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

def kill_demon_setup(): 
	cmd = "pkill -9 -ef ./setup.pyc 2>&1" 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)

# 확인된 변수로 데몬을 실행 한다
def run_demon_RLS3(): 
	cmd = "python3 ./RLS3.pyc 2>&1 & "
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def run_demon_setup(): 
	cmd = "python3 ./setup.pyc 2>&1 & "
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def isTableExist(tableName): ###################### Optex REDSCAN
	query = "SELECT * FROM information_schema.tables WHERE table_schema = '"+config["mysql"]["name"]+"' AND table_name = '"+tableName+"' LIMIT 1;"
	try:
		conn = pymysql.connect(host=config["mysql"]["host"], user=config["mysql"]["user"], passwd=config["mysql"]["pass"], db=config["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute(query)
		result = cursor.fetchone()
		if result: # 테이블이 존재 하면
			return 0
		else: # 테이블이 존재 하지 않으면
			return 1
	except pymysql.Error as error:
		print(error)
 	# except pymysql.Warning as warning:
	else:
		pass
	finally:
		cursor.close()
		conn.close()

def create_table_w_log_RLS_V(): # create_table_w_log(uniqueOfSensor)
	try:
		# 데이타베이스 연결 Open database connection
		conn = pymysql.connect(host=config["mysql"]["host"], user=config["mysql"]["user"], passwd=config["mysql"]["pass"], db=config["mysql"]["name"], charset='utf8', use_unicode=True) 
		cursor = conn.cursor()
		# 기존 테이 삭제 후 생성 Drop table if it already exist using execute() method.
		# cursor.execute("DROP TABLE IF EXISTS w_log_sensor")
		tableName = config["mysql"]["table"]["log"]
		'''
		[INFO|RLS3.py:167] 2022-09-13 21:46:44,327 > {'id': 5, 'kind': 'detected', 'initialPos': {'x': 2071, 'y': 5468}, 'currentPos': {'x': 2069, 'y': 5463}, 'distance': 5842, 'step': 297, 'size': 896}
		[INFO|RLS3.py:167] 2022-09-13 21:46:44,495 > {'id': 0, 'kind': 'detected', 'initialPos': {'x': -3988, 'y': 4276}, 'currentPos': {'x': -4000, 'y': 4290}, 'distance': 5866, 'step': 552, 'size': 102}
		[INFO|RLS3.py:167] 2022-09-13 21:46:44,500 > {'id': 1, 'kind': 'detected', 'initialPos': {'x': -3982, 'y': 4662}, 'currentPos': {'x': -3943, 'y': 4658}, 'distance': 6104, 'step': 541, 'size': 158}

		Level:Alert ID:5648-793 key:B1-724_158 Size:446mm Keep:True Set#:8 Cur#:8th
		Level:Warning ID:5474-2074 key:C2-821_156 Size:100mm Keep:True Set#:12 Cur#:12th
		Level:Alert ID:5648-793 key:B1-724_158 Size:446mm Keep:True Set#:8 Cur#:8th
		'''		
		if isTableExist(tableName):
			tbl_w_log_sensor_sql = """
				CREATE TABLE IF NOT EXISTS %s (
				`w_id` int(11) NOT NULL AUTO_INCREMENT,
				`kind` varchar(16) NULL DEFAULT '',
				`initialPosX` int NOT NULL DEFAULT '0',
				`initialPosY` int NOT NULL DEFAULT '0',
				`currentPosX` int NOT NULL DEFAULT '0',
				`currentPosY` int NOT NULL DEFAULT '0',
				`distance` int NOT NULL DEFAULT '0',
				`step` int NOT NULL DEFAULT '0',
				`size` int NOT NULL DEFAULT '0',
				`zone` varchar(3) NULL DEFAULT '',
				`level` int NOT NULL DEFAULT '0',
				`count` int NOT NULL DEFAULT '0',
				`w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				PRIMARY KEY (`w_id`)
				) ENGINE=MyISAM DEFAULT CHARSET=utf8;
				""" % tableName
			cursor.execute(tbl_w_log_sensor_sql) # create table
			conn.commit()
			return cursor.lastrowid
	except pymysql.Error as error:
		print(error)
 	# except pymysql.Warning as warning:
	else:
		pass
	finally:
		cursor.close()
		conn.close()

def MASQUERADE(active,ip,port):
	if active:
		# 연결 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(port, ip)
	else:
		# 차단 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		sudo iptables -D FORWARD -i eth0 -j ACCEPT
		sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE
		sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(port, ip)
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return (active, ip, port)

def makeHtml(type_RLS): 
	#################################################
	## 바탕화면 크기 설정

	if type_RLS == "RLS-3060V" or type_RLS == "RLS-50100V":
		width = config["model"][type_RLS]["size"] # 80000
		height = config["model"][type_RLS]["size"] # 80000
		start_x = -(config["model"][type_RLS]["size"]) # -80000
		start_y = -int(config["model"][type_RLS]["rangeTopY"]*1000) # 4150
		size_x = config["model"][type_RLS]["size"] * 2 # 160000
		size_y =  config["model"][type_RLS]["size"] + int(config["model"][type_RLS]["rangeTopY"]*1000) # 84150
	else:
		print("Unknown Model :{}".format(type_RLS))
		return 1

	min_x = -(width/2) # 브라우저 초기 화면 시작점 X
	min_y = -(height/4) # 브라우저 초기 화면 시작
	## SVG viewBox = "<min-x>, <min-y>, <width>, <height>"
	html_viewBox = "{} {} {} {}".format(min_x, min_y, width, height)
	html_grid = '' # 박스 프레임에 눈금자를 그린다.
	html_user = '' # 센서가 아닌 사용자 수용 또는 거부 영역
	gridStep = 1000 # 미리미터 
	## html_grid - 그리드 세로선 그리기
	for i in range((start_x//gridStep), ((size_x+start_x)//gridStep)+1):
		# html_grid += "<path class='html_grid' id='grid_v_{}' d='M {} 0 v 50000'></path>".format(i,(i*gridStep))
		if i%10 == 0: 
			style = 'html_gridB'
			html_grid += f"<text x='{(i*gridStep)}' y='-100' text-anchor='right' style='fill:#ffffff80; font-size:10cm;'>{i}</text>"
		else: 
			style = 'html_grid'
		html_grid += "<path class='{}' id='grid_v_{}' d='M {} 0 v {}'></path>".format(style,i,(i*gridStep),height)
		# html_grid += "<path class='html_grid' id='grid_v_{}' d='M {} 0 v {}'></path>".format(i,(i*gridStep),height)
	## html_grid - 그리드 가로선 그리기
	for i in range(0, ((size_y+start_y)//gridStep)+1):
		# html_grid += "<path class='html_grid' id='grid_h_{}' d='M -50000 {} h 100000'></path>".format(i,(i*gridStep))
		if i%10 == 0: 
			style = 'html_gridB'
			html_grid += f"<text x='0' y='{(i*gridStep)+400}' text-anchor='right' style='fill:#ffffff80; font-size:10cm;'>{i}</text>"
		else: 
			style = 'html_grid'
		html_grid += "<path class='{}' id='grid_h_{}' d='M -{} {} h {}'></path>".format(style,i,width,(i*gridStep),size_x)
		# html_grid += "<path class='html_grid' id='grid_h_{}' d='M -{} {} h {}'></path>".format(i,width,(i*gridStep),size_x)
		
	if type_RLS == "RLS-3060V":
		## html_frame - 하단의 반원모양 영역
		html_frame = "<path class='html_frame' d='M 0 0 L -50000 -4150 L -50000 0 C -50000 66666, 50000 66666, 50000 0 L 50000 -4150 Z '></path>"
		## html_over - 상단의 180도 넘는 나비모양 영역
		html_over = "<path class='html_over' d='M -50000 0 L -50000 -4150 L 0 0 L 50000 -4150 L 50000 0 L 0 0' Z></path>"
		html_zone = ""
	elif type_RLS == "RLS-50100V":
		## html_frame - 하단의 반원모양 영역
		html_frame = "<path class='html_frame' d='M 0 0 L -80000 -4150 L -80000 0 C -80000 106666, 80000 106666, 80000 0 L 80000 -4150 Z '></path>"
		## html_over - 상단의 180도 넘는 나비모양 영역
		html_over = "<path class='html_over' d='M -80000 0 L -80000 -4150 L 0 0 L 80000 -4150 L 80000 0 L 0 0' Z></path>"
		html_zone = ""

	__script_jquery_js__ = '/home/pi/common/jquery/jquery-3.1.1.min.js'
	__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	__script_jquery_ui_js__ = '/home/pi/common/jquery/ui/jquery-ui.js'
	__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	__style_jquery_ui_css__ = '/home/pi/common/jquery/ui/jquery-ui.css'
	__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	__svg_pan_zoom__ = '/home/pi/common/svg-pan-zoom/svg-pan-zoom.js'
	__svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'

	replacements = {
		"__liveCam__":f'''<div id="liveCam" style="background-image:url({config["camera"]["liveMjpg"]});">
<div style="width:100%;height:1px;margin:unset;padding:unset;background-color:crimson;position:absolute;top:50%;left:0"></div>
<div style="width:1%;height:2%;margin:unset;padding:unset;background-color:crimson;position:absolute;top:50%;left:50%"></div>
<div id="objPostion" style="position:absolute;top:50%;left:0%;background:#67db8036;border-radius:50%;width:1px;height:px;border: 1px solid red;"></div>
<div name="toggleViewCam" id="toggleViewCam" style="width:6px;position:absolute;top:0;left:0;height:6px;background-color:#007e8b;margin:1px;z-index:1;"></div>
<div name="toggleSizeCam" id="toggleSizeCam" style="width:6px;position:absolute;top:0;right:0;height:6px;background-color:darkred;margin:1px;z-index:1;"></div>
</div>''',
		"__health__":'''<div class='health' id='health'>
<div class="wdWrap, cpuStataus"><div class="wdName">cpu</div><div class="wdStatus"><hr class="cpu" style="width:80%;background-color:orangered;" title=""><hr class="cpuOv wdLeftover" title=""></div></div>
<div class="wdWrap, memStataus"><div class="wdName">mem</div><div class="wdStatus"><hr class="mem" style="width:80%;background-color:blueviolet;" title=""><hr class="memOv wdLeftover" title=""></div></div>
<div class="wdWrap, soilStataus"><div class="wdName">dust</div><div class="wdStatus"><hr class="soil" style="width:80%;background-color:deepskyblue;" title=""><hr class="soilOv wdLeftover" title=""></div></div>
<div class="wdWrap, tempStataus"><div class="wdName">temp</div><div class="wdStatus"><hr class="temp" style="width:80%;background-color:forestgreen;" title=""><hr class="tempOv wdLeftover" title=""></div></div>
<div class="wdWrap, lastStataus"><div class="wdName">last</div><div class="wdStatus"></div></div>
</div>''',
		"__model_and_rev__":config["gInfoDevice"]["model"], 
		"__version__":config["gInfoDevice"]["version"], 
		"__boundary_of_zone__":html_zone, 
		"__boundary_of_area__":config["wsDetectArea"]["svg"]["area"], 
		"__boundary_of_mask__":'', 
		"__boundary_of_allocate__":'', 
		"__boundary_of_grid__":html_grid, 
		"__boundary_of_frame__":html_frame, 
		"__boundary_of_over__":html_over, 
		"__boundary_of_background__":'',
		"__boundary_of_user__":html_user, 
		"__script_jquery_js__":__script_jquery_js__, 
		"__script_jquery_ui_js__":__script_jquery_ui_js__, 
		"__style_jquery_ui_css__":__style_jquery_ui_css__, 
		"__svg_viewBox__":html_viewBox, 
		"__svg_pan_zoom__":__svg_pan_zoom__
	}
	
	
	# For Area Setup and Monitoring
	with open(config["file"]["templet"]["source"]) as infile, open(config["file"]["templet"]["target"], 'w') as outfile:
		for line in infile:
			for src, config["file"]["templet"]["target"] in replacements.items():
				line = line.replace(src, config["file"]["templet"]["target"])
			outfile.write(line)
	
	# # For IMS Popup
	# with open(source_ims) as infile, open(target_ims, 'w') as outfile:
	# 	for line in infile:
	# 		for src, target_ims in replacements.items():
	# 			line = line.replace(src, target_ims)
	# 		outfile.write(line)
	
	# # For Ignore Ares Filtering
	# with open(config["file"]["templet"]["sourceArea"]) as infile, open(config["file"]["templet"]["targetArea"], 'w') as outfile:
	# 	for line in infile:
	# 		for src, config["file"]["templet"]["targetArea"] in replacements.items():
	# 			line = line.replace(src, config["file"]["templet"]["targetArea"])
	# 		outfile.write(line)

	return 0

def main():

	############ create log table ################
	## 로그 테이블 생성
	returnMsg = create_table_w_log_RLS_V() 
	# print(returnMsg) # 0 - Success

	## 센서 동작 테스트 및 관련 정보취합
	## Getting device information
	status, desc = requestApi(config["sensor"]["cmd"]["gInfoDevice"], "get")
	if status:
		print (f"Error Getting device information - {status}")
		exit("Critical Error: Sensor Connection.")
	else:
		print ("Pass Getting device information")
		config["gInfoDevice"] = desc.copy()

	## Getting internal status
	status, desc = requestApi(config["sensor"]["cmd"]["gInfoStatus"], "get")
	if status:
		print (f"Error Getting internal status - {status}")
		exit("Critical Error: Sensor Connection.")
	else:
		print (f"Pass Getting internal status")
		config["gInfoStatus"] = desc.copy()

	## Getting output status - Current
	status, desc = requestApi(config["sensor"]["cmd"]["gInOutCurr"], "get")
	if status:
		print (f"Error Getting output status - Current - {status}")
		exit("Critical Error: Sensor Connection.")
	else:
		print ("Pass Getting output status - Current")
		config["gInOutCurr"] = desc.copy()

	## Getting output status - Diff
	status, desc = requestApi(config["sensor"]["cmd"]["gInOutDiff"], "get")
	if status:
		print (f"Error Getting output status - Diff - {status}")
		exit("Critical Error: Sensor Connection.")
	else:
		print ("Pass Getting output status - Diff")
		config["gInOutDiff"] = desc.copy()

	## Getting mounting information
	status, desc = requestApi(config["sensor"]["cmd"]["gMounting"], "get")
	if status:
		print (f"Error Getting mounting information - {status}")
		exit("Critical Error: Sensor Connection.")
	else:
		print ("Pass Getting mounting information")
		config["gMounting"] = desc.copy()

	## Getting detection area
	status, desc = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectArea"], {"ctrl":"start"}))
	if status:
		print (f"Error Getting detection area - {status}")
		exit("Critical Error: Sensor Connection.")
	else:
		print ("Pass Getting detection area")
		config["wsDetectArea"] = desc.copy()

	## 참고: 지우지 말것
	# ## Getting position of detected object
	# status, desc = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectObj"], {"ctrl":"start","maxObject":50,"withCandidate":False}))
	# if status:
	# 	print ("Error Getting position of detected object")
	# else:
	# 	print ("Pass Getting position of detected object")
	# 	# config["wsDetectObj"] = desc.copy()

	# ## Getting event code
	# status, desc = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectEvent"], {"ctrl":"start"}))
	# if status:
	# 	print ("Error Getting event code")
	# else:
	# 	print ("Pass Getting event code")
	# 	# config["wsDetectEvent"] = desc.copy()

	# ## Set Profile switching 0
	# status, desc = requestApi(config["sensor"]["cmd"]["pProfile0"], "post")
	# if status:
	# 	print ("Error Detector Profile switching 0")
	# else:
	# 	print ("Pass Detector Profile switching 0")
	# 	config["pProfile0"] = desc.copy()

	# ## Getting masking/allocating area
	# status, desc = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectMask"], {"ctrl":"start"}))
	# if status:
	# 	print ("Error Getting masking/allocating area")
	# else:
	# 	print ("Pass Getting masking/allocating area")
	# 	config["wsDetectMask"] = desc.copy()
	# 	# print(config["wsDetectMask"])

	# ## Set Profile switching 1
	# status, desc = requestApi(config["sensor"]["cmd"]["pProfile1"], "post")
	# if status:
	# 	print ("Error Detector Profile switching 1")
	# else:
	# 	print ("Pass Detector Profile switching 1")
	# 	config["pProfile1"] = desc.copy()

	# ## Getting masking/allocating area
	# status, desc = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectMask"], {"ctrl":"start"}))
	# if status:
	# 	print ("Error Getting masking/allocating area")
	# else:
	# 	print ("Pass Getting masking/allocating area")
	# 	config["wsDetectMask1"] = desc.copy()
	# 	# print(config["wsDetectMask1"])


	## config["wsDetectArea"]["distances"] 값으로 부터 SVG(config["wsDetectArea"]["svg"]) 데이터를 생성하는 기능 
	count = 0
	maxX = 0 # 감지가능한 오른축 거리(양수값)
	maxY = 0 # 감지가능한 전방 거리(양수값)
	minX = 0 # 감지가능한 왼축 거리(음수값)
	minY = 0 # 감지가능한 후방 거리(음수값)
	objInfo = ''
	if config["gInfoDevice"]["model"] == "RLS-3060V": #  or "RLS-50100V":
		unitAngle = 0.25 # float(190/760) - RLS-3060V
	else:
		unitAngle = 0.125 # float(190/1520) - RLS-50100V

	config["wsDetectArea"]["svg"] = {}
	while (count < config["wsDetectArea"]["steps"]):
		orgX = 0
		fLN = count * 4
		tLN = fLN + 4
		length = config["wsDetectArea"]["distances"][count]
		angle = math.radians(unitAngle * (count - 20)) # 시작이 -20번째부터 진행 한다(총 185도)
		distX = int(length * math.cos(angle))
		distY = int(length * math.sin(angle))
		
		if (maxX < distX): maxX = distX
		if (maxY < distY): maxY = distY
		if (minX > distX): minX = distX
		if (minY > distY): minY = distY
		
		objInfo += "L {} {} ".format(distX + orgX, distY)
		count = count + 1
		
	config["wsDetectArea"]["svg"]["area"] = "<path class='html_scan' d='M{} 0 {} Z' />".format(orgX, objInfo)
	config["wsDetectArea"]["svg"]["steps"] = config["wsDetectArea"]["steps"]
	config["wsDetectArea"]["svg"]["maxX"] = maxX
	config["wsDetectArea"]["svg"]["maxY"] = maxY
	config["wsDetectArea"]["svg"]["minX"] = minX
	config["wsDetectArea"]["svg"]["minY"] = minY

	if maxX > abs(minX): # 스켄된 x 축의 최다값 : 카메라 영상에 죄표를 표시하기 위한 참고 값
		config["wsDetectArea"]["svg"]["scanWidth"] = maxX
	else:
		config["wsDetectArea"]["svg"]["scanWidth"] = abs(minX)
	## END

	## Sensor MASQUERADE
	## config["sensor"]["masquerade"] 값이 참(True)이면
	active, ip, port = MASQUERADE(config["sensor"]["masquerade"], config["sensor"]["addr"], config["port"]["masquerade"])
	if active:
		print ("Sensor MASQUERADE On, Access Port:{}".format(port))
	else:
		print ("MASQUERADE Off")
		
	# if config["sensor"]["masquerade"]:
	# 	config["camera"]["liveMjpg"] = f'http://{config["sensor"]["user"]}:{config["sensor"]["pass"]}@{config["server"]["localhost"]["addr"]}:{config["port"]["masquerade"]}{config["sensor"]["cmd"]["mjpg"]}'
	# 	config["camera"]["liveShot"] = f'http://{config["sensor"]["user"]}:{config["sensor"]["pass"]}@{config["server"]["localhost"]["addr"]}:{config["port"]["masquerade"]}{config["sensor"]["cmd"]["shot"]}'
	# else:
	# 	config["camera"]["liveMjpg"] = f'http://{config["sensor"]["user"]}:{config["sensor"]["pass"]}@{config["sensor"]["addr"]}{config["sensor"]["cmd"]["mjpg"]}'
	# 	config["camera"]["liveShot"] = f'http://{config["sensor"]["user"]}:{config["sensor"]["pass"]}@{config["sensor"]["addr"]}{config["sensor"]["cmd"]["shot"]}'
	if config["sensor"]["masquerade"]:
		config["camera"]["liveMjpg"] = f'http://{config["server"]["localhost"]["addr"]}:{config["port"]["masquerade"]}{config["sensor"]["cmd"]["mjpg"]}'
		config["camera"]["liveShot"] = f'http://{config["server"]["localhost"]["addr"]}:{config["port"]["masquerade"]}{config["sensor"]["cmd"]["shot"]}'
	else:
		config["camera"]["liveMjpg"] = f'http://{config["sensor"]["addr"]}{config["sensor"]["cmd"]["mjpg"]}'
		config["camera"]["liveShot"] = f'http://{config["sensor"]["addr"]}{config["sensor"]["cmd"]["shot"]}'
	config["camera"]["liveRtsp"] = config["sensor"]["cmd"]["rtsp"].format(config["sensor"]["user"],config["sensor"]["pass"],config["sensor"]["addr"])

	config["file"] = {}
	config["file"]["templet"] = {}
	config["file"]["templet"]["source"] = "{}/realtime_RLS_templet.html".format(config["path"]["myHome"]) # Optex Theme
	# config["file"]["templet"]["sourceArea"] = "{}/realtime_RLS_templet_Area.html".format(config["path"]["myHome"]) # Optex Theme
	config["file"]["templet"]["target"] = "{}/realtime_RLS_live.html".format(config["path"]["myHome"])
	# config["file"]["templet"]["targetArea"] = "{}/realtime_RLS_live_Area.html".format(config["path"]["myHome"]) # Area

	## Set masking/maskCoord
	filter = "{}/filter.json".format(config["path"]["data"])
	if os.path.exists(filter):
		config["filter"] = readConfig(filter)
	saveConfig(config["filter"], filter)

	level = "{}/level.json".format(config["path"]["data"])
	if os.path.exists(level):
		config["level"] = readConfig(level)
	saveConfig(config["level"], level)

	trigger = "{}/trigger.json".format(config["path"]["data"])
	if os.path.exists(trigger):
		config["trigger"] = readConfig(trigger)
	saveConfig(config["trigger"], trigger)



	# print ("Filter Reset Time: {}sec".format(config["filter"]["reset"]))
	# print ("Filter Count: {}".format(config["filter"]["hold"]["cont"]))
	# print ("Filter Keep: {}".format(config["filter"]["hold"]["keep"]))
	# # print ("Filter due Time: {}".format(config["filter"]["hold"]["due"]))
	# print ("Filter Size: {}mm ~ {}mm".format(config["filter"]["size"]["min"], config["filter"]["size"]["max"]))


	## 멀티트레딩 이벤트 타이머, 이벤트 카운트
	config["actTimer"] = {}
	config["actCount"] = {}
	config["actCycle"] = {}
	config["recordOn"] = False ## 최초 이벤트가 발생시:True, 이벤트가 없으면(len(config["actTimer"]) == 0): False

	# print(json.dumps(config["filter"], sort_keys=True, indent=4))

	saveConfig(config, "./config_RLS3.json")

	if makeHtml(config["gInfoDevice"]["model"]): 
		exit("Critical Error: Unknown Sensor Model.")

	run_demon_RLS3()
	# run_demon_setup()

if __name__ == '__main__':
	kill_demon_JS()
	kill_demon_RLS3()
	# kill_demon_setup()

	config = readConfig("./config.json")

	if not os.path.exists(config["path"]["data"]): # /var/www/html/its_web/data/log
		os.makedirs(config["path"]["data"])
	if not os.path.exists(config["path"]["log"]):
		os.makedirs(config["path"]["log"])
	if not os.path.exists(config["path"]["log"]+"/RLSV"): # /var/www/html/its_web/data/log/API3
		os.makedirs(config["path"]["log"]+"/RLSV")
	config["path"]["logger"] = config["path"]["log"]+"/RLSV/RLSV.log"
	
	# localhost IP주소는 setup.pyc에서 저장된다 
	config["server"]["localhost"]["addr"] = get_ip_address(get_interface())

	main()
	# if config["sensor"]["addr"] and config["server"]["localhost"]["addr"]:
	# 	main()
	# 	pass
	# else:
	# 	exit("Run Setup First!")
