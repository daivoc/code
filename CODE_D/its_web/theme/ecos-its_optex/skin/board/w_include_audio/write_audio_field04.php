<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_audio_field00.php');

if($write['w_audio4_name']){
	$audio_path = '/var/www/html/its_web/data/audio/'.$write['w_audio4_name'];
	if (file_exists($audio_path)) {
		$audio_URL = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/'.$write['w_audio4_name'];
	} else {
		$audio_URL = '';
	}
} else {
	$audio_URL = '';
}

if($write['w_audio4_time']) { 
	// echo $write['w_audio4_time'];
} else { 
	$write['w_audio4_time'] = '0';
} 

?>

<tr class='w_detail_tr'>
	<th scope="row" title="Audio Warning"><label for="w_warning">Audio Zone #4</label></th>
	<td>
	<script type="text/javascript">
	function resetAudio_04() {
		$('#w_audio4_name, #w_audio4_time').val('');
	}
	$(function() {
		$("#upload_04").click(function(){
			$("#audio_04").click();
		});
		$("#audio_04").change(function(){
			$("#submit_04").click();
		});
		
		// 오디오 파일이 로딩되면 음원길이 값을 w_audio4_time에 선언한다.
		$('#audioCtrl_04')[0].onloadeddata = function() {
			$('#w_audio4_time').val($('#audioCtrl_04')[0].duration);
		};					
		$('.submit_04').on('click', function() {
			var file_data = $('.audio_04').prop('files')[0];
			var file_name = $('.audio_04').val().split('\\').pop();
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
							$('#audioCtrl_04 source').attr('src', audio_URL);
							$("#audioCtrl_04")[0].load();
							// $("audio_04")[0].play();
							
							$('#w_audio4_name').val(file_name);

						} else if(response == 'false') {
							alert('Invalid file type.');
						} else {
							alert('Something went wrong. Please try again.');
						}
	
						$('.audio_04').val('');
					}
				});
			}
			return false;
		});
	
		$('#w_audio4_name').on('click', function() {
			$.ajax({
				type: 'POST',
				url: '<?php echo $board_skin_url."/../w_include_audio/mp3_selectList.php" ?>',
				data: { 
					selected: $(this).val(),
					id:"04"
				},
				success:function(response) {
					$('#selectList_04').html(response);

					$("#audioList_04").change(function() {
						var audio_URL = 'http://<?php echo $_SERVER['HTTP_HOST']?>/data/audio/'+$(this).val();
						$('#audioCtrl_04 source').attr('src', audio_URL);
						$("#audioCtrl_04")[0].load();
						// $("audio_04")[0].play();
						$('#w_audio4_name').val($(this).val());
					});
				}
			});
		});
	});
	</script>
	<form>
		<input style='display:none' id="audio_04" type="file" name="audio_04" class="audio_04">
		<input style='display:none' id="submit_04" type="submit" name="submit_04" class="submit_04" value="Submit">
	</form>			
	<input style='float:left;' type="button" value="Upload" id="upload_04" class="btn btn-warning">
	<input type="text" name="w_audio4_name" value="<?php echo $write['w_audio4_name'] ?>" id="w_audio4_name" class='form-control audioName' readonly placeholder='Name'>
	<div id='selectList_04'></div>
	<input type="text" name="w_audio4_time" value="<?php echo $write['w_audio4_time'] ?>" id="w_audio4_time" class='form-control audioTime' placeholder='Second'>
	<audio controls class='audioCtrl' id='audioCtrl_04'>
		<source src='<?php echo $audio_URL ?>' type='audio/mpeg'>
	</audio>
	<input type="text" name="w_audio4_volume" value="<?php echo $write['w_audio4_volume'] ?>" id="w_audio4_volume" class='form-control audioVol' placeholder='Volume'>
	<input style='float:left;' type="button" value="Reset" onclick="resetAudio_04()" class="btn btn-danger">
	</td>
</tr>