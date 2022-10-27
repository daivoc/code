<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// Optex BSS Series 신규 작업인 경우 기본값을 설정 한다.
// Optex Microwave Sensor BSS01 Area Type

//// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
$Event_read_cycle = 1.5; // Sec

$MAX_event_holdTime = 1000000; // 최대 이밴트 허용 횟수
$MAX_event_pickTime = 1000000; // 이밴트 픽업 주기 micro sec

$MAX_numberOfDist = 5000; // mm 감지 최대 길이 미리미터 
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

//// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
?>