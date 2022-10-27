///////////////////////////////////////////////////
// its가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
// 참고 : https://openclassrooms.com/courses/ultra-fast-applications-using-node-js/socket-io-let-s-go-to-real-time
///////////////////////////////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var path = require('path');

var portIn = process.argv[2];
var portOut = process.argv[3];
var fileSync = process.argv[4];

var html = fs.readFileSync(fileSync, 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

// 소켓을 통해 자료를 table.html로 전송한다.
function emit_event(ip, serial, subject, dirStat, valueIs, eventOn, beep) {
	io.sockets.emit('message_to_client', { ip: ip, serial: serial, subject: subject, dirStat: dirStat, valueIs: valueIs, eventOn: eventOn, beep: beep });
}
		
app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 포트 8000으로 부터 받은 정보를 파싱한후 포트 9000으로 전달한다.
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    // console.log("connected");
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
        // console.log(data.toString()); // ip=192.168.0.9,serial=g300t200_192_168_0_9_0001,subject=ULTRASONIC,dirStat=50,valueIs=231,eventOn=Left
		var alarmInfo = data.toString();
		var obj = alarmInfo.split(",").reduce(function(o, c){
		   var arr = c.split("=");
		   return o[arr[0].trim()] = arr[1].trim(), o; // comma operator
		},{});
		var ip = obj['ip'];
		var serial = obj['serial'];
		var subject = obj['subject'];
		var dirStat = obj['dirStat'];
		var valueIs = obj['valueIs'];
		var eventOn = obj['eventOn'];
		var beep = 1;

		emit_event(ip, serial, subject, dirStat, valueIs, eventOn, beep);
		
		socket.emit('received');
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');