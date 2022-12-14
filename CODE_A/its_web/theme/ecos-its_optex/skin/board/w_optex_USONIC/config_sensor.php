<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// Optex BSS Series 신규 작업인 경우 기본값을 설정 한다.
// Optex Microwave Sensor BSS01 Area Type

//// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
$Event_read_cycle = 1.5; // Sec

$MAX_event_cycle = 5000; // 이벤트 픽업 주기
$MAX_event_holdTime = 10; // 연속적인 유효 이벤트 갯수 (횟수)
$MAX_event_pickTime = 60; // 유효 이벤트감지를 위한 대기 시간 (초)

$MAX_numberOfDist = 10000; // mm 감지 최대 길이 미리미터 
$MAX_numberOfZone = 1; // GPIO는 하나에 지역임
$MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // 단위 분할 수

$SYSTEM_port = G5_CU_MASTER_PORT;

$DEVICE_IP = '192.168.168.30';
$DEVICE_port = '6000';
$DEVICE_vPort = '4000';

$DEVICE_email_Addr = '';
$DEVICE_email_Time = '08:30';
$DEVICE_table_PortIn = '8000';
$DEVICE_table_PortOut = '9000';

$DEVICE_alert = array( // Alert
	18 => 'Alert_01',
	23 => 'Alert_02',
	24 => 'Alert_03',
	25 => 'Alert_04',
	// 6 => 'Alert_05',
	// 7 => 'Alert_06',
	// 8 => 'Alert_07',
	// 9 => 'Alert_08'
);

$DEVICE_input = array( // Read
	19 => 'Relay_01',
	13 => 'Relay_02',
	6 => 'Relay_03',
	5 => 'Relay_04',
	22 => 'Relay_05',
	27 => 'Relay_06',
	17 => 'Relay_07',
	4 => 'Relay_08'
);

//// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
?>