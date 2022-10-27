<?php
include_once('./_common.php');
/* 
중요: 경로 <?php echo G5_THEME_URL ?>/utility/filemanager 는 웹사용자의 쓰기 권한이 있어야 한다.
window.open("<?php echo G5_THEME_URL ?>/utility/filemanager/fm.php?ID=<?php echo $view['w_sensor_serial']?>&PATH=data||image||<?php echo $view['w_sensor_serial']?>", "File Manager", "width=640,height=400,scrollbars=no");
*/
if ($is_guest) exit("Abnormal approach!");

// $_GET['ID']은 임시파일 생성을 위한 파일명 구분임
// $_GET['PATH']은 웹 Root를 기준으로한 서브 PATH 명으로 폴더간은 '||'로 한다.
// fm.php?ID=its&PATH=data||log
if ($_GET['ID'] && $_GET['PATH']){ 
	$target = "./fm_".$_GET['ID'].".php";
	$myPath = str_replace("||","/",$_GET['PATH']); // data--image -> data/image
	$files = file_get_contents('./filemanager.php');
	$files = str_replace("__current_path__",$myPath,$files);
	file_put_contents($target,$files);
} else {
	exit("Abnormal approach!");
}
header("Location: $target");

// if ($member['mb_id'] == 'manager') {
	// $target = "./fm_".$_GET['ID'].".php";
	// if (!file_exists($target)) {
		// $myPath = "data/image/".$_GET['ID'];
		// $files = file_get_contents('./filemanager.php');
		// $files = str_replace("__current_path__",$myPath,$files);
		// file_put_contents($target,$files);
	// }
// } else if($member['mb_id'] == 'its') { //  로그인 ID가 its 이면
	// $target = "./fm_its.php";
	// if (!file_exists($target)) {
		// $myPath = "";
		// $files = file_get_contents('./filemanager.php');
		// $files = str_replace("__current_path__",$myPath,$files);
		// file_put_contents($target,$files);
	// }
// } else {
	// exit("Abnormal approach!");
// }

// header("Location: $target");
?>