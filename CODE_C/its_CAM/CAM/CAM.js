///////////////////////////////////////////////////
// https://github.com/mafintosh/axis-camera
// https://www.dev2qa.com/node-js-tcp-socket-client-server-example/
///////////////////////////////////////////////////


var fs = require('fs');

///////////////////////////////////////////////////////////////////////////////
// config.json 파일을 읽어 환경설정 한다.
///////////////////////////////////////////////////////////////////////////////
var cfg = JSON.parse(fs.readFileSync('config.json', 'utf8')); // 환경 파일 읽기

var portOut = cfg.interface.portOut; // ICS Manager가 CAM.js를 접근하는 포트 node main Port
var portIn = cfg.interface.portIn; // 사용자가 ICS Manager를 접근하는 포트 py_portOut
var portIO = cfg.interface.portIO; // 센서가 CAM.js를 접근하는 포트

var html = fs.readFileSync(cfg.file.html_dst, 'utf8');

var http = require('http').createServer(function (req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.writeHead(200, { 'Content-Type': 'text/html'});
//	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
	res.end(html);
});
http.listen(portOut); // Display server  ICS Manager
console.log('\n\tOpened Node Port Main: '+portOut);

function saveConfigJson() {
	fs.writeFile("config.json", JSON.stringify(cfg, null, 4), (err) => {
		if (err) throw err;
		// console.log('The file has been saved!');
	});
}

//////////////////////////////////////////////////////////
// 센서ITS로 부터 정보를 받아 관련작업 수행(파싱) / portOut으로 전달한다.
// 예: id=ID, status=STATUS, msg=MSG
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    socket.on('data', function (data) { // 외부 portIO 으로 부터 받은 정보를 data 변수에 저장
		var alarmInfo = data.toString();
		// console.log(alarmInfo);
    });
}).listen(portIO); // Receive server

// Py Client CAM.py로 부터 받은 데이터를 확인후 ICS Manager로 보낸다.
// CAM.py --> CAM.js --> CAM.html(io.sockets.emit)
// client.connect({host: '127.0.0.1', port: portIn}, function() {

var io = require('socket.io').listen(http);
var net = require('net');
var client = new net.Socket();

client.connect({host: '', port: portIn}, function() {
	// console.log('\tConnect Py Server Port: '+portIn);
	// 들어온 패킷의 Json 정보를 구분하여 브라우저(CAM.html)로 목적에 따른 명령을 전송 한다.
	client.on('data', function (data) {
		try {
			// console.log('Receive client send data : ' + data + ', data size : ' + client.bytesRead);
			var commandDict = JSON.parse(data)
			// console.log(commandDict)
			if(commandDict['query'] == 'limits') {
				io.sockets.emit('cameraLimits', commandDict); // Py에서 data_dump = json.dumps(retuenValue) ## JSON 형식 변환	
			} else if(commandDict['query'] == 'position') {
				io.sockets.emit('cameraPosition', commandDict); // Py에서 data_dump = json.dumps(retuenValue) ## JSON 형식 변환	
			} else if(commandDict['reqFrom'].match(/^ctrl_/)) { // info 요청이 아닌 조정(ctrl)인 경우 (CAM.html)로 전송
				io.sockets.emit('cameraInformation', commandDict); // Py에서 data_dump = json.dumps(retuenValue) ## JSON 형식 변환	
			}
		} catch (e) {
			console.error("Client.on Error:", e.message, commandDict, data);
		}
	});
});

// 카메라 어카운트 정보 전송
function camAccInfo(obj) {
	io.sockets.emit('camAccInfo', { 
		addr: cfg.camera.addr,
		user: cfg.camera.user,
		pass: cfg.camera.pass,
		license: cfg.license.manager_key,
	});
}

// 카메라 어카운트 정보 저장
function camAccSave(obj) {
	if (obj.addr) { cfg.camera.addr = obj.addr; }
	if (obj.user) { cfg.camera.user = obj.user; }
	if (obj.pass) { cfg.camera.pass = obj.pass; }
	if (obj.license) { cfg.license.manager_key = obj.license; }
	saveConfigJson();
}

// 관련 브라우저 또는 외부에서 받은 명령어를 Py Server CAM.py에 명령을 보낸다.(client.write)
// CAM.html --> CAM.js --> CAM.py(client.write)
// Other Socket --> CAM.js --> CAM.py(client.write)
io.sockets.on('connection', function (socket) { // 내부 Client로 부터 받은 작업 실행
	var clientIP = socket.handshake.address.replace(/^.*:/, ''); //  접근자 아이피
	
	socket.on('camAccInfo', function(data) { camAccInfo(); });
	socket.on('camAccSave', function(data) { camAccSave(data); });
	socket.on('camRestart', function(data) { client.write('ctrl_' + clientIP + '&' + 'cmd=camRestart'); });

	socket.on('center', function(data) { 
		client.write('ctrl_' + clientIP + '&' + data); 
		client.write('info_' + clientIP + '&query=position'); 
	});
	socket.on('move', function(data) { client.write('ctrl_' + clientIP + '&' + 'move='+data); });
	socket.on('pan', function(data) { client.write('ctrl_' + clientIP + '&' + 'pan='+parseFloat(data)); });
	socket.on('tilt', function(data) { client.write('ctrl_' + clientIP + '&' + 'tilt='+parseFloat(data)); });
	socket.on('zoom', function(data) { client.write('ctrl_' + clientIP + '&' + 'zoom='+parseInt(data)); });
	socket.on('focus', function(data) { client.write('ctrl_' + clientIP + '&' + 'focus='+parseInt(data)); });
	socket.on('iris', function(data) { client.write('ctrl_' + clientIP + '&' + 'iris='+parseInt(data)); });
	socket.on('rPan', function(data) { client.write('ctrl_' + clientIP + '&' + 'rpan='+parseFloat(data)); });
	socket.on('rTilt', function(data) { client.write('ctrl_' + clientIP + '&' + 'rtilt='+parseFloat(data)); });
	socket.on('rZoom', function(data) { client.write('ctrl_' + clientIP + '&' + 'rzoom='+parseInt(data)); });
	socket.on('rFocus', function(data) { client.write('ctrl_' + clientIP + '&' + 'rfocus='+parseInt(data)); });
	socket.on('rIris', function(data) { client.write('ctrl_' + clientIP + '&' + 'riris='+parseInt(data)); });
	socket.on('rBrightness', function(data) { client.write('ctrl_' + clientIP + '&' + 'rbrightness='+parseInt(data)); }); 
	socket.on('aFocus', function(data) { client.write('ctrl_' + clientIP + '&' + 'autofocus='+data); });
	socket.on('aIris', function(data) { client.write('ctrl_' + clientIP + '&' + 'autoiris='+data); });
	socket.on('presetposno', function(data) { client.write('ctrl_' + clientIP + '&' + 'gotoserverpresetname='+data); });
	socket.on('normal', function(data) { client.write('ctrl_' + clientIP + '&' + data); });
	
	socket.on('query', function(data) { client.write('info_' + clientIP + '&' + 'query='+data); });

});