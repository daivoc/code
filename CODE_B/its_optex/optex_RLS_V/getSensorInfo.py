#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Python3
pip3 install websockets
'''
import json
import requests
from requests.auth import HTTPDigestAuth
import asyncio
from websockets import connect

def requestApi(command, method):
	if method == "get":
		response = requests.get(command.format(api["addr"]), auth=HTTPDigestAuth(api["user"], api["pass"]))
	elif method == "post":
		response = requests.post(command.format(api["addr"]), auth=HTTPDigestAuth(api["user"], api["pass"]))
	else:
		return 2, "Unknoe Methode"

	if response.status_code == 200:
		return 0, response.json()
	else:
		return 1, response.status_code

async def webSocketApi(uri, data):
	try:
		async with connect(uri.format(api["addr"])) as ws:
			await ws.send(json.dumps(data))
			try:
				response = await ws.recv()
				return 0, json.loads(response)
			except:
				return 1, "Except: recv"
	except:
		return 2, "Except: connect"

def saveConfig(config,pathName):
	with open(pathName, 'w') as json_file: ## 저장
		json.dump(config, json_file, sort_keys=True, indent=4)

def main():
	status, desc = requestApi(api["cmd"]["gInfoDevice"], "get")
	config["gInfoDevice"] = desc.copy()
	status, desc = requestApi(api["cmd"]["gInfoStatus"], "get")
	config["gInfoStatus"] = desc.copy()
	status, desc = requestApi(api["cmd"]["gInOutCurr"], "get")
	config["gInOutCurr"] = desc.copy()
	status, desc = requestApi(api["cmd"]["gInOutDiff"], "get")
	config["gInOutDiff"] = desc.copy()
	status, desc = requestApi(api["cmd"]["gParaMounting"], "get")
	config["gParaMounting"] = desc.copy()

	status, desc = asyncio.run(webSocketApi(api["cmd"]["wsDetectObj"], {"ctrl":"start","maxObject":50,"withCandidate":False}))
	config["wsDetectObj"] = desc.copy()
	status, desc = asyncio.run(webSocketApi(api["cmd"]["wsDetectArea"], {"ctrl":"start"}))
	config["wsDetectArea"] = desc.copy()
	status, desc = asyncio.run(webSocketApi(api["cmd"]["wsDetectMask"], {"ctrl":"start"}))
	config["wsDetectMask"] = desc.copy()
	status, desc = asyncio.run(webSocketApi(api["cmd"]["wsDetectEvent"], {"ctrl":"start"}))
	config["wsDetectEvent"] = desc.copy()

	## 아래의 Post명령은 WebSocket명령에 영향을 준다.
	status, desc = requestApi(api["cmd"]["pProfile0"], "post")
	config["pProfile0"] = desc.copy()
	status, desc = requestApi(api["cmd"]["pProfile1"], "post")
	config["pProfile1"] = desc.copy()

	saveConfig(config, "./sensorInfo.json")

	# print(config)

if __name__ == '__main__':
	api = {
		"addr":"192.168.168.30",
		"user":"root",
		"pass":"RLS-3060V",
		"cmd":{
			"gInfoDevice":"http://{}/api/info/device/get",
			"gInfoStatus":"http://{}/api/info/status/get",
			"gInOutCurr":"http://{}/api/io/get/current",
			"gInOutDiff":"http://{}/api/io/get/diff",
			"gParaMounting":"http://{}/api/param/get/system.information.mounting",
			"pProfile0":"http://{}/api/profile/select/0",
			"pProfile1":"http://{}/api/profile/select/1",
			"wsDetectObj":"ws://{}/detection",
			"wsDetectArea":"ws://{}/area",
			"wsDetectMask":"ws://{}/maskalloc",
			"wsDetectEvent":"ws://{}/event"
		}
	}
	config = {}

	main()
