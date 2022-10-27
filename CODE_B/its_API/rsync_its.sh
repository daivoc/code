#!/bin/bash

# sshpass -p its_iot rsync -avzr -e "ssh -p 112.187.234.55" --delete --exclude='data' ./its_web/ pi@112.187.234.55:/var/www/html/its_web

### # 로컬 ITS 업데이트 소스 생성
### rsync -avzr --delete --exclude='data' pi@192.168.0.9:/var/www/html/its_web ./update/
### rsync -avzr --delete pi@192.168.0.9:/data ./update/
### # 리모트 업데이트 실행 명령어
### rsync -avzr --delete --exclude='data' pi@115.139.183.226:./update/its_web /var/www/html/ 
### rsync -avzr --delete pi@115.139.183.226:./update/pi/ /data
### # 로컬 업데이트 실행 명령어
### rsync -avzr --delete --exclude='data' pi@192.168.0.9:/var/www/html/its_web /var/www/html/ 
### rsync -avzr --delete pi@192.168.0.9: /data

## 파라미터가 없으면 종료 
if [ "$#" -lt 1 ]; then
	## Array variable
	ipListS=()
	# ipListS+=('192.168.0.3:22') # Rasbian Desktop
	# ipListS+=('192.168.0.4:22') # Ubuntu Desktop
	# ipListS+=('192.168.0.8:22') # Rasbian
	# ipListS+=('192.168.0.10:22') # Rasbian
	ipListS+=('192.168.0.20:22') # ALL 옵텍스
	# ipListS+=('192.168.0.29:22') # ALL 옵텍스
	ipListS+=('192.168.0.30:22') # GPIO 옵텍스
	# ipListS+=('192.168.0.40:22') # SPEED 옵텍스
	# ipListS+=('192.168.0.50:22') # BSS 옵텍스
	# ipListS+=('192.168.0.60:22') # BSS_R 옵텍스
	# ipListS+=('192.168.0.70:22') # RLS 옵텍스
	ipListS+=('192.168.0.80:22') # PARKING 옵텍스
	# ipListS+=('192.168.0.90:22') # 옵텍스
	#ipListS+=('192.168.0.100:22') # 옵텍스
	# ipListS+=('192.168.0.128:22') # Rasbian Desktop
else
	## IP Address
	## ex: ./rsync_its.sh 192.168.0.29
	ipListS=("$1:22")
fi

