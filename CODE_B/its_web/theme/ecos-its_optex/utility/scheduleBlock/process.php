<?php
// https://www.jqueryajaxphp.com/fullcalendar-crud-with-jquery-and-php/
include('config.php');

$type = $_POST['type'];

if($type == 'newSelect') {
	$title = $_POST['title'];
	$startdate = $_POST['startdate'];
	$enddate = $_POST['enddate'];
	$allDay = $_POST['allDay'];
	$bo_table = $_POST['bo_table'];
	$wr_id = $_POST['wr_id'];
	$wr_subject = $_POST['wr_subject'];
	$w_week = $_POST['w_week']; // 2017 01 01 에 고정된 일주일 시간표
	$w_sensor_serial = $_POST['w_sensor_serial'];
	$insert = mysqli_query($con,"INSERT INTO $tableID(`title`, `startdate`, `enddate`, `allDay`, `bo_table`, `wr_id`, `wr_subject`, `w_sensor_serial`, `w_week`) VALUES('$title','$startdate','$enddate','$allDay','$bo_table','$wr_id','$wr_subject','$w_sensor_serial','$w_week')");
	$lastid = mysqli_insert_id($con);
	echo json_encode(array('status'=>'success','eventid'=>$lastid));
} 
// INSERT INTO `w_block_event`(`title`, `startdate`, `enddate`, `allDay`, `bo_table`, `wr_id`, `wr_subject`, `w_sensor_serial`, `w_week`) VALUES('$title','$startdate','$enddate','lDay','$bo_table','12','$wr_subject','$w_sensor_serial','1')

if($type == 'moveEvent' || $type == 'resizeEvent') {
	$title = $_POST['title'];
	$startdate = $_POST['startdate'];
	$enddate = $_POST['enddate'];
	$eventid = $_POST['eventid'];
	$update = mysqli_query($con,"UPDATE $tableID SET title='$title', startdate = '$startdate', enddate = '$enddate' where id='$eventid'");
	if($update)
		echo json_encode(array('status'=>'success'));
	else
		echo json_encode(array('status'=>'failed'));
}
 
if($type == 'new') {
	$startdate = $_POST['startdate'];
	$enddate = date("Y-m-d H:i:s", strtotime('+2 hours', strtotime($startdate)));
	$title = $_POST['title'];
	// $startdate = $_POST['startdate'];
	// $enddate = $_POST['startdate'].'+'.$_POST['zone'];
	$bo_table = $_POST['bo_table'];
	$wr_id = $_POST['wr_id'];
	$wr_subject = $_POST['wr_subject'];
	$w_sensor_serial = $_POST['w_sensor_serial'];
	$w_week = $_POST['w_week'];
	$insert = mysqli_query($con,"INSERT INTO $tableID(`title`, `startdate`, `enddate`, `allDay`, `bo_table`, `wr_id`, `wr_subject`, `w_sensor_serial`, `w_week`) VALUES('$title','$startdate','$enddate','$allDay','$bo_table','$wr_id','$wr_subject','$w_sensor_serial','$w_week')");
	$lastid = mysqli_insert_id($con);
	echo json_encode(array('status'=>'success','eventid'=>$lastid));
}

if($type == 'remove') {
	$eventid = $_POST['eventid'];
	$delete = mysqli_query($con,"DELETE FROM $tableID where id='$eventid'");
	if($delete)
		echo json_encode(array('status'=>'success'));
	else
		echo json_encode(array('status'=>'failed'));
}

if($type == 'fetch') {
	$bo_table = $_POST['bo_table'];
	$wr_id = $_POST['wr_id'];
	$wr_subject = $_POST['wr_subject'];
	$w_sensor_serial = $_POST['w_sensor_serial'];
	$events = array();
	// $query = mysqli_query($con, "SELECT * FROM $tableID where wr_id='$wr_id'");
	$query = mysqli_query($con, "SELECT * FROM $tableID where w_sensor_serial='$w_sensor_serial'");
	while($fetch = mysqli_fetch_array($query,MYSQLI_ASSOC)) {
	$e = array();
    $e['id'] = $fetch['id'];
    $e['title'] = $fetch['title'];
    $e['start'] = $fetch['startdate'];
    $e['end'] = $fetch['enddate'];

    $allday = ($fetch['allDay'] == "true") ? true : false;
    $e['allDay'] = $allday;

    array_push($events, $e);
	}
	echo json_encode($events);
}

if($type == 'changetitle') {
	$eventid = $_POST['eventid'];
	$title = $_POST['title'];
	$update = mysqli_query($con,"UPDATE $tableID SET title='$title' where id='$eventid'");
	if($update)
		echo json_encode(array('status'=>'success'));
	else
		echo json_encode(array('status'=>'failed'));
}

if($type == 'resetdate') {
	$title = $_POST['title'];
	$startdate = $_POST['start'];
	$enddate = $_POST['end'];
	$eventid = $_POST['eventid'];
	$update = mysqli_query($con,"UPDATE $tableID SET title='$title', startdate = '$startdate', enddate = '$enddate' where id='$eventid'");
	if($update)
		echo json_encode(array('status'=>'success'));
	else
		echo json_encode(array('status'=>'failed'));
}


?>