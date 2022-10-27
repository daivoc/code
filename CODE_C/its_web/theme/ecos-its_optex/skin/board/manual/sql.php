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
ADD `w_sub_title` varchar(256) DEFAULT NULL,
ADD `w_group_main` varchar(64) DEFAULT NULL,
ADD `w_group_sub` varchar(128) DEFAULT NULL,
ADD `w_order` int(11) NOT NULL DEFAULT '0'";
sql_query($sql, false);
}

?>
