<?php
// http://192.168.0.9/its_web/theme/ecos-its_optex/utility/socket/ims.php?id=id&name=name&beep=beep&shot=shot&subzone=subzone
// http://192.168.0.9/its_web/theme/ecos-its_optex/utility/socket/ims.php?id=rect-1&name=rect-1&beep=1&shot=&subzone=
	
	// header("HTTP/1.1 200 OK");
	
	// http_response_code(200);

	$id = trim($_GET['id']);
	if(!$id) exit(); // $id = 'Unknown';
	$name = trim($_GET['name']);
	if(!$name) $name = $id;
	$beep = trim($_GET['beep']);
	if(!$beep) $beep = '1';
	$shot = trim($_GET['shot']);
	if(!$shot) $shot = '';
	$subzone = trim($_GET['subzone']);
	if(!$subzone) $subzone = '';

	$host    = "127.0.0.1";
	$port    = 8087;
	$message = "id=$id,name=$name,beep=$beep,shot=$shot,subzone=$subzone";
	// echo "Message To server :".$message;

	// create socket
	$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");

	// connect to server
	$result = socket_connect($socket, $host, $port) or die("Could not connect to server\n"); 

	// send string to server
	socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");

	// // get server response
	// $result = socket_read ($socket, 1024) or die("Could not read server response\n");
	// // echo "Reply From Server  :".$result;

	// close socket
	socket_close($socket);
	
	// exit();
?>