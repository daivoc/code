<?php
if($_POST['w_sensor_serial']) { // Optex Model
	$tmpLog = "/var/www/html/its_web/data/log/".$_POST['w_sensor_serial'].".log";
} else if ($_POST['w_device_serial']) { 
	$tmpLog = "/var/www/html/its_web/data/log/".$_POST['w_device_serial'].".log";
} else if ($_POST['w_camera_serial']) { 
	$tmpLog = "/var/www/html/its_web/data/log/".$_POST['w_camera_serial'].".log";
} else { 
	exit("Abnormal approach!");
}
$windowTitle = $_POST['wr_subject'];

function tailFile ($filepath,$lines=1){
	return trim(implode("",array_slice(file($filepath),-$lines)));
}

if(file_exists($tmpLog)) {
	$logTails = tailFile($tmpLog,256);
	// 실시간 보기
	// echo "<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>$windowTitle</title><meta name='viewport' content='width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes'></head><body><pre id='endOfLine' style='font-size:6pt;'>$logTails</pre></body><script>window.setTimeout(function () { window.location.reload(); }, 1000);</script></html>";
	// 새로고침 보기
	echo "<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>$windowTitle</title><meta name='viewport' content='width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes'></head><body id='content'><pre id='endOfLine' style='font-size:6pt;'>$logTails</pre><hr></body><script>document.getElementById('content').scrollIntoView(false)</script></html>";
} else {
	echo "<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>HTML Reference</title><meta name='viewport' content='width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes'></head><body><div style='font-size:10pt'>Not found realtime log. </div>관련한 센서의 실시간 로그 파일이 존재하지 않습니다.</body></html>";
}
?>
