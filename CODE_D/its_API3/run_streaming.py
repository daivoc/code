#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import time
import subprocess 

def kill_demon_streaming(): 
	cmd = "sudo kill -9 $(ps aux | grep ' streaming.pyc' | awk '{print $2}')" # '{스페이스} itsAPI.pyc, itsAPI.js 포함' 중요함
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	return "kill_demon_streaming"

def run_demon_streaming(): 
	cmd = "python3 streaming.pyc 2>&1 & "
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_streaming"

def main():
	print(run_demon_streaming())
	
if __name__ == '__main__':
	print(kill_demon_streaming())
	main()
	# exit()	