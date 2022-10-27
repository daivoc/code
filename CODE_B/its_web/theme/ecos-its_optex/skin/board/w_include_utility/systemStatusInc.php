<?php
include_once('./_common.php');
?>
<script>
var GNU = ', GNU <?php echo G5_GNUBOARD_VER ?>'; // 그누버전
function systemStatus() {
	$.ajax({
		url : g5_url+"/theme/ecos-its_optex/skin/board/w_include_utility/systemStatus.php",
	}).done(function(data) {
		// console.log(data);
		// alert(data);
		// document.getElementById("systemStatus").innerHTML = data + GNU;
		document.getElementById("systemStatus").innerHTML = data;
	});
}

systemStatus();
// setInterval(systemStatus, 10000); // 5초마다
</script>
<style>
#systemStatus {font-size: 6pt; float: left; position: absolute; bottom: 16px; right: 14px; color: gray; text-align: right; }
</style>
<div id="systemStatus">System Status</div>
