<?php
// include_once('./_common.php');

// if ($sw == 'move')
    // $act = '�̵�';
// else if ($sw == 'copy')
    // $act = '����';
// else
    // alert('sw ���� ����� �Ѿ���� �ʾҽ��ϴ�.');

// // �Խ��� ������ �̻� ����, �̵� ����
// if ($is_admin != 'board' && $is_admin != 'group' && $is_admin != 'super')
    // alert_close("�Խ��� ������ �̻� ������ �����մϴ�.");

// include_once(G5_PATH.'/head.sub.php');

$wr_id_list = '';
$comma = '';
for ($i=0; $i<count($_POST['chk_wr_id']); $i++) {
	$wr_id_list .= $comma . $_POST['chk_wr_id'][$i];
	$comma = ',';
}

for ($i=0; $i<count($_POST['w_sensor_reload']); $i++) {
	$wr_id_list .= $comma . $_POST['w_sensor_reload'][$i];
	$comma = ',';
}

print $wr_id_list;

// //$sql = " select * from {$g5['board_table']} a, {$g5['group_table']} b where a.gr_id = b.gr_id and bo_table <> '$bo_table' ";
// // ���� �Խ����� ���� �� �� �ֵ��� ��.
// $sql = " select * from {$g5['board_table']} a, {$g5['group_table']} b where a.gr_id = b.gr_id ";
// if ($is_admin == 'group')
    // $sql .= " and b.gr_admin = '{$member['mb_id']}' ";
// else if ($is_admin == 'board')
    // $sql .= " and a.bo_admin = '{$member['mb_id']}' ";
// $sql .= " order by a.gr_id, a.bo_order, a.bo_table ";
// $result = sql_query($sql);
// for ($i=0; $row=sql_fetch_array($result); $i++)
// {
    // $list[$i] = $row;
// }
?>


<?php
// include_once(G5_PATH.'/tail.sub.php');
?>
