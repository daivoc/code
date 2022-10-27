#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import smtplib
import base64
import time

import MySQLdb
import config_db as c
from config_sensor import *

# from module_for_optex import *
# from module_for_mysql import *

table_RLS = ECOS_table_prefix+ECOS_table_RLS


def get_sensor_serial(): # Optex Microwave
	query = "SELECT wr_id, wr_subject, w_sensor_serial, w_email_Addr FROM " + table_RLS + " WHERE w_sensor_disable = 0 AND w_email_Addr != ''" 
	try:
		conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		return cursor.fetchall()

	except MySQLdb.Error as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

		
def export_report_by_DUE(dueDate='1 DAY'): # or '1 WEEK'
	w_cfg_sensor_serial = get_sensor_serial()
	for row in w_cfg_sensor_serial:
		ECOS_myID = row["wr_id"]
		ECOS_serialNo = row["w_sensor_serial"]
		ECOS_dbName = ITS_sensor_log_table + "_" + ECOS_serialNo
		ECOS_subjectIs = row["wr_subject"].replace(" ", "_") # mystring.replace(" ", "_")
		ECOS_exportFile = "/tmp/" + ECOS_subjectIs + "_" + time.strftime("%Y_%m_%d-%H:%M:%S")
		ECOS_targetEmail = row["w_email_Addr"]
	
		# 현재로부터 과거 24시간의 결과물을 /tmp/myfilename.txt로 출력하는 SQL Sample
		query = "SELECT w_stamp, w_event_stat, w_event_desc FROM "+ECOS_dbName+" WHERE w_event_sent = 1 AND w_event_stat != '' AND w_stamp >= NOW() - INTERVAL " + dueDate + " INTO OUTFILE '"+ECOS_exportFile+"'";
		try:
			conn = MySQLdb.connect(host=c.db_host, user=c.db_user, passwd=c.db_pass, db=c.db_name, charset='utf8', use_unicode=True) 
			cursor = conn.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(query)
			# return cursor.fetchall()
			return ECOS_exportFile, ECOS_targetEmail, ECOS_subjectIs, ECOS_serialNo
			
		except MySQLdb.Error as error:
			print(error)
		finally:
			cursor.close()
			conn.close()

			
# 일간 또는 주간 리포트 생성
ECOS_exportFile, ECOS_targetEmail, ECOS_subjectIs, ECOS_serialNo = export_report_by_DUE()

# Read a file and encode it into base64 format
fo = open(ECOS_exportFile, "rb")
filecontent = fo.read()
encodedcontent = base64.b64encode(filecontent)  # base64

sender = 'daivoc@gmail.com'
# sender_X = 'donotreply@'+ECOS_serialNo+'com' # 오류발생
receivers = ECOS_targetEmail

marker = "AUNIQUEMARKER"

body ="""Daily Report, 일간 리포트, 日報"""
# body ="""Daily Report"""

# Define the main headers.
part1 = """From: From Person <%s>
To: To Person <%s>
Subject: %s %s Sending Attachement
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (sender, receivers, ECOS_subjectIs, ECOS_serialNo, marker, marker)

# Define the message action
part2 = """Content-Type: text/plain;
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(ECOS_exportFile, ECOS_exportFile, encodedcontent, marker)
message = part1 + part2 + part3

try:
	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(sender, receivers, message)         
	print "Successfully sent email"
except SMTPException:
	print "Error: unable to send email"

