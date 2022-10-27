#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# 리브팅시 일정시간내에 GPIO 8번째 접점을 5번 접지시 
# 임시 아이피(192.168.0.99) 설정 기능

import time
import os, traceback
import subprocess
import RPi.GPIO as GPIO
	
def setDefaultIP(ITS_iface, ITS_newIP, action):
	cmd = "sudo ifconfig %s %s %s" % (ITS_iface, ITS_newIP, action)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return p.stderr

def main ():

	sleep_cycle = 1	# 데이터 픽업 주기 초
	
	# 액티브듀가 액티브타임 이내값에 액티브카운트 횟수이상이면 실행
	active_time = 10 * 2	# 감지 대기 시간 10회 = 1초
	active_due = 0	
	active_count = 3
	active_action = 0	# 0: none, 1: on, 2: off
	
	count_all = 0		# 전체 시작 카운터
	count_sub = 0		# 이벤트 카운터
	count_rise = 0		# 이벤트 업 카운터
	count_down = 0		# 이벤트 다운 카운터
	count_hold = 300	# 대기시간 (초)

	event_curr = 0		# 지금 이벤트
	event_last = 0		# 과거 이벤트

	curr_action = 0
	last_action = 0
	
	while True:
		event_curr = GPIO.input(GPIO_ID)

		if event_last is not event_curr: # 이벤트 바뀌면
			if event_curr: # 업 이벤트면
				count_rise += 1 # 업 이벤트 카운터 추가
			else: # 다운 이벤트면
				count_down += 1 # 다운 이벤트 카운터 추가

				active_due = count_all - count_sub # End Count

				if(count_down == 1): # First Count
					count_sub = count_all
				elif(count_down == active_count): # Reset
					if(active_due < active_time): # 툭정시간 이내에 발생한 이벤트이면
						active_action += 1
						curr_action = active_action % 2
						## 임시 아이피 설정 및 해지
						if(curr_action is not last_action):
							if curr_action:
								print("Enable IP:%s."%ITS_newIP)
								setDefaultIP(ITS_iface, ITS_newIP, "up")
							else:
								print("Disable IP:%s."%ITS_newIP)
								setDefaultIP(ITS_iface, ITS_newIP, "down")
						last_action = curr_action
					count_all = 0
					count_down = 0
					count_sub = 0
				else:
					if(active_due > active_time): # 타임아웃
						count_all = 0
						count_down = 0
						count_sub = 0
			
		if(count_all > count_hold):
			print(ITS_iface, ITS_newIP, "down")
			setDefaultIP(ITS_iface, ITS_newIP, "down")
			exit("Timeout Close.") # count_hold -> 5분 일정시간이 지나면 종료한다.
		else:
			if count_all % 60 is 0:
				print "%s/%s Sec" % (count_all, count_hold)
		# print count_all, count_down, active_due, active_action

		count_all += 1
		event_last = event_curr
		time.sleep(sleep_cycle)

if __name__ == '__main__':

	ITS_iface = "eth0:0"
	ITS_newIP = "192.168.0.99"
	GPIO_ID = 4

	# 실제 GPIO Port 는 2/3번 사용 제한 실제 4번 부터 27번
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(GPIO_ID, GPIO.IN, pull_up_down = GPIO.PUD_UP)

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)