<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// 센서전원(12v)을 일시적으로 차단(Reset)한다.
// # 변경 
// # $ sudo chmod 666 /dev/gpiomem
// $command_is = "sudo sed -i -e 's/".$_SERVER['HTTP_HOST']."/".$_POST["new_ipaddress"]."/g' /etc/network/interfaces";
// // $output = shell_exec($command_is);
// echo shell_exec($command_is);
// echo exec($command_is);
// echo system($command_is);
// echo "<pre>$command_is</pre>";
// echo "<pre>$output</pre>";
echo $_GET["myID"];
echo $_GET["myCommand"];
// echo shell_exec('/usr/bin/python /home/pi/optex_RLS_R/run_optex.pyc');
?>