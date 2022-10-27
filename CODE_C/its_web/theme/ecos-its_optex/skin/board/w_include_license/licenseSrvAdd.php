<?php
include_once('./_common.php');
// if ($is_guest) { exit("Abnormal approach!"); }
// 본프로그램은 서버단에서 실행 됩니다.
// licenseSrvAdd.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvCSV.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvList.php는 라이센스서버에 상주하는 프로그램 명이다.
// 본 프로그램을 통해 ITS 라이센스 정보를 데이터베이스에 등록한다.
// 위치는 theme.config.php내 G5_CU_LICENSE_URL이 결정한다.
// 예 : define('G5_CU_LICENSE_URL', 'http://'.G5_CU_LICENSE_SERVER.'/ecosLicense');
// 데이터베이스 구성은 아래와 같으며 사전에 테이블 구성이 되어있어야 한다.
// 본 데이터베이스에 'system license' 등록은 제외되며
// application license 만 등록하는것을 원칙으로 한다.
// 각각의 스킨의 write_update.skin.php에서 include licenseSrv.php 실행 된다.

$customer = $_POST['customer'];
$subject = $_POST['subject'];
$cpuID = $_POST['cpuID'];
$serial = $_POST['serial'];
$device = $_POST['device'];
$license = $_POST['license'];
$remoteAddr = $_SERVER['REMOTE_ADDR'].":".$_POST['remoteAddr'];

if ($customer && $cpuID && $serial && $device) {
	// 일차하는 레코드 검색
	$sql = " SELECT count(*) as cnt, l_id FROM w_its_license WHERE customer = '$customer' AND cpuID = '$cpuID' AND serial = '$serial' AND device = '$device' AND license = '$license' LIMIT 1; ";
	$row = sql_fetch($sql);
	if (!$row['cnt']) {
		$date = new DateTime();
		$date->modify('+'.$_POST['expiry'].' month');
		$expiry = $date->format('Y-m-d H:i:s');

		$sql = " insert into w_its_license
			set customer = '$customer',
				subject = '$subject',
				cpuID = '$cpuID',
				serial = '$serial',
				device = '$device',
				license = '$license',
				remoteAddr = '$remoteAddr',
				expiry = '$expiry' ";
		sql_query($sql);

		$l_id = sql_insert_id();

		$sql = " insert into w_its_license_index
			set cpuID = '$cpuID',
				l_id = '$l_id' ";
		sql_query($sql);
		// echo $l_id;
	} else {
		// echo $row['l_id'];
	}
} else {
	// echo "$customer && $cpuID && $serial && $device";
}

?>