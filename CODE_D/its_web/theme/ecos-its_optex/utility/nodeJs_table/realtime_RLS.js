// console.log(process.argv.length);
var portIn = process.argv[2];
var portOut = process.argv[3];

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');

var html = fs.readFileSync('realtime_RLS_'+portIn+'.html', 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

// // 소켓을 통해 자료를 realtime_RLS.html로 전송한다.
// function event_zone(id, name, lat_s, lng_s, lat_e, lng_e, ignore, alarmOut, area, zone, beep) {
	// io.sockets.emit('message_to_client', { id: id, name: name, lat_s: lat_s, lng_s: lng_s, lat_e: lat_e, lng_e: lng_e, ignore: ignore, alarmOut: alarmOut, area:area, zone: zone, beep: beep });
// }

// 소켓을 통해 자료를 realtime_RLS.html로 전송한다.
function obj_location(objInfo) {
	io.sockets.emit('message_to_client', { objInfo: objInfo });
}

app.listen(portOut); // Display server
// console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 포트 8000으로 부터 받은 정보를 파싱한후 포트 9000으로 전달한다.
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
		// 예: '4294967279654,1085,788,116|4294967279654,493,732,452|4294967279654,228,836,104| ~ 1,2,3,4|1,2,3,4|
		var objInfo = data.toString();
		// obj_location(objInfo); // 자료 전송
		
		var objInfoAll = objInfo.split('|');
		for(i = 0; i < objInfoAll.length; i++) {
			var cood_xyr = objInfoAll[i].split(',');
			// 이유는 모르겠으나 4개의 요소를 전송해야 하는데 첫번째 요소가 제거되는 상황을 피하기 위함
			if (cood_xyr.length == 4) {
				obj_location(objInfoAll[i]); // 자료 전송
				// console.log("cood_xyr",objInfoAll[i]);
			}
		}
		
    });
}).listen(portIn); // Receive server
// console.log('Receive server running at http://localhost:'+portIn+'/');