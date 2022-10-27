<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php');
// include_once(G5_THEME_PATH.'/skin/board/w_include_license/application.php');

$server = G5_THEME_URL.'/skin/board/w_include_license/ajaxApplication.php'; // 

?>
<script type="text/javascript">
	$(function() {
		$('#request').on('click', function() {
			if(document.getElementById('authKey').value && document.getElementById('customer').value && document.getElementById('w_device_id').value){
				$.ajax({
					type: 'POST',
					url: '<?php echo $server; ?>',
					data: {
						"host": document.getElementById('host').value,
						"customer": document.getElementById('customer').value,
						"subject": document.getElementById('subject').value,
						"authKey": document.getElementById('authKey').value,
						"device": document.getElementById('w_device_id').value,
						"serial": document.getElementById('w_sensor_serial').value,
						"cpuID": document.getElementById('cpuID').value
					},
					error : function(error) {
						alert("Error!");
					},
					success : function(data) {
						document.getElementById('w_license').value = data;
						// alert("Success!");
					}
				});
			} else {
				alert("Require system license and Auth. key and device ID.");
			}
		});
	});
</script>

<input style='display:none' id="host" type="text" name="host" value=<?php echo G5_CU_LICENSE_SERVER?>>
<input style='display:none' id="customer" type="text" name="customer" value=<?php echo $member['mb_10']?>>
<input style='display:none' id="subject" type="text" name="subject" value=<?php echo $board['bo_subject']?>>
<input style='display:none' id="cpuID" type="text" name="cpuID" value=<?php echo G5_CU_ITS_SERIAL?>>
<input id="authKey" type="password" name="authKey" value="" class="form-control input25P" autocomplete="on" placeholder="Password">
<input id="request" type="button" name="request" value="Request" class="btn btn-info">
