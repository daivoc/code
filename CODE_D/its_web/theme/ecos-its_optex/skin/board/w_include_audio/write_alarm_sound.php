<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php');

if($write['wr_2']){
	$audio_path = '/var/www/html/its_web/data/audio/'.$write['wr_2'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$write['wr_2'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

if($write['wr_3']) { 
	// echo $write['wr_3'];
} else { 
	$write['wr_3'] = '0';
} 

?>
<table class="table table-bordered">
<tbody>
	<tr class='w_detail_tr'>
		<th scope="row" title="Audio Warning"><label for="w_warning">Audio Warning</label></th>
		<td>
			<script type="text/javascript">
				function resetAudio() {
					$('#wr_2').val('');
					$('#wr_3').val('0');
				}
				$(function() {
					$("#upload").click(function(){
						$("#audio").click();
					});
					$("#audio").change(function(){
						$("#submit").click();
					});
					
					// 오디오 파일이 로딩되면 음원길이 값을 wr_3에 선언한다.
					$('audio')[0].onloadeddata = function() {
						$('#wr_3').val($('audio')[0].duration);
					};					
					$('.submit').on('click', function() {
						var file_data = $('.audio').prop('files')[0];
						var file_name = $('.audio').val().split('\\').pop();
						if(file_data != undefined) {
							var form_data = new FormData();                  
							form_data.append('file', file_data);
							$.ajax({
								type: 'POST',
								url: '<?php echo $board_skin_url."/../w_include_audio/mp3_upload.php" ?>',
								contentType: false,
								processData: false,
								data: form_data,
								success:function(response) {
									// alert(response);
									if(response == 'success') {
										alert('File uploaded successfully.');
										
										var audio_URL = 'http://<?php echo $_SERVER['HTTP_HOST']?>/data/audio/'+file_name;
										$('audio source').attr('src', audio_URL);
										$("audio")[0].load();
										// $("audio")[0].play();
										
										$('#wr_2').val(file_name);

									} else if(response == 'false') {
										alert('Invalid file type.');
									} else {
										alert('Something went wrong. Please try again.');
									}
			 
									$('.audio').val('');
								}
							});
						}
						return false;
					});
				
					$('#wr_2').on('click', function() {
						$.ajax({
							type: 'POST',
							url: '<?php echo $board_skin_url."/../w_include_audio/mp3_selectList.php" ?>',
							data: { selected: $(this).val() },
							success:function(response) {
								$('#selectList').html(response);

								$("#audioList").change(function() {
									var audio_URL = 'http://<?php echo $_SERVER['HTTP_HOST']?>/data/audio/'+$(this).val();
									$('audio source').attr('src', audio_URL);
									$("audio")[0].load();
									// $("audio")[0].play();
									$('#wr_2').val($(this).val());
								});
							}
						});
					});
				});
			</script>
			<form>
				<input style='display:none' id="audio" type="file" name="audio" class="audio">
				<input style='display:none' id="submit" type="submit" name="submit" class="submit" value="Submit">
			</form>			
			<input style='float:left;' type="button" value="Upload MP3" id="upload" class="btn btn-warning">
			<input style='float:left;margin-left:4px;width:200px;text-align:right;' type="text" name="wr_2" value="<?php echo $write['wr_2'] ?>" id="wr_2" class='form-control' readonly placeholder='Name'>
			<div id='selectList'></div>
			<input style='float:left;margin-left:4px;width:80px;text-align:right;' type="text" name="wr_3" value="<?php echo $write['wr_3'] ?>" id="wr_3" class='form-control' placeholder='Second'>
			<audio controls style='float:left;height:36px;margin-left:4px;'>
				<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
			</audio>
			<input style='float:left;' type="button" value="Reset" onclick="resetAudio()" class="btn btn-danger">
		</td>
	</tr>
	</tbody>
</table>