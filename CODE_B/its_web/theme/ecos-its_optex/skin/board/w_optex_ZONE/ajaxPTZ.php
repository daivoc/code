<?php
if(isset($_POST['camInfo'])) {
	// print_r($_POST['camInfo'][0]);
	$json = $_POST['camInfo'];
	// var $info = "cd /home/pi/utility && node onvifGetPTZ.js "; // .$json[0]." ".$json[1]." ".$json[2]." ".$json[3];
	$last_line = system("cd /home/pi/utility && node onvifGetPTZ.js $json[0] $json[1] $json[2] $json[3]");
	echo $last_line;
	// $json = $_POST['camInfo'];
	// print_r(json_decode($json, true));
	// cd /home/pi/utility && node onvifGetPTZ.js $_POST['camInfo'][0] $_POST['camInfo'][1] $_POST['camInfo'][2] $_POST['camInfo'][3]

}
?>