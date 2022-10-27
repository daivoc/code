<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// USB 드라이버 관련 device port
global $g5, $bo_table;

// 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)
$select_w_sensor_devID = '<select name="w_sensor_devID" id="w_sensor_devID" required class="form-control required" style=" margin-bottom: 4px;" placeholder="Select Sensor" ><option value="0" disabled selected>Select Sensor</option>';

// Optex BSS 목록
$bo_table_info = G5_CU_CONF_BSS;
// 목록보기 링크
$write_table = $g5['write_prefix'] . $bo_table_info;
$sql = " SELECT * FROM $write_table WHERE w_sensor_disable = '0' ORDER BY w_device_id ASC ";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$value_select = "?commType=BSS&devideID=".$row['w_device_id']."&sensorID=".$row['w_sensor_serial']."&subject=".$row['wr_subject'];
	if($subject == $row['wr_subject'])
		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	else
		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
}

$bo_table_name = G5_CU_CONF_RXTX;
// 목록보기 링크
$write_table = $g5['write_prefix'] . $bo_table_name;
$sql = " SELECT * FROM $write_table WHERE wr_10 = 'Enable' ORDER BY w_device_id ASC";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$value_select = "?commType=ttyUSB&devideID=".$row['w_device_id']."&sensorID=".$row['w_sensor_id']."&wr_id=".$row['wr_id']."&w_alarm_level=".$row['w_alarm_level']."&subject=".$row['wr_subject'];
	if($subject == $row['wr_subject'])
		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	else
		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
}

$bo_table_relay_info = G5_CU_CONF_RELAY;
// 목록보기 링크
$write_table = $g5['write_prefix'] . $bo_table_relay_info;
$sql = " SELECT * FROM $write_table WHERE wr_10 = 'Enable' ORDER BY w_device_id ASC";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$value_select = "?commType=GPIO&sensorID=".$row['w_sensor_id']."&wr_id=".$row['wr_id']."&w_alarm_level=".$row['w_alarm_level']."&subject=".$row['wr_subject'];
	if($subject == $row['wr_subject'])
		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	else
		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
}

$select_w_sensor_devID .= '</select>';

