
########################
# 시스템 코맨드 모음
########################

# Remote Command Example

	$ ssh pi@192.168.0.202 << EOF
		echo '>>>> rc.local >>>>'
		grep ^su /etc/rc.local
		echo
		echo '>>>> ps -rf >>>>'
		ps -ef | egrep 'node|python'
	EOF

	$ ssh pi@192.168.0.202 'bash -s' < script.sh


########################
# ITS 프로그램 배포 순서
########################

# Using TAR Command

	# 호스트 업데이트 생성 
		cd PI Home
		tar -zcvf its.tar *
		rcp ./its.tar pi@192.168.0.5:update/

		cd /var/www/html/its_web
		tar -zcvf web.tar *
		rcp ./web.tar pi@192.168.0.5:update/

	# 리모트 다운로드 업데이트
		rcp pi@115.139.183.226:./update/*.tar ~
		
		mv web.tar /var/www/html/its_web
		cd /var/www/html/its_web
		tar -zxvf web.tar
		chmod -R 777 /var/www/html/its_web/data
		chmod -R 777 /var/www/html/its_web/theme/ecos-its_optex/utility/filemanager
		
		cd ~
		tar -zxvf its.tar
		
		
########################
# Using Rsync Command
########################

	# Rsync ITS
		
		# its program copy
		rsync -avzr --delete /home/pi/ pi@192.168.0.101:/home/pi
		
		# its web copy
		rsync -avzr --delete --exclude='data' /var/www/html/its_web/ pi@192.168.0.101:/var/www/html/its_web

		# sshpass 사용 its_web copy
		sshpass -p $rPassword rsync -avzr -e "ssh -p ${ADDR[1]}" --delete --exclude='data' /var/www/html/its_web/ pi@${ADDR[0]}:/var/www/html/its_web #  >/dev/null 2>&1


	# 웹 데이터 폴더 Permission

		chmod -R 777 /var/www/html/its_web/data
		chmod -R 777 /var/www/html/its_web/theme/ecos-its_optex/utility/filemanager

		
	# Copy ITS to USB 

		# USB driver 확인
		sudo fdisk -l | grep sda ## 가변적임 sdc - ubuntu
		
		# USB를 Mount 할 폴더 생성
		sudo mkdir /media/usb
		sudo chown -R pi:pi /media/usb
		
		# Mount and Permission
		sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi
		
		# its program copy to USB
		rsync -avzr --delete /home/pi /media/usb # Programs
		rsync -avzr --delete --exclude='data' /var/www/html/its_web /media/usb # Programs

		# its source code copy to USB
		rsync -avzr --delete pi@192.168.0.5:/home/pi/ecos_its-OPTEX /media/usb # Programs
		
		# other example
		rsync -avzr --delete /home/pi pi@192.168.0.101:/media/usb # Programs
		rsync -avzr --delete /var/www/html/its_web pi@192.168.0.101:/media/usb # WEB

		# USB를 Un-Mount 할 폴더 생성
		sudo umount /media/usb
		

	# Copy USB to ITS 

		# USB를 Mount 할 폴더 생성
		sudo mkdir /media/usb
		sudo chown -R pi:pi /media/usb
		
		# Mount and Permission
		sudo mount /dev/sda1 /media/usb -o uid=pi,gid=pi

		# local copy USB to ITS
		sudo rsync -avzr --delete /media/usb/pi/* /home/pi # Programs
		sudo rsync -avzr --delete --exclude='data' /media/usb/its_web/* /var/www/html/its_web # Programs

		# remote copy USB to ITS
		sudo rsync -avzr --delete /media/usb/pi/* pi@192.168.0.101:/home/pi # Programs
		sudo rsync -avzr --delete --exclude='data' /media/usb/its_web/* pi@192.168.0.101:/var/www/html/its_web # Programs

		# USB를 Un-Mount 할 폴더 생성
		sudo umount /media/usb


########################
# 데이터베이스 SQL - 업데이트
########################
	
	ALTER TABLE `g5_write_g500t100` ADD `w_sns_id` varchar(64) DEFAULT NULL AFTER `w_linked_3`;
	ALTER TABLE `g5_write_g500t100` ADD `w_box_id` varchar(64) DEFAULT NULL AFTER `w_sns_id`;
	
	ALTER TABLE `g5_write_g500t200` ADD `w_box_id` varchar(64) DEFAULT NULL AFTER `w_ptz_3`;

	# GPIO #
	ALTER TABLE `g5_write_g300t100` ADD `w_alert3_Port` int(11) NOT NULL DEFAULT '0' AFTER `w_alert2_Value`;
	ALTER TABLE `g5_write_g300t100` ADD `w_alert3_Value` float NOT NULL DEFAULT '0' AFTER `w_alert3_Port`;
	ALTER TABLE `g5_write_g300t100` ADD `w_alert4_Port` int(11) NOT NULL DEFAULT '0' AFTER `w_alert3_Value`;
	ALTER TABLE `g5_write_g300t100` ADD `w_alert4_Value` float NOT NULL DEFAULT '0' AFTER `w_alert4_Port`;

########################
# /etc/sudoers
########################

	www-data ALL=(root) NOPASSWD: /sbin/reboot
	www-data ALL=(root) NOPASSWD: /sbin/poweroff
	www-data ALL=(root) NOPASSWD: /bin/date


########################
# 키보드 레이아웃
########################

	/etc/defaults/keyboard
	Make it
	XKBLAYOUT="us"
	
# GPIO TCP Data Sencer Example Value for
Custom	
	Format: USER||PASS||IP||Port||Opt1||Opt2
	Custom1	||||192.168.0.81||2154||1|| # -> Divisys NVR Popup
	Custom2	||||192.168.0.202||2154||1||
	