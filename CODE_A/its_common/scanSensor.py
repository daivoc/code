#!/usr/bin/env python
import socket
import sys
import MySQLdb
from config import *


def scanSensorInTable(host, table): # table
	cursor = None
	conn = None
	query = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial FROM " + table + " WHERE w_sensor_disable = 0 ORDER BY wr_id DESC" 
	try:
		conn = MySQLdb.connect(host=host, user=db_user, passwd=db_pass, db=db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()
	except MySQLdb.Error as error:
		return 0
	finally:
		if cursor:
			cursor.close()
		if conn:
			conn.close()
			
def scanSensorInHost(host): # host
	# 원격에서 Mysql 접근 허용을 위해서는
	# /etc/mysql/my.cnf 내에 bind-address를 주석 처리 한다.
	# # bind-address = 127.0.0.1
	sensorInfo = ''
	tables = [ECOS_table_prefix+ECOS_table_RLS, ECOS_table_prefix+ECOS_table_GPIO]
	for table in tables:
		result = scanSensorInTable(host, table)
		if result:
			for row in result:
				sensorInfo += '%s %s %s "%s" "%s" %s \n' % (host, table, row["wr_id"], row["wr_subject"], row["w_sensor_model"], row["w_sensor_serial"])
	return sensorInfo
		
if __name__ == '__main__':

	file = open("./scanSensor.txt", "w")
	try:
		# for port in range(1,65536):  
		for ips in range(1,256):  
			host = '192.168.0.%s'%ips
			port = 64446
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.01)
			result = sock.connect_ex((host, port))
			if result == 0:
				print "host %s port %s: Open" % (host,port)
				sensorInfo = scanSensorInHost(host)
				file.write("%s\n" % sensorInfo)
			# else:
				# print "host %s port %s: Close" % (host,port)
			sock.close()
	except KeyboardInterrupt:
		print "You pressed Ctrl+C"
		sys.exit()
	except socket.gaierror:
		print 'Hostname could not be resolved. Exiting'
		sys.exit()
	except socket.error:
		print "Couldn't connect to server"
		sys.exit()

	file.close()
	print 'Scanning Completed'