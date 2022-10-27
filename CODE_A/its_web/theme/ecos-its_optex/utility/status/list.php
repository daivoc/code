<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// USB 드라이버 관련 device port
global $g5, $bo_table;

// 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)
$select_w_sensor_devID = '<select name="w_sensor_devID" id="w_sensor_devID" required class="form-control required" style=" margin-bottom: 4px;" placeholder="Select Sensor" ><option value="0" disabled selected>Select Sensor</option>';

// // Optex BSS 목록
// $bo_table_info = G5_CU_CONF_RLS;
// // 목록보기 링크
// $write_table = $g5['write_prefix'] . $bo_table_info;
// $sql = " SELECT * FROM $write_table WHERE w_sensor_disable = '0' ORDER BY w_device_id ASC ";

// 목록보기 링크
$write_table = $g5['write_prefix'] . G5_CU_CONF_BSS;
$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
if($val !== FALSE) 
	$sql = "( SELECT w_id, wr_subject, w_device_id, w_sensor_lat_s, w_sensor_lng_s, w_sensor_lat_e, w_sensor_lng_e, w_sensor_serial FROM $write_table WHERE w_sensor_disable = 0 )";

$write_table = $g5['write_prefix'] . G5_CU_CONF_RLS;
$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
if($val !== FALSE) {
	if ($sql) {
		$sql = $sql . " UNION (SELECT w_id, wr_subject, w_device_id, w_sensor_lat_s, w_sensor_lng_s, w_sensor_lat_e, w_sensor_lng_e, w_sensor_serial FROM $write_table WHERE w_sensor_disable = 0 )";
	} else {
		$sql = "( SELECT w_id, wr_subject, w_device_id, w_sensor_lat_s, w_sensor_lng_s, w_sensor_lat_e, w_sensor_lng_e, w_sensor_serial FROM $write_table WHERE w_sensor_disable = 0 )";
	}
}

$write_table = $g5['write_prefix'] . G5_CU_CONF_GPIO;
$val = sql_query('select 1 from `'.$write_table.'` LIMIT 1');
if($val !== FALSE) {
	if ($sql) {
		$sql = $sql . " UNION (SELECT w_id, wr_subject, w_device_id, w_sensor_lat_s, w_sensor_lng_s, w_sensor_lat_e, w_sensor_lng_e, w_sensor_serial FROM $write_table WHERE w_sensor_disable = 0 )";
	} else {
		$sql = "( SELECT w_id, wr_subject, w_device_id, w_sensor_lat_s, w_sensor_lng_s, w_sensor_lat_e, w_sensor_lng_e, w_sensor_serial FROM $write_table WHERE w_sensor_disable = 0 )";
	}
}


$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$value_select = "?commType=BSS&devideID=".$row['w_device_id']."&sensorID=".$row['w_sensor_serial']."&subject=".$row['wr_subject'];
	if($subject == $row['wr_subject'])
		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	else
		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
}

// // RXTX 목록
// $bo_table_rxtx_info = G5_CU_CONF_RXTX;
// // 목록보기 링크
// $write_table = $g5['write_prefix'] . $bo_table_rxtx_info;
// $sql = " SELECT * FROM $write_table WHERE wr_10 = 'Enable' ORDER BY w_device_id ASC ";
// $result = sql_query($sql);
// while ($row = sql_fetch_array($result)) {
	// $value_select = "?commType=ttyUSB&devideID=".$row['w_device_id']."&sensorID=".$row['w_sensor_id']."&subject=".$row['wr_subject'];
	// if($subject == $row['wr_subject'])
		// $select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	// else
		// $select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
// }

// // 릴레이 목록
// $bo_table_relay_info = G5_CU_CONF_RELAY;
// // 목록보기 링크
// $write_table = $g5['write_prefix'] . $bo_table_relay_info;
// $sql = " SELECT * FROM $write_table WHERE wr_10 = 'Enable' ORDER BY w_device_id ASC";
// $result = sql_query($sql);
// while ($row = sql_fetch_array($result)) {
	// $value_select = "?commType=GPIO&sensorID=".$row['w_sensor_id']."&subject=".$row['wr_subject'];
	// if($subject == $row['wr_subject'])
		// $select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
	// else
		// $select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
// }

$select_w_sensor_devID .= '</select>';

