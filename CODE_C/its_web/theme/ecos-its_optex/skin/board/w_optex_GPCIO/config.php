<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

$relay_alert = array( // Alert
	18 => 'Alert_01',
	23 => 'Alert_02',
	24 => 'Alert_03',
	25 => 'Alert_04'
);

$relay_inputL = array( // Read
	19 => 'Relay_01',
	13 => 'Relay_02',
	6 => 'Relay_03',
	5 => 'Relay_04'
);
$relay_inputR = array( // Read
	22 => 'Relay_05',
	27 => 'Relay_06',
	17 => 'Relay_07',
	4 => 'Relay_08'
);

$opject_direction = array( //
	1 => '🡢 L : R 🡢',
	2 => '🡠 L : R 🡠',
	9 => '🡠 Both 🡢'
);

$event_status = array( // Read
	0 => 'NORMAL',
	1 => 'EVENT',
	2 => 'HEARTBEAT',
	3 => 'RESERVED',
	4 => 'RESERVED',
	5 => 'RESERVED',
	6 => 'RESERVED',
	7 => 'RESERVED',
	8 => 'ERR_COVER',
	9 => 'ERR_EVENT'
);
?>