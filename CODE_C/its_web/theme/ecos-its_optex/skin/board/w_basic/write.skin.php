<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/its_module.php"); // Local Function List

// add_stylesheet('css 구문', 출력순서); 숫자가 작을 수록 먼저 출력됨
add_stylesheet('<link rel="stylesheet" href="'.$board_skin_url.'/style.css">', 0);

$title_msg =(($w == 'u')?'수정':'신규');
$g5['title'] = ((G5_IS_MOBILE && $board['bo_mobile_subject']) ? $board['bo_mobile_subject'] : $board['bo_subject']).' '.$title_msg;
$access_log = $write['wr_content'].'<<<--'.date("Y-m-d h:i:s").' '.$title_msg.' Updated By '.$member['mb_name'].'-->>>\\r';
?>

<style>
.wr_content_tr { display:none; }
.w_detail_tr { display:none; background-color: #F5F8FF; }
.w_api_tr { display:none; background-color: aliceblue; }
.w_sensor_ignore_span { display: inline-block; border: 1px solid #dce4ec; border-radius: 4px; padding: 4px; margin: 2px; }
.btn_option_01 { text-align: right; }
</style>
<script type="text/javascript">
$(document).ready(function(){
	$("#wr_content").val('<?php echo $access_log; ?>');
	$('#wr_content').prop('readonly', true);
	$('#w_cpu_id').prop('readonly', true);
	$('#w_system_ip').prop('readonly', true);
	$('#w_model_id').prop('readonly', true);
	$('#w_sensor_serial').prop('readonly', true);
	$('#w_sensor_stop').prop('readonly', true);
	$('#w_stamp').prop('readonly', true);
	
	$('#btn_detail').on('click', function(event) {        
		 $('.w_detail_tr').toggle('show');
	});
	$('#btn_API').on('click', function(event) {        
		 $('.w_api_tr').toggle('show');
	});
});
</script>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name "><?php echo $g5['title'] ?><span class="sound_only"> 목록</span></span>
            <hr>
            <span class="skills"></span>
        </div>
    </div>
</section>

<section id="bo_w" class="container">
    <h2 id="container_title"></h2>
    <!-- 게시물 작성/수정 시작 { -->
    <form name="fwrite" id="fwrite" action="<?php echo $action_url ?>" onsubmit="return fwrite_submit(this);" method="post" enctype="multipart/form-data" autocomplete="off" style="width:<?php echo $width; ?>">
    <input type="hidden" name="uid" value="<?php echo get_uniqid(); ?>">
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
        <input type="button" value="고급설정" id="btn_detail" class="btn btn-info">
        <input type="button" value="API설정" id="btn_API" class="btn btn-warning">
    </div>
	
    <div class="tbl_wrap table-responsive">
		<table class="table table-bordered">
		<tbody>
		<?php if ($is_name) { ?>
		<tr>
			<th scope="row"><label for="wr_name">이름<strong class="sound_only"> 필수</strong></label></th>
			<td><input type="text" name="wr_name" value="<?php echo $name ?>" id="wr_name" required class="form-control required" size="10" maxlength="20"></td>
		</tr>
		<?php } ?>

		<?php if ($is_password) { ?>
		<tr>
			<th scope="row"><label for="wr_password">비밀번호<strong class="sound_only"> 필수</strong></label></th>
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
			<th scope="row">옵션</th>
			<td><?php echo $option ?></td>
		</tr>
		<?php } ?>

		<?php if ($is_category) { ?>
		<tr>
			<th scope="row"><label for="ca_name">분류<strong class="sound_only">필수</strong></label></th>
			<td>
				<select name="ca_name" id="ca_name" required class="required form-control" >
					<option value="">선택하세요</option>
					<?php echo $category_option ?>
				</select>
			</td>
		</tr>
		<?php } ?>

		<tr>
			<th scope="row"><label for="wr_subject">Title<strong class="sound_only">필수</strong></label></th>
			<td>
				<div id="autosave_wrapper">
					<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control required" size="50" maxlength="255" placeholder="센서의 위치 및 특징을 구분한 제목 - 예)북문 좌측 접근 1번">
					<?php /* if ($is_member) { // 임시 저장된 글 기능 ?>
					<script src="<?php echo G5_JS_URL; ?>/autosave.js"></script>
					<?php if($editor_content_js) echo $editor_content_js; ?>
					<button type="button" id="btn_autosave" class="btn_frmline">임시 저장된 글 (<span id="autosave_count"><?php echo $autosave_count; ?></span>)</button>
					<div id="autosave_pop">
						<strong>임시 저장된 글 목록</strong>
						<div><button type="button" class="autosave_close"><img src="<?php echo $board_skin_url; ?>/img/btn_close.gif" alt="닫기"></button></div>
						<ul></ul>
						<div><button type="button" class="autosave_close"><img src="<?php echo $board_skin_url; ?>/img/btn_close.gif" alt="닫기"></button></div>
					</div>
					<?php } */ ?>
				</div>
			</td>
		</tr>
		<tr class="wr_content_tr">
			<th scope="row"><label for="wr_content">History<strong class="sound_only">필수</strong></label></th>
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
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_id">ID</label></th>
			<td><input type="text" name="w_id" value="<?php echo $write['w_id'] ?>" id="w_id" class="form-control" placeholder="센서 생성 ID" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_cpu_id">CPU ID</label></th>
			<td><input type="text" name="w_cpu_id" value="<?php echo get_w_cpu_id($write['w_cpu_id']); ?>" id="w_cpu_id" class="form-control" placeholder="시스템 CPU ID" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_system_ip">WITS IP</label></th>
			<td><input type="text" name="w_system_ip" value="<?php echo get_w_system_ip($write['w_system_ip']) ?>" id="w_system_ip" class="form-control" placeholder="시스템 IP 주소" size="50"></td>
		</tr>
		<tr>
			<th scope="row"><label for="w_device_id">USB Device ID</label></th>
			<td>
				<!-- input type="text" name="w_device_id" value="<?php echo $write['w_device_id'] ?>" id="w_device_id" class="form-control" placeholder="센서와 Link된 USB 디바이스 명" size="50" -->
				<?php echo select_w_device_id($write['w_device_id']); ?>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_model_id">Model ID</label></th>
			<td>
				<input type="text" name="w_model_id" value="<?php echo $write['w_model_id'] ?>" id="w_model_id" class="form-control" placeholder="센서 모델 ID" size="50">
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="w_sensor_id">Sensor ID</label></th>
			<td>
				<!-- input type="text" name="w_sensor_id" value="<?php echo $write['w_sensor_id'] ?>" id="w_sensor_id" class="form-control" placeholder="센서 사용자 설정 ID (Logical ID) 예 1 ~ 31" size="50" -->
				<?php echo select_w_sensor_id($write['w_sensor_id']); ?>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_sensor_serial">Sensor Serial #</label></th>
			<td><input type="text" name="w_sensor_serial" value="<?php echo get_w_sensor_serial($write['w_sensor_serial']) ?>" id="w_sensor_serial" class="form-control" placeholder="센서 시리얼 번호(고정:FF FF)" size="50"></td>
		</tr>
		<tr>
			<th scope="row"><label for="w_sensor_model">Sensor Model</label></th>
			<td>
				<!-- input type="text" name="w_sensor_model" value="<?php echo $write['w_sensor_model'] ?>" id="w_sensor_model" class="form-control" placeholder="모델명 예 DND-60L" size="50" -->
				<?php echo select_w_sensor_model($write['w_sensor_model']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="w_sensor_baud">Serial Speed</label></th>
			<td>
				<!-- input type="text" name="w_sensor_baud" value="<?php echo $write['w_sensor_baud'] ?>" id="w_sensor_baud" class="form-control" placeholder="통신 속도" size="50" -->
				<?php echo select_w_sensor_baud($write['w_sensor_baud']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="w_sensor_timeout">Serial Time Out</label></th>
			<td>
				<!-- input type="text" name="w_sensor_timeout" value="<?php echo $write['w_sensor_timeout'] ?>" id="w_sensor_timeout" class="form-control" placeholder="통신 Timeout (second.0)" size="50" -->
				<?php echo select_w_sensor_timeout($write['w_sensor_timeout']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="w_sensor_ignore">Ignore Zone</label></th>
			<td>
				<!-- input type="text" name="w_sensor_ignore" value="<?php echo $write['w_sensor_ignore'] ?>" id="w_sensor_ignore" class="form-control" placeholder="감지 제외 지역 (Ignore zone) 예 1,12" size="50" -->
				<?php echo select_w_sensor_ignore($write['w_sensor_ignore']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="w_sensor_face">Sensor Face</label></th>
			<td>
				<!-- input type="text" name="w_sensor_face" value="<?php echo $write['w_sensor_face'] ?>" id="w_sensor_face" class="form-control" placeholder="설치된 센서 방향 Forward, Backward, Out, In" size="50" -->
				<?php echo select_w_sensor_face($write['w_sensor_face']); ?>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_sensor_angle">Sensor Angle</label></th>
			<td><input type="text" name="w_sensor_angle" value="<?php echo $write['w_sensor_angle'] ?>" id="w_sensor_angle" class="form-control" placeholder="설치된 센서 방위각 0은 무시 1~360" size="50"></td>
		</tr>
		<tr>
			<th scope="row" style="cursor: pointer;" onclick='window.open("<?php echo $board_skin_url?>/mapsInfo.php?get_location=1&myLatS=<?php echo $write['w_sensor_lat_s']?>&myLngS=<?php echo $write['w_sensor_lng_s']?>&myLatE=<?php echo $write['w_sensor_lat_e']?>&myLngE=<?php echo $write['w_sensor_lng_e']?>","mapsInfo", "width=600,height=400,scrollbars=no");'><label for="w_sensor_lat_s">Latitude S</label></th>
			<td><input type="text" name="w_sensor_lat_s" value="<?php echo $write['w_sensor_lat_s'] ?>" id="w_sensor_lat_s" class="form-control" placeholder="설치된 센서 위도" size="50"></td>
		</tr>
		<tr>
			<th scope="row" style="cursor: pointer;" onclick='window.open("<?php echo $board_skin_url?>/mapsInfo.php?get_location=1&myLatS=<?php echo $write['w_sensor_lat_s']?>&myLngS=<?php echo $write['w_sensor_lng_s']?>&myLatE=<?php echo $write['w_sensor_lat_e']?>&myLngE=<?php echo $write['w_sensor_lng_e']?>","mapsInfo", "width=600,height=400,scrollbars=no");'><label for="w_sensor_lng_s">Longitude S</label></th>
			<td><input type="text" name="w_sensor_lng_s" value="<?php echo $write['w_sensor_lng_s'] ?>" id="w_sensor_lng_s" class="form-control" placeholder="설치된 센서 경도" size="50"></td>
		</tr>
		<tr>
			<th scope="row" style="cursor: pointer;" onclick='window.open("<?php echo $board_skin_url?>/mapsInfo.php?get_location=1&myLatS=<?php echo $write['w_sensor_lat_s']?>&myLngS=<?php echo $write['w_sensor_lng_s']?>&myLatE=<?php echo $write['w_sensor_lat_e']?>&myLngE=<?php echo $write['w_sensor_lng_e']?>","mapsInfo", "width=600,height=400,scrollbars=no");'><label for="w_sensor_lat_e">Latitude E</label></th>
			<td><input type="text" name="w_sensor_lat_e" value="<?php echo $write['w_sensor_lat_e'] ?>" id="w_sensor_lat_e" class="form-control" placeholder="설치된 센서 위도" size="50"></td>
		</tr>
		<tr>
			<th scope="row" style="cursor: pointer;" onclick='window.open("<?php echo $board_skin_url?>/mapsInfo.php?get_location=1&myLatS=<?php echo $write['w_sensor_lat_s']?>&myLngS=<?php echo $write['w_sensor_lng_s']?>&myLatE=<?php echo $write['w_sensor_lat_e']?>&myLngE=<?php echo $write['w_sensor_lng_e']?>","mapsInfo", "width=600,height=400,scrollbars=no");'><label for="w_sensor_lng_e">Longitude E</label></th>
			<td><input type="text" name="w_sensor_lng_e" value="<?php echo $write['w_sensor_lng_e'] ?>" id="w_sensor_lng_e" class="form-control" placeholder="설치된 센서 경도" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_sensor_validLv">Due Level</label></th>
			<td><input type="text" name="w_sensor_validLv" value="<?php echo $write['w_sensor_validLv'] ?>" id="w_sensor_validLv" class="form-control" placeholder="연속 데이터간 시간차 (DND_dueTimeValidLv)" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alarm_enable">Alarm Enable</label></th>
			<td>
				<?php echo select_w_alarm_enable($write['w_alarm_enable']); ?>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alarm_level">Alarm Level</label></th>
			<td>
				<?php echo select_w_alarm_level($write['w_alarm_level']); ?>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_stamp">Time Stamp</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($write['w_stamp']) ?>" id="w_stamp" class="form-control" placeholder="TIMESTAMP - 등록 일시" size="50"></td>
		</tr>
		<tr class="w_api_tr">
			<th scope="row"><label for="w_api_devId">API ID</label></th>
			<td><input type="text" name="w_api_devId" value="<?php echo $write['w_api_devId'] ?>" id="w_api_devId" class="form-control" placeholder="API (디바이스 아이디)" size="50"></td>
		</tr>
		<tr class="w_api_tr">
			<th scope="row"><label for="w_api_devPass">API Password</label></th>
			<td><input type="text" name="w_api_devPass" value="<?php echo $write['w_api_devPass'] ?>" id="w_api_devPass" class="form-control" placeholder="API (디바이스 비밀번호)" size="50"></td>
		</tr>
		<tr class="w_api_tr">
			<th scope="row"><label for="w_api_gwId">API Gateway ID</label></th>
			<td><input type="text" name="w_api_gwId" value="<?php echo $write['w_api_gwId'] ?>" id="w_api_gwId" class="form-control" placeholder="API (디바이스 게이트웨이)" size="50"></td>
		</tr>
		<tr class="w_api_tr">
			<th scope="row"><label for="w_api_ipAddr">API IP</label></th>
			<td><input type="text" name="w_api_ipAddr" value="<?php echo $write['w_api_ipAddr'] ?>" id="w_api_ipAddr" class="form-control" placeholder="API (디바이스 아이피)" size="50"></td>
		</tr>
		<tr class="w_api_tr">
			<th scope="row"><label for="w_api_ipPort">API Port</label></th>
			<td><input type="text" name="w_api_ipPort" value="<?php echo $write['w_api_ipPort'] ?>" id="w_api_ipPort" class="form-control" placeholder="API (디바이스 포트)" size="50"></td>
		</tr>
		<tr class="w_api_tr">
			<th scope="row"><label for="w_api_tagId">API Tag ID</label></th>
			<td><input type="text" name="w_api_tagId" value="<?php echo $write['w_api_tagId'] ?>" id="w_api_tagId" class="form-control" placeholder="API (Tag Stream ID)" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_host_ip">Host IP</label></th>
			<td><input type="text" name="w_host_ip" value="<?php echo $write['w_host_ip'] ?>" id="w_host_ip" class="form-control" placeholder="Host(WITS) IP" size="50"></td>
		</tr>

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
        <input type="submit" value="작성완료" id="btn_submit" accesskey="s" class="btn btn-success">
        <a href="./board.php?bo_table=<?php echo $bo_table ?>" class="btn btn-primary">취소</a>
    </div>
    </form>

    <script>
    <?php if($write_min || $write_max) { ?>
    // 글자수 제한
    var char_min = parseInt(<?php echo $write_min; ?>); // 최소
    var char_max = parseInt(<?php echo $write_max; ?>); // 최대
    check_byte("wr_content", "char_count");

    $(function() {
        $("#wr_content").on("keyup", function() {
            check_byte("wr_content", "char_count");
        });
    });

    <?php } ?>
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

    function fwrite_submit(f)
    {
        <?php echo $editor_js; // 에디터 사용시 자바스크립트에서 내용을 폼필드로 넣어주며 내용이 입력되었는지 검사함   ?>

        var subject = "";
        var content = "";
        $.ajax({
            url: g5_bbs_url+"/ajax.filter.php",
            type: "POST",
            data: {
                "subject": f.wr_subject.value,
                "content": f.wr_content.value
            },
            dataType: "json",
            async: false,
            cache: false,
            success: function(data, textStatus) {
                subject = data.subject;
                content = data.content;
            }
        });

        if (subject) {
            alert("제목에 금지단어('"+subject+"')가 포함되어있습니다");
            f.wr_subject.focus();
            return false;
        }

        if (content) {
            alert("내용에 금지단어('"+content+"')가 포함되어있습니다");
            if (typeof(ed_wr_content) != "undefined")
                ed_wr_content.returnFalse();
            else
                f.wr_content.focus();
            return false;
        }

        if (document.getElementById("char_count")) {
            if (char_min > 0 || char_max > 0) {
                var cnt = parseInt(check_byte("wr_content", "char_count"));
                if (char_min > 0 && char_min > cnt) {
                    alert("내용은 "+char_min+"글자 이상 쓰셔야 합니다.");
                    return false;
                }
                else if (char_max > 0 && char_max < cnt) {
                    alert("내용은 "+char_max+"글자 이하로 쓰셔야 합니다.");
                    return false;
                }
            }
        }

        <?php echo $captcha_js; // 캡챠 사용시 자바스크립트에서 입력된 캡챠를 검사함  ?>

        document.getElementById("btn_submit").disabled = "disabled";

        return true;
    }
    </script>
</section>
<!-- } 게시물 작성/수정 끝 -->