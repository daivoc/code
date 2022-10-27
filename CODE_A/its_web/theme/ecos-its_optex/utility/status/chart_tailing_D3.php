<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.php';

// USB 드라이버 관련 device port
global $g5, $bo_table;

// 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)
$select_duration = '
<select name="duration" id="duration" required class="form-control required" style=" margin-bottom: 4px;" placeholder="Duration" >
<option value="0"></option>
<option value="1">분간</option>
<option value="2">시간</option>
<option value="3" selected>일간</option>
<option value="4">주간</option>
<option value="5">월간</option>
</select>
';


if(!$page) { $page = 1; }
// set the number of items to display per page
$items_per_page = 30;
// build query
$offset = ($page - 1) * $items_per_page;
// echo $offset;

if ($dueTableID) {
	$bo_table_name = 'w_log_giken_'.$dueTableID;
} else {
	$bo_table_name = 'w_log_giken_day';
}
	
// dueTableID=hour&subject=Per%20hour&dueFrom=2020-10-01%2000:00:00&dueTo=2020-10-13%2000:00:00&eventType=All
// 목록보기 링크

if($eventType == "Approved") {
	$eventTypeIs = "w_approved > 0 AND";
} else if($eventType == "Unknown") {
	$eventTypeIs = "w_unknown > 0 AND";
} else if($eventType == "Timeout") {
	$eventTypeIs = "w_timeout > 0 AND";
} else if($eventType == "Forward") {
	$eventTypeIs = "w_ax_cnt > 0 AND";
} else if($eventType == "Backward") {
	$eventTypeIs = "w_xa_cnt > 0 AND";
} else {
	$eventTypeIs = "";
}

if($seleteID == "1") {
	$groupBy = "w_serial, MINUTE(w_stamp)";
} else if($seleteID == "2") {
	$groupBy = "w_serial, HOUR(w_stamp)";
} else if($seleteID == "3") {
	$groupBy = "w_serial, DAY(w_stamp)";
} else if($seleteID == "4") {
	$groupBy = "w_serial, WEEK(w_stamp)";
} else if($seleteID == "5") {
	$groupBy = "w_serial, MONTH(w_stamp)";
} else {
	$groupBy = "w_serial, DAY(w_stamp)";
}

if($dueFrom && $dueTo) {
	if($dueFrom > $dueTo) { // 스와핑
		$itIsAday = 0;
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86400)); // 하루 - 1초 , 86400
	$titleIs = "$dueFrom ~ $dueToTmp : $eventType";
} else {
	$dueFrom = date("Y-m-d 00:00:00");
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueFrom) + (86400)); // 하루 - 1초 , 86400
	$dueTo = $dueToTmp;
	$titleIs = "$dueFrom ~ $dueToTmp";
}
$sqlTailing = " SELECT w_ymdhm, IFNULL(SUM(w_ax_cnt),0)AS sumForware,IFNULL(SUM(w_xa_cnt),0)AS sumBackward, IFNULL(SUM(w_approved),0)AS sumApproved, IFNULL(SUM(w_unknown),0)AS sumUnknown, IFNULL(SUM(w_timeout),0)AS sumTimeout, w_serial FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY $groupBy ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
// $sqlTailing = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
$sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
$sqlCountSum = " SELECT IFNULL(SUM(w_ax_cnt),0)AS sumForware,IFNULL(SUM(w_xa_cnt),0)AS sumBackward, IFNULL(SUM(w_approved),0)AS sumApproved, IFNULL(SUM(w_unknown),0)AS sumUnknown, IFNULL(SUM(w_timeout),0)AS sumTimeout FROM  $bo_table_name WHERE  $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";

$result = sql_query($sqlCountRow);
$num_rows = sql_num_rows($result); // 자료 갯수
$totalPage = ceil($num_rows / $items_per_page);



