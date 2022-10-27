#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import socket 
import time
import datetime

def reset_sensor_time(time): 
	'''
	４－４－１ 시각설정 커맨드
		컬럼    내용    Size
		1       버전        2   "50"
		2       커맨드      3   "001" ：시각설정
		3       기기번호    8   시리얼번호
		4       데이터길이  8   "00000014"
		5       일시        14  "yyyymmddHHMMSS" (UTC)

	４－４－２ 시각설정 리스폰스
		컬럼    내용        Size
		1       버전        2 "50"
		2       커맨드      3 "001" ：시각설정
		3       에러코드    3 "000"：정상
		4       데이터길이  8 "00000000"

	echo "500010030373900000014BUFFERCLEAR00200" | nc 192.168.168.30 50001
	'''
	command = '001'
	length = '00000014'
	msg = "%s%s%s%s%s"%(version,command,serial,length,time)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		sock.connect((ip, port))
		sock.send(msg) 
		while True:
			data = sock.recv(16)
			if data[5:8] == "000":
				return 1
			else:
				return 0
			return data.decode()
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

def reset_sensor_data():
	'''
	４－２－１ 계수데이터 클리어 커맨드
		컬럼    내용        Size
		1       버전        2   "50"
		2       커맨드      3   "200" ：카운트데이터 클리어
		3       기기번호    8   시리얼번호
		4       데이터길이  8   "00000016"
		5       고정문자열  16  "BUFFERCLEAR00200"

	４－２－２ 계수데이터 클리어 리스폰스
		컬럼    내용        Size
		1       버전        2   "50"
		2       커맨드      3   "200" ：카운트데이터 클리어
		3       에러코드    3   "000"：정상
		4       데이터길이  8   "00000000"

	echo "502000030373900000016BUFFERCLEAR00200" | nc 192.168.168.30 50001
	'''
	command = '200'
	length = '00000016'
	msg = "%s%s%s%s%s"%(version,command,serial,length,"BUFFERCLEAR00200") # 502000030373900000016BUFFERCLEAR00200
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		sock.connect((ip, port))
		sock.send(msg) 
		while True:
			data = sock.recv(16)
			if data[5:8] == "000":
				return 1
			else:
				return 0
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 

def read_sensor_count(dateS, dateE): 
	'''
	４－３－１ 카운트데이터 요구커맨드
		컬럼    내용            Size
		1       버전             2   "50"
		2       커맨드           3   "201" ：계수데이터
		3       기기번호         8   시리얼번호
		4       데이터길이       8   "00000032"
		5       검색시작 일시   12   "yyyymmddHHMM", "000000000000"로 가장 오래된 데이터
		6       검색종료 일시   12   "yyyymmddHHMM", "999999999999"로 최신 데이터※1
		7       카운트           1   출력지정 1 "0"~"1" ※2
		8       카운트           2   출력지정 1 "0"~"1" ※2
		9       카운트           3   출력지정 1 "0"~"1" ※2
		10      카운트           4   출력지정 1 "0"~"1" ※2
		11      예비영역         4   "0000"

		※1 최신데이터를 요구한 경우, 리스폰스의 제일 마지막 레코드에 미확정 데이터를 부가한다.
		1 분 이내의 간격으로 속보수치가 필요할 경우에 사용한다.
		※2 "0"＝출력없음, "1"＝출력있음

	４－３－２ 카운트 데이터 요구 리스폰스
		컬럼    내용            Size
		1       버전            2   "50"
		2       커맨드          3   "201"：계수데이터
		3       에러코드        3   "000"：정상
		4       데이터길이      8   "00000030" ~ 30＋레코드수×레코드사이즈
		5       미송신데이터    12 "000000000000" ※1
				선두일시
		6       레코드 수       8   "00000000"~
		7       레코드 사이즈   8   "00000000"~
		8       개행            2   CR(0x0D)＋LF(0x0A)
		9       카운트 데이터       레코드수×레코드사이즈

		※1 현시점의 센서 유닛 사양으로는 미송신 데이터는 발생하지 않기 때문에, 항상 0 이 설정됨.

		echo "50201003037390000003200000000000099999999999911110000" | nc 192.168.168.30 50001
	'''
	command = '201'
	length = '00000032'
	count = '1111'
	reserve = '0000'
	msg = "%s%s%s%s%s%s%s%s"%(version,command,serial,length,dateS,dateE,count,reserve)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		sock.connect((ip, port))
		sock.send(msg) 
		while True:
			data = sock.recv(128)
			return data.decode()
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		sock.close() 
		
