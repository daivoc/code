<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
include_once(G5_LIB_PATH.'/thumbnail.lib.php');
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

// define('G5_CU_GIKEN_PORT_IN', 37000); // GIKEN 모니터링을 위한 TCP Port 
// define('G5_CU_GIKEN_PORT_OUT', 37100); // GIKEN 모니터링을 위한 TCP Port 
// python 예: port_out = share["port"]["gikenc"]["portOut"] + int(row['w_device_id'].split('.')[-2])
$monPortNo = G5_CU_GIKENC_PORT_OUT + explode(".", $view['w_device_id'])[2]; // 192.168.[168].30
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

<style>
#bo_v_con { display:none; }
#bo_v_atc { padding: 0; min-height: 0; }
.f_right { float: right; margin: 0 2px; }

</style>

<script type="text/javascript">
$(document).ready(function(){
	$('#btn_history').on('click', function(event) {        
		 $('#bo_v_con').toggle('show');
	});
	$('#btn_Snapshot').click(function(){
		window.open("http://<?php echo $_SERVER["SERVER_NAME"]."/theme/ecos-its_optex/utility/filemanager/fm2.php?PATH=theme|ecos-its_optex|user|image|gikenC|counting" ?>","Snapshot_Giken_<?php echo $view['w_sensor_serial']?>", "width=500,height=600,scrollbars=no");
		return false;
    });

	$('#btn_Events').click(function(){
		var f = document.getElementById('TheForm');
		$("#TheForm").attr("action","<?php echo G5_CU_UTIL_URL ?>/systemExec/realtime_tail.php");
		$("#TheForm").attr("target","Event Log");
		$('#TheForm input[name="w_sensor_serial"]').val("<?php echo $view['w_sensor_serial']?>");
		$('#TheForm input[name="wr_subject"]').val("<?php echo $view['wr_subject']?>");
		window.open('', 'Event Log','width=600,height=400,scrollbars=no');
		f.submit();
	});
	$('#btn_Monitor').click(function(){
		window.open("http://<?php echo $_SERVER["SERVER_NAME"].":".$monPortNo ?>","Realtime_Giken_<?php echo $view['w_sensor_serial']?>", "width=360,height=500,scrollbars=no");
		return false;
    });
	$('#btn_Setup').click(function(){
		window.open("http://<?php echo $_SERVER["SERVER_NAME"] ?>:16830","Realtime_Giken_Setup", "width=640, height=480,scrollbars=no");
		return false;
	});
	
	$('#btn_Restart').click(function(){
		restartMyself();
    });
});

function restartMyself() { // 실행 않됨 kill 권한 문제 인듣 ..
	var r = confirm("Restat can take up to 10 seconds.");
	if (r == true) {
		$.ajax({
			url :  "<?php echo G5_THEME_URL ?>/utility/systemExec/restartGIKENC.php",
		}).done(function(data) {
			console.log(data);
			alert(data);
		});
	}
}

</script>

<script src="<?php echo G5_JS_URL; ?>/viewimageresize.js"></script>

<form id="TheForm" method="post" action="" target="">
<input type="hidden" name="w_sensor_serial" value="" />
<input type="hidden" name="wr_subject" value="" />
</form>

