<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_zone_serial' ";
// echo $sql."\n";
// exit();
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
	ADD `w_map_id` varchar(64) DEFAULT NULL,
	ADD `w_zone_serial` varchar(32) DEFAULT NULL,
	ADD `w_zone_model` varchar(32) DEFAULT NULL,
	ADD `w_zone_desc` varchar(256) DEFAULT NULL,
	ADD `w_zone_disable` tinyint(1) NOT NULL DEFAULT '0',
	ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',
	ADD `w_sns_0` varchar(64) DEFAULT NULL,
	ADD `w_sns_1` varchar(64) DEFAULT NULL,
	ADD `w_sns_2` varchar(64) DEFAULT NULL,
	ADD `w_sns_3` varchar(64) DEFAULT NULL,
	ADD `w_cam_0` varchar(64) DEFAULT NULL,
	ADD `w_cam_1` varchar(64) DEFAULT NULL,
	ADD `w_cam_2` varchar(64) DEFAULT NULL,
	ADD `w_cam_3` varchar(64) DEFAULT NULL,
	ADD `w_ptz_0` varchar(64) DEFAULT NULL,
	ADD `w_ptz_1` varchar(64) DEFAULT NULL,
	ADD `w_ptz_2` varchar(64) DEFAULT NULL,
	ADD `w_ptz_3` varchar(64) DEFAULT NULL,
	ADD `w_ptzOn_0` tinyint(1) NOT NULL DEFAULT '0',
	ADD `w_ptzOn_1` tinyint(1) NOT NULL DEFAULT '0',
	ADD `w_ptzOn_2` tinyint(1) NOT NULL DEFAULT '0',
	ADD `w_ptzOn_3` tinyint(1) NOT NULL DEFAULT '0',
	ADD `w_box_id` varchar(64) DEFAULT NULL,
	ADD `w_iFrame` varchar(256) DEFAULT NULL,
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

// ALTER TABLE `g5_write_g500t200` ADD `w_ptzOn_0` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_ptz_3`;
// ALTER TABLE `g5_write_g500t200` ADD `w_ptzOn_1` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_ptzOn_0`;
// ALTER TABLE `g5_write_g500t200` ADD `w_ptzOn_2` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_ptzOn_1`;
// ALTER TABLE `g5_write_g500t200` ADD `w_ptzOn_3` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_ptzOn_2`;
// ALTER TABLE `g5_write_g500t200` ADD `w_ptz_1` varchar(64) DEFAULT NULL AFTER `w_ptz_1`;
// ALTER TABLE `g5_write_g500t200` ADD `w_ptz_2` varchar(64) DEFAULT NULL AFTER `w_ptz_1`;
// ALTER TABLE `g5_write_g500t200` ADD `w_box_id` varchar(64) DEFAULT NULL AFTER `w_ptz_3`;
// ALTER TABLE `g5_write_g500t200` ADD `w_iFrame` varchar(128) DEFAULT NULL AFTER `w_box_id`;

?>
