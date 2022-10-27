<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가

///////////////////////
// 일시적 사용중지
///////////////////////
return;

/*
$sql = "CREATE TABLE IF NOT EXISTS `w_its_license` (
 `l_id` int(11) NOT NULL AUTO_INCREMENT,
 `customer` varchar(32) NOT NULL default '',
 `subject` varchar(32) NOT NULL default '',
 `cpuID` varchar(32) NOT NULL default '',
 `serial` varchar(32) NOT NULL default '',
 `status` varchar(32) NOT NULL default '',
 `device` varchar(32) NOT NULL default '',
 `license` varchar(64) NOT NULL default '',
 `remoteAddr` varchar(32) NOT NULL default '',
 `stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 `expiry` DATETIME,
 `int_01` int(11) NOT NULL default '0',
 `int_02` int(11) NOT NULL default '0',
 `int_03` int(11) NOT NULL default '0',
 `int_04` int(11) NOT NULL default '0',
 `chr_01` varchar(16) NOT NULL default '',
 `chr_02` varchar(16) NOT NULL default '',
 `chr_03` varchar(16) NOT NULL default '',
 `chr_04` varchar(16) NOT NULL default '',
 PRIMARY KEY  (`l_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8";

$sql = "CREATE TABLE IF NOT EXISTS `w_its_license_index` (
 `cpuID` varchar(32) NOT NULL default '',
 `l_id` int(11) NOT NULL default '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8";
*/


/* 
라이센스 등록 
https://stackoverflow.com/questions/5647461/how-do-i-send-a-post-request-with-php
*/

// expiry = 개월수
$url = G5_CU_LICENSE_URL.'/licenseSrvAdd.php';
$data = array('customer' => $member['mb_10'], 'subject' => $board['bo_subject'], 'cpuID' => $w_cpu_id, 'serial' => $w_sensor_serial, 'status' => $w_sensor_status, 'device' => $w_device_id, 'license' => $w_license, 'remoteAddr' => $_SERVER['REMOTE_ADDR'], 'expiry' => 24);

// use key 'http' even if you send the request to https://...
$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data)
    )
);
$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
if ($result === FALSE) {
	alert("Error License Server. ".$result);
} else {
	// alert("Success. ".$result.$url.$context);
}

