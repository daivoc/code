<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

$MIN_RCS = 0;
$MAX_RCS = 999;
// Optex REDSCAN Series 신규 작업인 경우 기본값을 설정 한다.
// Optex Laser SensorREDSCAN

// //// 매우 중요함 config_sensor.py에 같은 값이 꼭 있어야 함 ///////////////////////
$MAX_event_holdTime = 100; // config_sensor.py// 최대 이밴트 허용 횟수 : 1회 =~ 0.1초
$MAX_event_pickTime = 3000; // config_sensor.py// mSec 

// $MAX_numberOfZone = 5; // 미터  
// $MAX_numberOfDist = $MAX_numberOfZone * 1000; // mm 감지 최대 길이 미리미터 
// $MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // 단위 분할 수
// $MAX_event_offset = 500; // 센치미터

$SYSTEM_port = G5_CU_MASTER_PORT;
$SYSTEM_nodeIn = G5_CU_SYSTEM_PORT_IN;
$SYSTEM_nodeOut = G5_CU_SYSTEM_PORT_OUT;
	// varPort = int(sensor_IP.split('.')[2]) + int(sensor_IP.split('.')[3])
	// nodeIn = 50000 + varPort # sensor_IP = '192.168.168.30' -> 50168
	// nodeOut = 51000 + varPort # sensor_IP = '192.168.168.30' -> 51168

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