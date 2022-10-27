#!/bin/bash

myIP=`hostname -I | cut -d' ' -f1`
today=`date '+%Y-%m-%d'`
itsName=$today"_"$myIP"_its.tar"
webName=$today"_"$myIP"_web.tar"
dbName="/tmp/"$today"_"$myIP"_db.sql"

rHost="pi@192.168.0.5:update/ECOS/"
# rPath="pi@192.168.0.5:/home/pi/ITS/db/"
newest=$rHost"newest.sql"

## 디비 백업
echo "Download"
mysqldump -uits -pGXnLRNT9H50yKQ3G its_web > $dbName
echo "Upload rHost"
sshpass -p its_iot rcp $dbName $rHost
# echo "Upload rPath"
# sshpass -p its_iot rcp $dbName $rPath
echo "Upload newest"
sshpass -p its_iot rcp $dbName $newest
echo "Done"
rm -rf $dbName
