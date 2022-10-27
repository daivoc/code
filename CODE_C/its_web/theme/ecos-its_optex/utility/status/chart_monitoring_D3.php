<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.php';

global $g5, $bo_table;

// 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)
$select_w_sensor_devID = '<select name="w_sensor_devID" id="w_sensor_devID" required class="form-control required" style=" margin-bottom: 4px;" placeholder="Select Sensor" ><option value="0" disabled selected>Select Sensor</option>';
$sensor_list = array();
foreach ($G5_CU_CONF_GROUP as $key => $value) {
    // echo "\$G5_CU_CONF_GROUP[$key] => $value.\n";
	// 목록보기 링크
	$write_table = $g5['write_prefix'] . $value;
	$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
	if($val !== FALSE) {
		$sql = "SELECT w_id, wr_subject, w_sensor_serial FROM $write_table WHERE w_sensor_disable = 0";
		$result = sql_query($sql);
		while ($row = sql_fetch_array($result)) {
			// $value_select = "?sensorID=".$row['w_sensor_serial']."&subject=".$row['wr_subject'];
			$value_select = "?sensorID=".$row['w_sensor_serial']."&subject=".urlencode($row['wr_subject']);
			$sensor_list[] = $value_select;
			if($subject == $row['wr_subject'])
				$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
			else
				$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
		}
	}
}
$select_w_sensor_devID .= '</select>';
// 끝 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)

if (count($sensor_list) == 1 && $sensorID == "") {
	header ("Location: $_SERVER[PHP_SELF]$sensor_list[0]"); 
} else {

// 목록보기 링크
$bo_table_name = 'w_log_sensor_'.$sensorID; // w_log_sensor_19216818_ETH1_19216816810

$eventType = "All";

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
	
					   
								   
				   
								 
  
	// 카렌다 차트를 위한 쿼리
	// if($itIsAday) { // 하루 이내의 기간이면 시간을 기준으로 분단위 그룹
		// $sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	// } else { // 날짜를 기준으로 시간단위 그룹
		// $sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY HOUR(w_stamp), DAY(w_stamp) ORDER BY w_id ASC; ";
	// }
	$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY HOUR(w_stamp), DAY(w_stamp) ORDER BY w_id ASC; ";
	$titleIs = "$dueFrom ~ $dueToTmp : $eventType";
} else {
	$dueFrom = date("Y-m-d 00:00:00");
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueFrom) + (86399)); // 하루 - 1초 , 86400
	$dueTo = $dueToTmp;
	$sql = " SELECT w_stamp AS Time, count(w_stamp) AS Count FROM  $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' GROUP BY MINUTE(w_stamp), HOUR(w_stamp) ORDER BY w_id ASC; ";
	$titleIs = "$dueFrom ~ $dueToTmp : $eventType";
}

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
if($subject) $board['bo_subject'] = $subject; else $board['bo_subject'] = "Chart";


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
	$('#w_sensor_devID').on('change', function() { // 센서 선택 후 
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value, "_self");
	});
	$('#item_date_fr,#item_date_to').on('change', function() { // 날짜 선택후 
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?sensorID=<?php echo $sensorID ?>&subject=<?php echo urlencode($subject) ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});	
});
</script>

				 
						
				
												
					 
				  

			   
					   
				 
				   
				 
			 
					
	
					   
  
				
				   
		  

				
				   
					
					  

					   
				   
				  
				   
				 
 
			 
				  
				   
				   
			   
	 
			  
			  
				 
				 
			   
				  
				
	  
					  
	 
	
 
				 
					 
		 
				   

<style>
.shadow { text-shadow: 4px 6px 4px black; }
.item_date_fr { text-align: center; padding: 4px 2px; vertical-align: middle; }
.item_date_to { text-align: center; padding: 4px 2px; vertical-align: middle; }
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name"><?php echo $board['bo_subject'] ?><span class="sound_only"> 차트</span></span>
            <hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>
<div id="bo_list" class="container">
	<div style="margin:10px;text-align: center;">
		<?php echo $select_w_sensor_devID // Select Box Tag ?>
		<input class="item_date_fr" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date">
		<input class="item_date_to" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date">
		<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./list_union.php?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "chart");'>List</button>
	</div>

<?php if($num_rows) { // 자료가 존재 하면 ?>

<!-- 버블차트 시작 -->
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
<div><?php echo $chartDataC; ?></div>
<div><?php echo $chartDataD; ?></div>

<?php } ?>

</div>


<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
}
?>