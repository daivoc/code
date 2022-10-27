<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/config_sensor.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List

$title_msg =(($w == 'u')?$SK_BO_Modify[ITS_Lang]:$SK_BO_New[ITS_Lang]);
$g5['title'] = ((G5_IS_MOBILE && $board['bo_mobile_subject']) ? $board['bo_mobile_subject'] : $board['bo_subject']).' '.$title_msg;
$access_log = $_SERVER[REMOTE_ADDR].':'.date("Y-m-d h:i:s").'-'.$title_msg.'-'.$member['mb_name'].'<br>'.$write['wr_content'];

if($w == '') {
	include_once("$board_skin_path/sql.php"); // Local Function List

	$write['w_sensor_face'] = 0; // TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_angle'] = 0; // int(11) NOT NULL DEFAULT '0',
	$write['w_sensor_lat_s'] = 0; // double NOT NULL DEFAULT '0', 37.516529,127.1046888
	$write['w_sensor_lng_s'] = 0; // double NOT NULL DEFAULT '0',
	$write['w_sensor_lat_e'] = 0; // double NOT NULL DEFAULT '0', 37.516689,127.1051638
	$write['w_sensor_lng_e'] = 0; // double NOT NULL DEFAULT '0',
	$write['w_sensor_ignoreS'] = 0; // 적용범위 float NOT NULL DEFAULT '0',
	$write['w_sensor_ignoreE'] = $MAX_numberOfDist; // 적용범위 float NOT NULL DEFAULT '0',
	$write['w_sensor_ignoreZone'] = ''; // 상시차단 varchar(256) DEFAULT NULL,
	$write['w_sensor_scheduleS'] = 0; // 예약차단 float NOT NULL DEFAULT '0',
	$write['w_sensor_scheduleE'] = 0; // 예약차단 float NOT NULL DEFAULT '0',
	$write['w_sensor_disable'] = 0; // 사용중지 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_stop'] = 0; // 일시정지 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_reload'] = 0; // 즉시적용 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_Addr'] = $DEVICE_IP; // 즉시적용 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_sensor_Port'] = $DEVICE_port; // 즉시적용 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_virtual_Addr'] = $DEVICE_vIP; // 즉시적용 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_virtual_Port'] = $DEVICE_vPort; // 즉시적용 TINYINT(1) NOT NULL DEFAULT '0',
	$write['w_email_Addr'] = $DEVICE_email_Addr; // `w_email_Addr` varchar(256) DEFAULT NULL,
	$write['w_email_Time'] = $DEVICE_email_Time; // `w_email_Time` varchar(16) DEFAULT NULL,
	$write['w_event_pickTime'] = 0; // 대기시간 double NOT NULL DEFAULT '0',
	$write['w_event_holdTime'] = 7; // 허용회수 double NOT NULL DEFAULT '0', 7회 ~ 1초
	$write['w_sensor_spot'] = 2000; // 동일한 위치 허용 범위 MAX_event_syncDist = 4000 이전 거리와 비교 동일한 거리로 간주 함 1m = 1000 
	$write['w_sensor_offset'] = 0; // 허용회수 double NOT NULL DEFAULT '0', 7회 ~ 1초
	$write['w_alarm_disable'] = 0; // 알람정지 tinyint(1) NOT NULL DEFAULT '0',
	$write['w_alarm_level'] = 2; // 알람등급 tinyint(4) NOT NULL DEFAULT '0',
}
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/css/jquery-ui.css">
<script src="<?php echo $board_skin_url?>/js/jquery-ui.js"></script>

