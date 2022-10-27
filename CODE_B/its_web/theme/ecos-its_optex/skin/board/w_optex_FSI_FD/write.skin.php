<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

$share = json_decode(file_get_contents('/home/pi/common/config.json', true), true);
$local = json_decode(file_get_contents('/home/pi/FSI/config.json', true), true);
$cfg = json_decode(file_get_contents("$board_skin_path/config.json", true), true); 

$cfg["model"] = $local["model"];

////////////////////////////////////////
// 보드 형태에 따라 IO값이 다르며
// 다양한 릴리에와 센서 조합이 가능 하다.
////////////////////////////////////////
// 기존값을 불러온다
// 설정보드 타입 its 또는 acu
$sql_ioB = " SELECT `mb_4` FROM `g5_member` WHERE mb_id = 'its'";
$row_ioB = sql_fetch($sql_ioB);
$ioB = $row_ioB['mb_4']; // std or acu
// if($ioB == "") $ioB = "std"; // 기본값은 standard
if($ioB != "acu") $ioB = "std"; // 기본값은 standard
$cfg["DEVICE_alert"] = [];
$cfg["DEVICE_all"] = [];
foreach($share["ioBoard"][$ioB]["setIO"] as $io => $value) {
	if($value == 'true') {
		$cfg['DEVICE_all'][$share["ioBoard"][$ioB]["gpio"][$io]] = str_replace ("io", "Relay_", $io);
		$cfg['DEVICE_alert'][$share["ioBoard"][$ioB]["gpio"][$io]] = str_replace ("io", "Relay_", $io);
	} else {
		$cfg['DEVICE_all'][$share["ioBoard"][$ioB]["gpio"][$io]] = str_replace ("io", "Sensor_", $io);
	}
}

// view.skin.php 에서 사용할수 있도록 환경값을 저장 한다.
$fp = fopen("$board_skin_path/config.json", "w") or die("Error opening for write $board_skin_path/config.json");
fwrite($fp, json_encode($cfg, JSON_PRETTY_PRINT)); // ,JSON_UNESCAPED_UNICODE
fclose($fp);
	
include_once("$board_skin_path/its_module.php"); // Local Function List

/* 라이센스 등록 */
// include_once(G5_THEME_PATH.'/skin/board/w_include_license/licenseChk.php');

$title_msg =(($w == 'u')?$SK_BO_Modify[ITS_Lang]:$SK_BO_New[ITS_Lang]);
$g5['title'] = ((G5_IS_MOBILE && $board['bo_mobile_subject']) ? $board['bo_mobile_subject'] : $board['bo_subject']).' '.$title_msg;
$access_log = $_SERVER[REMOTE_ADDR].':'.date("Y-m-d h:i:s").'-'.$title_msg.'-'.$member['mb_name'].'<br>'.$write['wr_content'];

if($w == '') {
	include_once("$board_skin_path/sql.php"); // Local Function List
	$write['w_sensor_disable'] = 0; // 사용중지 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_stop'] = 0; // 일시정지 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_reload'] = 0; 
	$write['w_alarm_disable'] = 0; // 알람정지 tinyint(1) NOT NULL DEFAULT '0',
	
	$write['w_parent_id'] = $parent_id;
	$write['w_zone_id'] = $zone_id;
	$write['w_zone_name'] = $zone_name;

}

?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/css/jquery-ui.css">
<script src="<?php echo $board_skin_url?>/js/jquery-ui.js"></script>

