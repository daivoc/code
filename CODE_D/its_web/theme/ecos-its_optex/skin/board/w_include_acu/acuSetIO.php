<?php
include_once('./_common.php');

$configACU = json_decode(file_get_contents('/home/pi/common/config.json', true), true);

foreach($_POST['setIO'] as $io => $value) {
	if($value == 'true') {
		$_POST['setIO'][$io] = TRUE;
	} else {
		$_POST['setIO'][$io] = FALSE;
	}
}
$configACU["ioBoard"]['acu']['setIO'] = $_POST['setIO'];

foreach($_POST['setPW'] as $io => $value) {
	if($value == 'true') {
		$_POST['setPW'][$io] = TRUE;
	} else {
		$_POST['setPW'][$io] = FALSE;
	}
}
$configACU["ioBoard"]['acu']['setPW'] = $_POST['setPW'];

$fp = fopen('/home/pi/common/config.json', 'w') or die("Error opening for write config.json");
// fwrite($fp, json_encode($configACU, JSON_PRETTY_PRINT)); // ,JSON_UNESCAPED_UNICODE, , JSON_FORCE_OBJECT
fwrite($fp, json_encode($configACU, JSON_FORCE_OBJECT | JSON_PRETTY_PRINT)); // ,JSON_UNESCAPED_UNICODE, , JSON_FORCE_OBJECT
// fwrite($fp, json_encode($configACU)); // ,JSON_UNESCAPED_UNICODE
fclose($fp);
die();
?>