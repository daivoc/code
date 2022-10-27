#!/usr/bin/env python
# -*- coding: utf-8 -*-  
			
import sys
import time
import socket 
import os, traceback, subprocess
import RPi.GPIO as GPIO
from multiprocessing import Process # 백그라운드 타이머 구동

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

portID = {}
portID[12]	= 'P01'
portID[8]	= 'P02'
portID[14]	= 'R485'
portID[15]  = 'T485'
portID[19]	= 'R01'
portID[13]	= 'R02'
portID[6]	= 'R03'
portID[5]	= 'R04'
portID[22]	= 'R05'
portID[27]	= 'R06'
portID[17]	= 'R07'
portID[4]	= 'R08'
portID[26]	= 'R09'
portID[21]	= 'R10'
portID[20]	= 'R11'
portID[16]	= 'R12'
portID[7]	= 'R13'
portID[25]	= 'R14'
portID[24]	= 'R15'
portID[23]	= 'R16'
portID[2]	= 'RSV1'
portID[3]	= 'RSV2'
portID[10]	= 'RSV3'
portID[9]	= 'RSV4'
portID[11]	= 'RSV5'
portID[0]	= 'RSV6'
portID[1]	= 'RSV7'
portID[18]	= 'RSV8'


def insert_socket_GPWIO(ip, id, status, msg): 
    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        # node.connect((ip,port))
        node.connect((ip, 18040))
        msg_data = ('id=%s,status=%s,msg=%s' % (id, status, msg))
        return node.send(msg_data) 
    except socket.error:
        return 0
    except socket.timeout:
        return 0
    finally:
        node.close() 

def main ():
    relayGPIO = [19,13,6,5,22,27,17,4,26,21,20,16,7,25,24,23]
    relay485 = [14,15]
    relayPower = [12,8]
    relayReserve = [2,3,10,9,11,0,1,18]
    ip = raw_input('Target(GPACU) IP: ')
    if ip:
        for count in range(100):
            for id in relayGPIO:
                insert_socket_GPWIO(ip, id=id, status=int(count % 2), msg='init')
                time.sleep(0.1)
    else:
        ## https://studymake.tistory.com/498
        try: # GPIO 포트 초기화
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False) # 경고 출력 무시
        except:
            print('Error GPIO Setmode.')

        ##########################################
        # GPIO.setup(id, GPIO.IN) # 값이 오락 가락 함 pull_up_down을 설정 해야 함
        # GPIO.setup(id, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        print('{}SET Input Mode{}').format(Y,X)
        for id in range(28): # 라즈베리파이의 전체 GPIO
            try: # GPIO 포트 PUD_DOWN으로 초기화
                GPIO.setup(id, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            except:
                print('%s Error GPIO port Init.' % id)
            statusA = GPIO.input(id)
            try: # GPIO 포트 PUD_UP으로 초기화
                GPIO.setup(id, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            except:
                print('%s Error GPIO port Init.' % id)
            statusB = GPIO.input(id)
            print("\tID:{}, {}:{}, {}:{}").format(id,'PUD_DOWN',statusA,'PUD_UP',statusA)

        ### Relay #######################################
        print('{}Relay Output Mode{}').format(Y,X)
        for count in range(10):
            sleepTime = float(1.0 / (count + 1))
            print('Count:{}{}/10{}, Sleep:{}').format(G,count + 1,X,sleepTime)
            for id in relayGPIO: # 라즈베리파이의 전체 GPIO
                try: # GPIO 포트 초기화
                    GPIO.setup(id, GPIO.OUT)
                except:
                    print('%s Error GPIO port Init.' % id)

                statusA = GPIO.input(id)

                # GPIO Set High
                GPIO.output(id, GPIO.HIGH)
                statusB = GPIO.input(id)

                time.sleep(sleepTime) # 1초를 카운터(+1)으로 나눔
                # GPIO Set Low
                GPIO.output(id, GPIO.LOW)
                statusC = GPIO.input(id)

                print("\tRelay #{} - ID:{}, {}:{} {}:{} {}:{}").format(portID[id],id,'PUD_DOWN',statusA,'HIGH',statusB,'LOW',statusC)

        ### Power #######################################
        print('{}Power Output Mode{}').format(Y,X)
        for count in range(10):
            sleepTime = float(1.0 / (count + 1))
            print('Count:{}{}/10{}, Sleep:{}').format(G,count + 1,X,sleepTime)
            for id in relayPower: # 라즈베리파이의 전체 GPIO
                try: # GPIO 포트 초기화
                    GPIO.setup(id, GPIO.OUT)
                except:
                    print('%s Error GPIO port Init.' % id)

                statusA = GPIO.input(id)

                # GPIO Set High
                GPIO.output(id, GPIO.HIGH)
                statusB = GPIO.input(id)

                time.sleep(sleepTime) # 1초를 카운터(+1)으로 나눔
                # GPIO Set Low
                GPIO.output(id, GPIO.LOW)
                statusC = GPIO.input(id)

                print("\tPower #{} - ID:{}, {}:{} {}:{} {}:{}").format(portID[id],id,'PUD_DOWN',statusA,'HIGH',statusB,'LOW',statusC)

        ### Reserve #######################################
        print('{}Reserve Output Mode{}').format(Y,X)
        for count in range(10):
            sleepTime = float(1.0 / (count + 1))
            print('Count:{}{}/10{}, Sleep:{}').format(G,count + 1,X,sleepTime)
            for id in relayReserve: # 라즈베리파이의 전체 GPIO
                try: # GPIO 포트 초기화
                    GPIO.setup(id, GPIO.OUT)
                except:
                    print('%s Error GPIO port Init.' % id)

                statusA = GPIO.input(id)

                # GPIO Set High
                GPIO.output(id, GPIO.HIGH)
                statusB = GPIO.input(id)

                time.sleep(sleepTime) # 1초를 카운터(+1)으로 나눔
                # GPIO Set Low
                GPIO.output(id, GPIO.LOW)
                statusC = GPIO.input(id)

                print("\tReserve #{} - ID:{}, {}:{} {}:{} {}:{}").format(portID[id],id,'PUD_DOWN',statusA,'HIGH',statusB,'LOW',statusC)

        ### 485 #######################################
        print('{}485 Output Mode{}').format(Y,X)
        for count in range(10):
            sleepTime = float(1.0 / (count + 1))
            print('Count:{}{}/10{}, Sleep:{}').format(G,count + 1,X,sleepTime)
            for id in relay485: # 라즈베리파이의 전체 GPIO
                try: # GPIO 포트 초기화
                    GPIO.setup(id, GPIO.OUT)
                except:
                    print('%s Error GPIO port Init.' % id)

                statusA = GPIO.input(id)

                # GPIO Set High
                GPIO.output(id, GPIO.HIGH)
                statusB = GPIO.input(id)

                time.sleep(sleepTime) # 1초를 카운터(+1)으로 나눔
                # GPIO Set Low
                GPIO.output(id, GPIO.LOW)
                statusC = GPIO.input(id)

                print("\t485 #{} - ID:{}, {}:{} {}:{} {}:{}").format(portID[id],id,'PUD_DOWN',statusA,'HIGH',statusB,'LOW',statusC)

        GPIO.cleanup()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ("\nCancelled")
    except Exception, e:
        print str(e)
        traceback.print_exc()
        os._exit(1)