<?php
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

/* NVR 업데이트 */
include_once($board_skin_path.'/../w_include_nvr/nvrWriteUpdate.php');

$w_sensor_serial = get_w_sensor_serial($bo_table, $wr_id); // MD5(Wits IP + '||' + Device ID) 
// if($w_alert_Value1 == 0) $w_alert_Port1 = 0;
// if($w_alert_Value2 == 0) $w_alert_Port2 = 0;
// if (!$w_opencv_crop_w) $w_opencv_crop_w = 220;
// if (!$w_opencv_crop_h) $w_opencv_crop_h = 130;
// if (!$w_opencv_crop_x) $w_opencv_crop_x = 90;
// if (!$w_opencv_crop_y) $w_opencv_crop_y = 0;
// if (!$w_opencv_object_w) $w_opencv_object_w = 90;
// if (!$w_opencv_object_h) $w_opencv_object_h = 90;
// if (!$w_opencv_object_p) $w_opencv_object_p = 20;

if (!$w_tailing_ip) $w_tailing_ip = "192.168.168.30";
if (!$w_tailing_live_url) $w_tailing_live_url = "http://192.168.168.30/cgi-bin/trace.cgi";

if (!$w_gpio_out) $w_gpio_out = '11110000';
if (!$w_gpio_in) $w_gpio_in = '11111111';
if (!$w_bounce_time) $w_bounce_time = 200;

$sql = "UPDATE $write_table 
	SET 
		w_cpu_id = '$w_cpu_id',
		w_device_id = '$w_device_id',
		w_sensor_url = '$w_sensor_url',
		w_sensor_serial = '$w_sensor_serial',
		w_sensor_desc = '$w_sensor_desc',
		w_sensor_disable = '$w_sensor_disable',
		w_security_mode = '$w_security_mode',
		w_allow_permit = '$w_allow_permit',
		w_allow_multiple = '$w_allow_multiple',
		w_face_direction_A = '$w_face_direction_A',
		w_face_direction_B = '$w_face_direction_B',
		w_face_direction_C = '$w_face_direction_C',
		w_face_direction_D = '$w_face_direction_D',
		w_alert_Port1 = '$w_alert_Port1',
		w_alert_Value1 = '$w_alert_Value1',
		w_alert_Port2 = '$w_alert_Port2',
		w_alert_Value2 = '$w_alert_Value2',
		w_alert_Port3 = '$w_alert_Port3',
		w_alert_Value3 = '$w_alert_Value3',
		w_alert_Port4 = '$w_alert_Port4',
		w_alert_Value4 = '$w_alert_Value4',
		w_host_Addr1 = '$w_host_Addr1',
		w_host_Port1 = '$w_host_Port1',
		w_host_Addr2 = '$w_host_Addr2',
		w_host_Port2 = '$w_host_Port2',
		w_event_Addr1 = '$w_event_Addr1',
		w_event_Port1 = '$w_event_Port1',
		w_event_Addr2 = '$w_event_Addr2',
		w_event_Port2 = '$w_event_Port2',
		w_reset_interval = '$w_reset_interval',

		w_opencv_crop_w = '$w_opencv_crop_w',
		w_opencv_crop_h = '$w_opencv_crop_h',
		w_opencv_crop_x = '$w_opencv_crop_x',
		w_opencv_crop_y = '$w_opencv_crop_y',
		w_opencv_mask_w = '$w_opencv_mask_w',
		w_opencv_mask_h = '$w_opencv_mask_h',
		w_opencv_mask_x = '$w_opencv_mask_x',
		w_opencv_mask_y = '$w_opencv_mask_y',
		w_opencv_mask2_w = '$w_opencv_mask2_w',
		w_opencv_mask2_h = '$w_opencv_mask2_h',
		w_opencv_mask2_x = '$w_opencv_mask2_x',
		w_opencv_mask2_y = '$w_opencv_mask2_y',
		w_opencv_mask3_w = '$w_opencv_mask3_w',
		w_opencv_mask3_h = '$w_opencv_mask3_h',
		w_opencv_mask3_x = '$w_opencv_mask3_x',
		w_opencv_mask3_y = '$w_opencv_mask3_y',
		w_opencv_object_w = '$w_opencv_object_w',
		w_opencv_object_h = '$w_opencv_object_h',
		w_opencv_object_p = '$w_opencv_object_p',
		w_opencv_tail_w = '$w_opencv_tail_w',
		w_opencv_tail_h = '$w_opencv_tail_h',
		w_opencv_tail_x = '$w_opencv_tail_x',
		w_opencv_tail_y = '$w_opencv_tail_y',
		w_opencv_tail_over_x = '$w_opencv_tail_over_x',
		w_opencv_tail_over_y = '$w_opencv_tail_over_y',
		w_opencv_tail_pixel = '$w_opencv_tail_pixel',
		w_opencv_grayLv = '$w_opencv_grayLv',
		w_opencv_threshold = '$w_opencv_threshold',
		w_opencv_gBlur = '$w_opencv_gBlur',
		w_opencv_canny = '$w_opencv_canny',
		w_opencv_kernel = '$w_opencv_kernel',
		w_opencv_filter = '$w_opencv_filter',
		w_opencv_tuner = '$w_opencv_tuner',
		w_opencv_mask = '$w_opencv_mask',
		w_opencv_iLog = '$w_opencv_iLog',

		w_bounce_time = '$w_bounce_time',
		w_group_level = '$w_group_level',

		w_gpio_in = '$w_gpio_in',
		w_gpio_out = '$w_gpio_out',

		w_remote_accessible = '$w_remote_accessible',
		
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

// $config['db']['gpwio_serial'] = $w_sensor_serial;
// $config['db']['gpwio_desc'] = $w_sensor_desc;
// $config['db']['w_sensor_direction'] = $w_sensor_direction;
// $config['db']['w_sensor_detect_L'] = $w_sensor_detect_L;
// $config['db']['w_sensor_detect_R'] = $w_sensor_detect_R;
// $config['db']['gpwio_disable'] = $w_sensor_disable;
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
// if($w_sensor_disable) {
// 	unlink(G5_CU_CFG_PATH.'/COUNT_GPIO_'.$w_sensor_serial.'.json');
// } else {
// 	$fp = fopen(G5_CU_CFG_PATH.'/COUNT_GPIO_'.$w_sensor_serial.'.json', 'w');
// 	fwrite($fp, json_encode($config, JSON_PRETTY_PRINT));
// 	fclose($fp);
// }
?>
