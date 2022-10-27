<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

// 카메라 API 정보
$icc = json_decode(file_get_contents('/home/pi/MONITOR/netapp.json', true), true);

$title_msg =(($w == 'u')?$SK_BO_Modify[ITS_Lang]:$SK_BO_New[ITS_Lang]);
$g5['title'] = ((G5_IS_MOBILE && $board['bo_mobile_subject']) ? $board['bo_mobile_subject'] : $board['bo_subject']).' '.$title_msg;
$access_log = $_SERVER[REMOTE_ADDR].':'.date("Y-m-d h:i:s").'-'.$title_msg.'-'.$member['mb_name'].'<br>'.$write['wr_content'];

if($w == '') { // 신규 입력일떄
	include_once("$board_skin_path/sql.php"); // Local Function List
}
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name "><?php echo $g5['title'] ?><span class="sound_only"><?php echo $SK_BO_List[ITS_Lang]?></span></span>
            <hr>
            <span class="skills"><?php echo get_w_system_ip($write['w_system_ip']) ?></span>
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
		<tr class="w_hide">
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
		<tr>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Name[ITS_Lang]?>/<br>Serial</label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control input50P required" size="50" maxlength="255" placeholder="NetApp Name Ex: East Gate 3">
				<input type="text" name="w_netapp_serial" value="<?php echo $write['w_netapp_serial'] ?>" id="w_netapp_serial" readonly class="form-control input50P" placeholder="Serial No" size="50"></td>
			</td>
		</tr>
		<tr>
			<th scope="row" title="Title"><label for="wr_model">Map ID</label></th>
			<td>
				<input type="text" name="w_map_id" value="<?php echo $write['w_map_id'] ?>" id="w_map_id" class="form-control input25P" size="50" maxlength="255" placeholder="Map ID">
				<?php echo select_w_netapp_model($write['w_netapp_model'], $icc); ?>
				<input type="text" name="w_opt_int_01" value="<?php echo $write['w_opt_int_01'] ?>" id="w_opt_int_01" class="form-control input25P" placeholder="opt_int_01" size="50">
				<input type="text" name="w_opt_int_02" value="<?php echo $write['w_opt_int_02'] ?>" id="w_opt_int_02" class="form-control input25P" placeholder="opt_int_02" size="50">
			</td>
		</tr>
		<tr>
			<th scope="row" title="Title"><label for="w_netapp_desc">Description</label></th>
			<td>
				<input type="text" name="w_netapp_desc" value="<?php echo $write['w_netapp_desc'] ?>" id="w_netapp_desc" class="form-control input100P" size="50" maxlength="255" placeholder="NetApp Description">
			</td>
		</tr>
		</tbody>
		</table>
		
		<table class="table table-bordered">
		<tbody>
		<tr><?php // w_sns_ ?>
			<th scope="row"><label for="w_sns_id">Linked<br>Sensor/Box</label></th>
			<td>
				<input type="text" name="w_sns_id" value="<?php echo $write['w_sns_id'] ?>" id="w_sns_id" class="form-control input50P" placeholder="Sensor ID" size="50">
			
				<?php echo select_w_box($write['w_box_id'], 'w_box_id'); ?>

			</td>
		</tr>
		<tr><?php // w_netapp_addr w_netapp_port w_netapp_serial ?>
			<th scope="row"><label for="w_netapp_addr">NetApp IP Info</label></th>
			<td>
			<input type="text" name="w_netapp_addr" value="<?php echo $write['w_netapp_addr'] ?>" id="w_netapp_addr" class="form-control input25P" placeholder="IP Ex:121.165.208.119" size="50">
			<input type="text" name="w_netapp_port" value="<?php echo $write['w_netapp_port'] ?>" id="w_netapp_port" class="form-control" placeholder="Default:80" size="50" style="float: left;width:15%;">
			<input type="text" name="w_opt_char_01" value="<?php echo $write['w_opt_char_01'] ?>" id="w_opt_char_01" class="form-control input25P" placeholder="opt_char_01" size="50">
			<input type="text" name="w_opt_char_02" value="<?php echo $write['w_opt_char_02'] ?>" id="w_opt_char_02" class="form-control input25P" placeholder="opt_char_02" size="50">
			<input type="checkbox" name="w_opt_tiny_01" value="1" <?php echo $write['w_opt_tiny_01']?'checked':'';?> id="w_opt_tiny_01" class="form-control" style="float: left;width:10%;height:30px;">
			</td>
		</tr>
		<tr><?php // w_port_01,2,3,4 ?>
			<th scope="row"><label for="w_port_">Access Port</label></th>
			<td>
			<input type="text" name="w_port_01" value="<?php echo $write['w_port_01'] ?>" id="w_port_01" readonly class="form-control input25P" placeholder="Port 01" size="50">
			<input type="text" name="w_port_02" value="<?php echo $write['w_port_02'] ?>" id="w_port_02" readonly class="form-control input25P" placeholder="Port 02" size="50">
			<input type="text" name="w_port_03" value="<?php echo $write['w_port_03'] ?>" id="w_port_03" readonly class="form-control input25P" placeholder="Port 03" size="50">
			<input type="text" name="w_port_04" value="<?php echo $write['w_port_04'] ?>" id="w_port_04" readonly class="form-control input25P" placeholder="Port 04" size="50">
			</td>
		</tr>
		<tr><?php // w_url_01 w_url_02 ?>
			<th scope="row"><label for="w_url_0">NetApp<br>Image/Video</label></th>
			<td>
			<input type="text" name="w_url_01" value="<?php echo $write['w_url_01'] ?>" id="w_url_01" class="form-control input50P" placeholder="URL" size="50">
			<input type="text" name="w_url_02" value="<?php echo $write['w_url_02'] ?>" id="w_url_02" class="form-control input50P" placeholder="URL" size="50">
			<input type="text" name="w_url_03" value="<?php echo $write['w_url_03'] ?>" id="w_url_03" class="form-control input50P" placeholder="URL" size="50">
			<input type="text" name="w_url_04" value="<?php echo $write['w_url_04'] ?>" id="w_url_04" class="form-control input50P" placeholder="URL" size="50">
			</td>
		</tr>
		<tr><?php // w_link_0 ?>
			<th scope="row"><label for="w_link_0">Coverage</br>SensorID</label></th>
			<td>
			<input type="text" name="w_link_01" value="<?php echo $write['w_link_01'] ?>" id="w_link_01" class="form-control input50P" placeholder="Sensor ID" size="50">
			<input type="text" name="w_link_02" value="<?php echo $write['w_link_02'] ?>" id="w_link_02" class="form-control input50P" placeholder="Sensor ID" size="50">
			<input type="text" name="w_link_03" value="<?php echo $write['w_link_03'] ?>" id="w_link_03" class="form-control input50P" placeholder="Sensor ID" size="50">
			<input type="text" name="w_link_04" value="<?php echo $write['w_link_04'] ?>" id="w_link_04" class="form-control input50P" placeholder="Sensor ID" size="50">
			</td>
		</tr>

		<tr class='w_hide'><?php // w_keycode w_license?>
			<th scope="row"><label for="w_keycode">Key/License</label></th>
			<td>
			<input type="text" name="w_keycode" value="<?php echo $write['w_keycode'] ?>" id="w_keycode" class="form-control input50P" placeholder="Key Code" size="50">
			<input type="text" name="w_license" value="<?php echo $write['w_license'] ?>" id="w_license" class="form-control input50P" placeholder="License Code" size="50">
			</td>
		</tr>
		<tr class='w_hide'><?php // w_stamp ?>
			<th scope="row"><label for="w_stamp">Last Modified</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($write['w_stamp']) ?>" id="w_stamp" class="form-control" placeholder="TIMESTAMP - Date and time" size="50"></td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr>
			<th scope="row"><label for="w_netapp_disable"></label></th>
			<?php // w_netapp_disable ?>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_netapp_disable" id="w_netapp_disable" value="1" <?php echo $write[w_netapp_disable]?'checked':'';?> title="Permanently Disable NetApp"></td>
			<?php // w_alarm_disable ?>
			<td><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><input type="checkbox" class="form-control" name="w_alarm_disable" id="w_alarm_disable" value="1" <?php echo $write[w_alarm_disable]?'checked':'';?> title="Do not send valid event to host."></td>
			<?php // w_netapp_reload ?>
			<td><?php echo $SK_BO_Apply[ITS_Lang]?><input type="checkbox" class="form-control" name="w_netapp_reload" id="w_netapp_reload" value="1" <?php echo $write[w_netapp_reload]?'checked':'';?> title="Restart NetApp when catch first event after save this"></td>
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
	var icc = <?php echo json_encode($icc); ?>; 
	$("#w_netapp_model").on('change', function() { 
		// console.log($(this).val());
		if(!$(this).val()) {
			$("#w_url_01").val("");
			$("#w_url_02").val("");
			$("#w_url_01").attr("readonly", true);
			$("#w_url_02").attr("readonly", true);
			return;
		}
		if($(this).val() == "Others") {
			$("#w_url_01").attr("readonly", false);
			$("#w_url_02").attr("readonly", false);
		} else {
			$("#w_url_01").attr("readonly", true);
			$("#w_url_02").attr("readonly", true);
		}
		
		if(typeof(icc[$(this).val()].nAppImage) !== "undefined" && icc[$(this).val()].nAppImage !== null ) { 
			// console.log(icc[$(this).val()].nAppImage); // w_url_01
			$("#w_url_01").val(icc[$(this).val()].nAppImage);
		} else {
			$("#w_url_01").val("");
		}
		
		if(typeof(icc[$(this).val()].nAppVideo) !== "undefined" && icc[$(this).val()].nAppVideo !== null ) { 
			// console.log(icc[$(this).val()].nAppVideo); // w_url_02
			$("#w_url_02").val(icc[$(this).val()].nAppVideo);
		} else {
			$("#w_url_02").val("");
		}
	});	
	</script>

    <script>
    function html_auto_br(obj) {
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
			// +"device_id: "+f.w_device_id.value+", "
			+"map_id: "+f.w_map_id.value+", "
			+"netapp_serial: "+f.w_netapp_serial.value+", "
			+"netapp_addr: "+f.w_netapp_addr.value+", "
			+"netapp_model: "+f.w_netapp_model.value+", "
			+"netapp_desc: "+f.w_netapp_desc.value+", "
			+"netapp_user: "+f.w_opt_char_01.value+", "
			+"netapp_pass: "+f.w_opt_char_02.value+", "
			+"w_url_01: "+f.w_url_01.value+", "
			+"w_url_02: "+f.w_url_02.value+", "
			+"w_url_03: "+f.w_url_03.value+", "
			+"w_url_04: "+f.w_url_04.value+", "
			+"license: "+f.w_license.value+", "
			+"netapp_disable: "+is_check('w_netapp_disable')+", "
			+"alarm_disable: "+is_check('w_alarm_disable')+", "
			+"netapp_reload: "+is_check('w_netapp_reload')
			;
		
		$("#wr_content").append(content);

        <?php echo $captcha_js; // 캡챠 사용시 자바스크립트에서 입력된 캡챠를 검사함  ?>

        document.getElementById("btn_submit").disabled = "disabled";

        return true;
    }
    </script>
</section>
<!-- } 게시물 작성/수정 끝 -->