<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
include_once(G5_LIB_PATH.'/thumbnail.lib.php');
include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

<style>
#bo_v_con { display:none; }
#bo_v_atc { padding: 0; min-height: 0; }
</style>

<script type="text/javascript">
$(document).ready(function(){
	$('#btn_history').on('click', function(event) {        
		 $('#bo_v_con').toggle('show');
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
	<div class="its_version" style="float:left;color:silver;padding:4px 8px;font-size:8pt;"><?php echo get_w_program_info(G5_CU_CONF_GPCIO)[0]; ?></div>
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
        <!-- div id="bo_v_con"><?php // echo get_view_thumbnail($view['content']); ?></div -->
        <div id="bo_v_con"><pre style="font-size: 9pt;white-space: pre-wrap;"><?php echo $view['wr_content']; ?></pre></div>
        <?php//echo $view['rich_content']; // {이미지:0} 과 같은 코드를 사용할 경우 ?>
        <!-- } 본문 내용 끝 -->

    </section>
    <section id="bo_v_atc" class="">
	<table class="table table-bordered">
		<tbody>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="wr_subject"><?php echo $SK_BO_Name[ITS_Lang]?><br>Desc./Serial</label></th>
			<td>
				<input type="text" name="wr_subject" value="<?php echo $view['wr_subject'] ?>" id="wr_subject" readonly class="form-control input50P" size="50" maxlength="255">
                <input type="text" name="w_gpcio_desc" value="<?php echo $view['w_gpcio_desc'] ?>" id="w_gpcio_desc" readonly class="form-control input25P">
                <input type="text" name="w_sensor_serial" value="<?php echo $view['w_sensor_serial'] ?>" id="w_sensor_serial" readonly class="form-control input25P" >
			</td>
		</tr>
		<tr class='w_default_tr'>
			<th scope="row" title="Title"><label for="w_gpcio_desc">Port/Speed</label></th>
			<td>
                <div class="form-control input50P" style="text-align:center">
                    <span><?php if($view['w_gpcio_trigger_L']) echo '🡫'; else echo '🡩'; ?> <?php echo $relay_inputL[$view['w_gpcio_detect_L']] ?></span>
                    <span><?php echo $opject_direction[$view['w_gpcio_direction']] ?></span>
                    <span><?php echo $relay_inputR[$view['w_gpcio_detect_R']] ?> <?php if($view['w_gpcio_trigger_R']) echo '🡫'; else echo '🡩'; ?></span>
                </div>
                <div class="form-control input50P" style="text-align:center">
                    <span>Distance [ <?php echo $view['w_distance'] ?> ] cm, Min. Speed [ <?php echo $view['w_speed_L'] ?> ] km/h,  Max. Speed [ <?php echo $view['w_speed_H'] ?> ] km/h</span>
                </div>
                
			</td>
		</tr>
		<tr class='w_detail_tr'>
            <th scope="row"><label for="w_countIn">Count In<br>Out</label></th>
			<td>
                <div class="input25P inputCntGrp">
					<div class="dirName">D1:<input type="text" name="w_capacity_A" value="<?php echo $view['w_capacity_A'] ?>" id="w_capacity_A" class="form-control inputCap" disabled placeholder="D1" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_AX" value="<?php echo $view['w_direction_AX'] ?>" id="w_direction_AX" class="form-control input50P inputCnt" disabled placeholder="Count1 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_AX" id="w_internal_AX" value="1" <?php echo $view[w_internal_AX]?'checked':'';?> disabled >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_AX" id="w_external_AX" value="1" <?php echo $view[w_external_AX]?'checked':'';?> disabled >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XA" value="<?php echo $view['w_direction_XA'] ?>" id="w_direction_XA" class="form-control input50P inputCnt" disabled placeholder="Count1 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XA" id="w_internal_XA" value="1" <?php echo $view[w_internal_XA]?'checked':'';?> disabled >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XA" id="w_external_XA" value="1" <?php echo $view[w_external_XA]?'checked':'';?> disabled >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
				<div class="input25P inputCntGrp hide">
                    <div class="dirName">D2:<input type="text" name="w_capacity_B" value="<?php echo $view['w_capacity_B'] ?>" id="w_capacity_B" class="form-control inputCap" disabled placeholder="D2" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_BX" value="<?php echo $view['w_direction_BX'] ?>" id="w_direction_BX" class="form-control input50P inputCnt" disabled placeholder="Count2 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_BX" id="w_internal_BX" value="1" <?php echo $view[w_internal_BX]?'checked':'';?> disabled >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_BX" id="w_external_BX" value="1" <?php echo $view[w_external_BX]?'checked':'';?> disabled >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XB" value="<?php echo $view['w_direction_XB'] ?>" id="w_direction_XB" class="form-control input50P inputCnt" disabled placeholder="Count2 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XB" id="w_internal_XB" value="1" <?php echo $view[w_internal_XB]?'checked':'';?> disabled >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XB" id="w_external_XB" value="1" <?php echo $view[w_external_XB]?'checked':'';?> disabled >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
				<div class="input25P inputCntGrp hide">
                    <div class="dirName">D3:<input type="text" name="w_capacity_C" value="<?php echo $view['w_capacity_C'] ?>" id="w_capacity_C" class="form-control inputCap" disabled placeholder="D3" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_CX" value="<?php echo $view['w_direction_CX'] ?>" id="w_direction_CX" class="form-control input50P inputCnt" disabled placeholder="Count3 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_CX" id="w_internal_CX" value="1" <?php echo $view[w_internal_CX]?'checked':'';?> disabled >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_CX" id="w_external_CX" value="1" <?php echo $view[w_external_CX]?'checked':'';?> disabled >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XC" value="<?php echo $view['w_direction_XC'] ?>" id="w_direction_XC" class="form-control input50P inputCnt" disabled placeholder="Count3 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XC" id="w_internal_XC" value="1" <?php echo $view[w_internal_XC]?'checked':'';?> disabled >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XC" id="w_external_XC" value="1" <?php echo $view[w_external_XC]?'checked':'';?> disabled >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
				<div class="input25P inputCntGrp hide">
                    <div class="dirName">D4:<input type="text" name="w_capacity_D" value="<?php echo $view['w_capacity_D'] ?>" id="w_capacity_D" class="form-control inputCap" disabled placeholder="D4" size="50"></div>
					<div class="input100P inputCntIn">
						<input type="text" name="w_direction_DX" value="<?php echo $view['w_direction_DX'] ?>" id="w_direction_DX" class="form-control input50P inputCnt" disabled placeholder="Count4 In" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_DX" id="w_internal_DX" value="1" <?php echo $view[w_internal_DX]?'checked':'';?> disabled >
							<label class="inputLbIn">Internal IN</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_DX" id="w_external_DX" value="1" <?php echo $view[w_external_DX]?'checked':'';?> disabled >
							<label class="inputLbIn">External IN</label>
						</div>
					</div>
					<div class="input100P inputCntOut">
						<input type="text" name="w_direction_XD" value="<?php echo $view['w_direction_XD'] ?>" id="w_direction_XD" class="form-control input50P inputCnt" disabled placeholder="Count4 Out" size="50">
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_internal_XD" id="w_internal_XD" value="1" <?php echo $view[w_internal_XD]?'checked':'';?> disabled >
							<label class="inputLbOut">Internal OUT</label>
						</div>
						<div class="input50P inputLbGrp">
							<input type="checkbox" name="w_external_XD" id="w_external_XD" value="1" <?php echo $view[w_external_XD]?'checked':'';?> disabled >
							<label class="inputLbOut">External OUT</label>
						</div>
					</div>
				</div>
			</td>
		</tr>

		<tr class="w_detail_tr">
			<th scope="row"><label for="w_alert_Port">Relay Out/Time</label></th>
			<td>
				<input type="text" name="w_alert_Port" value="<?php echo $relay_alert[$view['w_alert_Port']] ?>" id="w_alert_Port" readonly class="form-control input25P">
				<input type="text" name="w_alert_Value" value="<?php echo $view['w_alert_Value'] ?>" id="w_alert_Value" readonly class="form-control input25P">
                <span style="display:inline-grid;padding: 0 10px;vertical-align: top;"><label style="color:crimson;margin: unset;">Security</label><input type="checkbox" class="form-control" name="w_security_mode" id="w_security_mode" value="1" <?php echo $view[w_security_mode]?'checked':'';?> disabled ></span>
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_host_Addr">HOST IP/Port<br>for IMS</label></th>
			<td>
			<input type="text" name="w_host_Addr1" value="<?php echo $view['w_host_Addr1'] ?>" id="w_host_Addr1" readonly class="form-control input25P">
			<input type="text" name="w_host_Port1" value="<?php echo $view['w_host_Port1'] ?>" id="w_host_Port1" readonly class="form-control input25P">
			<input type="text" name="w_host_Addr2" value="<?php echo $view['w_host_Addr2'] ?>" id="w_host_Addr2" readonly class="form-control input25P">
			<input type="text" name="w_host_Port2" value="<?php echo $view['w_host_Port2'] ?>" id="w_host_Port2" readonly class="form-control input25P">
			</td>
		</tr>

		<?php include_once($board_skin_path.'/../w_include_custom/customView.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_custom/requestView.php'); ?>
		<?php include_once($board_skin_path.'/../w_include_audio/view_alarm_sound.php'); ?>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_keycode">Key/License</label></th>
			<td>
			<input type="text" name="w_keycode" value="<?php echo $view['w_keycode'] ?>" id="w_keycode" readonly class="form-control input50P">
			<input type="text" name="w_license" value="<?php echo $view['w_license'] ?>" id="w_license" readonly class="form-control input50P">
			</td>
		</tr>
		<tr class="w_detail_tr">
			<th scope="row"><label for="w_stamp">Last Modified</label></th>
			<td><input type="text" name="w_stamp" value="<?php echo get_w_stamp($view['w_stamp']) ?>" id="w_stamp" readonly class="form-control"></td>
		</tr>
		</tbody>
	</table>
    <table class="table table-bordered">
            <tbody>
            <tr class='w_default_tr'>
                <th class="w_hide" scope="row"><label for="w_gpcio_disable"></label></th>
                <td><?php echo $SK_BO_Disable[ITS_Lang]?><input type="checkbox" class="form-control" name="w_gpcio_disable" id="w_gpcio_disable" value="1" <?php echo $view[w_gpcio_disable]?'checked':'';?> disabled title="Permanently Disable GPCIO"></td>
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