<?php
if (!defined('_GNUBOARD_')) exit; // ���� ������ ���� �Ұ�

// Optex REDSCAN Series �ű� �۾��� ��� �⺻���� ���� �Ѵ�.
// Optex Laser SensorREDSCAN

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
$MAX_event_holdTime = 100; // config_sensor.py// �ִ� �̹�Ʈ ��� Ƚ�� : 1ȸ =~ 0.1��
$MAX_event_pickTime = 3000; // config_sensor.py// mSec 

$MAX_numberOfSensor = 8; // �ִ� ��ġ������ ���� ��� ���� 8��

$MAX_numberOfZone = 5; // ����  
$MAX_numberOfDist = $MAX_numberOfZone * 1000; // mm ���� �ִ� ���� �̸����� 
$MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // ���� ���� ��
$MAX_event_offset = 500; // ��ġ����

$SYSTEM_port = G5_CU_MASTER_PORT;
$SYSTEM_nodeIn = G5_CU_SYSTEM_PORT_IN;
$SYSTEM_nodeOut = G5_CU_SYSTEM_PORT_OUT;

	// varPort = int(sensor_IP.split('.')[2]) + int(sensor_IP.split('.')[3])
	// nodeIn = 50000 + varPort # sensor_IP = '192.168.168.30' -> 50168
	// nodeOut = 51000 + varPort # sensor_IP = '192.168.168.30' -> 51168

// $DEVICE_vIP = '192.168.168.10';
// $DEVICE_vPort = '4000';
$DEVICE_IP = '192.168.0.126';
$DEVICE_port = '50001';

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

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
?>