<?php
include_once('./_common.php');
// if ($is_guest) { exit("Abnormal approach!"); }


$list_body = '';
$result = sql_query("SHOW COLUMNS FROM ". base64_decode($license_tbl_name)); 
while ($row = sql_fetch_array($result)) { 
  $list_body .= '"'.$row['Field'].'",';
}
$list_body .= "\n";
$sql = base64_decode($sqlCountRow);
$result = sql_query($sql);
while ($row = sql_fetch_array($result)) {
    foreach ($row as $col_value) {
        $list_body .= '"'.($col_value).'",';
	}
	$list_body .= "\n";
}

// https://wonis-lifestory.tistory.com/entry/php-csv-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C-%EC%8B%9C-%ED%95%9C%EA%B8%80-%EA%B9%A8%EC%A7%90
header('Content-Type:text/csv;charset=UTF-8;');
header("Content-Disposition: attachment; filename=export.csv");

print "\xEF\xBB\xBF";
print "$list_body";
?>
