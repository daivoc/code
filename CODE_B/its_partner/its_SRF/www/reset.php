<?php
copy("/home/pi/SRF/config.json", "/var/www/html/SRF/config/config.json");
chmod("/var/www/html/SRF/config/config.json", 0666);
header('Location: ' . $_SERVER['HTTP_REFERER']);
?>
