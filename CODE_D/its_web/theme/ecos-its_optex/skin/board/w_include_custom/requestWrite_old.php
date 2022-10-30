<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
if($write['wr_4']) {
    list($wr4_User, $wr4_Pass, $wr4_URL, $wr4_Encry) = explode("||", $write['wr_4']);
    if($wr4_Encry) $wr4_Encry = "checked";
}
if($write['wr_5']) {
    list($wr5_User, $wr5_Pass, $wr5_URL, $wr5_Encry) = explode("||", $write['wr_5']);
    if($wr5_Encry) $wr5_Encry = "checked";
}
?>

<script>
$(document).ready(function(){
	$('.wr4_Group').change(function(){
        if ($('#wr4_Encry').is(":checked")) { 
            var wr4_Encry = 1;
        } else {
            var wr4_Encry = 0;
        }
        if($('#wr4_URL').val()) {
            var wr4_Value = $('#wr4_User').val() + '||' + $('#wr4_Pass').val() + '||' + $('#wr4_URL').val() + '||' + wr4_Encry;
            $('#wr_4').val(wr4_Value);
        } else {
            $('#wr_4').val('');
        }
	})	
	$('.wr5_Group').change(function(){
        if ($('#wr5_Encry').is(":checked")) { 
            var wr5_Encry = 1;
        } else {
            var wr5_Encry = 0;
        }
        if($('#wr5_URL').val()) {
            var wr5_Value = $('#wr5_User').val() + '||' + $('#wr5_Pass').val() + '||' + $('#wr5_URL').val() + '||' + wr5_Encry;
            $('#wr_5').val(wr5_Value);
        } else {
            $('#wr_5').val('');
        }
	})	
});
</script>

<style>
.wr4_Group, .wr5_Group { float:left; display: grid; }
#wr4_URL, #wr5_URL { width: 50%; }
#wr4_User, #wr4_Pass, #wr5_User, #wr5_Pass { text-align: right;width: 20%;margin-right:4px; }
#wr4_Encry, #wr5_Encry { margin-left: 6px; width:20px;height:20px; }
.wr_Encry { width: 8%;  }
</style>

<table class="table table-bordered">
<tbody>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_4">Request 1/2</label></th>
	<td>
		<div style="width: 100%;">
		<input type='hidden' name='wr_4' value='<?php echo $write['wr_4'] ?>' id='wr_4'>
		<input type='text' class='form-control wr4_Group' id='wr4_User' value='<?php echo $wr4_User; ?>' placeholder='User'>
		<input type='text' class='form-control wr4_Group' id='wr4_Pass' value='<?php echo $wr4_Pass; ?>' placeholder='Pass'>
		<input type='text' class='form-control wr4_Group' id='wr4_URL' value='<?php echo $wr4_URL; ?>' placeholder='http://ip/option'>
		<span class='wr4_Group wr_Encry'><input type="checkbox" class="form-control wr4_Group" id="wr4_Encry" <?php echo $wr4_Encry ?> value="1"><label>암호화</label></span>
		</div>
		<div style="width: 100%;">
		<input type='hidden' name='wr_5' value='<?php echo $write['wr_5'] ?>' id='wr_5'>
		<input type='text' class='form-control wr5_Group' id='wr5_User' value='<?php echo $wr5_User; ?>' placeholder='User'>
		<input type='text' class='form-control wr5_Group' id='wr5_Pass' value='<?php echo $wr5_Pass; ?>' placeholder='Pass'>
		<input type='text' class='form-control wr5_Group' id='wr5_URL' value='<?php echo $wr5_URL; ?>' placeholder='http://ip/option'>
		<span class='wr5_Group wr_Encry'><input type="checkbox" class="form-control wr5_Group" id="wr5_Encry" <?php echo $wr5_Encry ?> value="1"><label>암호화</label></span>
		</div>
	</td>
</tr>
</tbody>
</table>