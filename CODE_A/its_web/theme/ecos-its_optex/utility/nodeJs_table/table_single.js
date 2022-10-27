// console.log(process.argv.length);
if (process.argv.length >= 5) {
	var portIn = process.argv[2];
	var portOut = process.argv[3];
	var noOfZone = process.argv[4];
	var beep = process.argv[5]; // 변수가 1이면 소리 출력
} else {
	var portIn = 8000;
	var portOut = 9000;
	var noOfZone = 200;
	var beep = 1; // 변수가 1이면 소리 출력
}

///////////////////////////////////////////////////
// 위트가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
// wits data -> port 8000 -> port 9000
///////////////////////////////////////////////////
var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var path = require('path');

var appDir = path.dirname(require.main.filename);
// console.log(appDir)

if (noOfZone > 1) {
	var html = fs.readFileSync('table_GPIO.html', 'utf8');
} else {
	var html = fs.readFileSync('table_single.html', 'utf8');
}
function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

// 소켓을 통해 자료를 table.html로 전송한다.
function event_zone(id, name, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, zone, beep) {
	io.sockets.emit('message_to_client', { id: id, name: name, lat_s: lat_s, lng_s: lng_s, lat_e: lat_e, lng_e: lng_e, dist: dist, alarmOut: alarmOut, zone: zone, beep: beep });
}
function event_zone_OBJ(id, name, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, zone, length, time, speed, move, beep) {
	io.sockets.emit('message_to_client', { id: id, name: name, lat_s: lat_s, lng_s: lng_s, lat_e: lat_e, lng_e: lng_e, dist: dist, alarmOut: alarmOut, zone: zone, length: length, time: time, speed: speed, move: move, beep: beep });
}


		
app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 포트 8000으로 부터 받은 정보를 파싱한후 포트 9000으로 전달한다.
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    // console.log("connected");
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
        // console.log(data.toString());
		// alarmInfo 예: "A=1,B=32" 형식을 배열로 변공함
		var alarmInfo = data.toString();
		var obj = alarmInfo.split(",").reduce(function(o, c){
		   var arr = c.split("=");
		   return o[arr[0].trim()] = arr[1].trim(), o; // comma operator
		},{});
		var id = obj['id'];
		var name = obj['name'];
		var lat_s = obj['lat_s'];
		var lng_s = obj['lng_s'];
		var lat_e = obj['lat_e'];
		var lng_e = obj['lng_e'];
		var dist = obj['dist'];
		var alarmOut = obj['alarmOut'];
		var zone = obj['zone'];
		var length = obj['obj_length'];
		var time = obj['obj_time'];
		var speed = obj['obj_speed'];
		var move = obj['obj_move'];

		// event_zone(id, name, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, zone, beep);
		event_zone_OBJ(id, name, lat_s, lng_s, lat_e, lng_e, dist, alarmOut, zone, length, time, speed, move, beep);
		
		socket.emit('received');
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');