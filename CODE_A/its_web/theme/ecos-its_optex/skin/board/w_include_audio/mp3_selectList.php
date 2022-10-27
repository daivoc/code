<?php
$target_dir = '/var/www/html/its_web/data/audio';
$selectList = '<select id="audioList_'.$_POST['id'].'" class="form-control input20P">';
$selected = $_POST['selected'];
if ($handle = opendir($target_dir)) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
			if ($selected == $entry){
				$selectList .= "<option selected>$entry</option>";
			} else {
				$selectList .= "<option>$entry</option>";
			}
        }
    }
    closedir($handle);
}
$selectList .= "</select>";
echo $selectList;
die();
?>