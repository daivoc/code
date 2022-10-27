///////////////////////////////////////////////////
// https://github.com/fivdi/onoff
// https://www.npmjs.com/package/onoff -- writeSync 모듈
// https://webofthings.org/2016/10/23/node-gpio-and-the-raspberry-pi/
///////////////////////////////////////////////////

var fs = require('fs');
var net = require('net');
var http = require('http');
var app = http.createServer(handler); // app.listen(port);
var io = require('socket.io').listen(app);

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfg = JSON.parse(fs.readFileSync('/home/pi/FSI/FSI.json', 'utf8')); // 환경 파일 읽기
var html = fs.readFileSync(cfg.nodejs.html_target, 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
	res.end(html);
}

// https://stackabuse.com/executing-shell-commands-with-node-js/
const { exec } = require('child_process');
function exec_command(command) {
	exec(command, (error, stdout, stderr) => {
		if (error) {
			console.log(`error: ${error.message}`);
			return;
		}
		if (stderr) {
			console.log(`stderr: ${stderr}`);
			return;
		}
		// console.log(`stdout: ${stdout}`);
	});
}

app.listen(cfg.nodejs.port_js_to_html); // Display server
console.log('GUI running at http://localhost:'+cfg.nodejs.port_js_to_html+'/');

//////////////////////////////////////////////////////////
// 1. Client로 부터 이벤트를 받고 관련 작업 실행
// From FSI.html
//////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) {
	// var address = socket.handshake.address;
	var clientIP = socket.handshake.address.split(':').pop(); // ::ffff:192.168.0.4 -> 192.168.0.4
	console.log(clientIP);
	// var allow = cfg["permission"]["filterIP"]["allow"].includes(clientIP); // 정상 IP가 접근 하는지 판단 True or False
	// var deny = cfg["permission"]["filterIP"]["deny"].includes(clientIP); // 정상 IP가 접근 하는지 판단 True or False
	// if (deny) return; // 부정 접근

	// io.sockets.emit('global_var', cfg); // 초기화 - 전역변수 값을 FSI.html로 전송

	socket.on('send_ping', function (data) {
		console.log('user command: '+data["key"]);
		exec_command('touch '+cfg.pathUserCmd+'/'+data["key"]);
	});

	socket.on('reboot_self', function (data) {
		console.log('reboot_self',data);
		exec_command('sudo reboot');
	});

	socket.on('restart_self', function(data) {
		console.log('restart_self',data);
		exec_command('python run_FSI.pyc > /tmp/fsi.log');
	});
});

//////////////////////////////////////////////////////////
// 2. 송(to html)수신(fr py)용 코드
// 외부(FSI.pyc) -> cfg.nodejs.port_py_to_js(52011) -> FSI.js -> port_js_to_html(52012) -> FSI.html
// 예: {"id":"deviceName", "value":{"deviceName": deviceName}}
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
	socket.on('data', function (data) { // 외부 port_py_to_js 으로 부터 받은 데이터
		// 파이선 FSI.py의 function sendDataToSocket()에서 JS 포트(port_py_to_js)를 통해 여기로 옴
		// 접수된 데이터는 바로 FSI.html로 전송
		// console.log(JSON.parse(data));
		obj = JSON.parse(data)
		io.sockets.emit(obj.id, obj.value);
	});
}).listen(cfg.nodejs.port_py_to_js); // Receive server
