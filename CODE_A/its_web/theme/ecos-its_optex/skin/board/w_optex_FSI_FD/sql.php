<?php
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_id' ";
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_id` varchar(32) DEFAULT NULL,
ADD `w_parent_id` int(11) NOT NULL DEFAULT '0',
ADD `w_zone_id` int(11) NOT NULL DEFAULT '0',
ADD `w_zone_name` varchar(32) DEFAULT NULL,
ADD `w_system_ip` varchar(16) DEFAULT NULL,

ADD `w_device_name` varchar(32) DEFAULT NULL,
ADD `w_device_serial` varchar(32) DEFAULT NULL,

ADD `w_sensor_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_sensor_stop` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_sensor_reload` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_event_keepHole` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',

ADD `w_ims_address_P` varchar(32) DEFAULT NULL,
ADD `w_ims_port_P` int(11) NOT NULL DEFAULT '0',
ADD `w_ims_address_S` varchar(32) DEFAULT NULL,
ADD `w_ims_port_S` int(11) NOT NULL DEFAULT '0',
ADD `w_snapshot_url` varchar(128) DEFAULT NULL,
ADD `w_snapshot_qty` int(11) NOT NULL DEFAULT '0',
ADD `w_snapshot_enc` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_streaming_url` varchar(128) DEFAULT NULL,
ADD `w_streaming_enc` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_alert_port` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_value` float NOT NULL DEFAULT '0',
ADD `w_license` varchar(64) DEFAULT NULL,
ADD `w_keycode` varchar(64) DEFAULT NULL,
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);
}
?>
