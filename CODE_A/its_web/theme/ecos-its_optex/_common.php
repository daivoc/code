group.php                                                                                           0000664 0001751 0001751 00000002514 14047704766 010552  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

if (G5_IS_MOBILE) {
    include_once(G5_THEME_MOBILE_PATH.'/group.php');
    return;
}

if(!$is_admin && $group['gr_device'] == 'mobile')
    alert($group['gr_subject'].' 그룹은 모바일에서만 접근할 수 있습니다.');

$g5['title'] = $group['gr_subject'];
include_once(G5_THEME_PATH.'/head.php');
include_once(G5_LIB_PATH.'/latest.lib.php');
?>


<!-- 메인화면 최신글 시작 -->
<?php
//  최신글
$sql = " select bo_table, bo_subject
            from {$g5[board_table]}
            where gr_id = '{$gr_id}'
              and bo_list_level <= '{$member[mb_level]}'
              and bo_device <> 'mobile' ";
if(!$is_admin)
    $sql .= " and bo_use_cert = '' ";
$sql .= " order by bo_order ";
$result = sql_query($sql);
for ($i=0; $row=sql_fetch_array($result); $i++) {
    $lt_style = "";
    if ($i%2==1) $lt_style = "margin-left:20px";
    else $lt_style = "";
?>
    <div style="float:left;<?php echo $lt_style ?>">
    <?php
    // 이 함수가 바로 최신글을 추출하는 역할을 합니다.
    // 사용방법 : latest(스킨, 게시판아이디, 출력라인, 글자수);
    echo latest('theme/basic', $row['bo_table'], 5, 70);
    ?>
    </div>
<?php
}
?>
<!-- 메인화면 최신글 끝 -->

<?php
include_once(G5_THEME_PATH.'/tail.php');
?>
                                                                                                                                                                                    head.php                                                                                            0000664 0001751 0001751 00000021536 14222460365 010311  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// GUI Main 페이지 관련 보드선별및 출력
// 예 <li><a href="/bbs/board.php?bo_table=g300t100">GPIO</a></li>
//
$jsonFile = "/home/pi/common/config.json";
$fOpen = fopen($jsonFile, "r") or die("Call Administrator.");
$fRead = fread($fOpen,filesize($jsonFile));
fclose($fOpen);
$tables = json_decode($fRead, TRUE)["table"];
$runProg = json_decode($fRead, TRUE)["run"];

$mainMenu = "";
foreach ($runProg as $key => $val) {
	if (array_key_exists($key, $tables)) {
		$tmp_bo_table = end(explode('_',$tables[$key])); // g300t100
		$mainMenu .= "<li><a href='/bbs/board.php?bo_table=".$tmp_bo_table."'>".strtoupper($key)."</a></li>";
	}
}


if (G5_IS_MOBILE) {
    include_once G5_THEME_MOBILE_PATH.'/head.php';
    return;
}
include_once G5_LIB_PATH.'/thumbnail.lib.php';
include_once G5_THEME_PATH.'/head.sub.php';
?>

<?php if ($is_member) { ?>
<script>
function startTime() {
    var today = new Date();
    var yy = today.getFullYear();
    var mm = today.getMonth()+1;
    var dd = today.getDate();
	
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
	$('#now_dateTime').val(yy + "-" + mm + "-" + dd + " " +h + ":" + m + ":" + s);
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}

$( document ).ready(function() {
	startTime();
	////////// scanned_ITS //////////
	// /its_web/utility/systemExec/scanned_ITS.php 는 관리자에게 필요한 유틸리티을 제공한다.
	// $.ajax({
	// 	url : "<?php echo G5_THEME_URL ?>/utility/systemExec/menu_ITS.php?isITS_M=<?php echo $isITS_M ?>",
	// }).done(function(data) {
	// 	// console.log('<?php echo $isITS_M ?>');
	// 	$('#menu_ITS').html(data);
	// });

	$.ajax({
		type: 'POST',
		url: '<?php echo G5_THEME_URL?>/utility/systemExec/menu_ITS.php', // point to server-side PHP script 
		data: {'isITS_M': <?php echo $isITS_M ?> },
		success: function (data) {
			$('#menu_ITS').html(data);
		},
		error: function (data) {
			alert("error");
		}
	});
	

});	

function its_log() {
	// 중요: 경로 <?php echo G5_THEME_URL ?>/utility/filemanager 는 웹사용자의 쓰기 권한이 있어야 한다.
	window.open("<?php echo G5_THEME_URL ?>/utility/filemanager/fm.php?ID=its&PATH=data||log", "Log View", "width=640,height=400,scrollbars=no");
}

function its_reboot() {
	// var r = confirm("Reboot can take up to 30 seconds.");
	var r = confirm("<?php echo $SK_BO_Conform_Reboot[ITS_Lang]?>");
	if (r == true) {
		$.ajax({
			url :  "<?php echo G5_THEME_URL ?>/utility/systemExec/reboot.php",
		}).done(function(data) {
			// console.log(data);
			// alert(data);
		});
	}
}
function its_shutdown() {
	// var r = confirm("Reboot can take up to 30 seconds.");
	var r = confirm("<?php echo $SK_BO_Conform_Shutdown[ITS_Lang]?>");
	if (r == true) {
		$.ajax({
			url :  "<?php echo G5_THEME_URL ?>/utility/systemExec/poweroff.php",
		}).done(function(data) {
			// console.log(data);
			// alert(data);
		});
	}
}
</script>
<?php } ?>

<!-- Navigation -->
<style>
.ecos_logo_main {
	/* position: absolute; */
	/* top: 50%; */
	/* left: 50%; */
	width: 30px;
	height: 30px;
	margin: 8px 6px 0 0;
	-webkit-animation:spin 4s linear infinite;
	-moz-animation:spin 4s linear infinite;
	animation: spin 2s linear infinite;
	float: left;
}
@-moz-keyframes spin { 100% { -moz-transform: rotate(360deg); } }
@-webkit-keyframes spin { 100% { -webkit-transform: rotate(360deg); } }
@keyframes spin { 100% { -webkit-transform: rotate(360deg); transform:rotate(360deg); } }

hr { padding: 0; border: none; border-top: solid 1px; text-align: center; max-width: 250px; margin-top: 10px; margin-bottom: 10px; }

#header { text-align: center; }
#header .intro-text .name { font-size: 2em; margin-top: 10px; }
#header .intro-text .skills { font-size: 1em; margin-bottom: 10px; }
#header .container { padding-bottom: 10px; color: white; background: #41576d; border-radius: 8px; margin-top: 2px; }
.intro-text { margin-top: 10px; }
.titleDeco { font-size: 18pt; }
.navbar-nav>li { float: left; }

@media (max-width: 768px) {
	.sub-menu { display:none!important; }
}
</style>

