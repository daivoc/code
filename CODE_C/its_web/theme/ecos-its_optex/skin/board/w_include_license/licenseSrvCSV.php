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

$list_body = '';
$result = sql_query("SHOW COLUMNS FROM ". base64_decode($license_tbl_name)); 
while ($row = sql_fetch_array($result)) { 
  $list_body .= '"'.$row['Field'].'",';
}
$list_body .= "\n";
$sql = base64_decode($sqlCountRow);
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
    foreach ($row as $col_value) {
        $list_body .= '"'.$col_value.'",';
	}
	$list_body .= "\n";
}

header("Content-Type: application/octet-stream");
header("Content-Disposition: attachment; filename=export.csv");
print "$list_body";
?>
