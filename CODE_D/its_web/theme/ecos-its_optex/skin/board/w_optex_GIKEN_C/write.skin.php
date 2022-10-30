<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

// /* 라이센스 등록 */
// include_once($board_skin_path.'/../w_include_license/licenseChk.php');
    
$detect = (get_w_detect_id()); // 현재의 릴레이포스 사용 상태

$title_msg =(($w == 'u')?$SK_BO_Modify[ITS_Lang]:$SK_BO_New[ITS_Lang]);
$g5['title'] = ((G5_IS_MOBILE && $board['bo_mobile_subject']) ? $board['bo_mobile_subject'] : $board['bo_subject']).' '.$title_msg;
$access_log = $write['wr_content'].'<br>'.$_SERVER[REMOTE_ADDR].':'.date("Y-m-d h:i:s").'-'.$title_msg.'-'.$member['mb_name'];

if($w == '') { // 신규 입력일떄
	include_once("$board_skin_path/sql.php"); // Local Function List
}
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">
<style>
th { width:120px; }
.wr_content_tr { display:none; }
.w_hide { display:none; }
.w_detail_tr { display:none; background-color: #fff8e1; font-size: 8pt; }
.w_detail_tr th { background-color: white; }
.w_default_tr { background-color: #f0f0f0; font-size: 8pt; }
.w_default_tr th { background-color: white; }
.w_number_input	{ border:0; width: 60px; color:#808080; text-align: right; font-size: 8pt; padding-right: 4pt; margin-bottom: 4px; }
.btn_option_01 { text-align: right; padding: 4px 0; }
.input75P { width: 75%; display: initial; float: left; margin:0; }
.input60P { width: 60%; display: initial; float: left; margin:0; }
.input50P { width: 50%; display: initial; float: left; margin:0; }
.input33P { width: 33%; display: initial; float: left; margin:0; }
.input25P { width: 25%; display: initial; float: left; margin:0; }
.input20P { width: 20%; display: initial; float: left; margin:0; }
.input16P { width: 16.5%; display: initial; float: left; margin:0; }
.weekday {width: 28px; float: left; text-align: center;}

.ckboxGrp {background:unset;}
.cRadio {text-align: center; width: 50px; float:left;}
</style>
<script>
function setValue(setGpioOut, obj) {
	var x = document.getElementsByName(obj), iset;
	for (var iset = 0; iset < setGpioOut.length; iset++) {
		if(setGpioOut[iset] == "1"){
			x[iset].checked = true;
		} else {
			x[iset].checked = false;
		}
	}
}
// function reSetValue(setGpioOut) {
// 	var x = document.getElementsByName("w_gpioOut[]"), iset;
// 	for (var iset = 0; iset < setGpioOut.length; iset++) {
// 		if(setGpioOut[iset] == "1"){
// 			x[iset].disabled = false;
// 		} else {
// 			x[iset].checked = false;
// 			x[iset].disabled = true;
// 		}
// 	}
// 	var curVal = updateValue("w_gpioOut");
// 	$( "#w_gpio_out" ).val(curVal);
// }

function updateValue(obj) {
	var tmpVal = ""
	$('input:checkbox[name^='+obj+']').each(function() {
		if ($(this).is(':checked')) {
			tmpVal = tmpVal + "1"
		} else {
			tmpVal = tmpVal + "0"
		}
	});
	return(tmpVal);
}

$(document).ready(function(){
	
	$('#btn_detail').on('click', function(event) {        
		 $('.w_detail_tr').toggle('show');
	});
	// $('#btn_default').on('click', function(event) {        
	// 	 $('.w_default_tr').toggle('show');
	// });

	$('#licenseToggle').click(function(){ // 활성 비횔성 토글
		console.log(this.id);
		$('#w_license').prop('readonly', function(i, v) { return !v; });
	});

	$('input:radio[name^="w_groupLevel"]').click(function () {
		$('input:radio[name^="w_groupLevel"]').each(function() {
			if ($(this).is(':checked')) {
				$( "#w_group_level" ).val($(this).val());
			}
		});
	});
	
	$('input:radio[name^="w_groupLevel"]').each(function() {
		if ($(this).val() == "<?php echo $write['w_group_level'] ?>") {
			$(this).attr("checked", true);
		}
	});

	$('input:checkbox[name^="w_gpioOut"]').click(function () {
		var curVal = updateValue("w_gpioOut");
		$("#w_gpio_out").val(curVal);
	});
	$('input:checkbox[name^="w_gpioIn"]').click(function () {
		var curVal = updateValue("w_gpioIn");
		$("#w_gpio_in").val(curVal);
	});

	
	// $('#w_opencv_tuner').on('click', function(event) {        
	// 	if ($(this).is(':checked')) {
	// 		;
	// 	} else {
	// 		$( "#w_opencv_crop_x, #w_opencv_crop_y, #w_opencv_crop_w, #w_opencv_crop_h, #w_opencv_filter, #w_opencv_threshold, #w_opencv_object_w, #w_opencv_object_h, #w_opencv_object_p" ).val(0);
	// 	}
	// });

	// setGpioIn 값은 최초 실행시 1로 설정 한다.
	var setGpioOut = "<?php if($write['w_gpio_out']) echo $write['w_gpio_out']; else echo '11110000'; ?>";
	setValue(setGpioOut, "w_gpioOut[]");
	// $("#w_gpio_out").val(setGpioOut);
	
	var setGpioIn = "<?php if($write['w_gpio_in']) echo $write['w_gpio_in']; else echo '11111111'; ?>";
	setValue(setGpioIn, "w_gpioIn[]");
	// $("#w_gpio_in").val(setGpioIn);
	// reSetValue(setGpioIn);
});
</script>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name "><?php echo $g5['title'] ?><span class="sound_only"><?php echo $SK_BO_List[ITS_Lang]?></span></span>
            <hr>
            <span class="skills"><?php echo $_SERVER['SERVER_ADDR'] ?></span>
        </div>
    </div>
</section>

<section id="bo_w" class="container">
	<h2 id="container_title"></h2>
	<!-- 게시물 작성/수정 시작 { -->
	<form name="fwrite" id="fwrite" action="<?php echo $action_url ?>" onsubmit="return fwrite_submit(this);" method="post" enctype="multipart/form-data" autocomplete="off" style="width:<?php echo $width; ?>">
	<input type="hidden" name="w" value="<?php echo $w ?>">
	<input type="hidden" name="bo_table" value="<?php echo $bo_table ?>">
	<input type="hidden" name="wr_id" value="<?php echo $wr_id ?>">
	<input type="hidden" name="sca" value="<?php echo $sca ?>">
	<input type="hidden" name="sfl" value="<?php echo $sfl ?>">
	<input type="hidden" name="stx" value="<?php echo $stx ?>">
	<input type="hidden" name="spt" value="<?php echo $spt ?>">
	<input type="hidden" name="sst" value="<?php echo $sst ?>">
	<input type="hidden" name="sod" value="<?php echo $sod ?>">
	<input type="hidden" name="page" value="<?php echo $page ?>">
	<?php
	$option = '';
	$option_hidden = '';
	if ($is_notice || $is_html || $is_secret || $is_mail) {
		$option = '';
		if ($is_notice) {
			$option .= "\n".'<input type="checkbox" id="notice" name="notice" value="1" '.$notice_checked.'>'."\n".'<label for="notice">공지</label>';
		}
		if ($is_html) {
			if ($is_dhtml_editor) {
				$option_hidden .= '<input type="hidden" value="html1" name="html">';
			} else {
				$option .= "\n".'<input type="checkbox" id="html" name="html" onclick="html_auto_br(this);" value="'.$html_value.'" '.$html_checked.'>'."\n".'<label for="html">html</label>';
			}
		}
		if ($is_secret) {
			if ($is_admin || $is_secret==1) {
				$option .= "\n".'<input type="checkbox" id="secret" name="secret" value="secret" '.$secret_checked.'>'."\n".'<label for="secret">비밀글</label>';
			} else {
				$option_hidden .= '<input type="hidden" name="secret" value="secret">';
			}
		}
		if ($is_mail) {
			$option .= "\n".'<input type="checkbox" id="mail" name="mail" value="mail" '.$recv_email_checked.'>'."\n".'<label for="mail">답변메일받기</label>';
		}
	}
	echo $option_hidden;
	?>

	<div class="btn_option_01">
		<!-- <input type="button" value="<?php echo $SK_BO_Basic[ITS_Lang]?>" id="btn_default" class="btn btn-warning"> -->
		<input type="button" value="<?php echo $SK_BO_Advanced[ITS_Lang]?>" id="btn_detail" class="btn btn-info">
	</div>

	<div class="tbl_wrap table-responsive">
		<table class="table table-bordered">
		<tbody>
		<?php if ($is_name) { ?>
		<tr>
			<th scope="row"><label for="wr_name"><?php echo $SK_BO_Name[ITS_Lang]?></label></th>
			<td><input type="text" name="wr_name" value="<?php echo $name ?>" id="wr_name" required class="form-control required" size="10" maxlength="20"></td>
		</tr>
		<?php } ?>
		<?php if ($is_password) { ?>
		<tr>
			<th scope="row"><label for="wr_password"><?php echo $SK_BO_Password[ITS_Lang]?></label></th>
			<td><input type="password" name="wr_password" id="wr_password" <?php echo $password_required ?> class="form-control <?php echo $password_required ?>" maxlength="20"></td>
		</tr>
		<?php } ?>
		<?php if ($is_email) { ?>
		<tr>
			<th scope="row"><label for="wr_email">이메일</label></th>
			<td><input type="text" name="wr_email" value="<?php echo $email ?>" id="wr_email" class="form-control email" size="50" maxlength="100"></td>
		</tr>
		<?php } ?>
		<?php if ($is_homepage) { ?>
		<tr>
			<th scope="row"><label for="wr_homepage">홈페이지</label></th>
			<td><input type="text" name="wr_homepage" value="<?php echo $homepage ?>" id="wr_homepage" class="form-control" size="50"></td>
		</tr>
		<?php } ?>
		<?php if ($option) { ?>
		<tr>
			<th scope="row"><?php echo $SK_BO_Option[ITS_Lang]?></th>
			<td><?php echo $option ?></td>
		</tr>
		<?php } ?>
		<?php if ($is_category) { ?>
		<tr>
			<th scope="row"><label for="ca_name">분류</label></th>
			<td>
				<select name="ca_name" id="ca_name" required class="required form-control" >
					<option value="">선택하세요</option>
					<?php echo $category_option ?>
				</select>
			</td>
		</tr>
		<?php } ?>
		<tr class="wr_content_tr w_hide">
			<th scope="row"><label for="wr_content"><?php echo $SK_BO_History[ITS_Lang]?></label></th>
			<td class="wr_content">
				<textarea id="wr_content" name="wr_content" class="" maxlength="65536" style="width:100%;height:300px"><?php echo $access_log ?></textarea>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class="w_hide">
			<th scope="row" title="ID"><label for="w_id">ITS/CPU ID</label></th>
			<td><input type="text" name="w_id" value="<?php echo $write['w_id'] ?>" id="w_id" class="form-control input50P" placeholder="Sensor ID" size="50"><input type="text" name="w_cpu_id" value="<?php echo get_w_cpu_id(); ?>" id="w_cpu_id" class="form-control input50P" placeholder="System CPU ID" size="50"></td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="wr_subject">Title/Desc.<br>Device/ID</label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control input25P required" placeholder="Sensor Name Ex: East Gate 3">
				<input type="text" name="w_sensor_desc" value="<?php echo $write['w_sensor_desc'] ?>" id="w_sensor_desc" class="form-control input25P" placeholder="Sensor Description">
				<?php echo select_w_etherNet_id($write['w_device_id']); ?>
				<input type="text" name="w_sensor_serial" value="<?php echo $write['w_sensor_serial'] ?>" id="w_sensor_serial" readonly class="form-control input25P" placeholder="Sensor Serial" size="50">
			</td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row"><label>Sensor<br>Info</label></th>
			<td>
			<input type="text" name="w_giken_ip" value="<?php echo $write['w_giken_ip'] ?>" id="w_giken_ip" readonly class="form-control input25P" placeholder="GIKEN IP">
			<input type="text" name="w_giken_live_url" value="<?php echo $write['w_giken_live_url'] ?>" id="w_giken_live_url" readonly class="form-control input25P" placeholder="Live URL">
			<input type="text" name="w_giken_serial" value="<?php echo $write['w_giken_serial'] ?>" id="w_giken_serial" required class="form-control input20P required" placeholder="GIKEN Serial">
			<input type="text" name="w_giken_verson" value="<?php echo $write['w_giken_verson'] ?>" id="w_giken_verson" required class="form-control input10P required" placeholder="GIKEN Verson">
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_face_direction">Direction</label></th>
			<td>
			<div class="selectPart">D1:<br><select name="w_face_direction_A" id="w_face_direction_A" class="form-control selectDir" placeholder="Direct">
					<option value="0" <?php if($write["w_face_direction_A"] == "0") echo 'selected'; ?> >None</option>
					<option value="1" <?php if($write["w_face_direction_A"] == "1") echo 'selected'; ?> >🡢  In  🡢</option>
					<option value="2" <?php if($write["w_face_direction_A"] == "2") echo 'selected'; ?> >🡠 Out  🡠</option>
					<option value="3" <?php if($write["w_face_direction_A"] == "3") echo 'selected'; ?> >🡠 Both 🡢</option>
				</select></div>
			<div class="selectPart">D2:<br><select name="w_face_direction_B" id="w_face_direction_B" class="form-control selectDir" placeholder="Direct">
					<option value="0" <?php if($write["w_face_direction_B"] == "0") echo 'selected'; ?> >None</option>
					<option value="1" <?php if($write["w_face_direction_B"] == "1") echo 'selected'; ?> >🡢  In  🡢</option>
					<option value="2" <?php if($write["w_face_direction_B"] == "2") echo 'selected'; ?> >🡠 Out  🡠</option>
					<option value="3" <?php if($write["w_face_direction_B"] == "3") echo 'selected'; ?> >🡠 Both 🡢</option>
				</select></div>
			<div class="selectPart">D3:<br><select name="w_face_direction_C" id="w_face_direction_C" class="form-control selectDir" placeholder="Direct">
					<option value="0" <?php if($write["w_face_direction_C"] == "0") echo 'selected'; ?> >None</option>
					<option value="1" <?php if($write["w_face_direction_C"] == "1") echo 'selected'; ?> >🡢  In  🡢</option>
					<option value="2" <?php if($write["w_face_direction_C"] == "2") echo 'selected'; ?> >🡠 Out  🡠</option>
					<option value="3" <?php if($write["w_face_direction_C"] == "3") echo 'selected'; ?> >🡠 Both 🡢</option>
				</select></div>
			<div class="selectPart">D4:<br><select name="w_face_direction_D" id="w_face_direction_D" class="form-control selectDir" placeholder="Direct">
					<option value="0" <?php if($write["w_face_direction_D"] == "0") echo 'selected'; ?> >None</option>
					<option value="1" <?php if($write["w_face_direction_D"] == "1") echo 'selected'; ?> >🡢  In  🡢</option>
					<option value="2" <?php if($write["w_face_direction_D"] == "2") echo 'selected'; ?> >🡠 Out  🡠</option>
					<option value="3" <?php if($write["w_face_direction_D"] == "3") echo 'selected'; ?> >🡠 Both 🡢</option>
				</select></div>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label>Zone/Filter/Limit</label>
			<span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Over Size</label><input type="checkbox" class="form-control" name="w_opencv_tuner" id="w_opencv_tuner" value="1" <?php echo $write[w_opencv_tuner]?'checked':'';?> ></span>
			</th>
			<td>
			<div class="inputPart">Crop Width Start:<br><input type="text" name="w_opencv_crop_x" value="<?php echo $write['w_opencv_crop_x'] ?>" id="w_opencv_crop_x" class="form-control" placeholder="w_opencv_crop_x" size="50"></div>
			<div class="inputPart">Crop Width End:<br><input type="text" name="w_opencv_crop_w" value="<?php echo $write['w_opencv_crop_w'] ?>" id="w_opencv_crop_w" class="form-control" placeholder="w_opencv_crop_w" size="50"></div>
			<div class="inputPart">Crop Height Start:<br><input type="text" name="w_opencv_crop_y" value="<?php echo $write['w_opencv_crop_y'] ?>" id="w_opencv_crop_y" class="form-control" placeholder="w_opencv_crop_y" size="50"></div>
			<div class="inputPart">Crop Height End:<br><input type="text" name="w_opencv_crop_h" value="<?php echo $write['w_opencv_crop_h'] ?>" id="w_opencv_crop_h" class="form-control" placeholder="w_opencv_crop_h" size="50"></div>
			<div class="inputPart">Noise Remove:<br><select name="w_opencv_filter" id="w_opencv_filter" class="form-control" placeholder="w_opencv_filter">
				<option value="0" <?php if($write["w_opencv_filter"] == "0") echo 'selected'; ?> >None</option>
				<option value="2" <?php if($write["w_opencv_filter"] == "2") echo 'selected'; ?> >2 X 2</option>
				<option value="3" <?php if($write["w_opencv_filter"] == "3") echo 'selected'; ?> >3 X 3</option>
				<option value="4" <?php if($write["w_opencv_filter"] == "4") echo 'selected'; ?> >4 X 4</option>
				<option value="5" <?php if($write["w_opencv_filter"] == "5") echo 'selected'; ?> >5 X 5</option>
				<option value="6" <?php if($write["w_opencv_filter"] == "6") echo 'selected'; ?> >6 X 6</option>
				<option value="7" <?php if($write["w_opencv_filter"] == "7") echo 'selected'; ?> >7 X 7</option>
				<option value="8" <?php if($write["w_opencv_filter"] == "8") echo 'selected'; ?> >8 X 8</option>
				<option value="9" <?php if($write["w_opencv_filter"] == "9") echo 'selected'; ?> >9 X 9</option>
				</select></div>
			<div class="inputPart">Threshold:<br><input type="text" name="w_opencv_threshold" value="<?php echo $write['w_opencv_threshold'] ?>" id="w_opencv_threshold" class="form-control" placeholder="w_opencv_threshold" size="50"></div>
			<div class="form-control hide">gBlur:<br><input type="text" name="w_opencv_gBlur" value="<?php echo $write['w_opencv_gBlur'] ?>" id="w_opencv_gBlur" class="form-control" placeholder="w_opencv_gBlur" size="50"></div>
			<div class="form-control hide">Canny:<br><input type="text" name="w_opencv_canny" value="<?php echo $write['w_opencv_canny'] ?>" id="w_opencv_canny" class="form-control" placeholder="w_opencv_canny" size="50"></div>
			<div class="form-control hide">Kernel:<br><input type="text" name="w_opencv_kernel" value="<?php echo $write['w_opencv_kernel'] ?>" id="w_opencv_kernel" class="form-control" placeholder="w_opencv_kernel" size="50"></div>
			<span style="display:none;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Permit</label><input type="checkbox" class="form-control" name="w_allow_permit" id="w_allow_permit" value="1" <?php echo $write[w_allow_permit]?'checked':'';?> ></span>
			<span style="display:none;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Multiple</label><input type="checkbox" class="form-control" name="w_allow_multiple" id="w_allow_multiple" value="1" <?php echo $write[w_allow_multiple]?'checked':'';?> ></span>
			<span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Image Log</label><input type="checkbox" class="form-control" name="w_opencv_iLog" id="w_opencv_iLog" value="1" <?php echo $write[w_opencv_iLog]?'checked':'';?> ></span>
			<hr>
			<div class="inputPart">Limit Width:<br><input type="text" name="w_opencv_object_w" value="<?php echo $write['w_opencv_object_w'] ?>" id="w_opencv_object_w" class="form-control" placeholder="w_opencv_object_w" size="50"></div>
			<div class="inputPart">Limit Height:<br><input type="text" name="w_opencv_object_h" value="<?php echo $write['w_opencv_object_h'] ?>" id="w_opencv_object_h" class="form-control" placeholder="w_opencv_object_h" size="50"></div>
			<div class="inputPart">Limit Pixel:<br><input type="text" name="w_opencv_object_p" value="<?php echo $write['w_opencv_object_p'] ?>" id="w_opencv_object_p" class="form-control" placeholder="w_opencv_object_p" size="50"></div>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label>Mask Primary</label></th>
			<td>
			<div class="inputPart">Width Start:<br><input type="text" name="w_opencv_mask_x" value="<?php echo $write['w_opencv_mask_x'] ?>" id="w_opencv_mask_x" class="form-control" placeholder="w_opencv_mask_x" size="50"></div>
			<div class="inputPart">Width End:<br><input type="text" name="w_opencv_mask_w" value="<?php echo $write['w_opencv_mask_w'] ?>" id="w_opencv_mask_w" class="form-control" placeholder="w_opencv_mask_w" size="50"></div>
			<div class="inputPart">Height Start:<br><input type="text" name="w_opencv_mask_y" value="<?php echo $write['w_opencv_mask_y'] ?>" id="w_opencv_mask_y" class="form-control" placeholder="w_opencv_mask_y" size="50"></div>
			<div class="inputPart">Height End:<br><input type="text" name="w_opencv_mask_h" value="<?php echo $write['w_opencv_mask_h'] ?>" id="w_opencv_mask_h" class="form-control" placeholder="w_opencv_mask_h" size="50"></div>
			<span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Use Mask</label><input type="checkbox" class="form-control" name="w_opencv_mask" id="w_opencv_mask" value="1" <?php echo $write[w_opencv_mask]?'checked':'';?> ></span>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label>Mask Secondary</label></th>
			<td>
			<div class="inputPart">Width Start:<br><input type="text" name="w_opencv_mask2_x" value="<?php echo $write['w_opencv_mask2_x'] ?>" id="w_opencv_mask2_x" class="form-control" placeholder="w_opencv_mask2_x" size="50"></div>
			<div class="inputPart">Width End:<br><input type="text" name="w_opencv_mask2_w" value="<?php echo $write['w_opencv_mask2_w'] ?>" id="w_opencv_mask2_w" class="form-control" placeholder="w_opencv_mask2_w" size="50"></div>
			<div class="inputPart">Height Start:<br><input type="text" name="w_opencv_mask2_y" value="<?php echo $write['w_opencv_mask2_y'] ?>" id="w_opencv_mask2_y" class="form-control" placeholder="w_opencv_mask2_y" size="50"></div>
			<div class="inputPart">Height End:<br><input type="text" name="w_opencv_mask2_h" value="<?php echo $write['w_opencv_mask2_h'] ?>" id="w_opencv_mask2_h" class="form-control" placeholder="w_opencv_mask2_h" size="50"></div>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label>Mask Third</label></th>
			<td>
			<div class="inputPart">Width Start:<br><input type="text" name="w_opencv_mask3_x" value="<?php echo $write['w_opencv_mask3_x'] ?>" id="w_opencv_mask3_x" class="form-control" placeholder="w_opencv_mask3_x" size="50"></div>
			<div class="inputPart">Width End:<br><input type="text" name="w_opencv_mask3_w" value="<?php echo $write['w_opencv_mask3_w'] ?>" id="w_opencv_mask3_w" class="form-control" placeholder="w_opencv_mask3_w" size="50"></div>
			<div class="inputPart">Height Start:<br><input type="text" name="w_opencv_mask3_y" value="<?php echo $write['w_opencv_mask3_y'] ?>" id="w_opencv_mask3_y" class="form-control" placeholder="w_opencv_mask3_y" size="50"></div>
			<div class="inputPart">Height End:<br><input type="text" name="w_opencv_mask3_h" value="<?php echo $write['w_opencv_mask3_h'] ?>" id="w_opencv_mask3_h" class="form-control" placeholder="w_opencv_mask3_h" size="50"></div>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label>GPIO<br>Output/Timer</label></th>
			<td>
			<input type="hidden" name="w_alert_Port1" value="18" id="w_alert_Port1" size="50">
			<input type="hidden" name="w_alert_Port2" value="23" id="w_alert_Port2" size="50">
			<input type="hidden" name="w_alert_Port3" value="24" id="w_alert_Port3" size="50">
			<input type="hidden" name="w_alert_Port4" value="25" id="w_alert_Port4" size="50">
			<div class="inputPart">Inner:(1)<br><input type="text" name="w_alert_Value1" value="<?php echo $write['w_alert_Value1'] ?>" id="w_alert_Value1" class="form-control" placeholder="Hold Time(Float)" size="50"></div>
			<div class="inputPart">Outer:(2)<br><input type="text" name="w_alert_Value2" value="<?php echo $write['w_alert_Value2'] ?>" id="w_alert_Value2" class="form-control" placeholder="Hold Time(Float)" size="50"></div>
			<div class="inputPart">Unknown:(3)<br><input type="text" name="w_alert_Value3" value="<?php echo $write['w_alert_Value3'] ?>" id="w_alert_Value3" class="form-control" placeholder="Hold Time(Float)" size="50"></div>
			<span class="inputPart" style="width: 70px; margin: unset;display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Light:(4)</label><input type="checkbox" class="form-control" name="w_alert_Value4" id="w_alert_Value4" value="1" <?php echo $write[w_alert_Value4]?'checked':'';?> ></span>
			<div class="inputPart">Base Light Lv(%):<br><input type="text" name="w_opencv_grayLv" value="<?php echo $write['w_opencv_grayLv'] ?>" id="w_opencv_grayLv" class="form-control" placeholder="w_opencv_grayLv" size="50"></div>
			<span class="inputPart" style="width: 70px; margin: unset;display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Security</label><input type="checkbox" class="form-control" name="w_security_mode" id="w_security_mode" value="1" <?php echo $write[w_security_mode]?'checked':'';?> ></span>
			<div class="inputPart">Time Over:<br><input type="text" name="w_reset_interval" value="<?php echo $write['w_reset_interval'] ?>" id="w_reset_interval" class="form-control" placeholder="Sec. Ex:3.54" size="50"></div>
			</td>
		</tr>
		<tr class='w_hide'>
			<th scope="row"><label>GPIO<br>Output/Init.<br>Input/Mode</label></th>
			<td>
			<div style="text-align:center; float: left; margin-right: 20px;">Initial Value of Relay Out:<br>
			<input class="form-control" type="text" name="w_gpio_out" value="<?php echo $write['w_gpio_out'] ?>" id="w_gpio_out">
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" value="1"><label style="color:green;font-weight:900;">1</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" value="1"><label style="color:green;font-weight:900;">2</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" value="1"><label style="color:green;font-weight:900;">3</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" value="1"><label style="color:green;font-weight:900;">4</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" disabled value="1"><label style="color:green;font-weight:900;">5</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" disabled value="1"><label style="color:green;font-weight:900;">6</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" disabled value="1"><label style="color:green;font-weight:900;">7</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioOut[]" disabled value="1"><label style="color:green;font-weight:900;">8</label></span>
			</div>
			<div style="text-align:center; float: left; margin-right: 20px;">Set S/W Mode to Normal Close(NC):<br>
			<input class="form-control" type="text" name="w_gpio_in" value="<?php echo $write['w_gpio_in'] ?>" id="w_gpio_in">
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">1</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">2</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">3</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">4</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">5</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">6</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">7</label></span>
			<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpioIn[]" value="1"><label style="color:crimson;font-weight:900;">8</label></span>
			</div>
			<div class="inputPart">Bounce(mSec):<br><input type="text" name="w_bounce_time" value="<?php echo $write['w_bounce_time'] ?>" id="w_bounce_time" class="form-control" placeholder="Not use" size="50"></div>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label for="w_remote_accessible">Accessible<br>Remote IP</label></th>
			<td>
			<input type="text" name="w_remote_accessible" value="<?php echo $write['w_remote_accessible'] ?>" id="w_remote_accessible" class="form-control input50P" placeholder="IP Ex:192.168.0.10,192.168.0.20" size="50">
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label>Group<br>Level</label></th>
			<td>
				<table>
				<tr class="ckboxGrp">
					<td class="cRadio">Level 0</td>
					<td class="cRadio">Level 1</td>
					<td class="cRadio">Level 2</td>
					<td class="cRadio">Level 3</td>
					<td class="cRadio">Level 4</td>
					<td class="cRadio">Level 5</td>
					<td class="cRadio">Level 6</td>
					<td class="cRadio">Level 7</td>
				</tr>
				<tr class="ckboxGrp">
					<input class="hide" type="text" name="w_group_level" value="<?php echo $write['w_group_level'] ?>" id="w_group_level">
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="0"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="1"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="2"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="3"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="4"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="5"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="6"></td>
					<td class="cRadio"><input class="form-control" type="radio" name="w_groupLevel[]" value="7"></td>
				</tr>
				</table>
			</td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
		<tr class='w_detail_tr'>
			<th scope="row"><label for="w_host_Addr1">HOST IP/Port<br>for IMS</label></th>
			<td>
			<input type="text" name="w_host_Addr1" value="<?php echo $write['w_host_Addr1'] ?>" id="w_host_Addr1" class="form-control input25P" placeholder="IP Ex:121.165.208.119" size="50">
			<input type="text" name="w_host_Port1" value="<?php echo $write['w_host_Port1'] ?>" id="w_host_Port1" class="form-control input25P" placeholder="Port 1 Ex:50007" size="50">
			<input type="text" name="w_host_Addr2" value="<?php echo $write['w_host_Addr2'] ?>" id="w_host_Addr2" class="form-control input25P" placeholder="IP Ex:121.165.208.119" size="50">
			<input type="text" name="w_host_Port2" value="<?php echo $write['w_host_Port2'] ?>" id="w_host_Port2" class="form-control input25P" placeholder="Port 2 Ex:50007" size="50">
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label for="w_event_Addr1">Event DB Server</label></th>
			<td>
			<input type="text" name="w_event_Addr1" value="<?php echo $write['w_event_Addr1'] ?>" id="w_event_Addr1" class="form-control input25P" placeholder="IP Ex:192.168.0.4" size="50">
			<input type="text" name="w_event_Port1" value="<?php echo $write['w_event_Port1']?$write['w_event_Port1']:'3306';?>" id="w_event_Port1" class="form-control input25P" placeholder="Port 1 Ex:3306" readonly size="50">
			<input type="text" name="w_event_Addr2" value="<?php echo $write['w_event_Addr2'] ?>" id="w_event_Addr2" class="form-control input25P" placeholder="IP Ex:192.168.0.4" size="50">
			<input type="text" name="w_event_Port2" value="<?php echo $write['w_event_Port2']?$write['w_event_Port2']:'3306';?>" id="w_event_Port2" class="form-control input25P" placeholder="Port 2 Ex:3306" readonly size="50">
			</td>
		</tr>

		<tr class="w_hide">
			<th scope="row" ><label id="licenseToggle" for="w_license">License</label></th>
			<td>
				<input type="text" name="w_license" value="<?php echo $write['w_license'] ?>" id="w_license" readonly class="form-control input50P" placeholder="License Code" size="50">
				<input type="text" name="w_keycode" value="<?php echo $write['w_keycode'] ?>" id="w_keycode" class="form-control hide" placeholder="Key Code" size="50">
				<?php include_once($board_skin_path.'/../w_include_license/application.php'); ?>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label for="w_stamp">Last Modified</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($write['w_stamp']) ?>" id="w_stamp" readonly class="form-control" placeholder="TIMESTAMP - Date and time" size="50"></td>
		</tr>
		</tbody>
		</table>

		<?php // include_once($board_skin_path.'/../w_include_acu/acuWrite.php'); // 원격릴레이 ACU ?>
		<?php include_once($board_skin_path.'/../w_include_custom/customWrite.php'); // ITS API Interface ?>
		<?php // include_once($board_skin_path.'/../w_include_custom/requestWrite.php'); ?>
		<?php // include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php'); ?>
		<?php // include_once($board_skin_path.'/../w_include_nvr/nvrWrite.php'); ?>

		<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th class='hide' scope="row"><label for="w_sensor_disable"></label></th>
			<?php // w_sensor_disable ?>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_disable" id="w_sensor_disable" value="1" <?php echo $write[w_sensor_disable]?'checked':'';?> title="Permanently Disable Sensor"></td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>

		<?php for ($i=1; $is_link && $i<=G5_LINK_COUNT; $i++) { ?>
		<tr>
			<th scope="row"><label for="wr_link<?php echo $i ?>">링크 #<?php echo $i ?></label></th>
			<td><input type="text" name="wr_link<?php echo $i ?>" value="<?php if($w=="u"){echo$write['wr_link'.$i];} ?>" id="wr_link<?php echo $i ?>" class="form-control" size="50"></td>
		</tr>
		<?php } ?>

		<?php for ($i=0; $is_file && $i<$file_count; $i++) { ?>
		<tr>
			<th scope="row">파일 #<?php echo $i+1 ?></th>
			<td>
				<input type="file" name="bf_file[]" title="파일첨부 <?php echo $i+1 ?> :  용량 <?php echo $upload_max_filesize ?> 이하만 업로드 가능" class="frm_file form-control">
				<?php if ($is_file_content) { ?>
				<input type="text" name="bf_content[]" value="<?php echo ($w == 'u') ? $file[$i]['bf_content'] : ''; ?>" title="파일 설명을 입력해주세요." class="frm_file form-control" size="50">
				<?php } ?>
				<?php if($w == 'u' && $file[$i]['file']) { ?>
				<input type="checkbox" id="bf_file_del<?php echo $i ?>" name="bf_file_del[<?php echo $i;  ?>]" value="1"> <label for="bf_file_del<?php echo $i ?>"><?php echo $file[$i]['source'].'('.$file[$i]['size'].')';  ?> 파일 삭제</label>
				<?php } ?>
			</td>
		</tr>
		<?php } ?>

		<?php if ($is_guest) { //자동등록방지  ?>
		<tr>
			<th scope="row">자동등록방지</th>
			<td>
				<?php echo $captcha_html ?>
			</td>
		</tr>
		<?php } ?>

		</tbody>
		</table>
	</div>

	<div class="btn_confirm">
		<input type="submit" value="<?php echo $SK_BO_Save[ITS_Lang]?>" id="btn_submit" accesskey="s" class="btn btn-success">
		<a href="./board.php?bo_table=<?php echo $bo_table ?>" class="btn btn-primary"><?php echo $SK_BO_Cancel[ITS_Lang]?></a>
	</div>
	</form>

	<script>
	function html_auto_br(obj)
	{
		if (obj.checked) {
			result = confirm("자동 줄바꿈을 하시겠습니까?\n\n자동 줄바꿈은 게시물 내용중 줄바뀐 곳을<br>태그로 변환하는 기능입니다.");
			if (result)
				obj.value = "html2";
			else
				obj.value = "html1";
		}
		else
			obj.value = "";
	}

	function is_check(id) {
		if(document.getElementById(id).checked == true) {
			return 1;
		} else {
			return 0;
		}
	}
	
	function fwrite_submit(f) {
		var content = 
			"\n\n_/_/_/ <?php echo $_SERVER[REMOTE_ADDR].':'.date("Y-m-d h:i:s") ?> Modified by <?php echo "'".$member['mb_name']."'" ?> (<?php echo "'".$_SERVER['REMOTE_ADDR']."'" ?>) _/_/_/\n"
			+"crop_x: "+f.w_opencv_crop_x.value+", "
			+"crop_w: "+f.w_opencv_crop_w.value+", "
			+"crop_y: "+f.w_opencv_crop_y.value+", "
			+"crop_h: "+f.w_opencv_crop_h.value+", "
			+"mask_x: "+f.w_opencv_mask_x.value+", "
			+"mask_w: "+f.w_opencv_mask_w.value+", "
			+"mask_y: "+f.w_opencv_mask_y.value+", "
			+"mask_h: "+f.w_opencv_mask_h.value+", "
			+"multiple: "+f.w_allow_multiple.value+", "
			+"image_log "+f.w_opencv_iLog.value+", "
			+"object_w: "+f.w_opencv_object_w.value+", "
			+"object_h: "+f.w_opencv_object_h.value+", "
			+"object_p: "+f.w_opencv_object_p.value+", "
			+"threshold: "+f.w_opencv_threshold.value+", "
			+"filter: "+f.w_opencv_filter.value+", "
			+"interval: "+f.w_reset_interval.value+", "
			+"tuner: "+f.w_opencv_tuner.value+", "
			+"gpio_in: "+f.w_gpio_in.value+", "
			+"gpio_out: "+f.w_gpio_out.value+", "
			+"bounce: "+f.w_bounce_time.value+", "
			+"group_level: "+f.w_group_level.value
			;
		
		$("#wr_content").append(content);	

		<?php echo $captcha_js; // 캡챠 사용시 자바스크립트에서 입력된 캡챠를 검사함  ?>

		document.getElementById("btn_submit").disabled = "disabled";

		return true;
	}
	</script>
</section>
<!-- } 게시물 작성/수정 끝 -->