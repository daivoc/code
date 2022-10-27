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

if (count($sensor_list) == 1) {
	header ("Location: $_SERVER[PHP_SELF]$sensor_list[0]"); 
} else {

// 목록보기 링크
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

// 목록보기 링크
$bo_table_name = 'w_log_IMS_data';
// $dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
// $sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY HOUR(w_stamp), DAY(w_stamp) ORDER BY w_id ASC; ";
$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY HOUR(w_stamp), DAY(w_stamp) ORDER BY w_id ASC; ";
$titleIs = "$dueFrom ~ $dueTo : $eventType";

// 버블차트 
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$chartDataB = ""; // "{'Weekday', 'Date', 'HourMin', 'Count'},"; // 버블차트 
	while ($row = sql_fetch_array($result)) {
		list($dateIs, $timeIs) = explode(' ', $row['Time']);
		list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
		$monthIs--;
		list($hIs, $mIs, $sIs) = explode(':', $timeIs);
		$dateValue = new DateTime($row['Time']);
		$unixTimestamp = strtotime($row['Time']);
		$subjectChart = date("l", $unixTimestamp);
		//$chartDataB .= "{'Shift':'Early','Date':'".date_format($dateValue,"d M Y H:i")."','Value':".$row['Count']."},";
		// $chartDataB .= "{ 'Shift':'Early','Date':'".date_format($dateValue,"Y-m-d H:i")."','Value':".$row['Count']."},";
		$chartDataB .= "{ 'Weekday':'".$subjectChart."','Date':'".date_format($dateValue,"Y-m-d H:i")."','HourMin':".$hIs.",'Count':".$row['Count']."},";
	}
}

// 카렌다차트 
// $sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY DAY(w_stamp), MONTH(w_stamp), YEAR(w_stamp) ORDER BY w_id ASC; ";
$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY DAY(w_stamp), MONTH(w_stamp), YEAR(w_stamp) ORDER BY w_id ASC; ";
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	// $chartDataC = ""; // [ new Date(2012, 3, 13), 37032 ], // 카렌다차트
	// $chartDataD = "['Date', 'Count'],"; // [ new Date(2012, 3, 13), 37032 ], // 카렌다차트
	$chartDataE = "";
	while ($row = sql_fetch_array($result)) {
		list($dateIs, $timeIs) = explode(' ', $row['Time']);
		// $chartDataC .= $dateIs.", ".$row['Count']."\n";
		// $chartDataD .= "[".$dateIs.", ".$row['Count']."],";
		$chartDataE .= "{'Date': '".$dateIs."', 'Events': '".$row['Count']."'},";
	}
}

if($subject) $board['bo_subject'] = $subject; else $board['bo_subject'] = "Chart";
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
		// window.open("<?php echo $_SERVER["PHP_SELF"] ?>?subject=<?php echo urlencode($subject) ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?devideID="+$('#devideID').val()+"&eventType="+$('#eventType').val()+"&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});	
});
</script>

<style>
.shadow { text-shadow: 4px 6px 4px black; }
.item_date_fr { text-align: center; padding: 4px 2px; vertical-align: middle; }
.item_date_to { text-align: center; padding: 4px 2px; vertical-align: middle; }
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container" style="padding:0;margin-top: 10px;" onclick="self.close()"><?php echo $SK_BO_Close_this_window[ITS_Lang]?></div>
</section>

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
		<a href="./list_IMS.php?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>" target="_self">
			<button type="button" id="btn_history" class="btn btn-info btn-sm"><?php echo $SK_BO_List[ITS_Lang]?></button>
		</a>
		<a href="./event_trend.php?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>" target="_self">
			<button type="button" id="btn_history" class="btn btn-warning btn-sm"><?php echo "경향"?></button>
		</a>
	</div>

