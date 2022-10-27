import socket
import sys
import binascii
import os, traceback
import fcntl
import struct
import time
import subprocess 
import re
import config_db as c

### Packet field access ###
def all(packet):
	return binascii.hexlify(packet).decode()

# 정수를 부호있는 숫자로 변환
def hex2int(dataObj):
	x = int(binascii.hexlify(dataObj).decode(), 16)
	if x > 0x7FFFFFFF:
		x -= 0x100000000
	return x
	
def cmd00(packet): # Sensor information.
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	# ['OPTEX', 'RLS-3060', 'SH', '0100', '\x00\x1f\xd1\x16\x06\xd3', '', '']
	# print(packet.splitlines()[0]) # 'OPTEX'
	# print(packet.splitlines()[1]) # 'RLS-3060'
	# print(packet.splitlines()[2]) # 'SH'
	# print(packet.splitlines()[3]) # '0100'
	# print(packet.split('\n\n\r')[0])
	return '%s %s %s' % (packet.splitlines()[0], packet.splitlines()[1], packet.splitlines()[2]) # INFO

def cmd01(packet): # 맥 어드레스
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	return all(dataObj)
	
def cmd02(packet): # 버전 정보
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	return (dataObj)
	
def cmd03(packet): # 유니트 아이디
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	return (dataObj)
	
def cmd04(packet): # 
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	cntObj = len(dataObj)/4 # 4 바이트씩 그룹핑 - 기본 Object Info Size
	count = 0
	objInfo = ''
	while (count < cntObj):
		fLN = count * 4
		tLN = fLN + 4
		# print all(dataObj[fLN:tLN])
		objInfo += '%s,' % hex2int(dataObj[fLN:tLN])
		
		count = count + 1
	return objInfo
	
def cmd05(packet): # 존(zone) 정보
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	objInfo = '%s %s %s %s %s %s' % (hex2int(dataObj[0:4]), hex2int(dataObj[4:8]), dataObj[8:14], dataObj[14:17], dataObj[17:18], hex2int(dataObj[18:22]))
	return (objInfo)
	
