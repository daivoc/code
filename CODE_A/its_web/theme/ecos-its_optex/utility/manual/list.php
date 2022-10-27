<?php
include_once('./_common.php');
global $g5, $bo_table;

if($is_guest) exit("Abnormal approach!");

include_once G5_THEME_PATH.'/head.php';
?>

<?php
function recursiveArrayToList(Array $array = array()) {
	echo "<ul>";
	foreach ($array as $key => $value) {
		if (is_array($value)) {
			echo "<li>" . $key . "</li>";
			recursiveArrayToList($value);
		} else {
			echo "<li onclick='get_content(".$value.")'>" . $key . "</li>";
		}
	}
	echo "</ul>";
}

// 메뉴 불러오기
if($category) {
	$filter = " WHERE w_group_main = '".$category."' ORDER BY w_order ASC";
} else {
	$filter = " ORDER BY w_order ASC";
}
// $sql = " SELECT wr_id, wr_subject, wr_content, w_group_main, w_group_sub, w_order, w_sub_title FROM g5_write_".G5_CU_CONF_MANUAL.$filter;
$sql = " SELECT wr_id, wr_subject, w_order, w_group_main, w_group_sub FROM g5_write_".G5_CU_CONF_MANUAL.$filter;
$manual_list = '';
$manual_group = array();
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
	if($row[w_order] > 0){ // 0 이 아닌 문서 추출
		// $manual_list .="<li onclick='get_content(".$row[wr_id].")'>".($category?'':'<font color=orange>['.$row[w_group_main].']</font>').($category?'':'<font color=green>['.$row[w_group_sub].']</font>').$row[wr_subject]."</li>";
		$manual_list .="<li onclick='get_content(".$row[wr_id].")'><font color=orange>[".$row[w_group_main]."]</font><font color=green>[".$row[w_group_sub]."]</font>".$row[wr_subject]."</li>";
		if($row[w_group_main]){
			// $manual_group[$row[w_group_main]] += 1;
			// $manual_group[$row[w_group_main]][$row[w_group_sub]] += 1;
			$manual_group[$row[w_group_main]][$row[w_group_sub]][$row[wr_subject]] = $row[wr_id];
		}
	}
}
// 카테고리 불러오기
$manual_cata = "";
foreach ($manual_group as $key => $value) {
	if($category) {
		$manual_cata .= "<span class='btn btn-xs btn-default'>".$key."(".count($manual_group[$key]).")</span>";
	} else {
		$manual_cata .= "<a href=".htmlspecialchars(G5_URL.$_SERVER['PHP_SELF'])."?category=".$key." class='btn btn-xs btn-default'>".$key."(".count($manual_group[$key]).")</a>";
	}
}
if($manual_cata) {
	$manual_cata = "<a href=".htmlspecialchars(G5_URL.$_SERVER['PHP_SELF'])." class='btn btn-xs btn-success'>전체</a>".$manual_cata;
}
?>

<script>
function get_content(wr_id) {
	$.ajax({
		url : "<?php echo G5_URL ?>/theme/ecos-its_optex/utility/manual/getContent.php?id="+wr_id
	}).done(function(data) {
		console.log(data);
		document.getElementById("contents").innerHTML = data;
	});
}

$(document).ready(function(){
	$(window).resize(function() { // container의 폭에서 menu폭을 뺀 값을 contents에 적용한다.
		var widthIs = $(".container").width() - $(".menu").width();
		console.log(widthIs);
		$(".contents").width(widthIs);
	});
	$(window).resize();
});
</script>

<style>
	.menu {
		padding-right: 10px;
		width: 200px;
		overflow: auto;
		height: 700px;
		color: gray;
	}
	.menu ul { 
		display:table;
		font-size: 8pt;
	}
	.menu ul ul { 
		margin-left:10px;
	}
	.menu ul ul ul { 
		margin-left:10px;
	}
	.contents {
		overflow: auto;
		height: 700px;
	}
	.class_grp a {
		margin: 0 4px;
	}
	.lists_grp {
		font-size: 9pt;
	}
	.lists_grp li {
		padding-top: 6px;
		cursor: pointer;
	}
</style>

<section style="padding-top:60px">
    <div class="container">
		<table>
			<tr>
				<td colspan=2>
					<div class="class_grp"><?php print $manual_cata; ?></div>
				</td>
			</tr>
			<tr>
				<td>
					<div class="menu">
						<?php echo recursiveArrayToList($manual_group); ?>
						<ul class="lists_grp"><?php print $manual_list; ?></ul>
					</div>
				</td>
				<td>
					<div class="contents" id="contents">
						<div>ITS</div>
						<video width="100%" controls>
							<source src="<?php echo G5_CU_VDO_URL?>/OPTEX Corporate Video.mp4" type="video/mp4">
						</video>
					</div>
				</td>
			</tr>
		</table>
	</div>
</section>


<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>