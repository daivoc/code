<?php
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

$w_id = $w_cpu_id;
$w_netapp_serial = get_w_netapp_serial($bo_table, get_w_system_ip(), $wr_id); // MD5(Wits IP + '||' + Device ID) 
$w_port_01 = $DEVICE_init_port + ($wr_id*4); // ex) 7000 + (1 * 4) = 7004
$w_port_02 = $w_port_01 + 1;
$w_port_03 = $w_port_02 + 1;
$w_port_04 = $w_port_03 + 1;

$sql = "UPDATE $write_table 
	SET 
		w_device_id = '$w_device_id',
		w_map_id = '$w_map_id',
		w_netapp_serial = '$w_netapp_serial',
		w_netapp_model = '$w_netapp_model',
		w_netapp_desc = '$w_netapp_desc',
		w_opt_char_01 = '$w_opt_char_01',
		w_opt_char_02 = '$w_opt_char_02',
		w_opt_tiny_01 = '$w_opt_tiny_01',
		w_netapp_disable = '$w_netapp_disable',
		w_netapp_reload = '$w_netapp_reload',
		w_netapp_addr = '$w_netapp_addr',
		w_netapp_port = '$w_netapp_port',
		w_opt_int_01 = '$w_opt_int_01',
		w_opt_int_02 = '$w_opt_int_02',
		w_alarm_disable = '$w_alarm_disable',
		w_port_01 = '$w_port_01',
		w_port_02 = '$w_port_02',
		w_port_03 = '$w_port_03',
		w_port_04 = '$w_port_04',
		w_url_01 = '$w_url_01',
		w_url_02 = '$w_url_02',
		w_url_03 = '$w_url_03',
		w_url_04 = '$w_url_04',
		w_link_04 = '$w_link_04',
		w_link_01 = '$w_link_01',
		w_link_02 = '$w_link_02',
		w_link_03 = '$w_link_03',
		w_sns_id = '$w_sns_id',
		w_box_id = '$w_box_id',
		w_keycode = '$w_keycode',
		w_license = '$w_license',
		w_stamp = '$w_stamp'
	WHERE wr_id = '$wr_id' ";

sql_query($sql);



?>