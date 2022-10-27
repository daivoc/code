<?php
if (!defined('_GNUBOARD_')) exit;

// 시스템 아이피 주소 확인
function get_w_system_ip() {
	$get_w_system_ip = $_SERVER['SERVER_ADDR'];
	return $get_w_system_ip;
}

function get_w_box_serial($bo_table, $w_system_ip, $wr_id) { // MD5(Wits IP + Sensor ID) $w_system_ip, $w_device_id
	$string = $bo_table."_".$w_system_ip."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_box_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_box_serial =  strtoupper($string);
	return $get_w_box_serial;
}

function select_w_box_model($cur_w_box_model) {
    global $SENSOR_model;
	$select_w_box_model = '<select name="w_box_model" id="w_box_model" required class="form-control input50P required" placeholder="<?php echo $SK_BO_Model_Name[ITS_Lang]?>" >';
	foreach ($SENSOR_model as $value) {
		if($cur_w_box_model == $value)
			$select_w_box_model .='<option selected>'.$value.'</option>';
		else
			$select_w_box_model .='<option>'.$value.'</option>';
	}
	$select_w_box_model .= '</select>';
	return $select_w_box_model;
}

function select_w_camera($cur_w_camera_id, $id) {
	// wr_subject, w_map_id, w_camera_model, w_camera_addr, w_camera_serial
	global $g5;
	$cameraList = array();
	$write_table = $g5['write_prefix'] . G5_CU_CONF_CAMERA;
	$sql = " SELECT wr_subject, w_map_id, w_camera_model, w_camera_addr, w_camera_serial FROM $write_table WHERE w_camera_disable = 0 ORDER BY wr_id DESC ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$cameraList[$row['w_camera_serial']] = $row['wr_subject'];
	}

	$select_w_camera_id = '<select name="'.$id.'" id="'.$id.'" class="form-control input25P" placeholder="" ><option value="" selected></option>';
	while (list($key, $value) = each($cameraList)) { 
		if($cur_w_camera_id == $key) {
			$select_w_camera_id .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_w_camera_id .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_w_camera_id .= '</select>';
	return $select_w_camera_id;
}

function get_w_camInfo($cur_w_camera_id, $fieldIs) {
	global $g5;
	$write_table = $g5['write_prefix'] . G5_CU_CONF_CAMERA;
	// wr_subject, w_map_id, w_camera_model, w_camera_addr
	$sql = " SELECT $fieldIs FROM $write_table WHERE w_camera_serial = '$cur_w_camera_id' LIMIT 1 ";
    $result = sql_query($sql);
	$row = sql_fetch_array($result);
    // while ($row = sql_fetch_array($result)) {
		// $wr_subject = $row['wr_subject'];
	// }
	// return $sql;
	return $row[$fieldIs];
}

function get_w_stamp($cur_w_stamp) {
	if($cur_w_stamp) {
		$get_w_stamp = $cur_w_stamp;
	} else {
		$get_w_stamp = date('Y-m-d h:i:s');
	}
	// return $get_w_stamp;
	return date('Y-m-d h:i:s');
}

function get_w_program_info($path) {
	$filename = $path.'/readme.txt';
	if (is_readable($filename)){
		$handle  = fopen($filename, "r");
		while(!feof($handle)) {
			$str = fgets($handle);
			if(substr( $str, 0, 16 ) === "Product Version:") {
				$info[0] = $str;
			} else if(substr( $str, 0, 15 ) === "Product Detail:") {
				$info[1] = $str;
			}
		}
		fclose($handle);
	} else {
		$info[0] = "Unknown"; // $filename."No Programs Info.";
	}
	return $info;
}
?>