<?php if($num_rows) { // 자료가 존재 하면 ?>

<!-- 버블차트 시작 -->
<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/d3.v4.3.0.js"></script> <!-- Load d3.js -->
<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/dimple.v2.3.0.min.js"></script> <!-- Load dimplejs.js -->

<div id="chartContainer" style="text-align:center;">
	<script type="text/javascript">
		var svg = dimple.newSvg("#chartContainer", 900, 200);
		var data = [<?php echo $chartDataE; // {'Date': '2019-06-13', 'Events': '776'}, ?>];
		var myChart = new dimple.chart(svg, data);
		myChart.setBounds(70, 40, 800, 100); // 차트 크기
		// myChart.addCategoryAxis("y", "Events"); // 로그함수 형식 출력
		// myChart.addMeasureAxis("y", "Events").hidden = true;	
		
		var x = myChart.addTimeAxis("x", "Date", "%Y-%m-%d", "%m/%d");
		var y = myChart.addMeasureAxis("y", "Events");
		x.overrideMin = new Date("<?php echo $dueFrom?>".substring(0,10));
		x.overrideMax = new Date("<?php echo $dueTo?>".substring(0,10));
		// y.overrideMin = new Date("01/01/2000 00:00");
		// y.overrideMax = new Date("01/02/2000 00:00");
		x.showGridlines = true;
		x.addOrderRule("Date");
		y.tickFormat = "d"; // 1/1000 = k
		
		var s = myChart.addSeries("Date", dimple.plot.bar);
		
		myChart.draw();

		// 동작 않됨
		s.afterDraw = function (shape, data) {
			svg.append("text")
			.style("font-size", "7px")
			.style("font-family", "sans-serif");
			
			// // Get the shape as a d3 selection
			// var s = d3.select(shape),
			// rect = {
				// x: parseFloat(s.attr("x")),
				// y: parseFloat(s.attr("y")),
				// width: parseFloat(s.attr("width")),
				// height: parseFloat(s.attr("height"))
			// };
			// // Only label bars where the text can fit
			// if (rect.height >= 8) {
				// // Add a text label for the value
				// svg.append("text")
				// // Position in the centre of the shape (vertical position is
				// // manually set due to cross-browser problems with baseline)
				// .attr("x", rect.x + rect.width / 2)
				// .attr("y", rect.y + rect.height / 2 + 3.5)
				// // Centre align
				// .style("text-anchor", "middle")
				// .style("font-size", "10px")
				// .style("font-family", "sans-serif")
				// // Make it a little transparent to tone down the black
				// .style("opacity", 0.6)
				// // Prevent text cursor on hover and allow tooltips
				// .style("pointer-events", "none")
				// // Format the number
				// .text(d3.format(",.1f")(data.yValue / 1000) + "k");
			// }
		};

	</script>
</div>

<div id="chartContainer" style="text-align:center;">
	<script type="text/javascript">
		// http://dimplejs.org/index.html
		var svg = dimple.newSvg("#chartContainer", 900, 600);
		dataB = [
		  <?php echo $chartDataB; ?>
		];

		dataB.forEach(function (d) {
			d["Day"] = d["Date"].substring(0, d["Date"].length - 6);
			d["Time of Day"] = "2000-01-01 " + d["Date"].substring(d["Date"].length - 5);
		}, this);

		// Create the chart as usual
		var myChart = new dimple.chart(svg, dataB);
		myChart.setBounds(70, 40, 800, 500); // 차트 크기

		// var x = myChart.addTimeAxis("x", "Day", "%Y-%m-%d", "%Y %m %d");
		var x = myChart.addTimeAxis("x", "Day", "%Y-%m-%d", "%m/%d");
		var y = myChart.addTimeAxis("y", "Time of Day","%Y-%m-%d %H:%M", "%H:%M"); // HourMin
		var z = myChart.addMeasureAxis("z", "Count") * 100;

		x.overrideMin = new Date("<?php echo $dueFrom?>".substring(0,10));
		x.overrideMax = new Date("<?php echo $dueTo?>".substring(0,10));
		y.overrideMin = new Date("01/01/2000 00:00");
		y.overrideMax = new Date("01/02/2000 00:00");

		// Show a label for every 4 weeks.
		// x.timePeriod = d3.timeWeek; // 주간의 인터벌
		// x.timeInterval = 4; // 주간의 인터벌의 배수로 표시됨
		y.timeInterval = 2; // 사간의 인터벌의 배수로 표시됨

		// Control bubble sizes by setting the max and min values
		z.overrideMin = 900;
		z.overrideMax = 3000;

		// Add the bubble series for shift values first so that it is drawn behind the lines
		var mySeries = myChart.addSeries("Weekday", dimple.plot.bubble);
		// mySeries.addOrderRule(["\월", "\화", "\수", "\묵", "\금", "\토", "\일"]); // 오류발생
		mySeries.addOrderRule(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]);
		
		// Show a legend
		myChart.addLegend(180, 10, 800, 20, "left");

		// Draw everything
		myChart.draw();
	</script>
</div>
 
<!-- 카렌다 차트 시작 -->
<div><?php// echo $chartDataB; ?></div>
<div><?php// echo $chartDataC; ?></div>
<div><?php// echo $chartDataD; ?></div>
<div><?php// echo $chartDataE; ?></div>

<?php } ?>

</div>


<?php
// include_once(G5_THEME_PATH.'/tail.php');
// include_once(G5_PATH.'/tail.php');
}
?>