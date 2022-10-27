<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
include_once(G5_LIB_PATH.'/thumbnail.lib.php');
$cfg = json_decode(file_get_contents("$board_skin_path/config.json", true), true);
include_once("$board_skin_path/its_module.php"); // Local Function List

?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

<link rel="stylesheet" href="<?php echo $board_skin_url?>/css/jquery-ui.css">
<script src="<?php echo $board_skin_url?>/js/jquery-ui.js"></script>

<style>
/* ECOS */
th { width:120px; background-color: silver; }
hr { border: none;margin-top: 4px;margin-bottom: 4px;clear: both; }
#bo_v_con { display:none; }
#bo_v_atc { padding: 0; min-height: 0; }
#bo_v_bot { clear: unset; }
.table { margin-bottom: 2px; }
.wr_content_tr { display:none; }
.f_right { float: right; margin: 0 2px; }

.w_hide { display:none; }
.w_detail_tr { background-color: #fff8e1; font-size: 8pt; }
.w_detail_tr th { background-color:gray; font-size: 10pt; color: white; }
.w_default_tr { background-color: #f0f0f0; font-size: 8pt; }
.w_default_tr th { background-color: #f0f0f0; font-size: 10pt; color: gray; }
.w_number_input	{ border:0; width: 60px; color:#808080; text-align: right; font-size: 8pt; padding-right: 4pt; margin-bottom: 4px; }
.btn_option_01 { text-align: right; padding: 4px 0; }
.pointer { cursor: pointer; }
.input75P { width: 75%; display: initial; float: left; margin:0; }
.input60P { width: 60%; display: initial; float: left; margin:0; }
.input50P { width: 50%; display: initial; float: left; margin:0; }
.input33P { width: 33%; display: initial; float: left; margin:0; }
.input25P { width: 25%; display: initial; float: left; margin:0; }
.input20P { width: 20%; display: initial; float: left; margin:0; }
.input16P { width: 15.5%; display: initial; float: left; margin:0; }
.input10P { width: 9.5%; display: initial; float: left; margin:0; }
</style>
	
<script type="text/javascript">
$(document).ready(function(){
	$('#btn_history').on('click', function(event) {        
		 $('#bo_v_con').toggle('show');
	});
	$('#btn_Schedule').click(function(){
		window.open("<?php echo G5_THEME_URL ?>/utility/scheduleBlock/index.php?bo_table=<?php echo $bo_table?>&wr_id=<?php echo $view['wr_id']?>&wr_subject=<?php echo $view['wr_subject']?>&w_device_serial=<?php echo $view['w_device_serial']?>","scheduleBlock_<?php echo $view['wr_id']?>", "width=600,height=500,scrollbars=no");
		return false;
	});
	$('#btn_Stream').click(function(){
		window.open("<?php echo $view['w_streaming_url'] ?>","Realtime_Zone_Stream", "width=640,height=360,scrollbars=no");
		return false;
	});
	$('#btn_Snapshot').click(function(){
		window.open("<?php echo G5_THEME_URL ?>/utility/filemanager/fm.php?ID=<?php echo $view['w_device_serial']?>&PATH=data||image||<?php echo $view['w_device_serial']?>", "File Manager", "width=640,height=400,scrollbars=no");
		return false;
	});
	$('#btn_Events').click(function(){
		var f = document.getElementById('TheForm');
		$("#TheForm").attr("action","<?php echo G5_CU_UTIL_URL ?>/systemExec/realtime_tail.php");
		$("#TheForm").attr("target","Event Log");
		$('#TheForm input[name="w_device_serial"]').val("<?php echo $view['w_device_serial']?>");
		$('#TheForm input[name="wr_subject"]').val("<?php echo $view['wr_subject']?>");
		window.open('', 'Event Log','width=600,height=400,scrollbars=no');
		f.submit();
		// window.open("<?php echo G5_CU_UTIL_URL ?>/systemExec/realtime_tail.php?w_device_serial=<?php echo $view['w_device_serial']?>&wr_subject=<?php echo $view['wr_subject']?>","Realtime_Log_<?php echo $view['w_device_serial']?>", "width=600,height=400,scrollbars=no");
		// return false;
	});
});
</script>

<script src="<?php echo G5_JS_URL; ?>/viewimageresize.js"></script>

<form id="TheForm" method="post" action="" target="">
<input type="hidden" name="w_device_serial" value="" />
<input type="hidden" name="wr_subject" value="" />
</form>

<!-- 게시물 읽기 시작 { -->
<div id="bo_v_table"><?php echo $board['bo_subject']; ?></div>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name "><?php echo $board['bo_subject'] ?><span class="sound_only"><?php echo $SK_BO_List[ITS_Lang]?></span></span>
            <hr>
            <span class="skills"></span>
        </div>
    </div>
</section>

<article id="bo_v" class="container">
    <div class="panel panel-success">
	<div class="its_version" style="float:left;color:silver;padding:4px 8px;font-size:8pt;"><?php echo get_w_program_info(G5_CU_PATH_GPIO)[0]; ?></div>
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
            <?php if ($prev_href) { ?><li><a href="<?php echo $prev_href ?>" class="previous"><span aria-hidden="true">&larr; </span> <?php echo $SK_BO_Previous[ITS_Lang]?></a></li><?php } ?>
            <?php if ($next_href) { ?><li><a href="<?php echo $next_href ?>" class="next"><?php echo $SK_BO_Next[ITS_Lang]?> <span aria-hidden="true"> &rarr;</span></a></li><?php } ?>
        </ul>
        <?php } ?>

        <ul class="bo_v_com">
            <?php if ($update_href) { ?><li><a href="<?php echo $update_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Modify[ITS_Lang]?></a></li><?php } ?>
			<?php if ($delete_href) { ?><li><a href="<?php echo $delete_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Delete[ITS_Lang]?></a></li><?php } ?>
            <?php if ($search_href) { ?><li><a href="<?php echo $search_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Search[ITS_Lang]?></a></li><?php } ?>
            <li><a href="<?php echo $list_href ?>" class="btn btn-sm btn-success"><?php echo $SK_BO_List[ITS_Lang]?></a></li>
            <?php /* if ($write_href) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_Write[ITS_Lang]?></a></li><?php } */ ?>
        </ul>
        <?php
        $link_buttons = ob_get_contents();
        ob_end_flush();
         ?>
    </div>
    <!-- } 게시물 상단 버튼 끝 -->

	<div>
        <input type="button" value="<?php echo $SK_BO_History[ITS_Lang]?>" id="btn_history" class="btn btn-info">
        <!-- input type="button" value="<?php echo $SK_BO_Schedule[ITS_Lang]?>" id="btn_Schedule" class="btn btn-success f_right" -->
        <?php if ($view['w_streaming_url']) { ?>
        <input type="button" value="<?php echo $SK_BO_Streaming[ITS_Lang]?>" id="btn_Stream" class="btn btn-success f_right">
		<?php } ?>
        <?php if ($view['w_snapshot_url']) { ?>
		<input type="button" value="<?php echo $SK_BO_Snapshot[ITS_Lang]?>" id="btn_Snapshot" class="btn btn-primary f_right">
		<?php } ?>
		<input type="button" value="<?php echo $SK_BO_Events[ITS_Lang]?>" id="btn_Events" class="btn btn-warning f_right">
        <input type="button" value="<?php echo $SK_BO_Monitor[ITS_Lang]?>" id="btn_Monitor" class="btn btn-danger f_right">
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
        <div id="bo_v_con"><pre style="font-size: 8pt;white-space: pre-wrap;"><?php echo $view['wr_content']; ?></pre></div>
        <?php//echo $view['rich_content']; // {이미지:0} 과 같은 코드를 사용할 경우 ?>
        <!-- } 본문 내용 끝 -->

    </section>
    <section id="bo_v_atc" class="col-md-10 col-md-offset-1">
		<table class="table table-bordered" style="width:49%; float:left;">
		<tbody>
		<tr>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Sensor_Name[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['wr_subject']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row" title="Sensor Model"><label for="w_device_id"><?php echo $SK_BO_Model_Name[ITS_Lang]?></label></th>
			<td>
				<?php echo ($cfg["model"][$view['w_device_model']]); ?>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered" style="width:49%; float:right;">
		<tbody>
		<tr>
			<th scope="row" title="USB Device ID"><label for="w_device_id"><?php echo $SK_BO_Device_Name[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['w_device_id']); ?>
			</td>
		</tr>
		<tr>
			<th scope="row" title="Sensor Serial"><label for="w_device_serial"><?php echo $SK_BO_Serial_Number[ITS_Lang]?></label></th>
			<td>
				<?php echo ($view['w_device_serial']); ?>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr class="w_hide">
			<th scope="row" title="ID"><label for="w_id">ITS ID</label></th>
			<td>
				<?php echo $view['w_id'] ?>
			</td>
		</tr>
		<tr class="w_hide">
			<th scope="row" title="ITS Serial"><label for="w_cpu_id">ITS Serial</label></th>
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
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_ims_address_P">IMS</label></th>
			<td><input type="text" name="w_ims_address_P" value="<?php echo $view['w_ims_address_P'] ?>" id="w_ims_address_P" class="form-control input50P" disabled placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_ims_port_P" value="<?php echo $view['w_ims_port_P'] ?>" id="w_ims_port_P" class="form-control input50P" disabled placeholder="Port Ex:50007" size="50">
			<hr>
			<input type="text" name="w_ims_address_S" value="<?php echo $view['w_ims_address_S'] ?>" id="w_ims_address_S" class="form-control input50P" disabled placeholder="IP Ex:121.165.208.119" size="50"><input type="text" name="w_ims_port_S" value="<?php echo $view['w_ims_port_S'] ?>" id="w_ims_port_S" class="form-control input50P" disabled placeholder="Port Ex:50007" size="50"></td>
		</tr>
		</tbody>
		</table>
		
		<table class="table table-bordered">
		<tbody>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_snapshot_url"><?php echo $SK_BO_Snapshot[ITS_Lang]?></label></th>
			<td>
			<input type="text" name="w_snapshot_url" value="<?php echo $view['w_snapshot_url'] ?>" id="w_snapshot_url" class="form-control input50P" disabled placeholder="URL Ex:http://121.165.208.119:8080/" size="50">
			<span class="input25P" style="padding: 0 15px;">
				<input type="text" name="w_snapshot_qty" value="<?php echo $view['w_snapshot_qty'] ?>" id="w_snapshot_qty" class="form-control input100P" readonly>
			</span>
			<span class="input25P" style="display:inline-block;text-align:center;height:20px;font-weight:unset;" >
				<input type="checkbox" class="form-control" style="float:none;height:20px;" name="w_snapshot_enc" id="w_snapshot_enc" value="1" <?php echo $view[w_snapshot_enc]?'checked':'';?> disabled title="w_snapshot_enc"><label><?php echo $SK_BO_Encryption[ITS_Lang]?></label>
			</span>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_streaming_url"><?php echo $SK_BO_Streaming[ITS_Lang]?></label></th>
			<td><input type="text" name="w_streaming_url" value="<?php echo $view['w_streaming_url'] ?>" id="w_streaming_url" class="form-control input75P" disabled placeholder="URL Ex:http://121.165.208.119:8080/" size="50">
			<span class="input25P" style="display:inline-block;text-align:center;height:20px;font-weight:unset;" ><input type="checkbox" class="form-control" style="float:none;height:20px;" name="w_streaming_enc" id="w_streaming_enc" value="1" <?php echo $view[w_streaming_enc]?'checked':'';?> disabled title="w_streaming_enc"><label><?php echo $SK_BO_Encryption[ITS_Lang]?></label></span></td>
		</tr>

		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alert_port"><?php echo $SK_BO_Alert[ITS_Lang]?></label></th>
			<td>
				<input type="text" name="w_alert_port" value="<?php echo $cfg["DEVICE_all"][$view['w_alert_port']] ?>" id="w_alert_port" class="form-control input50P" disabled placeholder="Due Time" size="50">
				<input type="text" name="w_alert_value" value="<?php echo $view['w_alert_value'] ?>" id="w_alert_value" class="form-control input50P" disabled placeholder="Due Time" size="50">
			</td>
		</tr>
		</tbody>
		</table>

		<table class="table table-bordered">
		<tbody>
			
		<?php include_once($board_skin_path.'/../w_include_custom/customView.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_custom/requestView.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_acu/acuView.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_audio/view_alarm_sound.php'); ?>

		<tr class="w_hide">
			<th scope="row" title="Time Stamp"><label for="w_keycode"><?php echo $SK_BO_Key[ITS_Lang]?></label></th>
			<td>
				<?php echo $view['w_keycode'] ?>
			</td>
		</tr>
		<tr class="hide">
			<th scope="row" title="Time Stamp"><label for="w_license"><?php echo $SK_BO_License[ITS_Lang]?></label></th>
			<td>
				<?php echo $view['w_license'] ?>
			</td>
		</tr>
		<tr class="hide">
			<th scope="row" title="Time Stamp"><label for="w_stamp"><?php echo $SK_BO_Created[ITS_Lang]?></label></th>
			<td>
				<?php echo $view['w_stamp'] ?>
			</td>
		</tr>
		</tbody>
		</table>
		<table class="table table-bordered">
		<tbody>
		<tr>
			<th class="w_hide" scope="row"><label for="w_sensor_disable"></label></th>
			<td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_disable" id="w_sensor_disable" value="1" <?php echo $view[w_sensor_disable]?'checked':'';?> disabled title="Permanently Disable Sensor"></td>
			<td class="w_hide"><?php echo $SK_BO_Apply[ITS_Lang]?><input type="checkbox" class="form-control" name="w_sensor_reload" id="w_sensor_reload" value="1" <?php echo $view[w_sensor_reload]?'checked':'';?> disabled title="Restart Sensor when catch first event after save this"></td>
			<td class="w_hide"><?php echo $SK_BO_Keep_Cycle[ITS_Lang]?><input type="checkbox" class="form-control" name="w_event_keepHole" id="w_event_keepHole" value="1"<?php echo $view[w_event_keepHole]?'checked':'';?> disabled title="Keep event hold cycle."></td>
		</tr>
		</tbody>
		</table>
    </section>

	<div style="float:left;margin-bottom:10px;clear:both;">
		<button type="button" id="btn_history" class="btn btn-success btn-sm" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/status/printCFG.php?&bo_table=<?php echo $bo_table?>&wr_id=<?php echo $view['wr_id']?>", "Print Config");'>Print Config</button>
	</div>
	
	<?php
	// 코멘트 입출력
	// include_once(G5_BBS_PATH.'/view_comment.php');
	?>

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