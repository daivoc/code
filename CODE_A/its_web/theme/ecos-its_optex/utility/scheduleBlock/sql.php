<?php
$tableID = "w_block_event";
$write_table = $tableID;
// 필드 존재여부에 따라 세롭개 생성 {
$sql = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_id' ";
$exeQuery = sql_query($sql);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sql = " CREATE TABLE IF NOT EXISTS `".$write_table."` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`title` varchar(255) DEFAULT '',
		`startdate` varchar(48) DEFAULT '',
		`enddate` varchar(48) DEFAULT '',
		`allDay` varchar(5) DEFAULT '',
		`disabled` tinyint(1) NOT NULL DEFAULT 0,
		`color` varchar(16) DEFAULT '',
		`bgColor` varchar(16) DEFAULT '',
		`borderColor` varchar(16) DEFAULT '',
		`textColor` varchar(16) DEFAULT '',
		`bo_table` varchar(32) DEFAULT '',
		`wr_id` int(11) NOT NULL DEFAULT 0,
		`wr_subject` varchar(255) DEFAULT '',
		`w_sensor_serial` varchar(255) NOT NULL,
		`w_week` int(1) NOT NULL DEFAULT 0,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=utf8";
		sql_query($sql, false);
	// $sql = " CREATE TABLE IF NOT EXISTS `".$write_table."` (
	// `id` int(11) NOT NULL AUTO_INCREMENT,
	// `title` varchar(255) DEFAULT NULL,
	// `startdate` varchar(48) DEFAULT NULL,
	// `enddate` varchar(48) DEFAULT NULL,
	// `allDay` varchar(5) DEFAULT NULL,
	// `disabled` tinyint(1) NOT NULL DEFAULT '0',
	// `color` varchar(16) DEFAULT NULL,
	// `bgColor` varchar(16) DEFAULT NULL,
	// `borderColor` varchar(16) DEFAULT NULL,
	// `textColor` varchar(16) DEFAULT NULL,
	// `bo_table` varchar(32) DEFAULT NULL,
	// `wr_id` int(11) NOT NULL DEFAULT '0',
	// `wr_subject` varchar(255) DEFAULT NULL,
	// `w_sensor_serial` varchar(255) DEFAULT NULL,
	// `w_week` tinyint(1) NOT NULL DEFAULT '0',
	// PRIMARY KEY (`id`)
	// ) ENGINE=MyISAM DEFAULT CHARSET=utf8;";
	// sql_query($sql, false);
}
?>