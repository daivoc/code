#!/usr/bin/env python
# -*-coding: utf-8 -*-

help = '''
CCTV의 스트리밍을 일정량(maxCntPrev)의 스넵샷으로 저장하는 기능
스넵샷을 maxCntPrev 횟수까지 저장하는 주기는 환경에 따라 시간이 변동적이다.
CCTV의 성능에 따라 저장속도나 량은 가변적으로 상황에 따른 튜닝이 필요하다.
이미지는 /var/www/html/its_web/data/cam/dirCur 에 저장 된다.

스트리밍 프로토클은 Local Camera(/dev/video0) 외에 RTSP, AVI, MJPG가 가능 하다.
	# cap = cv2.VideoCapture(0) # On Board 카메라 
	# cap = cv2.VideoCapture('/dev/video0') # On Board 카메라 
	# cap = cv2.VideoCapture('video.avi') # On Board 카메라 
	# cap = cv2.VideoCapture('http://admin:admin@192.168.0.140/cgi-bin/mjpg/video.cgi?channel=0&subtype=1') # MJPG
	# cap = cv2.VideoCapture('rtsp://admin:admin@192.168.0.140/cam/realmonitor?channel=1&subtype=00') # RTSP http://192.168.0.113/
	# cap = cv2.VideoCapture('rtsp://admin:admin@96.48.233.195:5540') # Standard RTSP Camera
	# cap = cv2.VideoCapture('rtsp://admin:admin@192.168.0.113') # Standard RTSP Camera

응용:
	이벤트 발생:
		- echo '[{ "camera": { "command": "grap", "value": "" }}]' | nc 192.168.0.80 34001 -q 0
		- 폴더 'dirRoot' 내에 'dirTmp'란 빈 폴더를 생성(트리거)하면
		- 프로그램은 최근 저장된(dirCur) 스넵샷 최대 갯수(maxCntPrev)를 현재시간(연월일시분초)으로 제목변경(저장)
		- 저장시 폴더명의 마지막이 초단위로 이는 1초 이내 1번 이상 요청은 무시을 의미함
		- 트리거용으로 생성된 폴더 'dirTmp'를 'dirCur'로 바꿔 스넵샷 저장을 지속한다.
		- 모든 이벤트 스넵샷은 'dirRoot'내에 저장된다.
		- 파일명에 A는 이벤트 발생 이전이고 Z는 이벤트 발생 이후의 스넵샷이지만
		- 카메라의 해상도와 캐싱과 관련하여 웹켐인 경우 640x480부터 이벤트 발생 시점이후(B) 프레임이 이전(A) 프레임에 저장되기도 한다.
		- 저해상도 일수록 시점이 일치 하는 경향을 보인다.
		- 최종 이벤트 관련 이미지 방의 웹접속을 위한 심벌릭 링크
		- 최종 이벤트 뷰 URL: http://ips.ip/theme/ecos-its_optex/utility/ubergallery/

참고:
	- 웹켐인 경우 기본 640 X 480 초당 20장 정도를 저장 한다.
	- 파일 생성일 초단위로 보는 명령
		ls -ltR --time-style=full-iso dirCur/

	- cntPostShotMax 값이 0 이상일떄
		스넵샷 요청이 빠르게 연속으로 들어와도 cntPostShotMax 횟수를 채운 후 다음 요청을 수용 한다.
	- cntPostShotMax 값이 0 일떄 1초 이내 다수의 요청은 폴더명을 변경하여 저장 한다.
		drwxr-xr-x 2 pi pi 4096 Mar 25 19:52 20210325_195218
		drwxr-xr-x 2 pi pi 4096 Mar 25 19:52 20210325_195218_1
		drwxr-xr-x 2 pi pi 4096 Mar 25 19:52 20210325_195218_1_1
		drwxr-xr-x 2 pi pi 4096 Mar 25 19:52 20210325_195218_1_1_1
		drwxr-xr-x 2 pi pi 4096 Mar 25 19:52 20210325_195218_1_1_1_1

'''

import os 
import time 
import cv2
import json
import subprocess 
import shutil
# import numpy as np

def make_1080p():
	cap.set(3, 1920)
	cap.set(4, 1080)

def make_720p():
	cap.set(3, 1280)
	cap.set(4, 720)

def make_480p(): # 기본값
	cap.set(3, 640)
	cap.set(4, 480)

def make_240p():
	cap.set(3, 320)
	cap.set(4, 240)

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

## 환경설정 파일(JSON)읽기
def readConfig(name):
	with open(name) as json_file:  
		return json.load(json_file)
	
## 환경설정 파일(JSON) 저장
def saveConfig(cfg,name):
	with open(name, 'w') as json_file: ## 저장
		json.dump(cfg, json_file, sort_keys=True, indent=4)

