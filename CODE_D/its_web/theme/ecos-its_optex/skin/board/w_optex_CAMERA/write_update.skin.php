<?php
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

$w_id = $w_cpu_id;
$w_camera_serial = get_w_camera_serial($bo_table, get_w_system_ip(), $wr_id); // MD5(Wits IP + '||' + Device ID) 
$w_port_IO01 = $DEVICE_init_port + ($wr_id*4); // ex) 7000 + (1 * 4) = 7004
$w_port_IO02 = $w_port_IO01 + 1;
$w_port_IO03 = $w_port_IO02 + 1;
$w_port_IO04 = $w_port_IO03 + 1;

$sql = "UPDATE $write_table 
	SET 
		w_device_id = '$w_device_id',
		w_map_id = '$w_map_id',
		w_camera_serial = '$w_camera_serial',
		w_camera_model = '$w_camera_model',
		w_camera_desc = '$w_camera_desc',
		w_camera_user = '$w_camera_user',
		w_camera_pass = '$w_camera_pass',
		w_camera_hash = '$w_camera_hash',
		w_camera_disable = '$w_camera_disable',
		w_camera_reload = '$w_camera_reload',
		w_camera_addr = '$w_camera_addr',
		w_camera_port = '$w_camera_port',
		w_camera_px_X = '$w_camera_px_X',
		w_camera_px_Y = '$w_camera_px_Y',
		w_alarm_disable = '$w_alarm_disable',
		w_port_IO01 = '$w_port_IO01',
		w_port_IO02 = '$w_port_IO02',
		w_port_IO03 = '$w_port_IO03',
		w_port_IO04 = '$w_port_IO04',
		w_url1 = '$w_url1',
		w_url2 = '$w_url2',
		w_url3 = '$w_url3',
		w_url4 = '$w_url4',
		w_linked_0 = '$w_linked_0',
		w_linked_1 = '$w_linked_1',
		w_linked_2 = '$w_linked_2',
		w_linked_3 = '$w_linked_3',
		w_sns_id = '$w_sns_id',
		w_box_id = '$w_box_id',
		w_keycode = '$w_keycode',
		w_license = '$w_license',
		w_stamp = '$w_stamp'
	WHERE wr_id = '$wr_id' ";

sql_query($sql);

/* JSON 생성 */
// http://192.168.0.80/theme/ecos-its_optex/utility/status/jsonCFG.php?&bo_table=g300t100&wr_id=1
$jsonCFG = file_get_contents(G5_THEME_URL."/utility/status/jsonCFG.php?&bo_table=$bo_table&wr_id=$wr_id");
// alert($jsonCFG);

?>