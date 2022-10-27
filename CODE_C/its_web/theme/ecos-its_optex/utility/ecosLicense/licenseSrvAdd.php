<?php
include_once('./_common.php');
// if ($is_guest) { exit("Abnormal approach!"); }
// 본프로그램은 서버단에서 실행 됩니다.
// licenseSrvAdd.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvCSV.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvList.php는 라이센스서버에 상주하는 프로그램 명이다.
// 본 프로그램을 통해 ITS 라이센스 정보를 데이터베이스에 등록한다.
// 클라이언트측 G:\Development\ecos_ITS\its_utility\licenseKey.py 와 연계됨

if($_POST["systemTitle"]){
    $customer = $_POST["systemTitle"]; // 회사명
} else {
    $customer = ""; // 회사명
}
$subject = $_POST["run"]; // 실행하는 프로그램
$cpuID = $_POST["serialKey"]; // CPU or Mac ID
$serial = "";
$status = $_POST["licenseStatus"];
$device = $_POST["ioBoard"];
$remoteAddr = $_SERVER['REMOTE_ADDR'].":".$_POST['ipAddr'];
$expiry = 36; // 계약 종료일

$license = hash('sha256', $cpuID . hash('sha256', $customer));

$date = new DateTime();
$date->modify('+'.$expiry.' month');
$expiry = $date->format('Y-m-d H:i:s');

$sql = " insert into w_its_license
    set customer = '$customer',
        subject = '$subject',
        cpuID = '$cpuID',
        serial = '$serial',
        status = '$status',
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

echo "<script>window.close();</script>";
?>