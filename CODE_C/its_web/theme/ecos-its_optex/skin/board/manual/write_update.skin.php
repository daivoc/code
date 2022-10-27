<?php
// if(!$w_order) $w_order = 9999;
$sql = "UPDATE $write_table 
	SET 
		w_sub_title = '$w_sub_title',
		w_group_main = '$w_group_main',
		w_group_sub = '$w_group_sub',
		w_order = '$w_order'
	WHERE wr_id = '$wr_id' ";

sql_query($sql);
?>