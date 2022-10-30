<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php 
/*
$ cat /etc/motion/giken.conf
# Level of log messages [1..9] (EMG, ALR, CRT, ERR, WRN, NTC, INF, DBG, ALL). (default: 6 / NTC)
log_level 5
# 사진 및 영상의 대상 기본 디렉토리, 절대 경로 (기본값 : 현재 작업 디렉토리)
target_dir /var/www/html/its_web/data/cctv
# stream_port 포트를 통한 접근 (기본값 : 0 = 사용 안함)
stream_port 8090
# 텍스트는 왼쪽 아래 모서리에 배치됩니다
text_left GIKEN
# Full Network Camera URL. Valid Services: http:// ftp:// mjpg:// rtsp:// mjpeg:// file:// rtmp://
netcam_url http://192.168.0.249/cgi-bin/trace.cgi
# 필요한 경우(Option) 네트워크 카메라의 사용자 이름과 비밀번호. 구문은 user:password
netcam_userpass admin:admin
# off : HTTP / 1.0을 사용한 히스토리 구현. 각 http 요청 후 소켓을 닫습니다.
# force : 연결 유지 헤더와 함께 HTTP / 1.0 요청을 사용하여 동일한 연결을 재사용하십시오.
# on : 기본 상태로 유지를 지원하는 HTTP / 1.1 요청을 사용하십시오.
netcam_keepalive off
# 모션 감지를 트리거하는 이미지에서 변경된 픽셀 수에 대한 임계 값 (기본값 : 1500)
threshold 1000
# 이미지에서 변경된 픽스 수 표시 (기본값 : off), 텍스트는 오른쪽 상단에 있습니다
text_changes on
# 로컬 호스트로만 스트림 연결을 제한합니다 (기본값 : on)
stream_localhost off
# 이미지에 보통 크기의 두 배로 문자를 표시.
text_double off
# Image width (pixels). Valid range: Camera dependent, default: 352
width 640
# Image height (pixels). Valid range: Camera dependent, default: 288
height 480
# Maximum number of frames to be captured per second. Valid range: 2-100. Default: 100 (almost no limit).
framerate 5
*/

// 필드 존재여부에 따라 세롭개 생성 {
$sqlNVR = " SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '".G5_MYSQL_DB."' AND TABLE_NAME = '".$write_table."' AND COLUMN_NAME = 'w_nvr_motion' ";
$exeQuery = sql_query($sqlNVR);
if(sql_num_rows($exeQuery)) {
	; // 테이블 내에 필드가 존재한다.
} else { // 필드가 없으면 생성 한다.
	$sqlNVR = " ALTER TABLE  `$write_table` 
ADD `w_nvr_motion` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_nvr_camera_ip` varchar(128) DEFAULT NULL,
ADD `w_nvr_log_level` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_nvr_target_dir` varchar(128) DEFAULT NULL,
ADD `w_nvr_netcam_url` varchar(128) DEFAULT NULL,
ADD `w_nvr_stream_port` int(11) NOT NULL DEFAULT '0',
ADD `w_nvr_netcam_userpass` varchar(64) DEFAULT NULL,
ADD `w_nvr_threshold` int(11) NOT NULL DEFAULT '0',
ADD `w_nvr_text_left` varchar(32) DEFAULT NULL,
ADD `w_nvr_text_changes` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_nvr_stream_localhost` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_nvr_text_double` tinyint(1) NOT NULL DEFAULT '0',
ADD `w_nvr_width` int(11) NOT NULL DEFAULT '0',
ADD `w_nvr_height` int(11) NOT NULL DEFAULT '0',
ADD `w_nvr_framerate` int(11) NOT NULL DEFAULT '0' ";
sql_query($sqlNVR, false);

}
?>

<?php
// $nvrZoneID = array( // Alert
//     0 => 'All Zone',
//     1 => 'Zone 01',
//     2 => 'Zone 02',
//     3 => 'Zone 03',
//     4 => 'Zone 04'
// );

// function select_w_Zone($nvrZone, $nvrZoneID) {
// 	$select_Zone = '<select class="form-control nvrGroup" id="nvrZone" >';
// 	while (list($key, $value) = each($nvrZoneID)) { 
// 		if($nvrZone == $key) {
// 			$select_Zone .='<option selected value="'.$key.'">'.$value.'</option>';
// 		} else {
// 			$select_Zone .='<option value="'.$key.'">'.$value.'</option>';
// 		}
// 	} 
// 	$select_Zone .= '</select>';
// 	return $select_Zone;
// }

