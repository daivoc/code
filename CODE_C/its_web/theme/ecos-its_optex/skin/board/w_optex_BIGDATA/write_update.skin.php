<?php
include_once("$board_skin_path/config_sensor.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

$w_id = $w_cpu_id;
// $w_sensor_serial = get_w_sensor_serial($w_system_ip, $w_device_id, $w_sensor_model); // MD5(Wits IP + '||' + Device ID)  
$w_sensor_serial = get_w_sensor_serial($bo_table, $w_system_ip, $wr_id); // MD5(Wits IP + '||' + Device ID)  
$w_table_PortIn = getNodePort($DEVICE_table_PortIn, $bo_table, $wr_id, $w_device_id);
$w_table_PortOut = getNodePort($DEVICE_table_PortOut, $bo_table, $wr_id, $w_device_id);
if($w_alert_Value == 0) $w_alert_Port = 0;
if($w_alert2_Value == 0) $w_alert2_Port = 0;
if($w_alert3_Value == 0) $w_alert3_Port = 0;
if($w_alert4_Value == 0) $w_alert4_Port = 0;
// $w_virtual_Addr = get_w_virtual_addr($w_device_id); // 디바이스 아이디에 포함된 아이피를 추출

$sql = "UPDATE $write_table 
	SET 
		w_id = '$w_id',
		w_cpu_id = '$w_cpu_id',
		w_license = '$w_license',
		w_device_id = '$w_device_id',
		w_sensor_serial = '$w_sensor_serial',
		w_sensor_model = '$w_sensor_model',
		w_sensor_face = '$w_sensor_face',
		w_sensor_angle = '$w_sensor_angle',
		w_sensor_lat_s = '$w_sensor_lat_s',
		w_sensor_lng_s = '$w_sensor_lng_s',
		w_sensor_lat_e = '$w_sensor_lat_e',
		w_sensor_lng_e = '$w_sensor_lng_e',
		w_sensor_ignoreS = '$w_sensor_ignoreS',
		w_sensor_ignoreE = '$w_sensor_ignoreE',
		w_sensor_noOfZone = '$w_sensor_noOfZone',
		w_sensor_stepOfZone = '$w_sensor_stepOfZone',
		w_sensor_ignoreZone = '$w_sensor_ignoreZone',
		w_sensor_scheduleS = '$w_sensor_scheduleS',
		w_sensor_scheduleE = '$w_sensor_scheduleE',
		w_sensor_scheduleZone = '$w_sensor_scheduleZone',
		w_sensor_week = '$w_sensor_week',
		w_sensor_time = '$w_sensor_time',
		w_sensor_disable = '$w_sensor_disable',
		w_sensor_stop = '$w_sensor_stop',
		w_sensor_reload = '$w_sensor_reload',
		w_event_pickTime = '$w_event_pickTime',
		w_event_holdTime = '$w_event_holdTime',
		w_event_keepHole = '$w_event_keepHole',
		w_event_syncDist = '$w_event_syncDist',
		w_alarm_disable = '$w_alarm_disable',
		w_alarm_level = '$w_alarm_level',
		w_system_ip = '$w_system_ip',
		w_system_port = '$w_system_port',
		w_systemBF_ip = '$w_systemBF_ip',
		w_systemBF_port = '$w_systemBF_port',
		w_systemAF_ip = '$w_systemAF_ip',
		w_systemAF_port = '$w_systemAF_port',
		w_master_Addr = '$w_master_Addr',
		w_master_Port = '$w_master_Port',
		w_virtual_Addr = '$w_virtual_Addr',
		w_virtual_Port = '$w_virtual_Port',
		w_sensor_Addr = '$w_sensor_Addr',
		w_sensor_Port = '$w_sensor_Port',
		w_email_Addr = '$w_email_Addr',
		w_email_Time = '$w_email_Time',
		w_table_PortIn = '$w_table_PortIn',
		w_table_PortOut = '$w_table_PortOut',
		w_host_Addr = '$w_host_Addr',
		w_host_Port = '$w_host_Port',
		w_host_Addr2 = '$w_host_Addr2',
		w_host_Port2 = '$w_host_Port2',
		w_tcp_Addr = '$w_tcp_Addr',
		w_tcp_Port = '$w_tcp_Port',
		w_tcp_Addr2 = '$w_tcp_Addr2',
		w_tcp_Port2 = '$w_tcp_Port2',
		w_url1 = '$w_url1',
		w_url2 = '$w_url2',
		w_url3 = '$w_url3',
		w_url4 = '$w_url4',
		w_alert_Port = '$w_alert_Port',
		w_alert_Value = '$w_alert_Value',
		w_alert2_Port = '$w_alert2_Port',
		w_alert2_Value = '$w_alert2_Value',
		w_alert3_Port = '$w_alert3_Port',
		w_alert3_Value = '$w_alert3_Value',
		w_alert4_Port = '$w_alert4_Port',
		w_alert4_Value = '$w_alert4_Value',
		w_opt22 = '$w_opt22',
		w_opt91 = '$w_opt91',
		w_opt92 = '$w_opt92',
		w_opt93 = '$w_opt93',
		w_opt94 = '$w_opt94',
		w_keycode = '$w_keycode',
		w_stamp = '$w_stamp'
	WHERE wr_id = '$wr_id' ";

sql_query($sql);



?>