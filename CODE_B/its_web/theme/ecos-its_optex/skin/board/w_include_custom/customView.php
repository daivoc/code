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

<style>
hr { border: none;margin-top: 4px;margin-bottom: 4px;clear: both; }
.wr8_Group, .wr9_Group { float:left;margin-right:4px; }
#wr8_IP, #wr9_IP { width: 25%; }
#wr8_Port, #wr9_Port { text-align: right;width:12%; }
/* #wr8_Opt1, #wr8_Opt2, #wr9_Opt1, #wr9_Opt2 { text-align: right;width:30%; } */
#wr8_Opt1, #wr9_Opt1 { width:60%; }
</style>

<tr class="w_detail_tr">
	<th scope="row"><label for="wr_8">ITS API Interface<br><a onclick='window.open("<?php echo G5_THEME_URL ?>/utility/filemanager/api_audio_common.php","Common_Audio", "width=600,height=500");'>Audio File</a></label></th>
	<td>
		<div style="width: 100%;">
        <input type='text' class='form-control wr8_Group' disabled id='wr8_IP' value='<?php echo $wr8_IP; ?>' placeholder='IP'>
        <input type='text' class='form-control wr8_Group' disabled id='wr8_Port' value='<?php echo $wr8_Port; ?>' placeholder='Port'>
        <input type='text' class='form-control wr8_Group' disabled id='wr8_Opt1' value='<?php echo $wr8_Opt1; ?>' placeholder='[{"audio":{"source":"1","volume":"30","loop":"0"}}]'>
		<input type='hidden' class='form-control wr8_Group' disabled id='wr8_Opt2' value='<?php echo $wr8_Opt2; ?>' placeholder='Opt2'>
		<hr>
        <input type='text' class='form-control wr9_Group' disabled id='wr9_IP' value='<?php echo $wr9_IP; ?>' placeholder='IP'>
        <input type='text' class='form-control wr9_Group' disabled id='wr9_Port' value='<?php echo $wr9_Port; ?>' placeholder='Port'>
        <input type='text' class='form-control wr9_Group' disabled id='wr9_Opt1' value='<?php echo $wr9_Opt1; ?>' placeholder='[{"gpio":{"status":"1","id":"P01","hold":"2.0","msg":"n/a"}}]'>
		<input type='hidden' class='form-control wr9_Group' disabled id='wr9_Opt2' value='<?php echo $wr9_Opt2; ?>' placeholder='Opt2'>
		</div>
	</td>
</tr>
