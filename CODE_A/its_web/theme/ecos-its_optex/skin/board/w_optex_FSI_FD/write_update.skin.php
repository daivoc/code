<?php
$cfg = json_decode(file_get_contents("$board_skin_path/config.json", true), true);
include_once("$board_skin_path/its_module.php"); // Local Function List

$w_device_serial = get_w_device_serial($bo_table, $w_system_ip, $wr_id); // MD5(Wits IP + '||' + Device ID)  
if($w_alert_value == 0) $w_alert_port = 0;

$sql = "UPDATE $write_table 
	SET 
		w_id = '$w_id',
		w_parent_id = '$w_parent_id',
		w_zone_id = '$w_zone_id',
		w_zone_name = '$w_zone_name',
		w_system_ip = '$w_system_ip',
		w_device_name = '$w_device_name',
		w_device_serial = '$w_device_serial',
		w_sensor_disable = '$w_sensor_disable',
		w_sensor_stop = '$w_sensor_stop',
		w_sensor_reload = '$w_sensor_reload',
		w_event_keepHole = '$w_event_keepHole',
		w_alarm_disable = '$w_alarm_disable',
		w_ims_address_P = '$w_ims_address_P',
		w_ims_port_P = '$w_ims_port_P',
		w_ims_address_S = '$w_ims_address_S',
		w_ims_port_S = '$w_ims_port_S',
		w_snapshot_url = '$w_snapshot_url',
		w_streaming_url = '$w_streaming_url',
		w_alert_port = '$w_alert_port',
		w_alert_value = '$w_alert_value',
		w_snapshot_qty = '$w_snapshot_qty',
		w_snapshot_enc = '$w_snapshot_enc',
		w_streaming_enc = '$w_streaming_enc',
		w_license = '$w_license',
		w_keycode = '$w_keycode',
		w_stamp = '$w_stamp'
	WHERE wr_id = '$wr_id' ";

sql_query($sql);

/* JSON 생성 */
// 생성 - /var/www/html/its_web/data/config/cfg_g400t100_1.json
$jsonCFG = file_get_contents(G5_THEME_URL."/utility/status/jsonCFG.php?&bo_table=$bo_table&wr_id=$wr_id");
// alert($jsonCFG);

?>