<style>
	hr { border: none;margin-top: 4px;margin-bottom: 4px;clear: both; }
	.table { margin-bottom: 2px; }
	.table th { width:120px; font-size: 10pt; text-align: center; color: gray; }
	.wr_content_tr { display:none; }
	.w_hide { display:none; }
	.w_detail_tr { display:none; background-color: #f0f4ff; font-size: 8pt; color: gray; zoom:0.8; }
	.w_detail_tr th { background-color:gray; color: white; }

	.w_default_tr { display:none; background-color: #f0f0f0; font-size: 8pt; color: gray; }
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
	.input80px { width: 80px; display: initial; float: left; margin:0; }
	.weekday {width: 28px; float: left; text-align: center;}
</style>

<script type="text/javascript">
$(document).ready(function(){
	$('#wr_content').prop('readonly', true);
	$('#w_system_ip').prop('readonly', true);
	$('#w_device_serial').prop('readonly', true);
	$('#w_stamp').prop('readonly', true);
	
	$('#btn_detail').on('click', function(event) {        
		$('.w_detail_tr').toggle('show');
	});
	$('#btn_default').on('click', function(event) {        
		$('.w_default_tr').toggle('show');
	});

	$(function() {
		$("#slider-range_count").slider({ // 참조 https://jqueryui.com/slider/#rangemax
			range: "max",
			min: 1,
			max: 10,
			value: $("#w_snapshot_qty").val(),
			slide: function(event, ui) {
				$("#w_snapshot_qty").val(ui.value);
				$("#w_opt22Disp").text(ui.value);
			}
		});
		$("#w_opt22Disp").text($("#w_snapshot_qty").val());
	});

	$('#licenseToggle').click(function(){ // 활성 비횔성 토글
		console.log(this.id);
		$('#w_license').prop('readonly', function(i, v) { return !v; });
	});

});
</script>

<section class="success" id="header" style="padding:0;">
	<div class="container">
		<div class="intro-text">
			<span class="name "><?php echo $g5['title'] ?><span class="sound_only"><?php echo $SK_BO_List[ITS_Lang]?></span></span>
			<hr>
			<span class="skills"><?php echo get_w_system_ip($write['w_system_ip']) ?></span>
			<span class="skills"><?php echo $pID . "-" . $pName; ?></span>
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
		<input type="button" value="<?php echo $SK_BO_Basic[ITS_Lang]?>" id="btn_default" class="hide btn btn-warning">
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
		<tr class="wr_content_tr">
			<th scope="row"><label for="wr_content"><?php echo $SK_BO_History[ITS_Lang]?></label></th>
			<td class="wr_content">
				<textarea id="wr_content" name="wr_content" class="" maxlength="65536" style="width:100%;height:300px"><?php echo $access_log ?></textarea>
				<?php /* if($write_min || $write_max) { ?>
				<!-- 최소/최대 글자 수 사용 시 -->
				<p id="char_count_desc">이 게시판은 최소 <strong><?php echo $write_min; ?></strong>글자 이상, 최대 <strong><?php echo $write_max; ?></strong>글자 이하까지 글을 쓰실 수 있습니다.</p>
				<?php } ?>
				<?php echo $editor_html; // 에디터 사용시는 에디터로, 아니면 textarea 로 노출 ?>
				<?php if($write_min || $write_max) { ?>
				<!-- 최소/최대 글자 수 사용 시 -->
				<div id="char_count_wrap"><span id="char_count"></span>글자</div>
				<?php } */ ?>
			</td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
		<tr>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Name[ITS_Lang]?>/<?php echo $SK_BO_Device_Name[ITS_Lang]?></label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control input25P required" size="50" maxlength="255" placeholder="Sensor Name Ex: East Gate 3">
				<input type="text" name="w_device_name" value="<?php echo $write['w_device_name'] ?>" id="w_device_name" class="form-control input25P" placeholder="IP Ex:E110545" size="50">
				<input type="text" name="w_device_serial" value="<?php echo $write['w_device_serial'] ?>" id="w_device_serial" readonly class="form-control input50P" placeholder="Sensor Serial" size="50">
			</td>
		</tr>
		<tr>
			<th scope="row" title="ID"><label for="w_id">Parent ID / Zone</label></th>
			<td>
			<input type="hidden" name="w_id" value="<?php echo $write['w_id'] ?>" id="w_id" class="form-control input25P" readonly placeholder="Sensor ID" size="50">
			<input type="text" name="w_parent_id" value="<?php echo $write['w_parent_id'] ?>" id="w_parent_id" class="form-control input25P" readonly placeholder="Parent ID" size="50">
			<input type="text" name="w_zone_id" value="<?php echo $write['w_zone_id'] ?>" id="w_zone_id" class="form-control input25P" readonly placeholder="Zone Name" size="50">
			<input type="text" name="w_zone_name" value="<?php echo $write['w_zone_name'] ?>" id="w_zone_name" class="form-control input25P" placeholder="Zone Name" size="50">
			<input type="text" name="w_system_ip" value="<?php echo get_w_system_ip($write['w_system_ip']) ?>" id="w_system_ip" class="form-control input25P" placeholder="System IP Address" size="50">
			</td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_ims_address_P">IMS</label></th>
			<td><input type="text" name="w_ims_address_P" value="<?php echo $write['w_ims_address_P'] ?>" id="w_ims_address_P" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_ims_port_P" value="<?php echo $write['w_ims_port_P'] ?>" id="w_ims_port_P" class="form-control input50P" placeholder="Port Ex:50007" size="50">
			<hr>
			<input type="text" name="w_ims_address_S" value="<?php echo $write['w_ims_address_S'] ?>" id="w_ims_address_S" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_ims_port_S" value="<?php echo $write['w_ims_port_S'] ?>" id="w_ims_port_S" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		</tbody>
		</table>
		
		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_snapshot_url"><?php echo $SK_BO_Snapshot[ITS_Lang]?></label></th>
			<td>
			<input type="text" name="w_snapshot_url" value="<?php echo $write['w_snapshot_url'] ?>" id="w_snapshot_url" class="form-control input50P" placeholder="URL Ex:http://121.165.208.119:8080/" size="50">
			<span class="input25P" style="padding: 0 15px;">
				Shut Max: <span id="w_opt22Disp"></span>
				<input type="text" name="w_snapshot_qty" value="<?php echo $write['w_snapshot_qty'] ?>" id="w_snapshot_qty" readonly class="w_hide">
				<div id="slider-range_count"></div>
			</span>
			<span class="input25P" style="display:inline-block;text-align:center;height:20px;font-size:10pt;font-weight:unset;" >
				<input type="checkbox" class="form-control" style="float:none;height:20px;" name="w_snapshot_enc" id="w_snapshot_enc" value="1" <?php echo $write[w_snapshot_enc]?'checked':'';?> title="w_snapshot_enc"><label><?php echo $SK_BO_Encryption[ITS_Lang]?></label>
			</span>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_streaming_url"><?php echo $SK_BO_Streaming[ITS_Lang]?></label></th>
			<td><input type="text" name="w_streaming_url" value="<?php echo $write['w_streaming_url'] ?>" id="w_streaming_url" class="form-control input75P" placeholder="URL Ex:http://121.165.208.119:8080/" size="50">
			<span class="input25P" style="display:inline-block;text-align:center;height:20px;font-size:10pt;font-weight:unset;" ><input type="checkbox" class="form-control" style="float:none;height:20px;" name="w_streaming_enc" id="w_streaming_enc" value="1" <?php echo $write[w_streaming_enc]?'checked':'';?> title="w_streaming_enc"><label><?php echo $SK_BO_Encryption[ITS_Lang]?></label></span></td>
		</tr>
		</tbody>
		</table>
		
		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alert_port"><?php echo $SK_BO_Alert[ITS_Lang]?></label></th>
			<td>
				<?php echo select_w_GPIO_alert($write['w_alert_port']); ?>
				<input type="text" name="w_alert_value" value="<?php echo $write['w_alert_value'] ?>" id="w_alert_value" class="form-control input50P" placeholder="Due Time" size="50">
			</td>
		</tr>
		</tbody>
		</table>

		<?php include_once($board_skin_path.'/../w_include_custom/customWrite.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_custom/requestWrite.php'); ?>
		
		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alert_port">Replace Rule<br>for<br>Socket IO<br>Http Request</label></th>
			<td>
				<pre class="input100P">
	Key : __zone__, __value__, __type__, __name__, __model__, __serial__, __ip__, __time__
		XML:	&lt;Msg&gt;&lt;Type&gt;__type__&lt;/Type&gt;&lt;Group&gt;__value__&lt;/Group&gt;&lt;ID&gt;__zone__&lt;/ID&gt;&lt;Time&gt;__time__&lt;/Time&gt;&lt;/Msg&gt;
		JSON:	[{ "gpio": { "status": "__type__", "id": "__value__", "hold": "1.0", "ipaddress": "__ip__"} }]</pre>
			</td>
		</tr>
		</tbody>
		</table>
		<?php include_once($board_skin_path.'/../w_include_acu/acuWrite.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_audio/write_alarm_sound.php'); ?>
		
		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label id="licenseToggle" for="w_license"><?php echo $SK_BO_License[ITS_Lang]?></label></th>
			<td>
				<input type="text" name="w_license" value="<?php echo $write['w_license'] ?>" id="w_license" readonly class="form-control input50P" placeholder="License Code" size="50">
				<input type="text" name="w_keycode" value="<?php echo $write['w_keycode'] ?>" id="w_keycode" class="hide form-control input50P" placeholder="Key Code" size="50">
				<?php include_once(G5_THEME_PATH.'/skin/board/w_include_license/application.php'); ?>
			</td>
		</tr>

		<tr class="w_hide">
			<th scope="row"><label for="w_stamp"><?php echo $SK_BO_Created[ITS_Lang]?></label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($write['w_stamp']) ?>" id="w_stamp" class="form-control" placeholder="TIMESTAMP - Date and time" size="50"></td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr>
			<th class="w_hide" scope="row"><label for="w_sensor_disable"></label></th>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_disable" id="w_sensor_disable" value="1" <?php echo $write[w_sensor_disable]?'checked':'';?> title="Permanently Disable Sensor"></td>
			<td class="w_hide"><?php echo $SK_BO_Pause[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_stop" id="w_sensor_stop" value="1" <?php echo $write[w_sensor_stop]?'checked':'';?> title="Temporary Disable Sensor(keep log)"></td>
			<td class="w_hide"><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><input type="checkbox" class="form-control" name="w_alarm_disable" id="w_alarm_disable" value="1" <?php echo $write[w_alarm_disable]?'checked':'';?> title="Do not send valid event to host."></td>
			<td class="w_hide"><?php echo $SK_BO_Apply[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_reload" id="w_sensor_reload" value="1" <?php echo $write[w_sensor_reload]?'checked':'';?> title="Restart Sensor when catch first event after save this"></td>
			<td class="w_default_tr"><?php echo $SK_BO_Keep_Cycle[ITS_Lang]?><input type="checkbox" class="form-control" name="w_event_keepHole" id="w_event_keepHole" value="1" <?php echo $write[w_event_keepHole]?'checked':'';?> title="Keep event hold cycle."></td>
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
	</script>
</section>
<!-- } 게시물 작성/수정 끝 -->