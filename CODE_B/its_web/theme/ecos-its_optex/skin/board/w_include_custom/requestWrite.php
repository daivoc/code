<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
if($write['wr_4']) {
    list($wr4_Addr, $wr4_Para, $wr4_Encry, $wr4_Type) = explode("||", $write['wr_4']);
    if($wr4_Encry) $wr4_Encry = "checked";
    if($wr4_Type) $wr4_Type = "checked";
}
if($write['wr_5']) {
    list($wr5_Addr, $wr5_Para, $wr5_Encry, $wr5_Type) = explode("||", $write['wr_5']);
    if($wr5_Encry) $wr5_Encry = "checked";
    if($wr5_Type) $wr5_Type = "checked";
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
        if ($('#wr4_Type').is(":checked")) { 
            var wr4_Type = 1;
        } else {
            var wr4_Type = 0;
        }
        if($('#wr4_Addr').val() && $('#wr4_Para').val()) {
            var wr4_Value = $('#wr4_Addr').val() + '||' + $('#wr4_Para').val() + '||' + wr4_Encry + '||' + wr4_Type;
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
        if ($('#wr5_Type').is(":checked")) { 
            var wr5_Type = 1;
        } else {
            var wr5_Type = 0;
        }
        if($('#wr5_Addr').val() && $('#wr5_Para').val()) {
            var wr5_Value = $('#wr5_Addr').val() + '||' + $('#wr5_Para').val() + '||' + wr5_Encry + '||' + wr5_Type;
            $('#wr_5').val(wr5_Value);
        } else {
            $('#wr_5').val('');
        }
	})	
});
</script>

<style>
hr { border: none;margin-top: 4px;margin-bottom: 4px;clear: both; }
.wr4_Group, .wr5_Group { float:left; display: grid; }
#wr4_Addr, #wr5_Addr { width: 40%; }
#wr4_Para, #wr5_Para { text-align: right;width: 40%; margin-right:4px; }
#wr4_Encry, #wr5_Encry, #wr4_Type, #wr5_Type { height:20px; width:20px;}
.wr_Encry, .wr_Type { width: 8%; margin-left: 4px; height:20px; }
.wr_Encry label, .wr_Type label { font-weight: normal; }
</style>

<table class="table table-bordered">
<tbody>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_4">Http Request</th>
	<td>
		<div style="width: 100%;">
		<input type='hidden' name='wr_4' value='<?php echo $write['wr_4'] ?>' id='wr_4'>
		<input type='text' class='form-control wr4_Group' id='wr4_Addr' value='<?php echo $wr4_Addr; ?>' placeholder='URL Ex:https://id:pass@ip.address:52001/path'>
		<input type='text' class='form-control wr4_Group' id='wr4_Para' value='<?php echo $wr4_Para; ?>' placeholder='Json or XML :_curTime_'>
		<span class='wr4_Group wr_Encry'><input type="checkbox" class="form-control wr4_Group" id="wr4_Encry" <?php echo $wr4_Encry ?> value="1" title="Default Get"><label>Post</label></span>
		<span class='wr4_Group wr_Type'><input type="checkbox" class="form-control wr4_Group" id="wr4_Type" <?php echo $wr4_Type ?> value="1" title="Default Json"><label>XML</label></span>
		<hr>
		<input type='hidden' name='wr_5' value='<?php echo $write['wr_5'] ?>' id='wr_5'>
		<input type='text' class='form-control wr5_Group' id='wr5_Addr' value='<?php echo $wr5_Addr; ?>' placeholder='URL Ex:https://id:pass@ip.address:52001/path'>
		<input type='text' class='form-control wr5_Group' id='wr5_Para' value='<?php echo $wr5_Para; ?>' placeholder='Json or XML :_curTime_'>
		<span class='wr5_Group wr_Encry'><input type="checkbox" class="form-control wr5_Group" id="wr5_Encry" <?php echo $wr5_Encry ?> value="1" title="Post or Get"><label>Post</label></span>
		<span class='wr5_Group wr_Type'><input type="checkbox" class="form-control wr5_Group" id="wr5_Type" <?php echo $wr5_Type ?> value="1" title="XML or Json"><label>XML</label></span>
		</div>
	</td>
</tr>
</tbody>
</table>