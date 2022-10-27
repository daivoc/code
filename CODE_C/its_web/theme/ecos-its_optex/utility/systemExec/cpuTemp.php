<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// measure_temp

echo shell_exec('/usr/bin/python /home/pi/utility/cpuTemp.pyc');
?>