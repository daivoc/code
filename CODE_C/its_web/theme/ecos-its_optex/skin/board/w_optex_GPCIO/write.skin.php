<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

/* 라이센스 등록 */
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

<script>
$(document).ready(function(){

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
    <input type="hidden" name="w_device_id" id="w_device_id" value="<?php echo $write['w_gpcio_detect_L'] ?>">
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
			<td><input type="text" name="w_id" value="<?php echo $write['w_id'] ?>" id="w_id" class="form-control input50P" placeholder="Sensor ID" size="50"><input type="text" name="w_cpu_id" value="<?php echo get_w_cpu_id($write['w_cpu_id']); ?>" id="w_cpu_id" class="form-control input50P" placeholder="System CPU ID" size="50"></td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Name[ITS_Lang]?><br>Desc./Serial</label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control input50P required" placeholder="GPCIO Name Ex: East Gate 3">
				<input type="text" name="w_gpcio_desc" value="<?php echo $write['w_gpcio_desc'] ?>" id="w_gpcio_desc" class="form-control input25P" placeholder="GPCIO Description">
				<input type="text" name="w_sensor_serial" value="<?php echo $write['w_sensor_serial'] ?>" id="w_sensor_serial" readonly class="form-control input25P" placeholder="Serial No" size="50"></td>
			</td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="w_gpcio_desc">Port Set/<br>Speed</label></th>
			<td>
				<div class="input50P" style="text-align:center">
					<span style='display:inline-grid;'><input type='checkbox' class='form-control gGpio' name='w_gpcio_trigger_L' id='w_gpcio_trigger_L' value='1' <?php if($write['w_gpcio_trigger_L']) echo 'checked'; ?> disabled ><label style='color:crimson;font-weight:900;'>Dn</label></span>
					<?php echo select_w_GPIO_sensor($write['w_gpcio_detect_L'], 'w_gpcio_detect_L', $relay_inputL) ?>
					<select name="w_gpcio_direction" id="w_gpcio_direction" class="form-control" style="width: 110px;display: inline;vertical-align: super;" placeholder="Direct">
						<option value="1" <?php if($write["w_gpcio_direction"] == 1) echo 'selected'; ?> >🡢 L:R 🡢</option>
						<option value="9" <?php if($write["w_gpcio_direction"] == 9) echo 'selected'; ?> >🡠 Both 🡢</option>
						<option value="2" <?php if($write["w_gpcio_direction"] == 2) echo 'selected'; ?> >🡠 L:R 🡠</option>
					</select>
					<?php echo select_w_GPIO_sensor($write['w_gpcio_detect_R'], 'w_gpcio_detect_R', $relay_inputR) ?>
					<span style='display:inline-grid;'><input type='checkbox' class='form-control gGpio' name='w_gpcio_trigger_R' id='w_gpcio_trigger_R' value='1' <?php if($write['w_gpcio_trigger_R']) echo 'checked'; ?> disabled ><label style='color:crimson;font-weight:900;'>Dn</label></span>
				</div>

				<div class="input50P" style="text-align:center">
					<input type="text" name="w_distance" value="<?php echo $write['w_distance'] ?>" id="w_distance" class="form-control" style="width: 110px;display:inline; text-align: right;" placeholder="Distance Cm" > cm, 
					<input type="text" name="w_speed_L" value="<?php echo $write['w_speed_L'] ?>" id="w_speed_L" class="form-control" style="width: 110px;display:inline; text-align: right;" placeholder="Min. Km/h" > 🡢 Speed 🡠  
					<input type="text" name="w_speed_H" value="<?php echo $write['w_speed_H'] ?>" id="w_speed_H" class="form-control" style="width: 110px;display:inline; text-align: right;" placeholder="Max. Km/h" > Km/h
				</div>
			</td>
		</tr>
		<tr class='w_detail_tr'>
			<th scope="row"><label for="w_countIn">Count In<br>Out</label></th>
			<td>
				<div class="input25P inputCntGrp">
					<div class="dirName">D1:<input type="text" name="w_capacity_A" value="<?php echo $write['w_capacity_A'] ?>" id="w_capacity_A" class="form-control inputCap" placeholder="D1" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_AX" value="<?php echo $write['w_direction_AX'] ?>" id="w_direction_AX" class="form-control input50P inputCnt" placeholder="Count1 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_AX" id="w_internal_AX" value="1" <?php echo $write[w_internal_AX]?'checked':'';?> >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_AX" id="w_external_AX" value="1" <?php echo $write[w_external_AX]?'checked':'';?> >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XA" value="<?php echo $write['w_direction_XA'] ?>" id="w_direction_XA" class="form-control input50P inputCnt" placeholder="Count1 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XA" id="w_internal_XA" value="1" <?php echo $write[w_internal_XA]?'checked':'';?> >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XA" id="w_external_XA" value="1" <?php echo $write[w_external_XA]?'checked':'';?> >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
				<div class="input25P inputCntGrp hide">
					<div class="dirName">D2:<input type="text" name="w_capacity_B" value="<?php echo $write['w_capacity_B'] ?>" id="w_capacity_B" class="form-control inputCap" placeholder="D2" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_BX" value="<?php echo $write['w_direction_BX'] ?>" id="w_direction_BX" class="form-control input50P inputCnt" placeholder="Count2 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_BX" id="w_internal_BX" value="1" <?php echo $write[w_internal_BX]?'checked':'';?> >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_BX" id="w_external_BX" value="1" <?php echo $write[w_external_BX]?'checked':'';?> >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XB" value="<?php echo $write['w_direction_XB'] ?>" id="w_direction_XB" class="form-control input50P inputCnt" placeholder="Count2 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XB" id="w_internal_XB" value="1" <?php echo $write[w_internal_XB]?'checked':'';?> >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XB" id="w_external_XB" value="1" <?php echo $write[w_external_XB]?'checked':'';?> >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
				<div class="input25P inputCntGrp hide">
					<div class="dirName">D3:<input type="text" name="w_capacity_C" value="<?php echo $write['w_capacity_C'] ?>" id="w_capacity_C" class="form-control inputCap" placeholder="D3" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_CX" value="<?php echo $write['w_direction_CX'] ?>" id="w_direction_CX" class="form-control input50P inputCnt" placeholder="Count3 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_CX" id="w_internal_CX" value="1" <?php echo $write[w_internal_CX]?'checked':'';?> >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_CX" id="w_external_CX" value="1" <?php echo $write[w_external_CX]?'checked':'';?> >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XC" value="<?php echo $write['w_direction_XC'] ?>" id="w_direction_XC" class="form-control input50P inputCnt" placeholder="Count3 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XC" id="w_internal_XC" value="1" <?php echo $write[w_internal_XC]?'checked':'';?> >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XC" id="w_external_XC" value="1" <?php echo $write[w_external_XC]?'checked':'';?> >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
				<div class="input25P inputCntGrp hide">
					<div class="dirName">D4:<input type="text" name="w_capacity_D" value="<?php echo $write['w_capacity_D'] ?>" id="w_capacity_D" class="form-control inputCap" placeholder="D4" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_DX" value="<?php echo $write['w_direction_DX'] ?>" id="w_direction_DX" class="form-control input50P inputCnt" placeholder="Count4 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_DX" id="w_internal_DX" value="1" <?php echo $write[w_internal_DX]?'checked':'';?> >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_DX" id="w_external_DX" value="1" <?php echo $write[w_external_DX]?'checked':'';?> >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XD" value="<?php echo $write['w_direction_XD'] ?>" id="w_direction_XD" class="form-control input50P inputCnt" placeholder="Count4 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XD" id="w_internal_XD" value="1" <?php echo $write[w_internal_XD]?'checked':'';?> >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XD" id="w_external_XD" value="1" <?php echo $write[w_external_XD]?'checked':'';?> >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
			</td>
		</tr>

		<tr class='w_detail_tr'>
			<th scope="row"><label for="w_alert_Port">Relay Out/Time</label></th>
			<td>
				<?php echo select_w_GPIO_alert($write['w_alert_Port']); ?>
				<input type="text" name="w_alert_Value" value="<?php echo $write['w_alert_Value'] ?>" id="w_alert_Value" class="form-control input25P" placeholder="Hold Time(Float)" size="50">
				<span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Security</label><input type="checkbox" class="form-control" name="w_security_mode" id="w_security_mode" value="1" <?php echo $write[w_security_mode]?'checked':'';?> ></span>
			</td>
		</tr>
		<tr class='w_detail_tr'>
			<th scope="row"><label for="w_host_Addr1">HOST IP/Port<br>for IMS</label></th>
			<td>
			<input type="text" name="w_host_Addr1" value="<?php echo $write['w_host_Addr1'] ?>" id="w_host_Addr1" class="form-control input25P" placeholder="IP Ex:121.165.208.119" size="50">
			<input type="text" name="w_host_Port1" value="<?php echo $write['w_host_Port1'] ?>" id="w_host_Port1" class="form-control input25P" placeholder="Port 1 Ex:50007" size="50">
			<input type="text" name="w_host_Addr2" value="<?php echo $write['w_host_Addr2'] ?>" id="w_host_Addr2" class="form-control input25P" placeholder="IP Ex:121.165.208.119" size="50">
			<input type="text" name="w_host_Port2" value="<?php echo $write['w_host_Port2'] ?>" id="w_host_Port2" class="form-control input25P" placeholder="Port 2 Ex:50007" size="50">
			</td>
		</tr>
		</tbody>
		</table>

		<?php include_once($board_skin_path.'/../w_include_custom/customWrite.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_custom/requestWrite.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php'); ?>

		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_license"><?php echo $SK_BO_License[ITS_Lang]?></label></th>
			<td>
				<input type="text" name="w_license" value="<?php echo $write['w_license'] ?>" id="w_license" readonly class="form-control input50P" placeholder="License Code" size="50">
				<input type="text" name="w_keycode" value="<?php echo $write['w_keycode'] ?>" id="w_keycode" class="form-control input50P" placeholder="Key Code" size="50">
				<?php include_once($board_skin_path.'/../w_include_license/application.php'); ?>
			</td>
		</tr>

		<tr class='w_detail_tr'>
			<th scope="row"><label for="w_stamp">Last Modified</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($write['w_stamp']) ?>" id="w_stamp" readonly class="form-control" placeholder="TIMESTAMP - Date and time" size="50"></td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th class='hide' scope="row"><label for="w_gpcio_disable"></label></th>
			<?php // w_gpcio_disable ?>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_gpcio_disable" id="w_gpcio_disable" value="1" <?php echo $write[w_gpcio_disable]?'checked':'';?> title="Permanently Disable GPCIO"></td>
			<?php // w_alarm_disable ?>
			<!-- td><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><input type="checkbox" class="form-control" name="w_alarm_disable" id="w_alarm_disable" value="1" <?php echo $write[w_alarm_disable]?'checked':'';?> title="Do not send valid event to host."></td -->
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
		
        <?php echo $captcha_js; // 캡챠 사용시 자바스크립트에서 입력된 캡챠를 검사함  ?>

        document.getElementById("btn_submit").disabled = "disabled";

        return true;
    }
    </script>
</section>
<!-- } 게시물 작성/수정 끝 -->