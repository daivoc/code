<?php
if (!defined('_GNUBOARD_')) exit; // ���� ������ ���� �Ұ�

// Optex BSS Series �ű� �۾��� ��� �⺻���� ���� �Ѵ�.
// Optex Microwave Sensor BSS01 Area Type

//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
$MAX_event_holdTime = 10; // �ִ� �̹�Ʈ ��� Ƚ�� : 1ȸ =~ 0.1��
$MAX_event_pickTime = 10; // km
$MIN_event_speed = 11; // ���ӵ�
$MAX_event_speed = 199; // ���ӵ�

$MAX_numberOfZone = 100; // ��ü ���� ���� ��
$MAX_numberOfDist = $MAX_numberOfZone * 1000; // mm ���� �ִ� ���� �̸����� 
$MAX_stepOfZone = round($MAX_numberOfDist / $MAX_numberOfZone); // ���� ���� ��
$MAX_event_offset = 499; // ��ġ����
$MAX_event_spot = 999; // �̸�����, ������ ��ġ ��� ���� MAX_event_syncDist = 4000 ���� �Ÿ��� �� ������ �Ÿ��� ���� �� 1m = 100 

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


//// �ſ� �߿��� config_sensor.py�� ���� ���� �� �־�� �� ///////////////////////
?>