## Home Dir
# homeName="ecos_its-OPTEX"
homeName=${PWD##*/}

echo ""
echo ">>> $homeName ${ipListS[@]} <<<"
echo ""

rPassword="its_iot"

K='\e[30m' # : 글자색:검정
R='\e[31m' # : 글자색:빨강
G='\e[32m' # : 글자색:초록
Y='\e[33m' # : 글자색:노랑
B='\e[34m' # : 글자색:파랑
M='\e[35m' # : 글자색:마젠트(분홍)
C='\e[36m' # : 글자색:시안(청록)
W='\e[37m' # : 글자색:백색
X='\e[39m' # : 글자색으로 기본값으로

BK='\e[40m' # : 바탕색:흑색
BR='\e[41m' # : 바탕색:적색
BG='\e[42m' # : 바탕색:녹색
BY='\e[43m' # : 바탕색:황색
BB='\e[44m' # : 바탕색:청색
BM='\e[45m' # : 바탕색:분홍색
BC='\e[46m' # : 바탕색:청록색
BW='\e[47m' # : 바탕색:흰색
BX='\e[49m' # : 바탕색을 기본값으로

function its_GPIO {
	#### its_GPIO
	if [ -d "/home/pi/$homeName/its_GPIO" ]; then
		cd /home/pi/$homeName/its_GPIO
		rm *.pyc
		python -m compileall config.py module.py GPIO.py run_GPIO.py # >/dev/null 2>&1
		mkdir -p ./GPIO
		# rm ./GPIO/*.pyc
		cp readme.txt config.json config.pyc module.pyc GPIO.pyc run_GPIO.pyc table_GPIO.js table_templet.html ./GPIO/ > /dev/null

		# cp -R node_modules GPIO ## 복사를 위해 한번만 실행

		rsync -avzr --delete ./GPIO/ /home/pi/ITS_PKG/code/GPIO >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:GPIO"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./GPIO/ pi@${ADDR[0]}:GPIO >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_GPWIO {
	#### its_GPWIO
	if [ -d "/home/pi/$homeName/its_GPWIO" ]; then
		cd /home/pi/$homeName/its_GPWIO
		rm *.pyc
		python -m compileall GPWIO.py # >/dev/null 2>&1
		mkdir -p ./GPWIO
		# rm ./GPWIO/*.pyc
		cp  config.json run GPWIO.pyc GPWIO.js GPWIO.html ./GPWIO/ > /dev/null

		rsync -avzr --delete ./GPWIO/ /home/pi/ITS_PKG/code/GPWIO >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:GPWIO"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./GPWIO/ pi@${ADDR[0]}:GPWIO >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_API {
	#### its_API
	if [ -d "/home/pi/$homeName/its_API" ]; then
		cd /home/pi/$homeName/its_API
		rm *.pyc
		python -m compileall itsAPI.py run_itsAPI.py streaming.py # >/dev/null 2>&1
		mkdir -p ./API
		# rm ./API/*.pyc
		cp config.json run itsAPI.pyc run_itsAPI.pyc itsAPI.js itsAPI.html itsAPI.php streaming.pyc ./API/ > /dev/null

		rsync -avzr --delete ./API/ /home/pi/ITS_PKG/code/API >/dev/null 2>&1

		# ## for client
		# cp -r api-ecos.conf client ./API/ > /dev/null
		# chmod -R 755 ./API/client

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:API"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" ./API/ pi@${ADDR[0]}:API >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_GPACU {
	#### its_GPACU
	if [ -d "/home/pi/$homeName/its_GPACU" ]; then
		cd /home/pi/$homeName/its_GPACU
		rm *.pyc
		python -m compileall GPACU.py # >/dev/null 2>&1
		mkdir -p ./GPACU
		# rm ./GPACU/*.pyc
		cp  config.json run GPACU.pyc GPACU.js GPACU.html ./GPACU/ > /dev/null

		rsync -avzr --delete ./GPACU/ /home/pi/ITS_PKG/code/GPACU >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:GPACU"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./GPACU/ pi@${ADDR[0]}:GPACU >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_FRAME {
	#### its_FRAME
	if [ -d "/home/pi/$homeName/its_FRAME" ]; then
		cd /home/pi/$homeName/its_FRAME
		rm *.pyc
		python -m compileall run_FRAME.py # >/dev/null 2>&1
		mkdir -p ./FRAME
		# rm ./FRAME/*.pyc
		cp config.json camera.json templet.json run_FRAME.pyc FRAME.js FRAME.html ./FRAME/ > /dev/null

		rsync -avzr --delete ./FRAME/ /home/pi/ITS_PKG/code/FRAME >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:FRAME"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./FRAME/ pi@${ADDR[0]}:FRAME >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_SRF {
	#### its_SPOTTER
	if [ -d "/home/pi/$homeName/its_partner/its_SRF" ]; then
		cd /home/pi/$homeName/its_partner/its_SRF
		rm *.pyc
		python -m compileall module.py spotter.py # >/dev/null 2>&1
		mkdir -p ./SRF
		# rm ./SRF/*.pyc
		cp -r config.json language.json module.pyc run spotter.pyc spotter.js spotter_templet.html www ./SRF/ > /dev/null

		rsync -avzr --delete ./SRF/ /home/pi/ITS_PKG/code/SRF >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:SRF"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./SRF/ pi@${ADDR[0]}:SRF >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_FSI {
	#### its_SPOTTER
	if [ -d "/home/pi/$homeName/its_partner/its_FSI" ]; then
		cd /home/pi/$homeName/its_partner/its_FSI
		rm *.pyc
		python -m compileall FSI.py run_FSI.py FDX.py # >/dev/null 2>&1
		mkdir -p ./FSI
		# rm ./FSI/*.pyc
		cp -r config.json run FSI.pyc run_FSI.pyc FDX.pyc ./FSI/ > /dev/null

		rsync -avzr --delete ./FSI/ /home/pi/ITS_PKG/code/FSI >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:FSI"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./FSI/ pi@${ADDR[0]}:FSI >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_GIKENP {
	#### its_GIKENP
	if [ -d "/home/pi/$homeName/its_partner/its_GIKENP" ]; then
		cd /home/pi/$homeName/its_partner/its_GIKENP
		rm *.pyc
		python -m compileall GIKENP.py run_GIKENP.py  # >/dev/null 2>&1
		mkdir -p ./GIKENP
		# rm ./GIKENP/*.pyc
		cp config.json run run_GIKENP.pyc GIKENP.pyc GIKENP.js GIKENP.html ./GIKENP/ > /dev/null

		rsync -avzr --delete ./GIKENP/ /home/pi/ITS_PKG/code/GIKENP >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:GIKENP"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./GIKENP/ pi@${ADDR[0]}:GIKENP >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_GIKENT {
	#### its_GIKENT
	if [ -d "/home/pi/$homeName/its_partner/its_GIKENT" ]; then
		cd /home/pi/$homeName/its_partner/its_GIKENT
		rm *.pyc
		python -m compileall GIKENT.py run_GIKENT.py  # >/dev/null 2>&1
		mkdir -p ./GIKENT
		# rm ./GIKENT/*.pyc
		cp config.json run run_GIKENT.pyc GIKENT.pyc GIKENT.js GIKENT.html ./GIKENT/ > /dev/null

		rsync -avzr --delete ./GIKENT/ /home/pi/ITS_PKG/code/GIKENT >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:GIKENT"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./GIKENT/ pi@${ADDR[0]}:GIKENT >/dev/null 2>&1
			TOUCH;
		done
	fi
}


function its_TAILING {
	#### its_TAILING
	if [ -d "/home/pi/$homeName/its_TAILING" ]; then
		cd /home/pi/$homeName/its_TAILING
		rm *.pyc
		python -m compileall TAILING.py run_TAILING.py # >/dev/null 2>&1
		mkdir -p ./TAILING
		# rm ./TAILING/*.pyc
		cp config.json run run_TAILING.pyc TAILING.pyc TAILING.js TAILING.html ./TAILING/ > /dev/null
		cp streaming.py test.py ./TAILING/ > /dev/null

		rsync -avzr --delete ./TAILING/ /home/pi/ITS_PKG/code/TAILING >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:TAILING"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./TAILING/ pi@${ADDR[0]}:TAILING >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function optex_BSS {
	#### optex_BSS
	if [ -d "/home/pi/$homeName/its_optex/optex_BSS" ]; then
		cd /home/pi/$homeName/its_optex/optex_BSS
		rm *.pyc
		python -m compileall config.py module.py optex_BSS01.py run_optex.py # >/dev/null 2>&1
		mkdir -p ./optex_BSS
		cp readme.txt config.pyc module.pyc optex_BSS01.pyc run_optex.pyc ./optex_BSS/ > /dev/null

		rsync -avzr --delete ./optex_BSS/ /home/pi/ITS_PKG/code/optex_BSS >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:optex_BSS"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./optex_BSS/ pi@${ADDR[0]}:optex_BSS >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function optex_RLS_R {
	##### optex_RLS_R
	if [ -d "/home/pi/$homeName/its_optex/optex_RLS_R" ]; then
		cd /home/pi/$homeName/its_optex/optex_RLS_R
		rm *.pyc
		python -m compileall config.py module.py optex_RLS_R.py optex_RLS_alarm.py run_optex.py # >/dev/null 2>&1
		mkdir -p ./optex_RLS_R
		cp readme.txt realtime_RLS.js realtime_RLS_templet.html realtime_RLS_templet_IMS.html realtime_RLS_templet_Area.html config.pyc module.pyc optex_RLS_R.pyc optex_RLS_alarm.pyc run_optex.pyc ./optex_RLS_R/ > /dev/null

		rsync -avzr --delete ./optex_RLS_R/ /home/pi/ITS_PKG/code/optex_RLS_R >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:optex_RLS_R"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./optex_RLS_R/ pi@${ADDR[0]}:optex_RLS_R >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function optex_SPEED {
	#### optex_SPEED
	if [ -d "/home/pi/$homeName/its_optex/optex_SPEED" ]; then
		cd /home/pi/$homeName/its_optex/optex_SPEED
		rm *.pyc
		python -m compileall config_db.py module_for_optex.py optex_SPEED.py config_sensor.py module_for_mysql.py module_for_sendmail.py run_optex.py # >/dev/null 2>&1
		mkdir -p ./optex_SPEED 2>/dev/null
		cp readme.txt config_db.pyc module_for_optex.pyc optex_SPEED.pyc config_sensor.pyc module_for_mysql.pyc module_for_sendmail.pyc run_optex.pyc ./optex_SPEED/ > /dev/null

		rsync -avzr --delete ./optex_SPEED/ /home/pi/ITS_PKG/code/optex_SPEED >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:optex_SPEED"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./optex_SPEED/ pi@${ADDR[0]}:optex_SPEED >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_CAM {
	#### its_CAM
	if [ -d "/home/pi/$homeName/its_CAM" ]; then
		cd /home/pi/$homeName/its_CAM
		mkdir -p ./CAM
		mkdir -p ./CAM/model
		python -m compileall *.py model/*.py # >/dev/null 2>&1

		cp config.json module.pyc CAM.pyc run_CAM.pyc CAM.js CAM.html ./CAM/ > /dev/null
		cp model/*.pyc ./CAM/model/ > /dev/null
		rm *.pyc model/*.pyc

		rsync -avzr --delete ./CAM/ /home/pi/ITS_PKG/code/CAM >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BB Remote sync $BX pi@${ADDR[0]}:CAM"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./CAM/ pi@${ADDR[0]}:CAM >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function its_MONITOR {
	##### MONITOR
	if [ -d "/home/pi/$homeName/its_MONITOR" ]; then
		cd /home/pi/$homeName/its_MONITOR
		rm *.pyc
		python -m compileall run_IMS.py # >/dev/null 2>&1
		mkdir -p ./MONITOR
		cp config.json camera.json language.json readme.txt ipCamInfo.js ipCamView.js ipCamView.html procOnvif.js its_M_map.js its_M_map_templet.html run_IMS.pyc ./MONITOR/ > /dev/null
		chmod 666 ./MONITOR/*.json
		# cp -R node_modules MONITOR ## 복사를 위해 한번만 실행

		# IMS 기능으로 Ubuntu Mate의 기본 사용자는 [ims]로 사용자 [ims]가 접근 가능 하도록 퍼미션을 변경 한다. 
		# chmod 707 -R ./MONITOR

		rsync -avzr --delete ./MONITOR/ /home/pi/ITS_PKG/code/MONITOR >/dev/null 2>&1
		
		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BM Remote sync $BX pi@${ADDR[0]}:MONITOR"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./MONITOR/ pi@${ADDR[0]}:MONITOR >/dev/null 2>&1
			TOUCH;
		done
	fi
}	

function its_utility {
	##### utility
	if [ -d "/home/pi/$homeName/its_utility" ]; then
		cd /home/pi/$homeName/its_utility
		python -m compileall download_ITS.py systemStatus.py ipSetup.py licenseKey.py licenseSrv.py productKey.py readPort.py readGPIO.py readGPIO_single.py portScan.py its_Scan.py check_RLS.py check_Relay.py streamClip.py check_GPACU.py # >/dev/null 2>&1
		
		mkdir -p ./utility
		cp download_ITS.pyc systemStatus.pyc ipSetup.pyc licenseKey.pyc licenseSrv.pyc productKey.pyc readPort.pyc readGPIO.pyc readGPIO_single.pyc portScan.pyc its_Scan.pyc check_RLS.pyc check_Relay.pyc streamClip.pyc check_GPACU.pyc ./utility/ > /dev/null
		cp networkSetup.py networkSetup.json ./utility/ > /dev/null
		cp setup_its.sh ./utility/ > /dev/null
		# cp update_its.sh ./utility/ > /dev/null
		# cp onvifGetPTZ.js onvifScanCamera.js onvifGetCamInfo.js onvifCamPTZ.js onvifStreamRSP.js onvifSnapshot.js onvifSnapshot.html ./utility/ > /dev/null
		rm *.pyc
		
		rsync -avzr --delete ./utility/ /home/pi/ITS_PKG/code/utility >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BM Remote sync $BX pi@${ADDR[0]}:utility"
			# sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./utility/ pi@${ADDR[0]}:utility >/dev/null 2>&1
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./utility/ pi@${ADDR[0]}:utility >/dev/null 2>&1
			TOUCH;
		done
	fi
}	

function its_common {
	##### common
	if [ -d "/home/pi/$homeName/its_common" ]; then
		cd /home/pi/$homeName/its_common
		python -m compileall m_authRequest.py m_findAngle.py # >/dev/null 2>&1
		python -m compileall audioOut.py audioOutVolume.py dbRepairOptimize.py scanSensor.py run_table.py msg_on_image.py resetIP.py resetSensor.py systemConfig.py watchdog.py gikenEventServerTable_DB.py # >/dev/null 2>&1

		mkdir -p ./common
		cp m_authRequest.pyc m_findAngle.pyc ./common/ > /dev/null
		cp config.json language.json audioOut.pyc audioOutVolume.pyc dbRepairOptimize.pyc scanSensor.pyc run_table.pyc msg_on_image.pyc resetIP.pyc resetSensor.pyc systemConfig.pyc watchdog.pyc gikenEventServerTable_DB.pyc table_union.js table_templet.html exportDB.sh ./common/ > /dev/null
		chmod 666 ./common/config.json
		rm *.pyc

		rsync -avzr --delete ./common/ /home/pi/ITS_PKG/code/common >/dev/null 2>&1

		for i in "${ipListS[@]}"
		do
			IFS=':' read -ra ADDR <<< "$i"
			echo -e "$BC$R Remote sync $X$BX pi@${ADDR[0]}:common"
			sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./common/ pi@${ADDR[0]}:common >/dev/null 2>&1
			TOUCH;
		done
	fi
}

function WEB {
	cd /home/pi/$homeName

	rsync -avzr --delete ./its_web/ /home/pi/ITS_PKG/web # >/dev/null 2>&1

	for i in "${ipListS[@]}"
	do
		IFS=':' read -ra ADDR <<< "$i"
		echo -e "$BR Remote sync $BX pi@${ADDR[0]}:its_web"
		sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete --exclude='data/session' --exclude='data/log' --exclude='data/file' --exclude='data/cache' --exclude='data/config' ./its_web pi@${ADDR[0]}:/var/www/html/ #  >/dev/null 2>&1
		# sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./its_web/theme pi@${ADDR[0]}:/var/www/html/its_web/ #  >/dev/null 2>&1
		# sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete ./its_web/home/pi/*.php pi@${ADDR[0]}:/var/www/html/its_web/home/pi/ #  >/dev/null 2>&1
		TOUCH_WEB;
	done
}

# function BACKUP {
# 	echo -e "BACKUP from /home/pi/ecos_its-OPTEX to /optex/pi/"
# 	rsync -avzr --delete /data /optex/
# 	rsync -avzr --delete /var/www/html/optex_web /optex/
# }

function TOUCH {
	echo -e "Touch pi@${ADDR[0]}"
	sshpass -p $rPassword ssh pi@${ADDR[0]} /usr/bin/touch ~
}

function TOUCH_WEB {
	echo -e "Touch pi@${ADDR[0]}"
	sshpass -p $rPassword ssh pi@${ADDR[0]} /usr/bin/touch /var/www/html/its_web
}


PS3="Select : "
select yn in "API" "GPIO" "GPACU" "GPWIO" "SRF" "FSI" "FRAME" "GIKENP" "GIKENT" "TAILING" "BSS" "RLS_R" "SPEED" "CAM" "MONITOR" "Utility" "Common" "WEB" 
do
	echo ""
	echo ">>> $homeName ${ipListS[@]} <<<"
	echo ""
	case $yn in
		API ) its_API;;
		GPIO ) its_GPIO;;
		GPACU ) its_GPACU;;
		GPWIO ) its_GPWIO;;
		SRF ) its_SRF;;
		FSI ) its_FSI;;
		FRAME ) its_FRAME;;
		GIKENP ) its_GIKENP;;
		GIKENT ) its_GIKENT;;
		TAILING ) its_TAILING;;
		BSS ) optex_BSS;;
		RLS_R ) optex_RLS_R;;
		SPEED ) optex_SPEED;;
		CAM ) its_CAM;;
		MONITOR ) its_MONITOR;;
		Utility ) its_utility;;
		Common ) its_common;;
		WEB) WEB;;
		*) exit;;
	esac
	echo "cd /home/pi/ITS_PKG && git add . && git commit -m'Updated:ITS_PKG' && git push"
	echo "rsync -avzr --delete /home/pi/ITS_PKG pi@119.207.126.79:~"
done	
	