<?php
if (!defined('_GNUBOARD_')) exit; // ���� ������ ���� �Ұ�

// Optex BSS Series �ű� �۾��� ��� �⺻���� ���� �Ѵ�.
// Optex Microwave Sensor BSS01 Area Type

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
$Event_read_cycle = 1.5; // Sec

$MAX_event_holdTime = 1000000; // �ִ� �̹�Ʈ ��� Ƚ��
$MAX_event_pickTime = 1000000; // �̹�Ʈ �Ⱦ� �ֱ� micro sec

$MAX_numberOfDist = 5000; // mm ���� �ִ� ���� �̸����� 
$MAX_numberOfZone = 1; // GPIO�� �ϳ��� ������
$MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // ���� ���� ��

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

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
?>