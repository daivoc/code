<?php
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_id' ";
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " ALTER TABLE  `$write_table` 
ADD `w_id` int(11) NOT NULL DEFAULT '0',
ADD `w_cpu_id` varchar(32) DEFAULT NULL,
ADD `w_system_ip` varchar(16) DEFAULT NULL,
ADD `w_device_id` varchar(64) DEFAULT NULL,
ADD `w_model_id` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_sensor_id` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_sensor_serial` varchar(32) DEFAULT NULL,
ADD `w_sensor_model` varchar(32) DEFAULT NULL,
ADD `w_sensor_ignore` varchar(64) DEFAULT NULL,
ADD `w_alarm_enable` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_alarm_level` tinyint(4) NOT NULL DEFAULT '0',
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);
// echo $sql;
}
?>