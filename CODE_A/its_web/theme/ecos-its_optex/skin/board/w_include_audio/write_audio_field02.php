<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_audio_field00.php');

if($write['w_audio2_name']){
	$audio_path = '/var/www/html/its_web/data/audio/'.$write['w_audio2_name'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$write['w_audio2_name'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

if($write['w_audio2_time']) { 
	// echo $write['w_audio2_time'];
} else { 
	$write['w_audio2_time'] = '0';
} 

?>

<tr class='w_detail_tr'>
	<th scope="row" title="Audio Warning"><label for="w_warning">Audio Zone #2</label></th>
	<td>
	<script type="text/javascript">
	function resetAudio_02() {
		$('#w_audio2_name, #w_audio2_time').val('');
	}
	$(function() {
		$("#upload_02").click(function(){
			$("#audio_02").click();
		});
		$("#audio_02").change(function(){
			$("#submit_02").click();
		});
		
		// 오디오 파일이 로딩되면 음원길이 값을 w_audio2_time에 선언한다.
		$('#audioCtrl_02')[0].onloadeddata = function() {
			$('#w_audio2_time').val($('#audioCtrl_02')[0].duration);
		};					
		$('.submit_02').on('click', function() {
			var file_data = $('.audio_02').prop('files')[0];
			var file_name = $('.audio_02').val().split('\\').pop();
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
							$('#audioCtrl_02 source').attr('src', audio_URL);
							$("#audioCtrl_02")[0].load();
							// $("audio_02")[0].play();
							
							$('#w_audio2_name').val(file_name);

						} else if(response == 'false') {
							alert('Invalid file type.');
						} else {
							alert('Something went wrong. Please try again.');
						}
	
						$('.audio_02').val('');
					}
				});
			}
			return false;
		});
	
		$('#w_audio2_name').on('click', function() {
			$.ajax({
				type: 'POST',
				url: '<?php echo $board_skin_url."/../w_include_audio/mp3_selectList.php" ?>',
				data: { 
					selected: $(this).val(),
					id:"02"
				},
				success:function(response) {
					$('#selectList_02').html(response);

					$("#audioList_02").change(function() {
						var audio_URL = 'http://<?php echo $_SERVER['HTTP_HOST']?>/data/audio/'+$(this).val();
						$('#audioCtrl_02 source').attr('src', audio_URL);
						$("#audioCtrl_02")[0].load();
						// $("audio_02")[0].play();
						$('#w_audio2_name').val($(this).val());
					});
				}
			});
		});
	});
	</script>
	<form>
		<input style='display:none' id="audio_02" type="file" name="audio_02" class="audio_02">
		<input style='display:none' id="submit_02" type="submit" name="submit_02" class="submit_02" value="Submit">
	</form>			
	<input style='float:left;' type="button" value="Upload" id="upload_02" class="btn btn-warning">
	<input type="text" name="w_audio2_name" value="<?php echo $write['w_audio2_name'] ?>" id="w_audio2_name" class='form-control audioName' readonly placeholder='Name'>
	<div id='selectList_02'></div>
	<input type="text" name="w_audio2_time" value="<?php echo $write['w_audio2_time'] ?>" id="w_audio2_time" class='form-control audioTime' placeholder='Second'>
	<audio controls class='audioCtrl' id='audioCtrl_02'>
		<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
	</audio>
	<input type="text" name="w_audio2_volume" value="<?php echo $write['w_audio2_volume'] ?>" id="w_audio2_volume" class='form-control audioVol' placeholder='Volume'>
	<input style='float:left;' type="button" value="Reset" onclick="resetAudio_02()" class="btn btn-danger">
	</td>
</tr>