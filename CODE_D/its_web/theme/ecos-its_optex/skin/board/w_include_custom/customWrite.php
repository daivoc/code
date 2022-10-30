<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
if($write['wr_8']) {
    list($wr8_IP, $wr8_Port, $wr8_Opt1) = explode("||", $write['wr_8']);
}
if($write['wr_9']) {
    list($wr9_IP, $wr9_Port, $wr9_Opt1) = explode("||", $write['wr_9']);
}
?>

<script>
$(document).ready(function(){
	$('.wr8_Group').change(function(){
		if($('#wr8_IP').val() && $('#wr8_Port').val() && $('#wr8_Opt1').val()) {
			// var wr8_Value = '||||' + $('#wr8_IP').val() + '||' + $('#wr8_Port').val() + '||' + $('#wr8_Opt1').val() + '||' + $('#wr8_Opt2').val();
			var wr8_Value = $('#wr8_IP').val() + '||' + $('#wr8_Port').val() + '||' + $('#wr8_Opt1').val();
			$('#wr_8').val(wr8_Value);
			$('.wr8_Group').css('background-color', "#ebffcc");
		} else {
			$('#wr_8').val('');
			$('.wr8_Group').css('background-color', "#fff2de");
		}
	})	
	$('.wr9_Group').change(function(){
		if($('#wr9_IP').val() && $('#wr9_Port').val() && $('#wr9_Opt1').val()) {
			// var wr9_Value = '||||' + $('#wr9_IP').val() + '||' + $('#wr9_Port').val() + '||' + $('#wr9_Opt1').val() + '||' + $('#wr9_Opt2').val();
			var wr9_Value = $('#wr9_IP').val() + '||' + $('#wr9_Port').val() + '||' + $('#wr9_Opt1').val();
			$('#wr_9').val(wr9_Value);
			$('.wr9_Group').css('background-color', "#ebffcc");
		} else {
			$('#wr_9').val('');
			$('.wr9_Group').css('background-color', "#fff2de");
		}
	})	
});
</script>

<style>
hr { border: none;margin-top: 4px;margin-bottom: 4px;clear: both; }
.wr8_Group, .wr9_Group { float:left;margin-right:4px; }
#wr8_IP, #wr9_IP { width: 25%; }
#wr8_Port, #wr9_Port { text-align: right;width:12%; }
/* #wr8_Opt1, #wr8_Opt2, #wr9_Opt1, #wr9_Opt2 { text-align: right;width:30%; } */
#wr8_Opt1, #wr9_Opt1 { width:60%; }
</style>

<table class="table table-bordered">
<tbody>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_8">ITS API Interface<br><a onclick='window.open("<?php echo G5_THEME_URL ?>/utility/filemanager/api_audio_common.php","Common_Audio", "width=600,height=500");'>Audio File</a></label></th>
	

	<td>
		<div style="width: 100%;">
        <input type='hidden' name='wr_8' value='<?php echo $write['wr_8'] ?>' id='wr_8'>
        <input type='text' class='form-control wr8_Group' id='wr8_IP' value='<?php echo $wr8_IP; ?>' placeholder='192.168.0.20'>
        <input type='text' class='form-control wr8_Group' id='wr8_Port' value='34001' placeholder='34001'>
        <input type='text' class='form-control wr8_Group' id='wr8_Opt1' value='<?php echo $wr8_Opt1; ?>' placeholder='[{"audio":{"source":"1","volume":"30","loop":"0"}}]'>
		<input type='hidden' class='form-control wr8_Group' id='wr8_Opt2' value='<?php echo $wr8_Opt2; ?>' placeholder='Opt2'>
		<hr>
        <input type='hidden' name='wr_9' value='<?php echo $write['wr_9'] ?>' id='wr_9'>
        <input type='text' class='form-control wr9_Group' id='wr9_IP' value='<?php echo $wr9_IP; ?>' placeholder='192.168.0.20'>
        <input type='text' class='form-control wr9_Group' id='wr9_Port' value='34001' placeholder='34001'>
        <input type='text' class='form-control wr9_Group' id='wr9_Opt1' value='<?php echo $wr9_Opt1; ?>' placeholder='[{"gpio":{"status":"1","id":"P01","hold":"2.0","msg":"n/a"}}]'>
		<input type='hidden' class='form-control wr9_Group' id='wr9_Opt2' value='<?php echo $wr9_Opt2; ?>' placeholder='Opt2'>
		</div>
	</td>
</tr>
</tbody>
</table>
