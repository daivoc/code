<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

		<tr class='w_detail_tr'>
			<th scope='row'><label for='w_Tracking'>Auto Tracking</label></th>
			<td>
				<table style='font-size: 8pt;color: gray;padding-right: 10px;'>
				<tr>
					<td style='width:120px'></td>
					<td>Length X from Sensor to PTZ</td>
					<td>Length Y from Sensor to PTZ</td>
					<td>Height from Sensor to PTZ</td>
					<td>Angle to Direction X +</td>
				</tr>
				<tr>
					<td style='padding-left: 20px;'>PTZ</td>
					<td><?php echo $view['w_ptzX'] ?></td>
					<td><?php echo $view['w_ptzY'] ?></td>
					<td><?php echo $view['w_ptzH'] ?></td>
					<td><?php echo $view['w_ptzA'] ?></td>
				</tr>
				</table>

				<table style='display: none;font-size: 8pt;color: gray;padding-right: 10px;'>
				<tr>
					<td style='width:120px'></td>
					<td>Distance from Origin</td>
					<td>Angle Panning</td>
					<td>Angle Tilting</td>
					<td>Zoom</td>
				</tr>
				<tr>
					<td style='padding-left: 20px;'><a href='<?php echo $view['w_ptzCamURL'] ?>&pan=<?php echo $view['w_anglePanO'] ?>&tilt=<?php echo $view['w_angleTiltO'] ?>&zoom=<?php echo $view['w_zoomO'] ?>'>Origin</a></td>
					<td><?php echo $view['w_distanceO'] ?></td>
					<td><?php echo $view['w_anglePanO'] ?></td>
					<td><?php echo $view['w_angleTiltO'] ?></td>
					<td><?php echo $view['w_zoomO'] ?></td>
				</tr>
				<tr>
					<td style='padding-left: 20px;'><a href='<?php echo $view['w_ptzCamURL'] ?>&pan=<?php echo $view['w_anglePanA'] ?>&tilt=<?php echo $view['w_angleTiltA'] ?>&zoom=<?php echo $view['w_zoomA'] ?>'>Spot A</a></td>
					<td><?php echo $view['w_distanceA'] ?></td>
					<td><?php echo $view['w_anglePanA'] ?></td>
					<td><?php echo $view['w_angleTiltA'] ?></td>
					<td><?php echo $view['w_zoomA'] ?></td>
				</tr>
				<tr>
					<td style='padding-left: 20px;'><a href='<?php echo $view['w_ptzCamURL'] ?>&pan=<?php echo $view['w_anglePanB'] ?>&tilt=<?php echo $view['w_angleTiltB'] ?>&zoom=<?php echo $view['w_zoomB'] ?>'>Spot B</a></td>
					<td><?php echo $view['w_distanceB'] ?></td>
					<td><?php echo $view['w_anglePanB'] ?></td>
					<td><?php echo $view['w_angleTiltB'] ?></td>
					<td><?php echo $view['w_zoomB'] ?></td>
				</tr>
				</table>
				<table style='font-size: 8pt;color: gray;padding-right: 10px;'>
				<tr>
					<td style='width: 120px;padding-left: 20px;'>Camera URL</td>
					<td colspan=4><?php echo $view['w_ptzCamURL'] ." ".(($view['w_ptzCamENC'])?'checked':'unchecked') ?> -> encryption</td>
				</tr>
				</table>
				
				<table style='font-size: 8pt;color: gray;padding-right: 10px;'>
				<tr>
					<td style='width: 120px;padding-left: 20px;'>PresetA</td>
					<td>
						<?php echo $view['wr_4'] ?> : <?php echo $view['wr_5'] ?> : <?php echo $view['wr_6'] ?>
					</td>
				</tr>
				<tr>
					<td style='width: 120px;padding-left: 20px;'>PresetB</td>
					<td>
						<?php echo $view['wr_7'] ?> : <?php echo $view['wr_8'] ?> : <?php echo $view['wr_9'] ?>
					</td>
				</tr>
				</table>
			</td>
		</tr>	