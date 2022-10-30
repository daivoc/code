<?php
$host = strip_tags($_POST['host']);
$customer = strip_tags($_POST['customer']);
$authKey = strip_tags($_POST['authKey']);
$cpuID = strip_tags($_POST['cpuID']);

$license = hash("sha256", $cpuID.$authKey);

echo $license;

// $port = 80; 
// $waitTimeoutInSeconds = 1; 
// if($fp = fsockopen($host,$port,$errCode,$errStr,$waitTimeoutInSeconds)){   
// 	echo $license;
// } else {
// 	echo "The license server could not be reached.";
// } 
// fclose($fp);

die();
?>