<nav class="container navbar-inverse">
	<div class="container-fluid">
		<div class="navbar-header">
			<a href="/"><img class="ecos_logo_main" src="<?php echo G5_THEME_IMG_URL?>/profile.png" alt=""></a>
			<a class="titleDeco navbar-brand" href="/">ECOS<?php // echo $config['cf_title']?></a>
		</div>
		
		<ul class="nav navbar-nav navbar-right">
		<?php if($is_guest) { ?>
			<li>
				<a href="<?php echo G5_BBS_URL?>/login.php"><span class="glyphicon glyphicon-user"></span> <?php echo $SK_HD_Login[ITS_Lang]?></a>
			</li>
		<?php } else { ?>
			<li>
				<a href="<?php echo G5_BBS_URL?>/logout.php"><span class="glyphicon glyphicon-user"></span> <?php echo $SK_HD_Logout[ITS_Lang]?></a>
			</li>
		<?php } ?>
		</ul>

		<?php if(!$is_guest) { ?>
		<ul class="sub-menu nav navbar-nav navbar-right">
			<?php if($member['mb_id'] == 'its') { ?>
				<?php if($isITS_M) { // IMS 사용자 // 변수값은 head.sub.php 에서 결정한다. ?>
				<li>
					<a href="http://<?php echo $_SERVER['HTTP_HOST'].':'.G5_CU_IMS_PORT?>"><span class="glyphicon glyphicon-map-marker"></span> <?php echo $SK_BO_Monitoring[ITS_Lang]?></a>
				</li>						
				<li class="dropdown">
					<a class="dropdown-toggle" data-toggle="dropdown" href="#"><span class="glyphicon glyphicon-check"></span> <?php echo $SK_BO_Setup[ITS_Lang]?>
					<span class="caret"></span></a>
					<ul class="dropdown-menu" style="right: unset;">
						<li><a href="/bbs/board.php?bo_table=g500t200">Zone</a></li>
						<li><a href="/bbs/board.php?bo_table=g500t100">Camera</a></li>
						<li><a href="/bbs/board.php?bo_table=g500t300">Box</a></li>
					</ul>
				</li>
				<?php } ?>
			<?php } else { ?>
				<?php if(!$isITS_M) { // ITS 사용자 ?>
				<li class="dropdown">
					<a class="dropdown-toggle" data-toggle="dropdown" href="#"><span class="glyphicon glyphicon-wrench"></span> <?php echo $SK_HD_Menu[ITS_Lang]?>
					<span class="caret"></span></a>
					<ul class="dropdown-menu" style="right: unset;">
						<li><a href="/theme/ecos-its_optex/utility/status/status_union.php">Event Status</a></li>
						<li><a href="/theme/ecos-its_optex/utility/status/list_union.php">Action Log</a></li>
						<!-- li><a href="/theme/ecos-its_optex/utility/status/config_union.php">Sensor Config</a></li -->
					</ul>
				</li>
				<li class="dropdown">
					<a class="dropdown-toggle" data-toggle="dropdown" href="#"><span class="glyphicon glyphicon-check"></span> <?php echo $SK_BO_Sensor[ITS_Lang]?>
					<span class="caret"></span></a>
					<ul class="dropdown-menu" style="right: unset;">
						<?php echo $mainMenu; ?>
					</ul>
				</li>
				<?php } ?>
			<?php } ?>
			<li>
				<a onclick="document.getElementById('form_now_dateTime').submit();"><span class="glyphicon glyphicon-time"></span> <?php echo $SK_HD_Sync_Clock[ITS_Lang]?></a>
				<form id="form_now_dateTime" method="post" action="<?php echo G5_URL?>/theme/ecos-its_optex/utility/systemExec/setdate.php">
				<input type="hidden" id="now_dateTime" name="now_dateTime" value="">
				</form>
			</li>
			<li>
				<a href="<?php echo G5_BBS_URL ?>/member_confirm.php?url=<?php echo G5_BBS_URL ?>/register_form.php"><span class="glyphicon glyphicon-cog"></span> <?php echo $SK_HD_Info[ITS_Lang]?></a>
			</li>
			<?php if($member['mb_id'] == 'its') { ?>
			<!-- <li class="dropdown">
				<a class="dropdown-toggle" data-toggle="dropdown" href="#"><span class="glyphicon glyphicon-tasks"></span> <?php echo $SK_BO_Log[ITS_Lang]?>
				<span class="caret"></span></a>
				<ul class="dropdown-menu" style="right: unset;">
					<li><a href="/theme/ecos-its_optex/utility/status/list_IMS.php">IMS Status</a></li>
					<li><a href="/theme/ecos-its_optex/utility/status/list_tailing.php">Tailing</a></li>
				</ul>
			</li> -->

			<?php } else { ?>
				<?php if(!$isITS_M) { // ITS 사용자 ?>
				<li>
					<a href="#" onclick="its_log()"><span class="glyphicon glyphicon-tasks"> <?php echo $SK_BO_Log[ITS_Lang]?></a>
				</li>
				<?php } ?>
			<?php } ?>
			<li>
				<a href="#" onclick="its_reboot()"><span class="glyphicon glyphicon-refresh"></span> <?php echo $SK_HD_Reboot[ITS_Lang]?></a>
			</li>
			<?php /*
			<li>
				<a href="#" onclick="its_shutdown()"><span class="glyphicon glyphicon-off"></span> <?php echo $SK_HD_Shutdown[ITS_Lang]?></a>
			</li>
			*/ ?>
			<?php if($member['mb_id'] == 'admin') { ?>
			<li>
				<a href="<?php echo G5_THEME_URL?>/utility/manual/list.php"><?php echo $SK_BO_Help[ITS_Lang]?></a>
			</li>
			<?php } ?>
		</ul>
		<?php } ?>
	</div>
</nav>

<div id="container">                                                                                                                                                                  head.sub.php                                                                                        0000664 0001751 0001751 00000011041 14222411325 011057  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
// 이 파일은 새로운 파일 생성시 반드시 포함되어야 함
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// 언어 정의 파일 열기
include_once G5_THEME_PATH.'/its_web_lan.php';

$begin_time = get_microtime();
?>
<?php // ECOS Code 모니터링과 카메라 관련 데몬이 존재하는지 확인한다.
if($config['cf_10'] == 'ims') {
	$isITS_M = 1;
	$g5['title'] = 'IMS System';
} else {
	$isITS_M = 0;
}
// print_r($member);
// // if($member['mb_id'] == 'its') {
// 	// 모니터링 프로그램 실행중 인지 확인 함
// 	exec("ps aux | grep 'node .*its_M_map.js' | grep -v grep | awk '{ print $2 }' | head -1", $outM);
// 	// print "The PID is: " . $outM[0];
// 	if ($outM[0]) {
// 		$isITS_M = $outM[0];
// 		$g5['title'] = 'IMS System';
// 	} else {
// 		$isITS_M = 0;
// 	}

// 	// // 카메라 프로그램 실행중 인지 확인 함
// 	// exec("ps aux | grep 'node .*CAM.js' | grep -v grep | awk '{ print $2 }' | head -1", $outC);
// 	// // print "The PID is: " . $outC[0];
// 	// if ($outC[0]) {
// 		// $isITS_C = $outC[0]; 
// 	// } else {
// 		// $isITS_C = 0;
// 	// }
// // }
?>
<?php
if (!isset($g5['title'])) {
    $g5['title'] = $config['cf_title'];
    $g5_head_title = $g5['title'];
}
else {
    $g5_head_title = $g5['title']; // 상태바에 표시될 제목
    // $g5_head_title .= " | ".$config['cf_title'];
}

// 현재 접속자
// 게시판 제목에 ' 포함되면 오류 발생
$g5['lo_location'] = addslashes($g5['title']);
if (!$g5['lo_location'])
    $g5['lo_location'] = addslashes(clean_xss_tags($_SERVER['REQUEST_URI']));
$g5['lo_url'] = addslashes(clean_xss_tags($_SERVER['REQUEST_URI']));
if (strstr($g5['lo_url'], '/'.G5_ADMIN_DIR.'/') || $is_admin == 'super') $g5['lo_url'] = '';

/*
// 만료된 페이지로 사용하시는 경우
header("Cache-Control: no-cache"); // HTTP/1.1
header("Expires: 0"); // rfc2616 - Section 14.21
header("Pragma: no-cache"); // HTTP/1.0
*/
?>
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes">
<meta name="HandheldFriendly" content="true">
<meta name="format-detection" content="telephone=no">
<meta http-equiv="imagetoolbar" content="no">
<meta http-equiv="X-UA-Compatible" content="IE=10,chrome=1">
<?php
if($config['cf_add_meta'])
    echo $config['cf_add_meta'].PHP_EOL;
?>
<title><?php echo $g5_head_title; ?></title>
<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL; ?>/<?php echo G5_IS_MOBILE ? 'mobile' : 'default'; ?>.css">
<link rel="stylesheet" href="<?php echo G5_THEME_CSS_URL; ?>/bootstrap.min.css">

<link rel="icon" type="image/png" href="<?php echo G5_THEME_IMG_URL; ?>/favicon.ico" />

<script src="<?php echo G5_THEME_JS_URL; ?>/jquery.min.js"></script>
<script src="<?php echo G5_THEME_JS_URL; ?>/jquery.easing.min.js"></script>
<script src="<?php echo G5_THEME_JS_URL; ?>/bootstrap.min.js"></script>
<!-- <script src="<?php echo G5_THEME_JS_URL; ?>/wow.min.js"></script> -->
<script src="<?php echo G5_JS_URL ?>/common.js"></script>
<script src="<?php echo G5_JS_URL ?>/wrest.js"></script>

<script>
// 자바스크립트에서 사용하는 전역변수 선언
var g5_url       = "<?php echo G5_URL ?>";
var g5_bbs_url   = "<?php echo G5_BBS_URL ?>";
var g5_is_member = "<?php echo isset($is_member)?$is_member:''; ?>";
var g5_is_admin  = "<?php echo isset($is_admin)?$is_admin:''; ?>";
var g5_is_mobile = "<?php echo G5_IS_MOBILE ?>";
var g5_bo_table  = "<?php echo isset($bo_table)?$bo_table:''; ?>";
var g5_sca       = "<?php echo isset($sca)?$sca:''; ?>";
var g5_editor    = "<?php echo ($config['cf_editor'] && $board['bo_use_dhtml_editor'])?$config['cf_editor']:''; ?>";
var g5_cookie_domain = "<?php echo G5_COOKIE_DOMAIN ?>";
</script>
<?php
if(!defined('G5_IS_ADMIN'))
    echo $config['cf_add_script'];
