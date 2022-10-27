<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// USB 드라이버 관련 device port
global $g5, $bo_table;

if(!$page) { $page = 1; }
// set the number of items to display per page
$items_per_page = 50;
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
	if($dueFrom > $dueTo) { // 스와핑
		$itIsAday = 0;
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo)); // + (86399)); // 하루 - 1초 , 86400
	$sql = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
	$sqlCountRow = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
	$titleIs = "$dueFrom ~ $dueToTmp";
	$result = sql_query($sqlCountRow);
	$num_rows = sql_num_rows($result); // 자료 갯수
	$totalPage = ceil($num_rows / $items_per_page);
} else {
	$dueFrom = date("Y-m-d H:i:s", strtotime('-1 hours'));
	$dueToTmp = date("Y-m-d H:i:s"); // + (86399)); // 하루 - 1초 , 86400
	$dueTo = $dueToTmp;
	$sql = " SELECT * FROM $bo_table_name ORDER BY w_id DESC LIMIT 1, 10; "; // 마지막 50개
	$sqlCountRow = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
	$titleIs = "Event of Last 50";
	// $result = sql_query($sqlCountRow);
	$num_rows = 50; // 자료 갯수
	$totalPage = ceil($num_rows / $items_per_page);
}
	
// $sql = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
// $sqlCountRow = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
// $titleIs = "$dueFrom ~ $dueToTmp";
// // echo $sql;

// $result = sql_query($sqlCountRow);
// $num_rows = sql_num_rows($result); // 자료 갯수
// $totalPage = ceil($num_rows / $items_per_page);
?>

	
<?php
$svg_element = '';
$masking_value = '';
$masking_all = '';
$element_array = array();

$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$list_body .= "<tr style='line-height:12px;'>";
    foreach ($row as $col_value) {
        $list_body .= "<td style='font-size:7pt; text-align: center; padding:0;'>".$col_value."</td>";
	}
	$list_body .= "</tr>";

	$cR = $row['w_evt_id'] % 256;
	$cG = $row['w_evt_id'] % 254;
	$cB = $row['w_evt_id'] % 253;
	$fillColor = "fill='rgba(".$cR.", ".$cG.", ".$cB.", 0.4)'";
	$svg_element .= "<circle id='".$row['w_evt_id']."' cx='".$row['w_evt_X']."' cy='".$row['w_evt_Y']."' r='".$row['w_evt_S']."' ".$fillColor." stroke='white' stroke-width='1'><title>".$row['w_stamp']."</title></circle>";

	$element_array[$row['w_evt_id']]['X'][] = $row['w_evt_X'];
	$element_array[$row['w_evt_id']]['Y'][] = $row['w_evt_Y'];
	$element_array[$row['w_evt_id']]['S'][] = $row['w_evt_S'];
}

// // 이벤트 그룹별로 박스(Rect)로 표시
// foreach ($element_array as $key => $value) { //  전체 어레이레서 최고 최소값 표현 '12:12_12:12','23:43_34:45'
// 	$masking_value .= '<br>'.$key.' '.min($value['X']).':'.min($value['Y']).'_'.max($value['X']).':'.max($value['Y']).', '.min($value['S']).':'.max($value['S']).'mm';
// 	$svg_element .= "<rect id='".min($value['X'])."' style='fill:#ffffff10; stroke:gray; stroke-width:1px;' x='".min($value['X'])."' y='".min($value['Y'])."' width='".(max($value['X']) - min($value['X']))."' height='".(max($value['Y']) - min($value['Y']))."'></rect>";
// 	$masking_all .= min($value['X']).':'.min($value['Y']).'_'.max($value['X']).':'.max($value['Y']).', ';
// }
?>

<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL; ?>/bootstrap-combined.min.css">
<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL; ?>/bootstrap-datetimepicker.min.css">

<script src="<?php echo G5_THEME_JS_URL; ?>/jquery.min.js"></script>
<script src="<?php echo G5_THEME_JS_URL; ?>/bootstrap.min.js"></script>
<script src="<?php echo G5_THEME_JS_URL; ?>/bootstrap-datetimepicker.min.js"></script>
	
