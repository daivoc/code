<?php
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

$w_id = $w_cpu_id;
$w_box_serial = get_w_box_serial($bo_table, get_w_system_ip(), $wr_id); // MD5(Wits IP + '||' + Device ID) 

$sql = "UPDATE $write_table 
	SET 
		w_map_id = '$w_map_id',
		w_box_serial = '$w_box_serial',
		w_box_desc = '$w_box_desc',
		w_box_disable = '$w_box_disable',
		w_alarm_disable = '$w_alarm_disable',
		w_cam_0 = '$w_cam_0',
		w_cam_1 = '$w_cam_1',
		w_cam_2 = '$w_cam_2',
		w_cam_3 = '$w_cam_3',
		w_ptz_0 = '$w_ptz_0',
		w_ptz_1 = '$w_ptz_1',
		w_ptz_2 = '$w_ptz_2',
		w_ptz_3 = '$w_ptz_3',
		w_iFrame = '$w_iFrame',
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