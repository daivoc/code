#!/usr/bin/env python
import socket
import subprocess
import sys
import fcntl
import struct
import traceback, os
from datetime import datetime

def get_ip_address(ifname): # get_ip_address('eth0')  # '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

def checkPort(ip, port, msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.01)
	result = sock.connect_ex((ip, port))
	sock.close()
	if result == 0:
		return msg
	else:
		return ''

def cmd_proc_Popen(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out
	
def main():
	try:
		# for port in range(1,65536):  
		for ips in range(2,255):  
			
			port_info = ''
			ip = '%s.%s'%(ip_class,ips)
			
			if ip_port:
				port_info += checkPort(ip, int(ip_port), 'Manual ')
			else:
				## http//home.zany.kr9003/board/bView.asp?bCode=12&aCode=769
				# if 'FTP' in checkList: port_info += checkPort(ip, 21, 'FTP ')
				# if 'SSH' in checkList: port_info += checkPort(ip, 22, 'SSH ')
				# if 'SMTP' in checkList: port_info += checkPort(ip, 25, 'SMTP ')
				# if 'DNS' in checkList: port_info += checkPort(ip, 53, 'DNS ')
				if 'HTTP' in checkList: port_info += checkPort(ip, 80, 'HTTP ')
				# if 'NNTP' in checkList: port_info += checkPort(ip, 119, 'NNTP ')
				# if 'RPC' in checkList: port_info += checkPort(ip, 135, 'RPC ')
				# if 'NetBT' in checkList: port_info += checkPort(ip, 137, 'NetBT ')
				# if 'NetBT' in checkList: port_info += checkPort(ip, 138, 'NetBT ')
				# if 'NetBT' in checkList: port_info += checkPort(ip, 139, 'NetBT ')
				# if 'CHRONYD' in checkList: port_info += checkPort(ip, 323, 'CHRONYD ')
				# if 'HTTPS' in checkList: port_info += checkPort(ip, 443, 'HTTPS ')
				# if 'SMB' in checkList: port_info += checkPort(ip, 445, 'SMB ')
				# if 'ISAKMP' in checkList: port_info += checkPort(ip, 500, 'ISAKMP ')
				if 'CAMERA' in checkList: port_info += checkPort(ip, 554, 'CAMERA ')
				# if 'RDP' in checkList: port_info += checkPort(ip, 3389, 'RDP ')
				# if 'SHELL' in checkList: port_info += checkPort(ip, 4200, 'SHELL ')
				# if 'ICC' in checkList: port_info += checkPort(ip, 7000, 'ICC ')
				# if 'GPIO' in checkList: port_info += checkPort(ip, 8311, 'GPIO ') 
				# if 'GPWIO' in checkList: port_info += checkPort(ip, 8040, 'GPWIO ') 
				# if 'AOIP' in checkList: port_info += checkPort(ip, 9040, 'AOIP ') 
				# if 'SRF' in checkList: port_info += checkPort(ip, 18100, 'SRF ')
				if 'uApi' in checkList: port_info += checkPort(ip, 32001, 'uApi ')
				if 'iApi' in checkList: port_info += checkPort(ip, 34001, 'iApi ')
				# if 'GIKEN' in checkList: port_info += checkPort(ip, 35168, 'GIKEN ')
				# if 'IMS' in checkList: port_info += checkPort(ip, 38088, 'IMS ')
				# if 'RLS' in checkList: port_info += checkPort(ip, 50001, 'RLS ')
				# if 'WD' in checkList: port_info += checkPort(ip, 53000, 'WD ')
				# if 'ITS' in checkList: port_info += checkPort(ip, 64446, 'ITS ')

			if port_info:
				print('{} : {}'.format(ip, port_info))
			
	except KeyboardInterrupt:
		print ("You pressed Ctrl+C")
		sys.exit()

	except socket.gaierror:
		print ('Hostname could not be resolved. Exiting')
		sys.exit()

	except socket.error:
		print ("Couldn't connect to server")
		sys.exit()


if __name__ == '__main__':
	# Check what time the scan started
	t1 = datetime.now()
	# Clear the screen
	subprocess.call('clear', shell=True)

	ITS_iface = str(cmd_proc_Popen("route | grep '^default' -m1 | awk -F' ' '{print $8}' 2>/dev/null")).strip()

	if len(sys.argv) > 1:
		ip_class = sys.argv[1]
		ip_port = 0
	else:
		ip_class = raw_input('Enter C Type Class(Ex:192.168.0): ')
		ip_port = raw_input('Enter Port# Default Enter: ')
	if not ip_class: 
		ip_me = get_ip_address(ITS_iface) # eth0, enp2s0 
		ip_class = ip_me.rsplit('.', 1)[0] # eth0, enp2s0 

	# ip_interface = raw_input("Enter the Interface (eth0 or enp2s0): ")
	# if not ip_interface:
		# ip_interface = 'eth0' # eth0, enp2s0 
	# ip_me = get_ip_address(ip_interface) # eth0, enp2s0 
		
	print("Class {}".format(ip_class))
	if ip_port:
		checkList = 0
	else: 
		checkList = 1
	
	if checkList:
		# checkList = raw_input("Ex:) FTP SSH SMTP DNS HTTP NNTP NetBT HTTPS SMB ISAKMP CAMERA SNEWS RPC LDAP L2TP PPTP IAS MGC RDP RLS ITS \nEnter the servece name: ").upper()
		checkList = raw_input("Ex:) CAMERA SRF ICC IMS ITS HTTP\nEnter the service name: ").upper()
		if not checkList:
			# checkList = "HTTP CAMERA GPIO GPWIO AOIP IMS ITS GIKEN SRF ICC "
			checkList = "HTTP CAMERA uApi iApi "

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		os._exit(1)

	# Calculates the difference of time, to see how long it took to run the script
	t2 = datetime.now()
	total =  t2 - t1

	# Printing the information to screen
	print ('\nCompleted: {}'.format(total))