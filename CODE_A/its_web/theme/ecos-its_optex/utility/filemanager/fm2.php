<?php
include_once('./_common.php');
/* 
window.open("<?php echo G5_THEME_URL ?>/utility/filemanager/fm.php?PATH=data||image", "File Manager", "width=640,height=400,scrollbars=no");
*/
if ($is_guest) exit("Abnormal approach!");

// $_GET['PATH']은 웹 web_Root를 기준으로한 서브 PATH 명으로 폴더간은 '|'로 한다.
// fm.php?PATH=data||log
// if ($_GET['ID'] && $_GET['PATH']){ 
if ($_GET['PATH']){ 
	$myPath = str_replace("|","/",$_GET['PATH']); // theme|ecos-its_optex|user|image|gikenC -> 
	$files = file_get_contents('./filemanager.php');
	$files = str_replace("__current_path__",$myPath,$files);
	$target = "/var/www/html/its_web/".$myPath."/../index.php";
	file_put_contents($target,$files);
} else {
	exit("Abnormal approach!");
}
header("Location: http://".$_SERVER['SERVER_ADDR']."/".$myPath."/../index.php");

?>