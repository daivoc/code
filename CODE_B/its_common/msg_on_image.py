#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os, sys, traceback
from PIL import Image, ImageDraw, ImageFont

def main(): 
	if len(sys.argv) is 3:
		path = sys.argv[1]
		text = sys.argv[2]
		if os.stat(path).st_size:
			image = Image.open(open(path, 'rb'))
			draw = ImageDraw.Draw(image)
			font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",30)
			draw.text((200, 1000), text, font=font) # X, Y 해상도에 위치함
			image.save(path,optimize=True,quality=100)
			print "write message to photo"
		else:
			print "error - no photo found check camera connection"
	else:
		print "error - need ARGV!"
		exit()
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print ("\nCancelled")
	except Exception, e:
		print str(e)
		traceback.print_exc()
		os._exit(1)	