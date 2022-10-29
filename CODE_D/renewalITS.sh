#!/bin/bash
# 각각의 아이티에스 업데이트하는 기능

BK='\e[40m'; # : 바탕색:흑색
BR='\e[41m'; # : 바탕색:적색
BG='\e[42m'; # : 바탕색:녹색
BY='\e[43m'; # : 바탕색:황색
BB='\e[44m'; # : 바탕색:청색
BM='\e[45m'; # : 바탕색:분홍색
BC='\e[46m'; # : 바탕색:청록색
BW='\e[47m'; # : 바탕색:흰색
BX='\e[49m'; # : 바탕색을 기본값으로

# echo "All args: $*"
# echo "All args count: $#"

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 target_ip_address"
    exit 0
fi

export IFS=" "
export args=$*

function yes_or_no {
    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0 ;;  
            [Nn]*) return 1 ;;
        esac
    done
}

# 요청한 IP의 ssh 키를 모두 생성 한다
> /home/pi/.ssh/known_hosts
for itsIP in $args; do
    # 키생성이 정싱적이면 호스트목록에 등록 하고 오류가 생기면 종료한다.
    ssh-keyscan -H -T1 $itsIP 2>1 >> /home/pi/.ssh/known_hosts && echo ">>>> Pass Connect to $itsIP" || { echo "---- Error Connect to $itsIP"; exit 2; }
done

yes_or_no " Do you want renewal of ITS GUI? " && GUI="Y"
yes_or_no " Do you want renewal of ITS Code? " && Code="Y"
yes_or_no " Do you want upgrade of Python3 Modules? " && ModsPY="Y"
yes_or_no " Do you want upgrade of NodeJs Modules? " && ModsNode="Y"
yes_or_no " Do you want renewal of Database? " && Database="Y"
# yes_or_no " Do you want renewal of License? " && License="Y"
# yes_or_no " Do you want expand of SD Card? " && Expand="Y"
# yes_or_no " Do you want reboot remote ITS? " && Reboot="Y"

# echo "$GUI, $Code, $Modules, $Database, $License, $Expand, $Reboot,"

if [[ $GUI =~ [Yy]$ ]]; then
    for itsIP in $args; do
        echo -e "$BR>>> Upload Web $BX";
        sshpass -pits_iot rsync --progress --delete -avzr -e ssh ./web/* pi@$itsIP:/var/www/html/its_web/ 2> /dev/null;
        echo -e "$BR>>> Mode Change (data) $BX";
        sshpass -pits_iot ssh pi@$itsIP "chmod -R 777 /var/www/html/its_web/data;";
        echo -e "$BR>>> Mode Change (filemanager) $BX";
        sshpass -pits_iot ssh pi@$itsIP "chmod 777 /var/www/html/its_web/theme/ecos-its_optex/utility/filemanager;";
        echo -e "$BR>>> Mode Change (config.json) $BX";
        sshpass -pits_iot ssh pi@$itsIP "find /var/www/html/its_web/ -name config.json -exec chmod 777 {} \;";
        sshpass -pits_iot ssh pi@$itsIP "find /var/www/html/its_web/ -name config.json -exec ls -al {} \;";
        echo
        echo -e "$BC>>> Done Web - $itsIP$BX";
        echo
    done
fi

if [[ $Code =~ [Yy]$ ]]; then
    for itsIP in $args; do
        echo -e "$BB>>> Upload Code $BX";
        sshpass -pits_iot rsync --progress --delete -avzr -e ssh ./code/* pi@$itsIP:/home/pi/ 2> /dev/null;
        echo -e "$BB>>> Mode Change (config.json) $BX";
        sshpass -pits_iot ssh pi@$itsIP "find /home/pi/ -name config.json -exec chmod 777 {} \;";
        sshpass -pits_iot ssh pi@$itsIP "find /home/pi/ -name config.json -exec ls -al {} \;";
        echo
        echo -e "$BC>>> Done Code - $itsIP$BX";
        echo
    done
fi

if [[ $ModsPY =~ [Yy]$ ]]; then
    for itsIP in $args; do
        echo -e "$BG>>> Upload Python3 Modules $BX";
        sshpass -pits_iot scp ./module/local.tgz pi@$itsIP:~;
        echo -e "$BG>>> Decompress (local.tgz) $BX";
        sshpass -pits_iot ssh pi@$itsIP "tar zxvf local.tgz; rm local.tgz;";
        echo
        echo -e "$BC>>> Done Python3 Modules - $itsIP$BX";
        echo
    done
fi

if [[ $ModsNode =~ [Yy]$ ]]; then
    for itsIP in $args; do
        echo -e "$BY>>> Upload NodeJs Modules $BX";
        sshpass -pits_iot scp ./module/node.tgz pi@$itsIP:~;
        echo -e "$BY>>> Decompress (node.tgz) $BX";
        sshpass -pits_iot ssh pi@$itsIP "tar zxvf node.tgz; rm node.tgz;";
        sshpass -pits_iot ssh pi@$itsIP "find . -maxdepth 1 -type d \( ! -name . \) -exec bash -c 'cd {}; test -e node_modules && rm -rf node_modules && ln -sf ../node_modules .;' \;";
        echo
        echo -e "$BC>>> Done NodeJs Modules - $itsIP$BX";
        echo
    done
fi

if [[ $Database =~ [Yy]$ ]]; then
    for itsIP in $args; do
        echo -e "$BB>>> Upload DB Templet $BX";
        sshpass -pits_iot scp ./db/newest.sql pi@$itsIP:/tmp;
        echo -e "$BB>>> Drop DATABASE $BX";
        sshpass -pits_iot ssh pi@$itsIP "mysql -uits -pGXnLRNT9H50yKQ3G -e 'DROP DATABASE IF EXISTS its_web';";
        echo -e "$BB>>> Create DATABASE $BX";
        sshpass -pits_iot ssh pi@$itsIP "mysql -uits -pGXnLRNT9H50yKQ3G -e 'CREATE DATABASE its_web';";
        echo -e "$BB>>> Import DATABASE $BX";
        sshpass -pits_iot ssh pi@$itsIP "mysql -uits -pGXnLRNT9H50yKQ3G its_web < /tmp/newest.sql;";
        sshpass -pits_iot ssh pi@$itsIP "rm /tmp/newest.sql;";
        echo
        echo -e "$BC>>> Done Database Update - $itsIP$BX";
        echo
    done
fi

exit 0

# # read -p " Do you want renewal License? " -n 1 License;
# # echo    # (optional) move to a new line
# if [[ $License =~ [Yy]$ ]]; then
#     echo -e "$BM >>> License Key Code Gen $BX";
#     python /home/pi/utility/licenseKey.pyc ECOS $itsIP;
# fi


# # read -p " Do you want disk Expand? " -n 1 Expand;
# # echo    # (optional) move to a new line
# if [[ $Expand =~ [Yy]$ ]]; then
#     if grep --quiet Raspberry /proc/cpuinfo; 
#     then
#         echo -e "$M >>> Expand Root File System $X";
#         sudo raspi-config --expand-rootfs > /dev/null;
#     fi
# fi

# # read -p " Do you want remote ITS Reboot? " -n 1 Reboot;
# # echo    # (optional) move to a new line
# if [[ $Reboot =~ [Yy]$ ]]; then
#     echo -e "$BW$K/_/_/_/_/_/_/_/_/_/$X$BX";
#     echo -e "$BW$K/_/ Reboot ITS  /_/$X$BX";
#     echo -e "$BW$K/_/_/_/_/_/_/_/_/_/$X$BX";
# fi
