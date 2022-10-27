<?php
include_once('./_common.php');
// if ($is_guest) exit("Abnormal approach!");

// USB 드라이버 관련 device port
global $g5, $bo_table;

// http://192.168.0.80/theme/ecos-its_optex/utility/status/jsonCFG.php?&bo_table=g300t100&wr_id=1
// 생성 -> /var/www/html/its_web/theme/ecos-its_optex/user/config/cfg_g800t100_1.json
// define('$cfgPath', G5_DATA_PATH.'/config');
$gJson = json_decode(file_get_contents("/home/pi/common/config.json"), TRUE);
$cfgPath = $gJson["path"]["its_web"].$gJson['path']['user']['config'];
// D:\code\ITS_CODE\its_common\systemConfig.py에서 풀더 생성됨
if (!file_exists($cfgPath)) {
    mkdir($cfgPath, 0777, true);
}

$write_table = $g5['write_prefix'] . $bo_table;
$sql = " SELECT * FROM $write_table WHERE wr_id = $wr_id; ";
$config = array();

$result = sql_query($sql);
$row = sql_fetch_array($result);
$replace = array('wr_', 'w_'); 
foreach($row as $field => $value) {
    // if(substr( $field, 0, 2 ) === "w_") {
    //     $field = str_replace($replace,'',$field); 
    //     $config[] = array($field => $value);
    // }
    // if(substr( $field, 0, 3 ) === "wr_") {
    //     $field = str_replace($replace,'',$field); 
    //     $config[] = array($field => $value);
    // }
    $config[$field] = $value;
}

$cfgName = $cfgPath . '/cfg_' . $bo_table . '_' . $wr_id . '.json';
$fp = fopen($cfgName , 'w');
fwrite($fp, json_encode($config, JSON_PRETTY_PRINT));
fclose($fp);
?> 