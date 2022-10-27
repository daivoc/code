<?php
include_once('./_common.php');
if ($is_guest) { exit("Abnormal approach!"); }
// 본프로그램은 서버단에서 실행 됩니다.
// licenseSrvAdd.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvCSV.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvList.php는 라이센스서버에 상주하는 프로그램 명이다.
// 본 프로그램을 통해 ITS 라이센스 정보를 데이터베이스에 등록한다.
// 위치는 theme.config.php내 G5_CU_LICENSE_URL이 결정한다.
// 예 : define('G5_CU_LICENSE_URL', 'http://'.G5_CU_LICENSE_SERVER.'/ecosLicense');
// 데이터베이스 구성은 아래와 같으며 사전에 테이블 구성이 되어있어야 한다.
// 본 데이터베이스에 'system license' 등록은 제외되며
// application license 만 등록하는것을 원칙으로 한다.
// 각각의 스킨의 write_update.skin.php에서 include licenseSrv.php 실행 된다.

// USB 드라이버 관련 device port
global $g5, $bo_table;

if(!$page) { $page = 1; }
// set the number of items to display per page
$items_per_page = 20;
// build query
$offset = ($page - 1) * $items_per_page;
// echo $offset;

$list_body = '';
$license_tbl_name = 'w_its_license';
	
// 라이센스 데이터 추가
if($customer && $cpuID && $item_add_new) {
	// 데이터베이스 업데이트
	$customer;
	$cpuID; // CPU or Mac ID
	$subject = "N/A"; // 실행하는 프로그램
	$serial = "N/A";
	$status = "N/A";
	$device = "N/A";
	$remoteAddr = $_SERVER['REMOTE_ADDR'].":".$_SERVER['SERVER_ADDR'];
	$expiry = 0; // 계약 종료일
	$license = hash('sha256', $cpuID . hash('sha256', $customer));

	$date = new DateTime();
	$date->modify('+'.$expiration.' month');
	$expiry = $date->format('Y-m-d H:i:s');
	
	$sql = " insert into w_its_license
		set customer = '$customer',subject = '$subject',cpuID = '$cpuID',serial = '$serial',status = '$status',device = '$device',license = '$license',remoteAddr = '$remoteAddr',expiry = '$expiry' ";
	sql_query($sql);
	
	$l_id = sql_insert_id();
	$sql = " insert into w_its_license_index
		set cpuID = '$cpuID',
			l_id = '$l_id' ";
	sql_query($sql);

	$customer = "";
	$cpuID = ""; // CPU or Mac ID
} 

// 목록보기 링크
if($dueFrom && $dueTo) {
	if($customer) {
		$tmpCustomer = "customer like '%{$customer}%' AND";
	} else {
		$tmpCustomer = "";
	}
	if($cpuID) {
		$tmpCpuID = "cpuID like '%{$cpuID}%' AND";
	} else {
		$tmpCpuID = "";
	}
	if($dueFrom > $dueTo) { // 스와핑
		$itIsAday = 0;
		$dueToTmp = $dueFrom;
		$dueFrom = $dueTo;
		$dueTo = $dueToTmp;
	}
	$dueToTmp = date("Y-m-d H:i:s", strtotime($dueTo) + (86399)); // 하루 - 1초 , 86400
	$sql = " SELECT * FROM $license_tbl_name WHERE $tmpCustomer $tmpCpuID stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY l_id DESC LIMIT $offset, $items_per_page; ";
	$sqlCountRow = " SELECT * FROM $license_tbl_name WHERE stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY l_id DESC; ";
	$titleIs = "$dueFrom ~ $dueToTmp";
} else {
	// $dueFrom = date("Y-m-d 00:00:00");
	// $dueToTmp = date("Y-m-d H:i:s", strtotime($dueFrom) + (86399)); // 하루 - 1초 , 86400
	// $dueTo = $dueToTmp;
	// $sql = " SELECT * FROM $license_tbl_name WHERE $tmpCustomer $tmpCpuID stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY l_id DESC LIMIT $offset, $items_per_page; ";
	// $sqlCountRow = " SELECT * FROM $license_tbl_name WHERE stamp BETWEEN '$dueFrom' AND '$dueToTmp' ORDER BY l_id DESC; ";
	// $titleIs = "$dueFrom ~ $dueToTmp";
	$sql = " SELECT * FROM $license_tbl_name ORDER BY l_id DESC LIMIT $offset, $items_per_page; ";
	$sqlCountRow = " SELECT * FROM $license_tbl_name ORDER BY l_id DESC; ";
	$titleIs = "";
}

$result = sql_query($sqlCountRow);
$num_rows = sql_num_rows($result); // 자료 갯수
$totalPage = ceil($num_rows / $items_per_page);
if (G5_IS_MOBILE) {
    include_once G5_MOBILE_PATH.'/index.php';
    return;
}
include_once G5_PATH.'/head.php';
?>

