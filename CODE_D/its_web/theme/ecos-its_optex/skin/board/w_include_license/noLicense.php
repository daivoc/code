<?php
// 메인설정 파일에서 라이센스 서버 정보 추출
$jsonFile = "/home/pi/common/config.json";
$fOpen = fopen($jsonFile, "r") or die("Unable to open common/config.json");
$fRead = fread($fOpen,filesize($jsonFile));
fclose($fOpen);
$share = json_decode($fRead, TRUE)["license"];
$license = explode(":", $share["server_addr"]);
$host = $license[0]; 
$port = (int)$license[1]; 
if(!$port) $port = 80;
$waitTimeoutInSeconds = 1;
// 온라인 테스트 후 전송 버튼 유무 결정
if($fp = fsockopen($host,$port,$errCode,$errStr,$waitTimeoutInSeconds)){
    $licenseServer = $share["server_url"]."/licenseSrvAdd.php";
    $submitBtn = "<input class='submit' type='submit' value='Submit'>";
} else {
    $licenseServer = "";
    $submitBtn = "";
} 
fclose($fp);

?>
<html>
<head>
<style>
    textarea {width:100%; height:240px;}
    .submit { position: absolute;top: 20px;right: 20px; }
</style>
</head>
<body>
<div style="padding: 10px;color: gray;border: 1px solid silver;font-weight: bold;font-size: 14pt;">License Info.</div>
<?php
exec("pgrep -f watchdog.pyc", $output, $retval);
// print count($output); // 존재하면 2 또는 이상, 없으면 1
if(count($output) > 1) {
    $jsonFile = "/home/pi/.config/watchdog.json";
    $wdFile = fopen($jsonFile, "r") or die("Abnormal State, Call Administrator!");
    $watchDog = fread($wdFile,filesize($jsonFile));
    fclose($wdFile);

    $textarea = "";
    $jsonIterator = new RecursiveIteratorIterator(
        new RecursiveArrayIterator(json_decode($watchDog, TRUE)["fixed"]),
        RecursiveIteratorIterator::SELF_FIRST);
        
    echo "<form method='post' action='$licenseServer'>";
    foreach ($jsonIterator as $key => $val) {
        if(is_array($val)) {
            $textarea .= "$key:\n";
        } else {
            $textarea .= "$key : $val\n";
            echo "<input id='$key' type='hidden' name='$key' readonly value='$val'>";
        }
    }
    // 보안상에 이유로 커멘트 처리함
    // echo "$submitBtn</form>";
    echo "<textarea readonly disabled>$textarea</textarea>";
} else {
    echo "<div>Abnormal State, Call Administrator!</div>";
    echo "<div>Try Reboot System</div>";
}
?>

</body>
</html>