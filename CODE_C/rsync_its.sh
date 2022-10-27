#!/bin/bash

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
> $HOME/.ssh/known_hosts
ipListS=()
if [ "$#" -lt 1 ]; then
	## Array variable
	curIP='192.168.0.10'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.20'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.30'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.40'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.50'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.60'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.70'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.80'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
	curIP='192.168.0.90'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
else
	## IP Address
	## ex: ./rsync_its.sh 192.168.0.29
	curIP=("$1")
	curIP='192.168.0.10'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
fi

## ITS PI PAss
itsPass="its_iot"

## Home Dir
homeName=${PWD##*/}

## Package Name
ITS_PKG='Cherry'
# ITS_PKG='Apple'
# ITS_PKG='Banana'
# ITS_PKG='Dragon'

if [ ! -d "$HOME/$ITS_PKG" ]; then
	mkdir -p $HOME/$ITS_PKG
elif [ ! -d "$HOME/$ITS_PKG/code" ]; then
	mkdir -p $HOME/$ITS_PKG/code
elif [ ! -d "$HOME/$ITS_PKG/web" ]; then
	mkdir -p $HOME/$ITS_PKG/web
elif [ ! -d "$HOME/$ITS_PKG/db" ]; then
	mkdir -p $HOME/$ITS_PKG/db
elif [ ! -d "$HOME/$ITS_PKG/module" ]; then
	mkdir -p $HOME/$ITS_PKG/module
else
	echo ""
fi

echo ""
echo ">>> $homeName ${ipListS[@]} <<<"
echo -e ">>> Current Package Name is $Y$ITS_PKG$X <<<"
echo ""


function TOUCH {
	echo -e "Touch pi@$1"
	sshpass -p $itsPass ssh pi@$1 /usr/bin/touch /home/pi
}

function TOUCH_WEB {
	echo -e "Touch pi@$1"
	sshpass -p $itsPass ssh pi@$1 /usr/bin/touch /var/www/html/its_web
}

function its_rsync {
	for i in "${ipListS[@]}"
	do
		echo -e "$BB Remote sync $BX pi@$i:$1"
		sshpass -p $itsPass rsync -avzr -e ssh -p 22 --delete --exclude='data' ./$1/ pi@$i:$1 >/dev/null 2>&1
		TOUCH $i;
	done
}

function its_GPIO {
	#### its_GPIO
	if [ -d "$HOME/$homeName/its_GPIO" ]; then
		cd $HOME/$homeName/its_GPIO
		rm *.pyc
		python2 -m compileall config.py module.py GPIO.py run_GPIO.py # >/dev/null 2>&1
		mkdir -p ./GPIO
		cp readme.txt config.json config.pyc module.pyc GPIO.pyc run_GPIO.pyc table_GPIO.js table_templet.html ./GPIO/ > /dev/null

		rsync -avzr --delete ./GPIO $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "GPIO"
	fi
}

function its_GPWIO {
	#### its_GPWIO
	if [ -d "$HOME/$homeName/its_GPWIO" ]; then
		cd $HOME/$homeName/its_GPWIO
		rm *.pyc
		python2 -m compileall GPWIO.py # >/dev/null 2>&1
		mkdir -p ./GPWIO
		# rm ./GPWIO/*.pyc
		cp  config.json run GPWIO.pyc GPWIO.js GPWIO.html ./GPWIO/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./GPWIO $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "GPWIO"
	fi
}

function its_API {
	#### its_API
	if [ -d "$HOME/$homeName/its_API" ]; then
		cd $HOME/$homeName/its_API
		rm *.pyc
		python2 -m compileall itsAPI.py run_itsAPI.py run_streaming.py streaming.py # >/dev/null 2>&1
		mkdir -p ./API
		# rm ./API/*.pyc
		cp config.json camera.json streaming.json run itsAPI.pyc run_itsAPI.pyc itsAPI.js itsAPI.html itsAPI.php run_streaming.pyc streaming.pyc quickGuide.pdf QnA.pdf example.html ./API/ > /dev/null

		rsync -avzr --delete ./API $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "API"
	fi
}

function its_API3 {
	#### its_API3
	if [ -d "$HOME/$homeName/its_API3" ]; then
		cd $HOME/$homeName/its_API3
		rm *.pyc
		python3.7 -m compileall -f -b itsAPI.py run_itsAPI.py run_streaming.py streaming.py
		mkdir -p ./API3
		cp config.json camera.json streaming.json itsEventProtocol.json run itsAPI.pyc run_itsAPI.pyc itsAPI.js itsAPI.html itsAPI.php run_streaming.pyc streaming.pyc readme.pdf example.html ./API3/ > /dev/null
		rsync -avzr --delete ./API3 $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "API3"
	fi
}

function its_GPACU {
	#### its_GPACU
	if [ -d "$HOME/$homeName/its_GPACU" ]; then
		cd $HOME/$homeName/its_GPACU
		rm *.pyc
		python2 -m compileall GPACU.py # >/dev/null 2>&1
		mkdir -p ./GPACU
		# rm ./GPACU/*.pyc
		cp  config.json run GPACU.pyc GPACU.js GPACU.html ./GPACU/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./GPACU $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "GPACU"
	fi
}

function its_FRAME {
	#### its_FRAME
	if [ -d "$HOME/$homeName/its_FRAME" ]; then
		cd $HOME/$homeName/its_FRAME
		rm *.pyc
		python2 -m compileall run_FRAME.py # >/dev/null 2>&1
		mkdir -p ./FRAME
		# rm ./FRAME/*.pyc
		cp config.json camera.json templet.json run_FRAME.pyc FRAME.js FRAME.html ./FRAME/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./FRAME $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "FRAME"
	fi
}

function its_SRF {
	#### its_SPOTTER
	if [ -d "$HOME/$homeName/its_partner/its_SRF" ]; then
		cd $HOME/$homeName/its_partner/its_SRF
		rm *.pyc
		python2 -m compileall module.py spotter.py # >/dev/null 2>&1
		mkdir -p ./SRF
		# rm ./SRF/*.pyc
		cp -r config.json language.json run spotter.pyc spotter.js spotter_templet.html www ./SRF/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./SRF $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "SRF"
	fi
}

function its_FSI {
	#### its_SPOTTER
	if [ -d "$HOME/$homeName/its_partner/its_FSI" ]; then
		cd $HOME/$homeName/its_partner/its_FSI
		rm *.pyc
		python2 -m compileall FSI.py run_FSI.py FDX.py # >/dev/null 2>&1
		mkdir -p ./FSI
		# rm ./FSI/*.pyc
		cp -r config.json run FSI.pyc run_FSI.pyc FDX.pyc FSI.js FSI.html ./FSI/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./FSI $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "FSI"
	fi
}

function its_GIKENP {
	#### its_GIKENP
	if [ -d "$HOME/$homeName/its_partner/its_GIKENP" ]; then
		cd $HOME/$homeName/its_partner/its_GIKENP
		rm *.pyc
		python2 -m compileall GIKENP.py run_GIKENP.py  # >/dev/null 2>&1
		mkdir -p ./GIKENP
		# rm ./GIKENP/*.pyc
		cp config.json run run_GIKENP.pyc GIKENP.pyc GIKENP.js GIKENP.html ./GIKENP/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./GIKENP $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "GIKENP"
	fi
}

function its_GIKENC {
	#### its_GIKENC
	if [ -d "$HOME/$homeName/its_partner/its_GIKENC" ]; then
		cd $HOME/$homeName/its_partner/its_GIKENC
		rm *.pyc
		python2 -m compileall GIKENC.py run_GIKENC.py  # >/dev/null 2>&1
		mkdir -p ./GIKENC
		# rm ./GIKENC/*.pyc
		cp config.json run run_GIKENC.pyc GIKENC.pyc GIKENC.js GIKENC.html ./GIKENC/ > /dev/null

		rsync -avzr --delete ./GIKENC $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "GIKENC"
	fi
}

function its_GIKENT {
	#### its_GIKENT
	if [ -d "$HOME/$homeName/its_partner/its_GIKENT" ]; then
		cd $HOME/$homeName/its_partner/its_GIKENT
		rm *.pyc
		python2 -m compileall GIKENT.py run_GIKENT.py  # >/dev/null 2>&1
		mkdir -p ./GIKENT
		# rm ./GIKENT/*.pyc
		cp config.json run run_GIKENT.pyc GIKENT.pyc GIKENT.js GIKENT.html ./GIKENT/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./GIKENT $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "GIKENT"
	fi
}

function its_TAILING {
	#### its_TAILING
	if [ -d "$HOME/$homeName/its_TAILING" ]; then
		cd $HOME/$homeName/its_TAILING
		rm *.pyc
		python2 -m compileall TAILING.py run_TAILING.py # >/dev/null 2>&1
		mkdir -p ./TAILING
		# rm ./TAILING/*.pyc
		cp config.json run run_TAILING.pyc TAILING.pyc TAILING.js TAILING.html ./TAILING/ > /dev/null
		cp streaming.py test.py ./TAILING/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./TAILING $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "TAILING"
	fi
}

function optex_BSS {
	#### optex_BSS
	if [ -d "$HOME/$homeName/its_optex/optex_BSS" ]; then
		cd $HOME/$homeName/its_optex/optex_BSS
		rm *.pyc
		python2 -m compileall config.py module.py optex_BSS01.py run_optex.py # >/dev/null 2>&1
		mkdir -p ./optex_BSS
		cp readme.txt config.pyc module.pyc optex_BSS01.pyc run_optex.pyc ./optex_BSS/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./optex_BSS $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "optex_BSS"
	fi
}

function optex_RLS_R {
	##### optex_RLS_R
	if [ -d "$HOME/$homeName/its_optex/optex_RLS_R" ]; then
		cd $HOME/$homeName/its_optex/optex_RLS_R
		rm *.pyc
		python2 -m compileall config.py module.py optex_RLS_R.py optex_RLS_alarm.py run_optex.py # >/dev/null 2>&1
		mkdir -p ./optex_RLS_R
		cp readme.txt realtime_RLS.js realtime_RLS_templet.html realtime_RLS_templet_IMS.html realtime_RLS_templet_Area.html config.pyc module.pyc optex_RLS_R.pyc optex_RLS_alarm.pyc run_optex.pyc ./optex_RLS_R/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./optex_RLS_R $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "optex_RLS_R"
	fi
}

function optex_RLS_V {
	##### optex_RLS_V
	if [ -d "$HOME/$homeName/its_optex/optex_RLS_V" ]; then
		cd $HOME/$homeName/its_optex/optex_RLS_V
		rm *.pyc
		python2 -m compileall config.py module.py optex_RLS_V.py optex_RLS_alarm.py run_optex.py # >/dev/null 2>&1
		python3.7 -m compileall -f -b getSensorInfo.py

		mkdir -p ./optex_RLS_V
		cp readme.md realtime_RLS.js realtime_RLS_templet.html realtime_RLS_templet_IMS.html realtime_RLS_templet_Area.html config.pyc module.pyc optex_RLS_V.pyc optex_RLS_alarm.pyc run_optex.pyc getSensorInfo.pyc ./optex_RLS_V/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./optex_RLS_V $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "optex_RLS_V"
	fi
}

function its_RLS3 {
	##### its_RLS3
	if [ -d "$HOME/$homeName/its_RLS3" ]; then
		cd $HOME/$homeName/its_RLS3
		python3.7 -m compileall -f -b run_RLS3.py RLS3.py setup.py ims.py

		mkdir -p ./RLS3
		mkdir -p ./RLS3/static
		mkdir -p ./RLS3/templates
		# cp config.json readme.md realtime_RLS.js realtime_RLS_templet.html realtime_RLS_templet_Area.html run_RLS3.pyc RLS3.pyc ./RLS3/ > /dev/null
		cp config.json readme.md realtime_RLS.js realtime_RLS_templet.html run_RLS3.pyc RLS3.pyc setup.pyc ims.pyc ./RLS3/ > /dev/null
		cp ./templates/index.html ./templates/setup.html ./templates/ims.html ./readme.html ./RLS3/templates/ > /dev/null
		rsync -avzr --delete ./RLS3 $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		rm *.pyc

		its_rsync "RLS3"
	fi
}


function optex_SPEED {
	#### optex_SPEED
	if [ -d "$HOME/$homeName/its_optex/optex_SPEED" ]; then
		cd $HOME/$homeName/its_optex/optex_SPEED
		rm *.pyc
		python2 -m compileall config_db.py module_for_optex.py optex_SPEED.py config_sensor.py module_for_mysql.py module_for_sendmail.py run_optex.py # >/dev/null 2>&1
		mkdir -p ./optex_SPEED 2>/dev/null
		cp readme.txt config_db.pyc module_for_optex.pyc optex_SPEED.pyc config_sensor.pyc module_for_mysql.pyc module_for_sendmail.pyc run_optex.pyc ./optex_SPEED/ > /dev/null

		rsync -avzr --delete --exclude='node_modules' ./optex_SPEED $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "optex_SPEED"
	fi
}

function its_CAM {
	#### its_CAM
	if [ -d "$HOME/$homeName/its_CAM" ]; then
		cd $HOME/$homeName/its_CAM
		mkdir -p ./CAM
		mkdir -p ./CAM/model
		python2 -m compileall *.py model/*.py # >/dev/null 2>&1

		cp config.json module.pyc CAM.pyc run_CAM.pyc CAM.js CAM.html ./CAM/ > /dev/null
		cp model/*.pyc ./CAM/model/ > /dev/null
		rm *.pyc model/*.pyc

		rsync -avzr --delete --exclude='node_modules' ./CAM $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "CAM"
	fi
}

function its_MONITOR {
	##### MONITOR
	if [ -d "$HOME/$homeName/its_MONITOR" ]; then
		cd $HOME/$homeName/its_MONITOR
		rm *.pyc
		python2 -m compileall run_IMS.py # >/dev/null 2>&1
		mkdir -p ./MONITOR
		cp config.json camera.json language.json readme.txt ipCamInfo.js ipCamView.js ipCamView.html procOnvif.js its_M_map.js its_M_map_templet.html run_IMS.pyc ./MONITOR/ > /dev/null
		chmod 666 ./MONITOR/*.json

		# IMS 기능으로 Ubuntu Mate의 기본 사용자는 [ims]로 사용자 [ims]가 접근 가능 하도록 퍼미션을 변경 한다. 
		# chmod 707 -R ./MONITOR

		rsync -avzr --delete --exclude='node_modules' ./MONITOR $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		
		its_rsync "MONITOR"
	fi
}	

function its_utility {
	##### utility
	if [ -d "$HOME/$homeName/its_utility" ]; then
		cd $HOME/$homeName/its_utility
		python2 -m compileall download_ITS.py systemStatus.py ipSetup.py licenseKey.py licenseSrv.py productKey.py readPort.py readGPIO.py readGPIO_single.py portScan.py its_Scan.py check_RLS.py check_Relay.py streamClip.py check_GPACU.py # >/dev/null 2>&1

		python3.7 -m compileall -f -b productKey3.py licenseKey3.py
		
		mkdir -p ./utility
		cp download_ITS.pyc systemStatus.pyc ipSetup.pyc licenseKey.pyc licenseSrv.pyc productKey.pyc readPort.pyc readGPIO.pyc readGPIO_single.pyc portScan.pyc its_Scan.pyc check_RLS.pyc check_Relay.pyc streamClip.pyc check_GPACU.pyc ./utility/ > /dev/null

		cp productKey3.pyc licenseKey3.pyc ./utility/ > /dev/null
		
		cp setup_its.sh ./utility/ > /dev/null
		rm *.pyc
		
		rsync -avzr --delete --exclude='node_modules' ./utility $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "utility"
	fi
}	

function its_common {
	##### common
	if [ -d "$HOME/$homeName/its_common" ]; then
		cd $HOME/$homeName/its_common
		# python2 -m compileall m_authRequest.py m_findAngle.py # >/dev/null 2>&1
		python2 -m compileall audioOut.py audioOutVolume.py dbRepairOptimize.py scanSensor.py run_table.py msg_on_image.py resetIP.py resetSensor.py systemConfig.py watchdog.py userApi.py gikenEventServerTable_DB.py # >/dev/null 2>&1
		python3.7 -m compileall -f -b systemConfig3.py watchdog3.py userApi3.py

		mkdir -p ./common
		# cp m_authRequest.pyc m_findAngle.pyc ./common/ > /dev/null
		cp config.json language.json audioOut.pyc audioOutVolume.pyc dbRepairOptimize.pyc scanSensor.pyc run_table.pyc msg_on_image.pyc resetIP.pyc resetSensor.pyc systemConfig.pyc watchdog.pyc userApi.pyc gikenEventServerTable_DB.pyc table_union.js table_templet.html exportDB.sh ./common/ > /dev/null
		chmod 666 ./common/config.json
		cp systemConfig3.pyc watchdog3.pyc userApi3.pyc ./common/ > /dev/null
		rm *.pyc

		rsync -avzr --delete --exclude='node_modules' ./common $HOME/$ITS_PKG/code/ >/dev/null 2>&1

		its_rsync "common"
	fi
}

function WEB {
	cd $HOME/$homeName

	rsync -avzr --delete ./its_web/ $HOME/$ITS_PKG/web # >/dev/null 2>&1

	for i in "${ipListS[@]}"
	do
		echo -e "$BR Remote sync $BX pi@$i:its_web"
		sshpass -p $itsPass rsync -avzr -e ssh -p 22 --delete \
		--exclude='.*' \
		--exclude='data/session' \
		--exclude='data/log' \
		--exclude='data/file' \
		--exclude='data/image' \
		--exclude='data/config' \
		./its_web pi@$i:/var/www/html/ #  >/dev/null 2>&1
		TOUCH_WEB $i;
	done
}

PS3="Select : "
# select yn in "API" "API3" "GPIO" "GPACU" "GPWIO" "SRF" "FSI" "FRAME" "GIKENP" "GIKENT" "GIKENC" "TAILING" "BSS" "RLS_R" "RLS_V" "SPEED" "CAM" "MONITOR" "Utility" "Common" "WEB" 
select yn in "API" "API3" "GPIO" "GPACU" "GPWIO" "SRF" "FSI" "FRAME" "GIKENT" "GIKENC" "BSS" "RLS3" "RLS_R" "RLS_V" "CAM" "MONITOR" "Utility" "Common" "WEB" 
do
	echo ""
	echo -e "$C>>> $homeName ${ipListS[@]} <<<$X"
	echo ""
	case $yn in
		API ) its_API;;
		API3 ) its_API3;;
		GPIO ) its_GPIO;;
		GPACU ) its_GPACU;;
		GPWIO ) its_GPWIO;;
		SRF ) its_SRF;;
		FSI ) its_FSI;;
		FRAME ) its_FRAME;;
		GIKENP ) its_GIKENP;;
		GIKENT ) its_GIKENT;;
		GIKENC ) its_GIKENC;;
		TAILING ) its_TAILING;;
		BSS ) optex_BSS;;
		RLS3 ) its_RLS3;;
		RLS_R ) optex_RLS_R;;
		RLS_V ) optex_RLS_V;;
		SPEED ) optex_SPEED;;
		CAM ) its_CAM;;
		MONITOR ) its_MONITOR;;
		Utility ) its_utility;;
		Common ) its_common;;
		WEB) WEB;;
		*) exit;;
	esac

	echo -e "Backup code, db, modules"
	echo -e "\trsync --progress -avzr --delete --exclude='.*' $HOME/ pi@192.168.0.6:~"
	echo -e "\trsync --progress -avzr --delete --exclude='.*' $HOME/ pi@192.168.0.4:~/ecos"
	echo -e "\tssh pi@192.168.0.10 mysqldump -uits -pGXnLRNT9H50yKQ3G its_web > ~/Cherry/db/newest.sql"
	echo -e "\tssh pi@192.168.0.10 tar zcfP - .local > ~/Cherry/module/local.tgz"
	echo -e "\tssh pi@192.168.0.10 tar zcfP - GPIO/node_modules > ~/Cherry/module/node.tgz"
	echo -e '\tssh pi@192.168.0.70 "cd GPIO; tar zcfP - node_modules;" > ~/Cherry/module/node.tgz'
	cp $HOME/$homeName/renewalITS.sh $HOME/$ITS_PKG/
done	
	