?>
</head>
<body <?php echo isset($g5['body_script']) ? $g5['body_script'] : ''; ?> id="page-top" class="index">
<?php
if ($is_member) { // 회원이라면 로그인 중이라는 메세지를 출력해준다.
    $sr_admin_msg = '';
    if ($is_admin == 'super') $sr_admin_msg = "최고관리자 ";
    else if ($is_admin == 'group') $sr_admin_msg = "그룹관리자 ";
    else if ($is_admin == 'board') $sr_admin_msg = "게시판관리자 ";

    echo '<div id="hd_login_msg">'.$sr_admin_msg.get_text($member['mb_nick']).'님 로그인 중 ';
    echo '<a href="'.G5_BBS_URL.'/logout.php">로그아웃</a></div>';
}
?>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               index.php                                                                                           0000664 0001751 0001751 00000010751 14222460653 010514  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
define('_INDEX_', true);
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

if (G5_IS_MOBILE) {
	include_once G5_THEME_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_THEME_PATH.'/head.php';

?>
<?php if($is_guest) { ?>
<style>
html, body { text-align: center; margin:0; padding:0; background: #000000; color: #666666; line-height: 1.25em; }
#outer { position: absolute; top: 50%; left: 50%; width: 1px; height: 1px; overflow: visible;}
#canvasContainer { position: absolute; width: 1000px; height: 560px; top: -290px; left: -500px; }
canvas { border: 1px solid #333333; }
a { color: #00CBCB; text-decoration: none; font-weight: bold; }
a:hover { color: #FFFFFF; }
#output { font-family: Arial, Helvetica, sans-serif; font-size: 0.75em; margin-top: 4px; }
.container { z-index: 1; position: relative; }
</style>
<script type="text/javascript">
(function(){function C(){e.globalCompositeOperation="source-over";e.fillStyle="rgba(8,8,12,0.65)";e.fillRect(0,0,f,p);e.globalCompositeOperation="lighter";x=q-u;y=r-v;u=q;v=r;for(var d=0.86*f,l=0.125*f,m=0.5*f,t=Math.random,n=Math.abs,o=z;o--;){var h=A[o],i=h.x,j=h.y,a=h.a,b=h.b,c=i-q,k=j-r,g=Math.sqrt(c*c+k*k)||0.001,c=c/g,k=k/g;if(w&&g<m)var s=14*(1-g/m),a=a+(c*s+0.5-t()),b=b+(k*s+0.5-t());g<d&&(s=0.0014*(1-g/d)*f,a-=c*s,b-=k*s);g<l&&(c=2.6E-4*(1-g/l)*f,a+=x*c,b+=y*c);a*=B;b*=B;c=n(a);k=n(b);g=0.5*(c+k);0.1>c&&(a*=3*t());0.1>k&&(b*=3*t());c=0.45*g;c=Math.max(Math.min(c,3.5),0.4);i+=a;j+=b;i>f?(i=f,a*=-1):0>i&&(i=0,a*=-1);j>p?(j=p,b*=-1):0>j&&(j=0,b*=-1);h.a=a;h.b=b;h.x=i;h.y=j;e.fillStyle=h.color;e.beginPath();e.arc(i,j,c,0,D,!0);e.closePath();e.fill()}}function E(d){d=d?d:window.event;q=d.clientX-m.offsetLeft-n.offsetLeft;r=d.clientY-m.offsetTop-n.offsetTop}function F(){w=!0;return!1}function G(){return w=!1}function H(){this.color="rgb("+Math.floor(255*Math.random())+","+Math.floor(255*Math.random())+","+Math.floor(255*Math.random())+")";this.b=this.a=this.x=this.y=0;this.size=1}var D=2*Math.PI,f=1E3,p=560,z=600,B=0.96,A=[],o,e,n,m,q,r,x,y,u,v,w;window.onload=function(){o=document.getElementById("mainCanvas");if(o.getContext){m=document.getElementById("outer");n=document.getElementById("canvasContainer");e=o.getContext("2d");for(var d=z;d--;){var l=new H;l.x=0.5*f;l.y=0.5*p;l.a=34*Math.cos(d)*Math.random();l.b=34*Math.sin(d)*Math.random();A[d]=l}q=u=0.5*f;r=v=0.5*p;document.onmousedown=F;document.onmouseup=G;document.onmousemove=E;setInterval(C,33);}else document.getElementById("output").innerHTML="Sorry, needs a recent version of Chrome, Firefox, Opera, Safari, or Internet Explorer 9."}})();
</script>
<div id="outer">
	<div id="canvasContainer">
		<canvas id="mainCanvas" width="1000" height="560">
		</canvas>
	</div>
</div>

<?php } else if($member['mb_id'] == 'its') { ?>
<style> #header { filter: drop-shadow(2px 4px 6px black); }</style>
<!-- Header -->
<header id="header">
	<div class="container">
		<div class="row">
			<div class="col-lg-12">
				<div class="intro-text">
					<?php if($isITS_M) { ?>
						<style> #header .container { background: #896d2e; }</style>
						<span class="name">Intelligent Monitoring Server(IMS)</span>
					<?php } else { ?>
						<span class="name">Intelligent Terminal Server(ITS)</span>
					<?php } ?>
					<hr>
					<span>Technology by ECOS</span>
				</div>
			</div>
		</div>
</div>
</header>

<div id="menu_ITS" class="container"></div>
<?php } else if($member['mb_id'] == 'manager' && $isITS_M) {
	// 모니터링 데몬이 있는상태에서 매니저로 로그인 하면 바로 모니터링으로 화면 전환
	exec("ps aux | grep 'node .*its_M_map.js' | grep -v grep | awk '{ print $2 }' | head -1", $outM);
	// print "The PID is: " . $outM[0];
	if ($outM[0]) {
		$urlMonotoring = "http://".$_SERVER['HTTP_HOST'].":".G5_CU_IMS_PORT;
		header("Location: ".$urlMonotoring);
	} else {
		echo '<div style="position:absolute;top:30vh;left:40vw;text-align:center;"><img style="width:20vw;height:20vw;animation: spin 10s linear infinite;filter: invert(1);" src="'.G5_THEME_IMG_URL.'/profile.png" alt=""><div style="color:gray; text-align:center;">모니터링 서버간 일시적 접속 오류가 발생했습니다.<br>복구를 위해 상단 <span class="glyphicon glyphicon-refresh"></span>[재부팅]을 실행 하십시오.</div></div>';
	}

} else { 
	$urlMonotoring = "http://".$_SERVER['HTTP_HOST']."/theme/ecos-its_optex/utility/status/status_union.php";
	header("Location: ".$urlMonotoring);
} ?>

<?php
include_once(G5_THEME_PATH.'/tail.php');
?>                       its_web_lan.php                                                                                     0000664 0001751 0001751 00000060147 14047704766 011712  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
if (!defined('_GNUBOARD_')) exit;

// its_web 'OPTEX', its_webC 'Chinese', its_webE 'English', its_webJ 'Japaness', its_webK 'Korean'
$ITS_Lang = array( 'its_web' => 0,'its_webC' => 1,'its_webE' => 2,'its_webJ' => 3,'its_webK' => 4 );
// 사용자 manager의 예약필드 mb_7의 내용을 통해 언어를 선언 한다.
$sql = " select mb_7 from {$g5['member_table']} where mb_id = 'manager' ";
$row = sql_fetch($sql);
if ($row['mb_7']) {
	define('ITS_Lang', $ITS_Lang[$row['mb_7']]);
} else {
	define('ITS_Lang', 0);
}

$SK_BO_Accept_Boundary	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Accept Boundary',	3 =>'Japaness',	4 =>'허용범주');
$SK_BO_Accept_Range		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Accept Range',		3 =>'Japaness',	4 =>'허용범위');
$SK_BO_About			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'About',			3 =>'Japaness',	4 =>'대략');
$SK_BO_Advanced			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Advanced',			3 =>'Japaness',	4 =>'고급설정');
$SK_BO_Alarm_Cycle		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Alarm Cycle',		3 =>'Japaness',	4 =>'경보주기');
$SK_BO_Alert			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Alert',			3 =>'Japaness',	4 =>'경보');
$SK_BO_All				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'All',				3 =>'Japaness',	4 =>'전체');
$SK_BO_Allowable		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Allowable',		3 =>'Japaness',	4 =>'허용조건');
$SK_BO_Allowable_Dia	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Allowable Dia.',	3 =>'Japaness',	4 =>'허용직경');
$SK_BO_Angle			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Angle',			3 =>'Japaness',	4 =>'각도');
$SK_BO_Apply			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Apply',			3 =>'Japaness',	4 =>'즉시적용');
$SK_BO_Area_Block		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Area Block',		3 =>'Japaness',	4 =>'지역차단');
$SK_BO_Box				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Box',				3 =>'Japaness',	4 =>'함체');
$SK_BO_Basic			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Basic',			3 =>'Japaness',	4 =>'기본설정');
$SK_BO_Blocked			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Blocked',			3 =>'Japaness',	4 =>'상시차단');
$SK_BO_Camera			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Camera',			3 =>'Japaness',	4 =>'카메라');
$SK_BO_Cameraview		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Camera View',		3 =>'Japaness',	4 =>'카메라뷰');
$SK_BO_Capacity			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Capacity',			3 =>'Japaness',	4 =>'수용량');
$SK_BO_Cancel			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Cancel',			3 =>'Japaness',	4 =>'취소');
$SK_BO_Category			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Category',			3 =>'Japaness',	4 =>'분류');
$SK_BO_Choose			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Choose',			3 =>'Japaness',	4 =>'선택하세요');
$SK_BO_Chart			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Chart',			3 =>'Japaness',	4 =>'차트');
$SK_BO_Cmeter			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Cm',				3 =>'Japaness',	4 =>'센티미터');
$SK_BO_Created			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Created',			3 =>'Japaness',	4 =>'생성됨');
$SK_BO_Current			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Current',			3 =>'Japaness',	4 =>'현재');
$SK_BO_Day				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Day',				3 =>'Japaness',	4 =>'일');
$SK_BO_Daily			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Daily',			3 =>'Japaness',	4 =>'일간');
$SK_BO_Delete			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Delete',			3 =>'Japaness',	4 =>'삭제');
$SK_BO_Delay			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Delay',			3 =>'Japaness',	4 =>'지연');
$SK_BO_Detect_Range		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Detect. Range',	3 =>'Japaness',	4 =>'감지범위');
$SK_BO_Device_Name		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Device Name',		3 =>'Japaness',	4 =>'디바이스');
$SK_BO_Direction		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Direction',		3 =>'Japaness',	4 =>'방향');
$SK_BO_Disable			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Disable',			3 =>'Japaness',	4 =>'사용중지');
$SK_BO_Email			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Email',			3 =>'Japaness',	4 =>'이메일');
$SK_BO_Empty_Board		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Empty Board',		3 =>'Japaness',	4 =>'게시물이 없습니다');
$SK_BO_Encryption		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Encryption',		3 =>'Japaness',	4 =>'암호화');
$SK_BO_End				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'End',				3 =>'Japaness',	4 =>'종료');
$SK_BO_End_Coord		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'End Coord',		3 =>'Japaness',	4 =>'종료좌표');
$SK_BO_Event			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event',			3 =>'Japaness',	4 =>'이벤트');
$SK_BO_Event_Count		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event Count',		3 =>'Japaness',	4 =>'허용횟수');
$SK_BO_Event_Cycle		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event Cycle',		3 =>'Japaness',	4 =>'이벤트주기');
$SK_BO_Event_Hold		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event Hold',		3 =>'Japaness',	4 =>'대기시간');
$SK_BO_Events			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Events',			3 =>'Japaness',	4 =>'이벤트');
$SK_BO_Events_Level		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Events Level',		3 =>'Japaness',	4 =>'이벤트레벨');
$SK_BO_Help				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Help',				3 =>'Japaness',	4 =>'도움말');
$SK_BO_History			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'History',			3 =>'Japaness',	4 =>'수정내역');
$SK_BO_Hold				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Hold',				3 =>'Japaness',	4 =>'대기');
$SK_BO_Hold_Distance	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Hold Distance',	3 =>'Japaness',	4 =>'거리고정');
$SK_BO_Home_Page		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Home Page',		3 =>'Japaness',	4 =>'홈페이지');
$SK_BO_Host_Main		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Host(Main)',		3 =>'Japaness',	4 =>'호스트(주)');
$SK_BO_Host_Mirror		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Host(Mirror)',		3 =>'Japaness',	4 =>'호스트(부)');
$SK_HD_Info				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Information',		3 =>'Japaness',	4 =>'정보수정');
$SK_BO_Ignore_Area		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Ignore Area',		3 =>'Japaness',	4 =>'무시영역');
$SK_BO_ID				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'ID',				3 =>'Japaness',	4 =>'아이디');
$SK_BO_IP				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'IP',				3 =>'Japaness',	4 =>'아이피');
$SK_BO_Keep_Cycle		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Keep Cycle',		3 =>'Japaness',	4 =>'주기고정');
$SK_BO_Keep_Location	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Hold Location',	3 =>'Japaness',	4 =>'위치고정');
$SK_BO_Key				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Key',				3 =>'Japaness',	4 =>'키');
$SK_BO_Level			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Level',			3 =>'Japaness',	4 =>'레벨');
$SK_BO_License			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'License',			3 =>'Japaness',	4 =>'라이센스');
$SK_BO_List				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'List',				3 =>'Japaness',	4 =>'목록');
$SK_BO_Location			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Location',			3 =>'Japaness',	4 =>'설치장소');
$SK_BO_Log				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Log',				3 =>'Japaness',	4 =>'로그');
$SK_HD_Login			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Login',			3 =>'Japaness',	4 =>'로그인');
$SK_HD_Logout			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Logout',			3 =>'Japaness',	4 =>'로그아웃');
$SK_BO_Map				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Map',				3 =>'Japaness',	4 =>'지도');
$SK_BO_Master			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Master',			3 =>'Japaness',	4 =>'마스터');
$SK_HD_Menu				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Menu',				3 =>'Japaness',	4 =>'메뉴');
$SK_BO_Meter			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Meter',			3 =>'Japaness',	4 =>'미터');
$SK_BO_Model_Name		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Model Name',		3 =>'Japaness',	4 =>'모델명');
$SK_BO_Modified			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Modified',			3 =>'Japaness',	4 =>'수정됨');
$SK_BO_Modify			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Modify',			3 =>'Japaness',	4 =>'수정');
$SK_BO_Monitor			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monitor',			3 =>'Japaness',	4 =>'모니터');
$SK_BO_Monitoring		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monitoring',		3 =>'Japaness',	4 =>'모니터링');
$SK_BO_Multiful_Check	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Multiful Check',	3 =>'Japaness',	4 =>'복수금지');
$SK_BO_Name				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Name',				3 =>'Japaness',	4 =>'이름');
$SK_BO_New				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'New',				3 =>'Japaness',	4 =>'신규');
$SK_BO_Next				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Next',				3 =>'Japaness',	4 =>'다음');
$SK_BO_Offset			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Offset',			3 =>'Japaness',	4 =>'오프셋');
$SK_HD_Oneway			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Oneway',			3 =>'Japaness',	4 =>'일방통행');
$SK_BO_Option			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Option',			3 =>'Japaness',	4 =>'옵션');
$SK_BO_Password			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'password',			3 =>'Japaness',	4 =>'비밀번호');
$SK_BO_Pause			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Pause',			3 =>'Japaness',	4 =>'일시정지');
$SK_BO_Port				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Port',				3 =>'Japaness',	4 =>'포트');
$SK_BO_Position			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Position',			3 =>'Japaness',	4 =>'위치');
$SK_BO_Previous			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Previous',			3 =>'Japaness',	4 =>'이전');
$SK_BO_Range			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Range',			3 =>'Japaness',	4 =>'영역');
$SK_HD_Reboot			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Reboot',			3 =>'Japaness',	4 =>'재부팅');
$SK_BO_Reservation		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Reservation',		3 =>'Japaness',	4 =>'예약차단');
$SK_BO_Reserve			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Reserve',			3 =>'Japaness',	4 =>'예약');
$SK_BO_Restart			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Restart',			3 =>'Japaness',	4 =>'재실행');
$SK_BO_Save2			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Save',				3 =>'Japaness',	4 =>'작성완료');
$SK_BO_Save				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Save',				3 =>'Japaness',	4 =>'저장');
$SK_BO_Schedule			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Schedule',			3 =>'Japaness',	4 =>'스케줄');
$SK_BO_Search			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Search',			3 =>'Japaness',	4 =>'검색');
$SK_BO_Second			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sec.',				3 =>'Japaness',	4 =>'초');
$SK_BO_Sensitivity		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensitivity',		3 =>'Japaness',	4 =>'허용감도');
$SK_BO_Sensing_Boundary	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensing Boundary',	3 =>'Japaness',	4 =>'감지지역');
$SK_BO_Sensor			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor',			3 =>'Japaness',	4 =>'센서');
$SK_BO_Sensor_Azimuth	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Azimuth',	3 =>'Japaness',	4 =>'센서방위');
$SK_BO_Sensor_Face		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Face',		3 =>'Japaness',	4 =>'센서방향');
$SK_BO_Sensor_Name		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Name',		3 =>'Japaness',	4 =>'센서관리명');
$SK_BO_Sensor_IP		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor IP',		3 =>'Japaness',	4 =>'센서아이피');
$SK_BO_Sensor_Type		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Type',		3 =>'Japaness',	4 =>'센서형태');
$SK_BO_Setup			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Setup',			3 =>'Japaness',	4 =>'설정');
$SK_BO_Serial_Number	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Serial Number',	3 =>'Japaness',	4 =>'고유번호');
$SK_HD_Shutdown			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Shutdown',			3 =>'Japaness',	4 =>'종료');
$SK_BO_Shot_Per_Event	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Shot / Event',		3 =>'Japaness',	4 =>'사진수');
$SK_BO_Snapshot			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Snapshot',			3 =>'Japaness',	4 =>'스넵샷');
$SK_BO_Speed_Limit		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Speed Limit',		3 =>'Japaness',	4 =>'허용속도');
$SK_BO_Start			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Start',			3 =>'Japaness',	4 =>'시작');
$SK_BO_Start_Coord		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Start Coord',		3 =>'Japaness',	4 =>'시작좌표');
$SK_BO_Stop_Alarm		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Stop Alarm',		3 =>'Japaness',	4 =>'알람정지');
$SK_BO_Streaming		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Streaming',		3 =>'Japaness',	4 =>'스트리밍');
$SK_HD_Sync_Clock		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sync Clock',		3 =>'Japaness',	4 =>'시간동기');
$SK_BO_Submit			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Submit',			3 =>'Japaness',	4 =>'전송');
$SK_BO_Times			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Times',			3 =>'Japaness',	4 =>'회');
$SK_BO_Trace			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Trace',			3 =>'Japaness',	4 =>'리뷰');
$SK_BO_Update			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Update',			3 =>'Japaness',	4 =>'등록');
$SK_BO_URL_Main			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'URL(Main)',		3 =>'Japaness',	4 =>'URL(주)');
$SK_BO_URL_Mirror		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'URL(Json)',		3 =>'Japaness',	4 =>'URL(Json)');
$SK_BO_Week				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Week',				3 =>'Japaness',	4 =>'주');
$SK_BO_Weekly			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Weekly',			3 =>'Japaness',	4 =>'주간');
$SK_BO_Write			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Write',			3 =>'Japaness',	4 =>'글쓰기');
$SK_BO_Zone				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Zone',				3 =>'Japaness',	4 =>'지역');
	