def main ():
	
	if(reset_sensor_data()):
		print "Cleared Sensor Buffer"
	else:
		os._exit("Error - Clear Sensor Buffer")
	
	# dateTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # UTC+9
	dateTime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") # UTC - 센서 요청시간대

	if reset_sensor_time(dateTime):
		print "Set Sensor Time: %s" % datetime.datetime.now()
	else:
		os._exit("Error - Set Sensor Time")

	dateS = dateTime[:-2] # 센서 시간 설정후 시작시간 설정
	dateE = '999999999999'
	saveDate = '000000000000'
	
	trigger = 0

	allCnt_I = 0
	allCnt_O = 0

	totalZ_AA = 0
	totalZ_aa = 0
	totalZ_BB = 0
	totalZ_bb = 0
	totalZ_CC = 0
	totalZ_cc = 0
	totalZ_DD = 0
	totalZ_dd = 0

	oldZ_AA = 0
	oldZ_aa = 0
	oldZ_BB = 0
	oldZ_bb = 0
	oldZ_CC = 0
	oldZ_cc = 0
	oldZ_DD = 0
	oldZ_dd = 0

	diffSum_1 = 0
	diffSum_2 = 0
	diffSum_3 = 0
	diffSum_4 = 0

	direction_1 = "NA"
	direction_2 = "NA"
	direction_3 = "NA"
	direction_4 = "NA"

	print "Start Count"
	# print "\tDire_A In:%s, Out:%s, D_1:%s(%s)"%(totalZ_AA, totalZ_aa, direction_1, diffSum_1)
	# print "\tDire_B In:%s, Out:%s, D_2:%s(%s)"%(totalZ_BB, totalZ_bb, direction_2, diffSum_2)
	# print "\tDire_C In:%s, Out:%s, D_3:%s(%s)"%(totalZ_CC, totalZ_cc, direction_3, diffSum_3)
	# print "\tDire_D In:%s, Out:%s, D_4:%s(%s)\n"%(totalZ_DD, totalZ_dd, direction_4, diffSum_4)

	while True:
		data = read_sensor_count(dateS, dateE)
		# print data
		if data is 0: # 페킷 읽기 오류
			continue

		for line in data.splitlines()[1:]:
			dateS = int(line[8:20]) # 신규 픽업시간 저장
			newDataIs = line[22:] # 신규데이터 저장
			if len(newDataIs) is not 32: # print len(newDataIs)
				continue

			# print int(newDataIs)

			newZ_AA = int(newDataIs[0:4])
			newZ_aa = int(newDataIs[4:8])
			newZ_BB = int(newDataIs[8:12])
			newZ_bb = int(newDataIs[12:16])
			newZ_CC = int(newDataIs[16:20])
			newZ_cc = int(newDataIs[20:24])
			newZ_DD = int(newDataIs[24:28])
			newZ_dd = int(newDataIs[28:32])

			if newZ_AA > oldZ_AA:
				diffSum_1 = newZ_AA - oldZ_AA
				totalZ_AA += diffSum_1
				allCnt_I += diffSum_1
				direction_1 = "In"
				oldZ_AA = newZ_AA
				trigger = 1
			if newZ_aa > oldZ_aa:
				diffSum_1 = newZ_aa - oldZ_aa
				totalZ_aa += diffSum_1
				allCnt_O += diffSum_1
				direction_1 = "Out" 
				oldZ_aa = newZ_aa
				trigger = 1

			if newZ_BB > oldZ_BB:
				diffSum_2 = newZ_BB - oldZ_BB
				totalZ_BB += diffSum_2
				allCnt_I += diffSum_2
				direction_2 = "In"
				oldZ_BB = newZ_BB
				trigger = 1
			if newZ_bb > oldZ_bb:
				diffSum_2 = newZ_bb - oldZ_bb
				totalZ_bb += diffSum_2
				allCnt_O += diffSum_2
				direction_2 = "Out" 
				oldZ_bb = newZ_bb
				trigger = 1

			if newZ_CC > oldZ_CC:
				diffSum_3 = newZ_CC - oldZ_CC
				totalZ_CC += diffSum_3
				allCnt_I += diffSum_3
				direction_3 = "In"
				oldZ_CC = newZ_CC
				trigger = 1
			if newZ_cc > oldZ_cc:
				diffSum_3 = newZ_cc - oldZ_cc
				totalZ_cc += diffSum_3
				allCnt_O += diffSum_3
				direction_3 = "Out" 
				oldZ_cc = newZ_cc
				trigger = 1

			if newZ_DD > oldZ_DD:
				diffSum_4 = newZ_DD - oldZ_DD
				totalZ_DD += diffSum_4
				allCnt_I += diffSum_4
				direction_4 = "In"
				oldZ_DD = newZ_DD
				trigger = 1
			if newZ_dd > oldZ_dd:
				diffSum_4 = newZ_dd - oldZ_dd
				totalZ_dd += diffSum_4
				allCnt_O += diffSum_4
				direction_4 = "Out" 
				oldZ_dd = newZ_dd
				trigger = 1

			if trigger:
				print "Total In:%s, Out:%s"%(allCnt_I, allCnt_O)
				print "\t%s - Sum In:%s, Out:%s, D_1:%s(%s)"%(dateS, totalZ_AA, totalZ_aa, direction_1, diffSum_1)
				print "\t%s - Sum In:%s, Out:%s, D_2:%s(%s)"%(dateS, totalZ_BB, totalZ_bb, direction_2, diffSum_2)
				print "\t%s - Sum In:%s, Out:%s, D_3:%s(%s)"%(dateS, totalZ_CC, totalZ_cc, direction_3, diffSum_3)
				print "\t%s - Sum In:%s, Out:%s, D_4:%s(%s)"%(dateS, totalZ_DD, totalZ_dd, direction_4, diffSum_4)
				print line,"\n"
				
			trigger = 0
			diffSum_1 = 0
			diffSum_2 = 0
			diffSum_3 = 0
			diffSum_4 = 0
				
			if dateS > saveDate:
				# 초기화
				oldZ_AA = 0
				oldZ_aa = 0
				oldZ_BB = 0
				oldZ_bb = 0
				oldZ_CC = 0
				oldZ_cc = 0
				oldZ_DD = 0
				oldZ_dd = 0

				# 분당 집계 - 데이터베이스 연계
				dataMin = read_sensor_count(saveDate,dateS)
				for lineMin in dataMin.splitlines()[1:]:
					dateMin = lineMin[8:20] # 신규 픽업시간 저장 newDateMin
					newDataIs = lineMin[22:] # 신규데이터 저장

					newCntMin1_I = int(newDataIs[0:4])
					newCntMin1_O = int(newDataIs[4:8])
					newCntMin2_I = int(newDataIs[8:12])
					newCntMin2_O = int(newDataIs[12:16])
					newCntMin3_I = int(newDataIs[16:20])
					newCntMin3_O = int(newDataIs[20:24])
					newCntMin4_I = int(newDataIs[24:28])
					newCntMin4_O = int(newDataIs[28:32])

					print "Date: %s/%s %s:%s Total In:%s, Out:%s"%(dateMin[4:6], dateMin[6:8], dateMin[8:10], dateMin[10:12], allCnt_I, allCnt_O)
					print "\tDire_A: In:%s, Out:%s"%(newCntMin1_I, newCntMin1_O)
					print "\tDire_B: In:%s, Out:%s"%(newCntMin2_I, newCntMin2_O)
					print "\tDire_C: In:%s, Out:%s"%(newCntMin3_I, newCntMin3_O)
					print "\tDire_D: In:%s, Out:%s"%(newCntMin4_I, newCntMin4_O)
					print "\tTotal : In:%s, Out:%s\n"%(newCntMin1_I + newCntMin2_I + newCntMin3_I + newCntMin4_I, newCntMin1_O + newCntMin2_O + newCntMin3_O + newCntMin4_O)
				# 종료 분당 집계 - 데이터베이스 연계

			saveDate = dateS # 이전 픽업시간 저장

		time.sleep(0.1) # 1초에 한번 이상 확인하기 위함
		
if __name__ == '__main__':
	ip = '192.168.168.30'
	port = 50001
	version = '50'
	serial = '00303739'
		
	print "ip:%s, port:%s, version:%s, serial:%s"%(ip, port, version, serial)
	main()