<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// /etc/sudoers:
// www-data ALL=(root) NOPASSWD: /sbin/date 
// echo 'Reset System Clock - '.$_POST["now_dateTime"];
$command_is = "sudo /bin/date -s '".$_POST["now_dateTime"]."'";
$output = shell_exec($command_is);
// echo "<pre>$output</pre>";

// header("location:javascript://history.go(-1)");
header('Location: ' . $_SERVER['HTTP_REFERER']);
?>