$SK_BO_Sun				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sun',				3 =>'Japaness',	4 =>'일');
$SK_BO_Mon				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Mon',				3 =>'Japaness',	4 =>'월');
$SK_BO_Tue				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Tue',				3 =>'Japaness',	4 =>'화');
$SK_BO_Wed				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Wed',				3 =>'Japaness',	4 =>'수');
$SK_BO_Thu				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Thu',				3 =>'Japaness',	4 =>'목');
$SK_BO_Fri				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Fri',				3 =>'Japaness',	4 =>'금');
$SK_BO_Sat				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sat',				3 =>'Japaness',	4 =>'토');

$SK_BO_Sunday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sunday',			3 =>'Japaness',	4 =>'일요일');
$SK_BO_Monday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monday',			3 =>'Japaness',	4 =>'월요일');
$SK_BO_Tuesday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Tuesday',			3 =>'Japaness',	4 =>'화요일');
$SK_BO_Wednesday		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Wednesday',		3 =>'Japaness',	4 =>'수요일');
$SK_BO_Thursday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Thursday',			3 =>'Japaness',	4 =>'목요일');
$SK_BO_Friday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Friday',			3 =>'Japaness',	4 =>'금요일');
$SK_BO_Saturday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Saturday',			3 =>'Japaness',	4 =>'토요일');

