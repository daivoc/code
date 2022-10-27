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
	# cap = cv2.VideoCapture('rtsp://admin:admin@96.48.233.195:5560') # Standard RTSP Camera
	# cap = cv2.VideoCapture('rtsp://admin:admin@192.168.0.113') # Standard RTSP Camera

응용:
	이벤트 발생:
		- 실행요청: echo '[{"camera":{"command":"footprint","value":""},"debug":true}]' | nc 192.168.0.90 34001 -q 0 
		- 완료보고: echo '[{"system":{"command":"saved_mDVR","value":"20220506_101420"},"debug":true}]' | nc 192.168.0.90 34001 -q 0
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
import glob

def saveIndexPHP(path, index_php):
	f = open("{}/index.php".format(path), "w")
	f.write(index_php)
	f.close

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

## 동영상 
def makeAVI(path,name):
	# 지금까지 MP4 생성은 오류 발생 AVI만 생성 가능한 상태임
	img_array = []
	for filename in glob.glob('{}/*.png'.format(path)):
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
		
	# out = cv2.VideoWriter('{}/{}.webm'.format(path,name),cv2.VideoWriter_fourcc(*'vp80'), 10, size) # Error 
	# out = cv2.VideoWriter('{}/{}.mp4'.format(path,name),cv2.VideoWriter_fourcc(*'H264'), 10, size) # Error 
	out = cv2.VideoWriter('{}/{}.avi'.format(path,name),cv2.VideoWriter_fourcc(*'DIVX'), 10, size) # Good
	for i in range(len(img_array)):
		out.write(img_array[i])
	out.release()

