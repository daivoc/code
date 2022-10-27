#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
## FLASK
from flask import Flask, render_template #, session
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app)

config = None

@app.route('/')
def index(name=None):
	return render_template('ims.html')

@socketio.event
def connect():
	emit('connect', config)

## 환경설정 파일(JSON) 읽기
def readConfig(pathName):
	with open(pathName) as json_file:  
		return json.load(json_file)

def main():
	print(f'Access: http://localhost:{config["port"]["forIMS"]}')
	socketio.run(app, host='0.0.0.0', port=config["port"]["forIMS"])

if __name__ == '__main__':
	config = readConfig("./config_RLS3.json")
	main()