$SK_BO_January			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'January',			3 =>'Japaness',	4 =>'1월');
$SK_BO_February 		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'February',			3 =>'Japaness',	4 =>'2월');
$SK_BO_March			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'March',			3 =>'Japaness',	4 =>'3월');
$SK_BO_April			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'April',			3 =>'Japaness',	4 =>'4월');
$SK_BO_May				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'May',				3 =>'Japaness',	4 =>'5월');
$SK_BO_June				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'June',				3 =>'Japaness',	4 =>'6월');
$SK_BO_July				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'July',				3 =>'Japaness',	4 =>'7월');
$SK_BO_August			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'August',			3 =>'Japaness',	4 =>'8월');
$SK_BO_September		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'September',		3 =>'Japaness',	4 =>'9월');
$SK_BO_October			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'October',			3 =>'Japaness',	4 =>'10월');
$SK_BO_November			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'November',			3 =>'Japaness',	4 =>'11월');
$SK_BO_December			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'December',			3 =>'Japaness',	4 =>'12월');

$SK_BO_Jan				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Jan',				3 =>'Japaness',	4 =>'1월');
$SK_BO_Feb				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Feb',				3 =>'Japaness',	4 =>'2월');
$SK_BO_Mar				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Mar',				3 =>'Japaness',	4 =>'3월');
$SK_BO_Apr				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Apr',				3 =>'Japaness',	4 =>'4월');
$SK_BO_May				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'May',				3 =>'Japaness',	4 =>'5월');
$SK_BO_Jun				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Jun',				3 =>'Japaness',	4 =>'6월');
$SK_BO_Jul				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Jul',				3 =>'Japaness',	4 =>'7월');
$SK_BO_Aug				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Aug',				3 =>'Japaness',	4 =>'8월');
$SK_BO_Sep				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sep',				3 =>'Japaness',	4 =>'9월');
$SK_BO_Oct				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Oct',				3 =>'Japaness',	4 =>'10월');
$SK_BO_Nov				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Nov',				3 =>'Japaness',	4 =>'11월');
$SK_BO_Dec				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Dec',				3 =>'Japaness',	4 =>'12월');

$SK_BO_Today			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Today',			3 =>'Japaness',	4 =>'오늘');
$SK_BO_Monthly			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monthly',			3 =>'Japaness',	4 =>'월간');



$SK_BO_Delete_event		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Delete the selected event.',		3 =>'XXX',			4 =>'선택한 이밴트를 삭제합니다.');
$SK_BO_Link_Interface	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor and linked interface.',		3 =>'XXX',			4 =>'센서와 연결된 인터페이스');
$SK_BO_Link_Alarm		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor and linked alert.',			3 =>'XXX',			4 =>'센서와 연결된 알람');
$SK_BO_Conform_Reboot	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Do you want to restart the system?',3 =>'XXX',		4 =>'시스템을 재 시작 합니다.');
$SK_BO_Conform_Shutdown	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Do you want to shutdown the system?',3 =>'XXX',		4 =>'시스템을 종료 합니다. 전원은 최소 20초 후에 제거 하시기 바랍니다.');
$SK_BO_Close_this_window		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Close_this_window',		3 =>'XXX',			4 =>'현재 창 닫기');
$SK_BO_Download_CSV		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Download_CSV',		3 =>'XXX',		4 =>'엑셀 다운로드');



