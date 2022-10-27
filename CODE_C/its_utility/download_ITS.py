#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import sys
import socket
from datetime import datetime

def is_connected(hostname): # 다운로드 서버 접속 유무 확인
	try:
		# see if we can resolve the host name -- tells us if there is
		# a DNS listening
		host = socket.gethostbyname(hostname)
		# connect to the host -- tells us if the host is actually
		# reachable
		# s = socket.create_connection((host, 80), 2)
		s = socket.create_connection((host, 22), 2)
		s.close()
		return True
	except:
		pass

	return False

def main():	
	# 기존 프로그램 백업
	if progName is 'web' or progName is 'LIST':
		pass
	else:
		if os.path.isdir(sourceDir):
			responseBackup = os.system("cp -R %s %s" % (sourceDir, targetDir))
			if responseBackup == 0:
				print "Backup %s" % targetDir
			else:
				print "Error backup %s" % targetDir
		else:
			# 신규인 경우 폴더 생성
			os.makedirs(sourceDir)

	# 원격 다운로드 프로그램 실행
	runCommand = remoteCmd[progName].replace("__IP__",serverIP)
	runCommand = runCommand.replace("__PATH__",pathName)
	os.system(runCommand)
	# print(runCommand)
	
if __name__ == '__main__':
	# 다운로드 가능한 프로그램 목록
	# sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete --exclude='node_modules' ./optex_BIND/ pi@${ADDR[0]}:optex_BIND >/dev/null 2>&1

	remoteCmd = { # remoteCmd['GPIO'] -> GPIO
		'LIST':'rsh pi@__IP__ "ls -d ecos_its-*"',
		'BIGDATA':'rsync -avzr pi@__IP__:__PATH__/its_BIGDATA/BIGDATA ~',
		'CAM':'rsync -avzr pi@__IP__:__PATH__/its_CAM/CAM ~',
		'COUNTER':'rsync -avzr pi@__IP__:__PATH__/its_COUNTER/COUNTER ~',
		'GPIO':'rsync -avzr pi@__IP__:__PATH__/its_GPIO/GPIO ~',
		'GPCIO':'rsync -avzr pi@__IP__:__PATH__/its_GPCIO/GPCIO ~',
		'GPWIO':'rsync -avzr pi@__IP__:__PATH__/its_GPWIO/GPWIO ~',
		'GPACU':'rsync -avzr pi@__IP__:__PATH__/its_GPACU/GPACU ~',
		'MON_TBL':'rsync -avzr pi@__IP__:__PATH__/its_MON_TBL/MON_TBL ~',
		'MONITOR':'rsync -avzr pi@__IP__:__PATH__/its_MONITOR/MONITOR ~',
		'GIKENP':'rsync -avzr pi@__IP__:__PATH__/its_partner/its_GIKENP/GIKENP ~',
		'GIKENT':'rsync -avzr pi@__IP__:__PATH__/its_partner/its_GIKENT/GIKENT ~',
		'SRF':'rsync -avzr pi@__IP__:__PATH__/its_partner/its_SRF/SRF ~',
		'BIND':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_BIND/optex_BIND ~',
		'BSS':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_BSS/optex_BSS ~',
		'BSS_R':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_BSS_R/optex_BSS_R ~',
		'RLS':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_RLS/optex_RLS ~',
		'RLS_R':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_RLS_R/optex_RLS_R ~',
		'SPEED':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_SPEED/optex_SPEED ~',
		'VEHICLE':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_VEHICLE/optex_VEHICLE ~',
		'PARKING':'rsync -avzr pi@__IP__:__PATH__/its_optex/optex_PARKING/optex_PARKING ~',
		'common':'rsync -avzr pi@__IP__:__PATH__/its_common/common ~',
		'utility':'rsync -avzr pi@__IP__:__PATH__/its_utility/utility ~',
		'web':'rsync -avzr --delete --exclude="data" pi@__IP__:__PATH__/its_web /var/www/html'
	}

	defaultIP = '115.139.183.226'
	defaultPath = 'ecos_its-OPTEX'

	# 입력하는 변수(다운로드 서버 아이피, 프로그램명) 확인
	if(len(sys.argv) >= 3):
		root='/home/pi'
		postName = datetime.today().strftime('%Y%m%d')
		serverIP = sys.argv[1] # 다운로드 서버 아이피
		progName = sys.argv[2] # 프로그램명
		if(len(sys.argv) == 3):
			pathName = root + "/" + defaultPath # 기본 폴더명 
		else:
			pathName = root + "/" + sys.argv[3] # 경로명 예: ecos_its-OPTEX_20200902_DSSC_Updated

		sourceDir = "%s/%s" % (root, progName)
		targetDir = "%s_%s" % (sourceDir, postName)
	else: # 도움말 출력
		lists = '\nProgram Lists:\n'
		for key, value in sorted(remoteCmd.items()):
			# print (key, value)
			lists += '[' + key + '] '
		print lists + '\n'

		print("Usage Ex1: python %s %s LIST" % (sys.argv[0], defaultIP))
		print("Usage Ex2: python %s %s GPIO" % (sys.argv[0], defaultIP))
		print("Usage Ex3: python %s %s GPIO Folder_name" % (sys.argv[0], defaultIP))
		exit()

	# 다운로드 서버 접속 유무 확인
	if is_connected(serverIP) == True:
		pass
	else:
		print "Error network connect %s" % serverIP
		exit()

	# 요청 프로그램 검증
	if progName in remoteCmd:
		pass
	else:
		print("Error: Not found program %s in server lists" % progName)
		exit()

	main()