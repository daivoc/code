<?php
include_once("$board_skin_path/its_module.php"); // Local Function List
$w_model_id = get_w_model_id($w_sensor_model);

$tmp_check = '';
foreach($ignore_check_list as $check) {
	$tmp_check .= $check.','; //echoes the value set in the HTML form for each checked checkbox.
}
$w_sensor_ignore = $tmp_check;

if($w == 'u') {
	$sql = "UPDATE $write_table 
	SET 
		w_id = '$wr_id',
		w_cpu_id = '$w_cpu_id',
		w_system_ip = '$w_system_ip',
		w_device_id = '$w_device_id',
		w_model_id = '$w_model_id',
		w_sensor_id = '$w_sensor_id',
		w_sensor_serial = '$w_sensor_serial',
		w_sensor_model = '$w_sensor_model',
		w_sensor_baud = '$w_sensor_baud',
		w_sensor_ignore = '$w_sensor_ignore',
		w_sensor_timeout = '$w_sensor_timeout',
		w_sensor_face = '$w_sensor_face',
		w_sensor_angle = '$w_sensor_angle',
		w_sensor_lat_s = '$w_sensor_lat_s',
		w_sensor_lng_s = '$w_sensor_lng_s',
		w_sensor_lat_e = '$w_sensor_lat_e',
		w_sensor_lng_e = '$w_sensor_lng_e',
		w_sensor_validLv = '$w_sensor_validLv',
		w_alarm_enable = '$w_alarm_enable',
		w_alarm_level = '$w_alarm_level',
		w_stamp = '$w_stamp',
		w_api_devId = '$w_api_devId',
		w_api_devPass = '$w_api_devPass',
		w_api_gwId = '$w_api_gwId',
		w_api_ipAddr = '$w_api_ipAddr',
		w_api_ipPort = '$w_api_ipPort',
		w_api_tagId = '$w_api_tagId'
	WHERE wr_id = '$wr_id' ";
} else {
	$sql = "UPDATE $write_table 
	SET 
		w_id = '$wr_id',
		w_cpu_id = '$w_cpu_id',
		w_system_ip = '$w_system_ip',
		w_device_id = '$w_device_id',
		w_model_id = '$w_model_id',
		w_sensor_id = '$w_sensor_id',
		w_sensor_serial = '$w_sensor_serial',
		w_sensor_model = '$w_sensor_model',
		w_sensor_baud = '$w_sensor_baud',
		w_sensor_ignore = '$w_sensor_ignore',
		w_sensor_timeout = '$w_sensor_timeout',
		w_sensor_face = '$w_sensor_face',
		w_sensor_angle = '$w_sensor_angle',
		w_sensor_lat_s = '$w_sensor_lat_s',
		w_sensor_lng_s = '$w_sensor_lng_s',
		w_sensor_lat_e = '$w_sensor_lat_e',
		w_sensor_lng_e = '$w_sensor_lng_e',
		w_sensor_validLv = '$w_sensor_validLv',
		w_stamp = '$w_stamp',
		w_api_devId = '$w_api_devId',
		w_api_devPass = '$w_api_devPass',
		w_api_gwId = '$w_api_gwId',
		w_api_ipAddr = '$w_api_ipAddr',
		w_api_ipPort = '$w_api_ipPort',
		w_api_tagId = '$w_api_tagId'
	WHERE wr_id = '$wr_id' ";
}
// echo $sql;
// exit();
sql_query($sql);

?>