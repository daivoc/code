<?php
if (!defined('_GNUBOARD_')) exit; // ���� ������ ���� �Ұ�

// Optex REDSCAN Series �ű� �۾��� ��� �⺻���� ���� �Ѵ�.
// Optex Laser SensorREDSCAN

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
$MAX_event_holdTime = 100; // config_sensor.py// �ִ� �̹�Ʈ ��� Ƚ�� : 1ȸ =~ 0.1��
$MAX_event_pickTime = 3000; // config_sensor.py// mSec 

$MAX_numberOfZone = 8; // ��ü ���� ���� ��
$MAX_numberOfDist = $MAX_numberOfZone * 1000; // mm ���� �ִ� ���� �̸����� 
$MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // ���� ���� ��
$MAX_event_offset = 500; // ��ġ����

$SYSTEM_port = G5_CU_MASTER_PORT;

$DEVICE_vIP = '192.168.168.10';
$DEVICE_vPort = '4000';

$SENSOR_IP_1 = '192.168.168.30';
$SENSOR_port_1 = '';
$SENSOR_IP_2 = '';
$SENSOR_port_2 = '';

$DEVICE_email_Addr = '';
$DEVICE_email_Time = '';
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


$RLS_map_LA[4] = 'A11'; // ['A11'] = 4
$RLS_map_LA[5] = 'A12'; // ['A12'] = 5
$RLS_map_LA[6] = 'A21'; // ['A21'] = 6
$RLS_map_LA[7] = 'A22'; // ['A22'] = 7
$RLS_map_LA[3] = 'B11'; // ['B11'] = 3
$RLS_map_LA[2] = 'B12'; // ['B12'] = 2
$RLS_map_LA[1] = 'B21'; // ['B21'] = 1
$RLS_map_LA[0] = 'B22'; // ['B22'] = 0

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
?>