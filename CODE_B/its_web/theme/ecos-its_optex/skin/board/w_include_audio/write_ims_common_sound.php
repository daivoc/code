<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php');

if($member['mb_2']){
	$audio_path = G5_CU_AUD_PATH.'/'.$member['mb_2'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$member['mb_2'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

if($member['mb_3']) { 
	// echo $member['mb_3'];
} else { 
	$member['mb_3'] = '0';
} 

?>
<script type="text/javascript">
	$(function() {
		$("#upload").click(function(){
			$("#audio").click();
		});
		$("#audio").change(function(){
			$("#submit").click();
		});
		
		// 오디오 파일이 로딩되면 음원길이 값을 mb_3에 선언한다.
		$('audio')[0].onloadeddata = function() {
			$('#mb_3').val($('audio')[0].duration);
		};					
		$('.submit').on('click', function() {
			var file_data = $('.audio').prop('files')[0];
			var file_name = "<?php echo md5(time()).'.mp3'?>"; // $('.audio').val().split('\\').pop();
			if(file_data != undefined) {
				var form_data = new FormData();                  
				form_data.append('file', file_data);
				$.ajax({
					type: 'POST',
					url: '<?php echo G5_THEME_URL."/skin/board/w_include_audio/ims_common_mp3_upload.php?filename=" ?>'+file_name,
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
							
							$('#mb_2').val(file_name);

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
	});
</script>
<tr class='w_detail_tr'>
	<th scope="row" title="Audio Warning"><label for="w_warning">Audio Warning</label></th>
	<td>
	<form>
		<input style='display:none' id="audio" type="file" name="audio" class="audio">
		<input style='display:none' id="submit" type="submit" name="submit" class="submit" value="Submit">
	</form>			
	<input style='float:left;' type="button" value="Upload MP3" id="upload" class="btn">
	<input style='float:left;margin-left:4px;width:160px;text-align:right;' type="text" name="mb_2" value="<?php echo $member['mb_2'] ?>" id="mb_2" class='form-control' readonly placeholder='Name'>
	<input style='float:left;margin-left:4px;width:80px;text-align:right;' type="text" name="mb_3" value="<?php echo $member['mb_3'] ?>" id="mb_3" class='form-control' readonly placeholder='Second'>
	<audio controls style='float:left;height:36px;margin:4px;width:100%;'>
		<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
	</audio>
</td>
</tr>