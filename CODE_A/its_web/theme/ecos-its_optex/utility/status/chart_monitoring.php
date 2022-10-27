<?php
include_once('./_common.php');
if(!$sensorID) exit("Abnormal approach!");

if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.sub.php';

global $g5, $bo_table;

if (count($sensor_list) == 1 && $sensorID == "") {
	header ("Location: $_SERVER[PHP_SELF]$sensor_list[0]"); 
} else {

$bo_table_name = 'w_log_sensor_'.$sensorID; // w_log_sensor_19216818_ETH1_19216816810

if($dueFrom && $dueTo) { // 날짜 시작 및 끝 정보가 있는경우
	if($dueFrom == $dueTo) { // 최초 시작인 경우 
		$itIsAday = 1;
	} else if($dueFrom > $dueTo) { // 시작과 끝 날짜가 바뀐 경우 스와핑
		$itIsAday = 0;
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
	
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
	
	if($itIsAday) { // 하루 이내의 기간이면 시간을 기준으로 분단위 그룹
		$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	} else { // 날짜를 기준으로 시간단위 그룹
		$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY HOUR(w_stamp), DAY(w_stamp) ORDER BY w_id ASC; ";
	}
	// 카렌다 차트를 위한 쿼리
	$titleIs = "$dueFrom ~ $dueToTmp";
} else {
	$dueFrom = date("Y-m-d 00:00:00");
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueFrom) + (86399)); // 하루 - 1초 , 86400
	$dueTo = $dueToTmp;
	$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	$titleIs = "$dueFrom ~ $dueToTmp";
}

// 버블차트 
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$chartData_0 = "['ID', 'Date', 'Hour', 'Location', 'Count'],"; // 버블차트 
	while ($row = sql_fetch_array($result)) {
		list($dateIs, $timeIs) = explode(' ', $row['Time']);
		list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
		$monthIs--;
		list($hIs, $mIs, $sIs) = explode(':', $timeIs);
		
		$unixTimestamp = strtotime($row['Time']);
		$subjectChart = date("l", $unixTimestamp);
		
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

// 카렌다차트 
$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp) ORDER BY w_id ASC; ";
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$chartData_1 = ""; // [ new Date(2012, 3, 13), 37032 ], // 카렌다차트
	while ($row = sql_fetch_array($result)) {
		list($dateIs, $timeIs) = explode(' ', $row['Time']);
		list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
		$monthIs--;
		$chartData_1 .= "[ new Date(".$yearIs.", ".$monthIs.", ".$dayIs."), ".$row['Count']."],";
	}
}
?>

<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL ?>/jquery-ui.css">
<script src="<?php echo G5_THEME_JS_URL ?>/jquery-ui.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$(function(){ // 날짜 입력
		$("#item_date_fr").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
		$("#item_date_to").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
	});
	$('#item_date_fr,#item_date_to').on('change', function() { // 날짜 선택후 
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});	
});
</script>

<?php if($num_rows) { // 자료가 존재 하면 ?>
	<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/loader.js"></script>
	<script type="text/javascript">
	// https://developers.google.com/chart/interactive/docs/gallery/columnchart https://www.gstatic.com/charts/loader.js
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawSeriesChart);

	function drawSeriesChart() {
		var data_all = google.visualization.arrayToDataTable([<?php echo $chartData_0; ?>]);
		var options = {
			title: 'Time Line - Event <?php echo $titleIs ?>',
			hAxis: {title: 'Date/Time',format: 'yy/M/dd'},
			vAxis: {title: 'Hour'},
			bubble: {textStyle: {fontSize: 18}},
		};
		var chart = new google.visualization.BubbleChart(document.getElementById('bubble_chart'));
		
		chart.draw(data_all, options);
	} // 버블차트 
	</script>

	<script type="text/javascript">
	// https://developers.google.com/chart/interactive/docs/gallery/calendar
	google.charts.load("current", {packages:["calendar"]});
	google.charts.setOnLoadCallback(drawChart);

	function drawChart() {
		var dataTable = new google.visualization.DataTable();
		dataTable.addColumn({ type: 'date', id: 'Date' });
		dataTable.addColumn({ type: 'number', id: 'Daily' });
		dataTable.addRows([<?php echo $chartData_1; ?>]);
	
		var chart = new google.visualization.Calendar(document.getElementById('calendar_basic'));
		var options = { 
			title: "Monthly and Weekly Trend",
			noDataPattern: {
				backgroundColor: 'silver',
			},
			height:400,
			calendar: {
				cellSize: 18,
				monthLabel: {
					fontName: 'Times-Roman',
					fontSize: 10,
					bold: true,
				},
				// daysOfWeek: '일월화수목금토',
			},
		};
	
		chart.draw(dataTable, options);
	} // 카렌다차트
</script>
<?php } // 자료가 존재 하면 ?>

<style>
.shadow { text-shadow: 4px 6px 4px black; }
.item_date_fr { text-align: center; padding: 4px 2px; vertical-align: middle; }
.item_date_to { text-align: center; padding: 4px 2px; vertical-align: middle; }
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container" style="padding:0;" onclick="self.close()">Close this window</div>
</section>
<div id="bo_list" class="container">
<div style="margin:20px 10px;text-align: center;">
<input class="item_date_fr" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date">
<input class="item_date_to" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date">
<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./list_monitoring.php?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "_self");'>List</button>
</div>
<div id="calendar_basic" style="width: 100%; height: 200px; text-align: center;"></div>
<div id="bubble_chart" style="width: 100%; height: 700px; text-align:center"></div>
</div>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
// include_once(G5_PATH.'/tail.php');
}
?>