/*

<?php echo $SK_BO_Delete_event[ITS_Lang]?>

일 <?php echo $SK_BO_Sun[ITS_Lang]?>
월 <?php echo $SK_BO_Mon[ITS_Lang]?>
화 <?php echo $SK_BO_Tue[ITS_Lang]?>
수 <?php echo $SK_BO_Wed[ITS_Lang]?>
목 <?php echo $SK_BO_Thu[ITS_Lang]?>
금 <?php echo $SK_BO_Fri[ITS_Lang]?>
토 <?php echo $SK_BO_Sat[ITS_Lang]?>

월별		<?php echo $SK_BO_Monthly[ITS_Lang]?>
>사용중지<   ><?php echo $SK_BO_Disable[ITS_Lang]?><
>일시정지<   ><?php echo $SK_BO_Pause[ITS_Lang]?><
>알람정지<   ><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><
>즉시적용<   ><?php echo $SK_BO_Apply[ITS_Lang]?><
>모델명<    ><?php echo $SK_BO_Model_Name[ITS_Lang]?><
>디바이스<   ><?php echo $SK_BO_Device_Name[ITS_Lang]?><
>고유번호<   ><?php echo $SK_BO_Serial_Number[ITS_Lang]?><
>감지범위<   ><?php echo $SK_BO_Detect_Range[ITS_Lang]?><
> 미터      > <?php echo $SK_BO_Meter[ITS_Lang]?>
>허용직경<   ><?php echo $SK_BO_Allowable_Diameter[ITS_Lang]?><
> 센티미터   > <?php echo $SK_BO_Cmeter[ITS_Lang]?>
>허용회수< >허용횟수<   ><?php echo $SK_BO_Event_Count[ITS_Lang]?><
> 회 >회      > <?php echo $SK_BO_Times[ITS_Lang]?>
>무시영역<   ><?php echo $SK_BO_Ignore_Area[ITS_Lang]?><
>시작좌표<   ><?php echo $SK_BO_Start_Coord[ITS_Lang]?><
>종료좌표<   ><?php echo $SK_BO_End_Coord[ITS_Lang]?><
>예약차단<   ><?php echo $SK_BO_Reservation[ITS_Lang]?><
>대기시간<   ><?php echo $SK_BO_Event_Hold[ITS_Lang]?><
>센서방향<   ><?php echo $SK_BO_Sensor_Face[ITS_Lang]?><
>센서방위<   ><?php echo $SK_BO_Sensor_Azimuth[ITS_Lang]?><
> 도       > <?php echo $SK_BO_Angle[ITS_Lang]?>
'수정':'신규'		'<?php echo $SK_BO_Modify[ITS_Lang]?>':'<?php echo $SK_BO_New[ITS_Lang]?>'	

관리명	고유 번호	센서 IP	호스트 A	호스트 B
시리얼	방향	수용량	현재량


>감지횟수<     ><?php echo $SK_BO_Event_Count[ITS_Lang]?><
>감지지역<     ><?php echo $SK_BO_Sensing_Boundary[ITS_Lang]?><
>경보유지<     ><?php echo $SK_BO_Event_Hold[ITS_Lang]?><
>거리고정<     ><?php echo $SK_BO_Hold_Distance[ITS_Lang]?><
>등록<     ><?php echo $SK_BO_Update[ITS_Lang]?><
기본설정     <?php echo $SK_BO_Basic[ITS_Lang]?>
고급설정     <?php echo $SK_BO_Advanced[ITS_Lang]?>
>관리/센서타입<     ><?php echo $SK_BO_Name[ITS_Lang]?><
>관리/모델명<     ><?php echo $SK_BO_Name[ITS_Lang]?><
"저장"     "<?php echo $SK_BO_Save[ITS_Lang]?>"
>취소<     ><?php echo $SK_BO_Cancel[ITS_Lang]?><
>허용조건<     ><?php echo $SK_BO_Allowable[ITS_Lang]?><

>시작<     ><?php echo $SK_BO_Start[ITS_Lang]?><
>종료<     ><?php echo $SK_BO_End[ITS_Lang]?><
>허용감도<     ><?php echo $SK_BO_Sensitivity[ITS_Lang]?><
>허용범주<     ><?php echo $SK_BO_Accept_Boundary[ITS_Lang]?><
>경보주기<     ><?php echo $SK_BO_Alarm_Cycle[ITS_Lang]?><
>주기고정<     ><?php echo $SK_BO_Fix_Cycle[ITS_Lang]?><
>위치<     ><?php echo $SK_BO_Location[ITS_Lang]?><
>예약<     ><?php echo $SK_BO_Reserve[ITS_Lang]?><
>사진<     ><?php echo $SK_BO_Snapshot[ITS_Lang]?><
>알람로그<     ><?php echo $SK_BO_Log[ITS_Lang]?><
>알람위치<     ><?php echo $SK_BO_Position[ITS_Lang]?><
>시작편차<     ><?php echo $SK_BO_Offset[ITS_Lang]?><
>레벨/지연<     ><?php echo $SK_BO_Level[ITS_Lang]?>/<?php echo $SK_BO_Delay[ITS_Lang]?><
(약 대략  (<?php echo $SK_BO_About[ITS_Lang]?>






허용범위  <?php echo $SK_BO_Accept_Range[ITS_Lang]?>
메뉴  <?php echo $SK_HD_Menu[ITS_Lang]?>
시간동기  <?php echo $SK_HD_Sync_Clock[ITS_Lang]?>
재부팅  <?php echo $SK_HD_Reboot[ITS_Lang]?>
정보수정  <?php echo $SK_HD_Info[ITS_Lang]?>
로그아웃  <?php echo $SK_HD_Logout[ITS_Lang]?>
로그인  <?php echo $SK_HD_Login[ITS_Lang]?>
URL(부)   <?php echo $SK_BO_URL_Mirror[ITS_Lang]?>
URL(주)   <?php echo $SK_BO_URL_Main[ITS_Lang]?>
검색  <?php echo $SK_BO_Search[ITS_Lang]?>
경보   <?php echo $SK_BO_Alert[ITS_Lang]?>
글쓰기  <?php echo $SK_BO_Write[ITS_Lang]?>
다음   <?php echo $SK_BO_Next[ITS_Lang]?>
대기  <?php echo $SK_BO_Hold[ITS_Lang]?>
라이센스   <?php echo $SK_BO_License[ITS_Lang]?>
마스터   <?php echo $SK_BO_Master[ITS_Lang]?>
모니터   <?php echo $SK_BO_Monitor[ITS_Lang]?>
목록  <?php echo $SK_BO_List[ITS_Lang]?>
방향   <?php echo $SK_BO_Direction[ITS_Lang]?>
분류  <?php echo $SK_BO_Category[ITS_Lang]?>
비밀번호  <?php echo $SK_BO_password[ITS_Lang]?>
삭제  <?php echo $SK_BO_Delete[ITS_Lang]?>
상시차단  <?php echo $SK_BO_Blocked[ITS_Lang]?>
선택하세요  <?php echo $SK_BO_Choose[ITS_Lang]?>
센서관리명  <?php echo $SK_BO_Sensor_Name[ITS_Lang]?>
수정  <?php echo $SK_BO_Modify[ITS_Lang]?>
스케줄   <?php echo $SK_BO_Schedule[ITS_Lang]?>
스트리밍   <?php echo $SK_BO_Streaming[ITS_Lang]?>
신규  <?php echo $SK_BO_New[ITS_Lang]?>
암호화   <?php echo $SK_BO_Encryption[ITS_Lang]?>
영역   <?php echo $SK_BO_Range[ITS_Lang]?>
옵션  <?php echo $SK_BO_Option[ITS_Lang]?>
이름  <?php echo $SK_BO_Name[ITS_Lang]?>
이메일  <?php echo $SK_BO_Email[ITS_Lang]?>
이벤트   <?php echo $SK_BO_Events[ITS_Lang]?>
이벤트  <?php echo $SK_BO_Event[ITS_Lang]?>
이벤트주기  <?php echo $SK_BO_Event_Cycle[ITS_Lang]?>
이전   <?php echo $SK_BO_Previous[ITS_Lang]?>
일  <?php echo $SK_BO_Day[ITS_Lang]?>
작성완료  <?php echo $SK_BO_Save2[ITS_Lang]?>
재실행  <?php echo $SK_BO_Restart[ITS_Lang]?>
주  <?php echo $SK_BO_Week[ITS_Lang]?>
지역   <?php echo $SK_BO_Zone[ITS_Lang]?>
지역차단  <?php echo $SK_BO_Area_Block[ITS_Lang]?>?>
초  <?php echo $SK_BO_Second[ITS_Lang]?>
키   <?php echo $SK_BO_Key[ITS_Lang]?>
포트  <?php echo $SK_BO_Port[ITS_Lang]?>
호스트(부)   <?php echo $SK_BO_Host_Mirror[ITS_Lang]?>
호스트(주)   <?php echo $SK_BO_Host_Main[ITS_Lang]?>
홈페이지  <?php echo $SK_BO_Home_Page[ITS_Lang]?>
*/

?>                                                                                                                                                                                                                                                                                                                                                                                                                         phpinfo.php                                                                                         0000664 0001751 0001751 00000000031 14047704766 011051  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
echo phpinfo();
?>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       tail.php                                                                                            0000664 0001751 0001751 00000004425 14222407307 010334  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

if (G5_IS_MOBILE) {
    include_once(G5_THEME_MOBILE_PATH.'/tail.php');
    return;
}
// if ($config['cf_10']) {
// 	$copyright = $config['cf_10'];
// } else {
// 	$copyright = "ECOS Co., Ltd.";
// }
$copyright = "ECOS";
?>

<!-- // 라이센스 등록 유무 표시 G:\Development\ecos_ITS\its_common\watchdog.py -->
<?php
$filename = G5_CU_PATH_CONFIG."/systemMsg.htm";