def main():
	maxCntPrev = cfg['camera']['cntPreShotMax']
	maxCntPost = cfg['camera']['cntPostShotMax']
	curCount = 0
	aftCount = 0

	eventOn = 0 # 이벤트가 들어왔으면

	status, frame = cap.read()
	# frames = np.empty([40, frame.shape[0], frame.shape[1], frame.shape[2]])

	if os.path.exists(cfg['camera']['dirTmp']):
		os.rmdir(cfg['camera']['dirTmp']) # 디랙토리 삭제
	if os.path.exists(cfg['camera']['lastEventShotLink']):
		os.unlink(cfg['camera']['lastEventShotLink']) # 심벌릭링크 삭제

	os.symlink(cfg['camera']['dirRoot'], cfg['camera']['lastEventShotLink']) # 최종 이벤트관련 이미지 방을 웹접속을 위한 심벌릭 링크

	while(True):

		ret, frame = cap.read()

		if not eventOn:
			cv2.imwrite('{}/A{:03d}.png'.format(cfg['camera']['dirCur'],curCount), frame)
			# 최종파일을 업데이트 한다.(실시간 모니터링을 위하여..)
			shutil.copyfile('{}/A{:03d}.png'.format(cfg['camera']['dirCur'],curCount), cfg['camera']['imgLast'])
			# print('{}/A{:03d}.png'.format(cfg['camera']['dirCur'],curCount), '{}/last.png'.format(cfg['camera']['dirRoot']))
			curCount += 1
			if curCount >= maxCntPrev: # 기본 스풀 카운터 
				curCount = 0
			# frames[curCount] = frame
		else:
			cv2.imwrite('{}/Z{:03d}.png'.format(cfg['camera']['dirCur'],aftCount), frame)
			aftCount += 1
			if aftCount >= maxCntPost: # 이벤트 발생이후 스넵샷 카운트를 모두 채웠으면 폴더 작업 실행
				aftCount = 0 # 리셋 이벤트 발생이후 스넵샷 카운트
				eventOn = 0

				dirSub = time.strftime(cfg['camera']['dirRoot'] + '/%Y%m%d_%H%M%S', time.localtime()) # 저장할 경로 + 펄더명

				# cntPostShotMax 량에 따라 적용(시간)이 가변적이다
				while True: # 1초 이내 1번 이상 요청이 들어오면 무시
					if os.path.exists(dirSub): # 1초 이내 1번 이상 요청이 들어오면 무시
						dirSub = '{}_1'.format(dirSub) # 저장할 경로명 변경
						continue
					else:
						break

				# if os.path.exists(dirSub): # 1초 이내 1번 이상 요청이 들어오면 
				# 	dirSub = '{}_1'.format(dirSub) # 저장할 경로명 변경

				os.rename(cfg['camera']['dirCur'], dirSub) # 현재폴더를 저장폴더로 경로변경
				os.rename(cfg['camera']['dirTmp'], cfg['camera']['dirCur']) # 빈 임시폴더를 현재폴더로 경로변경
				# # os.chmod(cfg['camera']['dirCur'],0o777)
				# if os.path.exists(cfg['camera']['lastEventShotLink']): 
				# 	os.unlink(cfg['camera']['lastEventShotLink'])

				# os.symlink(dirSub, cfg['camera']['lastEventShotLink']) # 최종 이벤트관련 이미지 방을 웹접속을 위한 심벌릭 링크

				# 폴더내 이미지 파일명 시간순으로 재정열
				cmd_proc_Popen('''n=0; ls -tr {0}/ | while read i; do n=$((n+1)); mv -- "{0}/$i" "$(printf '{0}/%03d' "$n")"_"$i"; done'''.format(dirSub))

		if os.path.exists(cfg['camera']['dirTmp']): # 임시폴더가 있으면 기본폴더를 현재 날째폴더로 바꾸고 임시폴더명을 기본폴더명으로 변경
			eventOn = 1

	cap.release()

if __name__ == '__main__':
	share = readConfig('/home/pi/common/config.json')
	# share['path']['its_web'],share['path']['user']['image']
	cfg = {}
	cfg['camera'] = {}
	cfg['camera']['camUrl'] = '/dev/video0'
	cfg['camera']['dirRoot'] = share['path']['its_web'] + share['path']['user']['image'] + '/camera'
	cfg['camera']['dirCur'] = cfg['camera']['dirRoot'] + '/dirCur'
	cfg['camera']['dirTmp'] = cfg['camera']['dirRoot'] + '/dirTmp'
	cfg['camera']['imgLast'] = cfg['camera']['dirRoot'] + '/last.png'
	cfg['camera']['lastEventShotLink'] = share['path']['its_web'] + '/theme/ecos-its_optex/utility/ubergallery/images'
	cfg['camera']['cntPreShotMax'] = 20
	cfg['camera']['cntPostShotMax'] = 30

	saveConfig(cfg,'./streaming.json')

	# 임시 폴더 삭제
	cmd_proc_Popen('rm -rf {}'.format(cfg['camera']['dirTmp']))
	cmd_proc_Popen('rm -rf {}'.format(cfg['camera']['lastEventShotLink']))
	
	cap = cv2.VideoCapture(cfg['camera']['camUrl'])
	if cap.read()[0]==False:
		print('Could not found Local Camera.')
		exit(0)

	make_480p() ## 해상도 설정

	if not os.path.exists(cfg['camera']['dirRoot']):
		os.makedirs(cfg['camera']['dirRoot'])
	os.chmod(cfg['camera']['dirRoot'],0o777)

	if not os.path.exists(cfg['camera']['dirCur']):
		os.makedirs(cfg['camera']['dirCur'])
	os.chmod(cfg['camera']['dirCur'],0o777)
	main()