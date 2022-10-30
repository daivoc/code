<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

include_once("$board_skin_path/config.php"); // Local Function List
include_once("$board_skin_path/its_module.php"); // Local Function List
// 선택옵션으로 인해 셀합치기가 가변적으로 변함
$colspan = 10;

if ($is_checkbox) $colspan++;
if ($is_good) $colspan++;
if ($is_nogood) $colspan++;
?>

<link rel="stylesheet" href="<?php echo $board_skin_url?>/style.css">

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
			<?php if ($write_href && count(get_w_detect_id()) < 2) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary"><?php echo $SK_BO_New[ITS_Lang]?></a></li><?php } ?>
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
            <th scope="col">Group Name</th>
            <th scope="col">In #</th>
            <th scope="col">Out #</th>
            <th scope="col">Relay_L</th>
            <th scope="col">Direction</th>
            <th scope="col">Relay_R</th>
            <th scope="col">Distance</th>
            <th scope="col">Speed_L</th>
            <th scope="col">Speed_H</th>
            
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
            <td class="td_board" style='font-size:10pt;'>
                <?php
                echo $list[$i]['icon_reply'];
                if ($is_category && $list[$i]['ca_name']) {
                ?>
                <a href="<?php echo $list[$i]['ca_name_href'] ?>" class="bo_cate_link"><?php echo $list[$i]['ca_name'] ?></a>
                <?php } ?>

                <a href="<?php echo $list[$i]['href'] ?>">
                    <?php 
						if ($list[$i]['w_gpcio_disable']) 
							echo "<del>" . $list[$i]['subject'] . "</del>"; 
						else 
							echo $list[$i]['subject'];
					?>
                    <?php if ($list[$i]['comment_cnt']) { ?><span class="sound_only">Comment</span><?php echo $list[$i]['comment_cnt']; ?><span class="sound_only">Each</span><?php } ?>
                </a>
            </td>

            <td class="td_board"><?php echo $list[$i]['w_direction_AX'] ?></td>
            <td class="td_board"><?php echo $list[$i]['w_direction_XA'] ?></td>
            <td class="td_board"><?php if($list[$i]['w_gpcio_trigger_L']) echo '🡫'; else echo '🡩'; ?> <?php if($list[$i]['w_gpcio_detect_L']) echo $relay_inputL[$list[$i]['w_gpcio_detect_L']] ?></td>
            <td class="td_board"><?php if($list[$i]['w_gpcio_detect_L']) echo $opject_direction[$list[$i]['w_gpcio_direction']] ?></td>
            <td class="td_board"><?php if($list[$i]['w_gpcio_detect_R']) echo $relay_inputR[$list[$i]['w_gpcio_detect_R']] ?> <?php if($list[$i]['w_gpcio_trigger_R']) echo '🡫'; else echo '🡩'; ?></td>
            <td class="td_board"><?php echo $list[$i]['w_distance'] ?> cm</td>
            <td class="td_board"><?php echo $list[$i]['w_speed_L'] ?> km/h</td>
            <td class="td_board"><?php echo $list[$i]['w_speed_H'] ?> km/h</td>
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
			<?php if ($write_href) { ?><li><a href="<?php echo $write_href ?>" class="btn btn-sm btn-primary hide"><?php echo $SK_BO_New[ITS_Lang]?></a></li><?php } ?>
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
