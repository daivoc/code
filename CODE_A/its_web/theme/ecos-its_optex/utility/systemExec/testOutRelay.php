<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// 센서전원(12v)을 일시적으로 차단(Reset)한다.
// # 변경 
// # $ sudo chmod 666 /dev/gpiomem

echo shell_exec('/usr/bin/python /home/pi/utility/check_Relay.pyc 3');
?>