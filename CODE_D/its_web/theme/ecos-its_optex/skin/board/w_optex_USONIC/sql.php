<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_id' ";
// echo $sql."\n";
// exit();
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_id` varchar(32) DEFAULT NULL,
ADD `w_cpu_id` varchar(32) DEFAULT NULL,
ADD `w_license` varchar(64) DEFAULT NULL,
ADD `w_device_id` varchar(64) DEFAULT NULL,
ADD `w_sensor_serial` varchar(32) DEFAULT NULL,
ADD `w_sensor_model` varchar(32) DEFAULT NULL,
ADD `w_sensor_face` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_sensor_angle` int(11) NOT NULL DEFAULT '0',
ADD `w_sensor_lat_s` double NOT NULL DEFAULT '0',
ADD `w_sensor_lng_s` double NOT NULL DEFAULT '0',
ADD `w_sensor_lat_e` double NOT NULL DEFAULT '0',
ADD `w_sensor_lng_e` double NOT NULL DEFAULT '0',
ADD `w_sensor_ignoreS` float NOT NULL DEFAULT '0',
ADD `w_sensor_ignoreE` float NOT NULL DEFAULT '0',
ADD `w_sensor_noOfZone` int(11) NOT NULL DEFAULT '0',
ADD `w_sensor_stepOfZone` float NOT NULL DEFAULT '0',
ADD `w_sensor_offset` float NOT NULL DEFAULT '0',
ADD `w_sensor_ignoreZone` varchar(256) DEFAULT NULL,
ADD `w_sensor_scheduleS` float NOT NULL DEFAULT '0',
ADD `w_sensor_scheduleE` float NOT NULL DEFAULT '0',
ADD `w_sensor_scheduleZone` varchar(256) DEFAULT NULL,
ADD `w_sensor_week` varchar(16) DEFAULT NULL,
ADD `w_sensor_time` varchar(256) DEFAULT NULL,
ADD `w_sensor_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_sensor_stop` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_sensor_reload` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_event_cycle` float NOT NULL DEFAULT '0',
ADD `w_event_pickTime` double NOT NULL DEFAULT '0',
ADD `w_event_holdTime` double NOT NULL DEFAULT '0',
ADD `w_event_keepHole` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_event_syncDist` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_alarm_level` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_system_ip` varchar(16) DEFAULT NULL,
ADD `w_system_port` int(11) NOT NULL DEFAULT '0',
ADD `w_systemBF_ip` varchar(16) DEFAULT NULL,
ADD `w_systemBF_port` int(11) NOT NULL DEFAULT '0',
ADD `w_systemAF_ip` varchar(16) DEFAULT NULL,
ADD `w_systemAF_port` int(11) NOT NULL DEFAULT '0',
ADD `w_master_Addr` varchar(32) DEFAULT NULL,
ADD `w_master_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_virtual_Addr` varchar(32) DEFAULT NULL,
ADD `w_virtual_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_sensor_Addr` varchar(32) DEFAULT NULL,
ADD `w_sensor_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_email_Addr` varchar(256) DEFAULT NULL,
ADD `w_email_Time` varchar(16) DEFAULT NULL,
ADD `w_table_PortIn` int(11) NOT NULL DEFAULT '0',
ADD `w_table_PortOut` int(11) NOT NULL DEFAULT '0',
ADD `w_host_Addr` varchar(32) DEFAULT NULL,
ADD `w_host_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_host_Addr2` varchar(32) DEFAULT NULL,
ADD `w_host_Port2` int(11) NOT NULL DEFAULT '0',
ADD `w_tcp_Addr` varchar(32) DEFAULT NULL,
ADD `w_tcp_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_tcp_Addr2` varchar(32) DEFAULT NULL,
ADD `w_tcp_Port2` int(11) NOT NULL DEFAULT '0',
ADD `w_url1` varchar(128) DEFAULT NULL,
ADD `w_url2` varchar(128) DEFAULT NULL,
ADD `w_url3` varchar(128) DEFAULT NULL,
ADD `w_url4` varchar(128) DEFAULT NULL,
ADD `w_alert_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_Value` float NOT NULL DEFAULT '0',
ADD `w_alert2_Port` int(11) NOT NULL DEFAULT '0',
ADD `w_alert2_Value` float NOT NULL DEFAULT '0',
ADD `w_opt11` varchar(32) DEFAULT NULL,
ADD `w_opt12` int(11) NOT NULL DEFAULT '0',
ADD `w_opt13` varchar(32) DEFAULT NULL,
ADD `w_opt14` varchar(32) DEFAULT NULL,
ADD `w_opt21` varchar(32) DEFAULT NULL,
ADD `w_opt22` int(11) NOT NULL DEFAULT '0',
ADD `w_opt23` varchar(32) DEFAULT NULL,
ADD `w_opt24` varchar(32) DEFAULT NULL,
ADD `w_opt91` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_opt92` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_opt93` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_opt94` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_keycode` varchar(64) DEFAULT NULL,
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);


}
?>
