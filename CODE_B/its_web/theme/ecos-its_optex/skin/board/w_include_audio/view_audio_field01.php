<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/view_audio_field00.php');

if($view['w_audio1_name']){
	$audio_path = '/var/www/html/its_web/data/audio/'.$view['w_audio1_name'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$view['w_audio1_name'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

?>
	<tr class='w_detail_tr'>
		<th scope="row" title="Audio Warning"><label for="w_warning">Audio Zone #1</label></th>
		<td>
			<input style='float:left;margin-left:4px;width:200px;text-align:center;' type="text" value="<?php echo $view['w_audio1_name'] ?>" class='form-control' readonly>
			<audio controls style='float:left;height:36px;margin-left:4px;'>
				<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
			</audio>
			<input style='float:left;margin-left:4px;width:60px;text-align:center;' type="text" value="<?php echo $view['w_audio1_volume'] ?>" class='form-control' readonly>
		</td>
	</tr>
