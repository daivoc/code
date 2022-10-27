<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// ims 폴더 확인후 생성
$imsImage = G5_CU_MAP_PATH;
if (!file_exists($imsImage)) {
    mkdir($imsImage, 0755, true);
}
$targetFile = $imsImage . '/' . 'customLogo.png';
$backupFile = $imsImage . '/' . $_FILES["file"]["name"];

$uploadOk = 1;

$imageFileType = strtolower(pathinfo($_FILES["file"]["name"],PATHINFO_EXTENSION));

// Check file size
// if ($_FILES["file"]["size"] > 500000) { // 500Kb
if ($_FILES["file"]["size"] > 1000000) { // 1Mb
    echo "Sorry, your file is too large.(Max:1Mb)";
    $uploadOk = 0;
}

// Allow certain file formats
if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" ) {
// if($imageFileType != "svg" ) {
    echo "Sorry, only png or jpg files are allowed.";
    $uploadOk = 0;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
	// echo move_uploaded_file($_FILES["file"]["tmp_name"], $target_file) or die($_FILES['file']['error'][0]);
    if (move_uploaded_file($_FILES["file"]["tmp_name"], $targetFile)) {
        echo "The file has been uploaded.";
		
		if (!copy($targetFile, $backupFile)) { // 백업
			echo "failed to copy $file...\n";
		}

    } else {
        echo $targetFile." Sorry, there was an error uploading... - ".$_FILES["file"]["name"];
    }
}
?>
