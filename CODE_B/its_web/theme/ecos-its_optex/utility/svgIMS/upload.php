<?php
include_once('./_common.php');

if ($is_guest) exit("Abnormal approach!");

$target_dir = G5_CU_IMG_PATH;

// ims 폴더 확인후 생성
$imsImage = $target_dir . '/ims/';
if (!file_exists($imsImage)) {
    mkdir($imsImage, 0777, true);
}

$targetFile = $imsImage . 'ims_map.svg';
$targetString = stripslashes($_POST["svgCode"]);

if (!is_dir($imsImage) or !is_writable($imsImage)) {
    echo "Error if directory doesn't exist or isn't writable.";
} elseif (is_file($targetFile) and !is_writable($targetFile)) {
    echo "Error if the file exists and isn't writable.";
}

$f = file_put_contents($targetFile, $targetString);
if ($f) {	
	echo "Saved";
} else {
	echo print_r(error_get_last());
}

// $ims_map = fopen("/home/pi/MONITOR/ims_map.svg", "w") or die("Unable to open file!");
// fwrite($ims_map, $targetString);
// fclose($ims_map);

// $pieces = str_split($targetString, 1024 * 4);
// foreach ($pieces as $piece) {
	// fwrite($targetFile, $piece, strlen($piece));
// }
// fclose($targetFile);
	
?>