<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

include_once G5_PATH.'/head.php';

// 관련프로그램
// su ecos -c "cd /home/pi/ecos_its-OPTEX/its_monitor/ && python run_sysmon_server.py"

if($subject) $titleIs = $subject; else $titleIs = "Monitoring"; // 서브잭트명이 없으면 Log로..
$board['bo_subject'] = $titleIs;

if($is_guest) {
	ob_start(); // ensures anything dumped out will be caught
	$url = G5_URL; // this can be set based on whatever
	while (ob_get_status()) 
	{
		ob_end_clean();
	}
	header( "Location: $url" );
}

$node_ip = $_SERVER['HTTP_HOST']; // Server IP
// $node_port = G5_CU_MASTER_NODE_0; // G5_CU_MASTER_PORT(64444) 데이터를 Node.js 서버가 읽고 G5_CU_MASTER_NODE_0(64446) 포트로 클라이언트 선언
$node_port = '60200';
$node_key = md5(microtime(true)); // 사용자 제한을 위한 키를 만들고 키값을 /tmp 내애 파일을 만든 다
touch(G5_PATH."/data/$node_key"); // 키파일 생성 사용된 파일은 nodejs server가 사용후 삭제
$iframe_address = "http://" . $node_ip . ":" . $node_port . "/" . $node_key;
?>

<script>
$(document).ready(function() {
	localStorage.setItem("node_key", "<?php echo $node_key ?>");

    $('#sysmonPopUp').click(function(){
		$.ajax({
			type: "GET",
			url: 'monitor_its_ajax.php',
			success: function(data){
				var sysmon_url = "http://<?php echo $node_ip ?>:<?php echo $node_port ?>/" + data;
				window.open(sysmon_url,'sysMon', 'toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=1280px, height=1024px');
			}
		});	
    });


});

</script>

<style>
table { display: inline; font-size: 7pt; }
td { padding: 0 10px; text-align: initial; }
.title { font-size: 8pt; }
.shadow { text-shadow: 4px 6px 4px black; }
.sysmon_container { width: 100%; text-align: center; margin: 0; padding: 0; }
.sysmon_chart { max-width:33%; }

// @media screen and (max-width: 900px) and (min-width: 501px) {
	// .sysmon_chart { max-width:50%; }
// }

@media screen and (max-width: 900px) {
	.sysmon_chart { max-width:100%; }
}
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container" id="sysmonPopUp">
        <div class="intro-text" >
            <span class="name"><?php echo $board['bo_subject']?><span class="sound_only"> 목록</span></span>
			<hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>

<iframe id="sysmon" src="<?php echo $iframe_address ?>" frameborder="0" width="100%" height="640" marginwidth="0" marginheight="0" scrolling="yes" ></iframe>

<?php /* 

<script language="JavaScript">
	// Image Auto Reload
	function refreshIt(element) {
		setTimeout(function() {
			element.src = element.src.split('?')[0] + '?' + new Date().getTime();
			refreshIt(element);
		}, 60000); // refresh every 1000ms = 1sec
	}
</script>

<section class="success" style="padding:0;">
    <div class="sysmon_container">
	<span><img class="sysmon_chart" id="chart_day" src="http://162.221.199.49:60010/162.221.199.1_tengigabitethernet1_1-day.png" alt="daily" onload="refreshIt(this)" /></span>
	<span><img class="sysmon_chart" id="chart_week" src="http://162.221.199.49:60010/162.221.199.1_tengigabitethernet1_1-week.png" alt="weelky" onload="refreshIt(this)" /></span>
	<span><img class="sysmon_chart" id="chart_month" src="http://162.221.199.49:60010/162.221.199.1_tengigabitethernet1_1-month.png" alt="monthly" onload="refreshIt(this)" /></span>
    </div>
</section>
*/?>

<?php
include_once(G5_PATH.'/tail.php');
?>