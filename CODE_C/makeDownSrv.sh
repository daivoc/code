#!/bin/bash

# 현장 작업을 위한 이동식 ITS Code Update 서버제작 프로그램

R='\e[31m'; # : 글자색:빨강
X='\e[39m'; # : 글자색으로 기본값으로

read -p "Type Download Server IP : " target_IP;
while ! ping -c1 -W1 $target_IP &>/dev/null
do echo "$target_IP Ping Fail - `date`."
	exit
done

read -p "Type ITS Version : " version_Name;
if [ -d "$HOME/$version_Name" ]; then
        echo
else
	echo "Check Version First."
        exit
fi

echo "IP: $target_IP, Version: $version_Name"

# sshpass -pits_iot rsync --progress --delete -avzr -e ssh /home/pi/$version_Name pi@$target_IP:/home/pi/;
# sshpass -pits_iot rsync --progress --delete --exclude='.*' -avzr -e ssh /home/pi/$version_Name pi@$target_IP:/home/pi/;
rsync --progress --delete --exclude='.*' -avzr -e ssh $HOME/$version_Name pi@$target_IP:/home/pi/

echo -e "Complet Program Server -$R $target_IP $X"