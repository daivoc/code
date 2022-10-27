#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import time
import datetime

def main():
    while True:
        ret, frame = cap.read()
        if ret:  # True or False
            out.write(frame)

        if time.time() > timeout:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # rtsp_stream_link = 'rtsp://root:pass@192.168.0.38/axis-media/media.amp'
    # rtsp_stream_link = 'rtsp://admin:admin@96.48.233.195:5550'
    # rtsp_stream_link = 'rtsp://admin:admin@96.48.233.195:5540'
    rtsp_stream_link = 0

    cap = cv2.VideoCapture(rtsp_stream_link)

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    out = cv2.VideoWriter('/var/www/html/its_web/data/image/tailing_g400t400_192_168_0_29_0001/output.avi', fourcc, 20.0, (640, 480))

    timeout = time.time() + 5  # 5 seconds from now
    main()
