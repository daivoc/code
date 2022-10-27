<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// USB 드라이버 관련 device port
global $g5, $bo_table;

$write_table = $g5['write_prefix'] . $bo_table;
$sql = " SELECT * FROM $write_table WHERE wr_id = $wr_id; ";

$result = sql_query($sql);
$row = sql_fetch_array($result);

$list_body = '';

$replace = array('wr_', 'w_'); 

foreach($row as $field => $value) {
	// $field = str_pad(str_replace($replace,'',$field), 20, " ", STR_PAD_RIGHT); 
	$list_body .= $field . ": " . $value . "\n";
}

?>
<!DOCTYPE html>
<html>
<head>
<script>
function download(){
    var a = document.body.appendChild(
        document.createElement("a")
    );
    a.download = "config.txt";
    a.href = "data:text/plain," + document.getElementById("list_body").innerHTML;
    a.click();
}
function myFunction() {
    window.print();
}
</script>
<style>
@media print {
  button {
    visibility: hidden;
  }
}
</style>
</head>
<body>
<button onclick="myFunction()">Print</button>
<button onClick="download()">Download</button>
<pre id="list_body">
<?php print $list_body ?>
</pre>
</body>
</html>