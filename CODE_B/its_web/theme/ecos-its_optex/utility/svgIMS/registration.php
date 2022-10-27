<?php
include_once('./_common.php');

if ($is_guest) exit("Abnormal approach!");

// define('G5_CU_CONF_CAMERA', 'g500t100');
// define('G5_CU_CONF_ZONE', 'g500t200');
// define('G5_CU_CONF_BOX', 'g500t300');

// http://192.168.0.4/bbs/write.php?w=u&bo_table=g500t200&wr_id=1
// http://192.168.0.4/bbs/write.php?bo_table=g500t200

if ($boardTableID == "zone") {
    $bo_table_info = G5_CU_CONF_ZONE;
} elseif ($boardTableID == "box") {
    $bo_table_info = G5_CU_CONF_BOX;
} elseif ($boardTableID == "camera") {
    $bo_table_info = G5_CU_CONF_CAMERA;
} else {
    $bo_table_info = "";
}

if($bo_table_info) {
    $write_table = $g5['write_prefix'] . $bo_table_info;
    $sqlCountRow = " SELECT wr_id FROM $write_table WHERE w_map_id = '$curElementID'; ";
    $result = sql_query($sqlCountRow);
    $num_rows = sql_num_rows($result); // 자료 갯수

    if ($num_rows) {
        $wr_id = sql_fetch_array($result)['wr_id'];
        // $boardTableLink = "http://192.168.0.4/bbs/write.php?w=u&bo_table=$bo_table_info&wr_id=$wr_id"; // 수정
        $boardTableLink = "/bbs/board.php?bo_table=$bo_table_info&wr_id=$wr_id"; // 보기
    } else {
        $boardTableLink = "/bbs/write.php?bo_table=$bo_table_info"; // 신규
    }
    echo $boardTableLink;
}

// $sql = " SELECT * FROM $write_table WHERE w_map_id = '0' ";
// $result = sql_query($sql);
// while ($row = sql_fetch_array($result)) {
// 	$value_select = "?devideID=".$row['w_device_id']."&sensorID=".$row['w_sensor_serial']."&subject=".$row['wr_subject'];
// 	if($subject == $row['wr_subject'])
// 		$select_w_sensor_devID .='<option value="'.$value_select.'" selected>'.$row['wr_subject'].'</option>';
// 	else
// 		$select_w_sensor_devID .='<option value="'.$value_select.'">'.$row['wr_subject'].'</option>';
// }

// echo "$num_rows, $boardTableID, $curElementID";	
?>