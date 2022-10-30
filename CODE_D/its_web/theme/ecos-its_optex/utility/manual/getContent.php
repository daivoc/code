<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

if($id) {
	$sql = " SELECT wr_content FROM g5_write_".G5_CU_CONF_MANUAL." WHERE wr_id = '".$id."'";
	$result = sql_query($sql);
	while ($row = sql_fetch_array($result)) {
		if($row["wr_content"]) {
			exit($row["wr_content"]);
		}
	}
} else {
	// $sql = " SELECT wr_content FROM g5_write_".G5_CU_CONF_MANUAL." WHERE w_order = '10000'";
	// $result = sql_query($sql);
	// while ($row = sql_fetch_array($result)) {
		// if($row["wr_content"]) {
			// exit($row["wr_content"]);
		// }
	// }
}
?>
