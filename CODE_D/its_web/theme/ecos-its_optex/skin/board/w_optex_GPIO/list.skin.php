<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

$cfg = json_decode(file_get_contents("$board_skin_path/config.json", true), true);
include_once("$board_skin_path/its_module.php"); // Local Function List
// 선택옵션으로 인해 셀합치기가 가변적으로 변함
$colspan = 15;
// $is_checkbox = 1;
if ($is_checkbox) $colspan++;
if ($is_good) $colspan++;
if ($is_nogood) $colspan++;

// add_stylesheet('css 구문', 출력순서); 숫자가 작을 수록 먼저 출력됨
add_stylesheet('<link rel="stylesheet" href="'.$board_skin_url.'/style.css">', 0);
?>
<script>
$(document).ready(function(){
	$('.btn_Events').click(function(){
		var f = document.getElementById('TheForm');
		$('#TheForm input[name="w_sensor_serial"]').val("");
		$('#TheForm input[name="wr_subject"]').val("");
		$("#TheForm").attr("action","<?php echo G5_CU_UTIL_URL ?>/systemExec/realtime_tail.php");
		$("#TheForm").attr("target","Event Log");
		$('#TheForm input[name="w_sensor_serial"]').val($(this).data("serial"));
		$('#TheForm input[name="wr_subject"]').val($(this).data("subject"));
		window.open('', 'Event Log','width=600,height=400,scrollbars=no');
		f.submit();
	});
});
</script>

<form id="TheForm" method="post" action="" target="">
<input type="hidden" name="w_sensor_serial" value="" />
<input type="hidden" name="wr_subject" value="" />
</form>

<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name "><?php echo $board['bo_subject'] ?><span class="sound_only"><?php echo $SK_BO_List[ITS_Lang]?></span></span>
            <hr>
            <span class="skills"></span>
        </div>
    </div>
</section>