/////////////////////////////////////
// 버블차트 
/////////////////////////////////////
$sqlChart = " SELECT w_ymdhm AS Time, IFNULL(SUM(w_ax_cnt),0)AS sumForware,IFNULL(SUM(w_xa_cnt),0)AS sumBackward, IFNULL(SUM(w_approved),0)AS sumApproved, IFNULL(SUM(w_unknown),0)AS sumUnknown, IFNULL(SUM(w_timeout),0)AS sumTimeout, w_serial FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY $groupBy ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
$result = sql_query($sqlChart);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$chartDataB = ""; // "{'Weekday', 'Date', 'HourMin', 'Count'},"; // 버블차트 
	while ($row = sql_fetch_array($result)) {
		// list($dateIs, $timeIs) = explode(' ', $row['Time']);
		// list($yearIs, $monthIs, $dayIs) = explode('-', $dateIs);
		// $monthIs--;
		// list($hIs, $mIs, $sIs) = explode(':', $timeIs);
		$ymdhis = str_pad($row['Time'], 14, "0");
		$yIs = substr($ymdhis, 0, 4);
		$mIs = substr($ymdhis, 4, 2);
		$dIs = substr($ymdhis, 6, 2);
		$hIs = substr($ymdhis, 8, 2);
		$iIs = substr($ymdhis, 10, 2);
		$sIs = substr($ymdhis, 12, 2);
		$dataDate = $yIs."-".$mIs."-".$dIs." ".$hIs.":".$iIs.":".$sIs;
		$dateValue = new DateTime($dataDate);
		$unixTimestamp = strtotime($dataDate);
		$subjectChart = date("l", $unixTimestamp);
		//$chartDataB .= "{'Shift':'Early','Date':'".date_format($dateValue,"d M Y H:i")."','Value':".$row['Count']."},";
		// $chartDataB .= "{ 'Shift':'Early','Date':'".date_format($dateValue,"Y-m-d H:i")."','Value':".$row['Count']."},";
		$chartDataB .= "{ 'Weekday':'".$subjectChart."','Date':'".date_format($dateValue,"Y-m-d H:i")."','HourMin':".$hIs.",'Count':".$row['sumForware']."},";
	}
}

// 카렌다차트 
$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY DAY(w_stamp), MONTH(w_stamp), YEAR(w_stamp) ORDER BY w_id ASC; ";
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
if($num_rows) { // 자료가 존재 하면
	$chartDataC = ""; // [ new Date(2012, 3, 13), 37032 ], // 카렌다차트
	$chartDataD = "['Date', 'Count'],"; // [ new Date(2012, 3, 13), 37032 ], // 카렌다차트
	while ($row = sql_fetch_array($result)) {
		list($dateIs, $timeIs) = explode(' ', $row['Time']);
		// $chartDataC .= "[ new Date(".$dateIs."), ".$row['Count']."],";
		$chartDataC .= $dateIs.", ".$row['Count']."\n";
		$chartDataD .= "[".$dateIs.", ".$row['Count']."],";
	}
}
/////////////////////////////////////
// 버블차트 End
/////////////////////////////////////


if($subject) $board['bo_subject'] = $subject; else $board['bo_subject'] = "Log List";
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
	
	$("#duration").val(<?php echo $seleteID?>);
	
	$('#duration').on('change', function() {
		if(this.value == "1") { var idIs ="?seleteID="+this.value+"&dueTableID=min&subject=Per min&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(); }
		else if(this.value == "2") { var idIs ="?seleteID="+this.value+"&dueTableID=hour&subject=Per hour&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(); }
		else if(this.value == "3") { var idIs ="?seleteID="+this.value+"&dueTableID=day&subject=Per day&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(); }
		else if(this.value == "4") { var idIs ="?seleteID="+this.value+"&dueTableID=week&subject=Per week&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(); }
		else if(this.value == "5") { var idIs ="?seleteID="+this.value+"&dueTableID=month&subject=Per month&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(); }
		else { var idIs ="?seleteID="+this.value; }
		
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+idIs+"&eventType=<?php if($eventType) echo $eventType; else echo ''; ?>", "_self");
	});
	$('#item_date_fr,#item_date_to').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?seleteID="+$("#duration").val()+"&dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});

    $('#btn_eventAll').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&seleteID="+$("#duration").val()+"&eventType=All", "_self");
	});
	$('#btn_eventApproved').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&seleteID="+$("#duration").val()+"&eventType=Approved", "_self");
	});
	$('#btn_eventUnknown').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&seleteID="+$("#duration").val()+"&eventType=Unknown", "_self");
	});
	$('#btn_eventTimeout').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&seleteID="+$("#duration").val()+"&eventType=Timeout", "_self");
	});
	$('#btn_eventForward').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&seleteID="+$("#duration").val()+"&eventType=Forward", "_self");
	});
	$('#btn_eventBackward').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&seleteID="+$("#duration").val()+"&eventType=Backward", "_self");
	});
});
</script>
	
<section class="success" id="header" style="padding:0;">
	<div class="container">
		<div class="intro-text">
			<span class="name"><?php echo $board['bo_subject'] ?><span class="sound_only"> 목록</span></span>
			<hr class="star-light wow zoomIn">
			<span class="skills wow fadeInUp" data-wow-delay="1s"></span>
		</div>
	</div>
</section>

