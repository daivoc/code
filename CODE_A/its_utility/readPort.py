#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import fcntl
import struct
import binascii
import os, traceback, subprocess

### Packet field access ###
def all(packet):
	return binascii.hexlify(packet).decode()

def main ():
	
	BUFFER = 1024  # Normally 1024, but we want fast response
	IPADDR = raw_input('Service IP - Default localhost #: ')
	PORT = raw_input('Service Port #: ')
	HEX = raw_input('HEX Out? - Default ASC: ')
	FILTER = raw_input('Filter String: ')
	if not PORT: exit("need service port ID")

	try:
		# print IPADDR, int(PORT)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((IPADDR, int(PORT))) # 'localhost'를 뜻함
	except:
		print "IP and Port are Busy.\nCheck Processor."
		exit()
		
	s.listen(1)

	if not IPADDR: IPADDR = 'localhost'
	print "Listen %s's PORT:"%IPADDR, PORT

	while True:
		conn, addr = s.accept()
		print 'Connection address:', addr
		while True:
			data = conn.recv(BUFFER)
			if not data: break
			if HEX:
				result = "HEX: " + all(data)
			else:
				result = "ASC: " + data
			
			if FILTER in result:
				print "\t%s"%result
		conn.close()
	s.close()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)