<?php // href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css" ?>
<?php // src="//code.jquery.com/ui/1.11.4/jquery-ui.min.js" ?>
<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="//code.jquery.com/ui/1.11.4/jquery-ui.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$(function(){ // 날짜 입력
		$("#item_date_fr").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
		$("#item_date_to").datepicker({ dateFormat: "yy-mm-dd 00:00:00", maxDate: 0 }); // 과거 선택
	});
	$('#btn_eventAdd').click(function() {
		if($("#item_add_new").is(':checked')) {
			window.open("<?php echo $_SERVER["PHP_SELF"] ?>?customer="+$('#item_customer').val()+"&cpuID="+$('#item_cpuID').val()+"&item_add_new=1", "_self");
		}
	});
	$('#btn_eventRun').click(function() {
		window.open("<?php echo $_SERVER["PHP_SELF"] ?>?customer="+$('#item_customer').val()+"&cpuID="+$('#item_cpuID').val()+"&dueFrom="+$('#item_date_fr').val()+"&dueTo="+$('#item_date_to').val(), "_self");
	});
});
</script>
<style>
.listInput {width:180px;height: 20pt;float:left;margin:4px;}
.listBtn {margin:10px;float:right;}
.listTR {line-height:10px;word-break:break-all;border-bottom: 1px solid silver;}
.listTD {font-size:8pt;text-align:center;padding:4px;color:gray;padding:4px;color:gray;max-width:150px;overflow:hidden;}
.listTH {font-size:8pt;text-align:center;padding:2px 0;line-height:12px;}
.TD_1, .TH_1 {width:40px; color:red;}
/* .TD_8, .TH_8, .TD_9, .TH_9 {width: 70px;} */
.TD_11, .TD_12, .TD_13, .TD_14, .TD_15, .TD_16, .TD_17, .TD_18 {display:none;}
.TH_11, .TH_12, .TH_13, .TH_14, .TH_15, .TH_16, .TH_17, .TH_18 {display:none;}
</style>
<?php
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$list_body .= "<tr class='listTR'>";
	$i = 1;
    foreach ($row as $col_value) {
        $list_body .= "<td class='listTD TD_".$i."'>".$col_value."</td>";
		$i++;
	}
	$list_body .= "</tr>";
}
?>
<div id="bo_list" class="container">
<div style="margin: 80px 10px 0 10px;text-align: center;">
	<input class="form-control listInput required" type="text" name="item_date_fr" id="item_date_fr" value="<?php echo $dueFrom ?>" placeholder=" Date">
	<input class="form-control listInput required" type="text" name="item_date_to" id="item_date_to" value="<?php echo $dueTo ?>" placeholder=" Date">
	<input class="form-control listInput required" type="text" name="item_customer" id="item_customer" value="<?php echo $customer ?>" placeholder=" Customer">
	<input class="form-control listInput required" type="text" name="item_cpuID" id="item_cpuID" value="<?php echo $cpuID ?>" placeholder=" cpuID">
	<input class="form-control listInput required" style="width:24px;" type="checkbox" name="item_add_new" id="item_add_new" placeholder=" Addnew"><label for="item_add_new" style="float:left;margin:8px;font-size:10pt;font-weight:normal;">Add</label>
	<div style="float: right;margin-bottom: 10px;">
		<button type="button" id="btn_eventAdd" class="btn btn-info btn-sm" value="">Add New</button>
		<button type="button" id="btn_eventRun" class="btn btn-default btn-sm" value="">Search</button>
	</div>
</div>


<div class="">
<table class="table-hover" style="width:100%;">
<thead style="background: #404040;color: silver;">
<tr>
<?php
$result = sql_query("SHOW COLUMNS FROM ". $license_tbl_name); 
$i = 1;
while ($row = sql_fetch_array($result)) { 
  // echo "<th style='font-size:8pt; text-align: center; padding:2px 0; line-height:12px;'>".substr(substr($row['Field'], strrpos($row['Field'], '_') + 1),0,4)."</th>";
  echo "<th class='listTH TH_".$i."'>".$row['Field']."</th>";
  $i++;
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
<?php if($page>1) { ?>
<span><a href="<?php echo $_SERVER["PHP_SELF"] ?>?customer=<?php echo $customer ?>&cpuID=<?php echo $cpuID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page - 1 ?>" class="btn btn-sm btn-primary"><</a></span>
<?php } ?>

<?php if(!$is_guest) { ?>
<div style="float:right; margin-left: 10px;"><button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("./licenseSrvCSV.php?sqlCountRow=<?php echo base64_encode($sqlCountRow) ?>&license_tbl_name=<?php echo base64_encode($license_tbl_name) ?>", "downloadCSV");'>Download CSV<?php // echo $sqlCountRow ?></button></div>
<?php } ?>

<?php if($page<$totalPage) { ?>
<span style="float:right;"><a href="<?php echo $_SERVER["PHP_SELF"] ?>?customer=<?php echo $customer ?>&cpuID=<?php echo $cpuID ?>&dueFrom=<?php echo $dueFrom ?>&dueTo=<?php echo $dueTo ?>&page=<?php echo $page + 1 ?>" class="btn btn-sm btn-primary">></a></span>
<?php } ?>
</div>
</div>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>