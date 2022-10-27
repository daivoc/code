<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

if (G5_IS_MOBILE) {
	include_once G5_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_PATH.'/head.php';

global $g5, $bo_table;

$cur_cpu_serial = shell_exec("cat /proc/cpuinfo | grep Serial | cut -d' ' -f2");

// 프로세서 실행중인지 확인
function checkProc($matchIs) {
	$query = "ps aux | grep '".$matchIs."' | grep -v grep | awk '{ print $2 }' | head -1";
	exec($query, $out);
	return $out[0];
}
// 설치된 모든 센서 목록보기 
$status_sensors = '<table><tr style=background-color:gray;><td class=title>SENSOR</td><td class=title>MODEL</td><td class=title>SERIAL</td></tr>';
$write_table = $g5['write_prefix'] . G5_CU_CONF_BSS;
$sql = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial, w_sensor_disable FROM $write_table ";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {	
	if($row['w_sensor_disable']) 
		$serial = "<span style=color:crimson;>".$row['w_sensor_serial']."</span>";
	else 
		$serial = $row['w_sensor_serial'];
	
	$model = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_BSS.">".$row['w_sensor_model']."</a>";
	$serial = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_BSS."&wr_id=".$row['wr_id'].">".$serial."</a>";
	$status_sensors .= "<tr><td class=title style=background-color:silver;>".$row['wr_subject']."</td><td style=background-color:white;color:gray;>".$model."</td><td style=background-color:white;color:gray;>".$serial."</td></tr>";
}

// $write_table = $g5['write_prefix'] . G5_CU_CONF_BSS_R;
// $sql = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial, w_sensor_disable FROM $write_table ";
// $result = sql_query($sql);
// while ($row = sql_fetch_array($result)) {	
// 	if($row['w_sensor_disable']) 
// 		$serial = "<span style=color:crimson;>".$row['w_sensor_serial']."</span>";
// 	else 
// 		$serial = $row['w_sensor_serial'];
	
// 	$model = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_BSS_R.">".$row['w_sensor_model']."</a>";
// 	$serial = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_BSS_R."&wr_id=".$row['wr_id'].">".$serial."</a>";
// 	$status_sensors .= "<tr><td class=title style=background-color:silver;>".$row['wr_subject']."</td><td style=background-color:white;color:gray;>".$model."</td><td style=background-color:white;color:gray;>".$serial."</td></tr>";
// }

// $write_table = $g5['write_prefix'] . G5_CU_CONF_RLS;
// $sql = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial, w_sensor_disable FROM $write_table ";
// $result = sql_query($sql);
// while ($row = sql_fetch_array($result)) {
// 	if($row['w_sensor_disable']) 
// 		$serial = "<del style=color:crimson;>".$row['w_sensor_serial']."</del>";
// 	else 
// 		$serial = $row['w_sensor_serial'];
	
// 	$model = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_RLS.">".$row['w_sensor_model']."</a>";
// 	$serial = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_RLS."&wr_id=".$row['wr_id'].">".$serial."</a>";
// 	$status_sensors .= "<tr><td class=title style=background-color:silver;>".$row['wr_subject']."</td><td style=background-color:white;color:gray;>".$model."</td><td style=background-color:white;color:gray;>".$serial."</td></tr>";
// }

$write_table = $g5['write_prefix'] . G5_CU_CONF_GIKEN_T;
$sql = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial, w_sensor_disable FROM $write_table ";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	if($row['w_sensor_disable']) 
		$serial = "<del style=color:crimson;>".$row['w_sensor_serial']."</del>";
	else 
		$serial = $row['w_sensor_serial'];
	
	$model = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_GIKEN_T.">".$row['w_sensor_model']."</a>";
	$serial = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_GIKEN_T."&wr_id=".$row['wr_id'].">".$serial."</a>";
	$status_sensors .= "<tr><td class=title style=background-color:silver;>".$row['wr_subject']."</td><td style=background-color:white;color:gray;>".$model."</td><td style=background-color:white;color:gray;>".$serial."</td></tr>";
}

$write_table = $g5['write_prefix'] . G5_CU_CONF_RLS_R;
$sql = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial, w_sensor_disable FROM $write_table ";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	if($row['w_sensor_disable']) 
		$serial = "<del style=color:crimson;>".$row['w_sensor_serial']."</del>";
	else 
		$serial = $row['w_sensor_serial'];
	
	$model = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_RLS_R.">".$row['w_sensor_model']."</a>";
	$serial = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_RLS_R."&wr_id=".$row['wr_id'].">".$serial."</a>";
	$status_sensors .= "<tr><td class=title style=background-color:silver;>".$row['wr_subject']."</td><td style=background-color:white;color:gray;>".$model."</td><td style=background-color:white;color:gray;>".$serial."</td></tr>";
}

$write_table = $g5['write_prefix'] . G5_CU_CONF_GPIO;
$sql = "SELECT wr_id, wr_subject, w_sensor_model, w_sensor_serial, w_sensor_disable FROM $write_table ";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	if($row['w_sensor_disable']) 
		$serial = "<del style=color:crimson;>".$row['w_sensor_serial']."</del>";
	else 
		$serial = $row['w_sensor_serial'];
	
	$model = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_GPIO.">".$row['w_sensor_model']."</a>";
	$serial = "<a href=".G5_BBS_URL."/board.php?bo_table=".G5_CU_CONF_GPIO."&wr_id=".$row['wr_id'].">".$serial."</a>";
	$status_sensors .= "<tr><td class=title style=background-color:silver;>".$row['wr_subject']."</td><td style=background-color:white;color:gray;>".$model."</td><td style=background-color:white;color:gray;>".$serial."</td></tr>";
}