def main():
	maxCntPrev = cfg["camera"]["cntPreShotMax"]
	maxCntPost = cfg["camera"]["cntPostShotMax"]
	curCount = 0
	aftCount = 0

	eventOn = 0 # 이벤트가 들어왔으면

	if os.path.exists(cfg["camera"]["dirTmp"]):
		os.rmdir(cfg["camera"]["dirTmp"]) # 디랙토리 삭제
	if os.path.exists(cfg["camera"]["lastEventShotLink"]):
		os.unlink(cfg["camera"]["lastEventShotLink"]) # 심벌릭링크 삭제

	os.symlink(cfg["camera"]["dirRoot"], cfg["camera"]["lastEventShotLink"]) # 최종 이벤트관련 이미지 방을 웹접속을 위한 심벌릭 링크
	print('\nImages Location is http://localhost/mDVR')
	
	cap = cv2.VideoCapture(cfg["camera"]["camUrl"])
	if cap.read()[0]==False:
		print('Could not found Local Area Camera.')
		exit(0)
	
	while(True):
		ret, frame = cap.read()

		if not ret: # 이미지 켑쳐 오류 발생시 카메라 재설정 시도
			print('No Camera Image ... ')
			cap.release()
			time.sleep(1)
			cap = cv2.VideoCapture(cfg["camera"]["camUrl"])
			continue

		if not eventOn:
			cv2.imwrite('{}/A{:03d}.png'.format(cfg["camera"]["dirCur"],curCount), frame)

			curCount += 1
			if curCount >= maxCntPrev: # 기본 스풀 카운터 
				curCount = 0

		else:
			cv2.imwrite('{}/Z{:03d}.png'.format(cfg["camera"]["dirCur"],aftCount), frame)
			aftCount += 1
			if aftCount >= maxCntPost: # 이벤트 발생이후 스넵샷 카운트를 모두 채웠으면 폴더 작업 실행
				finTime = time.strftime('%Y%m%d_%H%M%S', time.localtime()) # 저장할 경로 + 펄더명
				dirSub = cfg["camera"]["dirRoot"] + '/' + finTime # 저장할 경로 + 펄더명

				# cntPostShotMax 량에 따라 적용(시간)이 가변적이다
				while True: # 1초 이내 1번 이상 요청이 들어오면 무시
					if os.path.exists(dirSub): # 1초 이내 1번 이상 요청이 들어오면 무시
						dirSub = '{}_1'.format(dirSub) # 저장할 경로명 변경
						continue
					else:
						break

				# if os.path.exists(dirSub): # 1초 이내 1번 이상 요청이 들어오면 
				# 	dirSub = '{}_1'.format(dirSub) # 저장할 경로명 변경

				os.rename(cfg["camera"]["dirCur"], dirSub) # 현재폴더를 날자명(dirSub)의 저장폴더로 경로변경
				os.rename(cfg["camera"]["dirTmp"], cfg["camera"]["dirCur"]) # 빈 임시폴더를 현재폴더로 경로변경
				aftCount = 0 # 리셋 이벤트 발생이후 스넵샷 카운트
				eventOn = 0 # 리셋 Post 스넵샷 중지

				# 폴더내 이미지 파일명 시간순으로 재정열
				cmd_proc_Popen('''n=0; ls -tr {0}/ | while read i; do n=$((n+1)); mv -- "{0}/$i" "$(printf '{0}/%03d' "$n")"_"$i"; done'''.format(dirSub))

				# 이미지 폴더내의 모든 파일을 동영상으로 변환 한다. - 아직 미완성임
				# makeAVI(dirSub,finTime) # 이미지목록을 비디오파일로 
				saveIndexPHP(dirSub, index_img_php) # 폴더내 이미지를 화면에 출력하는 PHP Code 저장

				if cfg["runItsAPI"]: # itsAPI가 실행 중이면 스넵샷 저장이 완료된 상태를 itsAPI.py에 알린다.
					cmd = '''echo '[{"system":{"command":"saved_mDVR","value":"'''+finTime+'''"},"debug":true}]' | nc '''+cfg["myIP"]+''' 34001 -q 0'''
					# print (cmd)
					cmd_proc_Popen(cmd)

		# 폴더 cfg["camera"]["dirTmp"]는 이벤트 발생을 의미하며 사용자 요정에 따른 이미지를 취합후 저장 한다.
		# 임시폴더가 있으면 기본폴더를 현재 날째폴더로 바꾸고 임시폴더명을 기본폴더명으로 변경
		# if os.path.exists(cfg["camera"]["dirTmp"]): 
		# 	eventOn = 1
		dirOn = os.path.exists(cfg["camera"]["dirOn"])
		dirTmp = os.path.exists(cfg["camera"]["dirTmp"])
		if dirOn and dirTmp: # 연속적인 요청으로 스넵샷 카운트를 확장 한다.
			os.rmdir(cfg["camera"]["dirOn"])
			if maxCntPost < 100: # 폴더내 최대 포스트 스넵샷 제한
				maxCntPost += aftCount # 스넵샷 카운트를 확장
		elif dirOn and not dirTmp:
			os.rename(cfg["camera"]["dirOn"], cfg["camera"]["dirTmp"]) # 빈 임시폴더를 현재폴더로 경로변경
			os.chmod(cfg["camera"]["dirTmp"],0o777)
			maxCntPost = cfg["camera"]["cntPostShotMax"] # 스넵샷 카운트를 초기화
			eventOn = 1
		elif not dirOn and dirTmp:
			eventOn = 1
		else:
			pass

		time.sleep(cfg["camera"]["holeTime"]) # hold time
		# print(cfg["camera"]["holeTime"])

	cap.release()

