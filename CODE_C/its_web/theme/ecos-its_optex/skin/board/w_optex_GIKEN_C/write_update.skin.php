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

if (!$w_giken_ip) $w_giken_ip = "192.168.168.30";
if (!$w_giken_live_url) $w_giken_live_url = "http://192.168.168.30/cgi-bin/trace.cgi";

if (!$w_gpio_out) $w_gpio_out = '11110000';
if (!$w_gpio_in) $w_gpio_in = '11111111';
if (!$w_bounce_time) $w_bounce_time = 200;

$sql = "UPDATE $write_table 
	SET 
		w_cpu_id = '$w_cpu_id',
		w_device_id = '$w_device_id',
		w_sensor_serial = '$w_sensor_serial',
		w_sensor_desc = '$w_sensor_desc',
		w_sensor_disable = '$w_sensor_disable',
		w_giken_ip = '$w_giken_ip',
		w_giken_verson = '$w_giken_verson',
		w_giken_live_url = '$w_giken_live_url',
		w_giken_serial = '$w_giken_serial',
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

/* JSON 생성 */
// http://192.168.0.80/theme/ecos-its_optex/utility/status/jsonCFG.php?&bo_table=g300t100&wr_id=1
$jsonCFG = file_get_contents(G5_THEME_URL."/utility/status/jsonCFG.php?&bo_table=$bo_table&wr_id=$wr_id");
// alert($jsonCFG);

?>
