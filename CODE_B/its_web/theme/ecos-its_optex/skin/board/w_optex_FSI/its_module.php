<?php
if (!defined('_GNUBOARD_')) exit;

// 시스템 아이피 주소 확인
function get_w_system_ip() {
	$get_w_system_ip = $_SERVER['SERVER_ADDR'];
	return $get_w_system_ip;
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

// USB-Ethernet 디바이스 관련 정보
function select_w_etherNet_id($cur_w_device_id) {
    global $g5, $bo_table;
	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT * FROM $write_table ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$used_device .= $row['w_device_id'];
	}
	// echo($used_device); // 사용중인 센서 목록

	$select_w_device = '<select name="w_device_id" id="w_device_id" required class="form-control input25P required"><option value="" selected>Device ID</option>';

	// eth1 192.168.168.10
	// eth2 192.168.168.11
	exec("ip route | grep 192.168.168 | awk '{print $3,$9}'", $ethPort);
	// print_r($ethPort); // 사용중인 센서 목록
	// $lines = explode("\n", $ethPort);
	foreach ($ethPort as $line) {
		$nameIs = strtr(strtoupper($line), " ", "_");
		if($cur_w_device_id == $nameIs) {
			$select_w_device .='<option selected>'.$nameIs.'</option>';
		} else {
			if (strstr($used_device,$nameIs)) { // 다른 센서가 사용중이면 중복사용 금지
				;
			} else {
				$select_w_device .='<option>'.$nameIs.'</option>';
			}
		}
	}
	$select_w_device .= '</select>';
	return $select_w_device;
}

// 디바이스 ID
function select_w_zone_id($zoneID, $zoneOutID) {
	$select_ZONE = '<select name="w_zone_id" id="w_zone_id" class="form-control input25P"><option value="" selected>Zone ID</option>';
	while (list($key, $value) = each($zoneOutID)) { 
		if($zoneID == $key) {
			$select_ZONE .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_ZONE .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_ZONE .= '</select>';
	return $select_ZONE;
}

// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function select_w_GPIO_alert($w_alert_port) {
    global $g5, $bo_table, $cfg;
	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT * FROM $write_table WHERE w_sensor_disable = 0 ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$used_device .= $row['w_alert_port'].",";
	}
	// echo($used_device); // 사용중인 센서 목록
	$usedKey = explode(',', $used_device);

	$select_w_alert = '<select name="w_alert_port" id="w_alert_port" class="form-control input50P" placeholder="Alarm ID" ><option value="" disabled selected>Alarm ID</option>';
	while (list($key, $value) = each($cfg["DEVICE_alert"])) { 
		if($w_alert_port == $key) {
			$select_w_alert .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			if(in_array($key, $usedKey)) { // 다른 센서가 사용중이면 중복사용 금지
				;
			} else {
				$select_w_alert .='<option value="'.$key.'">'.$value.'</option>';
			}
		}
	} 
	$select_w_alert .= '</select>';
	return $select_w_alert;
}

function get_w_device_serial($bo_table, $w_system_ip, $wr_id) { 
	$string = $bo_table."_".$w_system_ip."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_device_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_device_serial =  strtoupper($string);
	return $get_w_device_serial;
}

function select_w_device_model($cur_w_device_model, $arr) {
	$select_w_device_model = '<select name="w_device_model" id="w_device_model" required class="form-control input25P required" >';
	while (list($key, $value) = each($arr)) { 
		if($cur_w_device_model == $key)
			$select_w_device_model .='<option selected value="'.$key.'">'.$value.'</option>';
		else
			$select_w_device_model .='<option value="'.$key.'">'.$value.'</option>';
	} 
	$select_w_device_model .= '</select>';
	return $select_w_device_model;
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