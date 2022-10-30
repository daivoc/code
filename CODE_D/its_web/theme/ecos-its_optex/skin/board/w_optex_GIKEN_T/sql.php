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
ADD `w_sensor_desc` varchar(128) DEFAULT NULL,
ADD `w_sensor_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_giken_ip` varchar(32) DEFAULT NULL,
ADD `w_giken_verson` varchar(32) DEFAULT NULL,
ADD `w_giken_serial` varchar(32) DEFAULT NULL,
ADD `w_giken_live_url` varchar(128) DEFAULT NULL,

ADD `w_security_mode` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_allow_permit` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_allow_multiple` tinyint(1) NOT NULL DEFAULT '0',

ADD `w_face_direction_A` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_face_direction_B` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_face_direction_C` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_face_direction_D` tinyint(1) NOT NULL DEFAULT '0',

ADD `w_alert_Port1` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_Value1` float NOT NULL DEFAULT '0',
ADD `w_alert_Port2` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_Value2` float NOT NULL DEFAULT '0',
ADD `w_alert_Port3` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_Value3` float NOT NULL DEFAULT '0',
ADD `w_alert_Port4` int(11) NOT NULL DEFAULT '0',
ADD `w_alert_Value4` float NOT NULL DEFAULT '0',
ADD `w_host_Addr1` varchar(32) DEFAULT NULL,
ADD `w_host_Port1` int(11) NOT NULL DEFAULT '0',
ADD `w_host_Addr2` varchar(32) DEFAULT NULL,
ADD `w_host_Port2` int(11) NOT NULL DEFAULT '0',
ADD `w_event_Addr1` varchar(32) DEFAULT NULL,
ADD `w_event_Port1` int(11) NOT NULL DEFAULT '0',
ADD `w_event_Addr2` varchar(32) DEFAULT NULL,
ADD `w_event_Port2` int(11) NOT NULL DEFAULT '0',

ADD `w_reset_interval` float NOT NULL DEFAULT '0',

ADD `w_opencv_crop_w` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_crop_h` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_crop_x` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_crop_y` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask_w` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask_h` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask_x` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask_y` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask2_w` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask2_h` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask2_x` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask2_y` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask3_w` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask3_h` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask3_x` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_mask3_y` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_object_w` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_object_h` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_object_p` int(11) NOT NULL DEFAULT '0',

ADD `w_opencv_grayLv` float NOT NULL DEFAULT '0',

ADD `w_opencv_threshold` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_gBlur` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_canny` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_kernel` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_filter` int(11) NOT NULL DEFAULT '0',
ADD `w_opencv_tuner` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_opencv_mask` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_opencv_iLog` tinyint(1) NOT NULL DEFAULT '0',

ADD `w_bounce_time` int(11) NOT NULL DEFAULT '0',

ADD `w_group_level` tinyint(1) NOT NULL DEFAULT '0',

ADD `w_gpio_in` varchar(16) DEFAULT NULL,
ADD `w_gpio_out` varchar(16) DEFAULT NULL,

ADD `w_remote_accessible` varchar(256) DEFAULT NULL,

ADD `w_alarm_disable` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_keycode` varchar(64) DEFAULT NULL,
ADD `w_license` varchar(64) DEFAULT NULL,
ADD `w_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP";
sql_query($sql, false);
}


// mysql -u its -p; // GXnLRNT9H50yKQ3G
// use its_web;

// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_grayLv` float NOT NULL DEFAULT '0' AFTER `w_opencv_object_p`;

// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_gBlur` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_filter`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_canny` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_gBlur`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_kernel` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_canny`;

// ALTER TABLE `g5_write_g400t300` ADD `w_bounce_time` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_tuner`;

// ALTER TABLE `g5_write_g400t300` ADD `w_group_level` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_opencv_tuner`;
// ALTER TABLE `g5_write_g400t300` ADD `w_gpio_in` varchar(16) DEFAULT NULL AFTER `w_group_level`;
// ALTER TABLE `g5_write_g400t300` ADD `w_gpio_out` varchar(16) DEFAULT NULL AFTER `w_gpio_in`;

// ALTER TABLE `g5_write_g400t300` ADD `w_remote_accessible` varchar(256) DEFAULT NULL AFTER `w_opencv_tuner`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_object_p` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_object_h`;
// ALTER TABLE `g5_write_g400t300` ADD `w_alert_Port3` int(11) NOT NULL DEFAULT '0' AFTER `w_alert_Value2`;
// ALTER TABLE `g5_write_g400t300` ADD `w_alert_Value3` float NOT NULL DEFAULT '0' AFTER `w_alert_Port3`;
// ALTER TABLE `g5_write_g400t300` ADD `w_alert_Port4` int(11) NOT NULL DEFAULT '0' AFTER `w_alert_Value3`;
// ALTER TABLE `g5_write_g400t300` ADD `w_alert_Value4` float NOT NULL DEFAULT '0' AFTER `w_alert_Port4`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_object_w` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_crop_y`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_object_h` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_object_w`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_threshold` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_object_h`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_filter` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_threshold`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_tuner` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_opencv_filter`;

// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask_w` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_crop_y`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask_h` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask_w`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask_x` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask_h`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask_y` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask_x`;

// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_opencv_tuner`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_iLog` tinyint(1) NOT NULL DEFAULT '0' AFTER `w_opencv_mask`;

// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask2_w` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask_y`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask2_h` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask2_w`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask2_x` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask2_h`;
// ALTER TABLE `g5_write_g400t300` ADD `w_opencv_mask2_y` int(11) NOT NULL DEFAULT '0' AFTER `w_opencv_mask2_x`;

// ALTER TABLE `g5_write_g400t300` ADD `w_event_Addr1` varchar(32) DEFAULT NULL AFTER `w_host_Port2`;
// ALTER TABLE `g5_write_g400t300` ADD `w_event_Port1` int(11) NOT NULL DEFAULT '0' AFTER `w_event_Addr1`;
// ALTER TABLE `g5_write_g400t300` ADD `w_event_Addr2` varchar(32) DEFAULT NULL AFTER `w_event_Port1`;
// ALTER TABLE `g5_write_g400t300` ADD `w_event_Port2` int(11) NOT NULL DEFAULT '0' AFTER `w_event_Addr2`;

?>
