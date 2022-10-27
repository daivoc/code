#!/usr/bin/env python
# -*- coding: utf-8 -*-  

##################################################
# GPIO Control and Managment
##################################################

from module import *


# 시스템 헬스체크 데몬 실행
def run_demon_GPWIO():
	cmd = "cd %s && python ./GPWIO.pyc 2>&1 & " % (share['path']['gpwio'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_GPWIO"
def run_demon_GPACU():
	cmd = "cd %s && python ./GPACU.pyc 2>&1 & " % (share['path']['gpacu'])
	p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
	return "run_demon_GPACU"


def main():
	# GPIO Relay Connection - 센서 설정 보드로 부터 읽은 필요한 값을 변수로 포함하여 실행 한다.
	# 센서 아이디, 센서 타임아웃, 위도, 경도 - w_sensor_id, w_sensor_timeout, w_sensor_lat_s, w_sensor_lng_s
	# 위도 경도는 관제 모니터링을 위한 임시 값으로 사용하기 위함
	# w_cfg_sensor_list_GPIO = read_table_w_cfg_sensorID_GPIO()
	for row in read_table_w_cfg_sensorID_GPIO():
		# Node Js를 통한 실시간 모니터링 입력 포트 http://localhost:myPortIn
		GPIO_sensor_noOfZone = row["w_sensor_noOfZone"]

		ECOS_system_port = row["w_system_port"]
		ECOS_system_portOut = ECOS_system_port + 2
		
		GPIO_table_PortIn = row["w_table_PortIn"]
		GPIO_table_PortOut = row["w_table_PortOut"]

		GPIO_node = '%s %s %s 1' % (GPIO_table_PortIn, GPIO_table_PortOut, GPIO_sensor_noOfZone) # node table.js 8008 9008 100 1
		result = run_demon_GPIO_table(GPIO_node)
		# print('\tRunning Table: %s' % result)
		
		ECOS_exeName = "%s" % row["wr_id"]
		result = run_GPIO(ECOS_exeName)
		# print('\tRunning GPIO: %s \n' % result)

if __name__ == '__main__':
	
	kill_demon_GPIO_table()
	kill_demon_GPIO()
	time.sleep(1) ## 주의) 직전에 실행된 프로세서를 죽이는 오류 발생 가능
		
	err_max = 20
	while True: # 데이터베이스 확인
		if database_test(): 
			print(G+"*** PASS ***\n\tDatabase connected."+W) # 데이터베이스 쿼리 오류
			break
		else:
			print(R+"*** ERROR ***\n\tDatabase connected error.\nPlease check database configuration. Waiting ..."+W) # 데이터베이스 쿼리 오류
			time.sleep(1)
			err_max=err_max-1
			if not err_max: exit('Time out')

	# ###########################
	# ## 시스템 라이센스 확인 - 시작
	# # /tmp/license_hash가 manager의 mb_1의 값과 일치하는지 확인 한다.
	# license = str(itsMemberConfig('manager','mb_1')['mb_1']).strip() # 라이센스 확인
	# if os.path.isfile('/tmp/'+license):
	# 	print(C+"\nPass ITS License\n"+W)
	# else:
	# 	print(R+"\nNot Found ITS License\n"+W+"\tPlease Call to Service Provider!!")
	# 	exit() 
	# ## 시스템 라이센스 확인 - 종료
	# ###########################

	make_table_GPIO(ITS_gpio_path+"/table_templet.html", ITS_gpio_path+"/table_GPIO.html") # index.html 생성후 SVG 파일 적용

	main()

	share = readConfig('/home/pi/common/config.json')
	# GPIO 과정이 모두 실행된후 GPWIO, GPACU를 실행한다.

	# ioB = str(itsMemberConfig('its','mb_4')['mb_4']).strip() # 라이센스 확인
	# if ioB == 'acu':
	# 	print run_demon_GPACU()
	# else:
	# 	print run_demon_GPWIO()
	
	# print run_demon_itsAPI()

	exit()