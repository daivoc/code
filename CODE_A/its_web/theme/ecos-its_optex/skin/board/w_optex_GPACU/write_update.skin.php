﻿<?php
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List


$w_id = $w_cpu_id;
$w_gpacu_serial = get_w_gpacu_serial($bo_table, $wr_id); // MD5(Wits IP + '||' + Device ID) 
if($w_alert_Value == 0) $w_alert_Port = 0;

// 라이센스 등록에 필요한 변수(w_device_id) 규정을 위한 복사
$w_cpu_id = shell_exec("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2");;
$w_device_id = $write['w_gpacu_group'];

$data = array('customer' => $member['mb_10'], 'subject' => $board['bo_subject'], 'cpuID' => $w_cpu_id, 'serial' => $w_sensor_serial, 'device' => $w_device_id, 'license' => $w_license, 'expiry' => 24);



$sql = "UPDATE $write_table 
	SET 
		w_gpacu_serial = '$w_gpacu_serial',
		w_gpacu_status = '$w_gpacu_status',
		w_gpacu_cover = '$w_gpacu_cover',
		w_gpacu_group = '$w_gpacu_group',
		w_gpacu_desc = '$w_gpacu_desc',
		w_gpacu_disable = '$w_gpacu_disable',
		w_sensor_serial = '$w_sensor_serial',
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

?>