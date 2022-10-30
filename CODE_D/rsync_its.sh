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

> $HOME/.ssh/known_hosts
# ssh-keyscan -H -T1 "git@github.com" 2>/dev/null > $HOME/.ssh/known_hosts
ipListS=()
if [ "$#" -lt 1 ]; then
	## Array variable
	curIP='192.168.0.10'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.20'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.30'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.40'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.50'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.60'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.70'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.80'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
	curIP='192.168.0.90'; ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass $curIP$X"; } || { echo -e "$Y---- Error $curIP$X"; }
else
	## IP Address
	## ex: ./rsync_its.sh 192.168.0.29
	curIP=("$1"); ssh-keyscan -H -T1 $curIP 2>/dev/null >> $HOME/.ssh/known_hosts && { ipListS+=("$curIP"); echo -e "$G>>>> Pass Connect to $curIP$X"; } || { echo -e "$Y---- Error Connect to $curIP$X"; }
fi

## ITS PI's Password
itsPass="its_iot"

## Home Dir
homeName=${PWD##*/}

## Package Name and Pass
# ITS_Key='Apple'
# ITS_Key='Banana'
# ITS_Key='Cherry'
ITS_Key='Dragon'

mkdir -p "$HOME/ecos"
# mkdir -p "$HOME/ecos/$ITS_Key"

ITS_Code="ecos/code/$homeName"
ITS_PKG="ecos/package/$ITS_Key"

mkdir -p "$HOME/$ITS_PKG"
mkdir -p "$HOME/$ITS_PKG/code"
mkdir -p "$HOME/$ITS_PKG/web"
mkdir -p "$HOME/$ITS_PKG/db"
mkdir -p "$HOME/$ITS_PKG/module"

cp renewalITS.sh readme.md  "$HOME/$ITS_PKG/"

echo ""
echo ">>> $homeName ${ipListS[@]} <<<"
echo -e ">>> Current Package Name is $Y$ITS_Key$X <<<"
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
	if [ -d "$HOME/$ITS_Code/its_GPIO" ]; then
		cd $HOME/$ITS_Code/its_GPIO
		mkdir -p ./GPIO
		cp readme.txt config.json table_GPIO.js table_templet.html ./GPIO/ > /dev/null
		python2 -m compileall config.py module.py GPIO.py run_GPIO.py
		mv config.pyc module.pyc GPIO.pyc run_GPIO.pyc ./GPIO/ > /dev/null

		rsync -avzr --delete ./GPIO $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "GPIO"
	fi
}

function its_API3 {
	#### its_API3
	if [ -d "$HOME/$ITS_Code/its_API3" ]; then
		cd $HOME/$ITS_Code/its_API3
		mkdir -p ./API3
		cp run config.json camera.json streaming.json itsEventProtocol.json itsAPI.js itsAPI.html itsAPI.php readme.pdf example.html ./API3/ > /dev/null
		python3.7 -m compileall -f -b itsAPI.py run_itsAPI.py run_streaming.py streaming.py
		mv itsAPI.pyc run_itsAPI.pyc run_streaming.pyc streaming.pyc ./API3/ > /dev/null

		rsync -avzr --delete ./API3 $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "API3"
	fi
}

function its_GPACU {
	#### its_GPACU
	if [ -d "$HOME/$ITS_Code/its_GPACU" ]; then
		cd $HOME/$ITS_Code/its_GPACU
		mkdir -p ./GPACU
		cp run config.json GPACU.js GPACU.html ./GPACU/ > /dev/null
		python2 -m compileall GPACU.py
		mv GPACU.pyc ./GPACU/ > /dev/null

		rsync -avzr --delete ./GPACU $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "GPACU"
	fi
}

function its_SRF {
	#### its_SPOTTER
	if [ -d "$HOME/$ITS_Code/its_partner/its_SRF" ]; then
		cd $HOME/$ITS_Code/its_partner/its_SRF
		mkdir -p ./SRF
		cp -r run config.json language.json spotter.js spotter_templet.html www ./SRF/ > /dev/null
		python2 -m compileall module.py spotter.py
		mv module.pyc spotter.pyc ./SRF/ > /dev/null

		rsync -avzr --delete ./SRF $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "SRF"
	fi
}

function its_FSI {
	#### its_FSI
	if [ -d "$HOME/$ITS_Code/its_partner/its_FSI" ]; then
		cd $HOME/$ITS_Code/its_partner/its_FSI
		mkdir -p ./FSI
		cp run config.json FSI.js FSI.html ./FSI/ > /dev/null
		python2 -m compileall FSI.py run_FSI.py FDX.py
		mv FSI.pyc run_FSI.pyc FDX.pyc ./FSI/ > /dev/null

		rsync -avzr --delete ./FSI $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "FSI"
	fi
}

