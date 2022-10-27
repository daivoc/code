#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# # # gpio-interrupt-test.py
# # GPIO12에 입력이 들어오면 문장을 출력한다.
# # 라이브러리 불러오기
# import RPi.GPIO as GPIO
# import time

# # 스위치 눌렸을 때 콜백함수
# def switchPressed(channel):
# 	print('channel %s Pressed'%channel)

# gpioID = int(raw_input("Enter a GPIO Port ID(1~27): "))
# if 0 < gpioID < 40:
# 	pass
# else:
# 	exit("Need gpioID (1~27)")

# # GPIO setup
# GPIO.setmode(GPIO.BCM)
# # GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 아마도 NO Mode: 스위치 안눌렸을 때 off, 눌렸을 때 on
# GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 아마도 NC Mode: 스위치 안눌렸을 때 on, 눌렸을 때 off

# # interrupt 선언
# # GPIO.add_event_detect(gpioID, GPIO.BOTH, callback=switchPressed, bouncetime=1000)
# GPIO.add_event_detect(gpioID, GPIO.RISING, callback=switchPressed, bouncetime=1000)
# # GPIO.add_event_detect(gpioID, GPIO.FALLING, callback=switchPressed, bouncetime=1000)
# GPIO.event_detected(gpioID)

# # 메인 쓰레드
# try:
# 	while 1:
# 		print(".")
# 		time.sleep(0.1)
# finally:
# 	GPIO.cleanup()




import time
import RPi.GPIO as GPIO
import os, traceback

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

def port_input(message):
   try:
      ret = int(input(message))
      return ret
   except:
      return port_input("Enter a GPIO Port ID(1~27): ")

def main ():

	gpioID = port_input("Enter a GPIO Port ID(1~27): ")
	if 0 < gpioID < 40:
		pass
	else:
		exit("Need gpioID (1~27)")

	sleep_cycle = 0.1	# 데이터 픽업 주기 초
	heart_limit = 10	# 하트비트 시간 주기 10회 = 1초
	active_limit = heart_limit * 3	# 감지 대기 시간 10초
	error_limit = heart_limit * 9	# 오류 대기 시간 주기 1분

	count_all = 0		# 전체 시작 카운터
	count_sub = 0		# 이벤트 카운터
	count_rise = 0		# 이벤트 업 카운터
	count_down = 0		# 이벤트 다운 카운터

	event_curr = 0		# 지금 이벤트
	event_last = 0		# 과거 이벤트

	heart_event = 0		# 하트비트 이벤트

	rise_event = 0		# 업 이벤트
	down_event = 0		# 다운 이벤트

	error_event = 0		# 오류 이벤트

	print """
	sleep_cycle =	%s	# 데이터 픽업 주기 초
	heart_limit =	%s	# 하트비트 주기 10회 = 1초
	active_limit =	%s	# 감지 대기 시간 초
	error_limit =	%s	# 오류 대기 시간 초
	"""%(sleep_cycle,heart_limit,active_limit/10,error_limit/10)

	# 실제 GPIO Port 는 2/3번 사용 제한 실제 4번 부터 27번
	GPIO.setmode(GPIO.BCM)

	# if modeNC:
	# 	GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 아마도 NC Mode: 스위치 안눌렸을 때 on, 눌렸을 때 off
	# else:
	# 	GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 아마도 NO Mode: 스위치 안눌렸을 때 off, 눌렸을 때 on

	GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 아마도 NC Mode: 스위치 안눌렸을 때 on, 눌렸을 때 off
	# GPIO.setup(gpioID, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 아마도 NO Mode: 스위치 안눌렸을 때 off, 눌렸을 때 on

	while True:
		status = time.strftime('%H:%M:%S')

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
				rise_event = setBlack_R(rise_event)
				count_rise += 1 # 업 이벤트 카운터 추가
				status = "%s - On" % status
			else: # 다운 이벤트로 바뀠으면
				down_event = 1
				down_event = setBlack_R(down_event)
				count_down += 1 # 다운 이벤트 카운터 추가
				status = "%s - Off" % status
			
		heart_event = 0
		error_event = 0
		if event_curr:
			# 감지 상태이며 count_sub가 error_limit의 배수이면 센서오류 이밴트 발생
			# if count_sub and (count_sub > error_limit) is 0: # 샌서 단선 또는 전원 오류
			if count_sub and count_sub > error_limit: # 샌서 단선 또는 전원 오류
				error_event = 1
				error_event = setRed_R(error_event)
				status = "%s - ERROR" % status
		else:
			# 비감지 상태이며 count_sub가 heart_limit의 배수이면 하트비트 이밴트 발생
			if count_sub and (count_sub % heart_limit) is 0: # 정상 동작으로 주기에 따른 하트비트 발생
				heart_event = 1
				heart_event = setRed_R(heart_event)
				
			# if count_sub > active_limit: # 감지 대기 시간에 따른 이벤트 활성상황 종료
				# count_rise = 0 # 리셋 업 카운터
				# count_down = 0 # 리셋 다운 카운터
				
			if count_sub and active_limit and (count_sub % active_limit) is 0: # 감지 대기 시간에 따른 이벤트 활성상황 종료
				count_rise = 0 # 리셋 업 카운터
				count_down = 0 # 리셋 다운 카운터
				status = "%s - Reset" % status

		event_last = event_curr

	############################################################################################
	############################################################################################
	############################################################################################
		
		count_all += 1
		if event_curr or heart_event or error_event or rise_event or down_event:
			if (count_sub % active_limit) is 0:
				# string_val = "#" * len(str(count_sub))  # gives you "xxxxxxxxxx"
				print "\n  COUNT SUB# S H E up# dn# Time" # .format(string_val)
			print "%7s %4s %1s %1s %1s %1s %2s %1s %2s %s" % (count_all, count_sub, event_curr, heart_event, error_event, rise_event, setGreen_R(count_rise), down_event, setCyan_R(count_down), status)

		time.sleep(sleep_cycle)


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