<!-- 게시판 목록 시작 { -->
<section id="bo_list" class="container">

	<!-- 게시판 카테고리 시작 { -->
	<?php if ($is_category) { ?>
	<nav id="bo_cate">
		<h2><?php echo $board['bo_subject'] ?> 카테고리</h2>
		<ul id="bo_cate_ul" class="nav nav-pills">
			<?php echo $category_option ?>
		</ul>
	</nav>
	<?php } ?>
	<!-- } 게시판 카테고리 끝 -->

	<!-- 게시판 페이지 정보 및 버튼 시작 { -->
	<div class="bo_fx">
		<!-- da href="./board.php?bo_table=<?php echo G5_CU_CONF_RELAY ?>" class="btn btn-sm btn-danger">Config Relay</a>
		<a href="./board.php?bo_table=<?php echo G5_CU_CONF_RXTX ?>" class="btn btn-sm btn-danger">Config RxTx</a -->
		<!-- div id="bo_list_total">
			<span>Total <?php echo number_format($total_count) ?>건</span>
			<?php echo $page ?> 페이지
		</div -->

		<?php if ($rss_href || $write_href) { ?>
		<ul class="btn_bo_user">
			<?php if ($rss_href) { ?><li><a href="<?php echo $rss_href ?>" class="btn_b01">RSS</a></li><?php } ?>
			<?php if ($admin_href) { ?><li><a href="<?php echo $admin_href ?>" class="btn btn-sm btn-danger">관리자</a></li><?php } ?>
			<?php /* if ($write_href) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_New[ITS_Lang]?></a></li><?php } */ ?>
		</ul>
		<?php } ?>
	</div>
	<!-- } 게시판 페이지 정보 및 버튼 끝 -->

	<form name="fboardlist" id="fboardlist" action="./board_list_update.php" onsubmit="return fboardlist_submit(this);" method="post">
	<input type="hidden" name="bo_table" value="<?php echo $bo_table ?>">
	<input type="hidden" name="sfl" value="<?php echo $sfl ?>">
	<input type="hidden" name="stx" value="<?php echo $stx ?>">
	<input type="hidden" name="spt" value="<?php echo $spt ?>">
	<input type="hidden" name="sca" value="<?php echo $sca ?>">
	<input type="hidden" name="sst" value="<?php echo $sst ?>">
	<input type="hidden" name="sod" value="<?php echo $sod ?>">
	<input type="hidden" name="page" value="<?php echo $page ?>">
	<input type="hidden" name="sw" value="">

	<div class="tbl_head01 tbl_wrap table-responsive">
		<table class="table table-hover">
		<caption><?php echo $board['bo_subject'] ?> List</caption>
		<thead class="thead-inverse">
		<tr>
			<th scope="col">No.</th>
			<?php if ($is_checkbox) { ?>
			<th scope="col">
				<label for="chkall" class="sound_only">현재 페이지 게시물 전체</label>
				<input type="checkbox" id="chkall" onclick="if (this.checked) all_checked(true); else all_checked(false);">
			</th>
			<?php } ?>
			<th scope="col" style="width: 200px;"><?php echo $SK_BO_Sensor_Name[ITS_Lang]?></th>
			<th scope="col"><?php echo $SK_BO_Serial_Number[ITS_Lang]?></th>

			<th scope="col">Device</th>
			<th scope="col">Host_1</th>
			<th scope="col">Host_2</th>
			<th scope="col">Alert</th>
			<th scope="col">Audio</th>

			<th scope="col"><?php echo $SK_BO_Event[ITS_Lang]?>(<?php echo $SK_BO_Times[ITS_Lang]?>)</th>
			<th scope="col"><?php echo $SK_BO_Event_Hold[ITS_Lang]?>(<?php echo $SK_BO_Second[ITS_Lang]?>)</th>
			<th scope="col"><?php echo $SK_BO_Keep_Cycle[ITS_Lang]?></th>
			<th scope="col"><?php echo $SK_BO_Location[ITS_Lang]?></th>
			<th scope="col"><?php echo $SK_BO_Reserve[ITS_Lang]?>(<?php echo $SK_BO_Week[ITS_Lang]?>)</th>
			<th scope="col"><?php echo $SK_BO_Reserve[ITS_Lang]?>(<?php echo $SK_BO_Day[ITS_Lang]?>)</th>
			<!-- th scope="col"><?php echo $SK_BO_Snapshot[ITS_Lang]?></th -->
			<th scope="col"><?php echo $SK_BO_Log[ITS_Lang]?></th>
			<?php if ($is_good) { ?><th scope="col"><?php echo subject_sort_link('wr_good', $qstr2, 1) ?>추천</a></th><?php } ?>
			<?php if ($is_nogood) { ?><th scope="col"><?php echo subject_sort_link('wr_nogood', $qstr2, 1) ?>비추천</a></th><?php } ?>
		</tr>
		</thead>
		<tbody>
		<?php for ($i=0; $i<count($list); $i++) { ?>
		<tr class="<?php if ($list[$i]['is_notice']) echo "bo_notice"; ?>">
			<td class="td_num">
			<?php
			if ($list[$i]['is_notice']) // 공지사항
				echo '<strong>공지</strong>';
			else if ($wr_id == $list[$i]['wr_id'])
				echo "<span class=\"bo_current\">열람중</span>";
			else
				echo $list[$i]['num'];
			?>
			</td>
			<?php if ($is_checkbox) { ?>
			<td class="td_chk">
				<label for="chk_wr_id_<?php echo $i ?>" class="sound_only"><?php echo $list[$i]['subject'] ?></label>
				<input type="checkbox" name="chk_wr_id[]" value="<?php echo $list[$i]['wr_id'] ?>" id="chk_wr_id_<?php echo $i ?>">
			</td>
			<?php } ?>
			<td class="td_board">
				<?php
				echo $list[$i]['icon_reply'];
				if ($is_category && $list[$i]['ca_name']) {
				?>
				<a href="<?php echo $list[$i]['ca_name_href'] ?>" class="bo_cate_link"><?php echo $list[$i]['ca_name'] ?></a>
				<?php } ?>

				<a href="<?php echo $list[$i]['href'] ?>">
					<?php 
						if ($list[$i]['w_sensor_disable']) 
							echo "<del>" . $list[$i]['subject'] . "</del>"; 
						else 
							echo $list[$i]['subject']; 
					?>
					<?php if ($list[$i]['comment_cnt']) { ?><span class="sound_only">Comment</span><?php echo $list[$i]['comment_cnt']; ?><span class="sound_only">Each</span><?php } ?>
				</a>
			</td>
			<td class="td_board"><?php echo $list[$i]['w_sensor_serial'] ?></td>

			<td class="td_board"><?php echo ($cfg["DEVICE_all"][$list[$i]['w_device_id']]); ?></td>
			<td class="td_board"><?php echo $list[$i]['w_host_Addr'] ?></td>
			<td class="td_board"><?php echo $list[$i]['w_host_Addr2'] ?></td>
			<td class="td_board"><?php echo $cfg["DEVICE_alert"][$list[$i]['w_alert_Port']] ?> <?php echo $list[$i]['w_alert_Value'] ?> s</td>
			<td class="td_board"><?php echo $list[$i]['wr_2'] ?></td>

			<td class="td_board"><?php echo $list[$i]['w_event_holdTime'] ?></td>
			<td class="td_board"><?php echo $list[$i]['w_event_pickTime'] ?></td>
			<td class="td_board"><?php if ($list[$i]['w_event_keepHole']) echo "On"; else echo "Off"; ?></td>
			<td class="td_board pointer" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/status/mapsInfo.php?myLatS=<?php echo $list[$i]['w_sensor_lat_s']?>&myLngS=<?php echo $list[$i]['w_sensor_lng_s']?>&myLatE=<?php echo $list[$i]['w_sensor_lat_e']?>&myLngE=<?php echo $list[$i]['w_sensor_lng_e']?>&wr_subject=<?php echo $list[$i]['wr_subject']?>","mapsLocation", "width=600,height=400,scrollbars=no");' ><?php echo $SK_BO_Map[ITS_Lang]?></td>
			<td class="td_board pointer" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/scheduleBlock/weekView.php?bo_table=<?php echo $bo_table?>&wr_id=<?php echo $list[$i]['wr_id']?>&wr_subject=<?php echo $list[$i]['wr_subject']?>&w_sensor_serial=<?php echo $list[$i]['w_sensor_serial']?>","scheduleWeek_GPIO_<?php echo $list[$i]['wr_id']?>", "width=600,height=500,scrollbars=no");'><?php echo $SK_BO_Weekly[ITS_Lang]?></td>
			<td class="td_board pointer" onclick='window.open("<?php echo G5_THEME_URL ?>/utility/scheduleBlock/index.php?bo_table=<?php echo $bo_table?>&wr_id=<?php echo $list[$i]['wr_id']?>&wr_subject=<?php echo $list[$i]['wr_subject']?>&w_sensor_serial=<?php echo $list[$i]['w_sensor_serial']?>","scheduleBlock_GPIO_<?php echo $list[$i]['wr_id']?>", "width=600,height=500,scrollbars=no");'><?php echo $SK_BO_Daily[ITS_Lang]?></td>
			<!-- td class="td_board pointer" onclick='window.open("<?php echo G5_CU_UTIL_URL ?>/ecosFileTree/snapshotView.php?ID=<?php echo $list[$i]['w_sensor_serial']?>&wr_subject=<?php echo $list[$i]['wr_subject']?>","Shot_Tree_<?php echo $list[$i]['w_sensor_serial']?>", "width=800,height=400,scrollbars=no");' >Shot</td -->
			<td class="td_board pointer btn_Events" data-serial="<?php echo $list[$i]['w_sensor_serial']?>" data-subject="<?php echo $list[$i]['wr_subject']?>"><?php echo $SK_BO_Log[ITS_Lang]?></td>
			<?php if ($is_good) { ?><td class="td_num"><?php echo $list[$i]['wr_good'] ?></td><?php } ?>
			<?php if ($is_nogood) { ?><td class="td_num"><?php echo $list[$i]['wr_nogood'] ?></td><?php } ?>
		</tr>
		<?php } ?>
		<?php if (count($list) == 0) { echo '<tr><td colspan="'.$colspan.'" class="empty_table">'.$SK_BO_Empty_Board[ITS_Lang].'</td></tr>'; } ?>
		</tbody>
		</table>
	</div>

	<?php if ($list_href || $is_checkbox || $write_href) { ?>
	<div class="bo_fx">
		<?php if ($admin_href) { ?><a href="<?php echo G5_CU_UTIL_URL ?>/ecosJstree/ecosTree.php?tmpPath=" class="btn btn-sm btn-info"><?php echo $SK_BO_Snapshot[ITS_Lang]?></a><?php } ?>
		<?php if ($is_checkbox) { ?>
		<ul class="btn_bo_adm">
			<li><input type="submit" name="btn_submit" value="선택적용" onclick="document.pressed=this.value" class="btn btn-sm btn-primary"></li>
			<!-- li><input type="submit" name="btn_submit" value="선택삭제" onclick="document.pressed=this.value" class="btn btn-sm btn-primary"></li>
			<li><input type="submit" name="btn_submit" value="선택복사" onclick="document.pressed=this.value" class="btn btn-sm btn-primary"></li>
			<li><input type="submit" name="btn_submit" value="선택이동" onclick="document.pressed=this.value" class="btn btn-sm btn-primary"></li -->
		</ul>
		<?php } ?>

		<?php if ($list_href || $write_href) { ?>
		<ul class="btn_bo_user">
			<?php if ($list_href) { ?><li><a href="<?php echo $list_href ?>" class="btn_b01"><?php echo $SK_BO_List[ITS_Lang]?></a></li><?php } ?>
			<?php /* if ($write_href) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary hide"><?php echo $SK_BO_New[ITS_Lang]?></a></li><?php } */ ?>
		</ul>
		<?php } ?>
	</div>
	<?php } ?>
	</form>

<?php if($is_checkbox) { ?>
<noscript>
<p>자바스크립트를 사용하지 않는 경우<br>별도의 확인 절차 없이 바로 선택삭제 처리하므로 주의하시기 바랍니다.</p>
</noscript>
<?php } ?>

<!-- 페이지 -->
<?php echo $write_pages;  ?>

<?php /* <!-- 게시판 검색 시작 { -->
<fieldset id="bo_sch">
    <form name="fsearch" method="get" class="form-inline">
    <input type="hidden" name="bo_table" value="<?php echo $bo_table ?>">
    <input type="hidden" name="sca" value="<?php echo $sca ?>">
    <input type="hidden" name="sop" value="and">
    <select name="sfl" id="sfl" class="form-control input-sm">
        <option value="wr_subject"<?php echo get_selected($sfl, 'wr_subject', true); ?>>제목</option>
        <option value="wr_content"<?php echo get_selected($sfl, 'wr_content'); ?>>내용</option>
        <option value="wr_subject||wr_content"<?php echo get_selected($sfl, 'wr_subject||wr_content'); ?>>제목+내용</option>
        <option value="mb_id,1"<?php echo get_selected($sfl, 'mb_id,1'); ?>>회원아이디</option>
        <option value="mb_id,0"<?php echo get_selected($sfl, 'mb_id,0'); ?>>회원아이디(코)</option>
        <option value="wr_name,1"<?php echo get_selected($sfl, 'wr_name,1'); ?>>글쓴이</option>
        <option value="wr_name,0"<?php echo get_selected($sfl, 'wr_name,0'); ?>>글쓴이(코)</option>
    </select>
    <label for="stx" class="sound_only">검색어<strong class="sound_only"> 필수</strong></label>
    <input type="text" name="stx" value="<?php echo stripslashes($stx) ?>" required id="stx" class="form-control input-sm required" size="15" maxlength="20">
    <input type="submit" value="검색" class="btn btn-sm btn-success">
    </form>
</fieldset>
</section>
<!-- } 게시판 검색 끝 --> */ ?>

<?php if ($is_checkbox) { ?>
<script>
function all_checked(sw) {
    var f = document.fboardlist;

    for (var i=0; i<f.length; i++) {
        if (f.elements[i].name == "chk_wr_id[]")
            f.elements[i].checked = sw;
    }
}

function fboardlist_submit(f) {
    var chk_count = 0;

    for (var i=0; i<f.length; i++) {
        if (f.elements[i].name == "chk_wr_id[]" && f.elements[i].checked)
            chk_count++;
    }

    if (!chk_count) {
        alert(document.pressed + "할 게시물을 하나 이상 선택하세요.");
        return false;
    }

    if(document.pressed == "선택적용") {
        select_update();
        return;
    }

    if(document.pressed == "선택복사") {
        select_copy("copy");
        return;
    }

    if(document.pressed == "선택이동") {
        select_copy("move");
        return;
    }

    if(document.pressed == "선택삭제") {
        if (!confirm("선택한 게시물을 정말 삭제하시겠습니까?\n\n한번 삭제한 자료는 복구할 수 없습니다\n\n답변글이 있는 게시글을 선택하신 경우\n답변글도 선택하셔야 게시글이 삭제됩니다."))
            return false;

        f.removeAttribute("target");
        f.action = "./board_list_update.php";
    }

    return true;
}

// 선택한 게시물 수정
function select_update() {
    var f = document.fboardlist;
    f.action = "<?php echo "$board_skin_url/update.php" ?>";
    f.submit();
}


// 선택한 게시물 복사 및 이동
function select_copy(sw) {
    var f = document.fboardlist;

    if (sw == "copy")
        str = "복사";
    else
        str = "이동";

    var sub_win = window.open("", "move", "left=50, top=50, width=500, height=550, scrollbars=1");

    f.sw.value = sw;
    f.target = "move";
    f.action = "./move.php";
    f.submit();
}
</script>
<?php } ?>
<!-- } 게시판 목록 끝 -->