// $itsOutID = array( // Alert
// 	18 => 'Relay 01',
// 	23 => 'Relay 02',
// 	24 => 'Relay 03',
// 	25 => 'Relay 04'
// );

$nvrLogLevel = array( // Alert
	 1 => 'Log Level 1',
	 2 => 'Log Level 2',
	 3 => 'Log Level 3',
	 4 => 'Log Level 4',
	 5 => 'Log Level 5',
	 6 => 'Log Level 6',
	 7 => 'Log Level 7',
	 8 => 'Log Level 8',
	 9 => 'Log Level 9'
);

function select_log_level($w_nvr_log_level, $nvrLogLevel) {
	$select_log_level = '<select class="form-control nvrGroup" id="w_nvr_log_level" ><option value="" disabled selected>Log Level</option>';
	while (list($key, $value) = each($nvrLogLevel)) { 
		if($w_nvr_log_level == $key) {
			$select_log_level .='<option selected value="'.$key.'">'.$value.'</option>';
		} else {
			$select_log_level .='<option value="'.$key.'">'.$value.'</option>';
		}
	} 
	$select_log_level .= '</select>';
	return $select_log_level;
}

?>

<style>
.nvrGroup { float:left; display: grid; margin:0;}
#nvrIP { width:25%; }
#nvrPort, #nvrTime { text-align: right;width: 10%; }
#nvrID, #nvrZone { text-align: right;width: 15%; }
#nvrEncryption { margin-left: 6px; width:20px;height:20px; }
.nvrEncry { width: 10%; }
</style>


<script>
$(document).ready(function(){
	// $('.nvrGroup').change(function(){
    //     if ($('#nvrEncryption').is(":checked")) { 
    //         var nvrEncryption = 1;
    //     } else {
    //         var nvrEncryption = 0;
    //     }
    //     var nvrValue = $('#nvrIP').val() + '||' + $('#nvrPort').val() + '||' + $('#nvrID').val() + '||' + $('#nvrZone').val() + '||' + $('#nvrTime').val() + '||' + nvrEncryption;
    //     if ($('#nvrIP').val() && $('#nvrPort').val() && $('#nvrID').val() && $('#nvrZone').val() && parseFloat($('#nvrTime').val())) {
    //         $('#wr_10').val(nvrValue);
    //     } else {
    //         $('#wr_10').val('');
    //     }
	// })	
});
</script>

<table class="table table-bordered">
<tbody>
<tr class="w_detail_tr">
	<th scope="row"><label for="NVR_Setup">CAMERA Info.</label></th>
	<td><?php // print $sqlNVR; ?>
        <input type='text' required class="form-control nvrGroup required" name='w_nvr_camera_ip' value='<?php if ($write['w_nvr_camera_ip']) echo $write['w_nvr_camera_ip']; else echo "192.168.0.249"; ?>' id='w_nvr_camera_ip' placeholder='w_nvr_camera_ip'>
		<input type='text' required class="form-control nvrGroup required" name='w_nvr_netcam_url' value='<?php if ($write['w_nvr_netcam_url']) echo $write['w_nvr_netcam_url']; else echo "/cgi-bin/trace.cgi"; ?>' id='w_nvr_netcam_url' placeholder='/cgi-bin/trace.cgi'>
	</td>
</tr>

<tr class="w_detail_tr">
	<th scope="row"><label for="NVR_Setup">NVR Setup</label></th>
	<td><?php // print $sqlNVR; ?>
		<span class='nvrGroup'>
        <input type="checkbox" class="form-control nvrGroup" name='w_nvr_motion' value="1" <?php echo $write[w_nvr_motion]?'checked':'';?> id="w_nvr_motion"><label>NVR</label>
        </span>
        <?php // echo select_log_level($write['w_nvr_log_level'], $nvrLogLevel); ?>

        <input type='text' class="form-control nvrGroup" name='w_nvr_threshold' value='<?php echo $write['w_nvr_threshold'] ?>' id='w_nvr_threshold' placeholder='w_nvr_threshold'>
        <input type='text' class="form-control nvrGroup" name='w_nvr_netcam_userpass' value='<?php echo $write['w_nvr_netcam_userpass'] ?>' id='w_nvr_netcam_userpass' placeholder='user:password'>
        <input type='hidden' class="form-control nvrGroup" name='w_nvr_width' value='<?php echo $write['w_nvr_width'] ?>' id='w_nvr_width' placeholder='w_nvr_width'>
        <input type='hidden' class="form-control nvrGroup" name='w_nvr_height' value='<?php echo $write['w_nvr_height'] ?>' id='w_nvr_height' placeholder='w_nvr_height'>
	</td>
</tr>
</tbody>
</table>