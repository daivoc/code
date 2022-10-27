<?php
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
?>