// echo $select_w_sensor_devID;
// $sensorID = (string)$sensorID;
if($commType) { // $commType && $sensorID
	if(!$page) { $page = 1; }
	// set the number of items to display per page
	$items_per_page = 40;
	// build query
	$offset = ($page - 1) * $items_per_page;
	// echo $offset;

	$list_body = '';
	if($commType == 'ttyUSB')
		$bo_table_name = 'w_log_sensor_'.end(explode('/',$devideID)).'_'.$sensorID;
	elseif($commType == 'GPIO')
		$bo_table_name = 'w_log_sensor_GPIO_'.$sensorID;
	elseif($commType == 'BSS')
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
	if($dueTo) {
		if(!$dueFrom) $dueFrom = $dueTo; // 시작일이 없으면 종료일자를 복사한다.
		if($dueFrom > $dueTo) { // 스와핑 과거일자를 시작일로 변경 한다.
			$dueToTmp = $dueFrom;
			$dueFrom = $dueTo;
			$dueTo = $dueToTmp;
		}
		$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
		$sql = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' $sql_w_filter ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
		$sqlCountRow = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' $sql_w_filter ORDER BY w_id DESC; ";
	} else if($due){
		$nowDatetime = date('Y-m-d H:i:s');
		if($due == '1h') $dueDatetime = date('Y-m-d H:i:s', strtotime('-1 hour'));
		else if($due == '1d') $dueDatetime = date('Y-m-d H:i:s', strtotime('-1 day'));
		else if($due == '1w') $dueDatetime = date('Y-m-d H:i:s', strtotime('-1 week'));
		else if($due == '1m') $dueDatetime = date('Y-m-d H:i:s', strtotime('-1 month'));
		else if($due == '3m') $dueDatetime = date('Y-m-d H:i:s', strtotime('-3 month'));
		else if($due == '6m') $dueDatetime = date('Y-m-d H:i:s', strtotime('-6 month'));
		else if($due == '1y') $dueDatetime = date('Y-m-d H:i:s', strtotime('-1 year'));
		
		$sql = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' $sql_w_filter ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
		$sqlCountRow = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' $sql_w_filter ORDER BY w_id DESC; ";
	} else { // 최초 로딩시 변수값이 없으면 한달을 기준으로 한다.
		$due = '1m';
		$nowDatetime = date('Y-m-d H:i:s');		
		$dueDatetime = date('Y-m-d H:i:s', strtotime('-1 month')); // 기본 값은 한달
		$sql = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' $sql_w_filter ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
		$sqlCountRow = " SELECT * FROM $bo_table_name WHERE w_stamp BETWEEN '$dueDatetime' AND '$nowDatetime' $sql_w_filter ORDER BY w_id DESC; ";
		// $sql = " SELECT * FROM $bo_table_name ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
		// $sqlCountRow = " SELECT * FROM $bo_table_name ORDER BY w_id DESC; ";
	}
	// $dueFrom = $dueDatetime;
	// $dueTo = $nowDatetime;
	// echo $sqlCountRow;
	$result = sql_query($sqlCountRow);
	$num_rows = sql_num_rows($result); // 자료 갯수
	$totalPage = ceil($num_rows / $items_per_page);
	// $totalPage = $num_rows;
	// while ($row = sql_fetch_array($result)) {
		// print_r($row);
	// }

}
if (G5_IS_MOBILE) {
    include_once G5_MOBILE_PATH.'/index.php';
    return;
}
include_once G5_PATH.'/head.php';

if($subject) $titleIs = $subject; else $titleIs = "Log"; // 서브잭트명이 없으면 Log로..
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
	$('#item_date_to').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
		
	});
	$('#w_sensor_devID').on('change', function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>"+this.value+"&due=<?php echo $due ?>", "_self");
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
        $list_body .= "<td style='font-size:7pt; text-align: center; padding:0;max-width:60px;'>".$col_value."</td>";
	}
	$list_body .= "</tr>";
}
?>
<?php if($commType) { ?>
<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
<?php echo $select_w_sensor_devID ?>
<?php if($page>1) { ?>
<span style="float:left;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Previous[ITS_Lang]?></a></span>
<?php } ?>
<input class="" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<input class="" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date" style=" width: 90px; padding: 4px 2px; vertical-align: middle;">
<!-- input type="button" value="1H" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1h", "_self");' -->
<input type="button" value="1D" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1d", "_self");'>
<input type="button" value="1W" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1w", "_self");'>
<input type="button" value="1M" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1m", "_self");'>
<!-- input type="button" value="3M" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=3m", "_self");'>
<input type="button" value="6M" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=6m", "_self");'>
<input type="button" value="1Y" id="btn_history" class="btn btn-sm" onclick='window.open("<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=1y", "_self");' -->
<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./chart.php?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "chart");'>Chart</button>

<?php if($page<$totalPage) { ?>
<span style="float:right;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?commType=<?php echo $commType ?>&devideID=<?php echo $devideID ?>&sensorID=<?php echo $sensorID ?>&subject=<?php echo $subject ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page + 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Next[ITS_Lang]?></a></span>
<?php } ?>
</div>
<div class="tbl_head01 tbl_wrap"   style="margin:10px;">
<table class="table table-hover">
<thead class="thead-inverse">
<tr>
<?php
$result = sql_query("SHOW COLUMNS FROM ". $bo_table_name); 
while ($row = sql_fetch_array($result)) { 
  echo "<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>".substr($row['Field'], strrpos($row['Field'], '_') + 1)."</th>";
} 
?>
</tr>
</thead>
<tbody>
<?php echo $list_body; ?>
</tbody>
</table>
</div>
<div><?php echo "Page: ". $page." of ".$totalPage.", Total events: ".$num_rows; ?></div>
<?php if(!$is_guest) { ?>
<div style="float:right; margin-bottom: 10px;"><button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("./downloadList.php?sqlCountRow=<?php echo base64_encode($sqlCountRow) ?>&bo_table_name=<?php echo base64_encode($bo_table_name) ?>", "downloadCSV");'>Download CSV<?php // echo $sqlCountRow ?></button></div>
<?php } ?>
</div>
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