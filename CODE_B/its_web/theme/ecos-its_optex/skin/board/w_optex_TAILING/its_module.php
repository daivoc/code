<?php
if (!defined('_GNUBOARD_')) exit;

function get_w_sensor_serial($bo_table, $wr_id) { // MD5(Wits IP + GPWIO ID) $w_system_ip
	$string = $bo_table."_".$_SERVER['SERVER_ADDR']."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_sensor_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_sensor_serial =  strtoupper($string);
	return $get_w_sensor_serial;
}

// // System CPU 시리얼 번호 확인
// function get_w_cpu_id($cur_w_cpu_id) {
// 	if($cur_w_cpu_id) {
// 		$get_w_cpu_id = $cur_w_cpu_id;
// 	} else {
// 		$get_w_cpu_id = "0000000000000000";
// 		$cur_cpu_serial = shell_exec("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2");
// 		if($cur_cpu_serial)
// 			$get_w_cpu_id = $cur_cpu_serial;
// 	}
// 	return $cur_cpu_serial;
// }
// System CPU 시리얼 번호 확인
function get_w_cpu_id() {
	$cur_cpu_serial = shell_exec("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2");
return $cur_cpu_serial;
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
	$sql = " SELECT wr_id, w_sensor_detect_L, w_sensor_detect_R FROM $write_table WHERE w_sensor_disable = $disable ";
	$result = sql_query($sql);
	// $num_rows = sql_num_rows($result);
	$used_id = array();
	while ($row = sql_fetch_array($result)) {
		array_push($used_id, array($row['wr_id'],$row['w_sensor_detect_L'],$row['w_sensor_detect_R']));
	}
	// ex: Array ( [0] => Array ( [0] => 3 [1] => 19 [2] => 27 [3] => 0 ) )
	return $used_id;
}

/*
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

	$select_w_device_id = '<select name="w_device_id" id="w_device_id" required class="form-control input25P required" placeholder="<?php echo $SK_BO_Link_Interface[ITS_Lang]?>" ><option value="" disabled selected><?php echo $SK_BO_Link_Interface[ITS_Lang]?></option>';

	// eth1 192.168.168.10
	// eth2 192.168.168.11
	exec("ip route | grep 192.168 | awk '{print $3,$9}' | grep eth[1234]", $ethPort);
	// exec("ip route | grep eth[1234] | awk '{print $3,$9}'", $ethPort);
	// print_r($ethPort); // 사용중인 센서 목록
	// $lines = explode("\n", $ethPort);
	foreach ($ethPort as $line) {
		$nameIs = strtr(strtoupper($line), " ", "_");
		if($cur_w_device_id == $nameIs) {
			$select_w_device_id .='<option selected>'.$nameIs.'</option>';
		} else {
			if (strstr($used_device,$nameIs)) { // 다른 센서가 사용중이면 중복사용 금지
				;
			} else {
				$select_w_device_id .='<option>'.$nameIs.'</option>';
			}
		}
	}
	$select_w_device_id .= '</select>';
	return $select_w_device_id;
}
*/

// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function select_w_GPIO_alert($id, $cur_w_alert_Port, $relay_alert) {
    // global $g5, $bo_table;

	// $write_table = $g5['write_prefix'] . $bo_table;
	// $sql = " SELECT * FROM $write_table ";
    // $result = sql_query($sql);
    // while ($row = sql_fetch_array($result)) {
	// 	$used_device .= $row[$id].",";
	// }
	// $usedKey = explode(',', $used_device);

	$select_w_device_id = '<select name='.$id.' id='.$id.' class="form-control input25P" placeholder="Alarm ID" ><option value="" disabled selected>Alarm ID</option>';
	while (list($key, $value) = each($relay_alert)) { 
		if($cur_w_alert_Port == $key) {
			$select_w_device_id .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_w_device_id .='<option value="'.$key.'">'.$value.'</option>';
			// if(in_array($key, $usedKey)) { // 다른 센서가 사용중이면 중복사용 금지
			// 	;
			// } else {
			// 	$select_w_device_id .='<option value="'.$key.'">'.$value.'</option>';
			// }
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