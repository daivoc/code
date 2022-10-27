<?php
////////////////////////////////////
// ITS API 프로그램의 일부로 설치 및 실행시 Document Root에 위치 한다.
// Document Root내의 파일명은 api.php로 이름이 변경 된다.
// Client로 부터 Http Request(GET, POST) 방식으로 만 접근이 가능하며 Plain Text화된 JSON Data를 처리한다. 형식: api=[Json]
// 전송된 데이터는 파싱과 JSON 분석을 거친후 내용에 따라 자신이나 외부서버에 명령문을 Socket을 통해 재전송 된다.
// 예:
// 트리거링 명령(활성)
//  http://192.168.0.50/api.php?api=[{"trigger":{"id":"io02"}}]
// 자신의 릴레이 제어(비활성)
//  http://192.168.0.50/api.php?api=[{"gpio":{"status":"2","id":"io12","hold":"4","msg":""},"debug":true}]
//  http://192.168.0.50/api.php?api=[{"custom":{"method":"tcp_socket","isJson":true,"data":{"id_01":"name_01","id_02":"name_02","id_03":"name_03","id_04":"name_04"},"count":"3","interval":"3"},"server":{"host":"192.168.0.50","port":"34001"},"debug":true}]
// 원격의 릴레이 제어(비활성)
//  http://192.168.0.80/api.php?api=[{"gpio":{"status":"2","id":"io11","hold":"3.16","msg":""},"server":{"host":"192.168.0.50","port":"34001"},"debug":true}]

$cfg = json_decode(file_get_contents('/home/pi/API/itsAPI.json'), true);
// $host = $cfg['tcpIpPort']['hostIP'];
// $port = $cfg['tcpIpPort']['portAPI'];
$allow = array_filter(explode(",", $cfg['permission']['filterIP']['allow']));
$deny = array_filter(explode(",", $cfg['permission']['filterIP']['deny']));
$userIP = $_SERVER["REMOTE_ADDR"];

// echo count($allow);
// echo count($deny);

if(count($allow)) {
	foreach($allow as $key=>$data) { // echo $key."=>".$data."<br>";
		// echo $userIP, trim($data);
		if(trim($data) == $userIP) {
			;
		} else {
			echo('Unallowed User permission');
			die();
		}
	}
}

if(count($deny)) {
	foreach($deny as $key=>$data) { // echo $key."=>".$data."<br>";
		// echo $userIP, trim($data);
		if(trim($data) == $userIP) {
			echo('Denied User permission');
			die();
		}
	}
}


// echo $cfg['tcpIpPort']['hostIP'];

// $api = '[{"gpio":{"status":"2","id":"R12","hold":"4","msg":""},"debug":true}]';
if($_GET["api"]){
	$api = $_GET["api"];
} else if($_POST["api"]){
	$api = $_POST["api"];
} else {
	echo('Error<br>');
	echo('Method : '.$_SERVER['REQUEST_METHOD'].'<br>');
	echo(urldecode($_SERVER['REQUEST_URI']).'<br>');
	die();
}

function json_validate($string) {
	// https://stackoverflow.com/questions/6041741/fastest-way-to-check-if-a-string-is-json-in-php
	// decode the JSON data
	$result = json_decode($string, true);

	// switch and check possible JSON errors
	switch (json_last_error()) {
		case JSON_ERROR_NONE:
			$error = ''; // JSON is valid // No error has occurred
			break;
		case JSON_ERROR_DEPTH:
			$error = 'The maximum stack depth has been exceeded.';
			break;
		case JSON_ERROR_STATE_MISMATCH:
			$error = 'Invalid or malformed JSON.';
			break;
		case JSON_ERROR_CTRL_CHAR:
			$error = 'Control character error, possibly incorrectly encoded.';
			break;
		case JSON_ERROR_SYNTAX:
			$error = 'Syntax error, malformed JSON.';
			break;
		// PHP >= 5.3.3
		case JSON_ERROR_UTF8:
			$error = 'Malformed UTF-8 characters, possibly incorrectly encoded.';
			break;
		// PHP >= 5.5.0
		case JSON_ERROR_RECURSION:
			$error = 'One or more recursive references in the value to be encoded.';
			break;
		// PHP >= 5.5.0
		case JSON_ERROR_INF_OR_NAN:
			$error = 'One or more NAN or INF values in the value to be encoded.';
			break;
		case JSON_ERROR_UNSUPPORTED_TYPE:
			$error = 'A value of a type that cannot be encoded was given.';
			break;
		default:
			$error = 'Unknown JSON error occured.';
			break;
	}
	if ($error !== '') {
		// $command = 'echo '.$error.' > /tmp/api.err';
		// echo(system ($command, $retval));
		file_put_contents('/var/www/html/its_web/data/log/API/API.log', '[From api.php] '.$error.PHP_EOL, FILE_APPEND | LOCK_EX);
		exit('Error From api.php: '.$error);
	}
	// everything is OK
	return $result;
}

$received ="";
// https://newbedev.com/how-handling-error-of-json-decode-by-try-and-catch

// $jsonObj  = json_decode($api, true);
$jsonObj  = json_validate($api);

foreach($jsonObj as $object) {

	$host = $object[server][host];
	$port = $object[server][port];

	if($host && $port){
		$hostNew = $host;
		$portNew = $port;
	} else {
		$hostNew = $cfg['tcpIpPort']['staticAddress'];
		$portNew = $cfg['portAPI'];
	}

	// 딕셔너리는 리스트 형식으로 변환후 전송한다
	if($object[trigger]) { // 트리거 명령은 따로 리스트가 아닌 딕셔너리 형태로 전송 해야 한다.
		$obj = json_encode($object);
	} else {
		$obj = '['.json_encode($object).']';
	}
	// echo $obj.'<br>';

	try {
		// 소켓 오브젝트를 만듭니다.
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($socket === false) {
			echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
		}
		// 접속을 합니다.
		$result = socket_connect($socket, $hostNew, $portNew); // 
		if ($result === false) {
			echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
		} 
		// 소켓 서버로 메시지를 보낸다. // 예 ?api=[{"gpio":{"status":"2","id":"R12","hold":"4","msg":""},"debug":true}]
		socket_write($socket, $obj, strlen($obj));
		// 소켓 서버로부터 메시지를 받는다.
		$received .= socket_read($socket, 1024);
	} finally {
		socket_close($socket);
	}
}

?>
<!DOCTYPE html>
<html><head></head>
<body><?=$received?></body>
</html>