<?php
$result = sql_query($sqlTailing);
$list_body = '';
$rowNo = 0 + $offset;
while ($row = sql_fetch_array($result)) {
	$list_body .= "<tr style=line-height:12px;'><td style='font-size:7pt; text-align: center; padding:0;'>".++$rowNo."</td>";
	foreach ($row as $col_value) {
		$list_body .= "<td style='font-size:7pt; text-align: center; padding:0;'>".$col_value."</td>";
	}
	$list_body .= "</tr>";
}
?>
<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
	<?php echo $select_duration ?>
	<?php if($page>1) { ?>
	<span style="float:left;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?seleteID=<?php echo $seleteID ?>&dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Previous[ITS_Lang]?></a></span>
	<?php } ?>
	<input class="" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date" style=" width: 80px; padding: 4px 2px; vertical-align: middle;">
	<input class="" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date" style=" width: 80px; padding: 4px 2px; vertical-align: middle;">

	<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./list_tailing.php?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "chart");'>List</button>

	<button type="button" id="btn_eventAll" class="btn btn-primary btn-sm" value="?dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">All Events</button>
	<button type="button" id="btn_eventApproved" class="btn btn-success btn-sm" value="?dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Approved</button>
	<button type="button" id="btn_eventUnknown" class="btn btn-info btn-sm" value="?dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Unknown</button>
	<button type="button" id="btn_eventTimeout" class="btn btn-warning btn-sm" value="?dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Timeout</button>
	<button type="button" id="btn_eventForward" class="btn btn-danger btn-sm" value="?dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Forward</button>
	<button type="button" id="btn_eventBackward" class="btn btn-default btn-sm" value="?dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Backward</button>


	<?php if($page<$totalPage) { ?>
	<span style="float:right;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?seleteID=<?php echo $seleteID ?>&dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page + 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Next[ITS_Lang]?></a></span>
	<?php } ?>
	</div>

	<div style="font-size: 7pt;float: right;margin: 0 10px;">
	<?php 
	// 합계 계산 후 출력
	$resultSum = sql_query($sqlCountSum); 
	$rowSum = sql_fetch_array($resultSum);
	echo " Forward:".$rowSum["sumForware"].", Backward:".$rowSum["sumBackward"].", Approved:".$rowSum["sumApproved"].", Disapproved:".($rowSum["sumForware"]-$rowSum["sumApproved"]).", Unknown:".$rowSum["sumUnknown"].", Timeout:".$rowSum["sumTimeout"].", Total Passers:".($rowSum["sumForware"]+$rowSum["sumBackward"]);
	// print_r($rowSum);
	// Array ( [sumForware] => 269 [sumBackward] => 90 [sumApproved] => 26 [sumUnknown] => 333 [sumTimeout] => 0 )
	?>
	</div>

	<div class="tbl_head01 tbl_wrap"   style="margin:10px;">
		<table class="table table-hover">
			<thead class="thead-inverse">
			<tr>
			<?php
			// $result = sql_query("SHOW COLUMNS FROM ". $bo_table_name); 
			// while ($row = sql_fetch_array($result)) { 
			// 	// if ($row['Field'] == 'w_ax_cnt')
			// 	echo "<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>".str_replace('w_', '', str_replace('_cnt', '', $row['Field']))."</th>";
			// }
			?>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>No</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>Time</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>Out</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>In</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>AP</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>UN</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>TO</th>
			<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>Sensor</th>
			</tr>
			</thead>
			<tbody>
			<?php echo $list_body; ?>
			</tbody>
		</table>
	</div>
	<div style='font-size:7pt';><?php echo "Page: ". $page." of ".$totalPage.", Total records: ".$num_rows." - About: ". $titleIs; ?></div>
	<?php if(!$is_guest) { ?>
	<div style="float:right; margin-bottom: 10px;"><button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("./downloadList_BSS.php?sqlCountRow=<?php echo base64_encode($sqlCountRow) ?>&bo_table_name=<?php echo base64_encode($bo_table_name) ?>", "downloadCSV");'>Download CSV<?php // echo $sqlCountRow ?></button></div>
	<?php } ?>
</div>

<?php if($num_rows) { // 자료가 존재 하면 ?>

<!-- /////////////////////////////// -->
<!-- 버블차트 시작 -->
<!-- /////////////////////////////// -->
<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/d3.v4.3.0.js"></script> <!-- Load d3.js -->
<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/dimple.v2.3.0.min.js"></script> <!-- Load dimplejs.js -->
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

		var x = myChart.addTimeAxis("x", "Day", "%Y-%m-%d", "%Y %m %d");
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
<div><?php // echo $chartDataC; ?></div>
<div><?php // echo $chartDataD; ?></div>

<?php } ?>
<!-- /////////////////////////////// -->
<!-- 버블차트 끝 -->
<!-- /////////////////////////////// -->



</div>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>