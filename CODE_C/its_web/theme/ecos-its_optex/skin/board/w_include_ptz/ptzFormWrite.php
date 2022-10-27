<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>
<tr class='w_detail_tr'>
	<th scope='row'><label for='w_Tracking'>Auto Tracking<div id='ptzHelp'>help</div></label></th>
	<td>

		<table style='font-size: 8pt;color: gray;padding-right: 10px;'>
		<tr>
			<td style='width:120px'></td>
			<td>Length Cx from Sensor to PTZ</td>
			<td>Length Cy from Sensor to PTZ</td>
			<td>Height Ch from Sensor to PTZ</td>
			<td>Angle Ax from Camera angle 0 to Direction X +</td>
		</tr>
		<tr>
			<td style='padding-left: 20px;vertical-align: top;'>PTZ</td>
			<td><input type='text' name='w_ptzX' value='<?php echo $write['w_ptzX'] ?>' id='w_ptzX' class='form-control' placeholder='Length to PTZ (Cx)'></td>
			<td><input type='text' name='w_ptzY' value='<?php echo $write['w_ptzY'] ?>' id='w_ptzY' class='form-control' placeholder='Length to PTZ (Cy)'></td>
			<td><input type='text' name='w_ptzH' value='<?php echo $write['w_ptzH'] ?>' id='w_ptzH' class='form-control' placeholder='Height to PTZ (Ch)'></td>
			<td><input type='text' name='w_ptzA' value='<?php echo $write['w_ptzA'] ?>' id='w_ptzA' class='form-control' placeholder='Angle to X Plus (Ax)'></td>
		</tr>
		</table>
		
		<table style='display:none;font-size: 8pt;color: gray;padding-right: 10px;'>
		<tr>
			<td style='width:120px'></td>
			<td>Distance from Origin</td>
			<td>Angle Panning</td>
			<td>Angle Tilting</td>
			<td>Zoom</td>
		</tr>
		<tr>
			<td style='padding-left: 20px;'>Origin</td>
			<td><input type='text' name='w_distanceO' value='<?php echo $write['w_distanceO'] ?>' id='w_distanceO' class='form-control' placeholder='Distance to Origin' readonly></td>
			<td><input type='text' name='w_anglePanO' value='<?php echo $write['w_anglePanO'] ?>' id='w_anglePanO' class='form-control' placeholder='Angle to Sensor(P)'></td>
			<td><input type='text' name='w_angleTiltO' value='<?php echo $write['w_angleTiltO'] ?>' id='w_angleTiltO' class='form-control' placeholder='Angle to Sensor(T)'></td>
			<td><input type='text' name='w_zoomO' value='<?php echo $write['w_zoomO'] ?>' id='w_zoomO' class='form-control' placeholder='Zoom Level Origin'></td>
		</tr>
		<tr>
			<td style='padding-left: 20px;'>Spot A</td>
			<td><input type='text' name='w_distanceA' value='<?php echo $write['w_distanceA'] ?>' id='w_distanceA' class='form-control' placeholder='Distance to Spot A'></td>
			<td><input type='text' name='w_anglePanA' value='<?php echo $write['w_anglePanA'] ?>' id='w_anglePanA' class='form-control' placeholder='Angle Spot A(P)'></td>
			<td><input type='text' name='w_angleTiltA' value='<?php echo $write['w_angleTiltA'] ?>' id='w_angleTiltA' class='form-control' placeholder='Angle Spot A(T)'></td>
			<td><input type='text' name='w_zoomA' value='<?php echo $write['w_zoomA'] ?>' id='w_zoomA' class='form-control' placeholder='Zoom Level A'></td>
		</tr>
		<tr>
			<td style='padding-left: 20px;'>Spot B</td>
			<td><input type='text' name='w_distanceB' value='<?php echo $write['w_distanceB'] ?>' id='w_distanceB' class='form-control' placeholder='Distance to Spot B'></td>
			<td><input type='text' name='w_anglePanB' value='<?php echo $write['w_anglePanB'] ?>' id='w_anglePanB' class='form-control' placeholder='Angle Spot B(P)'></td>
			<td><input type='text' name='w_angleTiltB' value='<?php echo $write['w_angleTiltB'] ?>' id='w_angleTiltB' class='form-control' placeholder='Angle Spot B(T)'></td>
			<td><input type='text' name='w_zoomB' value='<?php echo $write['w_zoomB'] ?>' id='w_zoomB' class='form-control' placeholder='Zoom Level B'></td>
		</tr>
		</table>
		<table style='font-size: 8pt;color: gray;padding-right: 10px;'>
		<tr>
			<td style='width: 120px;padding-left: 20px;vertical-align: top;'>Camera URL</td>
			<td colspan=4>
			<input type='text' name='w_ptzCamURL' value='<?php echo $write['w_ptzCamURL'] ?>' id='w_ptzCamURL' class='form-control input75P' placeholder='URL Ex:http://192.168.0.38/axis-cgi/com/ptz.cgi?autofocus=on' size='50'>
			<span class='input16P' style='display:inline-block;text-align: center;float: right;' >
			<input type='checkbox' class='form-control' style='height: 30px;' name='w_ptzCamENC' id='w_ptzCamENC' value='1' <?php echo (($write['w_ptzCamENC'])?'checked':'') ?> title='w_ptzCamENC'>
			<label><?php echo $SK_BO_Encryption[ITS_Lang] ?></label>
			</span></td>
		</tr>
		</table>
		
		<table style='font-size: 8pt;color: gray;padding-right: 10px;'>
		<tr>
			<td style='width: 120px;padding-left: 20px;vertical-align: top;'>PresetA</td>
			<td>
				<input type='text' name='wr_4' value='<?php echo $write['wr_4'] ?>' id='wr_4' class='form-control input60P' placeholder='URL Ex:http://192.168.0.64/axis-cgi/com/ptz.cgi?setserverpresetname=' size='50'>
				<input type="text" name="wr_6" value="<?php echo $write['wr_6'] ?>" id="wr_6" class='form-control input20P' placeholder='Unit: (1000 = 1m)'>
				<span class='input16P' style='display:inline-block;text-align: center;float: right;' >
				<input type='checkbox' class='form-control' style='height: 30px;' name='wr_5' id='wr_5' value='1' <?php echo (($write['wr_5'])?'checked':'') ?> title='wr_5'>
				<label><?php echo $SK_BO_Encryption[ITS_Lang] ?></label>
				</span>
			</td>
		</tr>
		<tr>
			<td style='width: 120px;padding-left: 20px;vertical-align: top;'>PresetB</td>
			<td>
				<input type='text' name='wr_7' value='<?php echo $write['wr_7'] ?>' id='wr_7' class='form-control input60P' placeholder='URL Ex:http://192.168.0.64/axis-cgi/com/ptz.cgi?setserverpresetname=' size='50'>
				<input type="text" name="wr_9" value="<?php echo $write['wr_9'] ?>" id="wr_9" class='form-control input20P' placeholder='Unit: (1000 = 1m)'>
				<span class='input16P' style='display:inline-block;text-align: center;float: right;' >
				<input type='checkbox' class='form-control' style='height: 30px;' name='wr_8' id='wr_8' value='1' <?php echo (($write['wr_8'])?'checked':'') ?> title='wr_8'>
				<label><?php echo $SK_BO_Encryption[ITS_Lang] ?></label>
				</span>
			</td>
		</tr>
		</table>
		
	</td>
</tr>