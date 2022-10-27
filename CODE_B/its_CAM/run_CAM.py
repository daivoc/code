#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from module import *

###############################################
## 파일 config.json내용을 사용자 변수로 선언
with open('config.json') as json_file:  
	cfg = json.load(json_file)

###### 기존 프로그램 중지 ######
camera_ID = cfg["camera"]["addr"] ## Py간 중계를 위한 통신 포트 공유

kill_demon_CAM(camera_ID)
kill_demon_CAM_js(camera_ID)
kill_port_CAM(cfg["interface"]["portIn"]) ## # sudo kill -9 `sudo lsof -t -i:7006`
kill_port_CAM(cfg["interface"]["portOut"])

run_demon_CAM(camera_ID)
	
exit()
