<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_4">PresetA</label></th>
	<td>
		<input type='text' name='wr_4' value='<?php echo $write['wr_4'] ?>' id='wr_4' class='form-control input60P' placeholder='URL Ex:http://192.168.0.64/axis-cgi/com/ptz.cgi?setserverpresetname=' size='50'>
		<input type='checkbox' class='form-control input16P' style='height: 30px;' name='wr_5' id='wr_5' value='1' <?php echo (($write['wr_5'])?'checked':'') ?> title='wr_5'>
		<input type="text" name="wr_6" value="<?php echo $write['wr_6'] ?>" id="wr_6" class='form-control input20P' placeholder='Preset ID'>
	</td>
</tr>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_7">PresetB</label></th>
	<td>
		<input type='text' name='wr_7' value='<?php echo $write['wr_7'] ?>' id='wr_7' class='form-control input60P' placeholder='URL Ex:http://192.168.0.64/axis-cgi/com/ptz.cgi?setserverpresetname=' size='50'>
		<input type='checkbox' class='form-control input16P' style='height: 30px;' name='wr_8' id='wr_8' value='1' <?php echo (($write['wr_8'])?'checked':'') ?> title='wr_8'>
		<input type="text" name="wr_9" value="<?php echo $write['wr_9'] ?>" id="wr_9" class='form-control input20P' placeholder='Preset ID'>
	</td>
</tr>
