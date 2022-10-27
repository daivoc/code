<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

$list_body = '';
$result = sql_query("SHOW COLUMNS FROM ". base64_decode($bo_table_name)); 
while ($row = sql_fetch_array($result)) { 
  $list_body .= '"'.$row['Field'].'",';
}
$list_body .= "\n";
$sql = base64_decode($sqlCountRow);
// print $sql;
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
    foreach ($row as $col_value) {
        $list_body .= '"'.$col_value.'",';
	}
	$list_body .= "\n";
}

$today = date("Ymd_His");

header('Content-type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename='.$today.'.csv');
header('Content-Length: '. strlen($list_body));

echo "\xEF\xBB\xBF"; 

echo $list_body;
?>
