#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import time
import subprocess 
import socket 
import fcntl
import struct
import json
import logging
import logging.handlers

### Unicode Reload 파이선 기본은 ascii이며 기본값을 utf-8로 변경한다
reload(sys)
sys.setdefaultencoding('utf-8')

def clearBuffer(sock, n):
	data = b''
	while True: 
		data = sock.recv(n)
		if len(data) < n: 
			return
			
## 환경설정 파일(JSON) 읽기
def readConfig():
	with open('config.json') as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 읽기
def saveConfig(cfg):
	with open('config.json', 'w') as json_file: ## 저장
		json.dump(cfg, json_file, indent=4)

# 서버 아이피 			
def get_ip_address(ifname): ## get_ip_address('eth0') -> '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])
			
# 확인된 변수로 데몬을 실행 한다
def run_demon_CAM_js(arg): 
	cmd = "cd /home/pi/CAM/; node CAM.js %s 2>&1 & " % (arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 실행하고 있는 'dndmon'란 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_CAM(arg): 
	cmd = "kill $(ps aux | grep 'CAM.pyc %s' | awk '{print $2}')" % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 확인된 변수로 데몬을 실행 한다
def run_demon_CAM_js(arg): 
	cmd = "cd /home/pi/CAM/; node CAM.js %s 2>&1 & " % (arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_CAM_js(arg): 
	cmd = "kill $(ps aux | grep 'CAM.js %s' | awk '{print $2}')" % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# Network Port를 사용하고 있는 프로세서 종료
def kill_port_CAM(arg): 
	cmd = "sudo kill -9 `sudo lsof -t -i:%s`" % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
			
# 확인된 변수로 데몬을 실행 한다
def run_demon_CAM(arg): 
	cmd = "python -u -W ignore /home/pi/CAM/CAM.pyc %s 2>&1 & " % arg 
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

def make_table_CAM(source, target, ITS_video_URL, imgX, imgY, path):
	jquery = '%s/jquery/jquery-3.1.1.min.js' % path
	__script_jquery_js__ = '<script>'+open(jquery, 'r').read()+'</script>'

	bootstrap_js = '%s/bootstrap/js/bootstrap.min.js' % path
	__script_bootstrap_js__ = '<script>'+open(bootstrap_js, 'r').read()+'</script>'
	bootstrap_css = '%s/bootstrap/css/bootstrap.min.css' % path
	__style_bootstrap_css__ = '<style>'+open(bootstrap_css, 'r').read()+'</style>'

	canvas_gauges_js = '%s/node_modules/canvas-gauges/gauge.min.js' % path
	__script_canvas_gauges_js__ = '<script>'+open(canvas_gauges_js, 'r').read()+'</script>'

	__camera_live_url__ = ITS_video_URL
	__camera_image_X__ = str(imgX)
	__camera_image_Y__ = str(imgY)
	
	with open(source, 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__script_bootstrap_js__', __script_bootstrap_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_bootstrap_css__', __style_bootstrap_css__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__script_canvas_gauges_js__', __script_canvas_gauges_js__)
		
		tmp_its_tmp = tmp_its_tmp.replace('__camera_live_url__', __camera_live_url__)
		tmp_its_tmp = tmp_its_tmp.replace('__camera_image_X__', __camera_image_X__)
		tmp_its_tmp = tmp_its_tmp.replace('__camera_image_Y__', __camera_image_Y__)

		with open(target, 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()

			
def check_opened_port(name):
	ports={'FTP':21,'SSH':22,'SMTP':25,'DNS':53,'HTTP':80,'NNTP':119,'RPC':135,'NetBT':137,'NetBT':138,'NetBT':139,'LDAP':389,'HTTPS':443,'SMB':445,'ISAKMP':500,'CAMERA':554,'SNEWS':563,'RPC':593,'LDAP':636,'IAS':1645,'IAS':1646,'L2TP':1701,'PPTP':1723,'IAS':1812,'IAS':1813,'MGC':3268,'MGC':3269,'RDP':3389,'RLS':50001,'ITS':64446}
	port = ports[name]
	ip_class=get_ip_address('eth0').rsplit('.',1)[0] #eth0,enp2s0
	port_info = []
	
	for ips in range(2,255):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.settimeout(0.01)
		ip='%s.%s'%(ip_class,ips)

		if sock.connect_ex((ip,port)):
			pass
		else:
			# port_info[ip] += "'%s':'%s'"%(name,ip)
			port_info.insert(0, ip)
			
		sock.close()
	return port_info
