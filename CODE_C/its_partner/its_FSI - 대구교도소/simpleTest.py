#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import struct
import socket
import xml.etree.ElementTree as ET
import xmltodict, json

def parserXML(data):
	# XML이 하나 이상 들어오는 경우를 대비 해서
	# XML 시작 라인을 구분자(delimiter)로 행열로 만든후
	# 시작(Blank) 그룹을 제거 한다. 
	rootGrps = data.split(data.splitlines()[0])[1:]
	response = {}
	for group in rootGrps:
		try: 
			root = ET.fromstring(group)
			rootTag = root.tag
			rootAttrib = root.attrib
			# return rootTag, rootAttrib
			response[rootTag] = rootAttrib
			# deviceName = root.find('DeviceIdentification').find('DeviceName').text
			# status = root.attrib['Status']
			# return deviceName, status
		except:
			return None
	return response

def main ():

	conn = socket.socket()             # Create a socket object
	host = "192.168.168.30"  #Ip address that the TCPServer  is there
	port = 10001                     # Reserve a port for your service every new transfer wants a new port or you must wait.

	conn.connect((host, port))
	conn.send('<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName>FD525R-109545</DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>')
	# s.send('<CommandMessage MessageType="Request"><DeviceIdentification><DeviceName></DeviceName></DeviceIdentification><Command><SimpleCommand>Ping</SimpleCommand></Command></CommandMessage>')

	buffer = 1024
	bucket = b''
	fLine = b'' # 이전 페킷의 시작 라인 저장
	lLine = b'' # 이전 페킷의 마지막 라인 저장
	while True:
		data = conn.recv(buffer)
		print("<----")
		print data
		print("---->")
		# tagHead = re.findall(r'^<\?xml', data, flags=re.MULTILINE)
		# print tagHead, len(tagHead)
		# tagTail = re.findall(r'^<[/|A-Z].*', data, flags=re.MULTILINE)
		# print tagTail, len(tagTail)
		# print data.splitlines()[0], len(data.splitlines()[0]) # 첫라인
		# print data.splitlines()[-1], len(data.splitlines()[-1]) # 마지막 라인
		# print bucket.split("\n",1)[1] # 시작라인 삭제
		
		sLine = data.splitlines()[0]
		eLine = data.splitlines()[-1]
		if re.match(r'^\n<', sLine) and re.match(r'^<\/.*>', eLine): # 시작점 과 끝, 엔터키이후 <가 나오면
			bucket = data
			print "<<<<<<<<<<<<<<<<<<"
			# print bucket.split("\n",1)[1]
			print parserXML(bucket.split("\n",1)[1]) # 분석요청
			# print bucket
			print ">>>>>>>>>>>>>>>>>>"
			bucket = b''
		elif re.match(r'^\n<', sLine): # 시작점 엔터키이후 <가 나오면
			bucket = data # 시작 점, 버텟에 채운다.
			fLine = sLine
		elif re.match(r'^<\/.*>', eLine) or re.match(r'^<\/.*>', lLine+eLine):
			# 마지막점 인지를 확인후 추가 기능 실행
			# 마지막 라인이 '</단어>' 로 끝나거나
			# '어>' 로 끝날시 이전 마지막 단어 '<단' 랑 결합후 조건 '</단어>'이 완성 되면
			bucket += data # 마지막 점, 버텟에 추가한다.
			print "<<<<<<<<<<<<<<<<<<"
			# print bucket.split("\n",1)[1]
			print parserXML(bucket.split("\n",1)[1]) # 분석요청
			# print bucket
			print ">>>>>>>>>>>>>>>>>>"
			bucket = b'' # 종료 점, 버텟을 비운다.
		else:
			bucket += data # 중간 점, 버텟에 추가한다.
			lLine = eLine
		
		if not data:
			break

	s.close()

if __name__ == '__main__':

	main()