if (file_exists($filename)) {
	// echo "$filename was last modified: " . date ("F d Y H:i:s.", filemtime($filename));
	$diff = time()-filemtime($filename);
	if($diff > G5_CU_WATCHDOG_INTV) {
		$htmlTag = "<div id='license' style='cursor:pointer;position:absolute;top:0;left:0;background:#ff0000;color:#fff;padding: 0 4px;z-index: 1;'>No Watchdog Daemon, Call Administrator</div>";
	} else {
		$htmlTag = file_get_contents($filename);
	}
} else {
	$htmlTag = "<div id='license' style='cursor:pointer;position:absolute;top:0;left:0;background:#ff0000;color:#fff;padding: 0 4px;z-index: 1;'>Abnormal State, Call Administrator</div>";
}
?>
<div id='license' onclick='noLicense()'><?php echo $htmlTag?></div>
<script>function noLicense() { window.open('<?php echo G5_THEME_URL ?>/skin/board/w_include_license/noLicense.php', 'License Request', 'toolbar=no,scrollbars=no,resizable=no,top=0,left=0,width=400,height=360'); }</script>

	<div style="font-size: 8pt; text-align: center;color: #ececec;">Copyright &copy; <?php echo $copyright?> All rights reserved.</div>
</div>
<!-- } 콘텐츠 끝 -->

<!-- 하단 시작 { -->
<div class="container" style="position:fixed;right:0;left:0;bottom:0;border-top:1px solid #b7b7b745;background:#f2f5f900;">
	<div style="font-size:8pt;text-align:right;">
		<div>
			<!-- a href="<?php echo G5_BBS_URL; ?>/content.php?co_id=company">회사소개</a>
			<a href="<?php echo G5_BBS_URL; ?>/content.php?co_id=privacy">개인정보처리방침</a>
			<a href="<?php echo G5_BBS_URL; ?>/content.php?co_id=provision">서비스이용약관</a>
			<a href="<?php echo G5_BBS_URL; ?>/content.php?co_id=about">About ITS</a -->
		</div>
	</div>
</div>
<!-- } 하단 끝 -->


<?php
if ($config['cf_analytics']) {
    echo $config['cf_analytics'];
}
include_once(G5_THEME_PATH."/tail.sub.php");
?>
                                                                                                                                                                                                                                           tail.sub.php                                                                                        0000664 0001751 0001751 00000001362 14047704766 011137  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가
?>

<?php if ($is_admin == 'super') {  ?><!-- <div style='float:left; text-align:center;'>RUN TIME : <?php echo get_microtime()-$begin_time; ?><br></div> --><?php }  ?>

<!-- ie6,7에서 사이드뷰가 게시판 목록에서 아래 사이드뷰에 가려지는 현상 수정 -->
<!--[if lte IE 7]>
<script>
$(function() {
    var $sv_use = $(".sv_use");
    var count = $sv_use.length;

    $sv_use.each(function() {
        $(this).css("z-index", count);
        $(this).css("position", "relative");
        count = count - 1;
    });
});
</script>
<![endif]-->

</body>
</html>
<?php echo html_end(); // HTML 마지막 처리 함수 : 반드시 넣어주시기 바랍니다. ?>                                                                                                                                                                                                                                                                              theme.config.php                                                                                    0000664 0001751 0001751 00000023703 14222160526 011750  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// 테마가 지원하는 장치 설정 pc, mobile
// 선언하지 않거나 값을 지정하지 않으면 그누보드5의 설정을 따른다.
// G5_SET_DEVICE 상수 설정 보다 우선 적용됨
define('G5_THEME_DEVICE', 'pc');

$theme_config = array();

// 갤러리 이미지 수 등의 설정을 지정하시면 게시판관리에서 해당 값을
// 가져오기 기능을 통해 게시판 설정의 해당 필드에 바로 적용할 수 있습니다.
// 사용하지 않는 스킨 설정은 값을 비워두시면 됩니다.

$theme_config = array(
	'set_default_skin'          => false,   // 기본환경설정의 최근게시물 등의 기본스킨 변경여부 true, false
	'preview_board_skin'        => 'basic', // 테마 미리보기 때 적용될 기본 게시판 스킨
	'preview_mobile_board_skin' => 'basic', // 테마 미리보기 때 적용될 기본 모바일 게시판 스킨
	'cf_member_skin'            => 'basic', // 회원 스킨
	'cf_mobile_member_skin'     => 'basic', // 모바일 회원 스킨
	'cf_new_skin'               => 'basic', // 최근게시물 스킨
	'cf_mobile_new_skin'        => 'basic', // 모바일 최근게시물 스킨
	'cf_search_skin'            => 'basic', // 검색 스킨
	'cf_mobile_search_skin'     => 'basic', // 모바일 검색 스킨
	'cf_connect_skin'           => 'basic', // 접속자 스킨
	'cf_mobile_connect_skin'    => 'basic', // 모바일 접속자 스킨
	'cf_faq_skin'               => 'basic', // FAQ 스킨
	'cf_mobile_faq_skin'        => 'basic', // 모바일 FAQ 스킨
	'bo_gallery_cols'           => 4,       // 갤러리 이미지 수
	'bo_gallery_width'          => 174,     // 갤러리 이미지 폭
	'bo_gallery_height'         => 124,     // 갤러리 이미지 높이
	'bo_mobile_gallery_width'   => 125,     // 모바일 갤러리 이미지 폭
	'bo_mobile_gallery_height'  => 100,     // 모바일 갤러리 이미지 높이
	'bo_image_width'            => 600,     // 게시판 뷰 이미지 폭
	'qa_skin'                   => 'basic', // 1:1문의 스킨
	'qa_mobile_skin'            => 'basic'  // 1:1문의 모바일 스킨
);

///////////// 커스텀 환경설정 /////////////////
///////////// 커스텀 환경설정 /////////////////
///////////// 커스텀 환경설정 /////////////////

define('G5_CU_UTIL_URL', G5_THEME_URL.'/utility');
define('G5_CU_UTIL_PATH', G5_THEME_PATH.'/utility');

define('G5_CU_IMG_URL', G5_DATA_URL.'/image');
define('G5_CU_IMG_PATH', G5_DATA_PATH.'/image');

define('G5_CU_AUD_URL', G5_DATA_URL.'/audio');
define('G5_CU_AUD_PATH', G5_DATA_PATH.'/audio');

define('G5_CU_VDO_URL', G5_DATA_URL.'/video');
define('G5_CU_VDO_PATH', G5_DATA_PATH.'/video');

define('G5_CU_CFG_URL', G5_DATA_URL.'/config');
define('G5_CU_CFG_PATH', G5_DATA_PATH.'/config');

define('G5_CU_MAP_URL', G5_CU_IMG_URL.'/ims');
define('G5_CU_MAP_PATH', G5_CU_IMG_PATH.'/ims');

define('DAIVOC_MAIL', 'daivoc@gmail.com'); // 개발자 메일
define('G5_CU_MAIL_ADDR', 'support@ecoskorea.com'); // 메일 전송시 발시자명
define('G5_CU_PUBLIC_NAME', 'ECOS');
define('G5_CU_MAIL_DEVELOPER', DAIVOC_MAIL); // 개발자 메일명

// 사용 : G:\Development\ecos_its-OPTEX\its_web\theme\ecos-its_optex\skin\member\basic\register_form.skin.php
$g5_cu_language = array(
	// 'its_webC' => 'Chinese',
	'its_webE' => 'English',
	// 'its_webJ' => 'Japaness',
	'its_webK' => 'Korean'
);

// 사용 : G:\Development\ecos_its-OPTEX\its_web\theme\ecos-its_optex\skin\member\basic\register_form.skin.php
$g5_cu_ioBoard = array(
	'std' => 'STD',
	'acu' => 'ACU',
	'psw' => 'PSW' // Power Switch
);

$g5_cu_systemType = array(
	'its' => 'ITS',
	'ims' => 'IMS'
);

$gJson = json_decode(file_get_contents("/home/pi/common/config.json"), TRUE);
// print_r($gJson);
// echo $gJson['license']['key_system];

define('G5_CU_CONF_MANUAL', 'g000t100');
define('G5_CU_CONF_RXTX', 'g100t100');
define('G5_CU_CONF_RELAY', 'g100t160');
define('G5_CU_CONF_BSS', 'g200t100');
define('G5_CU_CONF_BSS_R', 'g200t110');
define('G5_CU_CONF_SPEED', 'g200t120');
define('G5_CU_CONF_RLS', 'g200t200');
define('G5_CU_CONF_RLS_R', 'g200t210');
define('G5_CU_CONF_PARKING', 'g200t220');
define('G5_CU_CONF_RLS_T', 'g200t240');
define('G5_CU_CONF_BIND', 'g200t400');
define('G5_CU_CONF_SPOT', 'g200t500');
define('G5_CU_CONF_GPIO', 'g300t100');
define('G5_CU_CONF_COUNTER', 'g300t200');
define('G5_CU_CONF_GPCIO', 'g300t300');
define('G5_CU_CONF_GPACU', 'g300t400');
define('G5_CU_CONF_GPWIO', 'g300t500');
define('G5_CU_CONF_GIKEN_P', 'g400t200');
define('G5_CU_CONF_GIKEN_T', 'g400t300');
define('G5_CU_CONF_TAILING', 'g400t400');
define('G5_CU_CONF_GIKEN_C', 'g400t500');
define('G5_CU_CONF_CAMERA', 'g500t100');
define('G5_CU_CONF_ZONE', 'g500t200');
define('G5_CU_CONF_BOX', 'g500t300');

