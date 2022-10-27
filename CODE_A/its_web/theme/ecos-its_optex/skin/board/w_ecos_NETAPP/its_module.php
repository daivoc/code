<?php
if (!defined('_GNUBOARD_')) exit;

// 시스템 아이피 주소 확인
function get_w_system_ip() {
	$get_w_system_ip = $_SERVER['SERVER_ADDR'];
	return $get_w_system_ip;
}

// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function select_w_device_order($cur_w_device_id, $arr_R) {
    global $g5, $bo_table;
	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT * FROM $write_table ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$used_device .= $row['w_device_id'].","; // if($row['w_device_id']) 
	}
	// echo($used_device); // 사용중인 센서 목록
	$usedKey = explode(',', $used_device);

	$select_w_device_id = '<select name="w_device_id" id="w_device_id" required class="form-control input25P required" placeholder="<?php echo $SK_BO_Link_Interface[ITS_Lang]?>" >';
	while (list($key, $value) = each($arr_R)) { 
		if($cur_w_device_id == $key) {
			$select_w_device_id .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			if(in_array($key, $usedKey)) { // 다른 센서가 사용중이면 중복사용 금지
				;
			} else {
				$select_w_device_id .='<option value="'.$key.'">'.$value.'</option>';
			}
		}
	} 
	$select_w_device_id .= '</select>';
	return $select_w_device_id;
}

function get_w_netapp_serial($bo_table, $w_system_ip, $wr_id) { // MD5(Wits IP + Sensor ID) $w_system_ip
	$string = $bo_table."_".$w_system_ip."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_netapp_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_netapp_serial =  strtoupper($string);
	return $get_w_netapp_serial;
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

	$select_w_box_id = '<select name="'.$id.'" id="'.$id.'" class="form-control input50P" placeholder="" ><option value="" selected></option>';
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


function select_w_netapp_model($cur_w_netapp_model, $icc) {
	// $icc = json_decode(file_get_contents('/home/pi/MONITOR/netapp.json', true), true);
	$select_w_netapp_model = '<select name="w_netapp_model" id="w_netapp_model" required class="form-control input25P required" placeholder="<?php echo $SK_BO_Model_Name[ITS_Lang]?>" ><option></option>';
	foreach($icc as $key => $item){
		if($cur_w_netapp_model == $key)
			$select_w_netapp_model .='<option selected>'.$key.'</option>';
		else
			$select_w_netapp_model .='<option>'.$key.'</option>';
	}
	$select_w_netapp_model .= '</select>';
	return $select_w_netapp_model;

	// foreach ($NetApp_model as $value) {
		// if($cur_w_netapp_model == $value)
			// $select_w_netapp_model .='<option selected>'.$value.'</option>';
		// else
			// $select_w_netapp_model .='<option>'.$value.'</option>';
	// }
	// $select_w_netapp_model .= '</select>';
	// return $select_w_netapp_model;
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