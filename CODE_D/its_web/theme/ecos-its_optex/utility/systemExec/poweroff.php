<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// /etc/sudoers:
// www-data ALL=(root) NOPASSWD: /sbin/poweroff 

// echo "Restarting server...";
$output = shell_exec('sudo /sbin/poweroff > /dev/null 2>/dev/null &');
// echo "<pre>$output</pre>";
?>