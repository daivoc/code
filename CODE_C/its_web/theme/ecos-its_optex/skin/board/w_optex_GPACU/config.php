<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

$sensor_model = array( //  모델명은 그 자체가 제품 관련 프로그램 명으로 사용됨
	'', 
	'RLS-3060L', 
	'RLS-3060SH', 
	'RLS-22020I', 
	'RLS-2020S', 
	'BSS01-K', 
	'BSS01-KR', 
	'BSS200', 
	'FD-322', 
	'FD-535R', 
	'Outdoor PIR', 
	'Indoor PIR',
	'Active Infrared', 
	'Long Range PIR', 
	'CK-10', 
	'Other' 
);

$relay_alert = array( // Alert
	18 => 'Alert_01',
	23 => 'Alert_02',
	24 => 'Alert_03',
	25 => 'Alert_04',
	// 6 => 'Alert_05',
	// 7 => 'Alert_06',
	// 8 => 'Alert_07',
	// 9 => 'Alert_08'
);

$relay_input = array( // Read
	19 => 'Relay_01',
	13 => 'Relay_02',
	6 => 'Relay_03',
	5 => 'Relay_04',
	22 => 'Relay_05',
	27 => 'Relay_06',
	17 => 'Relay_07',
	4 => 'Relay_08'
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