// echo $select_w_sensor_devID;
if($commType) { // org $commType && $sensorID
	if($commType == 'ttyUSB')
		$bo_table_name = 'w_log_sensor_'.end(explode('/',$devideID)).'_'.$sensorID;
	elseif($commType == 'GPIO')
		$bo_table_name = 'w_log_sensor_GPIO_'.$sensorID;
	// $bo_table_name = 'w_log_sensor_'.end(explode('/',$devideID)).'_'.$sensorID;
	// 목록보기 링크
	// USB 드라이버 관련 device port
	if($dueFrom && $dueTo) {
		$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) - 1);
		if($dueFrom > $dueTo) { // 스와핑
			$dueToTmp = $dueFrom;
			$dueFrom = $dueTo;
			$dueTo = $dueToTmp;
		}
		$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
		if($dueFrom == $dueTo) {
			$due = '1d'; // 하루인 경우 1d로 설정
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - $dueFrom ~ $dueToTmp\\n $dueFrom ~ $dueToTmp";
		} else {
			$due = ''; // 하루인 아닌 경우
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 $dueFrom ~ $dueToTmp 동안의 이벤트의 분단위 통계\\n $dueFrom ~ $dueToTmp";
		}
	} else if($due){
		$nowDatetime = date('Y-m-d H:i:s');
		if($due == '1h') {
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-1 hour'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 한시간 동안의 이벤트의 분단위 통계\\n $dueDatetime ~ $nowDatetime";
		} else if($due == '1d') { 
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-1 day'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 24시간 동안의 이벤트의 분단위 통계\\n $dueDatetime ~ $nowDatetime";
		} else if($due == '1w') { 
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-1 week'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 한 주간 일간 이벤트의 시간대별 통계\\n $dueDatetime ~ $nowDatetime";
		} else if($due == '1m') { 
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-1 month'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 한 달간 일간 이벤트의 시간대별 통계\\n $dueDatetime ~ $nowDatetime";
		} else if($due == '3m') { 
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-3 month'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 3개월간 주간 이벤트의 시간대별 통계\\n $dueDatetime ~ $nowDatetime";
		} else if($due == '6m') { 
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-6 month'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY YEARWEEK(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY YEARWEEK(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY YEARWEEK(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY YEARWEEK(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 6개월간 주간 이벤트의 시간대별 통계\\n $dueDatetime ~ $nowDatetime";
		} else if($due == '1y') { 
			$dueDatetime = date('Y-m-d H:i:s', strtotime('-1 year'));
			$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId > '0' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MONTH(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_appear = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '1' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MONTH(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_move = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId >= '3' AND w_eventId <= '4' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MONTH(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$sql_positive = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_eventId = '11' AND w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY MONTH(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
			$titleIs = " - 지난 1년간 월간 이벤트의 시간대별 통계\\n $dueDatetime ~ $nowDatetime";
		}
		
		// $sql = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' ORDER BY w_id ASC; ";
		// $sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' GROUP BY hour( w_stamp ) , day( w_stamp ); ";
	} else {
		$sql = '';
	}

	$result = sql_query($sql);
	$num_rows = sql_num_rows($result); // 자료 갯수
	if($num_rows) { // 자료가 존재 하면
		$chartData_0 = "['ID', 'Date', 'Hour/Min', 'Location', 'Count'],";
		$subjectChart = "접근 감지";
		while ($row = sql_fetch_array($result)) {
			list($dateIs, $timeIs) = explode(' ', $row['Time']);
			list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
			$monthIs--;
			list($hIs, $mIs, $sIs) = explode(':', $timeIs);
			if($due == '1h') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.", ".$mIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1d') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1w' || $due == '1m') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1y') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			}
			// $chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
		}
		
		$result_appear = sql_query($sql_appear);
		$subjectChart = "움직임 감지";
		while ($row = sql_fetch_array($result_appear)) {
			list($dateIs, $timeIs) = explode(' ', $row['Time']);
			list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
			$monthIs--;
			list($hIs, $mIs, $sIs) = explode(':', $timeIs);
			if($due == '1h') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.", ".$mIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1d') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1w' || $due == '1m') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1y') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			}
			// $chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
		}
		$result_move = sql_query($sql_move);
		$subjectChart = "이동/차단 감지";
		while ($row = sql_fetch_array($result_move)) {
			list($dateIs, $timeIs) = explode(' ', $row['Time']);
			list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
			$monthIs--;
			list($hIs, $mIs, $sIs) = explode(':', $timeIs);
			if($due == '1h') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.", ".$mIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1d') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1w' || $due == '1m') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1y') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			}
			// $chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
		}
		$result_positive = sql_query($sql_positive);
		$subjectChart = "활성";
		while ($row = sql_fetch_array($result_positive)) {
			list($dateIs, $timeIs) = explode(' ', $row['Time']);
			list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
			$monthIs--;
			list($hIs, $mIs, $sIs) = explode(':', $timeIs);
			if($due == '1h') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.", ".$mIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1d') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$mIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1w' || $due == '1m') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else if($due == '1y') {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			} else {
				$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
				$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
			}
			// $chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
		}
	}
}
// echo $sql;
if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.php';
if($subject) $titleIs = $subject; else $titleIs = "Chart";
$board['bo_subject'] = $titleIs;
?>
<?php // href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css" ?>
<?php // src="//code.jquery.com/ui/1.11.4/jquery-ui.min.js" ?>
<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL ?>/jquery-ui.css">
<script src="<?php echo G5_THEME_JS_URL ?>/jquery-ui.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$(function(){ // 날짜 입력
		$("#item_date_fr").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
		$("#item_date_to").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
	});
	$('#item_date_fr,#item_date_to').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
		
	});	$('#w_sensor_devID').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&due=<?php if($due) echo $due; else echo '1w'; ?>", "_self");
	});
});
</script>
<?php if($num_rows) { // 자료가 존재 하면 ?>
<?php // src="https://www.gstatic.com/charts/loader.js" ?>
<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/loader.js"></script>
<script type="text/javascript">
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawSeriesChart);

	function drawSeriesChart() {

	var data_all = google.visualization.arrayToDataTable([
	<?php echo $chartData_0; ?>
	]);
	
	var options = {
	title: 'Time Line - Event <?php echo $titleIs ?>',
	hAxis: {title: 'Date/Time'},
	vAxis: {title: 'Hour/Min'},
	bubble: {textStyle: {fontSize: 11}}
	};

	var chart = new google.visualization.BubbleChart(document.getElementById('series_chart_div_all'));
	chart.draw(data_all, options);
	}
</script>
<?php } // 자료가 존재 하면 ?>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name"><?php echo $board['bo_subject'] ?><span class="sound_only"> 차트</span></span>
            <hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>
<style>
.list_body_tr { font-size: 8pt; text-align: center; }
.list_body_td { line-height:10px; padding:4px 0; }
</style>
<?php if($commType) { // org $commType && $sensorID ?>
<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
<?php echo $select_w_sensor_devID ?>
<input class="" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<input class="" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<!-- input type="button" value="1H" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1h", "_self");' -->
<input type="button" value="1D" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1d", "_self");'>
<input type="button" value="1W" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1w", "_self");'>
<input type="button" value="1M" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1m", "_self");'>
<!-- input type="button" value="3M" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=3m", "_self");' -->
<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./chart_positive.php?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "chart");'>Event Due</button>
<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./chart_error.php?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "chart");'>Event Error</button>
</div>
<div id="series_chart_div_all" style="width: 100%; height: 700px;"></div>
</div>

<?php } else { ?>

<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
<?php echo $select_w_sensor_devID ?>
</div>
<?php } ?>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>