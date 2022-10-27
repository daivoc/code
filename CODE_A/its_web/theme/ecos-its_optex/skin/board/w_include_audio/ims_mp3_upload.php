<?php
$target_dir = '/var/www/html/its_web/data/audio/'; // G5_CU_AUD_PATH 
$filename = $_GET["filename"];
$arr_file_types = ['audio/mpeg', 'audio/mp3'];
 
if (!(in_array($_FILES['file']['type'], $arr_file_types))) {
    echo "false";
    return;
}
 
if (!file_exists($target_dir)) {
    mkdir($target_dir, 0777);
}

// if (move_uploaded_file($_FILES['file']['tmp_name'], $target_dir . $_FILES['file']['name'])) {
if (move_uploaded_file($_FILES['file']['tmp_name'], $target_dir . $filename)) {
	echo "success";
} else {
	echo 'Sorry, there was an error uploading your file.';
}

die();
?>