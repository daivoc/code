#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# GPIO Port ID 12번에 연결된 센서전원(12v)을 일시적(5초)으로 차단(Reset)한다.

# GPIO  웹에서 관리하려면
# https://raspberrypi.stackexchange.com/questions/40105/access-gpio-pins-without-root-no-access-to-dev-mem-try-running-as-root
# $ sudo vi /etc/group
	# gpio:x:997:pi,www-data
# 또는 
# $ sudo adduser www-data gpio

import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)

def alarmOut(): # GPIO Port No. , Action Due
	GPIO.output(12, True)
	time.sleep(5) ## Wait one second
	GPIO.output(12, False)

if __name__ == '__main__':
	print "Turn off the sensor for 5 seconds."
	alarmOut()
	print "Turn On Sensors"
	exit()			
