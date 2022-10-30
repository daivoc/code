<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
// licenseSrvAdd.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvCSV.php는 라이센스서버에 상주하는 프로그램 명이다.
// licenseSrvList.php는 라이센스서버에 상주하는 프로그램 명이다.
// 본 프로그램을 통해 ITS 라이센스 정보를 데이터베이스에 등록한다.
// 위치는 theme.config.php내 G5_CU_LICENSE_URL이 결정한다.
// 예 : define('G5_CU_LICENSE_URL', 'http://'.G5_CU_LICENSE_SERVER.'/ecosLicense');
// 데이터베이스 구성은 아래와 같으며 사전에 테이블 구성이 되어있어야 한다.
// 본 데이터베이스에 'system license' 등록은 제외되며
// application license 만 등록하는것을 원칙으로 한다.
// 각각의 스킨의 write_update.skin.php에서 include licenseSrv.php 실행 된다.

if (!$member['mb_10']) {
	$msg = "기본정보 등록후 센서등록 및 변경이 가능합니다.";
	$url = G5_BBS_URL."/member_confirm.php?url=".G5_BBS_URL."/register_form.php";
	echo ("<script LANGUAGE='JavaScript'> window.alert('$msg'); window.location.href='$url'; </script>");	
}