<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_audio_field00.php');

if($write['w_audio3_name']){
	$audio_path = '/var/www/html/its_web/data/audio/'.$write['w_audio3_name'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$write['w_audio3_name'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

if($write['w_audio3_time']) { 
	// echo $write['w_audio3_time'];
} else { 
	$write['w_audio3_time'] = '0';
} 

?>

<tr class='w_detail_tr'>
	<th scope="row" title="Audio Warning"><label for="w_warning">Audio Zone #3</label></th>
	<td>
	<script type="text/javascript">
	function resetAudio_03() {
		$('#w_audio3_name, #w_audio3_time').val('');
	}
	$(function() {
		$("#upload_03").click(function(){
			$("#audio_03").click();
		});
		$("#audio_03").change(function(){
			$("#submit_03").click();
		});
		
		// 오디오 파일이 로딩되면 음원길이 값을 w_audio3_time에 선언한다.
		$('#audioCtrl_03')[0].onloadeddata = function() {
			$('#w_audio3_time').val($('#audioCtrl_03')[0].duration);
		};					
		$('.submit_03').on('click', function() {
			var file_data = $('.audio_03').prop('files')[0];
			var file_name = $('.audio_03').val().split('\\').pop();
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
							$('#audioCtrl_03 source').attr('src', audio_URL);
							$("#audioCtrl_03")[0].load();
							// $("audio_03")[0].play();
							
							$('#w_audio3_name').val(file_name);

						} else if(response == 'false') {
							alert('Invalid file type.');
						} else {
							alert('Something went wrong. Please try again.');
						}
	
						$('.audio_03').val('');
					}
				});
			}
			return false;
		});
	
		$('#w_audio3_name').on('click', function() {
			$.ajax({
				type: 'POST',
				url: '<?php echo $board_skin_url."/../w_include_audio/mp3_selectList.php" ?>',
				data: { 
					selected: $(this).val(),
					id:"03"
				},
				success:function(response) {
					$('#selectList_03').html(response);

					$("#audioList_03").change(function() {
						var audio_URL = 'http://<?php echo $_SERVER['HTTP_HOST']?>/data/audio/'+$(this).val();
						$('#audioCtrl_03 source').attr('src', audio_URL);
						$("#audioCtrl_03")[0].load();
						// $("audio_03")[0].play();
						$('#w_audio3_name').val($(this).val());
					});
				}
			});
		});
	});
	</script>
	<form>
		<input style='display:none' id="audio_03" type="file" name="audio_03" class="audio_03">
		<input style='display:none' id="submit_03" type="submit" name="submit_03" class="submit_03" value="Submit">
	</form>			
	<input style='float:left;' type="button" value="Upload" id="upload_03" class="btn btn-warning">
	<input type="text" name="w_audio3_name" value="<?php echo $write['w_audio3_name'] ?>" id="w_audio3_name" class='form-control audioName' readonly placeholder='Name'>
	<div id='selectList_03'></div>
	<input type="text" name="w_audio3_time" value="<?php echo $write['w_audio3_time'] ?>" id="w_audio3_time" class='form-control audioTime' placeholder='Second'>
	<audio controls class='audioCtrl' id='audioCtrl_03'>
		<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
	</audio>
	<input type="text" name="w_audio3_volume" value="<?php echo $write['w_audio3_volume'] ?>" id="w_audio3_volume" class='form-control audioVol' placeholder='Volume'>
	<input style='float:left;' type="button" value="Reset" onclick="resetAudio_03()" class="btn btn-danger">
	</td>
</tr>