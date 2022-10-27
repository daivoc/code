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

$string = $bo_table."_".$_SERVER['SERVER_ADDR']."_".str_pad($wr_id, 4, "0", STR_PAD_LEFT);
$w_sensor_serial =  preg_replace('/[^A-Za-z0-9_]/', '_', $string); // Removes special chars.

$w_nvr_log_level = 5;
$w_nvr_target_dir = '/var/www/html/its_web/data/image/giken_' . $w_sensor_serial;
// $w_nvr_netcam_url = 'http://'.$w_nvr_camera_ip.'/cgi-bin/trace.cgi';
$w_nvr_stream_port = 8090 + $wr_id;
$w_nvr_threshold = 1000;
$w_nvr_text_left = $wr_subject;
$w_nvr_text_changes = 1;
$w_nvr_stream_localhost = 0;
$w_nvr_text_double = 0;
$w_nvr_width = 640;
$w_nvr_height = 480;
$w_nvr_framerate = 100;

$sqlNVR = "UPDATE $write_table 
SET 
w_nvr_motion = '$w_nvr_motion', 
w_nvr_camera_ip = '$w_nvr_camera_ip', 
w_nvr_log_level = '$w_nvr_log_level', 
w_nvr_target_dir = '$w_nvr_target_dir', 
w_nvr_netcam_url = '$w_nvr_netcam_url', 
w_nvr_stream_port = '$w_nvr_stream_port', 
w_nvr_netcam_userpass = '$w_nvr_netcam_userpass', 
w_nvr_threshold = '$w_nvr_threshold', 
w_nvr_text_left = '$w_nvr_text_left', 
w_nvr_text_changes = '$w_nvr_text_changes', 
w_nvr_stream_localhost = '$w_nvr_stream_localhost', 
w_nvr_text_double = '$w_nvr_text_double', 
w_nvr_width = '$w_nvr_width', 
w_nvr_height = '$w_nvr_height', 
w_nvr_framerate = '$w_nvr_framerate'
WHERE wr_id = '$wr_id' ";
$result = sql_query($sqlNVR);
?>
