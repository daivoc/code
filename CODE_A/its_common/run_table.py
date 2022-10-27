#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import time
import subprocess 
import json

with open("./config.json") as json_file:  
	config = json.load(json_file)

# 모니터링을 위한 지도파일을 생성한다.
def make_table_union_map(source, target):
	__script_jquery_js__ = '%s/jquery/jquery-3.1.1.min.js' % config['path']['common']
	__script_jquery_js__ = '<script>'+open(__script_jquery_js__, 'r').read()+'</script>'
	__script_jquery_ui_js__ = '%s/jquery/ui/jquery-ui.js' % config['path']['common']
	__script_jquery_ui_js__ = '<script>'+open(__script_jquery_ui_js__, 'r').read()+'</script>'
	__style_jquery_ui_css__ = '%s/jquery/ui/jquery-ui.css' % config['path']['common']
	__style_jquery_ui_css__ = '<style>'+open(__style_jquery_ui_css__, 'r').read()+'</style>'
	
	# __svg_pan_zoom__ = '%s/svg-pan-zoom/svg-pan-zoom.js' % config['path']['common']
	# __svg_pan_zoom__ = '<script>'+open(__svg_pan_zoom__, 'r').read()+'</script>'
	# __smoothiecharts__ = '%s/smoothiecharts/smoothie.js' % config['path']['common']
	# __smoothiecharts__ = '<script>'+open(__smoothiecharts__, 'r').read()+'</script>'

	# print __style_jquery_ui_css__
	with open(source, 'r') as templet_file:
		tmp_its_tmp = templet_file.read()
		templet_file.close()
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_js__', __script_jquery_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__script_jquery_ui_js__', __script_jquery_ui_js__)
		tmp_its_tmp = tmp_its_tmp.replace('__style_jquery_ui_css__', __style_jquery_ui_css__)
		# tmp_its_tmp = tmp_its_tmp.replace('__svg_pan_zoom__', __svg_pan_zoom__)
		# tmp_its_tmp = tmp_its_tmp.replace('__smoothiecharts__', __smoothiecharts__)
		
		with open(target, 'w') as tmp_its_file:
			tmp_its_file.write(tmp_its_tmp)
			tmp_its_file.close()
			

# 실행하고 있는 arg 단어가 포함된 데몬을 awk를 이용하여 모두 종료 시킨다.
def kill_demon_UNION_table(): 
	cmd = "kill $(ps aux | grep '[n]ode table_union.js' | awk '{print $2}')"
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	time.sleep(1)
	
# 확인된 변수로 데몬을 실행 한다
# cd /var/www/html/its_web/theme/ecos-wits_optex/utility/nodeJs_table
# node ./table_union.js 64444 64446
def run_demon_UNION_table(arg): 
	# path = "theme/ecos-its_optex/utility/nodeJs_table/" # Optex Theme
	# cmd = "cd /var/www/html/its_web/%s; node table_union.js %s 2>&1 & " % (path, arg)
	cmd = "cd %s; node table_union.js %s 2>&1 & " % (config['path']['common'], arg)
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	
if __name__ == '__main__':
	kill_demon_UNION_table()

	make_table_union_map(config['path']['common']+"/table_templet.html", config['path']['common']+"/table_union.html") # index.html 생성후 SVG 파일 적용
	
	ECOS_unionTable = '%s %s' % (config['port']['tableUnion'], config['port']['tableUnion'] + 2)
	print('Running UNION Table: %s \n' % run_demon_UNION_table(ECOS_unionTable))		
		
	exit()	