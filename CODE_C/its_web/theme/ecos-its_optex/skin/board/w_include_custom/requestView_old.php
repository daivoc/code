<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
if($view['wr_4']) {
    list($wr4_User, $wr4_Pass, $wr4_URL, $wr4_Encry) = explode("||", $view['wr_4']);
    if($wr4_Encry) $wr4_Encry = "checked";
}
if($view['wr_5']) {
    list($wr5_User, $wr5_Pass, $wr5_URL, $wr5_Encry) = explode("||", $view['wr_5']);
    if($wr5_Encry) $wr5_Encry = "checked";
}
?>

<style>
.wr4_Group, .wr5_Group { float:left; display: grid; }
#wr4_URL, #wr5_URL { width: 50%; }
#wr4_User, #wr4_Pass, #wr5_User, #wr5_Pass { text-align: right;width: 20%;margin-right:4px; }
#wr4_Encry, #wr5_Encry { margin-left: 6px; width:20px;height:20px; }
.wr_Encry { width: 8%;  }
</style>

<tr class="w_detail_tr">
	<th scope="row"><label for="wr_4">Request 1/2</label></th>
	<td>
		<div style="width: 100%;">
        <input type='text' class='form-control wr4_Group' disabled id='wr4_User' value='<?php echo $wr4_User; ?>' placeholder='User'>
        <input type='text' class='form-control wr4_Group' disabled id='wr4_Pass' value='<?php echo $wr4_Pass; ?>' placeholder='Pass'>
        <input type='text' class='form-control wr4_Group' disabled id='wr4_URL' value='<?php echo $wr4_URL; ?>' placeholder='URL - http://ip/option'>
        <span class='wr4_Group wr_Encry'><input type="checkbox" class="form-control wr4_Group" disabled id="wr4_Encry" <?php echo $wr4_Encry ?> value="1"><label>암호화</label></span>
		</div>
		<div style="width: 100%;">
        <input type='text' class='form-control wr5_Group' disabled id='wr5_User' value='<?php echo $wr5_User; ?>' placeholder='User'>
        <input type='text' class='form-control wr5_Group' disabled id='wr5_Pass' value='<?php echo $wr5_Pass; ?>' placeholder='Pass'>
        <input type='text' class='form-control wr5_Group' disabled id='wr5_URL' value='<?php echo $wr5_URL; ?>' placeholder='URL - http://ip/option'>
        <span class='wr5_Group wr_Encry'><input type="checkbox" class="form-control wr5_Group" disabled id="wr5_Encry" <?php echo $wr5_Encry ?> value="1"><label>암호화</label></span>
		</div>
	</td>
</tr>
