<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// /etc/sudoers:
// echo 'Reset System Clock - '.$_POST["now_dateTime"];

// $_SERVER['REMOTE_ADDR']

// $command_is = "sudo sed -i -e 's/".$_SERVER['HTTP_HOST']."/".$_POST["new_ipaddress"]."/g' /etc/network/interfaces";
// // $output = shell_exec($command_is);
// echo shell_exec($command_is);
// echo exec($command_is);
// echo system($command_is);
// echo "<pre>$command_is</pre>";
// echo "<pre>$output</pre>";

header("location:javascript://history.go(-1)");
?>