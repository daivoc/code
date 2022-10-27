<?php
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

$w_device_id = get_w_device_id($wr_id); // MD5(Wits IP + '||' + Device ID) 
$w_sensor_serial = get_w_sensor_serial($bo_table, $wr_id); // MD5(Wits IP + '||' + Device ID) 

if($w_alert_Value == 0) $w_alert_Port = 0;

$sql = "UPDATE $write_table 
	SET 
		w_cpu_id = '$w_cpu_id',
		w_device_id = '$w_device_id',
		w_sensor_serial = '$w_sensor_serial',
		w_gpcio_desc = '$w_gpcio_desc',
		w_gpcio_direction = '$w_gpcio_direction',
		w_gpcio_detect_L = '$w_gpcio_detect_L',
		w_gpcio_detect_R = '$w_gpcio_detect_R',
		w_gpcio_trigger_L = '$w_gpcio_trigger_L',
		w_gpcio_trigger_R = '$w_gpcio_trigger_R',
		w_gpcio_disable = '$w_gpcio_disable',
		w_security_mode = '$w_security_mode',
		w_distance = '$w_distance',
		w_speed_L = '$w_speed_L',
		w_speed_H = '$w_speed_H',
		w_capacity_A = '$w_capacity_A',
		w_capacity_B = '$w_capacity_B',
		w_capacity_C = '$w_capacity_C',
		w_capacity_D = '$w_capacity_D',
		w_direction_AX = '$w_direction_AX',
		w_direction_XA = '$w_direction_XA',
		w_direction_BX = '$w_direction_BX',
		w_direction_XB = '$w_direction_XB',
		w_direction_CX = '$w_direction_CX',
		w_direction_XC = '$w_direction_XC',
		w_direction_DX = '$w_direction_DX',
		w_direction_XD = '$w_direction_XD',
		w_internal_AX = '$w_internal_AX',
		w_internal_XA = '$w_internal_XA',
		w_internal_BX = '$w_internal_BX',
		w_internal_XB = '$w_internal_XB',
		w_internal_CX = '$w_internal_CX',
		w_internal_XC = '$w_internal_XC',
		w_internal_DX = '$w_internal_DX',
		w_internal_XD = '$w_internal_XD',
		w_external_AX = '$w_external_AX',
		w_external_XA = '$w_external_XA',
		w_external_BX = '$w_external_BX',
		w_external_XB = '$w_external_XB',
		w_external_CX = '$w_external_CX',
		w_external_XC = '$w_external_XC',
		w_external_DX = '$w_external_DX',
		w_external_XD = '$w_external_XD',
		w_alert_Port = '$w_alert_Port',
		w_alert_Value = '$w_alert_Value',
		w_host_Addr1 = '$w_host_Addr1',
		w_host_Port1 = '$w_host_Port1',
		w_host_Addr2 = '$w_host_Addr2',
		w_host_Port2 = '$w_host_Port2',
		w_alarm_disable = '$w_alarm_disable',
		w_keycode = '$w_keycode',
		w_license = '$w_license',
		w_stamp = '$w_stamp'
	WHERE wr_id = '$wr_id' ";
$result = sql_query($sql);

// JSON  파일 생성 및 저장
// $config = array();
// $config['db'] = [];
// $config['db']['id'] = $wr_id;
// $config['db']['subject'] = $wr_subject;

// $config['db']['gpcio_serial'] = $w_sensor_serial;
// $config['db']['gpcio_desc'] = $w_gpcio_desc;
// $config['db']['w_gpcio_direction'] = $w_gpcio_direction;
// $config['db']['w_gpcio_detect_L'] = $w_gpcio_detect_L;
// $config['db']['w_gpcio_detect_R'] = $w_gpcio_detect_R;
// $config['db']['gpcio_disable'] = $w_gpcio_disable;
// $config['db']['alert'] = [];
// $config['db']['alert']['alert01'] = array('port' => $w_alert_Port, 'value' => $w_alert_Value);
// $config['db']['hosting'] = [];
// $config['db']['hosting']['host01'] = array('ip' => $w_host_Addr1, 'port' => $w_host_Port1);
// $config['db']['hosting']['host02'] = array('ip' => $w_host_Addr2, 'port' => $w_host_Port2);
// $config['db']['license'] = $w_license;

// $config['custom'] = array();
// $config['custom']['audio'] = array('file'=> $wr_2, 'time'=> $wr_3);
// list($user, $pass, $url, $enc) = explode('||', $wr_4);
// $config['custom']['request01'] = array('user'=> $user, 'pass'=> $pass, 'host'=> $url, 'enc'=> $enc);
// list($user, $pass, $url, $enc) = explode('||', $wr_5);
// $config['custom']['request02'] = array('user'=> $user, 'pass'=> $pass, 'host'=> $url, 'enc'=> $enc);
// list($user, $pass, $url, $enc) = explode('||', $wr_6);
// $config['custom']['request03'] = array('user'=> $user, 'pass'=> $pass, 'host'=> $url, 'enc'=> $enc);
// list($user, $pass, $url, $enc) = explode('||', $wr_7);
// $config['custom']['request04'] = array('user'=> $user, 'pass'=> $pass, 'host'=> $url, 'enc'=> $enc);

// list($var1, $var2, $host, $port, $opt1, $opt2) = explode('||', $wr_8);
// $config['custom']['socket01'] = array('var1'=> $var1, 'var2'=> $var2, 'host'=> $host, 'port'=> $port, 'opt1s'=> $opt1, 'opt2s'=> $opt2);
// list($var1, $var2, $host, $port, $opt1, $opt2) = explode('||', $wr_9);
// $config['custom']['socket02'] = array('var1'=> $var1, 'var2'=> $var2, 'host'=> $host, 'port'=> $port, 'opt1s'=> $opt1, 'opt2s'=> $opt2);

// if (!file_exists(G5_CU_CFG_PATH)) {
//     mkdir(G5_CU_CFG_PATH, 0777, true);
// }
// if($w_gpcio_disable) {
// 	unlink(G5_CU_CFG_PATH.'/COUNT_GPIO_'.$w_sensor_serial.'.json');
// } else {
// 	$fp = fopen(G5_CU_CFG_PATH.'/COUNT_GPIO_'.$w_sensor_serial.'.json', 'w');
// 	fwrite($fp, json_encode($config, JSON_PRETTY_PRINT));
// 	fclose($fp);
// }
?>