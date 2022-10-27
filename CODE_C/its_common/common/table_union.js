// console.log(process.argv.length);
// /var/www/html/wits_web/theme/ecos-wits_optex/utility/nodeJs_table 
// $ node table_union.js
if (process.argv.length > 3) {
	var portIn = process.argv[2];
	var portOut = process.argv[3];
} else {
	var portIn = 64444; // 연결된 모든 센서의 모니터링을 위한 TCP Port  예: $_SERVER['SERVER_ADDR'].":".G5_CU_MASTER_PORT
	var portOut = 64446; // G5_CU_MASTER_PORT 데이터를 Node.js 서버가 읽고 G5_CU_MASTER_NODE_0 포트로 클라이언트 서비스
}

///////////////////////////////////////////////////
// 위트가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
// wits data -> port 8000 -> port 9000
///////////////////////////////////////////////////
var app = require('http').createServer(handler);
var io = require('socket.io')(app); // require('socket.io').listen(app);
var fs = require('fs');
var html = fs.readFileSync('table_union.html', 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

// 소켓을 통해 자료를 table.html로 전송한다.
function event_send(id, name, ip, model, board, tableID, status, msg) {
	// io.sockets.emit('message_to_client', { id: id, name: name, status: status, msg: msg });
	io.sockets.emit('message_to_client', { id: id, name: name, ip: ip, model: model, board: board, tableID: tableID, status: status, msg: msg });
	// console.log('message_to_client', { id: id, name: name, status: status, msg: msg });
}

app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 포트 8000으로 부터 받은 정보를 파싱한후 포트 9000으로 전달한다.
//////////////////////////////////////////////////////////
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
		var ip = obj['ip'];
		var model = obj['model'];
		var board = obj['board'];
		var tableID = obj['tableID'];
		var status = obj['status'];
		var msg = obj['msg'];
		
		event_send(id, name, ip, model, board, tableID, status, msg);
		
		socket.emit('received');
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');