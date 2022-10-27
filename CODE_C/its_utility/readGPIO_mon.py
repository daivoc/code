#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import RPi.GPIO as GPIO
import os, traceback
from datetime import datetime

# http://mydb.tistory.com/245
# http://studymake.tistory.com/498

def setRed(text):
	return '\033[31m'+str(text)+'\033[39m'
def setGreen(text):
	return '\033[32m'+str(text)+'\033[39m'
def setYellow(text):
	return '\033[33m'+str(text)+'\033[39m'
def setCyan(text):
	return '\033[35m'+str(text)+'\033[39m'
def setBlack(text):
	return '\033[37m'+str(text)+'\033[39m'

def setRed_R(text):
	return '\033[41m'+'\033[30m'+str(text)+'\033[39m'+'\033[49m'
def setGreen_R(text):
	return '\033[42m'+'\033[30m'+str(text)+'\033[39m'+'\033[49m'
def setYellow_R(text):
	return '\033[43m'+'\033[30m'+str(text)+'\033[39m'+'\033[49m'
def setCyan_R(text):
	return '\033[46m'+'\033[30m'+str(text)+'\033[39m'+'\033[49m'
def setBlack_R(text):
	return '\033[47m'+'\033[30m'+str(text)+'\033[39m'+'\033[49m'

def main ():
	portID = [19,13,6,5,22,27,17,4]

	userInput = input("Enter a GPIO ID(1~8): ")
	portNum = int(userInput) - 1
	gpioID = portID[portNum]

	sleep_cycle = 0.1	# 데이터 픽업 주기 초
	heart_limit = 10	# 하트비트 시간 주기 10회 = 1초
	error_limit = heart_limit	# 오류 대기 시간 주기 1분

	count_sub = 0		# 이벤트 카운터
	count_rise = 0		# 이벤트 업 카운터
	count_down = 0		# 이벤트 다운 카운터

	event_curr = 0		# 지금 이벤트
	event_last = 0		# 과거 이벤트

	rise_event = 0		# 업 이벤트
	down_event = 0		# 다운 이벤트

	error_event = 0		# 오류 이벤트

	# 실제 GPIO Port 는 2/3번 사용 제한 실제 4번 부터 27번
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 아마도 NC Mode: 스위치 안눌렸을 때 on, 눌렸을 때 off

	while True:
		status = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

		if modeNC:
			event_curr = GPIO.input(gpioID)
		else:
			event_curr = not GPIO.input(gpioID)

		rise_event = 0 # 리셋 업 이벤트
		down_event = 0 # 리셋 다운 이벤트
		
		if event_last is event_curr: # 이전 이벤트가 지속되면 
			count_sub += 1
		else: # 지금 이벤트 바뀠으면
			count_sub = 0
			
			if event_curr: # 업 이벤트로 바뀠으면
				rise_event = 1
				rise_event = setYellow_R(rise_event)
				down_event = 0
				down_event = setGreen_R(down_event)
				curr_event = setBlack(event_curr)
				dire_event = "\t%s >>>>>> - "%userInput
			else: # 다운 이벤트로 바뀠으면
				rise_event = 0
				rise_event = setCyan_R(rise_event)
				down_event = 1
				down_event = setRed_R(down_event)
				curr_event = setBlack_R(event_curr)
				dire_event = "\t%s <<<<<< - "%userInput

			print "%1s %1s %2s %1s %2s %s %1s" % (dire_event, rise_event, setGreen(count_rise), down_event, setCyan(count_down), status, curr_event)
		event_last = event_curr

	############################################################################################
	############################################################################################
	############################################################################################

if __name__ == '__main__':

	modeNC = False # False # True
	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)