<style>
th { width:120px; }
.wr_content_tr { display:none; }
.w_hide { display:none; }
.w_detail_tr { display:none; background-color: #fff8e1; font-size: 8pt; }
.w_detail_tr th { background-color: white; }
.w_default_tr { display:none; background-color: #f0f0f0; font-size: 8pt; }
.w_default_tr th { background-color: white; }
.w_number_input	{ border:0; width: 60px; color:#808080; text-align: right; font-size: 8pt; padding-right: 4pt; margin-bottom: 4px; }
.btn_option_01 { text-align: right; padding: 4px 0; }
.input25P { width: 25%; display: initial; float: left; }
.input50P { width: 50%; display: initial; float: left; }
.weekday {width: 28px; float: left; text-align: center;}

#select_w_sensor_ignoreZone .ui-selecting { background: #FECA40; }
#select_w_sensor_ignoreZone .ui-selected { background: #ffc107; color: white; }
#select_w_sensor_ignoreZone { list-style-type: none; margin: 0; padding: 0; width: 100%; }
#select_w_sensor_ignoreZone li { margin: 1px; padding: 1px; float: left; width: 22px; height: 22px; font-size: 6pt; text-align: center; }
#select_w_sensor_scheduleZone .ui-selecting { background: #FECA40; }
#select_w_sensor_scheduleZone .ui-selected { background: #ffc107; color: white; }
#select_w_sensor_scheduleZone { list-style-type: none; margin: 0; padding: 0; width: 100%; }
#select_w_sensor_scheduleZone li { margin: 1px; padding: 1px; float: left; width: 22px; height: 22px; font-size: 6pt; text-align: center; }

#select_w_sensor_scheduleTime .ui-selecting { background: #FF5722; }
#select_w_sensor_scheduleTime .ui-selected { background: #FF5722; color: white; }
#select_w_sensor_scheduleTime { list-style-type: none; margin: 0; padding: 0; width: 100%; }
#select_w_sensor_scheduleTime li { margin: 0px; padding: 1px; float: left; width: 22px; height: 22px; border-radius: 8px; font-size: 6pt; text-align: center; }
</style>

<script type="text/javascript">
$(document).ready(function(){
	$("#wr_content").val('<?php echo $access_log; ?>');
	$('#wr_content').prop('readonly', true);
	$('#w_cpu_id').prop('readonly', true);
	$('#w_system_ip').prop('readonly', true);
	$('#w_system_port').prop('readonly', true);
	$('#w_sensor_serial').prop('readonly', true);
	$('#w_virtual_Addr').prop('readonly', true);
	$('#w_virtual_Port').prop('readonly', true);
	$('#w_sensor_Addr').prop('readonly', true);
	$('#w_sensor_Port').prop('readonly', true);
	$('#w_table_PortIn').prop('readonly', true);
	$('#w_table_PortOut').prop('readonly', true);
	$('#w_stamp').prop('readonly', true);
	$('#w_stamp').prop('readonly', true);
	
	$('#btn_detail').on('click', function(event) {        
		 $('.w_detail_tr').toggle('show');
	});
	$('#btn_default').on('click', function(event) {        
		 $('.w_default_tr').toggle('show');
	});


	$(function() {
		$("#slider-range_w_sensor_ignore").slider({ // 참조: https://jqueryui.com/slider/#range
			range: true,
			min: 0,
			max: <?php echo $MAX_numberOfDist ?>,
			values: [ $("#w_sensor_ignoreS").val(), $("#w_sensor_ignoreE").val() ],
			slide: function(event, ui) {
				$("#w_sensor_ignoreS").val(ui.values[ 0 ]);
				$("#w_sensor_ignoreE").val(ui.values[ 1 ]);
				$("#w_sensor_ignoreSDisp").text(Math.ceil((ui.values[ 0 ] / 1000) * 100)/100);
				$("#w_sensor_ignoreEDisp").text(Math.ceil((ui.values[ 1 ] / 1000) * 100)/100);
				// $("#w_sensor_scheduleSDisp").text(Math.ceil((ui.values[ 0 ] / 1000) * 100)/100);
				// $("#w_sensor_scheduleEDisp").text(Math.ceil((ui.values[ 1 ] / 1000) * 100)/100);
				
			}
		});
		$("#slider-range_w_sensor_ignore").slider({ // 참조: https://jqueryui.com/slider/#range
			stop: function(event, ui) {
				resultS = parseInt(ui.values[ 0 ] / <?php echo $MAX_stepOfZone ?>);
				for (i = 0; i < resultS; i++) { 
					$("#select_w_sensor_ignoreZone #igZone_"+i).addClass("ui-selected");
				}
				resultE = parseInt(ui.values[ 1 ] / <?php echo $MAX_stepOfZone ?>) + 1;
				for (i = resultE; i < <?php echo $MAX_numberOfZone ?>; i++) { 
					$("#select_w_sensor_ignoreZone #igZone_"+i).addClass("ui-selected");
				}
				for (i = resultS; i < resultE; i++) { 
					$("#select_w_sensor_ignoreZone #igZone_"+i).removeClass("ui-selected");
				}
				// 비활성화 영역을 저장 한다.
				$("#w_sensor_ignoreZone").val(""); // 기존값 삭제
				for (i = 0; i < <?php echo $MAX_numberOfZone ?>; i++) { 
					if($("#select_w_sensor_ignoreZone #igZone_"+i).hasClass("ui-selected"))
						$("#w_sensor_ignoreZone").val($("#w_sensor_ignoreZone").val() + i + ",");
				}
			}
		});
		$("#w_sensor_ignoreSDisp").text(Math.ceil(($("#slider-range_w_sensor_ignore").slider("values")[0] / 1000) * 100)/100);
		$("#w_sensor_ignoreEDisp").text(Math.ceil(($("#slider-range_w_sensor_ignore").slider("values")[1] / 1000) * 100)/100);
	});

	$(function() {
		$("#select_w_sensor_ignoreZone").selectable({ // 참조 http://jqueryui.com/selectable/#display-grid
			stop: function() { // 
				$("#w_sensor_ignoreZone").val("");
				$(".ui-selected", this).each(function() {
					var index = $("#select_w_sensor_ignoreZone li").index(this);
					$("#w_sensor_ignoreZone").val($("#w_sensor_ignoreZone").val() + index + ",");
				});
			}
		});
		// $("#igZone_2").addClass("ui-selected");
	});

	$(function() { 
		$("#slider-range_w_event_pickTime").slider({ // 참조 https://jqueryui.com/slider/#rangemax
			range: "max",
			min: 1,
			max: <?php echo $MAX_event_pickTime ?>,
			value: $("#w_event_pickTime").val(),
			slide: function(event, ui) {
				$("#w_event_pickTime").val(ui.value);
				$("#w_event_pickTimeDisp").text(ui.value / 1000);
			}
		});
		$("#w_event_pickTimeDisp").text($("#w_event_pickTime").val() / 1000);
	});

	$(function() {
		$("#slider-range_w_event_holdTime").slider({ // 참조 https://jqueryui.com/slider/#rangemax
			range: "max",
			min: 1,
			max: <?php echo $MAX_event_holdTime ?>,
			value: $("#w_event_holdTime").val(),
			slide: function(event, ui) {
				$("#w_event_holdTime").val(ui.value);
				$("#w_event_holdTimeDisp").text(ui.value);
				$("#w_event_holdTimeDispSec").text(Math.ceil((ui.value * 0.13) * 10)/10);
			}
		});
		$("#w_event_holdTimeDisp").text($("#w_event_holdTime").val());
		$("#w_event_holdTimeDispSec").text(Math.ceil(($("#w_event_holdTime").val() * 0.13) * 10)/10);
	});

	$(function() {
		$("#slider-range_w_sensor_offset").slider({ // 참조 https://jqueryui.com/slider/#rangemax
			range: "max",
			min: 0,
			max: <?php echo $MAX_event_offset ?>,
			value: $("#w_sensor_offset").val(),
			slide: function(event, ui) {
				$("#w_sensor_offset").val(ui.value);
				$("#w_sensor_offsetDisp").text(ui.value);
			}
		});
		$("#w_sensor_offsetDisp").text($("#w_sensor_offset").val());
	});

	$(function() {
		$("#slider-range_w_sensor_spot").slider({ // 참조 https://jqueryui.com/slider/#rangemax
			range: "max",
			min: 0,
			max: <?php echo $MAX_event_spot ?>,
			value: $("#w_sensor_spot").val(),
			slide: function(event, ui) {
				$("#w_sensor_spot").val(ui.value);
				$("#w_sensor_spotDisp").text(ui.value);
			}
		});
		$("#w_sensor_spotDisp").text($("#w_sensor_spot").val());
	});

	$(function() {
		$("#slider-range_w_sensor_schedule").slider({ // 참조: https://jqueryui.com/slider/#range
			range: true,
			min: 0,
			max: <?php echo $MAX_numberOfDist ?>,
			values: [ $("#w_sensor_scheduleS").val(), $("#w_sensor_scheduleE").val() ],
			slide: function(event, ui) {
				$("#w_sensor_scheduleS").val(ui.values[ 0 ]);
				$("#w_sensor_scheduleE").val(ui.values[ 1 ]);
				$("#w_sensor_scheduleSDisp").text(Math.ceil((ui.values[ 0 ] / 1000) * 100)/100);
				$("#w_sensor_scheduleEDisp").text(Math.ceil((ui.values[ 1 ] / 1000) * 100)/100);
			}
		});
		$("#slider-range_w_sensor_schedule").slider({ // 참조: https://jqueryui.com/slider/#range
			stop: function(event, ui) {
				resultS = parseInt(ui.values[ 0 ] / <?php echo $MAX_stepOfZone ?>);
				for (i = 0; i < resultS; i++) { 
					$("#select_w_sensor_scheduleZone #igZone_"+i).addClass("ui-selected");
				}
				resultE = parseInt(ui.values[ 1 ] / <?php echo $MAX_stepOfZone ?>) + 1;
				for (i = resultE; i < <?php echo $MAX_numberOfZone ?>; i++) { 
					$("#select_w_sensor_scheduleZone #igZone_"+i).addClass("ui-selected");
				}
				for (i = resultS; i < resultE; i++) { 
					$("#select_w_sensor_scheduleZone #igZone_"+i).removeClass("ui-selected");
				}
				// 비활성화 영역을 저장 한다.
				$("#w_sensor_scheduleZone").val(""); // 기존값 삭제
				for (i = 0; i < <?php echo $MAX_numberOfZone ?>; i++) { 
					if($("#select_w_sensor_scheduleZone #igZone_"+i).hasClass("ui-selected"))
						$("#w_sensor_scheduleZone").val($("#w_sensor_scheduleZone").val() + i + ",");
				}
			}
		});
		$("#w_sensor_scheduleSDisp").text(Math.ceil(($("#slider-range_w_sensor_schedule").slider("values")[0] / 1000) * 100)/100);
		$("#w_sensor_scheduleEDisp").text(Math.ceil(($("#slider-range_w_sensor_schedule").slider("values")[1] / 1000) * 100)/100);
	});
	$(function() {
		$("#select_w_sensor_scheduleZone").selectable({ // 참조 http://jqueryui.com/selectable/#display-grid
			stop: function() { // 
				$("#w_sensor_scheduleZone").val("");
				$(".ui-selected", this).each(function() {
					var index = $("#select_w_sensor_scheduleZone li").index(this);
					$("#w_sensor_scheduleZone").val($("#w_sensor_scheduleZone").val() + index + ",");
				});
			}
		});
		// $("#igZone_2").addClass("ui-selected");
	});
	
	$(function() {
		$("#slider-range_w_sensor_angle").slider({ // 참조 https://jqueryui.com/slider/#rangemax
			range: "max",
			min: 0,
			max: 360,
			value: $("#w_sensor_angle").val(),
			slide: function(event, ui) {
				$("#w_sensor_angle").val(ui.value);
				$("#w_sensor_angleDisp").text(ui.value);
			}
		});
		$("#w_sensor_angleDisp").text($("#w_sensor_angle").val());
	});

	$(function() {
		$("#select_w_sensor_scheduleTime").selectable({ // 참조 http://jqueryui.com/selectable/#display-grid
			stop: function() { // 
				$("#w_sensor_time").val("");
				$(".ui-selected", this).each(function() {
					var index = $("#select_w_sensor_scheduleTime li").index(this);
					$("#w_sensor_time").val($("#w_sensor_time").val() + index + ",");
				});
			}
		});
		// $("#igTime_2").addClass("ui-selected");
	});
	
	$('.weekBox input:checkbox').change(function(){
		var tempValue='';
		tempValue=$('.weekBox  input:checkbox').map(function(n){
			if(this.checked){
				return  this.value;
			};
		}).get().join(',');
		$('#w_sensor_week').val(tempValue);
	})	

	$( "#w_device_id" ).change(function() {
		var str_array = $( "#w_device_id" ).val().split('_');
		var w_virtual_Addr = str_array[1];
		$( "#w_virtual_Addr" ).val(w_virtual_Addr);
		var str_array = w_virtual_Addr.split('.');
		var w_sensor_Addr = str_array[0]+'.'+str_array[1]+'.'+str_array[2]+'.30'
		$( "#w_sensor_Addr" ).val(w_sensor_Addr);
	});
});
</script>
  
<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name "><?php echo $g5['title'] ?><span class="sound_only"> 목록</span></span>
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

    <input type="hidden" name="w_sensor_noOfZone" value="<?php echo $MAX_numberOfZone ?>">
    <input type="hidden" name="w_sensor_stepOfZone" value="<?php echo $MAX_stepOfZone ?>">
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
        <input type="button" value="<?php echo $SK_BO_Basic[ITS_Lang]?>" id="btn_default" class="btn btn-warning">
        <input type="button" value="<?php echo $SK_BO_Advanced[ITS_Lang]?>" id="btn_detail" class="btn btn-info">
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
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Name[ITS_Lang]?><strong class="sound_only">필수</strong></label></th>
			<td>
					<input type="text" name="wr_subject" value="<?php echo $subject ?>" id="wr_subject" required class="form-control input50P required" size="50" maxlength="255" placeholder="Sensor Name Ex: East Gate 3">
					<?php echo select_w_sensor_model($write['w_sensor_model']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row" title="USB Device ID"><label for="w_device_id"><?php echo $SK_BO_Device_Name[ITS_Lang]?></label></th>
			<td>
				<?php // echo select_w_device_id($write['w_device_id']); ?>
				<?php echo select_w_etherNet_id($write['w_device_id']); ?>
				
				<input type="text" name="w_sensor_serial" value="<?php echo $write['w_sensor_serial'] ?>" id="w_sensor_serial" class="form-control input50P" placeholder="Sensor Serial" size="50">
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class="w_hide">
			<th scope="row" title="Accept Range"><label for="w_sensor_ignore">상시차단</label></th>
			<td>
				<span id="w_sensor_ignoreSDisp">0</span> ~ <span id="w_sensor_ignoreEDisp">0</span> <?php echo $SK_BO_Meter[ITS_Lang]?>
				<input type="text" name="w_sensor_ignoreS" value="<?php echo $write['w_sensor_ignoreS'] ?>" id="w_sensor_ignoreS" readonly class="w_hide"><input type="text" name="w_sensor_ignoreE" value="<?php echo $write['w_sensor_ignoreE'] ?>" id="w_sensor_ignoreE" readonly class="w_hide">
				<div id="slider-range_w_sensor_ignore"></div>
				<?php echo select_w_sensor_ignoreZone($write['w_sensor_ignoreZone'], $MAX_numberOfZone); ?>
			</td>
		</tr>
		<tr class="w_default_tr">
			<th scope="row" title="Limit Due and Level"><label for="w_sensor_angle"><?php echo $SK_BO_Level[ITS_Lang]?>/<?php echo $SK_BO_Delay[ITS_Lang]?></label></th>
			<td>
				<?php echo select_w_alarm_level($write['w_alarm_level']); ?>
				<div class="input50P" style="padding: 10px 15px;">
				<?php echo $SK_BO_Event_Hold[ITS_Lang]?>: <span id="w_event_holdTimeDisp"></span><?php echo $SK_BO_Times[ITS_Lang]?> (<?php echo $SK_BO_About[ITS_Lang]?> <span id="w_event_holdTimeDispSec"></span> <?php echo $SK_BO_Second[ITS_Lang]?>)
				<input type="text" name="w_event_holdTime" value="<?php echo $write['w_event_holdTime'] ?>" id="w_event_holdTime" readonly class="w_hide">
				<div id="slider-range_w_event_holdTime"></div>
				</div>
			</td>
		</tr>
		<tr class="w_default_tr">
			<th scope="row" style="cursor: pointer;" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/status/mapsInfo.php?get_location=1&myLatS=<?php echo $write['w_sensor_lat_s']?>&myLngS=<?php echo $write['w_sensor_lng_s']?>&myLatE=<?php echo $write['w_sensor_lat_e']?>&myLngE=<?php echo $write['w_sensor_lng_e']?>","mapsInfo", "width=600,height=400,scrollbars=no");' title="Latitude S"><label for="w_sensor_lat_s"><?php echo $SK_BO_Start_Coord[ITS_Lang]?></label></th>
			<td><input type="text" name="w_sensor_lat_s" value="<?php echo $write['w_sensor_lat_s'] ?>" id="w_sensor_lat_s" class="form-control input50P" placeholder="Installed sensors latitude" size="50"><input type="text" name="w_sensor_lng_s" value="<?php echo $write['w_sensor_lng_s'] ?>" id="w_sensor_lng_s" class="form-control input50P" placeholder="Installed sensors longitude" size="50"></td>
		</tr>
		<tr class="w_default_tr">
			<th scope="row" style="cursor: pointer;" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/status/mapsInfo.php?get_location=1&myLatS=<?php echo $write['w_sensor_lat_s']?>&myLngS=<?php echo $write['w_sensor_lng_s']?>&myLatE=<?php echo $write['w_sensor_lat_e']?>&myLngE=<?php echo $write['w_sensor_lng_e']?>","mapsInfo", "width=600,height=400,scrollbars=no");' title="Latitude E"><label for="w_sensor_lat_e"><?php echo $SK_BO_End_Coord[ITS_Lang]?></label></th>
			<td><input type="text" name="w_sensor_lat_e" value="<?php echo $write['w_sensor_lat_e'] ?>" id="w_sensor_lat_e" class="form-control input50P" placeholder="Installed sensors latitude" size="50"><input type="text" name="w_sensor_lng_e" value="<?php echo $write['w_sensor_lng_e'] ?>" id="w_sensor_lng_e" class="form-control input50P" placeholder="Installed sensors longitude" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Serial Time Out"><label for="w_event_pickTime"><?php echo $SK_BO_Event_Hold[ITS_Lang]?></label></th>
			<td>
				<span id="w_event_pickTimeDisp"></span> <?php echo $SK_BO_Second[ITS_Lang]?>
				<input type="text" name="w_event_pickTime" value="<?php echo $write['w_event_pickTime'] ?>" id="w_event_pickTime" readonly class="w_hide">
				<div id="slider-range_w_event_pickTime"></div>
			</td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
		<tr class="w_hide">
			<th scope="row" title="Limit Due and Level"><label for="w_sensor_angle">범주/편차</label></th>
			<td>
				<div class="input50P" style="padding: 10px 15px;">
				Same Spot: <span id="w_sensor_spotDisp"></span> Cm
				<input type="text" name="w_sensor_spot" value="<?php echo $write['w_sensor_spot'] ?>" id="w_sensor_spot" readonly class="w_hide">
				<div id="slider-range_w_sensor_spot"></div>
				</div>
				<div class="input50P" style="padding: 10px 15px;">
				Offset: <span id="w_sensor_offsetDisp"></span> Cm
				<input type="text" name="w_sensor_offset" value="<?php echo $write['w_sensor_offset'] ?>" id="w_sensor_offset" readonly class="w_hide">
				<div id="slider-range_w_sensor_offset"></div>
				</div>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Schedule Ignore"><label for="w_sensor_schedule">Schedule Zone</label></th>
			<td>
				<span id="w_sensor_scheduleSDisp">0</span> ~ <span id="w_sensor_scheduleEDisp">0</span> M
				<input type="text" name="w_sensor_scheduleS" value="<?php echo $write['w_sensor_scheduleS'] ?>" id="w_sensor_scheduleS" readonly class="w_hide"><input type="text" name="w_sensor_scheduleE" value="<?php echo $write['w_sensor_scheduleE'] ?>" id="w_sensor_scheduleE" readonly class="w_hide">
				<div id="slider-range_w_sensor_schedule"></div>
				<?php echo select_w_sensor_scheduleZone($write['w_sensor_scheduleZone'], $MAX_numberOfZone); ?></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row" title="Schedule Ignore"><label for="w_sensor_schedule">Schedule<br>Week/Time</label></th>
			<td>
				<div class="weekBox input50P">
					<table><tr>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Sun" value = "6" <?php echo preg_match("/6/", $write['w_sensor_week'])?'checked':'';?> /><label for="Sun">Sun</label></td>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Mon" value = "0" <?php echo preg_match("/0/", $write['w_sensor_week'])?'checked':'';?> /><label for="Mon">Mon</label></td>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Tue" value = "1" <?php echo preg_match("/1/", $write['w_sensor_week'])?'checked':'';?> /><label for="Tue">Tue</label></td>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Wen" value = "2" <?php echo preg_match("/2/", $write['w_sensor_week'])?'checked':'';?> /><label for="Wen">Wen</label></td>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Thu" value = "3" <?php echo preg_match("/3/", $write['w_sensor_week'])?'checked':'';?> /><label for="Thu">Thu</label></td>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Fri" value = "4" <?php echo preg_match("/4/", $write['w_sensor_week'])?'checked':'';?> /><label for="Fri">Fri</label></td>
					<td class="weekday"><input class="form-control" type = "checkbox" id = "Sat" value = "5" <?php echo preg_match("/5/", $write['w_sensor_week'])?'checked':'';?> /><label for="Sat">Sat</label></td>
					<?php if($w == 'u') { ?>
					<td style="padding: 0 10px;"><input type="button" value="Time" class="form-control" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/scheduleBlock/weekView.php?bo_table=<?php echo $bo_table?>&wr_id=<?php echo $write['wr_id']?>&wr_subject=Setup Weekly Schedule&w_sensor_serial=<?php echo $write['w_sensor_serial']?>","scheduleWeek_<?php echo $write['wr_id']?>", "width=600,height=500,scrollbars=no");'></td>
					<?php } ?>
					</tr></table>
					<input type="text" name="w_sensor_week" value="<?php echo $write['w_sensor_week'] ?>" id="w_sensor_week" readonly class="w_hide">
				</div>
				<div class="input50P">
				<?php // echo select_w_sensor_scheduleTime($write['w_sensor_time']); ?>
				</div>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row" title="Sensor Angle"><label for="w_sensor_angle">Direction/Angle</label></th>
			<td>
				<?php echo select_w_sensor_face($write['w_sensor_face']); ?>
				<div class="input50P" style="padding: 10px 15px;"> Angle <span id="w_sensor_angleDisp"></span>˚
				<input type="text" name="w_sensor_angle" value="<?php echo $write['w_sensor_angle'] ?>" id="w_sensor_angle" readonly class="form-control w_hide">
				<div id="slider-range_w_sensor_angle"></div>
				</div>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ID"><label for="w_id">ITS/CPU ID</label></th>
			<td><input type="text" name="w_id" value="<?php echo $write['w_id'] ?>" id="w_id" class="form-control input50P" placeholder="Sensor ID" size="50"><input type="text" name="w_cpu_id" value="<?php echo get_w_cpu_id($write['w_cpu_id']); ?>" id="w_cpu_id" class="form-control input50P" placeholder="System CPU ID" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS IP"><label for="w_system_ip">ITS IP</label></th>
			<td><input type="text" name="w_system_ip" value="<?php echo get_w_system_ip($write['w_system_ip']) ?>" id="w_system_ip" class="form-control input50P" placeholder="System IP Address" size="50"><input type="text" name="w_system_port" value="<?php echo G5_CU_MASTER_PORT ?>" id="w_system_port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS BF IP"><label for="w_systemBF_ip">ITS BF IP</label></th>
			<td><input type="text" name="w_systemBF_ip" value="<?php echo ($write['w_systemBF_ip']) ?>" id="w_systemBF_ip" class="form-control input50P" placeholder="System IP Address" size="50"><input type="text" name="w_systemBF_port" value="<?php echo $write['w_systemBF_port'] ?>" id="w_systemBF_port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS AF IP"><label for="w_systemAF_ip">ITS AF IP</label></th>
			<td><input type="text" name="w_systemAF_ip" value="<?php echo ($write['w_systemAF_ip']) ?>" id="w_systemAF_ip" class="form-control input50P" placeholder="System IP Address" size="50"><input type="text" name="w_systemAF_port" value="<?php echo $write['w_systemAF_port'] ?>" id="w_systemAF_port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_master_Addr">Master</label></th>
			<td><input type="text" name="w_master_Addr" value="<?php echo $write['w_master_Addr'] ?>" id="w_master_Addr" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_master_Port" value="<?php echo $write['w_master_Port'] ?>" id="w_master_Port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_virtual_Addr">Virtual</label></th>
			<td><input type="text" name="w_virtual_Addr" value="<?php echo $write['w_virtual_Addr'] ?>" id="w_virtual_Addr" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_virtual_Port" value="<?php echo get_w_virtual_Port($write['w_virtual_Port']) ?>" id="w_virtual_Port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_sensor_Addr">Sensor</label></th>
			<td><input type="text" name="w_sensor_Addr" value="<?php echo get_w_sensor_Addr($write['w_sensor_Addr']) ?>" id="w_sensor_Addr" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_sensor_Port" value="<?php echo get_w_sensor_Port($write['w_sensor_Port']) ?>" id="w_sensor_Port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_email_Addr">Email</label></th>
			<td><input type="text" name="w_email_Addr" value="<?php echo $write['w_email_Addr'] ?>" id="w_email_Addr" class="form-control input50P" placeholder="Email for Alarm Report" size="50"><input type="text" name="w_email_Time" value="<?php echo $write['w_email_Time'] ?>" id="w_email_Time" class="form-control input50P" placeholder="Ex:09:00" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_table_PortIn">TablePort</label></th>
			<td><input type="text" name="w_table_PortIn" value="<?php echo $write['w_table_PortIn'] ?>" id="w_table_PortIn" class="form-control input50P" placeholder="Table PortIn Ex:8000~8999" size="50"><input type="text" name="w_table_PortOut" value="<?php echo $write['w_table_PortOut'] ?>" id="w_table_PortOut" class="form-control input50P" placeholder="Table PortOut Ex:9000~9999" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_host_Addr">Host(1st)</label></th>
			<td><input type="text" name="w_host_Addr" value="<?php echo $write['w_host_Addr'] ?>" id="w_host_Addr" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_host_Port" value="<?php echo $write['w_host_Port'] ?>" id="w_host_Port" class="form-control input50P" placeholder="Port Ex:9999" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_host_Addr2">Host(2nd)</label></th>
			<td><input type="text" name="w_host_Addr2" value="<?php echo $write['w_host_Addr2'] ?>" id="w_host_Addr2" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_host_Port2" value="<?php echo $write['w_host_Port2'] ?>" id="w_host_Port2" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_tcp_Addr">Tcp</label></th>
			<td><input type="text" name="w_tcp_Addr" value="<?php echo $write['w_tcp_Addr'] ?>" id="w_tcp_Addr" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_tcp_Port" value="<?php echo $write['w_tcp_Port'] ?>" id="w_tcp_Port" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_tcp_Addr2">Tcp2</label></th>
			<td><input type="text" name="w_tcp_Addr2" value="<?php echo $write['w_tcp_Addr2'] ?>" id="w_tcp_Addr2" class="form-control input50P" placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_tcp_Port2" value="<?php echo $write['w_tcp_Port2'] ?>" id="w_tcp_Port2" class="form-control input50P" placeholder="Port Ex:50007" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_url1">Snapshot</label></th>
			<td><input type="text" name="w_url1" value="<?php echo $write['w_url1'] ?>" id="w_url1" class="form-control" placeholder="URL Ex:http://121.165.208.119:8080/" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_url2">Streaming</label></th>
			<td><input type="text" name="w_url2" value="<?php echo $write['w_url2'] ?>" id="w_url2" class="form-control" placeholder="URL Ex:http://121.165.208.119:8080/" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alert_Port">Alert</label></th>
			<td>
				<?php echo select_w_GPIO_alert($write['w_alert_Port']); ?>
				<input type="text" name="w_alert_Value" value="<?php echo $write['w_alert_Value'] ?>" id="w_alert_Value" class="form-control input50P" placeholder="Due Time" size="50">
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_alert2_Port">Alert2</label></th>
			<td><input type="text" name="w_alert2_Port" value="<?php echo $write['w_alert2_Port'] ?>" id="w_alert2_Port" class="form-control input50P" placeholder="GPIO Port" size="50"><input type="text" name="w_alert2_Value" value="<?php echo $write['w_alert2_Value'] ?>" id="w_alert2_Value" class="form-control input50P" placeholder="Due Time" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_keycode">Key</label></th>
			<td><input type="text" name="w_keycode" value="<?php echo $write['w_keycode'] ?>" id="w_keycode" class="form-control" placeholder="Key" size="50"></td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_license">License</label></th>
			<td><input type="text" name="w_license" value="<?php echo $write['w_license'] ?>" id="w_license" class="form-control" placeholder="License Code" size="50"></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Time Stamp"><label for="w_stamp">Created</label></th>
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
			<td><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><input type="checkbox" class="form-control" name="w_alarm_disable" id="w_alarm_disable" value="1" <?php echo $write[w_alarm_disable]?'checked':'';?> title="Do not send valid event to host."></td>
			<td><?php echo $SK_BO_Apply[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_reload" id="w_sensor_reload" value="1" <?php echo $write[w_sensor_reload]?'checked':'';?> title="Restart Sensor when catch first event after save this"></td>
			<td class="w_default_tr">허용주기고정<input type="checkbox" class="form-control" name="w_event_keepHole" id="w_event_keepHole" value="1" <?php echo $write[w_event_keepHole]?'checked':'';?> title="Keep event hold cycle."></td>
			<td class="w_hide">동일거리고정<input type="checkbox" class="form-control" name="w_event_syncDist" id="w_event_syncDist" value="1" <?php echo $write[w_event_syncDist]?'checked':'';?> title="Allow event that same distence."></td>
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