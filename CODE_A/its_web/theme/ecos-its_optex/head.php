<?php
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

<div id="container">