<script type="text/javascript">
$(document).ready(function(){
	// $('#w_sensor_devID').on('change', function() {
		// window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value, "_self");
	// });
	$('#btn_search').on('click', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?nodeIn=<?php echo $nodeIn ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});
	
	$("#frameURL").attr("src","<?php echo G5_THEME_URL ?>/utility/nodeJs_table/realtime_RLS_<?php echo $nodeIn ?>_Area.html");
	// Iframe내에 출력된 목록의 자료를 표시한다.
	var iframe = $('#frameURL');
	iframe.load(function () {
		// console.log('iframe loaded');
		var frame = iframe.contents().find('#rls_event');
		frame.html("<?php echo $svg_element ?>");
		// console.log('frame html = ' + frame.html("<?php echo $svg_element ?>")); // This works!
	});
	
	$('#datetimepickerF').datetimepicker({
	format: 'yyyy-MM-dd hh:mm:ss',
	});
	$('#datetimepickerT').datetimepicker({
	format: 'yyyy-MM-dd hh:mm:ss',
	});

});
</script>

<div id="datetimepickerF" class="input-append date" style="float:left;padding:4px;">
	<input type="text" name="item_date_fr" id="item_date_fr" style="height: 30px;" value="<?php echo $dueFrom ?>" >
	<span class="add-on"><i data-time-icon="icon-time" data-date-icon="icon-calendar"></i></span>
</div>
<div id="datetimepickerT" class="input-append date" style="float:left;padding:4px;">
	<input type="text" name="item_date_to" id="item_date_to" style="height: 30px;" value="<?php echo $dueTo ?>" >
	<span class="add-on"><i data-time-icon="icon-time" data-date-icon="icon-calendar"></i></span>
</div>
<div style="float:right;padding:4px;">
	<button type="button" id="btn_search" class="btn btn-success btn-sm" >Search</button>
</div>

<div style='width: 100%;height:550px;text-align: center;position: absolute; top: 40px; left: 0;'>
	<iframe id="frameURL" name="frameURL" src="" width="98%" height="100%" scrolling="no" style='border: unset;'></iframe>
</div>

<div style="clear:both;padding:4px;display:none;">
	<?php if($page>1) { ?>
	<span style="float:left;padding:4px;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?nodeIn=<?php echo $nodeIn ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Previous[ITS_Lang]?></a></span>
	<?php } ?>
	<span style="float:left;padding:4px;"><?php // echo $select_w_sensor_devID ?></span>
	<?php if($page<$totalPage) { ?>
	<span style="float:left;padding:4px;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?nodeIn=<?php echo $nodeIn ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page + 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Next[ITS_Lang]?></a></span>
	<?php } ?>
	<span style="float:left;padding:4px 10px; font-size: 8pt;">Event Group <?php echo $masking_value ?></span>
	<div style="clear: both;padding:4px 10px; font-size: 7pt; color:gray;"><?php echo $masking_all ?></div>
</div>

<div id="bo_list" class="container" style="display:none;">
	<div class="tbl_head01 tbl_wrap" style="margin:10px;overflow: hidden;overflow-y: auto;clear: both;">
		<table class="table table-hover">
			<thead class="thead-inverse">
			<tr>
				<?php
				$result = sql_query("SHOW COLUMNS FROM ". $bo_table_name); 
				while ($row = sql_fetch_array($result)) { 
				echo "<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>".substr(substr($row['Field'], strrpos($row['Field'], '_') + 1),0,5)."</th>";
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
</div>


<?php /* if(!$is_guest) { ?>
<div style="float:right;padding:4px;"><button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("./downloadList.php?sqlCountRow=<?php echo base64_encode($sqlCountRow) ?>&bo_table_name=<?php echo base64_encode($bo_table_name) ?>", "downloadCSV");'>Download CSV<?php // echo $sqlCountRow ?></button></div>
<?php } */ ?>