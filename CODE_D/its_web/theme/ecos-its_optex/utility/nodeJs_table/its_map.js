///////////////////////////////////////////////////
// its가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
///////////////////////////////////////////////////
var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var path = require('path');

var appDir = path.dirname(require.main.filename);
// console.log(appDir)

var portIn = process.argv[2];
var portOut = process.argv[3];

var html = fs.readFileSync('its_map.html', 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

// 소켓을 통해 자료를 table_BSS_map.html로 전송한다.
function event_zone_OBJ(id, name) {
	io.sockets.emit('message_to_client', { id: id, name: name });
}
		
app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

///////////////////////////////////////////////////////////////////////////////
// 포트 8000(portIn)으로 부터 받은 정보를 파싱한후 포트 9000(portOut)으로 전달한다.
///////////////////////////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    // console.log("connected");
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
		var alarmInfo = data.toString();
		var obj = alarmInfo.split(",").reduce(function(o, c){
		   var arr = c.split("=");
		   return o[arr[0].trim()] = arr[1].trim(), o; // comma operator
		},{});
		var id = obj['id'];
		var name = obj['name'];

		event_zone_OBJ(id, name);
		
		socket.emit('received');
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');