<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

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

$deleteDue = 60; // 설정보다 과거 자료 삭제

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

// 타임스템ㅌ프로 검색 w_stamp
// $sqlTailing = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
// $sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";
// $sqlCountSum = " SELECT IFNULL(SUM(w_ax_cnt),0)AS sumForware,IFNULL(SUM(w_xa_cnt),0)AS sumBackward, IFNULL(SUM(w_approved),0)AS sumApproved, IFNULL(SUM(w_unknown),0)AS sumUnknown, IFNULL(SUM(w_timeout),0)AS sumTimeout FROM  $bo_table_name WHERE  $eventTypeIs w_stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY w_id DESC; ";

// 센서가 주는 시간으로 검색 w_ymdhm
$ymdhmFrom = date("YmdHi", strtotime($dueFrom));
$ymdhmTo = date("YmdHi", strtotime($dueToTmp));

$sqlDeleting = " DELETE FROM $bo_table_name WHERE `w_stamp` < NOW() - INTERVAL $deleteDue DAY; "; // 60일 이후 데이터 삭제
$result = sql_query($sqlDeleting);

$sqlTailing = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_ymdhm BETWEEN '$ymdhmFrom' AND '$ymdhmTo' ORDER BY w_id DESC LIMIT $offset, $items_per_page; ";
$sqlCountRow = " SELECT * FROM $bo_table_name WHERE $eventTypeIs w_ymdhm BETWEEN '$ymdhmFrom' AND '$ymdhmTo' ORDER BY w_id DESC; ";
$sqlCountSum = " SELECT IFNULL(SUM(w_ax_cnt),0)AS sumForware,IFNULL(SUM(w_xa_cnt),0)AS sumBackward, IFNULL(SUM(w_approved),0)AS sumApproved, IFNULL(SUM(w_unknown),0)AS sumUnknown, IFNULL(SUM(w_timeout),0)AS sumTimeout FROM  $bo_table_name WHERE  $eventTypeIs w_ymdhm BETWEEN '$ymdhmFrom' AND '$ymdhmTo' ORDER BY w_id DESC; ";

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
		// $("#item_date_fr").datepicker({ dateFormat: "yymmdd000000", maxDate: 0 }); // 과거 선택
		// $("#item_date_to").datepicker({ dateFormat: "yymmdd000000", maxDate: 0 }); // 과거 선택
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
<?php echo $select_duration ?>
<?php if($page>1) { ?>
<span style="float:left;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?seleteID=<?php echo $seleteID ?>&dueTableID=<?php echo $dueTableID ?>&subject=<?php echo $subject ?>&eventType=<?php echo $eventType ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Previous[ITS_Lang]?></a></span>
<?php } ?>
<input class="" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date" style=" width: 80px; padding: 4px 2px; vertical-align: middle;">
<input class="" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date" style=" width: 80px; padding: 4px 2px; vertical-align: middle;">

<button type="button" id="btn_history" class="btn btn-info btn-sm" onclick='window.open("./chart_tailing_D3.php?sensorID=<?php echo $sensorID ?>&subject=<?php echo urlencode($subject) ?>&due=<?php echo $due ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>", "chart");'>Chart</button>

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
$result = sql_query("SHOW COLUMNS FROM ". $bo_table_name); 
while ($row = sql_fetch_array($result)) { 
	// if ($row['Field'] == 'w_ax_cnt')
	echo "<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>".str_replace('w_', '', str_replace('_cnt', '', $row['Field']))."</th>";
}
?>
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
</div>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>