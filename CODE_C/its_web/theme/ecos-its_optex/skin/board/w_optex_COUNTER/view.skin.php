<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
include_once(G5_LIB_PATH.'/thumbnail.lib.php');
include_once("$board_skin_path/config_sensor.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

<link rel="stylesheet" href="<?php echo $board_skin_url?>/css/jquery-ui.css">
<script src="<?php echo $board_skin_url?>/js/jquery-ui.js"></script>

<style>
#bo_v_con { display:none; }
#bo_v_atc { padding: 0; min-height: 0; }
</style>
<style>
th { width:120px; }
.wr_content_tr { display:none; }
.w_hide { display:none; }
.w_detail_tr { background-color: #fff8e1; font-size: 8pt; }
.w_detail_tr th { background-color: white; }
.w_default_tr { background-color: #f0f0f0; font-size: 8pt; }
.w_default_tr th { background-color: white; }
.w_number_input	{ border:0; width: 60px; color:#808080; text-align: right; font-size: 8pt; padding-right: 4pt; margin-bottom: 4px; }

.f_right { float: right; margin: 0 2px; }
.btn_option_01 { text-align: right; padding: 4px 0; }
.input50P { width: 50%; display: initial; }

#select_w_sensor_ignoreZone .ui-selecting { background: #FECA40; }
#select_w_sensor_ignoreZone .ui-selected { background: #ffc107; color: white; }
#select_w_sensor_ignoreZone { list-style-type: none; margin: 0; padding: 0; width: 100%; }
#select_w_sensor_ignoreZone li { margin: 1px; padding: 1px; float: left; width: 16px; height: 22px; font-size: 6pt; text-align: center; }
#select_w_sensor_scheduleZone .ui-selecting { background: #FECA40; }
#select_w_sensor_scheduleZone .ui-selected { background: #ffc107; color: white; }
#select_w_sensor_scheduleZone { list-style-type: none; margin: 0; padding: 0; width: 100%; }
#select_w_sensor_scheduleZone li { margin: 1px; padding: 1px; float: left; width: 16px; height: 22px; font-size: 6pt; text-align: center; }
</style>
	
<script type="text/javascript">
$(document).ready(function(){
	$('#btn_history').on('click', function(event) {        
		 $('#bo_v_con').toggle('show');
	});
	$('#btn_Schedule').click(function(){
		window.open("<?php echo G5_THEME_URL ?>/utility/scheduleBlock/index.php?bo_table=<?php echo $bo_table?>&wr_id=<?php echo $view['wr_id']?>&wr_subject=<?php echo $view['wr_subject']?>&w_sensor_serial=<?php echo $view['w_sensor_serial']?>","scheduleBlock_<?php echo $view['wr_id']?>", "width=600,height=500,scrollbars=no");
		return false;
	});
	$('#btn_Snapshot').click(function(){
		window.open("<?php echo G5_CU_UTIL_URL ?>/ecosFileTree/snapshotView.php?ID=<?php echo $view['w_sensor_serial']?>&wr_subject=<?php echo $view['wr_subject']?>","Shot_Tree_<?php echo $view['w_sensor_serial']?>", "width=800,height=400,scrollbars=no");
		return false;
	});
	$('#btn_Position').click(function(){
		window.open("<?php echo G5_THEME_URL ?>/utility/status/mapsInfo.php?myLatS=<?php echo $view['w_sensor_lat_s']?>&myLngS=<?php echo $view['w_sensor_lng_s']?>&myLatE=<?php echo $view['w_sensor_lat_e']?>&myLngE=<?php echo $view['w_sensor_lng_e']?>&wr_subject=<?php echo $view['wr_subject']?>","mapsLocation", "width=600,height=400,scrollbars=no");
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
		// window.open("<?php echo G5_CU_UTIL_URL ?>/systemExec/realtime_tail.php?w_sensor_serial=<?php echo $view['w_sensor_serial']?>&wr_subject=<?php echo $view['wr_subject']?>","Realtime_Log_<?php echo $view['w_sensor_serial']?>", "width=600,height=400,scrollbars=no");
		// return false;
	});
	$('#btn_Monitor').click(function(){
		window.open("http://<?php echo $_SERVER["SERVER_NAME"].":".($view['w_table_PortOut']) ?>","Realtime_Zone_<?php echo $view['w_sensor_serial']?>", "width=230,height=500,scrollbars=no");
		return false;
	});
});
</script>

<script src="<?php echo G5_JS_URL; ?>/viewimageresize.js"></script>

<form id="TheForm" method="post" action="" target="">
<input type="hidden" name="w_sensor_serial" value="" />
<input type="hidden" name="wr_subject" value="" />
</form>
<!-- 게시물 읽기 시작 { -->
<div id="bo_v_table"><?php echo $board['bo_subject']; ?></div>

<article id="bo_v" class="container">
    <div class="panel panel-success">
	<div class="its_version" style="float:left;color:silver;padding:4px 8px;font-size:8pt;"><?php echo get_w_program_info(G5_CU_PATH_COUNTER)[0]; ?></div>
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
            <?php if ($prev_href) { ?><li><a href="<?php echo $prev_href ?>" class="previous"><span aria-hidden="true">&larr; </span> previous</a></li><?php } ?>
            <?php if ($next_href) { ?><li><a href="<?php echo $next_href ?>" class="next">next <span aria-hidden="true"> &rarr;</span></a></li><?php } ?>
        </ul>
        <?php } ?>

        <ul class="bo_v_com">
            <?php if ($update_href) { ?><li><a href="<?php echo $update_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Modify[ITS_Lang]?></a></li><?php } ?>
            <?php if ($delete_href) { ?><li><a href="<?php echo $delete_href ?>" class="btn btn-sm btn-primary" onclick="del(this.href); return false;"><?php echo $SK_BO_Delete[ITS_Lang]?></a></li><?php } ?>
            <?php if ($search_href) { ?><li><a href="<?php echo $search_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Search[ITS_Lang]?></a></li><?php } ?>
            <li><a href="<?php echo $list_href ?>" class="btn btn-sm btn-success"><?php echo $SK_BO_List[ITS_Lang]?></a></li>
            <?php /* if ($write_href) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary">글쓰기</a></li><?php } */ ?>
        </ul>
        <?php
        $link_buttons = ob_get_contents();
        ob_end_flush();
         ?>
    </div>
    <!-- } 게시물 상단 버튼 끝 -->

	<div>
        <input type="button" value="Log" id="btn_history" class="btn btn-info">
        <input type="button" value="Schedule" id="btn_Schedule" class="btn btn-success f_right">
		<?php /*
        <input type="button" value="Snapshot" id="btn_Snapshot" class="btn btn-primary f_right">
 		*/ ?>
        <input type="button" value="Position" id="btn_Position" class="btn btn-info f_right">
		<?php /*
        <input type="button" value="serverCommand" id="btn_Restart" class="btn btn-primary f_right" onclick="serverCommand()">
 		*/ ?>
       <input type="button" value="Events" id="btn_Events" class="btn btn-warning f_right">
        <input type="button" value="Monitor" id="btn_Monitor" class="btn btn-danger f_right">
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
        <!-- div id="bo_v_con"><?php echo get_view_thumbnail($view['content']); ?></div -->
        <div id="bo_v_con"><pre style="height:100px;font-size: 8pt;"><?php echo $view['wr_content']; ?></pre></div>
        <?php//echo $view['rich_content']; // {이미지:0} 과 같은 코드를 사용할 경우 ?>
        <!-- } 본문 내용 끝 -->

    </section>

    <section id="bo_v_atc" class="col-md-10 col-md-offset-1">
		<table class="table table-bordered">
		<tbody>
		<tr>
			<th class="w_hide" scope="row"><label for="w_sensor_disable"></label></th>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_disable" id="w_sensor_disable" value="1" <?php echo $view[w_sensor_disable]?'checked':'';?> disabled title="Permanently Disable Sensor"></td>
			<td><?php echo $SK_BO_Pause[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_stop" id="w_sensor_stop" value="1" <?php echo $view[w_sensor_stop]?'checked':'';?> disabled title="Temporary Disable Sensor(keep log)"></td>
			<td><?php echo $SK_BO_Log[ITS_Lang]?><input type="checkbox" class="form-control" name="w_alarm_disable" id="w_alarm_disable" value="1" <?php echo $view[w_alarm_disable]?'checked':'';?> disabled title="Do not send valid event to host."></td>
			<td><?php echo $SK_BO_Apply[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_reload" id="w_sensor_reload" value="1" <?php echo $view[w_sensor_reload]?'checked':'';?> disabled title="Restart Sensor when catch first event after save this"></td>
			<td class="w_default_tr">동일신호<input type="checkbox" class="form-control" name="w_event_keepHole" id="w_event_keepHole" value="1"<?php echo $view[w_event_keepHole]?'checked':'';?> disabled title="Keep event hold cycle."></td>
			<td class="w_default_tr">거리보정<input type="checkbox" class="form-control" name="w_event_syncDist" id="w_event_syncDist" value="1" <?php echo $view[w_event_syncDist]?'checked':'';?> disabled title="Allow event that same distence."></td>
			<td class="w_default_tr">일방통행<input type="checkbox" class="form-control" name="w_sensor_noOfZone" id="w_sensor_noOfZone" value="1" <?php echo $view[w_sensor_noOfZone]?'checked':'';?> disabled title="Oneway."></td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Sensor_Name[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['wr_subject']); ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="USB Device ID"><label for="w_device_id"><?php echo $SK_BO_Model_Name[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['w_sensor_model']); ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="USB Device ID"><label for="w_device_id"><?php echo $SK_BO_Device_Name[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['w_device_id']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row" title="Sensor Serial #"><label for="w_sensor_serial"><?php echo $SK_BO_Serial_Number[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['w_sensor_serial']); ?>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class="w_default_tr">
			<th scope="row" title="Accept Range"><label for="w_sensor_ignore"><?php echo $SK_BO_Detect_Range[ITS_Lang]?></label></th>
			<td>
				<span id="w_sensor_ignoreSDisp">최소<?php echo round($view['w_sensor_ignoreS'] / 10, 2) ?></span>에서 <span id="w_sensor_ignoreEDisp"><?php echo round($view['w_sensor_ignoreE'] / 10, 2) ?>까지</span> <?php echo $SK_BO_Cmeter[ITS_Lang]?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Ignore Zone"><label for="w_sensor_ignoreZone">지역차단</label></th>
			<td>
				<?php echo select_w_sensor_ignoreZone($view['w_sensor_ignoreZone'], $MAX_numberOfZone); ?>
			</td>
		</tr>
		<tr class="w_default_tr">
			<th scope="row" title="Limit Due(Sec)"><label for="w_sensor_schedule">유효범위</label></th>
			<td>
				<span id="w_sensor_scheduleSDisp">최소<?php echo round($view['w_sensor_scheduleS'] / 10, 2) ?></span>에서 <span id="w_sensor_scheduleEDisp"><?php echo round($view['w_sensor_scheduleE'] / 10, 2) ?>까지</span> <?php echo $SK_BO_Cmeter[ITS_Lang]?>
			</td>
		</tr>
		<tr class="w_default_tr">
			<th scope="row" title="Pickup Cycle"><label for="w_event_pickTime">재요청주기</label></th>
			<td>
				<span id="w_event_pickTimeDisp"><?php echo $view['w_event_pickTime'] ?></span> <?php echo $SK_BO_Second[ITS_Lang]?> (정상적인 이밴트가 종료된 직후 재 감지 직전 대기 시간 - 정상 이밴트 직후에만 적용)
			</td>
		</tr>
		<tr class="w_default_tr">
			<th scope="row" title="Hold Time Out"><label for="w_event_holdTime">사용자대기</label></th>
			<td>
				<span id="w_event_holdTimeDisp"><?php echo $view['w_event_holdTime'] ?></span> <?php echo $SK_BO_Second[ITS_Lang]?> (센서의 특성이나 사물의 크기에 따라 필요한 시간제한 - 모든 반복에 적용 )
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Alarm Level"><label for="w_alarm_level"><?php echo $SK_BO_Sensitivity[ITS_Lang]?></label></th>
			<td>
				<?php echo select_w_alarm_level($view['w_alarm_level'], 1); ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Latitude S"><label for="w_sensor_lat_s"><?php echo $SK_BO_Start_Coord[ITS_Lang]?></label></th>
			<td><?php echo $view['w_sensor_lat_s'] ?> - <?php echo $view['w_sensor_lng_s'] ?></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Latitude E"><label for="w_sensor_lat_e"><?php echo $SK_BO_End_Coord[ITS_Lang]?></label></th>
			<td><?php echo $view['w_sensor_lat_e'] ?> - <?php echo $view['w_sensor_lng_e'] ?></td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Accept Range"><label for="w_sensor_scheduleZone"><?php echo $SK_BO_Reservation[ITS_Lang]?></label></th>
			<td>
				<span id="w_sensor_scheduleSDisp"><?php echo round($view['w_sensor_scheduleS'] / 1000, 2) ?></span> ~ <span id="w_sensor_scheduleEDisp"><?php echo round($view['w_sensor_scheduleE'] / 1000, 2) ?></span> <?php echo $SK_BO_Meter[ITS_Lang]?>
				<?php echo select_w_sensor_scheduleZone($view['w_sensor_scheduleZone'], $MAX_numberOfZone); ?>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class="w_hide">
			<th scope="row" title="Sensor Face"><label for="w_sensor_face"><?php echo $SK_BO_Sensor_Face[ITS_Lang]?></label></th>
			<td>
				<?php echo select_w_sensor_face($view['w_sensor_face'], 1); ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="Sensor Angle"><label for="w_sensor_angle"><?php echo $SK_BO_Sensor_Azimuth[ITS_Lang]?></label></th>
			<td>
				<span id="w_sensor_angleDisp"><?php echo $view['w_sensor_angle'] ?></span> <?php echo $SK_BO_Angle[ITS_Lang]?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ID"><label for="w_id">ITS ID</label></th>
			<td>
				<?php echo $view['w_id'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="CPU ID"><label for="w_cpu_id">CPU ID</label></th>
			<td>
				<?php echo ($view['w_cpu_id']); ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS IP"><label for="w_system_ip">ITS IP</label></th>
			<td>
				<?php echo $view['w_system_ip'] ?> : <?php echo $view['w_system_port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS IP"><label for="w_system_ip">ITS BF IP</label></th>
			<td>
				<?php echo $view['w_systemBF_ip'] ?> : <?php echo $view['w_systemBF_port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS IP"><label for="w_system_ip">ITS AF IP</label></th>
			<td>
				<?php echo $view['w_systemAF_ip'] ?> : <?php echo $view['w_systemAF_port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_master_Addr">Master</label></th>
			<td>
				<?php echo $view['w_master_Addr'] ?> : <?php echo $view['w_master_Port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_master_Addr">Virtual</label></th>
			<td>
				<?php echo $view['w_virtual_Addr'] ?> : <?php echo $view['w_virtual_Port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_master_Addr">Sensor</label></th>
			<td>
				<?php echo $view['w_sensor_Addr'] ?> : <?php echo $view['w_sensor_Port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_email">Email</label></th>
			<td>
				<?php echo $view['w_email_Addr'] ?> : <?php echo $view['w_email_Time'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_tablePort">TablePort</label></th>
			<td>
				<?php echo $view['w_table_PortIn'] ?> : <?php echo $view['w_table_PortOut'] ?>
			</td>
		</tr>
		
		<tr class="<?php echo ($view['w_host_Addr'])?"w_detail_tr":"w_hide" ?>">
			<th scope="row"><label for="w_host_Addr">Host</label></th>
			<td>
				<?php echo $view['w_host_Addr'] ?> : <?php echo $view['w_host_Port'] ?>
			</td>
		</tr>
		<tr class="<?php echo ($view['w_host_Addr2'])?"w_detail_tr":"w_hide" ?>">
			<th scope="row"><label for="w_host_Addr2">Host2</label></th>
			<td>
				<?php echo $view['w_host_Addr2'] ?> : <?php echo $view['w_host_Port2'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_tcp_Addr">Tcp</label></th>
			<td>
				<?php echo $view['w_tcp_Addr'] ?> : <?php echo $view['w_tcp_Port'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_tcp_Addr2">Tcp2</label></th>
			<td>
				<?php echo $view['w_tcp_Addr2'] ?> : <?php echo $view['w_tcp_Port2'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_url1">Snapshot</label></th>
			<td>
				<?php echo $view['w_url1'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_url2">Streaming</label></th>
			<td>
				<?php echo $view['w_url2'] ?>
			</td>
		</tr>
		<tr class="<?php echo ($view['w_alert_Port'])?"w_detail_tr":"w_hide" ?>">
			<th scope="row"><label for="w_alert">Alert</label></th>
			<td>
				<?php echo $view['w_alert_Port'] ?> : <?php echo $view['w_alert_Value'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row"><label for="w_alert">Alert2</label></th>
			<td>
				<?php echo $view['w_alert2_Port'] ?> : <?php echo $view['w_alert2_Value'] ?>
			</td>
		</tr>
		<tr class="<?php echo ($view['w_keycode'])?"w_detail_tr":"w_hide" ?>">
			<th scope="row" title="Time Stamp"><label for="w_keycode">Key</label></th>
			<td>
				<?php echo $view['w_keycode'] ?>
			</td>
		</tr>
		<tr class="<?php echo ($view['w_license'])?"w_detail_tr":"w_hide" ?>">
			<th scope="row" title="Time Stamp"><label for="w_keycode">License</label></th>
			<td>
				<?php echo $view['w_license'] ?>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row" title="Time Stamp"><label for="w_stamp">Created</label></th>
			<td>
				<?php echo $view['w_stamp'] ?>
			</td>
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