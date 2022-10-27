<?php
shell_exec('sleep 1 && sudo /sbin/reboot > /dev/null 2>/dev/null &');
header('Location: ' . $_SERVER['HTTP_REFERER']);
?>
