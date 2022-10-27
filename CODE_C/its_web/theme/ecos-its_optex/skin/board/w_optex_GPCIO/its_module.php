<?php
if (!defined('_GNUBOARD_')) exit;

function get_w_sensor_serial($bo_table, $wr_id) { // MD5(Wits IP + GPCIO ID) $w_system_ip
	$string = $bo_table."_".$_SERVER['SERVER_ADDR']."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_sensor_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_sensor_serial =  strtoupper($string);
	return $get_w_sensor_serial;
}

function get_w_device_id($wr_id) {
	$string = "GPCIO_".$_SERVER['SERVER_ADDR']."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_device_id =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_sensor_serial =  strtoupper($string);
	return $get_w_device_id;
}


// System CPU 시리얼 번호 확인
function get_w_cpu_id($cur_w_cpu_id) {
	if($cur_w_cpu_id) {
		$get_w_cpu_id = $cur_w_cpu_id;
	} else {
		$get_w_cpu_id = "0000000000000000";
		$cur_cpu_serial = shell_exec("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2");
		if($cur_cpu_serial)
			$get_w_cpu_id = $cur_cpu_serial;
	}
	return $get_w_cpu_id;
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

function get_w_detect_id($disable = 0) {
    global $g5, $bo_table;
	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT wr_id, w_gpcio_detect_L, w_gpcio_detect_R FROM $write_table WHERE w_gpcio_disable = $disable ";
	$result = sql_query($sql);
	// $num_rows = sql_num_rows($result);
	$used_id = array();
	while ($row = sql_fetch_array($result)) {
		array_push($used_id, array($row['wr_id'],$row['w_gpcio_detect_L'],$row['w_gpcio_detect_R']));
	}
	// ex: Array ( [0] => Array ( [0] => 3 [1] => 19 [2] => 27 [3] => 0 ) )
	return $used_id;
}

// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function select_w_GPIO_sensor($cur_w_gpio, $field_name, $relay_input) {
    global $g5, $bo_table;

	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT * FROM $write_table ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$used_device .= $row[$field_name].",";
	}
	$usedKey = explode(',', $used_device);

	$select_w_device_id = "<select name='$field_name' id='$field_name' class='form-control' style='width: 110px;display: inline;vertical-align: super;' placeholder='Port'>";
	while (list($key, $value) = each($relay_input)) { 
		if($cur_w_gpio == $key) {
			$select_w_device_id .="<option selected value='$key'>$value</option>";
		} else {
			if(in_array($key, $usedKey)) { // 다른 센서가 사용중이면 중복사용 금지
				;
			} else {
				$select_w_device_id .="<option value='$key'>$value</option>";
			}
		}
	} 
	$select_w_device_id .= '</select>';
	return $select_w_device_id;
}


// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function select_w_GPIO_alert($cur_w_alert_Port) {
    global $g5, $bo_table, $relay_alert;

	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT * FROM $write_table ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$used_device .= $row['w_alert_Port'].",";
	}
	$usedKey = explode(',', $used_device);

	$select_w_device_id = '<select name="w_alert_Port" id="w_alert_Port" class="form-control input25P" placeholder="Alarm ID" ><option value="" disabled selected>Alarm ID</option>';
	while (list($key, $value) = each($relay_alert)) { 
		if($cur_w_alert_Port == $key) {
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