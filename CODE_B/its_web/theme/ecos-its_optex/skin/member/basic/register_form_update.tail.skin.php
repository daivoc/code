<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가
?>

<?php
if($member['mb_id'] == 'its' ) { // 
	// ADM Configure
	$sql = " update {$g5['config_table']}
	set cf_title = '{$_POST['cf_title']}',
		cf_10 = '{$_POST['cf_10']}',
		cf_possible_ip = '{$_POST['cf_possible_ip']}',
		cf_intercept_ip = '{$_POST['cf_intercept_ip']}' ";
	sql_query($sql);
}
?>


<?php
if($member['mb_id'] == 'manager' ) { // 
	// 수정된 아이피를 관련센서 정보(w_sensor_serial, w_system_ip)에 일괄적용한다.
	$w_system_ip = $mb_4;

	// 센서
	foreach ($G5_CU_CONF_GROUP as $key => $value) {
		// echo "\$G5_CU_CONF_GROUP[$key] => $value.\n";
		$write_table = $g5['write_prefix'] . $value;
		$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
		if($val !== FALSE) {
			$sql = "SELECT wr_id, wr_subject FROM $write_table";
			$result = sql_query($sql);
			while ($row = sql_fetch_array($result)) {
				$string = $value."_".$w_system_ip."_".str_pad($row['wr_id'], 4, "0", STR_PAD_LEFT);
				$get_w_sensor_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
				$sql = "UPDATE ".$write_table." SET w_sensor_serial = '".$get_w_sensor_serial."', w_system_ip = '".$w_system_ip."' WHERE wr_id = '".$row['wr_id']."' ";
				sql_query($sql);
				// echo $sql."<br>";
			}
		}
	}

	// 카메라
	$write_table = $g5['write_prefix'] . G5_CU_CONF_CAMERA;
	$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
	if($val !== FALSE) {
		$sql = "SELECT wr_id, wr_subject FROM $write_table";
		$result = sql_query($sql);
		while ($row = sql_fetch_array($result)) {
			$string = G5_CU_CONF_CAMERA."_".$w_system_ip."_".str_pad($row['wr_id'], 4, "0", STR_PAD_LEFT);
			$get_w_camera_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
			$sql = "UPDATE ".$write_table." SET w_camera_serial = '".$get_w_camera_serial."' WHERE wr_id = '".$row['wr_id']."' ";
			sql_query($sql);
		}
	}
	
	// GPWIO
	$write_table = $g5['write_prefix'] . G5_CU_CONF_GPWIO;
	$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
	if($val !== FALSE) {
		$sql = "SELECT wr_id, wr_subject FROM $write_table";
		$result = sql_query($sql);
		while ($row = sql_fetch_array($result)) {
			$string = G5_CU_CONF_GPWIO."_".$w_system_ip."_".str_pad($row['wr_id'], 4, "0", STR_PAD_LEFT);
			$get_w_gpwio_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
			$sql = "UPDATE ".$write_table." SET w_gpwio_serial = '".$get_w_gpwio_serial."' WHERE wr_id = '".$row['wr_id']."' ";
			sql_query($sql);
		}
	}
	
	// GPACU
	$write_table = $g5['write_prefix'] . G5_CU_CONF_GPACU;
	$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
	if($val !== FALSE) {
		$sql = "SELECT wr_id, wr_subject FROM $write_table";
		$result = sql_query($sql);
		while ($row = sql_fetch_array($result)) {
			$string = G5_CU_CONF_GPACU."_".$w_system_ip."_".str_pad($row['wr_id'], 4, "0", STR_PAD_LEFT);
			$get_w_gpacu_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
			$sql = "UPDATE ".$write_table." SET w_gpacu_serial = '".$get_w_gpacu_serial."' WHERE wr_id = '".$row['wr_id']."' ";
			sql_query($sql);
		}
	}
}
?>
