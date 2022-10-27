#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://codeday.me/ko/qa/20190505/463802.html

## RTSP 정보로 부터 
## 실시간 화면출력을 하거나 
## 스트리밍 클립을 만들거나
## 타임랩 이미지를 저장하는 기능
## 만들어진 자료는 mkdir_p 기능을 통해 
## 서브폴서 생성기능을 포함 한다.

from threading import Thread
import cv2
import time
import datetime
import errno
import os

class RTSPVideoWriterObject(object):
	def __init__(self, src=0):
		# Create a VideoCapture object
		self.capture = cv2.VideoCapture(src)

		# Default resolutions of the frame are obtained (system dependent)
		self.frame_width = int(self.capture.get(3))
		self.frame_height = int(self.capture.get(4))

		# Set up codec and output video settings
		self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
		self.folder = datetime.datetime.now().strftime("%Y%m%d/")
		mkdir_p(image_path + self.folder)
		mkdir_p(video_path + self.folder)
		self.video_target = video_path + self.folder + datetime.datetime.now().strftime("%H%M%S_%f")[:-4]
		self.output_video = cv2.VideoWriter('%s.avi' % self.video_target, self.codec, 30, (self.frame_width, self.frame_height))

		# Start the thread to read frames from the video stream
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()

	def update(self):
		# Read the next frame from the stream in a different thread
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()

	def show_frame(self):
		# Display frames in main program
		if self.status:
			cv2.imshow('frame', self.frame)

	def stop_frame(self):
		self.capture.release()
		self.output_video.release()
		cv2.destroyAllWindows()

	def save_frame(self):
		# Save obtained frame into video output file
		self.output_video.write(self.frame)

	def snapshot_frame(self):
		# Save obtained frame into snapshot file
		image_target = image_path + self.folder + datetime.datetime.now().strftime("%H%M%S_%f")[:-4]
		cv2.imwrite('%s.jpg' % image_target, self.frame)

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

if __name__ == '__main__':
	image_path = './stream/images/'
	video_path = './stream/videos/'

	# rtsp_stream_link = 'rtsp://root:pass@192.168.0.38/axis-media/media.amp'
	# rtsp_stream_link = 'rtsp://admin:admin@96.48.233.195:5550'
	# rtsp_stream_link = 'rtsp://admin:admin@96.48.233.195:5540'
	rtsp_stream_link = 'rtsp://admin:admin@192.168.0.110'

	video_stream_widget = RTSPVideoWriterObject(rtsp_stream_link)

	timeout = time.time() + 5  # 5 seconds from now
	while True:
		try:
			video_stream_widget.show_frame()
			video_stream_widget.save_frame()
			video_stream_widget.snapshot_frame()
		except AttributeError:
			pass

		if time.time() > timeout:
			video_stream_widget.stop_frame()
			exit()