if __name__ == '__main__':
	# 본 프로그램은 일정량(사용자 지정)의 카메라 이미지는 지속적으로 저장 한다.
	# 외부로 부터 저장요청("footprint") 이벤트가 들어오거나(itsAPI 연동시)
	# 이미지 홈 폴더에 dirTmp 블랭크 폴더가 생성되면(독립적으로 동작시)
	# 이벤트 접수 시잠을 기준으로 일정량(사용자 지정)의 카메라 이미지를 추가로 저장한후
	# 저장된 이미지 폴더를 접수일시로 폴더명을 변경후 보관한다.
	# 프로그램명은 micro DVR(mDVR)로 명명한다.

	# 본 프로그램의 부모프로그램인 itsAPI.py로 부터 실행된다.
	# 환경값은 itsAPI.py로 부터 itsAPI.json을 상속 받는다.
	common = readConfig('/home/pi/common/config.json')
	# share = readConfig('/home/pi/API/config.json')
	streaming = readConfig('/home/pi/API/streaming.json')

	cfg = {}
	cfg["runItsAPI"] = 0
	if os.path.isfile('/home/pi/API/itsAPI.json'): # itsAPI.py로 부터 실행시
		itsAPI = readConfig('/home/pi/API/itsAPI.json')
		if itsAPI["camera"]["name"] and itsAPI["camera"]["config"]:
			cfg["camera"] = itsAPI["camera"]["config"]
			cfg["camera"]["name"] = itsAPI["camera"]["name"]
			cfg["camera"]["dirRoot"] = itsAPI["mDVR"]["dirRoot"]
			cfg["camera"]["dirCur"] = itsAPI["mDVR"]["dirCur"]
			cfg["camera"]["dirTmp"] = itsAPI["mDVR"]["dirTmp"]
			cfg["camera"]["dirOn"] = itsAPI["mDVR"]["dirOn"]
			cfg["camera"]["imgLast"] = itsAPI["mDVR"]["imgLast"]
			cfg["camera"]["lastEventShotLink"] = common["path"]["its_web"] + '/mDVR'
			cfg["runItsAPI"] = 1
			cfg["myIP"] = itsAPI["tcpIpPort"]["staticAddress"]
		else:
			print('Disabled mDVR.')
			exit(0)
	else: # 독립적으로 실행시 기본 시스템카메라(local)를 실행한다.
		camName = "local" # 필요에 따라 streaming.json내 키값을 선언할수 있다. 예: axis, walkerSt ..
		cfg["camera"] = streaming[camName]
		cfg["camera"]["name"] = camName
		cfg["camera"]["dirRoot"] = common["path"]["its_web"] + common["path"]["user"]["image"] + '/'+camName
		cfg["camera"]["dirCur"] = cfg["camera"]["dirRoot"] + '/dirCur'
		cfg["camera"]["dirTmp"] = cfg["camera"]["dirRoot"] + '/dirTmp'
		cfg["camera"]["dirOn"] = cfg["camera"]["dirRoot"] + '/dirOn'
		cfg["camera"]["imgLast"] = cfg["camera"]["dirRoot"] + '/last.png'
		cfg["camera"]["lastEventShotLink"] = common["path"]["its_web"] + '/mDVR'

	print('\nCamera name: {}'.format(cfg["camera"]["name"]))

	index_img_php = '''<?php 
	echo '<html>
	<style>
	body { background: black; }
	img { width: calc(100%/6 - 4px); margin: 1px; border: 1px solid gray; }
	</style>
	<body>';

	$images = glob("./*.png");
	echo '<div>';
	foreach($images as $image){
		echo '<a href='.$image.' target=_blank><img src='.$image.'></a>';
	}
	echo '</div>';

	// $videos= glob("./*.mp4");
	// echo '<div>';
	// foreach($videos as $video){
	// 	echo '<video width="320" height="240" controls>
	// 		<source src='.$video.' type="video/mp4">Your browser does not support the video tag.
	// 	</video>';
	// }
	// echo '</div>';

	echo '</body></html>';
	?>'''

	index_dir_php = '''<?php 
	echo '<html>
	<style>
	body {{ background:black; }}
	.image {{ width:calc(100vw/8 - 1px); height:calc(100vw/8*0.6 - 1px); text-align:center; color:silver; display:inline-block; font-size:1vh; margin:1px; border:1px solid gray; }}
	</style>
	<body>';

	$folders = glob('*', GLOB_ONLYDIR);
	echo '<div class="images">';
	foreach($folders as $folder){{
		$files = scandir ($folder);
		$titleImg = './'.$folder.'/'.$files[{0}];
		if (strlen($folder) == 15) {{ // filtering 20220508_165955
			echo '<a href=./'.$folder.' target=_blank><span class="image" style="background-image: url('.$titleImg.'); background-position: center; background-size: cover;">'.$folder.'</span></a>';
		}}
	}}
	echo '</div>';

	echo '</body></html>';
	?>'''.format(cfg["camera"]["cntPreShotMax"] + 2) # ., ..을 제외한 cntPreShotMax번째 이미지 번호

	# 임시 폴더 삭제
	cmd_proc_Popen('rm -rf {}'.format(cfg["camera"]["dirTmp"]))
	cmd_proc_Popen('rm -rf {}'.format(cfg["camera"]["lastEventShotLink"]))

	if not os.path.exists(cfg["camera"]["dirRoot"]):
		os.makedirs(cfg["camera"]["dirRoot"])
	os.chmod(cfg["camera"]["dirRoot"],0o777)
	saveIndexPHP(cfg["camera"]["dirRoot"], index_dir_php)

	if not os.path.exists(cfg["camera"]["dirCur"]):
		os.makedirs(cfg["camera"]["dirCur"])
	os.chmod(cfg["camera"]["dirCur"],0o777)
	main()