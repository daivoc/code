<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_gpwio_serial' ";
// echo $sql."\n";
// exit();
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_gpwio_serial` varchar(32) DEFAULT NULL,
ADD `w_gpwio_desc` varchar(128) DEFAULT NULL,
ADD `w_gpwio_status` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_gpwio_cover` varchar(16) DEFAULT NULL,
ADD `w_gpwio_group` varchar(16) DEFAULT NULL,
ADD `w_gpwio_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_sensor_serial` varchar(32) DEFAULT NULL,
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
// ) ENGINE=MyISAM  DEFAULT CHARSET=utf8";
// sql_query($sql, false);

// ALTER TABLE `g5_write_g500t200` ADD `w_cam_0` varchar(64) DEFAULT NULL AFTER `w_sns_3`;
// ALTER TABLE `g5_write_g500t200` ADD `w_cam_1` varchar(64) DEFAULT NULL AFTER `w_cam_0`;
// ALTER TABLE `g5_write_g500t200` ADD `w_cam_2` varchar(64) DEFAULT NULL AFTER `w_cam_1`;
// ALTER TABLE `g5_write_g500t200` ADD `w_cam_3` varchar(64) DEFAULT NULL AFTER `w_cam_2`;

?>
