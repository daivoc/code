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
	$value_select = "?devideID=".$row['w_device_id']."&sensorID=".$row['w_sensor_serial']."&subject=".$row['wr_subject'];
	if($subject == $row['wr_subject'])
		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	else
		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
}

$select_w_sensor_devID .= '</select>';

if(!$page) { $page = 1; }
// set the number of items to display per page
$items_per_page = 30;
// build query
$offset = ($page - 1) * $items_per_page;
// echo $offset;

$list_body = '';
$bo_table_name = 'w_log_sensor_'.$sensorID;

// 필터 형식에 따라 오류나 이밴트 발생 이밴트 전송
// w_cfg_id = , 0:normal, 100:event, 200:log, 300:post, 400:socker, 500:camera, 600:video, 700:light,  800:siren, 900:init
// w_eventValue = -1, 0, 1, number
if($filterType == "") {
	$sql_w_filter = "";
} else {
	$sql_w_filter = "AND w_cfg_id = '$filterType'";
}
	

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
	
	if($dueFrom > $dueTo) { // 스와핑
		$itIsAday = 0;
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
	$sql = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
	$sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
	$titleIs = "$dueFrom ~ $dueToTmp : $eventType";
} else {
	$dueFrom = date("Y-m-d 00:00:00");
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueFrom) + (86399)); // 하루 - 1초 , 86400
	$dueTo = $dueToTmp;
	$sql = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
	$sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
	$titleIs = "$dueFrom ~ $dueToTmp";
}

$result = sql_query($sqlCountRow);
$num_rows = sql_num_rows($result); // 자료 갯수
$totalPage = ceil($num_rows / $items_per_page);
if (G5_IS_MOBILE) {
    include_once G5_MOBILE_PATH.'/index.php';
    return;
}
include_once G5_PATH.'/head.php';
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
	$('#w_sensor_devID').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&eventType=<?php if($eventType) echo $eventType; else echo ''; ?>", "_self");
	});
	$('#item_date_fr,#item_date_to').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
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
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$list_body .= "<tr style=line-height:12px;'>";
    foreach ($row as $col_value) {
        $list_body .= "<td style='font-size:7pt; text-align: center; padding:0;'>".$col_value."</td>";
	}
	$list_body .= "</tr>";
}
?>
<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
<?php echo $select_w_sensor_devID ?>
<?php if($page>1) { ?>
<span style="float:left;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Previous[ITS_Lang]?></a></span>
<?php } ?>
<input class="" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<input class="" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<button type="button" id="btn_eventAll" class="btn btn-primary btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">All Events</button>
<button type="button" id="btn_eventSent" class="btn btn-success btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Sent Events</button>
<button type="button" id="btn_eventSchedule" class="btn btn-info btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Sent Schedule</button>
<button type="button" id="btn_eventIgnore" class="btn btn-warning btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Ignore Event</button>
<button type="button" id="btn_eventError" class="btn btn-danger btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Error Events</button>
<button type="button" id="btn_eventRun" class="btn btn-default btn-sm" value="?sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>">Start/Restart</button>

<?php if($page<$totalPage) { ?>
<span style="float:right;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page + 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Next[ITS_Lang]?></a></span>
<?php } ?>
</div>


<div class="tbl_head01 tbl_wrap"   style="margin:10px;">
<table class="table table-hover">
<thead class="thead-inverse">
<tr>
<?php
$result = sql_query("SHOW COLUMNS FROM ". $bo_table_name); 
while ($row = sql_fetch_array($result)) { 
  echo "<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>".substr(substr($row['Field'], strrpos($row['Field'], '_') + 1),0,4)."</th>";
}
?>
</tr>
</thead>
<tbody>
<?php echo $list_body; ?>
</tbody>
</table>
</div>
<div style='font-size:7pt';><?php echo "Page: ". $page." of ".$totalPage.", Total events: ".$num_rows." - About: ". $titleIs; ?></div>
<?php if(!$is_guest) { ?>
<div style="float:right; margin-bottom: 10px;"><button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("./downloadList_BSS.php?sqlCountRow=<?php echo base64_encode($sqlCountRow) ?>&bo_table_name=<?php echo base64_encode($bo_table_name) ?>", "downloadCSV");'>Download CSV<?php // echo $sqlCountRow ?></button></div>
<?php } ?>
</div>
</div>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>