<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가

$audio_src = 'http://'.$_SERVER['HTTP_HOST'].'/data/audio/alarm.mp3';

?>
	<tr class='w_detail_tr'>
		<th scope="row" title="Audio Warning"><label for="w_warning">Audio Warning</label></th>
		<td>
			<script type="text/javascript">
				$(function() {
					$("#upload").click(function(){
						$("#audio").click();
					});
					$("#audio").change(function(){
						$("#submit").click();
					});
					$('.submit').on('click', function() {
						var file_data = $('.audio').prop('files')[0];
						var file_name = $('.audio').val().split('\\').pop();
						if(file_data != undefined) {
							$('#wr_2').val(file_name);
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
									} else if(response == 'false') {
										alert('Invalid file type or check permission config > path > audio]');
									} else {
										alert('Something went wrong. Please try again. or \ncheck permission config > path > audio');
									}
			 
									$('.audio').val('');
								}
							});
						}
						return false;
					});
				});
			</script>
			<form>
				<input style='display:none' id="audio" type="file" name="audio" class="audio" required>
				<input style='display:none' id="submit" type="submit" name="submit" class="submit" value="Submit">
			</form>			
			<input style='float:left;' type="button" value="Upload MP3" id="upload" class="btn btn-warning">
			<input style='float:left;margin-left:4px;width:200px;text-align:right;' type="text" name="wr_2" value="<?php echo $write['wr_2'] ?>" id="wr_2" class='form-control' readonly placeholder='Name'>
			<input style='float:left;margin-left:4px;width:74px;text-align:right;' type="text" name="wr_3" value="<?php echo $write['wr_3'] ?>" id="wr_3" class='form-control' placeholder='Second'>
			<audio controls style='float:left;height:36px;margin-left:4px;'>
				<source src='<?php echo $audio_src ?>' type='audio/mpeg'>
			</audio>
		</td>
	</tr>