def cmd06(packet): # 이벤트 발생정보 
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.splitlines()[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	cntObj = len(dataObj)/20 # 20 바이트씩 그룹핑 - 기본 Object Info Size
	count = 0
	objInfo = ''
	while (count < cntObj):
		fFX = count * 20
		fFY = fFX + 4
		fOX = fFY + 4
		fOY = fOX + 4
		fSZ = fOY + 4
		
		tFX = fFX + 4
		tFY = fFY + 4
		tOX = fOX + 4
		tOY = fOY + 4
		tSZ = fSZ + 4
		
		objID = '%s%s' % (hex2int(dataObj[fFX:tFX]),hex2int(dataObj[fFY:tFY])) # First X,Y coordinate
		objX = hex2int(dataObj[fOX:tOX]) # X-coordinate of detected object.
		objY = hex2int(dataObj[fOY:tOY]) # Y-coordinate of detected object.
		objD = hex2int(dataObj[fSZ:tSZ]) # Size of the detected object

		# objInfo += '%s,' % str(12000-(hex2int(dataObj[fOX:tOX])+6000)) # 화면 표시용 X-coordinate of detected object.
		objInfo += '%s,%s,%s,%s|' % (re.sub('-', '',str(objID)), str(objX), str(objY), str(objD))
		
		count = count + 1
		
		# print objID, objX, objY, objD
	return objInfo

def cmd07(packet): # 기본 좌표 정보
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	objInfo = '%s %s %s' % (dataObj[0:4], dataObj[4:8], dataObj[8:12])
	return (objInfo)
	
def cmd08(packet): # 센서 이벤트 출력 정보
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	return (dataObj)

def cmd09(packet): # 릴레이 정보
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	return (dataObj)

def cmd10(packet): # 마스킹/얼로케이션 파일
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	return (dataObj)

def cmd11(packet): # 마스킹/얼로케이션 영역
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	objInfo = '%s %s %s' % (dataObj[0:1], dataObj[1:2], all(dataObj[2]))
	return (objInfo) 

def cmd12(packet): # 모델명
	respCode = errorCheck(packet.split('\n')[3][2:4]) # errorCheck(code)
	if respCode:
		return respCode

	dataObj = packet.split('\n\n\r')[0] # 페킷내의 최종('\n\n\r') 포멧에 따른 자료만 추출
	dataObj = dataObj.split('\n',4)[4] # 0 ~ 3번째 라인이후의 모든 데이터를 선별한다.
	len_m_name = int(all(dataObj[0:1]))
	m_name = dataObj[1:len_m_name]
	
	len_s_name = int(all(dataObj[len_m_name+1:len_m_name+2]))
	s_name = dataObj[len_m_name+2:len_m_name+2+len_s_name]
	objInfo = '%s %s' % (m_name, s_name)
	return (objInfo) 
		
def errorCheck(code):
	if code == '10':
		msg = 'Requested command is not supported.'
	elif code == '11':
		msg = 'Format Error.'
	elif code == '12':
		msg = 'Requested command is ignored because it is doubled.'
	else:
		msg = ''
	return msg	
	
def reqCommand(id):
	command = {}
	command['cmd01'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][01][LF][LF][CR]'	# Requests MAC address.
	command['cmd02'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][02][LF][LF][CR]'	# Requests version number.
	command['cmd03'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][03][LF][LF][CR]'	# Requests ID of the unit.
	command['cmd04'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][04][00][LF][LF][CR]'	# Requests detection area information. 
	command['cmd05'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][05][LF][LF][CR]'	# Requests zone (area AB) information.
	command['cmd06'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][50][0011][LF][LF][CR]'	#  To start the report by limiting the number of detected objects to 50 and specifing 50 ms for valid report interval,
	command['cmd06I'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][25][0100][LF][LF][CR]'	#  To start the report by limiting the number of detected objects to 25 and specifing 5000 ms for valid report interval,
	command['cmd06S'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][0][00][0000][LF][LF][CR]'	# STOP Requests detected object information. 
	command['cmd06L'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][06][1][30][0000][LF][LF][CR]'	# To request only one report limiting the number of detected object to 30.
	command['cmd07'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][07][LF][LF][CR]'	# Requests basic parameter of detection area. 
	command['cmd08'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][08][LF][LF][CR]'	# TCP - Requests destination of Redwall Event Code (REC) and sending sample REC.
	# command['cmd09'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][09][02][600][LF][LF][CR]'	# In case of activating Output 02 10 minutes (600 sec.) Controls the relay output.
	command['cmd09'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][09][02][0][LF][LF][CR]'	# In case of activating Output 02 10 minutes (600 sec.) Controls the relay output.
	command['cmd10'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][10][CS][LF][LF][CR]'	# Requests/switches masking/allocating File.
	command['cmd11'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][11][LF][LF][CR]'	# Requests masking/allocating area information.
	command['cmd12'] = '[OPTEX][LF][*][LF][*][LF][*][LF][*][LF][12][LF][LF][CR]'	# Requests model name.(Only 2020)
	return command[id].replace('[','').replace(']','').replace('LF','\n').replace('CR','\r')
	
# 자신 아이피 확인 
def get_ip_address(ifname): # get_ip_address('eth0')  # '192.168.0.110'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])
	
def realtime_monitoring(ip,port,objInfo):
	node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try: 
		node.connect((ip,port))
		node.send(objInfo) 
		# print objInfo
		# return 1
	except socket.error:
		return 0
	except socket.timeout:
		return 0
	finally:
		node.close() 

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_realtime_RLS(arg): 
	cmd = "kill $(ps aux | grep '[n]ode realtime_RLS.js %s' | awk '{print $2}')" % arg
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	
# 확인된 변수로 데몬을 실행 한다
# cd /var/www/html/its_web/theme/ecos-its_optex/utility/nodeJs_table
# node ./realtime_RLS.js 64444 64446
def run_demon_realtime_RLS(arg): 
	path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	cmd = "cd /var/www/html/its_web/%s; node realtime_RLS.js %s 2>&1 & " % (path, arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

# 센서 아이피 확인 
def check_sensor(sensorIP): # 50001 포트가 살아있는지 확인 한다.
    # return os.system("ping -c1 -W1 " + sensorIP + " > /dev/null") # IF RETURN 0 THAT Network Active ELSE Network Error
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.1)
	result = sock.connect_ex((sensorIP, 50001))
	sock.close()
	return result

###################################################

if len(sys.argv) > 1:
	sensor_IP = sys.argv[1]
else:
	exit("Ex: %s %s" % (sys.argv[0], sensor_IP))

sensorPort = 50001
nodeIn = 50000 + int(sensor_IP.split('.')[3]) # sensor_IP = '192.168.168.30' -> 50030
nodeOut = 51000 + int(sensor_IP.split('.')[3]) # sensor_IP = '192.168.168.30' -> 50030

myIp = get_ip_address('eth0')


	
def main ():
	# Create a TCP/IP socket
	sockS30 = socket.create_connection((sensor_IP, sensorPort)) # 센서 연결

	sockS30.sendall(reqCommand('cmd12'))
	data_tmp = sockS30.recv(1024)
	print "model name: ", cmd12(data_tmp)
	
	sockS30.sendall(reqCommand('cmd01'))
	data_tmp = sockS30.recv(1024)
	print "mac address: ", cmd01(data_tmp)
	
	sockS30.sendall(reqCommand('cmd02'))
	data_tmp = sockS30.recv(1024)
	print "version: ", cmd02(data_tmp)
	
	sockS30.sendall(reqCommand('cmd03'))
	data_tmp = sockS30.recv(1024)
	print "unit ID: ", cmd03(data_tmp)

	# sockS30.sendall(reqCommand('cmd04')) # 센서에 자료('cmd04') 요청
	# data_tmp = sockS30.recv(1024)
	# print "detection area No: ", cmd04(data_tmp)
	
	sockS30.sendall(reqCommand('cmd05'))
	data_tmp = sockS30.recv(1024)
	print "zone information: ", cmd05(data_tmp)
	
	sockS30.sendall(reqCommand('cmd07'))
	data_tmp = sockS30.recv(1024)
	print "basic parameter: ", cmd07(data_tmp)
	
	sockS30.sendall(reqCommand('cmd08'))
	data_tmp = sockS30.recv(1024)
	print "destination of Redwall: ", cmd08(data_tmp)
	
	sockS30.sendall(reqCommand('cmd09'))
	data_tmp = sockS30.recv(1024)
	print "relay output: ", cmd09(data_tmp)

	sockS30.sendall(reqCommand('cmd10'))
	data_tmp = sockS30.recv(1024)
	print "masking/allocating file: ", cmd10(data_tmp)

	# sockS30.sendall(reqCommand('cmd11'))
	# data_tmp = sockS30.recv(1024)
	# print "masking/allocating area: ", cmd11(data_tmp)

	sockS30.sendall(reqCommand('cmd06')) # 센서에 자료('cmd06') 요청
	try:
		# Send data
		while True:
			data_tmp = sockS30.recv(1024)
			# print data_tmp
			data_S30 = cmd06(data_tmp) # 센서로 부터 받은 자료
			if data_S30: 
				print sensor_IP, data_S30 # 42949672541081,422,676,355|42949672541081,259,861,54|
				realtime_monitoring(myIp,nodeIn,data_S30)
	finally:
		print 'closing socket_S30'
		sockS30.close()

if __name__ == '__main__':
	if check_sensor(sensor_IP):
		exit("*** Sensor Test ERROR ***\n\tPlease check Sensor's IP(%s)" % sensor_IP)
		
	ECOS_unionTable = '%s %s' % (nodeIn, nodeOut)
	kill_demon_realtime_RLS(ECOS_unionTable)
	run_demon_realtime_RLS(ECOS_unionTable)
	print('Running RLS Realtime Monitoring\nhttp://%s:%s' %(sensor_IP,nodeOut))

	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)