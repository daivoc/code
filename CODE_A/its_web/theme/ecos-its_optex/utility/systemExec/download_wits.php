<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// echo "<br>";
// echo "Download wits programs...";
$output = shell_exec('/home/pi/dnd/download_wits.sh > /dev/null 2>/dev/null &');
// echo "<pre>$output</pre>";

header("location:javascript://history.go(-1)");
?>