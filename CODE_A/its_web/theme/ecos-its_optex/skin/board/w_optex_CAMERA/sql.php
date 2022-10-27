<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_camera_serial' ";
// echo $sql."\n";
// exit();
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_device_id` varchar(64) DEFAULT NULL,
ADD `w_map_id` varchar(64) DEFAULT NULL,
ADD `w_camera_serial` varchar(32) DEFAULT NULL,
ADD `w_camera_model` varchar(32) DEFAULT NULL,
ADD `w_camera_desc` varchar(256) DEFAULT NULL,
ADD `w_camera_user` varchar(32) DEFAULT NULL,
ADD `w_camera_pass` varchar(32) DEFAULT NULL,
ADD `w_camera_hash` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_camera_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_camera_reload` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_camera_addr` varchar(32) DEFAULT NULL,
ADD `w_camera_port` int(11) NOT NULL DEFAULT '0',
ADD `w_camera_px_X` int(11) NOT NULL DEFAULT '0',
ADD `w_camera_px_Y` int(11) NOT NULL DEFAULT '0',
ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_port_IO01` int(11) NOT NULL DEFAULT '0',
ADD `w_port_IO02` int(11) NOT NULL DEFAULT '0',
ADD `w_port_IO03` int(11) NOT NULL DEFAULT '0',
ADD `w_port_IO04` int(11) NOT NULL DEFAULT '0',
ADD `w_url1` varchar(128) DEFAULT NULL,
ADD `w_url2` varchar(128) DEFAULT NULL,
ADD `w_url3` varchar(128) DEFAULT NULL,
ADD `w_url4` varchar(128) DEFAULT NULL,
ADD `w_linked_0` varchar(64) DEFAULT NULL,
ADD `w_linked_1` varchar(64) DEFAULT NULL,
ADD `w_linked_2` varchar(64) DEFAULT NULL,
ADD `w_linked_3` varchar(64) DEFAULT NULL,
ADD `w_sns_id` varchar(64) DEFAULT NULL,
ADD `w_box_id` varchar(64) DEFAULT NULL,
ADD `w_keycode` varchar(64) DEFAULT NULL,
ADD `w_license` varchar(64) DEFAULT NULL,
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);
}

// ALTER TABLE `g5_write_g500t100` ADD `w_camera_px_X` int(11) NOT NULL DEFAULT '0' AFTER `w_camera_port`;
// ALTER TABLE `g5_write_g500t100` ADD `w_camera_px_Y` int(11) NOT NULL DEFAULT '0' AFTER `w_camera_px_X`;
// ALTER TABLE `g5_write_g500t100` ADD `w_sns_id` varchar(64) DEFAULT NULL AFTER `w_linked_3`;
// ALTER TABLE `g5_write_g500t100` ADD `w_box_id` varchar(64) DEFAULT NULL AFTER `w_linked_3`;

?>