if(checkProc('node itsAPI.js')) { 
	$model = "<a href=".G5_URL.":28080>API Monitoring System</a>";
	$status_sensors .= "<tr><td class=title style=background-color:silver;>ITS API</td><td colspan=2 style=text-align:center;background-color:white;color:gray;>".$model."</td></tr>";
} 
$status_sensors .= '<tr><td class=title style=background-color:black;color:white;>SYSTEM</td><td colspan=2 style=text-align:center;background-color:silver;color:black;>'.$cur_cpu_serial.'</td></tr></table>';

// $result = sql_query($sql);
// while ($row = sql_fetch_array($result)) {
	// $status_sensors .= "<div>".$row['w_sensor_serial']."<br>".$row['w_system_ip'].":".$row['w_system_port']."</div>";
// }

// 설치된 모든 센서 목록보기 


if($subject) $titleIs = $subject; else $titleIs = "Status"; // 서브잭트명이 없으면 Log로..
$board['bo_subject'] = $titleIs;
?>

<style>
table{display:inline;font-size:7pt;}
td{padding:0 10px;text-align:initial;}
.title{font-size:8pt;}
.shadow{text-shadow: 4px 6px 4px black;}
.iframe_Info{width:100%;height:200px;}
.iframe_its{width:300px;height:64px;padding:4px;}
.iframe_acu{width:600px;height:100px;padding:4px;}
.iframe_RLS{width:80%;height:300px;padding:4px;}
.iframe_peopleCount{width:280px;height:42px;padding:4px;}
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name"><?php echo $board['bo_subject']?><span class="sound_only"> 목록</span></span>
            <hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>


<div class="container" style="padding: 10px; text-align: center; color: white;">
<div>
<?php echo $status_sensors?>
</div>
</div>


<?php
$iframeHtml = "";
$sql = "SELECT mb_4 FROM g5_member WHERE mb_id = 'its' LIMIT 1";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$ioBoard = $row["mb_4"]; // its or acu
}
if ($ioBoard == "acu") {
	$matchIs = "node GPACU.js";
	$framePort = "18080";
} else {
	$matchIs = "node GPWIO.js";
	$framePort = "8080";
	$ioBoard = "its";
}
if(checkProc($matchIs)) {
	// WEB GPIO 모니터링
	$frameAddr = "http://".$_SERVER["SERVER_NAME"].":".$framePort;
	$iframeHtml .= "<div><iframe class='iframe_".$ioBoard."' src='".$frameAddr."' frameborder='0' marginwidth='0' marginheight='0'></iframe></div>";
} else {
	$iframeHtml .= "<div>Current Set To ".$ioBoard."</div>";
}

$matchIs = "table_union.js ".G5_CU_MASTER_PORT." ".G5_CU_MASTER_NODE_0;
if(checkProc($matchIs)) {
	// G5_CU_MASTER_PORT(64444) 데이터를 Node.js 서버가 읽고 G5_CU_MASTER_NODE_0(64446) 포트로 클라이언트 선언
	$frameAddr = "http://" . $_SERVER['HTTP_HOST'] . ":" . G5_CU_MASTER_NODE_0 . "/";
	$iframeHtml .= "<div><iframe class='iframe_Info' src='".$frameAddr."' frameborder='0' marginheight='0' scrolling='yes' ></iframe></div>";
}

$matchIs = "node /home/pi/GIKENC/GIKENC.js";
$framePort = "37268";
if(checkProc($matchIs)) {
	$frameAddr = "http://".$_SERVER["SERVER_NAME"].":".$framePort;
	$iframeHtml .= "<div><iframe class='iframe_peopleCount' src='".$frameAddr."' frameborder='0' marginheight='0' scrolling='no' ></iframe></div>";
}

// RLS
// print "The PID is: " . $out[0];
$write_table = $g5['write_prefix'] . G5_CU_CONF_RLS;
$sql = "SELECT w_sensor_Addr FROM $write_table WHERE w_sensor_disable = 0";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$ipSplit = explode(".", $row['w_sensor_Addr']);
	$nodeIn = G5_CU_SYSTEM_PORT_IN + $ipSplit[2] + $ipSplit[3];
	$matchIs = "realtime_RLS.js ".$nodeIn;
	if(checkProc($matchIs)) {
		$nodeOut = G5_CU_SYSTEM_PORT_OUT + $ipSplit[2] + $ipSplit[3]; 
		$frameAddr = "http://".$_SERVER["SERVER_NAME"].":".$nodeOut;
		$iframeHtml .= "<div><iframe class='iframe_RLS' src='".$frameAddr."' frameborder='0' marginwidth='0' marginheight='0'></iframe></div>";
	}
}

$write_table = $g5['write_prefix'] . G5_CU_CONF_RLS_R;
$sql = "SELECT w_sensor_Addr FROM $write_table WHERE w_sensor_disable = 0";
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	$ipSplit = explode(".", $row['w_sensor_Addr']);
	$nodeIn = G5_CU_SYSTEM_PORT_IN + $ipSplit[2] + $ipSplit[3];
	$matchIs = "realtime_RLS.js ".$nodeIn;
	if(checkProc($matchIs)) {
		$nodeOut = G5_CU_SYSTEM_PORT_OUT + $ipSplit[2] + $ipSplit[3]; 
		$frameAddr = "http://".$_SERVER["SERVER_NAME"].":".$nodeOut;
		$iframeHtml .= "<div><iframe class='iframe_RLS' src='".$frameAddr."' frameborder='0' marginwidth='0' marginheight='0'></iframe></div>";
	}
}
?>

<div class="container" style="text-align: center;">
	<?php echo $iframeHtml?>
</div>
<?php
include_once(G5_THEME_PATH.'/skin/board/w_include_utility/systemStatusInc.php');
?>

<?php include_once(G5_PATH.'/tail.php'); ?>