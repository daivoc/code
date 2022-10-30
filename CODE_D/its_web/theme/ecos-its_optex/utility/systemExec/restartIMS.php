<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// echo "Restarting IMS ...";
$output = shell_exec('/usr/bin/python /home/pi/MONITOR/run_itsmon.pyc');
echo "<pre>$output</pre>";
?>