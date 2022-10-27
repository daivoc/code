#!/bin/bash
## https://stackoverflow.com/questions/9293042/how-to-perform-a-mysqldump-without-a-password-prompt

myIP=`hostname -I | cut -d' ' -f1`
today=`date '+%Y-%m-%d'`
itsName=$today"_"$myIP"_its.tar"
webName=$today"_"$myIP"_web.tar"
dbName="/tmp/"$today"_"$myIP"_db.sql"
dbSQL="pi@192.168.0.5:/home/pi/ITS/db/newest.sql"

rTarget="pi@192.168.0.5:update/ECOS/"


## 디비 백업
mysqldump -uits -pGXnLRNT9H50yKQ3G its_web > $dbName

## 디비 -> 테이블 백업
# mysql -uits -pGXnLRNT9H50yKQ3G its_web -B -e "select * from \`w_log_sensor_g200t100_192_168_0_202_0016\`;" | sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > /tmp/`hostname -I | cut -d' ' -f1`.csv


## 코드 백업
cd ~
echo $itsName
tar --exclude='.[^/]*' -zcvf $itsName .

## 웹 백업
cd /var/www/html/its_web
echo $webName
# tar --exclude='.[^/]*' --exclude='./data' -zcvf ~/$webName .
tar --exclude='.[^/]*' -zcvf ~/$webName .

cd ~

# rcp $itsName $rTarget
# rcp $webName $rTarget
# rcp $itsName $webName $rTarget

ls -sh $dbName
sshpass -p its_iot rcp $dbName $rTarget
sshpass -p its_iot rcp $dbName $dbSQL

ls -sh $itsName
sshpass -p its_iot rcp $itsName $rTarget

ls -sh $webName
sshpass -p its_iot rcp $webName $rTarget

rm -rf $dbName $itsName $webName

# GXnLRNT9H50yKQ3G