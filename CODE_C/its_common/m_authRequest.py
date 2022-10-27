#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import shutil
import requests
import socket

from requests.auth import HTTPDigestAuth
from PIL import Image, ImageDraw, ImageFont

## 아이디와 비밀번호 추출후 암호화 옵션에 따라 HTTPDigestAuth 적용
## 카메라로부터 이미지 다운로드후 저장
def download_image(host, file, enc): 
	if(enc):
		a = host.rsplit('@',1)[0] # 맨 마지막 @를 기준으로 첫번째 요쇼
		b = a.split('://',1)[1] # 맨 처음 :// 를 기준으로 두번째요소 선택
		c = b.split(':',1) # admin:optex59:://@@71!!
		user = c[0]
		pwd = c[1]
		r = requests.get(host, auth=HTTPDigestAuth(user, pwd), stream=True)
	else:
		r = requests.get(host, stream=True)
		
	if r.status_code == 200:
		with open(file, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
	return r.status_code # , host

## 아이디와 비밀번호 추출후 암호화 옵션에 따라 HTTPDigestAuth 적용
## 카메라로부터 이미지 다운로드후 저장
## 정상적인 다운로드가 되면 워터마크를 추가 한다	
def download_image_n_wmark(host, file, text, enc): 
	# 이미지 다운로드 후 워터마크 등록
	if(enc):
		a = host.rsplit('@',1)[0] # 맨 마지막 @를 기준으로 첫번째 요쇼
		b = a.split('://',1)[1] # 맨 처음 :// 를 기준으로 두번째요소 선택
		c = b.split(':',1) # admin:optex59:://@@71!!
		user = c[0]
		pwd = c[1]
		r = requests.get(host, auth=HTTPDigestAuth(user, pwd), stream=True)
	else:
		r = requests.get(host, stream=True)
		
	if r.status_code == 200:
		with open(file, 'wb') as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)
		
		# 워터마크 등록
		# 이미지 생성 일시는 카메라자체 시간이 나오도록 
		try: 
			image = Image.open(open(file, 'rb'))
			draw = ImageDraw.Draw(image)
			font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",30)
			draw.text((100, 1000), text, font=font) # X, Y 해상도에 위치함
			image.save(file,optimize=True,quality=100)
		except:
			return r.status_code, "Downloaded image Format Error %s" % file
			
	# time.sleep(10) 스레드 테스트
	return r.status_code, "Snapshot OK"

	
## PRESET Http Request 
## 아이디와 비밀번호 추출후 암호화 옵션에 따라 HTTPDigestAuth 적용
## url = "http://아이디:비밀번호@아이피/명령문"
## 변수 예) payload = {'key':'value'}, payload = {'key1': 'value1', 'key2': 'value2'}
def requests_get(url, enc, payload):
	try:
		if(enc):
			a = url.rsplit('@',1)[0]
			b = a.split('://',1)[1]
			c = b.split(':',1) ## 아이디:비밀번호
			user = c[0]
			pwd = c[1]
			r = requests.get(url, params=payload, auth=HTTPDigestAuth(user, pwd))
		else:
			r = requests.get(url)
		# print url, payload
		return r
	except r.exceptions.Timeout:
		return "Timeout  %s" % url
	except:
		return "requests.get Error: %s" % url

## https://stackoverflow.com/questions/9733638/post-json-using-python-requests
## http://docs.python-requests.org/en/master/user/quickstart/
## 아이디와 비밀번호 추출후 암호화 옵션에 따라 HTTPDigestAuth 적용
## url = "http://아이디:비밀번호@아이피/명령문"
## 변수 예) payload = {'key':'value'}, payload = {'key1': 'value1', 'key2': 'value2'}
def requests_post(url, enc, payload):
	try:
		if(enc):
			a = url.rsplit('@',1)[0]
			b = a.split('://',1)[1]
			c = b.split(':',1) ## 아이디:비밀번호
			user = c[0]
			pwd = c[1]
			r = requests.post(url, params=payload, auth=HTTPDigestAuth(user, pwd))
		else:
			r = requests.get(url)
		# return "%s%s" % (r.status_code, payload) # r.text
		# return "%s%s" % (r.status_code, r.text) # r.text
		return r
	except r.exceptions.Timeout:
		return "Timeout  %s" % url
	except:
		return "requests.get Error: %s" % url

		
## https://stackoverflow.com/questions/9733638/post-json-using-python-requests
## http://docs.python-requests.org/en/master/user/quickstart/
## JSON Header 전송
## 아이디와 비밀번호 추출후 암호화 옵션에 따라 HTTPDigestAuth 적용
## url = "http://아이디:비밀번호@아이피/명령문"
## 변수 예) payload = {'some1': 'data1', 'some2': 'data2'}
def requests_post_json(url, enc, payload):
	headers = {'Content-type': 'application/json'}
	try:
		if(enc):
			a = url.rsplit('@',1)[0]
			b = a.split('://',1)[1]
			c = b.split(':',1) ## 아이디:비밀번호
			user = c[0]
			pwd = c[1]
			r = requests.post(url, auth=HTTPDigestAuth(user, pwd), json=payload, headers=headers)
		else:
			r = requests.post(url, json=payload, headers=headers)
		return "%s%s" % (r.status_code, r.text) # r.text
	except r.exceptions.Timeout:
		return "Timeout  %s" % url
	except:
		return "requests.post Error: %s" % url
		
def send_data_socket(ip, port, data): 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	msg_data = ('%s'%data)
	try: 
		s.connect((ip,port))
		ret = s.send(msg_data) 
		s.close() 
		return (msg_data, ret)
	except socket.error as error:
		return 0, error.errno
	except socket.timeout:
		return 0, 'timeout'
	finally:
		s.close()		