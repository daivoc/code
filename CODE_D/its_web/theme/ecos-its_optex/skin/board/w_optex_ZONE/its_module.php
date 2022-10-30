<?php
if (!defined('_GNUBOARD_')) exit;

// 시스템 아이피 주소 확인
function get_w_system_ip() {
	$get_w_system_ip = $_SERVER['SERVER_ADDR'];
	return $get_w_system_ip;
}

function get_w_zone_serial($bo_table, $w_system_ip, $wr_id) { // MD5(Wits IP + Sensor ID) $w_system_ip, $w_device_id
	$string = $bo_table."_".$w_system_ip."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_zone_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_zone_serial =  strtoupper($string);
	return $get_w_zone_serial;
}

function select_w_zone_group($linked_IP) {
	$zoneID = substr(substr($linked_IP, 9), 0, -5); // 192_168_0_14
	global $g5;
	$zoneListHTML = "";
	$write_table = $g5['write_prefix'] . G5_CU_CONF_ZONE;
	// $sql = " SELECT wr_subject, w_map_id, w_zone_serial FROM $write_table WHERE w_zone_disable = 0 AND w_sns_0 LIKE '%$zoneID%' ORDER BY wr_id DESC ";
	$sql = " SELECT * FROM $write_table WHERE w_zone_disable = 0 AND w_sns_0 LIKE '%$zoneID%' ORDER BY wr_id DESC ";
	$result = sql_query($sql);

	while ($row = sql_fetch_array($result)) {
		if($linked_IP != $row['w_sns_0']) {
			$href="./board.php?bo_table=".G5_CU_CONF_ZONE."&wr_id=".$row['wr_id'];
			$zoneListHTML .= "<a href=".$href." type='button' class='btn btn-danger btn-sm' style='margin-right:4px;'>".$row['wr_subject']."</a>";
		}
	}
	$zoneListHTML .= "";
	return $zoneListHTML;
}

function select_w_zone_model($cur_w_zone_model) {
	global $SENSOR_model;
	$select_w_zone_model = '<select name="w_zone_model" id="w_zone_model" required class="form-control input50P required" placeholder="<?php echo $SK_BO_Model_Name[ITS_Lang]?>" >';
	foreach ($SENSOR_model as $value) {
		if($cur_w_zone_model == $value)
			$select_w_zone_model .='<option selected>'.$value.'</option>';
		else
			$select_w_zone_model .='<option>'.$value.'</option>';
	}
	$select_w_zone_model .= '</select>';
	return $select_w_zone_model;
}

function select_w_box($cur_w_box_id, $id) {
	// wr_subject, w_map_id, w_box_model, w_box_addr, w_box_serial
	global $g5;
	$boxList = array();
	$write_table = $g5['write_prefix'] . G5_CU_CONF_BOX;
	$sql = " SELECT wr_subject, w_map_id, w_box_serial FROM $write_table WHERE w_box_disable = 0 ORDER BY wr_id DESC ";
	$result = sql_query($sql);
	while ($row = sql_fetch_array($result)) {
		$boxList[$row['w_box_serial']] = $row['wr_subject'];
	}

	$select_w_box_id = '<select name="'.$id.'" id="'.$id.'" class="form-control input25P" placeholder="" ><option value="" selected></option>';
	while (list($key, $value) = each($boxList)) { 
		if($cur_w_box_id == $key) {
			$select_w_box_id .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_w_box_id .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_w_box_id .= '</select>';
	return $select_w_box_id;
}

function select_w_camera($cur_w_camera_id, $id) {
	// wr_subject, w_map_id, w_camera_model, w_camera_addr, w_camera_serial
	global $g5;
	$write_table = $g5['write_prefix'] . G5_CU_CONF_CAMERA;
	$sql = " SELECT * FROM $write_table WHERE w_camera_disable = 0 ORDER BY wr_id DESC ";
	$result = sql_query($sql);
	
	$select_w_camera_id = '<select name="'.$id.'" id="'.$id.'" class="form-control input25P" placeholder="" ><option value="" selected></option>';
	while ($row = sql_fetch_array($result)) {
		$camAuth = $row['w_camera_addr'].",".$row['w_camera_user'].",".$row['w_camera_pass'].",".$row['w_camera_port'];
		if($cur_w_camera_id == $row['w_camera_serial']) {
			$select_w_camera_id .='<option selected value="'.$row['w_camera_serial'].'" data-auth="'.$camAuth.'">'.$row['wr_subject'].'</option>';
		} else {
			$select_w_camera_id .='<option value="'.$row['w_camera_serial'].'" data-auth="'.$camAuth.'">'.$row['wr_subject'].'</option>';
		}
	} 
	$select_w_camera_id .= '</select>';

	// while ($row = sql_fetch_array($result)) {
		// $cameraList[$row['w_camera_serial']] = $row['wr_subject'];
	// }

	// $select_w_camera_id = '<select name="'.$id.'" id="'.$id.'" class="form-control input25P" placeholder="" ><option value="" selected></option>';
	// while (list($key, $value) = each($cameraList)) { 
		// if($cur_w_camera_id == $key) {
			// $select_w_camera_id .='<option selected value="'.$key.'">'.$value.'</option>';
		// } else {
			// $select_w_camera_id .='<option value="'.$key.'">'.$value.'</option>';
		// }
	// } 
	// $select_w_camera_id .= '</select>';
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