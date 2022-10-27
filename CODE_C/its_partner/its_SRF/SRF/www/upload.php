<?php
$target_dir = 'config/';
$target_file = $target_dir . basename($_FILES['selectJson']['name']);
$uploadOk = 1;
$fileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
// // Check if file already exists
// if (file_exists($target_file)) {
//      echo 'Sorry, file already exists.';
//      $uploadOk = 0;
// }
// Check file size
if ($_FILES['selectJson']['size'] > 500000) {
		echo 'Sorry, your file is too large.';
		$uploadOk = 0;
}
// Allow certain file formats
if($fileType != 'json') {
		echo 'Sorry, only JSON files are allowed.'.$target_file;
		$uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
		echo 'Sorry, your file was not uploaded.';
// if everything is ok, try to upload file
} else {
		if (move_uploaded_file($_FILES['selectJson']['tmp_name'], $target_file)) {
				// alert('The file '. basename( $_FILES['selectJson']['name']). ' has been uploaded.');
				header('Location: ' . $_SERVER['HTTP_REFERER']);
		} else {
				echo 'Sorry, there was an error uploading your file.';
		}
}
?>
