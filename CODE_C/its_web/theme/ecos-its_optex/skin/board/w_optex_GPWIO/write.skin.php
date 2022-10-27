<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

/* 라이센스 등록 */
// include_once(G5_THEME_PATH.'/skin/board/w_include_license/licenseChk.php');

$title_msg =(($w == 'u')?$SK_BO_Modify[ITS_Lang]:$SK_BO_New[ITS_Lang]);
$g5['title'] = ((G5_IS_MOBILE && $board['bo_mobile_subject']) ? $board['bo_mobile_subject'] : $board['bo_subject']).' '.$title_msg;
$access_log = $_SERVER[REMOTE_ADDR].':'.date("Y-m-d h:i:s").'-'.$title_msg.'-'.$member['mb_name'].'<br>'.$write['wr_content'];

if($w == '') { // 신규 입력일떄
	include_once("$board_skin_path/sql.php"); // Local Function List
}
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

<script>
function setValue(setVal, obj) {
	var x = document.getElementsByName(obj), iset;
	for (var iset = 0; iset < setVal.length; iset++) {
		if(setVal[iset] == "1"){
			x[iset].checked = true;
		} else {
			x[iset].checked = false;
		}
	}
}
function reSetValue(setVal) {
	var x = document.getElementsByName("w_gpio[]"), iset;
	for (var iset = 0; iset < setVal.length; iset++) {
		if(setVal[iset] == "1"){
			x[iset].disabled = false;
		} else {
			x[iset].checked = false;
			x[iset].disabled = true;
		}
	}
	var curVal = updateValue("w_gpio");
	$( "#w_gpwio_group" ).val(curVal);
}
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
	$('input:checkbox[name^="w_gpio"]').click(function () {
		var curVal = updateValue("w_gpio");
		$( "#w_gpwio_group" ).val(curVal);
		
		// 라이센스 등록에 필요한 변수(w_device_id) 규정을 위한 복사
		$( "#w_device_id" ).val(curVal);
	});
	$('input:checkbox[name^="w_cove"]').click(function () {
		var curVal = updateValue("w_cove");
		$( "#w_gpwio_cover" ).val(curVal);
		reSetValue(curVal);
	});

	// setCov 값은 최초 실행시 1로 설정 한다.
	var setVal = "<?php echo $write['w_gpwio_group'] ?>";
	setValue(setVal, "w_gpio[]");
	var setCov = "<?php if($write['w_gpwio_cover']) echo $write['w_gpwio_cover']; else echo '11111111'; ?>";
	setValue(setCov, "w_cove[]");
	$( "#w_gpwio_cover" ).val(setCov);
	reSetValue(setCov);
	// setCov
	
	$("#w_sensor_serial").change(function () {
		// // alert_Port, alert_Value, host_Addr, host_Port, host_Addr2, host_Port2		
		// $("#w_alert_Port").val($(this).find(':selected').data('aport'));
		// $("#w_alert_Value").val($(this).find(':selected').data('avalue'));
		$("#w_host_Addr1").val($(this).find(':selected').data('haddr1'));
		$("#w_host_Port1").val($(this).find(':selected').data('hport1'));
		$("#w_host_Addr2").val($(this).find(':selected').data('haddr2'));
		$("#w_host_Port2").val($(this).find(':selected').data('hport2'));
	});
	
	
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
    <input type="hidden" name="w_device_id" id="w_device_id" value="<?php echo $write['w_gpwio_group'] ?>">
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
				<?php if($write_min || $write_max) { ?>
				<!-- 최소/최대 글자 수 사용 시 -->
				<p id="char_count_desc">이 게시판은 최소 <strong><?php echo $write_min; ?></strong>글자 이상, 최대 <strong><?php echo $write_max; ?></strong>글자 이하까지 글을 쓰실 수 있습니다.</p>
				<?php } ?>
				<?php echo $editor_html; // 에디터 사용시는 에디터로, 아니면 textarea 로 노출 ?>
				<?php if($write_min || $write_max) { ?>
				<!-- 최소/최대 글자 수 사용 시 -->
				<div id="char_count_wrap"><span id="char_count"></span>글자</div>
				<?php } ?>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Name[ITS_Lang]?>/Serial</label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control input50P required" placeholder="GPWIO Name Ex: East Gate 3">
				<input type="text" name="w_gpwio_serial" value="<?php echo $write['w_gpwio_serial'] ?>" id="w_gpwio_serial" readonly class="form-control input50P" placeholder="Serial No" size="50"></td>
			</td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="w_gpwio_desc">Desc./Links</label></th>
			<td>
				<input type="text" name="w_gpwio_desc" value="<?php echo $write['w_gpwio_desc'] ?>" id="w_gpwio_desc" class="form-control input50P" placeholder="GPWIO Description">
				<?php echo select_w_sensor($write['w_sensor_serial']); ?>
			</td>
		</tr> 
		<tr class='w_default_tr'>
			<th scope="row"><label for="w_gpwio_group">GPWIO Action/Group</label></th>
			<td>
				<?php echo select_w_gpwio_status($write['w_gpwio_status']); ?>
				<div class="input25P" style="text-align:center"><input class="form-control" type="text" ></div>
				<div class="input25P" style="text-align:center">
					<input class="form-control hide" type="text" name="w_gpwio_cover" value="<?php echo $write['w_gpwio_cover'] ?>" id="w_gpwio_cover">
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">1</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">2</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">3</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">4</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">5</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">6</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">7</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_cove[]" value="1"><label style="color:crimson;font-weight:900;">8</label></span>
				</div>
				<div class="input25P" style="text-align:center">
					<input class="form-control hide" type="text" name="w_gpwio_group" value="<?php echo $write['w_gpwio_group'] ?>" id="w_gpwio_group">
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">1</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">2</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">3</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">4</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">5</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">6</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">7</label></span>
					<span style="display:inline-grid;"><input type="checkbox" class="form-control gGpio" name="w_gpio[]" value="1"><label style="color:green;font-weight:900;">8</label></span>
				</div>
			</td>
		</tr>
		<tr class='w_detail_tr'>
			<th scope="row"><label for="w_alert_Port">Relay Out/Time</label></th>
			<td>
				<?php echo select_w_GPIO_alert($write['w_alert_Port']); ?>
				<input type="text" name="w_alert_Value" value="<?php echo $write['w_alert_Value'] ?>" id="w_alert_Value" class="form-control input25P" placeholder="Hold Time(Float)" size="50">
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

		<?php // include_once($board_skin_path.'/../w_include_audio/write_ims_sound.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_custom/customWrite.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_custom/requestWrite.php'); ?>

		<table class="table table-bordered w_hide">
		<tbody>
		<tr class="w_hide">
			<th scope="row"><label for="w_license"><?php echo $SK_BO_License[ITS_Lang]?></label></th>
			<td>
				<input type="text" name="w_license" value="<?php echo $write['w_license'] ?>" id="w_license" class="form-control input50P" placeholder="License Code" size="50">
				<input type="text" name="w_keycode" value="<?php echo $write['w_keycode'] ?>" id="w_keycode" class="hide form-control input50P" placeholder="Key Code" size="50">
				<?php include_once(G5_THEME_PATH.'/skin/board/w_include_license/application.php'); ?>
			</td>
		</tr>

		<tr class='w_hide'>
			<th scope="row"><label for="w_stamp">Last Modified</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($write['w_stamp']) ?>" id="w_stamp" readonly class="form-control" placeholder="TIMESTAMP - Date and time" size="50"></td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th class='hide' scope="row"><label for="w_gpwio_disable"></label></th>
			<?php // w_gpwio_disable ?>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_gpwio_disable" id="w_gpwio_disable" value="1" <?php echo $write[w_gpwio_disable]?'checked':'';?> title="Permanently Disable GPWIO"></td>
			<?php // w_alarm_disable ?>
			<td><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><input type="checkbox" class="form-control" name="w_alarm_disable" id="w_alarm_disable" value="1" <?php echo $write[w_alarm_disable]?'checked':'';?> title="Do not send valid event to host."></td>
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
		var currentdate = new Date(); 
		var datetime = "Last Sync: " 
			+ currentdate.getFullYear() + "-"
			+ (currentdate.getMonth()+1)  + "-" 
			+ currentdate.getDate() + " @ "  
			+ currentdate.getHours() + ":"  
			+ currentdate.getMinutes() + ":" 
			+ currentdate.getSeconds();
		var content = 
			"\n\n_/_/_/ "+datetime+" Modified by "+<?php echo "'".$member['mb_name']."'" ?>+" ("+<?php echo "'".$_SERVER['REMOTE_ADDR']."'" ?>+") _/_/_/\n"
			+"subject: "+f.wr_subject.value+", "
			+"gpwio_serial: "+f.w_gpwio_serial.value+", "
			+"gpwio_status: "+f.w_gpwio_status.value+", "
			+"gpwio_cover: "+f.w_gpwio_cover.value+", "
			+"gpwio_group: "+f.w_gpwio_group.value+", "
			+"gpwio_desc: "+f.w_gpwio_desc.value+", "
			+"alert_Port: "+f.w_alert_Port.value+", "
			+"alert_Value: "+f.w_alert_Value.value+", "
			+"host_Addr1: "+f.w_host_Addr1.value+", "
			+"host_Port1: "+f.w_host_Port1.value+", "
			+"host_Addr2: "+f.w_host_Addr2.value+", "
			+"host_Port2: "+f.w_host_Port2.value+", "
			+"keycode: "+f.w_keycode.value+", "
			+"license: "+f.w_license.value+", "
			+"gpwio_disable: "+is_check('w_gpwio_disable')+", "
			+"alarm_disable: "+is_check('w_alarm_disable')+", "
			;
		
		$("#wr_content").append(content);

        <?php echo $captcha_js; // 캡챠 사용시 자바스크립트에서 입력된 캡챠를 검사함  ?>

        document.getElementById("btn_submit").disabled = "disabled";

        return true;
    }
    </script>
</section>
<!-- } 게시물 작성/수정 끝 -->