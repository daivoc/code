#!/usr/bin/python
# -*- coding: utf-8 -*-

## https://gitlab.com/bambusekd-dev-blog/raspberry-measure-distance-jsn-sr04t/blob/master/distance.py

# Import required Python libraries
import time               # library for time reading time
import RPi.GPIO as GPIO   # library to controll Rpi GPIOs
import socket 

def initPortGPIO(GPIO_TRIG, GPIO_ECHO):
	GPIO.setwarnings(False) # Disable warnings
	GPIO.setmode(GPIO.BCM) # We will be using the BCM GPIO numbering
	GPIO.setup(GPIO_TRIG,GPIO.OUT) # Select which GPIOs you will use, Set TRIGGER to OUTPUT mode
	GPIO.setup(GPIO_ECHO,GPIO.IN) # Set ECHO to INPUT mode
	GPIO.output(GPIO_TRIG, False) # Set TRIGGER to LOW
	time.sleep(0.5) # Let the sensor settle for a while

def getEventGPIO(GPIO_TRIG, GPIO_ECHO):
	GPIO.output(GPIO_TRIG, True) # set TRIGGER to HIGH
	time.sleep(0.00001) # Send 10 microsecond pulse to TRIGGER and wait 10 microseconds
	GPIO.output(GPIO_TRIG, False) # set TRIGGER back to LOW
	start = time.time() # Create variable start and give it current time
	stop = start # Create variable start and give it current time
	while GPIO.input(GPIO_ECHO)==0: # Refresh start value until the ECHO goes HIGH = until the wave is send
		start = time.time()
	while GPIO.input(GPIO_ECHO)==1: # Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW
		stop = time.time()
	measuredTime = stop - start # Calculate the time it took the wave to travel there and back
	distanceBothWays = measuredTime * 33112 # # Calculate the travel distance by multiplying the measured time by speed of sound - cm/s in 20 degrees Celsius
	distance = int(distanceBothWays / 2) # Divide the distance by 2 to get the actual distance from sensor to obstacle, distance = distanceBothWays / 2
	return distance
	
################ Socket.io 
def insert_socket_monitor_COUNTER(ip, port, serial, subject, nameIs, valueIs): 
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((ip,port))
		msg_data = ('ip=%s,nameIs=%s,valueIs=%s' % (ip, nameIs, valueIs))
		node.send(msg_data) 
		node.close() 
		return ("status_msg")
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 

def main():

	COUNTER_system_ip = "192.168.0.9"
	COUNTER_table_PortIn = 8321
	COUNTER_sensor_serial = "COUNTER_sensor_serial"
	COUNTER_subject = "COUNTER_subject"

	L_TRIG = 5
	L_ECHO = 6
	R_TRIG = 13
	R_ECHO = 19
	T_TRIG = 22
	T_ECHO = 27
	
	initPortGPIO(L_TRIG, L_ECHO)
	initPortGPIO(R_TRIG, R_ECHO)

	CNT_minDist = 20 # cm ?????? ?????? ??????
	CNT_maxDist = 100 # cm ?????? ?????? ??????
	CNT_pickCycle = 0.2 # ????????????

	moveIN = '' ## Start Name
	moveOUT = '' ## End Name

	doubleIN = 0 ## Double Start
	doubleOUT = 0 ## Double End
	
	total_L = 0
	total_R = 0
	
	eventOn = 0
	
	while(1):
		dist_L = getEventGPIO(L_TRIG, L_ECHO)
		dist_R = getEventGPIO(R_TRIG, R_ECHO)
		
		insert_socket_monitor_COUNTER(COUNTER_system_ip, COUNTER_table_PortIn, COUNTER_sensor_serial, COUNTER_subject, "dist_L", dist_L)
		insert_socket_monitor_COUNTER(COUNTER_system_ip, COUNTER_table_PortIn, COUNTER_sensor_serial, COUNTER_subject, "dist_R", dist_R)
		
		if dist_L > CNT_maxDist and dist_R > CNT_maxDist: ## ??????????????? ????????? ???????????? ????????????
			if moveIN and moveOUT and moveIN is not moveOUT: ## ?????? ??????
				eventOn = 1
			elif doubleIN and moveOUT: ## ???????????? ?????? ??????
				eventOn = 2
			elif moveIN and doubleOUT: ## ???????????? ?????? ??????
				eventOn = 3
			else: 
				if doubleOUT and doubleIN: ## ?????? ??????
					print "LR:LR", "\a"
				else:
					if moveIN or moveOUT or doubleIN or doubleOUT:
						print "moveIN:%s moveOUT:%s doubleIN:%s doubleOUT:%s" % (moveIN, moveOUT, doubleIN, doubleOUT)
					
				eventOn = 0
				moveIN = ''
				moveOUT = ''
				doubleIN = 0
				doubleOUT = 0
				pass # ????????? ???????????? continue
				
		elif dist_L < CNT_maxDist and dist_R < CNT_maxDist: ## ??????????????? ????????? ???????????? ?????? ????????????
			if moveIN: ## ?????? ????????? - ???????????? ??????
				doubleOUT = 1
				moveOUT = '' ## Single Out ??????
			else: ## ?????? ????????? -???????????? ??????
				doubleIN = 1
			continue # ????????? ???????????? 
		else:
			if doubleIN: ## ?????? ????????? - ???????????? ??????
				if dist_L < dist_R:
					moveOUT = 'L'
				else:
					moveOUT = 'R'
				doubleOUT = 0 ## Double Out ??????
			else: ## ?????? ????????? -???????????? ??????
				if dist_L < dist_R:
					moveIN = 'L'
				else:
					moveIN = 'R'
			continue # ????????? ???????????? 
		
		if eventOn:
			## ?????? ??????
			if moveIN == 'L': total_L += 1
			if moveIN == 'R': total_R += 1
			
			## ?????? ??????
			insert_socket_monitor_COUNTER(COUNTER_system_ip, COUNTER_table_PortIn, COUNTER_sensor_serial, COUNTER_subject, "moveOut", CNT_maxDist)

			print moveIN, eventOn, total_L, total_R
		
			eventOn = 0
 			moveIN = ''
			moveOUT = ''
			doubleIN = 0
			doubleOUT = 0

		time.sleep(CNT_pickCycle) # wait 10 miliseconds
	# Reset GPIO settings
	GPIO.cleanup()
	
# Run the main function when the script is executed
if __name__ == "__main__":
    main()