function its_GIKENC {
	#### its_GIKENC
	if [ -d "$HOME/$ITS_Code/its_partner/its_GIKENC" ]; then
		cd $HOME/$ITS_Code/its_partner/its_GIKENC
		mkdir -p ./GIKENC
		cp run config.json GIKENC.js GIKENC.html ./GIKENC/ > /dev/null
		python2 -m compileall GIKENC.py run_GIKENC.py 
		mv run_GIKENC.pyc GIKENC.pyc ./GIKENC/ > /dev/null

		rsync -avzr --delete ./GIKENC $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "GIKENC"
	fi
}

function its_GIKENT {
	#### its_GIKENT
	if [ -d "$HOME/$ITS_Code/its_partner/its_GIKENT" ]; then
		cd $HOME/$ITS_Code/its_partner/its_GIKENT
		mkdir -p ./GIKENT
		cp run config.json rGIKENT.js GIKENT.html ./GIKENT/ > /dev/null
		python2 -m compileall GIKENT.py run_GIKENT.py 
		mv run_GIKENT.pyc GIKENT.pyc ./GIKENT/ > /dev/null

		rsync -avzr --delete ./GIKENT $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "GIKENT"
	fi
}

function optex_BSS {
	#### optex_BSS
	if [ -d "$HOME/$ITS_Code/its_optex/optex_BSS" ]; then
		cd $HOME/$ITS_Code/its_optex/optex_BSS
		mkdir -p ./optex_BSS
		cp readme.txt ./optex_BSS/ > /dev/null
		python2 -m compileall config.py module.py optex_BSS01.py run_optex.py
		mv config.pyc module.pyc optex_BSS01.pyc run_optex.pyc ./optex_BSS/ > /dev/null

		rsync -avzr --delete ./optex_BSS $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "optex_BSS"
	fi
}

function optex_RLS_R {
	##### optex_RLS_R
	if [ -d "$HOME/$ITS_Code/its_optex/optex_RLS_R" ]; then
		cd $HOME/$ITS_Code/its_optex/optex_RLS_R
		mkdir -p ./optex_RLS_R
		cp readme.txt realtime_RLS.js realtime_RLS_templet.html realtime_RLS_templet_IMS.html realtime_RLS_templet_Area.html ./optex_RLS_R/ > /dev/null
		python2 -m compileall config.py module.py optex_RLS_R.py optex_RLS_alarm.py run_optex.py
		mv config.pyc module.pyc optex_RLS_R.pyc optex_RLS_alarm.pyc run_optex.pyc ./optex_RLS_R/ > /dev/null

		rsync -avzr --delete ./optex_RLS_R $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "optex_RLS_R"
	fi
}

function its_RLS3 {
	##### its_RLS3
	if [ -d "$HOME/$ITS_Code/its_RLS3" ]; then
		cd $HOME/$ITS_Code/its_RLS3
		mkdir -p ./RLS3
		mkdir -p ./RLS3/static
		mkdir -p ./RLS3/templates
		cp config.json readme.md realtime_RLS.js realtime_RLS_templet.html ./RLS3/ > /dev/null
		cp ./templates/index.html ./templates/setup.html ./templates/ims.html ./readme.html ./RLS3/templates/ > /dev/null
		python3.7 -m compileall -f -b run_RLS3.py RLS3.py setup.py ims.py
		mv run_RLS3.pyc RLS3.pyc setup.pyc ims.pyc ./RLS3/ > /dev/null

		rsync -avzr --delete ./RLS3 $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "RLS3"
	fi
}


function optex_SPEED {
	#### optex_SPEED
	if [ -d "$HOME/$ITS_Code/its_optex/optex_SPEED" ]; then
		cd $HOME/$ITS_Code/its_optex/optex_SPEED
		mkdir -p ./optex_SPEED 2>/dev/null
		cp readme.txt ./optex_SPEED/ > /dev/null
		python2 -m compileall config_db.py module_for_optex.py optex_SPEED.py config_sensor.py module_for_mysql.py module_for_sendmail.py run_optex.py
		mv config_db.pyc module_for_optex.pyc optex_SPEED.pyc config_sensor.pyc module_for_mysql.pyc module_for_sendmail.pyc run_optex.pyc ./optex_SPEED/ > /dev/null

		rsync -avzr --delete ./optex_SPEED $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "optex_SPEED"
	fi
}

