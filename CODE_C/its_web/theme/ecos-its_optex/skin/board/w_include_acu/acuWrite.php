<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
$acuZoneID = array( // Alert
	0 => 'All Zone',
	1 => 'Zone 01',
	2 => 'Zone 02',
	3 => 'Zone 03',
	4 => 'Zone 04'
);

function select_w_Zone($acuZone, $acuZoneID) {
	$select_Zone = '<select class="form-control acuGroup" id="acuZone" >';
	while (list($key, $value) = each($acuZoneID)) { 
		if($acuZone == $key) {
			$select_Zone .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_Zone .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_Zone .= '</select>';
	return $select_Zone;
}

$itsOutID = array( // Alert
	18 => 'Relay 01',
	23 => 'Relay 02',
	24 => 'Relay 03',
	25 => 'Relay 04'
);

$acuOutID = array( // Alert
	1 => 'Relay 01',
	2 => 'Relay 02',
	3 => 'Relay 03',
	4 => 'Relay 04',
	5 => 'Relay 05',
	6 => 'Relay 06',
	7 => 'Relay 07',
	8 => 'Relay 08',
	9 => 'Relay 09',
	10 => 'Relay 10',
	11 => 'Relay 11',
	12 => 'Relay 12',
	13 => 'Relay 13',
	14 => 'Relay 14',
	15 => 'Relay 15',
	16 => 'Relay 16'
);

function select_w_ACU($acuID, $acuOutID) {
	$select_ACU = '<select class="form-control acuGroup" id="acuID" ><option value="" disabled selected>ACU ID</option>';
	while (list($key, $value) = each($acuOutID)) { 
		if($acuID == $key) {
			$select_ACU .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_ACU .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_ACU .= '</select>';
	return $select_ACU;
}

if($write['wr_10']) {
	list($acuIP, $acuPort, $acuID, $acuZone, $acuTime, $acuEncryption) = explode("||", $write['wr_10']);
	if($acuEncryption) $acuEncryption = "checked";
}
?>

<style>
.acuGroup { float:left; display: grid; margin-right:4px;}
#acuIP { width:25%; }
#acuPort, #acuTime { text-align: right;width: 10%; }
#acuID, #acuZone { text-align: right;width: 15%; }
#acuEncryption { margin-left: 6px; width:20px;height:20px; }
.acuEncry { width: 10%; height:20px; }
</style>


<script>
$(document).ready(function(){
	// $('.acuGroup').change(function(){
	$('.acuGroup, #acuIP, #acuPort, #acuID, #acuZone, #acuTime, #acuEncryption').change(function(){
		if ($('#acuEncryption').is(":checked")) { 
			var acuEncryption = 1;
		} else {
			var acuEncryption = 0;
		}
		var acuValue = $('#acuIP').val() + '||' + $('#acuPort').val() + '||' + $('#acuID').val() + '||' + $('#acuZone').val() + '||' + $('#acuTime').val() + '||' + acuEncryption;
		if ($('#acuIP').val() && $('#acuPort').val() && $('#acuID').val() && $('#acuZone').val() && parseFloat($('#acuTime').val())) {
			$('#wr_10').val(acuValue);
		} else {
			$('#wr_10').val('');
		}
	})	
});
</script>
<table class="table table-bordered">
<tbody>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_10">ITS_ACU</label></th>
	<td>
		<input type='hidden' name='wr_10' value='<?php echo $write['wr_10'] ?>' id='wr_10'>
		<input type='text' class='form-control acuGroup' id='acuIP' value='<?php if ($acuIP) echo $acuIP; else echo ""; ?>' placeholder='ACU IP'>
		<input type='text' class='form-control acuGroup' id='acuPort' value='<?php if ($acuPort) echo $acuPort; else echo "0"; ?>' placeholder='8040'>
		<?php echo select_w_ACU($acuID, $acuOutID); ?>
		<?php // echo select_w_ACU($acuID, $itsOutID); ?>
		<?php echo select_w_Zone($acuZone, $acuZoneID); ?>
		<input type='text' class='form-control acuGroup' id='acuTime' value='<?php if ($acuTime) echo $acuTime; else echo "0"; ?>' placeholder='ACU Time'>
		<span class='acuGroup acuEncry'><input type="checkbox" class="form-control acuGroup" id="acuEncryption" <?php echo $acuEncryption ?> value="1"><label>암호화</label></span>
	</td>
</tr>
</tbody>
</table>