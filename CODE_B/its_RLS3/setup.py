#!/usr/bin/env python
# -*- coding: utf-8 -*-

## python3.7 -m pip install flask
## python3.7 -m pip install flask_socketio
## python3.7 -m pip install websockets
## python3.7 -m pip install gevent-websocket
## python3 -m pip install suds-py3
## https://medium.com/the-research-nest/how-to-log-data-in-real-time-on-a-web-page-using-flask-socketio-in-python-fb55f9dad100

import json
import socket
import subprocess
import asyncio
import datetime

from flask import Flask, render_template #, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

config = None

@app.route('/')
@app.route('/<name>')
def index(name=None):
	return render_template('index.html', name=name)

@app.route('/setup/')
def setup():
	return render_template('setup.html')

@socketio.event
def connect():
	emit('connect', config)

# ####################
# ## ITS Server 시간
# # from threading import Lock
# from threading import Timer
# class threadingTimer(): # 타이머 실행기능 예: threadingTimer(1, current_datetime)
# 	def __init__(self, t, hFunction):
# 		self.t = t
# 		self.hFunction = hFunction
# 		self.thread = Timer(self.t, self.handle_function)
# 	def handle_function(self):
# 		self.hFunction()
# 		self.thread = Timer(self.t, self.handle_function)
# 		self.thread.start()
# 	def start(self):
# 		self.thread = Timer(self.t, self.handle_function)
# 		self.thread.start()
# 	def cancel(self):
# 		self.thread.cancel()
# itsClock = None
# @socketio.on('clockToggle')
# def clockToggle():
# 	if itsClock is None:
# 		itsClock = threadingTimer(1, current_datetime)
# 		itsClock.start()
# 	else:
# 		itsClock.cancel()
# 		itsClock = None
# def current_datetime():
# 	socketio.emit('system_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# ####################

####################
## Request_Api 요청
import requests
from requests.auth import HTTPDigestAuth
@socketio.on('Request_Api')
def Request_Api(data):
	status, desc = requestApi(data, "get")
	if status:
		emit('Return_JSON', f"{status} {desc}", broadcast=True)
	else:
		emit('Return_JSON', desc, broadcast=True)
	return
def requestApi(command, method):
	try:
		# print("http://{}{}".format(config["sensor"]["addr"],command))
		if method == "get":
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
####################

####################
## WebSocket_Api 요청
import websockets
@socketio.on('wSocket_Api')
def wSocket_Api(data):
	print(data)
	# status, desc = asyncio.run(webSocketApi(config["sensor"]["cmd"]["wsDetectArea"], {"ctrl":"start"}))
	status, desc = asyncio.run(webSocketApi(data["command"], data["data"]))
	if status:
		emit('Return_JSON', f"{status} {desc}", broadcast=True)
	else:
		emit('Return_JSON', desc, broadcast=True)
	return
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
		return 2, "Except: connect"
####################

####################
## Onvif 요청
# Onvif Python3 Install
# $ python3 -m pip install --upgrade onvif_zeep
# $ cd ~/.local/lib/python3.7/site-packages
# $ ln -s ../../python3.4/site-packages/wsdl .
from onvif import ONVIFCamera
# cameraRLS = ONVIFCamera('192.168.0.126', 80, 'root', 'RLS-50100V', '/home/pi/.local/lib/python3.7/site-packages/wsdl/')
# cameraRLS = ONVIFCamera('192.168.168.30', 80, 'root', 'RLS-3060V', '/home/pi/.local/lib/python3.7/site-packages/wsdl/')
@socketio.on('Onvif_Api')
def Onvif_Api(data):
	try:
		cameraRLS = ONVIFCamera(config["sensor"]["addr"], 80, config["sensor"]["user"], config["sensor"]["pass"])
		devicemgmt_service = cameraRLS.create_devicemgmt_service()
		if data["command"] == "ovGetDeviceInformation":
			response = devicemgmt_service.GetDeviceInformation()
		elif  data["command"] == "ovSystemReboot":
			response = devicemgmt_service.SystemReboot() ## tested
		else:
			response = "Command Not Found - {}".format(data["command"])
	except:
		response = f'''Error Onvif: GetDeviceInformation'''
	emit('Return_STR', f"{response}", broadcast=True)
	return
####################

@socketio.on('Save_Config')
def Save_Config(data):
	# print('received: ' + str(data) + data["sensor_pickup"])
	# print('received: ' + data["sensor_pickup"])
	config["sensor"]["addr"] = data["sensor_addr"]
	config["sensor"]["user"] = data["sensor_user"]
	config["sensor"]["pass"] = data["sensor_pass"]
	config["sensor"]["pickup"] = data["sensor_pickup"]
	if data["sensor_addr"] == "192.168.168.30":
		config["sensor"]["masquerade"] = True
	else:
		config["sensor"]["masquerade"] = False
	config["server"]["ims"]["addr"] = data["server_ims_addr"]
	config["permission"]["filterIP"]["admin"] = data["permission_filterIP_admin"]
	config["permission"]["filterIP"]["manager"] = data["permission_filterIP_manager"]
	config["permission"]["filterIP"]["deny"] = data["permission_filterIP_deny"]

	config["sensor"]["vServer"] = masquerade()

	saveConfig(config, "./config.json")
	
	emit('connect', config)
	emit('Return_JSON', "Parameters Updated", broadcast=True)
	return

@socketio.on('Is_Port_Open') # Is_Port_Open(config["port"]["nodeOut"])
def Is_Port_Open(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	location = ("127.0.0.1", port)
	result_of_check = sock.connect_ex(location)
	sock.close()

	if result_of_check == 0: 
		# print("Port is open")
		status = True
	else: 
		# print("Port is not open")
		status = False
	emit('Return_Is_Port_Open', status)
	return status

@socketio.on('Reboot_Self')
def Reboot_Self():
	cmd_proc_Popen('sudo reboot')

@socketio.on('Restart_Self')
def Restart_Self():
	cmd_proc_Popen('python3 ./run_RLS3.pyc > /dev/null')

def masquerade():
	if config["sensor"]["masquerade"]:
		# 연결 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null;
		sudo iptables -A FORWARD -i eth0 -j ACCEPT;
		sudo iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE;
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(config["port"]["masquerade"], config["sensor"]["addr"])
		vServer = f'{config["server"]["localhost"]["addr"]}:{config["port"]["masquerade"]}'
	else:
		# 차단 아이피 FORWARD
		cmd = '''
		sudo sysctl -w net.ipv4.ip_forward=0 > /dev/null;
		sudo iptables -D FORWARD -i eth0 -j ACCEPT
		sudo iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE
		sudo iptables -t nat -D PREROUTING -i eth0 -p tcp -m tcp --dport %s -j DNAT --to-destination %s:80;
		'''%(config["port"]["masquerade"], config["sensor"]["addr"])
		vServer = config["sensor"]["addr"]
	# print cmd
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return vServer

# 자신 아이피 확인 
def get_ip_address():
	iface = cmd_proc_Popen("ip addr | awk '/state UP/ {print $2}' | head -n 1 | sed 's/:$//' 2>/dev/null").strip().decode()
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

def main():
	config["server"]["localhost"]["addr"] = get_ip_address()
	config["sensor"]["vServer"] = masquerade()
	saveConfig(config, "./config.json")
	socketio.run(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
	config = readConfig("./config.json")
	main()