#!/bin/bash

K='\e[30m'; # : 글자색:검정
R='\e[31m'; # : 글자색:빨강
G='\e[32m'; # : 글자색:초록
Y='\e[33m'; # : 글자색:노랑
B='\e[34m'; # : 글자색:파랑
M='\e[35m'; # : 글자색:마젠트(분홍)
C='\e[36m'; # : 글자색:시안(청록)
W='\e[37m'; # : 글자색:백색
X='\e[39m'; # : 글자색으로 기본값으로

BK='\e[40m'; # : 바탕색:흑색
BR='\e[41m'; # : 바탕색:적색
BG='\e[42m'; # : 바탕색:녹색
BY='\e[43m'; # : 바탕색:황색
BB='\e[44m'; # : 바탕색:청색
BM='\e[45m'; # : 바탕색:분홍색
BC='\e[46m'; # : 바탕색:청록색
BW='\e[47m'; # : 바탕색:흰색
BX='\e[49m'; # : 바탕색을 기본값으로

itsSrvRemote=`grep -Po '"server_addr": *\K"[^"]*"' /home/pi/common/config.json | tr -d '"'`;

echo -e "$G >>> Adding the fingerprint $X";
echo -e " Current Server is $itsSrvRemote : ";
read -p " Type New IP or Enter to Continue : " userInput;
echo    # (optional) move to a new line
if [ -z "$userInput" ];
then
	itsSrvRemote=$itsSrvRemote;
else
	itsSrvRemote=$userInput
fi

PS3="Select : "
# downloadFolder="ECOS_PKG_01"; # Dragon(Next)
# downloadFolder="ITS_PKG"; # Cherry(Now)
# downloadFolder="Banana"; # Banana(21.05)
# downloadFolder="Apple"; # Apple(20.09)
select yn in "Apple[20.09]" "Banana[21.05]" "Cherry[22.01]" "Dragon[22.08]" 
do
	echo ""
	echo ">>> Selected $yn <<<"
	echo ""
	if [ $yn == 'Apple[20.09]' ]; then
		downloadFolder="Apple";
		break
	elif [ $yn == 'Banana[21.05]' ]; then
		downloadFolder="Banana";
		break
	elif [ $yn == 'Cherry[22.01]' ]; then
		downloadFolder="Cherry";
		break
	elif [ $yn == 'Dragon[22.08]' ]; then
		downloadFolder="Dragon";
		break
	else
		exit 1
	fi
done

echo -e "$BR >>> Adding the fingerprint $BX";
ssh-keyscan -H $itsSrvRemote >> /home/pi/.ssh/known_hosts;

while ! ping -c1 $itsSrvRemote &>/dev/null
do echo "$itsSrvRemote Ping Fail - `date`"
	exit 1
done
echo "$itsSrvRemote Found - `date`"

# -o ConnectTimeout=10
mkdir -p /home/pi/common;
sshpass -pits_iot scp pi@$itsSrvRemote:/home/pi/$downloadFolder/code/common/config.json /tmp;
if [ ! -f /tmp/config.json ]; then
	echo -e "$R <<< Download Folder($downloadFolder) Connection Error $X";
	exit
else
	rm /tmp/config.json;
fi

# echo -e "$R Be careful. $G It will be renewal all Database, Program and GUI. $X";
# read -p " Are you sure? " -n 1 -r;
# echo    # (optional) move to a new line
# if [[ ! $REPLY =~ ^[Yy]$ ]];
# then
# 	[[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1; # handle exits from shell or function but don't exit interactive shell
# fi

echo -e "$BG >>> Web Owner $BX";
sudo chown -R pi:pi /var/www/html;
mkdir -p /var/www/html/its_web;

echo -e "$BR >>> Download Code and Web $BX";
sshpass -pits_iot rsync --progress --delete -avzr -e ssh pi@$itsSrvRemote:/home/pi/$downloadFolder/code/* /home/pi/ 2> /dev/null;
sshpass -pits_iot rsync --progress --delete -avzr -e ssh pi@$itsSrvRemote:/home/pi/$downloadFolder/web/* /var/www/html/its_web/ 2> /dev/null;

echo -e "$BB >>> Data Folder and File Permission Change $BX"; 
chmod -R 777 /var/www/html/its_web/data;
chmod 777 /var/www/html/its_web/data/session;
chmod 777 /var/www/html/its_web/theme/ecos-its_optex/utility/filemanager;

echo -e "$BM >>> Config File Permission Change $BX"; 
find /home/pi/ /var/www/html/its_web/ -name config.json -exec chmod 777 {} \;
find /home/pi/ /var/www/html/its_web/ -name config.json -exec ls -al {} \;

echo -e "$C >>> Success, Web and Code Update and Reset File Permission. $X";
read -p " Do you want renewal Database? " -n 1 renewal;
echo    # (optional) move to a new line
if [[ $renewal =~ [Yy]$ ]];
then
	echo -e "$G >>> Database Download and Renewal. $X";
	# sshpass -pits_iot scp pi@$itsSrvRemote:/home/pi/$downloadFolder/db/newest.sql /tmp;
	sshpass -pits_iot scp pi@$itsSrvRemote:/home/pi/update/ECOS/newest.sql /tmp;
	echo -e "$Y >>> DROP DATABASE $X";
	mysql -uits -pGXnLRNT9H50yKQ3G -e "DROP DATABASE IF EXISTS its_web";
	echo -e "$Y >>> CREATE DATABASE $X";
	mysql -uits -pGXnLRNT9H50yKQ3G -e "CREATE DATABASE its_web";
	echo -e "$Y >>> UPLOAD DATABASE $X";
	mysql -uits -pGXnLRNT9H50yKQ3G its_web < /tmp/newest.sql;
	rm /tmp/newest.sql;
fi

echo -e "$BM >>> License Key Code Gen $BX";
python /home/pi/utility/licenseKey.pyc ECOS $itsSrvRemote;

echo -e "$C >>> Update Stamp $X";
unixtime=`date +%s`;
sshpass -pits_iot ssh pi@$itsSrvRemote mkdir -p /home/pi/.download_History;
sshpass -pits_iot scp /home/pi/.config/watchdog.json pi@$itsSrvRemote:/home/pi/.download_History/$unixtime;

if grep --quiet Raspberry /proc/cpuinfo; then
	echo -e "$M >>> Expand Root File System $X";
	sudo raspi-config --expand-rootfs > /dev/null;
fi

# echo -e "$BW$K/_/_/_/_/_/_/_/_/_/$X$BX";
# echo -e "$BW$K/_/ Reboot ITS  /_/$X$BX";
# echo -e "$BW$K/_/_/_/_/_/_/_/_/_/$X$BX";
echo -e "Reboot ITS $BM >>> Reboot ITS $BX";