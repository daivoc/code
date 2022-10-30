<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// // Optimize Database
// $output = shell_exec('mysqlcheck -uits -pGXnLRNT9H50yKQ3G --optimize its_web  > /tmp/db_optimize');
// echo "<pre>$output</pre>";

// echo "Restarting server...";
$output = shell_exec('sudo /sbin/reboot > /dev/null 2>/dev/null &');
?>