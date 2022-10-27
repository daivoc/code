<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// /etc/sudoers:
// www-data ALL=(root) NOPASSWD: /sbin/reboot 

// restart.php
// exec('sudo /sbin/reboot');

// <h3>Restart</h3>
// <p>
// <form action="restart.php" method="get">
  // <input type="submit" value="Press me.">
// </form>
// </p>


echo "<br>";
echo "Restarting wits...";
exec('sudo /usr/bin/python /home/pi/dnd/wits_dnd_db.pyc > /tmp/witDndDB.txt');
?>