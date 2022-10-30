<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_sensor_serial' ";
// echo $sql."\n";
// exit();
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_cpu_id` varchar(32) DEFAULT NULL,
ADD `w_device_id` varchar(32) DEFAULT NULL,
ADD `w_sensor_serial` varchar(32) DEFAULT NULL,
ADD `w_gpcio_desc` varchar(128) DEFAULT NULL,
ADD `w_gpcio_direction` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_gpcio_detect_L` int(11) NOT NULL DEFAULT '0',
ADD `w_gpcio_detect_R` int(11) NOT NULL DEFAULT '0',
ADD `w_gpcio_trigger_L` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_gpcio_trigger_R` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_gpcio_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_security_mode` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_distance` int(11) NOT NULL DEFAULT '0',
ADD `w_speed_L` float NOT NULL DEFAULT '0',
ADD `w_speed_H` float NOT NULL DEFAULT '0',

ADD `w_capacity_A` int(11) NOT NULL DEFAULT '0',
ADD `w_capacity_B` int(11) NOT NULL DEFAULT '0',
ADD `w_capacity_C` int(11) NOT NULL DEFAULT '0',
ADD `w_capacity_D` int(11) NOT NULL DEFAULT '0',

ADD `w_direction_AX` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_XA` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_BX` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_XB` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_CX` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_XC` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_DX` int(11) NOT NULL DEFAULT '0',
ADD `w_direction_XD` int(11) NOT NULL DEFAULT '0',

ADD `w_internal_AX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_XA` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_BX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_XB` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_CX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_XC` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_DX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_internal_XD` tinyint(1) NOT NULL DEFAULT '0',

ADD `w_external_AX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_XA` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_BX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_XB` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_CX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_XC` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_DX` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_external_XD` tinyint(1) NOT NULL DEFAULT '0',


ADD `w_alert_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_Value` float NOT NULL DEFAULT '0',
ADD `w_host_Addr1` varchar(32) DEFAULT NULL,
ADD `w_host_Port1` int(11) NOT NULL DEFAULT '0',
ADD `w_host_Addr2` varchar(32) DEFAULT NULL,
ADD `w_host_Port2` int(11) NOT NULL DEFAULT '0',
ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_keycode` varchar(64) DEFAULT NULL,
ADD `w_license` varchar(64) DEFAULT NULL,
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);
}

// $sql = "CREATE TABLE IF NOT EXISTS w_log_IMS_key (
// `w_id` int(11) NOT NULL AUTO_INCREMENT,
// `w_sensorId` varchar(64) NULL DEFAULT '',
// PRIMARY KEY (`w_id`), 
// UNIQUE (`w_sensorId`)
// ) ENGINE=InnoDB  DEFAULT CHARSET=utf8";
// sql_query($sql, false);

// ALTER TABLE `g5_write_g500t200` ADD `w_cam_0` varchar(64) DEFAULT NULL AFTER `w_sns_3`;
// ALTER TABLE `g5_write_g500t200` ADD `w_cam_1` varchar(64) DEFAULT NULL AFTER `w_cam_0`;
// ALTER TABLE `g5_write_g500t200` ADD `w_cam_2` varchar(64) DEFAULT NULL AFTER `w_cam_1`;
// ALTER TABLE `g5_write_g500t200` ADD `w_cam_3` varchar(64) DEFAULT NULL AFTER `w_cam_2`;

?>
