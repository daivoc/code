#!/usr/bin/env python

# http://112.187.234.55/optex_web/bbs/board.php?bo_table=g100t200&wr_id=12

import sys
import socket
import struct
import fcntl
import subprocess
import os, traceback
from datetime import datetime

def get_ip_address(ifname): # get_ip_address('eth0')  # '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def main():
	file = open("./ping_arp.txt","w") 
	
	for ips in range(2,255):  
		ip = '%s.%s'%(ip_class,ips)
		
		ping_arp = '' # 파일저장 버퍼

		if ip == myIP:
			continue

		p = subprocess.Popen(['ping', ip, '-c1 -w1 -W1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		# print out
		if out:
			# print ip, out.split('\n')[4]
			if ('Unreachable' in out):
				ip_mac = '%s\tUnreachable\t'%ip
				active = 0
			else:
				ip_mac = '%s\tActive\t'%ip
				active = 1
		if err:
			# print ip, err.split('\n')[4]
			ip_mac = '%s\tInactive\t'%ip
			active = 0
			
		# arp list
		if active:
			p = subprocess.Popen(['arp', '-n', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = p.communicate()
			if out:
				# print ip, out.split('\n')[4]
				# AAA = out.split('\n')[1] #.strip()[4]
				# BBB = " ".join(AAA.split())
				# CCC = BBB.split()
				# arp = CCC[2]
				arp = " ".join(out.split('\n')[1].split()).split()[2]
				file.write('sudo arp -s %s %s\n'%(ip,arp)) 
			if err:
				# print ip, err.split('\n')[4]
				arp = " ".join(out.split('\n')[1].split()).split()[1]
				
			print ip_mac, arp
		else:
			print ip_mac
	
	file.close() 
	
if __name__ == '__main__':
	# Check what time the scan started
	t1 = datetime.now()
	# Clear the screen
	subprocess.call('clear', shell=True)

	if len(sys.argv) > 1:
		ip_class = sys.argv[1]
	else:
		ip_class = raw_input('Enter C Type Class(Ex:192.168.0): ')

	myIP = get_ip_address('eth0') # eth0, enp2s0 
	if not ip_class: 
		ip_class = myIP.rsplit('.', 1)[0] # eth0, enp2s0 
	
	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)

	t2 = datetime.now()
	total =  t2 - t1

	# Printing the information to screen
	print '\nCompleted: ', total