<?php
$host = strip_tags($_POST['host']);
$customer = strip_tags($_POST['customer']);
$authKey = strip_tags($_POST['authKey']);
$device = strip_tags($_POST['device']);
$serial = strip_tags($_POST['serial']);
$cpuID = strip_tags($_POST['cpuID']);
$license = hash("sha256", $cpuID.$device.$authKey); // 순서 중요함

$port = 80; 
$waitTimeoutInSeconds = 1; 
if($fp = fsockopen($host,$port,$errCode,$errStr,$waitTimeoutInSeconds)){   
	echo $license;
} else {
	echo "The license server could not be reached.";
} 
fclose($fp);

// $host = "localhost";
// $user = "its";
// $pass = "GXnLRNT9H50yKQ3G";
// $name = "its_web";

// // Create connection
// $conn = new mysqli($host, $user, $pass, $name);
// // Check connection
// if ($conn->connect_error) {
    // die("Connection failed: " . $conn->connect_error);
// }

// $sql = "INSERT INTO w_its_license (customer, authKey, device, serial, cpuID, license) VALUES ($customer, $authKey, $device, $serial, $cpuID, $license)";

// $conn->query($sql);
// $conn->close();
die();
?>