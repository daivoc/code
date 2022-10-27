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
		// $sql = "SELECT wr_id, wr_subject FROM $write_table WHERE w_sensor_disable = 0";
		$sql = "SELECT wr_id, wr_subject, w_sensor_disable FROM $write_table";
		$result = sql_query($sql);
		while ($row = sql_fetch_array($result)) {
			$value_select = G5_BBS_URL."/board.php?bo_table=".$value."&wr_id=".$row['wr_id'];

			if($row['w_sensor_disable'])
				$subjectIs = "- ".$row['wr_subject'];
			else
				$subjectIs = "+ ".$row['wr_subject'];
			
			$sensor_list[] = $value_select;
			if($subject == $row['wr_subject'])
				$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$subjectIs.'</option>';
			else
				$select_w_sensor_devID .='<option value="'.$value_select.'">'.$subjectIs.'</option>';
		}
	}
}
$select_w_sensor_devID .= '</select>';
// 끝 등록된 디바이스(센서의 목록을 셀렉트 박스로 보여주고 선택된 값을 자신에게 적용하며 목록을 보여준다.)

if (count($sensor_list) == 1) {
	header ("Location: $sensor_list[0]"); 
} else {

if($subject) $titleIs = $subject; else $titleIs = "Config"; // 서브잭트명이 없으면 Log로..
$board['bo_subject'] = $titleIs;
?>

<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL ?>/jquery-ui.css">
<script src="<?php echo G5_THEME_JS_URL ?>/jquery-ui.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$('#w_sensor_devID').on('change', function() {
		window.open(this.value, "_self");
	});
});
</script>
<style>
.shadow { text-shadow: 4px 6px 4px black; }
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name"><?php echo $board['bo_subject'] ?></span>
            <hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>

<div id="bo_list" class="container">
<div style="margin:10px;text-align: center;">
<?php echo $select_w_sensor_devID ?>
</div>
</div>

<?php
include_once(G5_PATH.'/tail.php');
}
?>