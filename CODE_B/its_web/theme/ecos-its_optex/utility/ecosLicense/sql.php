<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가

$sql = "CREATE TABLE IF NOT EXISTS `w_its_license` (
 `l_id` int(11) NOT NULL AUTO_INCREMENT,
 `customer` varchar(32) NOT NULL default '',
 `subject` varchar(32) NOT NULL default '',
 `cpuID` varchar(32) NOT NULL default '',
 `serial` varchar(32) NOT NULL default '',
 `status` varchar(32) NOT NULL default '',
 `device` varchar(32) NOT NULL default '',
 `license` varchar(64) NOT NULL default '',
 `remoteAddr` varchar(32) NOT NULL default '',
 `stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 `expiry` DATETIME, 
 PRIMARY KEY (`l_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8";

sql_query($sql, false);

$sql = "CREATE TABLE IF NOT EXISTS `w_its_license_index` (
 `cpuID` varchar(32) NOT NULL default '',
 `l_id` int(11) NOT NULL default '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8";

sql_query($sql, false);
