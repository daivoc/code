<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// ex: include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php');
// include_once(G5_THEME_PATH.'/skin/board/w_include_license/system.php');

$server = G5_THEME_URL.'/skin/board/w_include_license/ajaxSystem.php'; // 
?>

<script type="text/javascript">
	$(function() {
		$('#request').on('click', function() {
			if(document.getElementById('authKey').value && document.getElementById('cu_name').value){
				$.ajax({
					type: 'POST',
					url: '<?php echo $server; ?>',
					data: {
						"host": document.getElementById('host').value,
						"customer": document.getElementById('cu_name').value,
						"authKey": document.getElementById('authKey').value,
						"cpuID": document.getElementById('cpuID').value
					},
					error : function(error) {
						alert("Error!");
					},
					success : function(data) {
						document.getElementById('mb_1').value = data;
						// alert("Success!");
					}
				});
			} else {
				alert("Require Customer Name and Auth. Key.");
			}
		});
	});
</script>

<input style='display:none' id="host" type="text" name="host" value=<?php echo G5_CU_LICENSE_SERVER?>>
<input style='display:block;width:60%;float:left;' id="authKey" type="password" name="authKey" value="" class="form-control" placeholder="Password">
<input style='display:none' id="cpuID" type="text" name="cpuID" value=<?php echo G5_CU_ITS_SERIAL ?>>
<input style='display:block;float:right;margin:4px;' id="request" type="button" name="request" value="Request">
