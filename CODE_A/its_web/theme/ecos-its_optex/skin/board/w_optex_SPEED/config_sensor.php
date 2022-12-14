<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// Optex BSS Series 신규 작업인 경우 기본값을 설정 한다.
// Optex Microwave Sensor BSS01 Area Type

//// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
$MAX_event_holdTime = 10; // 최대 이밴트 허용 횟수 : 1회 =~ 0.1초
$MAX_event_pickTime = 10; // km
$MIN_event_speed = 11; // 허용속도
$MAX_event_speed = 199; // 허용속도

$MAX_numberOfZone = 100; // 전체 지역 분할 수
$MAX_numberOfDist = $MAX_numberOfZone * 1000; // mm 감지 최대 길이 미리미터 
$MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // 단위 분할 수
$MAX_event_offset = 499; // 센치미터
$MAX_event_spot = 999; // 미리미터, 동일한 위치 허용 범위 MAX_event_syncDist = 4000 이전 거리와 비교 동일한 거리로 간주 함 1m = 100 

$SYSTEM_port = G5_CU_MASTER_PORT;

$DEVICE_vIP = '192.168.168.10';
$DEVICE_vPort = '4000';
$DEVICE_IP = '192.168.168.30';
$DEVICE_port = '6000';

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