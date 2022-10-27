#!/usr/bin/env python
# -*- coding: utf-8 -*-

## https://gist.github.com/stephenhouser/c0ecaacedc14cbe62502ec123a812e12

import requests
import time
from requests.auth import HTTPDigestAuth

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result
	
def cameraIMAGESIZE(enc, camera_addr, camera_user, camera_pass):
	result = {} ## requests.get에 대한 결과물 저장
	camera_url = "http://%s:%s@%s/axis-cgi/imagesize.cgi"%(camera_user,camera_pass,camera_addr)
	q_args = { 'camera': 1, 'imagerotation': 0, 'html': 'no', 'timestamp': int(time.time()) }
	
	if(enc):
		resp = requests.get(camera_url, params=q_args, auth=HTTPDigestAuth(camera_user, camera_pass))
	else:
		resp = requests.get(camera_url, params=q_args)
		
	if resp.text.startswith('Error'):
		result['error'] = resp.text
	else:
		for line in resp.text.splitlines():
			# print line
			try:
				(name, var) = line.split("=", 2)
				try:
					result[name.strip()] = float(var)
				except ValueError:
					result[name.strip()] = var
			except:
				result['error'] = 'cameraIMAGESIZE Responsed Parsing Error'
	return result

def cameraPTZ(q_cmd, enc, camera_addr, camera_user, camera_pass):
	result = {} ## requests.get에 대한 결과물 저장
	try:
		command = {}
		for pair in q_cmd:
			x,y = pair.split("=")
			command[x] = y
	except:
		result['error'] = 'Command Parsing Error'
		return result

	# print("command({})".format(command))
	if len(command):
		camera_url = "http://%s:%s@%s/axis-cgi/com/ptz.cgi"%(camera_user,camera_pass,camera_addr)
		base_q_args = { 'camera': 1, 'imagerotation': 0, 'html': 'no', 'timestamp': int(time.time()) }
		q_args = merge_dicts(command, base_q_args) # {'move': 'home', 'camera': 1, 'imagerotation': 0, 'html': 'no', 'timestamp': 1539151654}
		
		if(enc):
			resp = requests.get(camera_url, params=q_args, auth=HTTPDigestAuth(camera_user, camera_pass))
		else:
			resp = requests.get(camera_url, params=q_args)

		if resp.text.startswith('Error'):
			result['error'] = resp.text
		else:
			for line in resp.text.splitlines():
				# print line
				try:
					(name, var) = line.split("=", 2)
					try:
						result[name.strip()] = float(var)
					except ValueError:
						result[name.strip()] = var
				except:
					result['error'] = 'cameraPTZ Responsed Parsing Error'
		return result
	else:
		result['error'] = 'command not found'
		return result