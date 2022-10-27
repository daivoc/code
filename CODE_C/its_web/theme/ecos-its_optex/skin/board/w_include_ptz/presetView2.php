<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

		<tr class='w_detail_tr'>
			<th scope='row'><label for='w_Preset'>Custom<br>Request</label></th>
			<td>
				<table style='width: 100%;font-size: 8pt;color: gray;padding-right: 10px;'>
				<tr>
					<td>
						<?php // echo $view['wr_4'] ?>
						<input type='text' name='wr_4' value='<?php echo $view['wr_4'] ?>' id='wr_4' readonly class='form-control'>
					</td>
				</tr>
				<tr>
					<td>
						<?php // echo $view['wr_5'] ?>
						<input type='text' name='wr_5' value='<?php echo $view['wr_5'] ?>' id='wr_5' readonly class='form-control'>
					</td>
				</tr>
				<!-- tr>
					<td style='padding-left: 20px;'>Request 3</td>
					<td>
						<?php // echo $view['wr_6'] ?>
					</td>
				</tr>
				<tr>
					<td style='padding-left: 20px;'>Request 4</td>
					<td>
						<?php // echo $view['wr_7'] ?>
					</td>
				</tr -->
				</table>
			</td>
		</tr>	