$G5_CU_CONF_GROUP = array( 
	'G5_CU_CONF_MANUAL'	=> G5_CU_CONF_MANUAL,	
	'G5_CU_CONF_RXTX'	=> G5_CU_CONF_RXTX,	
	'G5_CU_CONF_RELAY'	=> G5_CU_CONF_RELAY,	
	'G5_CU_CONF_BSS'	=> G5_CU_CONF_BSS,	
	'G5_CU_CONF_BSS_R'	=> G5_CU_CONF_BSS_R,	
	'G5_CU_CONF_SPEED'	=> G5_CU_CONF_SPEED,	
	'G5_CU_CONF_RLS'	=> G5_CU_CONF_RLS,	
	'G5_CU_CONF_RLS_R'	=> G5_CU_CONF_RLS_R,	
	'G5_CU_CONF_PARKING'=> G5_CU_CONF_PARKING,	
	'G5_CU_CONF_RLS_T'	=> G5_CU_CONF_RLS_T,	
	'G5_CU_CONF_BIND'	=> G5_CU_CONF_BIND,	
	'G5_CU_CONF_SPOT'	=> G5_CU_CONF_SPOT,	
	'G5_CU_CONF_GPIO'	=> G5_CU_CONF_GPIO,
	'G5_CU_CONF_COUNTER'=> G5_CU_CONF_COUNTER,
	'G5_CU_CONF_GPCIO'	=> G5_CU_CONF_GPCIO,
	'G5_CU_CONF_GPACU'	=> G5_CU_CONF_GPACU,
	'G5_CU_CONF_GPWIO'	=> G5_CU_CONF_GPWIO,
	'G5_CU_CONF_GIKEN_P'=> G5_CU_CONF_GIKEN_P,
	'G5_CU_CONF_GIKEN_T'=> G5_CU_CONF_GIKEN_T,
	'G5_CU_CONF_TAILING'	=> G5_CU_CONF_TAILING,
	'G5_CU_CONF_GIKEN_C'=> G5_CU_CONF_GIKEN_C,
	'G5_CU_CONF_CAMERA'	=> G5_CU_CONF_CAMERA,
	'G5_CU_CONF_ZONE'	=> G5_CU_CONF_ZONE,
	'G5_CU_CONF_BOX'	=> G5_CU_CONF_BOX
);

define('G5_CU_MASTER_PORT', $gJson['port']['tableUnion']); // 연결된 모든 센서의 모니터링을 위한 TCP Port  예: $_SERVER['SERVER_ADDR'].":".G5_CU_MASTER_PORT
define('G5_CU_MASTER_NODE_0', G5_CU_MASTER_PORT + 2); // G5_CU_MASTER_PORT 데이터를 Node.js 서버가 읽고 G5_CU_MASTER_NODE_0 포트로 클라이언트 서비스
define('G5_CU_MASTER_NODE_1', G5_CU_MASTER_PORT + 4); // G5_CU_MASTER_PORT 데이터를 Node.js 서버가 읽고 G5_CU_MASTER_NODE_1 포트로 클라이언트 서비스

define('G5_CU_IMS_PORT', $gJson['port']['ims']); // RLS 모니터링을 위한 TCP Port 
define('G5_CU_GIKENP_PORT_IN', $gJson['port']['gikenp']['portIn']); // GIKEN 모니터링을 위한 TCP Port 
define('G5_CU_GIKENP_PORT_OUT', $gJson['port']['gikenp']['portOut']); // GIKEN 모니터링을 위한 TCP Port 
define('G5_CU_GIKENT_PORT_IN', $gJson['port']['gikent']['portIn']); // GIKEN 모니터링을 위한 TCP Port 
define('G5_CU_GIKENT_PORT_OUT', $gJson['port']['gikent']['portOut']); // GIKEN 모니터링을 위한 TCP Port 
define('G5_CU_TAILING_PORT_IN', $gJson['port']['tailing']['portIn']); // TAILING 모니터링을 위한 TCP Port 
define('G5_CU_TAILING_PORT_OUT', $gJson['port']['tailing']['portOut']); // TAILING 모니터링을 위한 TCP Port 
define('G5_CU_GIKENC_PORT_IN', $gJson['port']['gikenc']['portIn']); // GIKEN 모니터링을 위한 TCP Port 
define('G5_CU_GIKENC_PORT_OUT', $gJson['port']['gikenc']['portOut']); // GIKEN 모니터링을 위한 TCP Port 
define('G5_CU_SYSTEM_PORT_IN', $gJson['port']['systemIn']); // RLS 모니터링을 위한 TCP Port 
define('G5_CU_SYSTEM_PORT_OUT', $gJson['port']['systemOut']); // RLS 모니터링을 위한 TCP Port 
define('G5_CU_GPIO_PORT_IN', $gJson['port']['gpio']['portIn']); // GPIO 모니터링을 위한 TCP Port 
define('G5_CU_GPIO_PORT_OUT', $gJson['port']['gpio']['portOut']); // GPIO 모니터링을 위한 TCP Port 

define('G5_CU_WATCHDOG_INTV', $gJson["port"]["watchdog"]["interval"]); // 와치도그 파일 생성 주기

define('G5_CU_PATH_COUNTER', $gJson['path']['counter']);
define('G5_CU_PATH_GPIO', $gJson['path']['gpio']);
define('G5_CU_PATH_GPCIO', $gJson['path']['gpcio']);
define('G5_CU_PATH_GPACU', $gJson['path']['gpacu']);
define('G5_CU_PATH_GPWIO', $gJson['path']['gpwio']);
define('G5_CU_PATH_BSS', $gJson['path']['bss']);
define('G5_CU_PATH_BSS_R', $gJson['path']['bss_r']);
define('G5_CU_PATH_RLS', $gJson['path']['rls']);
define('G5_CU_PATH_RLS_R', $gJson['path']['rls_r']);
define('G5_CU_PATH_BIND', $gJson['path']['bind']);
define('G5_CU_PATH_SPEED', $gJson['path']['speed']);
define('G5_CU_PATH_GIKEN_P', $gJson['path']['gikenp']);
define('G5_CU_PATH_GIKEN_T', $gJson['path']['gikent']);
define('G5_CU_PATH_TAILING', $gJson['path']['tailing']);
define('G5_CU_PATH_GIKEN_C', $gJson['path']['gikenc']);
define('G5_CU_PATH_SPOTTER', $gJson['path']['spotter']);
define('G5_CU_PATH_PARKING', $gJson['path']['parking']);
define('G5_CU_PATH_CAMERA', $gJson['path']['camera']);
define('G5_CU_PATH_ZONE', $gJson['path']['zone']);
define('G5_CU_PATH_BOX', $gJson['path']['box']);
define('G5_CU_PATH_LOG', $gJson['path']['log']);
define('G5_CU_PATH_CONFIG', $gJson['path']['config']);

define('G5_CU_GPIO_ARR_IN', $gJson['gpio']['in']); // 
define('G5_CU_GPIO_ARR_OUT', $gJson['gpio']['out']); // 


define('G5_CU_LICENSE_SERVER', $gJson['license']['server_addr']); // 라이센스 서버 IP:PORT
define('G5_CU_LICENSE_URL', $gJson['license']['server_url']); // 라이센스 키 컨펌

// 시스템 시리얼 헤시코드
$serial = shell_exec("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2");
$serial = str_replace(array('.', ' ', "\n", "\t", "\r"), '', $serial);
$hash_key = hash('sha256', $serial);
$hash_otx = hash('sha256', shell_exec($hash_key));
$hash_its = hash('sha256', shell_exec($hash_otx));

define('G5_CU_ITS_SERIAL', $serial); // 기초 프로그램을 가동
define('G5_CU_ITS_HASH_KEY', $hash_key); // 기초 프로그램을 가동
define('G5_CU_ITS_HASH_OTX', $hash_otx); // 응용 프로그램 가동
define('G5_CU_ITS_HASH_ITS', $hash_its); // 관리 및 정비 프로그램 가동
?>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             