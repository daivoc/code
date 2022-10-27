#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import sys
import time
import RPi.GPIO as GPIO
from multiprocessing import Process # 백그라운드 타이머 구동
import traceback, os

# http://mydb.tistory.com/245
# http://studymake.tistory.com/498

def alarmOut(port, druation): # GPIO Port No. , Action Due
	GPIO.setup(port, GPIO.OUT)
	GPIO.output(port, GPIO.HIGH)
	time.sleep(druation) ## Wait one second
	GPIO.output(port, GPIO.LOW)

def main():
	count = 0
	count_max = 15000 # default 99 회
	relayGroup = [19,13,6,5,22,27,17,4,26,21,20,16,7,25,24,23]

	while True:
		count_max -= 1
		if int(count) == int(count_max):
			exit()

		for id in relayGroup:
			Process(target=alarmOut, args=(id,1)).start()
			sys.stdout.write('.')
			time.sleep(0.1)
		print(count_max)

if __name__ == '__main__':
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		os._exit(1)

