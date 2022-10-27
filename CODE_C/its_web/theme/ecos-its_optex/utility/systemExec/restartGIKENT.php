<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

$output = shell_exec('/usr/bin/python /home/pi/GIKENT/run_GILENT.pyc');
// $output = shell_exec('/bin/sh /home/pi/GIKENT/run');
// $output = exec('sudo /usr/bin/python /home/pi/GIKENT/run_GILENT.pyc');
// $output = exec('sudo /bin/sh /home/pi/GIKENT/run');
echo "<pre>$output</pre>";
?>