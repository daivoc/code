<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

$node_key = md5(microtime(true)); // 사용자 제한을 위한 키를 만들고 키값을 /tmp 내애 파일을 만든 다
touch(G5_PATH."/data/$node_key"); // 키파일 생성 사용된 파일은 nodejs server가 사용후 삭제
echo $node_key;
?>