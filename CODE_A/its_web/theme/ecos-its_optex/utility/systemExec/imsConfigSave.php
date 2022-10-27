<?php
if(isset($_POST['config'])) {
	$json = $_POST['config'];
	
	file_put_contents('/home/pi/MONITOR/config.json', $json);
	print_r(json_decode($json, true));
}
?>