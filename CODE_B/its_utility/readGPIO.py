#!/usr/bin/env python
# -*- coding: utf-8 -*-  
			
import sys
import time
import RPi.GPIO as GPIO
from multiprocessing import Process # 백그라운드 타이머 구동

# http://mydb.tistory.com/245
# http://studymake.tistory.com/498

GPIO.setmode(GPIO.BCM)

# def alarmOut(port, druation): # GPIO Port No. , Action Due
	# GPIO.setup(port, GPIO.OUT)
	# GPIO.output(port, GPIO.HIGH)
	# GPIO.output(port, False) ## On 17
	# time.sleep(druation) ## Wait one second
	# GPIO.output(port, True) ## Off 17
# Process(target=alarmOut, args=(2,7)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(3,5)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(4,3)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(5,1)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(6,5)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(7,5)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(8,2)).start()
# time.sleep(0.1)
# Process(target=alarmOut, args=(9,2)).start()
# time.sleep(0.1)

###########################################################

K  = '\033[30m' # : 글자색:검정
R  = '\033[31m' # : 글자색:빨강
G  = '\033[32m' # : 글자색:초록
Y  = '\033[33m' # : 글자색:노랑
B  = '\033[34m' # : 글자색:파랑
M  = '\033[35m' # : 글자색:마젠트(분홍)
C  = '\033[36m' # : 글자색:시안(청록)
W  = '\033[37m' # : 글자색:백색
X  = '\033[39m' # : 글자색으로 기본값으로

BK  = '\033[40m' # : 바탕색:흑색
BR  = '\033[41m' # : 바탕색:적색
BG  = '\033[42m' # : 바탕색:녹색
BY  = '\033[43m' # : 바탕색:황색
BB  = '\033[44m' # : 바탕색:청색
BM  = '\033[45m' # : 바탕색:분홍색
BC  = '\033[46m' # : 바탕색:청록색
BW  = '\033[47m' # : 바탕색:흰색
BX  = '\033[49m' # : 바탕색을 기본값으로

write = sys.stdout.write

# 실제 GPIO Port 는 2/3번 사용 제한 실제 4번 부터 27번
gpio_start = 1
gpio_end = 28

count = 0
count_max = 999 # default 99 회
start = time.time()
if len(sys.argv) > 1:
	count_max = sys.argv[1]

# for x in range (gpio_start, gpio_end):
for x in range (gpio_end):
	# GPIO.setup(x, GPIO.IN) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
	# GPIO.setup(x, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(x, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
while True:
	count += 1
	if int(count) > int(count_max):
		exit()
		
	write(BW+R+" %6s "%count+X+BX+"|") #
	# for y in range (gpio_start, gpio_end):
	for y in range (gpio_end):
		if GPIO.input(y):
			write("%s|"%y) #
		else:
			write(BW+K+"%s"%y+X+BX+"|") #
	end = time.time()
	print(end - start)
	start = end
	time.sleep(0.1)
	
