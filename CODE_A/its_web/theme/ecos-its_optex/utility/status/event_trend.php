<?php
include_once('./_common.php');
if($is_guest) exit("Abnormal approach!");

if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.sub.php';

global $g5, $bo_table;

function select_w_devideID($devideID='') {
	// wr_subject, w_map_id, w_camera_model, w_camera_addr, w_camera_serial
	global $g5;
	$zoneList = array();
	$write_table = $g5['write_prefix'] . G5_CU_CONF_ZONE;
	$sql = " SELECT wr_id, wr_subject FROM $write_table WHERE w_zone_disable = 0 ORDER BY wr_id DESC ";
	// print $sql;
	$result = sql_query($sql);
	while ($row = sql_fetch_array($result)) {
		$zoneList[$row['wr_id']] = $row['wr_subject'];
	}

	$select_w_sensor_id = '<select name="devideID" id="devideID" class="form-control input50P"><option value="" selected>Select All</option>';
	while (list($key, $value) = each($zoneList)) { 
		if($devideID == $key) {
			$select_w_sensor_id .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_w_sensor_id .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_w_sensor_id .= '</select>';
	return $select_w_sensor_id;
}

// home/theme/ecos-its_optex/utility/status/list_IMS.php?devideID=16&eventType=Clear&dueFrom=2019-11-26%2005:37:51&dueTo=2019-11-28%2000:00:00
// 로그 스타일 형식
if($eventType == "Alarm") {
	$eventTypeIs = "(w_action = 1 OR w_action = 7) AND";
} else if($eventType == "Log") {
	$eventTypeIs = "w_action = 3 AND";
} else if($eventType == "Block") {
	$eventTypeIs = "w_action = 4 AND";
} else if($eventType == "Error") {
	$eventTypeIs = "w_action >= 8 AND";
} else if($eventType == "Clear") {
	$eventTypeIs = "w_action = 0 AND";
// } else if($eventType == "Shot") {
	// $eventTypeIs = "w_shot != '' AND";
} else {
	$eventTypeIs = "";
}

if($devideID) {
	$devideIDIs = "w_gr = $devideID AND";
} else {
	$devideIDIs = "";
}

if($dueFrom && $dueTo) { // 날짜 시작 및 끝 정보가 있는경우
	if($dueFrom == $dueTo) { // 최초 시작인 경우 
		$dueFrom = date("Y-m-d H:i:s", strtotime($dueTo) - (86399)); // 하루 - 1초 , 86400
	} else if($dueFrom > $dueTo) { // 시작과 끝 날짜가 바뀐 경우 스와핑
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
} else {
	$dueTo = date("Y-m-d H:i:s");
	// $dueFrom = date("Y-m-d H:i:s", strtotime($dueTo) - (86399 * 7)); // 하루 - 1초 , 86400
	$dueFrom = date("Y-m-d H:i:s", strtotime($dueTo) - (86399)); // 하루 - 1초 , 86400
}


// 관련기간 디바이스별 통계 표시
$bo_table_name = 'w_log_IMS_data';
// $sql = " SELECT w_sensorName, count(w_gr) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY w_gr ORDER BY w_sensorName DESC;";
// $sql = " SELECT w_sensorName, count(w_sensorName) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY w_gr ORDER BY w_sensorName DESC;";
$sql = " SELECT w_sensorName AS Zone, count(w_sensorName) AS Count, w_stamp AS Stamp FROM  $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY w_gr, DAY(w_stamp), MONTH(w_stamp), YEAR(w_stamp) ORDER BY w_sensorName DESC;";

// 버블차트 
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$sensorEach = "";
	while ($row = sql_fetch_array($result)) {
		$dateValue = new DateTime($row['Stamp']);
		$sensorEach .= "{'Zone': '".$row['Zone']."', 'Count': '".$row['Count']."', 'Stamp': '".date_format($dateValue,"Y-m-d H:i")."'},";
	}
}
?>

<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL ?>/jquery-ui.css">
<script src="<?php echo G5_THEME_JS_URL ?>/jquery-ui.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$(function(){ // 날짜 입력
		$("#item_date_fr").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
		$("#item_date_to").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 1 }); // 과거 선택
	});

	$('#eventType,#devideID,#item_date_fr,#item_date_to').on('change', function() { // 날짜 선택후 
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?devideID="+$('#devideID').val()+"&eventType="+$('#eventType').val()+"&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});
});
</script>

<section class="success" id="header" style="padding:0;">
    <div class="container" style="padding:0;margin-top: 10px;" onclick="self.close()"><?php echo $SK_BO_Close_this_window[ITS_Lang]?></div>
</section>

<style>
.table thead tr th { padding:0;letter-spacing:0;text-transform:uppercase;color:gray;padding-top:4px;font-size:8pt; }
</style>
<div id="bo_list" class="container">
	<div style="margin:10px;display:flex;">
		<select class="form-control" id="eventType">
			<option value="" selected>Select All</option>
			<option <?php if($eventType == 'Alarm') echo 'selected';?>>Alarm</label>
			<option <?php if($eventType == 'Log') echo 'selected';?>>Log</label>
			<option <?php if($eventType == 'Block') echo 'selected';?>>Block</label>
			<option <?php if($eventType == 'Error') echo 'selected';?>>Error</label>
			<option <?php if($eventType == 'Clear') echo 'selected';?>>Clear</label>
			<!-- option <?php if($eventType == 'Shot') echo 'selected';?>>Shot</label -->
		</select>
		<?php echo select_w_devideID($devideID); ?>

		<input class="form-control" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date">
		<input class="form-control" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date">
	</div>
	<div style="text-align: center;">
		<a href="./chart_IMS_D3.php?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>" target="_self">
			<button type="button" class="btn btn-success btn-sm" id="btn_history"><?php echo $SK_BO_Chart[ITS_Lang]?></button>
		</a>
		<a href="./list_IMS.php?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>" target="_self">
			<button type="button" id="btn_history" class="btn btn-info btn-sm"><?php echo $SK_BO_List[ITS_Lang]?></button>
		</a>
	</div>

	<!-- 버블차트 시작 -->
	<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/d3.v4.3.0.js"></script> <!-- Load d3.js -->
	<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/dimple.v2.3.0.min.js"></script> <!-- Load dimplejs.js -->

	<div style="text-align: right;"><?php // echo $sensorEach; ?></div>
	<div id="chartContainer" style="text-align:center;">
		<script type="text/javascript">
			// http://dimplejs.org/index.html
			// {'Zone': '".$row['Zone']."', 'Count': '".$row['Count']."', 'Stamp': '".$row['Stamp']."'}
			var svg = dimple.newSvg("#chartContainer", 900, 600);
			var data = [<?php echo $sensorEach; ?>];
			data.forEach(function (d) {
				d["Day"] = d["Stamp"].substring(0, d["Stamp"].length - 6);
			}, this);
			var myChart = new dimple.chart(svg, data);
			
			myChart.setBounds(70, 40, 800, 500); // 차트 크기
			
			myChart.addTimeAxis("x", "Day", "%Y-%m-%d", "%m/%d");
			// myChart.addCategoryAxis("x", ["<?php echo $num_rows;?>"]);
			myChart.addMeasureAxis("y", "Count");

			myChart.addSeries("Zone", dimple.plot.bubble);
			s = myChart.addSeries("Zone", dimple.plot.line); // 
			// s.interpolation = "step";
			// s.interpolation = "cardinal";
			s.lineMarkers = true;
			
			myChart.addLegend(70, 10, 800, 40, "right"); // 바 이름 따로 표시

			myChart.draw();
		</script>
	</div>
</div>
