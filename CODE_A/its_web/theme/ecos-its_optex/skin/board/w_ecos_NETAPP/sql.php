<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_netapp_serial' ";
// echo $sql."\n";
// exit();
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_device_id` varchar(64) DEFAULT NULL,
ADD `w_map_id` varchar(64) DEFAULT NULL,
ADD `w_netapp_serial` varchar(32) DEFAULT NULL,
ADD `w_netapp_model` varchar(32) DEFAULT NULL,
ADD `w_netapp_desc` varchar(256) DEFAULT NULL,
ADD `w_opt_char_01` varchar(32) DEFAULT NULL,
ADD `w_opt_char_02` varchar(32) DEFAULT NULL,
ADD `w_opt_tiny_01` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_netapp_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_netapp_reload` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_netapp_addr` varchar(32) DEFAULT NULL,
ADD `w_netapp_port` int(11) NOT NULL DEFAULT '0',
ADD `w_opt_int_01` int(11) NOT NULL DEFAULT '0',
ADD `w_opt_int_02` int(11) NOT NULL DEFAULT '0',
ADD `w_port_01` int(11) NOT NULL DEFAULT '0',
ADD `w_port_02` int(11) NOT NULL DEFAULT '0',
ADD `w_port_03` int(11) NOT NULL DEFAULT '0',
ADD `w_port_04` int(11) NOT NULL DEFAULT '0',
ADD `w_url_01` varchar(128) DEFAULT NULL,
ADD `w_url_02` varchar(128) DEFAULT NULL,
ADD `w_url_03` varchar(128) DEFAULT NULL,
ADD `w_url_04` varchar(128) DEFAULT NULL,
ADD `w_link_01` varchar(64) DEFAULT NULL,
ADD `w_link_02` varchar(64) DEFAULT NULL,
ADD `w_link_03` varchar(64) DEFAULT NULL,
ADD `w_link_04` varchar(64) DEFAULT NULL,
ADD `w_sns_id` varchar(64) DEFAULT NULL,
ADD `w_box_id` varchar(64) DEFAULT NULL,
ADD `w_keycode` varchar(64) DEFAULT NULL,
ADD `w_license` varchar(64) DEFAULT NULL,
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);
}

// ALTER TABLE `g5_write_g500t100` ADD `w_opt_int_01` int(11) NOT NULL DEFAULT '0' AFTER `w_netapp_port`;
// ALTER TABLE `g5_write_g500t100` ADD `w_opt_int_02` int(11) NOT NULL DEFAULT '0' AFTER `w_opt_int_01`;
// ALTER TABLE `g5_write_g500t100` ADD `w_sns_id` varchar(64) DEFAULT NULL AFTER `w_link_03`;
// ALTER TABLE `g5_write_g500t100` ADD `w_box_id` varchar(64) DEFAULT NULL AFTER `w_link_03`;

?>
