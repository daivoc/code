﻿<?php
include_once("$board_skin_path/config_sensor.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

if(!$w_id) $w_id = $w_cpu_id;
// $w_sensor_serial = get_w_sensor_serial($w_system_ip, $w_device_id); // MD5(Wits IP + '||' + Device ID)  
$w_sensor_serial = get_w_sensor_serial($bo_table, $w_system_ip, $wr_id); // MD5(Wits IP + '||' + Device ID)  
$w_table_PortIn = getNodePort($DEVICE_table_PortIn, $bo_table, $wr_id, $w_device_id);
$w_table_PortOut = getNodePort($DEVICE_table_PortOut, $bo_table, $wr_id, $w_device_id);

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
		w_sensor_spot = '$w_sensor_spot',
		w_sensor_offset = '$w_sensor_offset',
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
		w_opt91 = '$w_opt91',
		w_opt92 = '$w_opt92',
		w_opt93 = '$w_opt93',
		w_opt94 = '$w_opt94',
		w_output1_relay = '$w_output1_relay',
		w_output1_value = '$w_output1_value',
		w_output1_group = '$w_output1_group',
		w_output2_relay = '$w_output2_relay',
		w_output2_value = '$w_output2_value',
		w_output2_group = '$w_output2_group',
		w_output3_relay = '$w_output3_relay',
		w_output3_value = '$w_output3_value',
		w_output3_group = '$w_output3_group',
		w_output4_relay = '$w_output4_relay',
		w_output4_value = '$w_output4_value',
		w_output4_group = '$w_output4_group',
		w_anglePanO = '$w_anglePanO',
		w_anglePanA = '$w_anglePanA',
		w_anglePanB = '$w_anglePanB',
		w_angleTiltO = '$w_angleTiltO',
		w_angleTiltA = '$w_angleTiltA',
		w_angleTiltB = '$w_angleTiltB',
		w_distanceO = '$w_distanceO',
		w_distanceA = '$w_distanceA',
		w_distanceB = '$w_distanceB',
		w_zoomO = '$w_zoomO',
		w_zoomA = '$w_zoomA',
		w_zoomB = '$w_zoomB',
		w_ptzX = '$w_ptzX',
		w_ptzY = '$w_ptzY',
		w_ptzH = '$w_ptzH',
		w_ptzA = '$w_ptzA',
		w_ptzCamURL = '$w_ptzCamURL',
		w_ptzCamENC = '$w_ptzCamENC',
		w_keycode = '$w_keycode',
		w_stamp = '$w_stamp'
	WHERE wr_id = '$wr_id' ";

sql_query($sql);

/* JSON 생성 */
// http://192.168.0.80/theme/ecos-its_optex/utility/status/jsonCFG.php?&bo_table=g300t100&wr_id=1
$jsonCFG = file_get_contents(G5_THEME_URL."/utility/status/jsonCFG.php?&bo_table=$bo_table&wr_id=$wr_id");
// alert($jsonCFG);

?>