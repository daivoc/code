<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가

if($view['wr_2']){
	$audio_path = '/var/www/html/its_web/data/audio/'.$view['wr_2'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$view['wr_2'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

?>
	<tr class='w_detail_tr'>
		<th scope="row" title="Audio Warning"><label for="w_warning">Audio Warning</label></th>
		<td>
			<input style='float:left;margin-left:4px;width:200px;text-align:center;' type="text" value="<?php echo $view['wr_2'] ?>" class='form-control' readonly>
			<audio controls style='float:left;height:36px;margin-left:4px;'>
				<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
			</audio>
		</td>
	</tr>
