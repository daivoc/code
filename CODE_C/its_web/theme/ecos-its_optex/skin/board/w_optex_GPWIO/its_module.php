<?php
if (!defined('_GNUBOARD_')) exit;

function get_w_gpwio_serial($bo_table, $wr_id) { // MD5(Wits IP + GPWIO ID) $w_system_ip, $w_device_id
	$string = $bo_table."_".$_SERVER['SERVER_ADDR']."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_gpwio_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_gpwio_serial =  strtoupper($string);
	return $get_w_gpwio_serial;
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

	$select_w_device_id = '<select name="w_alert_Port" id="w_alert_Port" class="form-control input50P" placeholder="Alarm ID" ><option value="" disabled selected>Alarm ID</option>';
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

function select_w_gpwio_status($cur_w_gpwio_status) {
    global $g5, $bo_table, $event_status;
	
	$select_w_gpwio_status = '<select name="w_gpwio_status" id="w_gpwio_status" class="form-control input25P required" required>';
	while (list($key, $value) = each($event_status)) { 
		if($cur_w_gpwio_status == $key)
			$select_w_gpwio_status .='<option selected value="'.$key.'">'.$value.'</option>';
		else
			$select_w_gpwio_status .='<option value="'.$key.'">'.$value.'</option>';
	} 
	$select_w_gpwio_status .= '</select>';
	return $select_w_gpwio_status;
}

function select_w_sensor($cur_w_sensor_id) {
	global $g5;
	$sensorList = array();
	$write_table = $g5['write_prefix'] . G5_CU_CONF_GPIO;
	// $sql = " SELECT wr_subject, w_sensor_serial, alert_Port, alert_Value, host_Addr, host_Port, host_Addr2, host_Port2 FROM $write_table WHERE w_sensor_disable = 0 ORDER BY wr_id ASC ";
	$sql = " SELECT * FROM $write_table WHERE w_sensor_disable = 0 ORDER BY wr_id ASC ";
    $result = sql_query($sql);
// data-aport="'.$row['alert_Port'].'" data-avalue="'.$row['alert_Value'].'" data-haddr1="'.$row['host_Addr'].'" data-hport1="'.$row['host_Port'].'" data-haddr2="'.$row['host_Addr2'].'" data-hport2="'.$row['host_Port2'].'"

	$select_w_sensor_id = '<select name="w_sensor_serial" id="w_sensor_serial" class="form-control input50P"><option value="" data-aport="" data-avalue="0" data-haddr1="" data-hport1="0" data-haddr2="" data-hport2="0" >Standalone</option>';
	// while (list($key, $value) = each($sensorList)) { 
    while ($row = sql_fetch_array($result)) {
		if($cur_w_sensor_id == $row['w_sensor_serial']) {
			$select_w_sensor_id .='<option value="'.$row['w_sensor_serial'].'" data-aport="'.$row['w_alert_Port'].'" data-avalue="'.$row['w_alert_Value'].'" data-haddr1="'.$row['w_host_Addr'].'" data-hport1="'.$row['w_host_Port'].'" data-haddr2="'.$row['w_host_Addr2'].'" data-hport2="'.$row['w_host_Port2'].'" selected>'.$row['wr_subject'].'</option>';
		} else {
			$select_w_sensor_id .='<option value="'.$row['w_sensor_serial'].'" data-aport="'.$row['w_alert_Port'].'" data-avalue="'.$row['w_alert_Value'].'" data-haddr1="'.$row['w_host_Addr'].'" data-hport1="'.$row['w_host_Port'].'" data-haddr2="'.$row['w_host_Addr2'].'" data-hport2="'.$row['w_host_Port2'].'">'.$row['wr_subject'].'</option>';
		}
	}
	$select_w_sensor_id .= '</select>';
	return $select_w_sensor_id;
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