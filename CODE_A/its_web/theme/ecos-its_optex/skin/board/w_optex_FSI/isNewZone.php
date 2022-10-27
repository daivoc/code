<?php
include_once('../../../../../common.php');

$parent_id = strip_tags($_POST['parent_id']);
$zone_id = strip_tags($_POST['zone_id']);
$zone_name = strip_tags($_POST['zone_name']);

// // 설정 보드 타입 its 또는 acu
// $sql = " SELECT COUNT(1) as count, `wr_id` FROM `g5_write_g400t140` WHERE w_sensor_disable = 0 AND w_parent_id = '$parent_id' AND  w_zone_id = '$zone_id'; " ;
// $counts = sql_fetch($sql);

$my_ID = 0;
if($parent_id && $zone_id) {
    // $sql = " SELECT `wr_id` FROM `g5_write_g400t140` WHERE w_sensor_disable = 0 AND w_parent_id = '$parent_id' AND  w_zone_id = '$zone_id'; " ;
    $sql = " SELECT `wr_id` FROM `g5_write_g400t140` WHERE w_parent_id = '$parent_id' AND  w_zone_id = '$zone_id'; " ;
    $row = sql_fetch($sql);
    if($row["wr_id"]){
        $my_ID = (int)$row["wr_id"];
    }
}

$sql = " SELECT `w_zone_id` FROM `g5_write_g400t140` WHERE w_sensor_disable = 0; " ;
$result = sql_query($sql);
$zones = array();
for ($i=0; $row=sql_fetch_array($result); $i++) {
    $zones[] = (int)$row["w_zone_id"];
}

// $json = json_encode(array('count' => $counts["count"], 'zones' => $zones, 'row_id' => $row["wr_id"], 'parent_id' => $parent_id, 'zone_id' => $zone_id, 'zone_name' => $zone_name));
// $json = json_encode(array('count' => $counts["count"], 'zones' => $zones, 'row_id' => $row["wr_id"], 'parent_id' => $parent_id, 'zone_id' => $zone_id, 'zone_name' => $zone_name));
$json = json_encode(array('zones' => $zones, 'my_ID' => $my_ID, 'parent_id' => $parent_id, 'zone_id' => $zone_id, 'zone_name' => $zone_name));
echo($json);
die();
?>