function its_CAM {
	#### its_CAM
	if [ -d "$HOME/$ITS_Code/its_CAM" ]; then
		cd $HOME/$ITS_Code/its_CAM
		mkdir -p ./CAM
		mkdir -p ./CAM/model
		cp config.json CAM.js CAM.html ./CAM/ > /dev/null
		python2 -m compileall *.py model/*.py
		mv module.pyc CAM.pyc run_CAM.pyc ./CAM/ > /dev/null
		mv model/*.pyc ./CAM/model/ > /dev/null

		rsync -avzr --delete ./CAM $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "CAM"
	fi
}

function its_MONITOR {
	##### MONITOR
	if [ -d "$HOME/$ITS_Code/its_MONITOR" ]; then
		cd $HOME/$ITS_Code/its_MONITOR
		mkdir -p ./MONITOR
		cp config.json camera.json language.json readme.txt ipCamInfo.js ipCamView.js ipCamView.html procOnvif.js its_M_map.js its_M_map_templet.html ./MONITOR/ > /dev/null
		chmod 666 ./MONITOR/*.json
		python2 -m compileall run_IMS.py
		mv run_IMS.pyc ./MONITOR/ > /dev/null

		rsync -avzr --delete ./MONITOR $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "MONITOR"
	fi
}	

function its_utility {
	##### utility
	if [ -d "$HOME/$ITS_Code/its_utility" ]; then
		cd $HOME/$ITS_Code/its_utility
		mkdir -p ./utility
		cp setup_its.sh ./utility/ > /dev/null
		python2 -m compileall download_ITS.py systemStatus.py ipSetup.py licenseKey.py licenseSrv.py productKey.py readPort.py readGPIO.py readGPIO_single.py portScan.py its_Scan.py check_RLS.py check_Relay.py streamClip.py check_GPACU.py
		mv download_ITS.pyc systemStatus.pyc ipSetup.pyc licenseKey.pyc licenseSrv.pyc productKey.pyc readPort.pyc readGPIO.pyc readGPIO_single.pyc portScan.pyc its_Scan.pyc check_RLS.pyc check_Relay.pyc streamClip.pyc check_GPACU.pyc ./utility/ > /dev/null
		python3.7 -m compileall -f -b productKey3.py licenseKey3.py
		mv productKey3.pyc licenseKey3.pyc ./utility/ > /dev/null
		
		rsync -avzr --delete ./utility $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "utility"
	fi
}	

function its_common {
	##### common
	if [ -d "$HOME/$ITS_Code/its_common" ]; then
		cd $HOME/$ITS_Code/its_common
		mkdir -p ./common
		cp config.json language.json table_union.js table_templet.html exportDB.sh ./common/ > /dev/null
		chmod 666 ./common/config.json
		python2 -m compileall audioOut.py audioOutVolume.py dbRepairOptimize.py scanSensor.py run_table.py msg_on_image.py resetIP.py resetSensor.py systemConfig.py watchdog.py userApi.py gikenEventServerTable_DB.py
		mv audioOut.pyc audioOutVolume.pyc dbRepairOptimize.pyc scanSensor.pyc run_table.pyc msg_on_image.pyc resetIP.pyc resetSensor.pyc systemConfig.pyc watchdog.pyc userApi.pyc gikenEventServerTable_DB.pyc ./common/ > /dev/null
		python3.7 -m compileall -f -b systemConfig3.py watchdog3.py userApi3.py
		mv systemConfig3.pyc watchdog3.pyc userApi3.pyc ./common/ > /dev/null

		rsync -avzr --delete ./common $HOME/$ITS_PKG/code/ >/dev/null 2>&1
		its_rsync "common"
	fi
}

function WEB {
	if [ -d "$HOME/$ITS_Code/its_web" ]; then
		cd $HOME/$ITS_Code

		rsync -avzr --delete ./its_web/ $HOME/$ITS_PKG/web

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
	fi


}

PS3="Select : "
select yn in "API3" "GPIO" "GPACU" "SRF" "FSI" "GIKENT" "GIKENC" "BSS" "RLS3" "RLS_R" "CAM" "MONITOR" "Utility" "Common" "WEB" 
do
	echo ""
	echo -e "$C>>> $homeName ${ipListS[@]} <<<$X"
	echo ""
	case $yn in
		API3 ) its_API3;;
		GPIO ) its_GPIO;;
		GPACU ) its_GPACU;;
		SRF ) its_SRF;;
		FSI ) its_FSI;;
		GIKENT ) its_GIKENT;;
		GIKENC ) its_GIKENC;;
		BSS ) optex_BSS;;
		RLS3 ) its_RLS3;;
		RLS_R ) optex_RLS_R;;
		CAM ) its_CAM;;
		MONITOR ) its_MONITOR;;
		Utility ) its_utility;;
		Common ) its_common;;
		WEB) WEB;;
		*) exit;;
	esac

	# echo -e "Backup code, db, modules"
	# echo -e "\trsync --progress -avzr --delete --exclude='.*' $HOME/ pi@192.168.0.6:~"
	# echo -e "\trsync --progress -avzr --delete --exclude='.*' $HOME/ pi@192.168.0.4:~/ecos"
	# echo -e "\tssh pi@192.168.0.10 mysqldump -uits -pGXnLRNT9H50yKQ3G its_web > ~/$ITS_PKG/db/newest.sql"
	# echo -e "\tssh pi@192.168.0.10 tar zcfP - .local > ~/$ITS_PKG/module/local.tgz"
	# echo -e "\tssh pi@192.168.0.10 tar zcfP - GPIO/node_modules > ~/$ITS_PKG/module/node.tgz"
	# echo -e '\tssh pi@192.168.0.70 "cd GPIO; tar zcfP - node_modules;" > ~/$ITS_PKG/module/node.tgz'
done	
	