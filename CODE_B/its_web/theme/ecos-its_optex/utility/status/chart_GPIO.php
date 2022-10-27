<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// USB 드라이버 관련 device port
global $g5, $bo_table;

// 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)
$select_w_sensor_devID = '<select name="w_sensor_devID" id="w_sensor_devID" required class="form-control required" style=" margin-bottom: 4px;" placeholder="Select Sensor" ><option value="0" disabled selected>Select Sensor</option>';
// Optex BSS 목록
$bo_table_info = G5_CU_CONF_GPIO;
// 목록보기 링크
$write_table = $g5['write_prefix'] . $bo_table_info;
$sql = " SELECT * FROM $write_table WHERE w_sensor_disable = '0' ORDER BY w_device_id ASC ";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$value_select = "?sensorID=".$row['w_sensor_serial']."&subject=".$row['wr_subject'];
	if($subject == $row['wr_subject'])
		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	else
		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
}
$select_w_sensor_devID .= '</select>';

// echo $select_w_sensor_devID;
$bo_table_name = 'w_log_sensor_'.$sensorID; // w_log_sensor_19216818_ETH1_19216816810
//echo $bo_table_name;
// 목록보기 링크
if($dueFrom && $dueTo) {
	if($eventType == "All") {
		$eventTypeIs = "";
	} else if($eventType == "Sent") {
		$eventTypeIs = "w_event_outCount > 0 AND";
	} else if($eventType == "Schedule") {
		$eventTypeIs = "w_event_schedule > 0 AND";
	} else if($eventType == "Ignore") {
		$eventTypeIs = "w_event_ignore > 0 AND";
	} else if($eventType == "Error") {
		$eventTypeIs = "w_event_error > 0 AND";
	} else if($eventType == "Run") {
		$eventTypeIs = "w_cfg_id > 0 AND";
	}
	
	if($dueFrom == $dueTo) {
		$itIsAday = 1;
	} else if($dueFrom > $dueTo) { // 스와핑
		$itIsAday = 0;
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
	if($itIsAday) {
		$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	} else {
		$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	}
	$titleIs = "$dueFrom ~ $dueToTmp : $eventType";
} else {
	$eventType = "All";
	$dueFrom = date("Y-m-d 00:00:00");
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueFrom) + (86399)); // 하루 - 1초 , 86400
	$dueTo = $dueToTmp;
	$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	$titleIs = "$dueFrom ~ $dueToTmp : $eventType";
}

$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$chartData_0 = "['ID', 'Date', 'Hour/Min', 'Location', 'Count'],";
	$subjectChart = "EVENT";
	while ($row = sql_fetch_array($result)) {
		list($dateIs, $timeIs) = explode(' ', $row['Time']);
		list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
		$monthIs--;
		list($hIs, $mIs, $sIs) = explode(':', $timeIs);
		if($itIsAday) {
			$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.", ".$mIs.")";
			// $dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.")";
		} else {
			$dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.", ".$hIs.")";
			// $dateIs = "new Date(".$yearIs.", ".$monthIs.", ".$dayIs.")";
		}
		$chartData_0 .= "['', ".$dateIs.", ".$hIs.", '".$subjectChart."', ".$row['Count']."],";
	}
}
// echo $sql;
if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.php';
if($subject) $board['bo_subject'] = $subject; else $board['bo_subject'] = "Chart";
?>
<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL ?>/jquery-ui.css">
<script src="<?php echo G5_THEME_JS_URL ?>/jquery-ui.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$(function(){ // 날짜 입력
		$("#item_date_fr").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
		$("#item_date_to").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
	});
	$('#w_sensor_devID').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=<?php if($eventType) echo $eventType; else echo ''; ?>", "_self");
	});
	$('#item_date_fr,#item_date_to').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});	
	$('#btn_eventAll').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=All", "_self");
	});
	$('#btn_eventSent').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=Sent", "_self");
	});
	$('#btn_eventSchedule').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=Schedule", "_self");
	});
	$('#btn_eventIgnore').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=Ignore", "_self");
	});
	$('#btn_eventError').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=Error", "_self");
	});
	$('#btn_eventRun').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=Run", "_self");
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
<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
<?php echo $select_w_sensor_devID ?>
<input class="" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<input class="" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<button type="button" id="btn_eventAll" class="btn btn-primary btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">All Events</button>
<button type="button" id="btn_eventSent" class="btn btn-success btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Sent Events</button>
<button type="button" id="btn_eventSchedule" class="btn btn-info btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Sent Schedule</button>
<button type="button" id="btn_eventIgnore" class="btn btn-warning btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Ignore Event</button>
<button type="button" id="btn_eventError" class="btn btn-danger btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Error Events</button>
<button type="button" id="btn_eventRun" class="btn btn-default btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Start/Restart</button>
</div>
<div id="series_chart_div_all" style="width: 100%; height: 700px;"></div>
</div>


<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>