<!-- 게시물 읽기 시작 { -->
<div id="bo_v_table"><?php echo $board['bo_subject']; ?></div>

<section class="success" id="header" style="padding:0;">
	<div class="container">
		<div class="intro-text">
			<span class="name "><?php echo $board['bo_subject'] ?><span class="sound_only"><?php echo $SK_BO_List[ITS_Lang]?></span></span>
			<hr>
			<span class="skills"></span>
		</div>
	</div>
</section>

<article id="bo_v" class="container">
	<div class="panel panel-success">
	<div class="its_version" style="float:left;color:silver;padding:4px 8px;font-size:8pt;"><?php echo get_w_program_info(G5_CU_CONF_GPWIO)[0]; ?></div>
	<header class="panel-heading">
		<h1 id="bo_v_title">
			<?php
			if ($category_name) echo $view['ca_name'].' | '; // 분류 출력 끝
			echo cut_str(get_text($view['wr_subject']), 70); // 글제목 출력
			?>
		</h1>
	</header>
	<div class="panel-body">
	<section id="bo_v_info">
		<h2>페이지 정보</h2>
		<strong><?php echo $view['name'] ?><?php if ($is_ip_view) { echo "&nbsp;($ip)"; } ?></strong>
		<span class="sound_only"></span><strong><?php echo date("y-m-d H:i", strtotime($view['wr_datetime'])) ?></strong>
		view<strong><?php echo number_format($view['wr_hit']) ?></strong>
		Comment<strong><?php echo number_format($view['wr_comment']) ?></strong>
	</section>

	<?php
	if ($view['file']['count']) {
		$cnt = 0;
		for ($i=0; $i<count($view['file']); $i++) {
			if (isset($view['file'][$i]['source']) && $view['file'][$i]['source'] && !$view['file'][$i]['view'])
				$cnt++;
		}
	}
		?>

	<?php if($cnt) { ?>
	<!-- 첨부파일 시작 { -->
	<section id="bo_v_file">
		<h2>첨부파일</h2>
		<ul>
		<?php
		// 가변 파일
		for ($i=0; $i<count($view['file']); $i++) {
			if (isset($view['file'][$i]['source']) && $view['file'][$i]['source'] && !$view['file'][$i]['view']) {
			?>
			<li>
				<a href="<?php echo $view['file'][$i]['href'];  ?>" class="view_file_download">
					<img src="<?php echo $board_skin_url ?>/img/icon_file.gif" alt="첨부">
					<strong><?php echo $view['file'][$i]['source'] ?></strong>
					<?php echo $view['file'][$i]['content'] ?> (<?php echo $view['file'][$i]['size'] ?>)
				</a>
				<span class="bo_v_file_cnt"><?php echo $view['file'][$i]['download'] ?><?php echo $SK_BO_Times[ITS_Lang]?> 다운로드</span>
				<span>DATE : <?php echo $view['file'][$i]['datetime'] ?></span>
			</li>
		<?php
			}
		}
			?>
		</ul>
	</section>
	<!-- } 첨부파일 끝 -->
	<?php } ?>

	<?php
	if ($view['link']) {
	?>
		<!-- 관련링크 시작 { -->
	<section id="bo_v_link">
		<h2>관련링크</h2>
		<ul>
		<?php
		// 링크
		$cnt = 0;
		for ($i=1; $i<=count($view['link']); $i++) {
			if ($view['link'][$i]) {
				$cnt++;
				$link = cut_str($view['link'][$i], 70);
			?>
			<li>
				<a href="<?php echo $view['link_href'][$i] ?>" target="_blank">
					<img src="<?php echo $board_skin_url ?>/img/icon_link.gif" alt="관련링크">
					<strong><?php echo $link ?></strong>
				</a>
				<span class="bo_v_link_cnt"><?php echo $view['link_hit'][$i] ?><?php echo $SK_BO_Times[ITS_Lang]?> 연결</span>
			</li>
		<?php
			}
		}
			?>
		</ul>
	</section>
	<!-- } 관련링크 끝 -->
	<?php } ?>

	<!-- 게시물 상단 버튼 시작 { -->
	<div id="bo_v_top">
		<?php
		ob_start();
			?>
		<?php if ($prev_href || $next_href) { ?>
		<ul class="bo_v_nb pager">
			<?php if ($prev_href) { ?><li><a href="<?php echo $prev_href ?>" class="previous"><span aria-hidden="true">&larr; </span> <?php echo $SK_BO_Previous[ITS_Lang]?></a></li><?php } ?>
			<?php if ($next_href) { ?><li><a href="<?php echo $next_href ?>" class="next"><?php echo $SK_BO_Next[ITS_Lang]?> <span aria-hidden="true"> &rarr;</span></a></li><?php } ?>
		</ul>
		<?php } ?>

		<ul class="bo_v_com">
			<?php if ($update_href) { ?><li><a href="<?php echo $update_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Modify[ITS_Lang]?></a></li><?php } ?>
            <?php if ($delete_href) { ?><li><a href="<?php echo $delete_href ?>" class="btn btn-sm btn-primary" onclick="del(this.href); return false;"><?php echo $SK_BO_Delete[ITS_Lang]?></a></li><?php } ?>
			<?php if ($search_href) { ?><li><a href="<?php echo $search_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Search[ITS_Lang]?></a></li><?php } ?>
			<li><a href="<?php echo $list_href ?>" class="btn btn-sm btn-success"><?php echo $SK_BO_List[ITS_Lang]?></a></li>
			<?php /* if ($write_href) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Write[ITS_Lang]?></a></li><?php } */ ?>
		</ul>
		<?php
		$link_buttons = ob_get_contents();
		ob_end_flush();
			?>
	</div>
	<!-- } 게시물 상단 버튼 끝 -->

	<div>
		<input type="button" value="<?php echo $SK_BO_History[ITS_Lang]?>" id="btn_history" class="btn btn-info">
		<input type="button" value="<?php echo $SK_BO_Setup[ITS_Lang]?>" id="btn_Setup" class="btn btn-danger f_right">
		<input type="button" value="<?php echo $SK_BO_Snapshot[ITS_Lang]?>" id="btn_Snapshot" class="btn btn-primary f_right">
		<input type="button" value="<?php echo $SK_BO_Events[ITS_Lang]?>" id="btn_Events" class="btn btn-warning f_right">
		<input type="button" value="<?php echo $SK_BO_Monitor[ITS_Lang]?>" id="btn_Monitor" class="btn btn-danger f_right">
		<!-- <input type="button" value="<?php echo $SK_BO_Restart[ITS_Lang]?>" id="btn_Restart" class="btn btn-danger f_right"> -->
	</div>

	<section id="bo_v_atc" class="col-md-10 col-md-offset-1">
		<h2 id="bo_v_atc_title">본문</h2>

		<?php
		// 파일 출력
		$v_img_count = count($view['file']);
		if($v_img_count) {
			echo "<div id=\"bo_v_img\">\n";

			for ($i=0; $i<=count($view['file']); $i++) {
				if ($view['file'][$i]['view']) {
					//echo $view['file'][$i]['view'];
					echo get_view_thumbnail($view['file'][$i]['view']);
				}
			}

			echo "</div>\n";
		}
			?>

		<!-- 본문 내용 시작 { -->
		<!-- div id="bo_v_con"><?php // echo get_view_thumbnail($view['content']); ?></div -->
		<div id="bo_v_con"><pre style="font-size: 9pt;white-space: pre-wrap;"><?php echo $view['wr_content']; ?></pre></div>
		<?php//echo $view['rich_content']; // {이미지:0} 과 같은 코드를 사용할 경우 ?>
		<!-- } 본문 내용 끝 -->

	</section>
	<section id="bo_v_atc" class="">
		<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="wr_subject">Title/Desc.<br>Device/ID</label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $view['wr_subject'] ?>" id="wr_subject" readonly class="form-control input25P" size="50" maxlength="255">
				<input type="text" name="w_sensor_desc" value="<?php echo $view['w_sensor_desc'] ?>" id="w_sensor_desc" readonly class="form-control input25P">
				<input type="text" name="w_device_id" value="<?php echo $view['w_device_id'] ?>" id="w_device_id" readonly class="form-control input25P">
				<input type="text" name="w_sensor_serial" value="<?php echo $view['w_sensor_serial'] ?>" id="w_sensor_serial" readonly class="form-control input25P" >
			</td>
		</tr>
		<tr class='w_detail_tr'>
			<th scope="row"><label>Sensor<br>Info</label></th>
			<td>
			<input type="text" name="w_giken_ip" value="<?php echo $view['w_giken_ip'] ?>" id="w_giken_ip" readonly class="form-control input25P" placeholder="GIKEN IP">
			<input type="text" name="w_giken_live_url" value="<?php echo $view['w_giken_live_url'] ?>" id="w_giken_live_url" readonly class="form-control input25P" placeholder="Live URL">
			<input type="text" name="w_giken_serial" value="<?php echo $view['w_giken_serial'] ?>" id="w_giken_serial" readonly class="form-control input10P" placeholder="GIKEN Serial">
			<input type="text" name="w_giken_verson" value="<?php echo $view['w_giken_verson'] ?>" id="w_giken_verson" readonly class="form-control input10P" placeholder="GIKEN Verson">
			</td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row"><label for="w_face_direction">Direction</label></th>
			<td>
			<div class="selectPart">D1:<br><input type="text" name="w_alert_Value" value="<?php echo $opject_direction[$view['w_face_direction_A']] ?>" id="w_face_direction_A" readonly class="form-control center"></div>
			<div class="selectPart">D2:<br><input type="text" name="w_alert_Value" value="<?php echo $opject_direction[$view['w_face_direction_B']] ?>" id="w_face_direction_B" readonly class="form-control center"></div>
			<div class="selectPart">D3:<br><input type="text" name="w_alert_Value" value="<?php echo $opject_direction[$view['w_face_direction_C']] ?>" id="w_face_direction_C" readonly class="form-control center"></div>
			<div class="selectPart">D4:<br><input type="text" name="w_alert_Value" value="<?php echo $opject_direction[$view['w_face_direction_D']] ?>" id="w_face_direction_D" readonly class="form-control center"></div>
			</td>
		</tr>
		<tr class='w_hide'>
			<th scope="row"><label>Zone Setting<br>Filter Limit<br>Pre Process</label>
			<span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Over Size</label><input type="checkbox" class="form-control" name="w_opencv_tuner" id="w_opencv_tuner" value="1" <?php echo $write[w_opencv_tuner]?'checked':'';?> disabled ></span>
			</th>
			<td>
			<div class="inputPart">Crop Width Start:<br><input type="text" name="w_opencv_crop_x" value="<?php echo $view['w_opencv_crop_x'] ?>" id="w_opencv_crop_x" readonly class="form-control" placeholder="w_opencv_crop_x" size="50"></div>
			<div class="inputPart">Crop Width End:<br><input type="text" name="w_opencv_crop_w" value="<?php echo $view['w_opencv_crop_w'] ?>" id="w_opencv_crop_w" readonly class="form-control" placeholder="w_opencv_crop_w" size="50"></div>
			<div class="inputPart">Crop Height Start:<br><input type="text" name="w_opencv_crop_y" value="<?php echo $view['w_opencv_crop_y'] ?>" id="w_opencv_crop_y" readonly class="form-control" placeholder="w_opencv_crop_y" size="50"></div>
			<div class="inputPart">Crop Height End:<br><input type="text" name="w_opencv_crop_h" value="<?php echo $view['w_opencv_crop_h'] ?>" id="w_opencv_crop_h" readonly class="form-control" placeholder="w_opencv_crop_h" size="50"></div>
			<div class="inputPart">Noise Remove:<br><input type="text" name="w_opencv_filter" value="<?php echo $view['w_opencv_filter'] ?>" id="w_opencv_filter" readonly class="form-control"></div>
			<div class="inputPart">Threshold:<br><input type="text" name="w_opencv_threshold" value="<?php echo $view['w_opencv_threshold'] ?>" id="w_opencv_threshold" readonly class="form-control" size="50"></div>
			<div class="hide">gBlur:<br><input type="text" name="w_opencv_gBlur" value="<?php echo $view['w_opencv_gBlur'] ?>" id="w_opencv_gBlur" readonly class="form-control" size="50"></div>
			<div class="hide">Canny:<br><input type="text" name="w_opencv_canny" value="<?php echo $view['w_opencv_canny'] ?>" id="w_opencv_canny" readonly class="form-control" size="50"></div>
			<div class="hide">Kernel:<br><input type="text" name="w_opencv_kernel" value="<?php echo $view['w_opencv_kernel'] ?>" id="w_opencv_kernel" readonly class="form-control" size="50"></div>
			<!-- <span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Permit</label><input type="checkbox" class="form-control" name="w_allow_permit" id="w_allow_permit" value="1" <?php echo $view[w_allow_permit]?'checked':'';?> disabled ></span> -->
			<!-- <span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Multiple</label><input type="checkbox" class="form-control" name="w_allow_multiple" id="w_allow_multiple" value="1" <?php echo $view[w_allow_multiple]?'checked':'';?> disabled ></span> -->
			<span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Image Log</label><input type="checkbox" class="form-control" name="w_opencv_iLog" id="w_opencv_iLog" value="1" <?php echo $view[w_opencv_iLog]?'checked':'';?> disabled ></span>
			<hr>
			<div class="inputPart">Limit Width:<br><input type="text" name="w_opencv_object_w" value="<?php echo $view['w_opencv_object_w'] ?>" id="w_opencv_object_w" readonly class="form-control" size="50"></div>
			<div class="inputPart">Limit Height:<br><input type="text" name="w_opencv_object_h" value="<?php echo $view['w_opencv_object_h'] ?>" id="w_opencv_object_h" readonly class="form-control" size="50"></div>
			<div class="inputPart">Limit Pixel:<br><input type="text" name="w_opencv_object_p" value="<?php echo $view['w_opencv_object_p'] ?>" id="w_opencv_object_p" readonly class="form-control" size="50"></div>
			</td>
		</tr>
		<tr class='w_detail_tr w_hide'>
			<th scope="row"><label>Mask Primary</label></th>
			<td>
			<div class="inputPart">Width Start:<br><input type="text" name="w_opencv_mask_x" value="<?php echo $view['w_opencv_mask_x'] ?>" id="w_opencv_mask_x" readonly class="form-control" placeholder="w_opencv_mask_x" size="50"></div>
			<div class="inputPart">Width End:<br><input type="text" name="w_opencv_mask_w" value="<?php echo $view['w_opencv_mask_w'] ?>" id="w_opencv_mask_w" readonly class="form-control" placeholder="w_opencv_mask_w" size="50"></div>
			<div class="inputPart">Height Start:<br><input type="text" name="w_opencv_mask_y" value="<?php echo $view['w_opencv_mask_y'] ?>" id="w_opencv_mask_y" readonly class="form-control" placeholder="w_opencv_mask_y" size="50"></div>
			<div class="inputPart">Height End:<br><input type="text" name="w_opencv_mask_h" value="<?php echo $view['w_opencv_mask_h'] ?>" id="w_opencv_mask_h" readonly class="form-control" placeholder="w_opencv_mask_h" size="50"></div>
			<!-- <span  style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Use Mask</label><input type="checkbox" class="form-control" name="w_opencv_mask" id="w_opencv_mask" value="1" <?php echo $view[w_opencv_mask]?'checked':'';?> disabled ></span> -->
			</td>
		</tr>
		<tr class='w_detail_tr w_hide'>
			<th scope="row"><label>Mask Secondary</label></th>
			<td>
			<div class="inputPart">Width Start:<br><input type="text" name="w_opencv_mask2_x" value="<?php echo $view['w_opencv_mask2_x'] ?>" id="w_opencv_mask2_x" readonly class="form-control" placeholder="w_opencv_mask2_x" size="50"></div>
			<div class="inputPart">Width End:<br><input type="text" name="w_opencv_mask2_w" value="<?php echo $view['w_opencv_mask2_w'] ?>" id="w_opencv_mask2_w" readonly class="form-control" placeholder="w_opencv_mask2_w" size="50"></div>
			<div class="inputPart">Height Start:<br><input type="text" name="w_opencv_mask2_y" value="<?php echo $view['w_opencv_mask2_y'] ?>" id="w_opencv_mask2_y" readonly class="form-control" placeholder="w_opencv_mask2_y" size="50"></div>
			<div class="inputPart">Height End:<br><input type="text" name="w_opencv_mask2_h" value="<?php echo $view['w_opencv_mask2_h'] ?>" id="w_opencv_mask2_h" readonly class="form-control" placeholder="w_opencv_mask2_h" size="50"></div>
			</td>
		</tr>
		<tr class='w_detail_tr w_hide'>
			<th scope="row"><label>Mask Third</label></th>
			<td>
			<div class="inputPart">Width Start:<br><input type="text" name="w_opencv_mask3_x" value="<?php echo $view['w_opencv_mask3_x'] ?>" id="w_opencv_mask3_x" readonly class="form-control" placeholder="w_opencv_mask3_x" size="50"></div>
			<div class="inputPart">Width End:<br><input type="text" name="w_opencv_mask3_w" value="<?php echo $view['w_opencv_mask3_w'] ?>" id="w_opencv_mask3_w" readonly class="form-control" placeholder="w_opencv_mask3_w" size="50"></div>
			<div class="inputPart">Height Start:<br><input type="text" name="w_opencv_mask3_y" value="<?php echo $view['w_opencv_mask3_y'] ?>" id="w_opencv_mask3_y" readonly class="form-control" placeholder="w_opencv_mask3_y" size="50"></div>
			<div class="inputPart">Height End:<br><input type="text" name="w_opencv_mask3_h" value="<?php echo $view['w_opencv_mask3_h'] ?>" id="w_opencv_mask3_h" readonly class="form-control" placeholder="w_opencv_mask3_h" size="50"></div>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label>Relay<br>Output/Time</label></th>
			<td>
			<div class="inputPart">Inner:(1)<br><input type="text" name="w_alert_Value1" value="<?php echo $view['w_alert_Value1'] ?>" id="w_alert_Value1" readonly class="form-control" size="50"></div>
			<div class="inputPart">Outer:(2)<br><input type="text" name="w_alert_Value2" value="<?php echo $view['w_alert_Value2'] ?>" id="w_alert_Value2" readonly class="form-control" size="50"></div>
			<div class="inputPart">Unknown:(3)<br><input type="text" name="w_alert_Value3" value="<?php echo $view['w_alert_Value3'] ?>" id="w_alert_Value3" readonly class="form-control" size="50"></div>
			<span class="inputPart" style="width: 70px; margin: unset; display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Light:(4)</label><input type="checkbox" class="form-control" name="w_alert_Value4" id="w_alert_Value4" value="1" <?php echo $view[w_alert_Value4]?'checked':'';?> disabled ></span>
			<div class="inputPart">Light Lv(%):<br><input type="text" name="w_opencv_grayLv" value="<?php echo $view['w_opencv_grayLv'] ?>" id="w_opencv_grayLv" readonly class="form-control" size="50"></div>
			<span class="inputPart" style="width: 70px; margin: unset; display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Security</label><input type="checkbox" class="form-control" name="w_security_mode" id="w_security_mode" value="1" <?php echo $view[w_security_mode]?'checked':'';?> disabled ></span>
			<div class="inputPart">Time Over:<br><input type="text" name="w_reset_interval" value="<?php echo $view['w_reset_interval'] ?>" id="w_reset_interval" readonly class="form-control"></div>
			</td>
		</tr>

		<tr class='w_detail_tr w_hide'>
			<th scope="row"><label>GPIO<br>Output/Init.<br>Input/Mode</label></th>
			<td>
			<div class="inputPart">Status Relay:<br><input type="text" name="w_gpio_out" value="<?php echo $view['w_gpio_out'] ?>" readonly class="form-control" id="w_gpio_out"></div>
			<div class="inputPart">Status (NC):<br><input type="text" name="w_gpio_in" value="<?php echo $view['w_gpio_in'] ?>" readonly class="form-control" id="w_gpio_in"></div>
			<div class="inputPart">Bounce(mSec):<br><input type="text" name="w_bounce_time" value="<?php echo $view['w_bounce_time'] ?>" readonly class="form-control" id="w_bounce_time"></div>
			</td>
		</tr>

		<tr class='w_detail_tr w_hide'>
			<th scope="row"><label for="w_remote_accessible">Accessible<br>Remote IP</label></th>
			<td>
			<input type="text" name="w_remote_accessible" value="<?php echo $view['w_remote_accessible'] ?>" id="w_remote_accessible" readonly class="form-control input100P" placeholder="IP Ex:192.168.0.10,192.168.0.20" size="50">
			</td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_host_Addr">HOST IP/Port<br>for IMS</label></th>
			<td>
			<input type="text" name="w_host_Addr1" value="<?php echo $view['w_host_Addr1'] ?>" id="w_host_Addr1" readonly class="form-control input25P">
			<input type="text" name="w_host_Port1" value="<?php echo $view['w_host_Port1'] ?>" id="w_host_Port1" readonly class="form-control input25P">
			<input type="text" name="w_host_Addr2" value="<?php echo $view['w_host_Addr2'] ?>" id="w_host_Addr2" readonly class="form-control input25P">
			<input type="text" name="w_host_Port2" value="<?php echo $view['w_host_Port2'] ?>" id="w_host_Port2" readonly class="form-control input25P">
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_event_Addr">Event DB Server</label></th>
			<td>
			<input type="text" name="w_event_Addr1" value="<?php echo $view['w_event_Addr1'] ?>" id="w_event_Addr1" readonly class="form-control input25P">
			<input type="text" name="w_event_Port1" value="<?php echo $view['w_event_Port1'] ?>" id="w_event_Port1" readonly class="form-control input25P">
			<input type="text" name="w_event_Addr2" value="<?php echo $view['w_event_Addr2'] ?>" id="w_event_Addr2" readonly class="form-control input25P">
			<input type="text" name="w_event_Port2" value="<?php echo $view['w_event_Port2'] ?>" id="w_event_Port2" readonly class="form-control input25P">
			</td>
		</tr>

		<?php // include_once($board_skin_path.'/../w_include_acu/acuView.php'); // 원격릴레이 ACU ?>
		<?php include_once($board_skin_path.'/../w_include_custom/customView.php'); ?>
		<?php // include_once($board_skin_path.'/../w_include_custom/requestView.php'); ?>


		<tr class="w_detail_tr w_hide">
			<th scope="row"><label for="w_keycode">License</label></th>
			<td>
			<input type="text" name="w_keycode" value="<?php echo $view['w_keycode'] ?>" id="w_keycode" readonly class="hide form-control input50P">
			<input type="text" name="w_license" value="<?php echo $view['w_license'] ?>" id="w_license" readonly class="form-control input50P">
			</td>
		</tr>
		<tr class="w_detail_tr w_hide">
			<th scope="row"><label for="w_stamp">Last Modified</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($view['w_stamp']) ?>" id="w_stamp" readonly class="form-control input50P"></td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th class="w_hide" scope="row"><label for="w_sensor_disable"></label></th>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_disable" id="w_sensor_disable" value="1" <?php echo $view[w_sensor_disable]?'checked':'';?> disabled title="Permanently Disable GPWIO"></td>
		</tr>
		</tbody>
		</table>
	</section>

	<div style="float:left;margin-bottom:10px;clear:both;">
		<button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/status/printCFG.php?&bo_table=<?php echo $bo_table?>&wr_id=<?php echo $view['wr_id']?>", "Print Config");'>Print Config</button>
	</div>

	<!-- 링크 버튼 시작 { -->
	<div id="bo_v_bot">
		<?php echo $link_buttons ?>
	</div>
	<!-- } 링크 버튼 끝 -->
	</div>
	</div>
</article>
<!-- } 게시판 읽기 끝 -->

<script>
<?php if ($board['bo_download_point'] < 0) { ?>
$(function() {
    $("a.view_file_download").click(function() {
        if(!g5_is_member) {
            alert("다운로드 권한이 없습니다.\n회원이시라면 로그인 후 이용해 보십시오.");
            return false;
        }

        var msg = "파일을 다운로드 하시면 포인트가 차감(<?php echo number_format($board['bo_download_point']) ?>점)됩니다.\n\n포인트는 게시물당 한번만 차감되며 다음에 다시 다운로드 하셔도 중복하여 차감하지 않습니다.\n\n그래도 다운로드 하시겠습니까?";

        if(confirm(msg)) {
            var href = $(this).attr("href")+"&js=on";
            $(this).attr("href", href);

            return true;
        } else {
            return false;
        }
    });
});
<?php } ?>

function board_move(href)
{
    window.open(href, "boardmove", "left=50, top=50, width=500, height=550, scrollbars=1");
}
</script>

<script>
$(function() {
    $("a.view_image").click(function() {
        window.open(this.href, "large_image", "location=yes,links=no,toolbar=no,top=10,left=10,width=10,height=10,resizable=yes,scrollbars=no,status=no");
        return false;
    });

    // 추천, 비추천
    $("#good_button, #nogood_button").click(function() {
        var $tx;
        if(this.id == "good_button")
            $tx = $("#bo_v_act_good");
        else
            $tx = $("#bo_v_act_nogood");

        excute_good(this.href, $(this), $tx);
        return false;
    });

    // 이미지 리사이즈
    $("#bo_v_atc").viewimageresize();
});

function excute_good(href, $el, $tx)
{
    $.post(
        href,
        { js: "on" },
        function(data) {
            if(data.error) {
                alert(data.error);
                return false;
            }

            if(data.count) {
                $el.find("strong").text(number_format(String(data.count)));
                if($tx.attr("id").search("nogood") > -1) {
                    $tx.text("이 글을 비추천하셨습니다.");
                    $tx.fadeIn(200).delay(2500).fadeOut(200);
                } else {
                    $tx.text("이 글을 추천하셨습니다.");
                    $tx.fadeIn(200).delay(2500).fadeOut(200);
                }
            }
        }, "json"
    );
}
</script>
<!-- } 게시글 읽기 끝 -->