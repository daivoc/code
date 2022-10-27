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

if(!$page) { $page = 1; }
// set the number of items to display per page
$items_per_page = 40;
// build query
$offset = ($page - 1) * $items_per_page;
// echo $offset;

// home/theme/ecos-its_optex/utility/status/list_IMS.php?devideID=16&eventType=Clear&dueFrom=2019-11-26%2005:37:51&dueTo=2019-11-28%2000:00:00
// 로그 스타일 형식
if($eventType == "All") {
	$eventTypeIs = "";
} else if($eventType == "Alarm") {
	$eventTypeIs = "w_action = 1 AND";
} else if($eventType == "Log") {
	$eventTypeIs = "w_action = 3 AND";
} else if($eventType == "Block") {
	$eventTypeIs = "w_action = 4 AND";
} else if($eventType == "Error") {
	$eventTypeIs = "(w_action = 8 OR w_action = 7) AND";
} else if($eventType == "Clear") {
	$eventTypeIs = "w_action = 0 AND";
} else if($eventType == "Repair") {
	
	// 데이터베이스 기간삭제 및 복구(Repair)
	$deleteDue = 70; // 10주 이후의 로그는 삭제 함
	$bo_table_name = 'w_log_IMS_data';
	$sqlDelete = "DELETE FROM ".$bo_table_name." WHERE `w_stamp` < NOW() -INTERVAL ".$deleteDue." DAY ";
	$deleted = sql_query($sqlDelete);

	$sqlRepair = "REPAIR TABLE ".$bo_table_name;
	$repaired = sql_query($sqlRepair);
	sql_fetch_array($repaired);

	// print("IMS Log Tables Repaired.");
	$eventTypeIs = "pass";
} else {
	$eventTypeIs = "pass";
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

if($eventTypeIs != "pass") {
	// 관련기간 전체 리스트 표시
	// $list_head = "<th scope='col'>ID</th><th scope='col'>sensorId</th><th scope='col'>sensorName</th><th scope='col'>userName</th><th scope='col'>action</th><th scope='col'>description</th><th scope='col'>stamp</th>";
	$list_head = "<th scope='col'>ID</th><th scope='col'>sensorName</th><th scope='col'>userName</th><th scope='col'>action</th><th scope='col'>description</th><th scope='col'>stamp</th>";

	$list_body = '';
	$bo_table_name = 'w_log_IMS_data';
	// $sql = " SELECT w_id, w_sensorId, w_sensorName, w_userName, w_action, w_description, w_stamp FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
	$sql = " SELECT w_id, w_sensorName, w_userName, w_action, w_description, w_stamp FROM $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
	// $sql = " SELECT w_id, w_sensorName, w_userName, w_action, w_description, w_stamp FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
	$result = sql_query($sql);
	while ($row = sql_fetch_array($result)) {
		$list_body .= "<tr style=line-height:12px;'>";
		foreach ($row as $col_value) {
			$list_body .= "<td style='font-size:7pt; text-align: center; padding:0;'>".$col_value."</td>";
		}
		$list_body .= "</tr>";
	}
	// print($sql);


	// 관련기간 디바이스별 통계 표시
	$bo_table_name = 'w_log_IMS_data';
	// $sql = " SELECT w_sensorName, count(w_gr) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY w_gr ORDER BY w_sensorName DESC;";
	// $sql = " SELECT w_sensorName, count(w_sensorName) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY w_gr ORDER BY w_sensorName DESC;";
	// $sql = " SELECT w_stamp AS Time, w_sensorName, count(w_sensorName) AS Count FROM  $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY DAY(w_stamp), w_gr ORDER BY w_sensorName DESC;";
	$sql = " SELECT w_stamp AS Time, w_sensorName, count(w_sensorName) AS Count FROM  $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' GROUP BY DAY(w_stamp), w_gr ORDER BY w_sensorName DESC;";

	// 버블차트 
	$result = sql_query($sql);
	$num_rows = sql_num_rows($result); // 자료 갯수
	if($num_rows) { // 자료가 존재 하면
		$sensorEach = "";
		while ($row = sql_fetch_array($result)) {
			$sensorEach .= "{'Time': '".$row['Time']."', 'Zone': '".$row['w_sensorName']."', 'Events': '".$row['Count']."'},";
		}
	}

	$sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs $devideIDIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' ORDER BY w_id DESC; ";
	// $sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueTo' ORDER BY w_id DESC; ";
	$result = sql_query($sqlCountRow);
	$num_rows = sql_num_rows($result); // 자료 갯수
	$totalPage = ceil($num_rows / $items_per_page);

	// print($sqlCountRow);
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

	$('#eventType,#devideID,#item_date_fr,#item_date_to').on('change', function(){ // 날짜 선택후 
		if($('#eventType').val()) {
			if (window.confirm("로그량에 따라 일정시간이 소요 됩니다.\n진행하겠습니까?")) {
				$("#waitContainer").css("display","block");
				window.open("<?php echo $_SERVER["PHP_SELF"] ?>?devideID="+$('#devideID').val()+"&eventType="+$('#eventType').val()+"&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
			}
		}
	});

	$('.switchPage').on('click', function(){ // 날짜 선택후 
		$("#waitContainer").css("display","block");
	});
});
</script>

<section class="success" id="header" style="padding:0;">
<button type="button" class="btn btn-danger btn-sm" style="padding:4px;margin:1px;" onclick="self.close()"><?php echo $SK_BO_Close_this_window[ITS_Lang]?></button>
</section>

<style>
.table thead tr th { padding:0;letter-spacing:0;text-transform:uppercase;color:gray;padding-top:4px;font-size:8pt; }
#waitContainer { display:none; height:50px; background-image: url('http://192.168.0.91/theme/ecos-its_optex/img/loading.gif');background-repeat: no-repeat;background-position: center;background-size: 40px; }
</style>
<div id="bo_list" class="container">
	<div style="margin:10px;display:flex;">
		<select class="form-control" id="eventType">
			<option value="" selected>Select</option>
			<option <?php if($eventType == 'All') echo 'selected';?>>All</label>
			<option <?php if($eventType == 'Alarm') echo 'selected';?>>Alarm</label>
			<option <?php if($eventType == 'Log') echo 'selected';?>>Log</label>
			<option <?php if($eventType == 'Block') echo 'selected';?>>Block</label>
			<option <?php if($eventType == 'Error') echo 'selected';?>>Error</label>
			<option <?php if($eventType == 'Clear') echo 'selected';?>>Clear</label>
			<option <?php if($eventType == 'Repair') echo 'selected';?>>Repair</label>
		</select>
		<?php echo select_w_devideID($devideID); ?>

		<input class="form-control" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date">
		<input class="form-control" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date">
	</div>
	<div style="text-align: center;">
		<a href="./chart_IMS_D3.php?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>" target="_new">
			<button type="button" class="btn btn-success btn-sm" id="btn_history"><?php echo $SK_BO_Chart[ITS_Lang]?></button>
		</a>
		<a href="./event_trend.php?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>" target="_new">
			<button type="button" id="btn_history" class="btn btn-warning btn-sm"><?php echo "경향"?></button>
		</a>
	</div>
	<?php if($page>1) { ?>
	<span style="float:left;margin:4px 0;" class="switchPage" ><a href="<?php echo $_SERVER["PHP_SELF"] ?>?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Previous[ITS_Lang]?></a></span>
	<?php } ?>
	<?php if($page<$totalPage) { ?>
	<span style="float:right;margin:4px 0;" class="switchPage" ><a href="<?php echo $_SERVER["PHP_SELF"] ?>?eventType=<?php echo $eventType ?>&devideID=<?php echo $devideID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page + 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Next[ITS_Lang]?></a></span>
	<?php } ?>

	<div id="waitContainer" style="text-align: center;"></div>

	<?php if($eventTypeIs != "pass") { ?>
		<!-- 버블차트 시작 -->
		<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/d3.v4.3.0.js"></script> <!-- Load d3.js -->
		<script type="text/javascript" src="<?php echo G5_THEME_JS_URL ?>/dimple.v2.3.0.min.js"></script> <!-- Load dimplejs.js -->

		<div id="chartContainer" style="text-align:center;">
			<script type="text/javascript">
				var svg = dimple.newSvg("#chartContainer", 900, 200);
				var data = [<?php echo $sensorEach; ?>];
				var myChart = new dimple.chart(svg, data);
				myChart.setBounds(70, 40, 800, 100); // 차트 크기

				myChart.addCategoryAxis("x", ["Zone"]);
				myChart.addMeasureAxis("y", "Events");
				myChart.addSeries("Zone", dimple.plot.bar); // 바 칼라 적용
				myChart.addLegend(70, 10, 800, 40, "right"); // 바 이름 따로 표시

				myChart.draw();
			</script>
		</div>
		
		<div id="listContainer" class="tbl_head01 tbl_wrap">
			<table class="table table-striped table-hover">
			<thead class="thead-dark">
			<tr>
				<?php echo $list_head; ?>
			</tr>
			</thead>
			<tbody>
				<?php echo $list_body; ?>
			</tbody>
			</table>
		</div>

		<div><?php echo "Page: ". $page." of ".$totalPage.", Total events: ".$num_rows; ?></div>
		<div style="float:right; margin-bottom: 10px;">
			<button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("./downloadList_union.php?sqlCountRow=<?php echo base64_encode($sqlCountRow) ?>&bo_table_name=<?php echo base64_encode($bo_table_name) ?>", "downloadCSV");'><?php echo $SK_BO_Download_CSV[ITS_Lang]?></button>
		</div>
	<?php } ?>
</div>
