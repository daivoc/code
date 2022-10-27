#!/bin/bash

R='\e[31m'; # : 글자색:빨강
X='\e[39m'; # : 글자색으로 기본값으로
BR='\e[41m'; # : 바탕색:적색
BX='\e[49m'; # : 바탕색을 기본값으로

myIP=`ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'`

read -p "Type Client IP : " userInput;
echo    # (optional) move to a new line
if [ -z "$userInput" ];
then
        exit
else
        itsSrvRemote=$userInput
fi

while ! ping -c1 -W1 $itsSrvRemote &>/dev/null
do echo "$itsSrvRemote Ping Fail - `date`"
	exit 1
done
echo "IP: $itsSrvRemote Found - `date`"

echo -e "$BR >>> Adding the fingerprint $BX";
ssh-keyscan -H $itsSrvRemote >> /home/pi/.ssh/known_hosts;

sshpass -pits_iot scp pi@$itsSrvRemote:/home/pi/.download_History/* /home/pi/.download_History/ 2> /dev/null;
sshpass -pits_iot scp pi@$itsSrvRemote:/home/pi/download_History/* /home/pi/.download_History/ 2> /dev/null;
# sshpass -pits_iot rsync --progress --delete -avzr -e ssh /home/pi/ecos_ITS_Download pi@192.168.0.110:/home/pi/;
sshpass -pits_iot rsync --progress --delete --exclude='.git' -avzr -e ssh /home/pi/ecos_ITS_Download pi@$itsSrvRemote:/home/pi/;

echo -e "Complet Program Server -$R $itsSrvRemote $X";
