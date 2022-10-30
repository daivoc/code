<?php
if (!defined('_GNUBOARD_')) exit;

function getNodePort($table_Port, $bo_table, $wr_id, $w_device_id) {
	preg_match_all('!\d+!', $bo_table, $matches);
	// return (int)$table_Port + $matches[0][0] + $matches[0][1] + $wr_id + $w_device_id;
	return (int)$table_Port + $matches[0][0] + ($matches[0][1]/10) + $wr_id;
}

function get_w_id($cur_w_id) {
	if($cur_w_id) {
		$get_w_id = $cur_w_id;
	} else {
		$get_w_id = $_SERVER['SERVER_ADDR'];
	}
	return $get_w_id;
}

// 시스템 아이피 주소 확인
function get_w_system_ip() {
	$get_w_system_ip = $_SERVER['SERVER_ADDR'];
	return $get_w_system_ip;
}
// 시스템 아이피 주소 확인
function get_w_host_ip($cur_w_host_ip) {
	if($cur_w_host_ip) {
		$get_w_host_ip = $cur_w_host_ip;
	} else {
		$get_w_host_ip = $_SERVER['SERVER_ADDR'];
	}
	return $get_w_host_ip;
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


// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function current_sensor_count() {
    global $g5, $bo_table;

	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = "SELECT count(*) as total FROM $write_table WHERE w_sensor_disable = 0";
    $result = sql_query($sql);
	$row = sql_fetch_array($result);
	return $row['total'];
}

// GPIO 디바이스포트, 템퍼포트는 디바이스포트의 짝수로 한다.
function select_w_GPIO_alert($cur_w_device_id) {
    global $g5, $bo_table, $DEVICE_alert;

	$write_table = $g5['write_prefix'] . $bo_table;
	$sql = " SELECT * FROM $write_table ";
    $result = sql_query($sql);
    while ($row = sql_fetch_array($result)) {
		$used_device .= $row['w_alert_Port'].",";
	}
	$usedKey = explode(',', $used_device);

	$select_w_device_id = '<select name="w_alert_Port" id="w_alert_Port" class="form-control input50P" placeholder="<?php echo $SK_BO_Link_Alarm[ITS_Lang]?>" ><option value="" disabled selected><?php echo $SK_BO_Link_Alarm[ITS_Lang]?></option>';
	while (list($key, $value) = each($DEVICE_alert)) { 
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

function get_w_sensor_serial($bo_table, $w_system_ip, $wr_id) { // MD5(Wits IP + Sensor ID) $w_system_ip, $w_device_id
	$string = $bo_table."_".$w_system_ip."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
	$get_w_sensor_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.
	// $get_w_sensor_serial =  strtoupper($string);
	return $get_w_sensor_serial;
}

function select_w_sensor_face($cur_w_sensor_face, $view=0) {
	$arr = array(
		0 => 'Ignore',
		1 => 'Forward',
		2 => 'Backward',
		3 => 'Outside',
		4 => 'Inside',
		5 => 'Upside',
		6 => 'Downside'
	);

	if($view) {
		$select_w_sensor_face = $arr[$cur_w_sensor_face];
	} else {
		$select_w_sensor_face = '<select name="w_sensor_face" id="w_sensor_face" class="form-control input50P">';
		while (list($key, $value) = each($arr)) { 
			if($cur_w_sensor_face == $key)
				$select_w_sensor_face .='<option selected value="'.$key.'">'.$value.'</option>';
			else
				$select_w_sensor_face .='<option value="'.$key.'">'.$value.'</option>';
		} 
		$select_w_sensor_face .= '</select>';
	}
	return $select_w_sensor_face;
}


function select_w_sensor_scheduleTime($w_sensor_time, $numberOfHour=24) { // BSS 시리즈 비활성 영역 설정
	$w_sensor_time = rtrim($w_sensor_time, ',');
	$cur_w_sensor_scheduleTime = explode(",", $w_sensor_time);
	$select_w_sensor_scheduleTime = '<input type="text" name="w_sensor_time" value="'.$w_sensor_time.'" id="w_sensor_time" readonly class="w_hide"><ol id="select_w_sensor_scheduleTime">';

	for ($i=0; $i<$numberOfHour; $i++) {
		if(in_array("$i", $cur_w_sensor_scheduleTime))
			$select_w_sensor_scheduleTime .= '<li class="ui-state-default ui-selected" id="igTime_'.$i.'">'.$i.'</li>';
		else
			$select_w_sensor_scheduleTime .= '<li class="ui-state-default" id="igTime_'.$i.'">'.$i.'</li>';
	}
	$select_w_sensor_scheduleTime .= '</ol>';
	return $select_w_sensor_scheduleTime;
}

function select_w_alarm_level($cur_w_alarm_level, $view=0) { // 0 ~ 254
	$arr = array(
		// 0 => '모든 정상 이벤트', single double triple quadruple
		1 => 'Single',
		2 => 'Double',
		3 => 'Triple',
		4 => 'Quadruple',
		// 64 => 'Debug Mode'
	);
	if($view) {
		$select_w_alarm_level = $arr[$cur_w_alarm_level];
	} else {
		$select_w_alarm_level = '<select name="w_alarm_level" id="w_alarm_level" required class="form-control input50P required" placeholder="<?php echo $SK_BO_Events_Level[ITS_Lang]?>" >';

		while (list($key, $value) = each($arr)) { 
			if($cur_w_alarm_level == $key)
				$select_w_alarm_level .='<option selected value="'.$key.'">'.$value.'</option>';
			else
				$select_w_alarm_level .='<option value="'.$key.'">'.$value.'</option>';
		} 
		$select_w_alarm_level .= '</select>';
	}
	return $select_w_alarm_level;
}
		
function get_w_stamp($cur_w_stamp) {
	if($cur_w_stamp) {
		$get_w_stamp = $cur_w_stamp;
	} else {
		$get_w_stamp = date('Y-m-d h:i:s');
	}
	return $get_w_stamp;
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