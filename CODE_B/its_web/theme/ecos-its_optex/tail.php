<?php
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
