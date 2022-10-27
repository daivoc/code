///////////////////////////////////////////////////
// REQUIRED:
// npm i socket.io
///////////////////////////////////////////////////

const app = require('http').createServer(handler);
const io = require('socket.io')(app);
const fs = require('fs');

const net = require('net');

const { exec } = require('child_process');

///////////////////////////////////////////////////////////////////////////////
// config.json 파일을 읽어 환경설정 한다.
///////////////////////////////////////////////////////////////////////////////
var cfg = JSON.parse(fs.readFileSync('./config_RLS3.json', 'utf8')); // 환경 파일 읽기
var portIn = cfg["port"]["nodeIn"];
var portOut = cfg["port"]["nodeOut"];

///////////////////////////////////////////////////////////////////////////////
// Html 파일, Client
///////////////////////////////////////////////////////////////////////////////
var html = fs.readFileSync(cfg.file.templet.target, 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

// 환경변수(config.json) 저장
function saveConfigJson(target, cfg) {
	fs.writeFile(target, JSON.stringify(cfg, null, 4), (err) => {
		if (err) throw err;
	});
}

// 환경변수(config.json)에 저장된 마스킹 정보
function readMasking() {
	var masking = '';
	var classmem = cfg.filter.masking;
	for (item in classmem) {
		for (subItem in classmem[item]) {
			// 텍스트 위치 보정 500, 1500 -  주프로그램에서 클릭시 path 를 우선하기 위해 text를 먼저 출력한다.
			masking += "<text class='"+subItem+"' x='"+(cfg.filter.maskCoord[item][subItem][0]+200)+"' y='"+(cfg.filter.maskCoord[item][subItem][1]+400)+"' text-anchor='right' style='fill:gray; font-size:10cm;' >"+subItem+"</text>";
			masking += '<path class="'+item+'" id="'+subItem+'" d="'+classmem[item][subItem]+'"></path>';
		}
	}
	io.sockets.emit('readMasking', masking); // 클라이언트동기화 
}

function setMasking(data) {
	// console.log(data);
	coord = data.value.split(" ");
	coordS = coord[0].substring(1).split(","); // M32761.745962445624,54930.81088586822 -> 32761.745962445624,54930.81088586822 -> 32761, 54930
	
	coordSx = parseInt(coordS[0]);
	coordSy = parseInt(coordS[1]);
	coordEx = coordSx + parseInt(coord[1].substring(1).split(",")[0]); // l16682.344050231957,0 -> 16682.344050231957,0 -> 16682.344050231957 -> 16682
	coordEy = coordSy + parseInt(coord[2].split(",")[1]); // 0,19295.24131111164 -> 19295.24131111164 -> 19295
	// 실제 Vector 값으로 변환한 값을 maskCoord에 저장
	cfg.filter.maskCoord[data.mask][data.id] = [coordSx,coordSy,coordEx,coordEy];
	cfg.filter.masking[data.mask][data.id] = data.value;
	mask = {
		"maskCoord" : cfg.filter.maskCoord,
		"masking" : cfg.filter.masking
	}
	saveConfigJson(cfg.path.data+"/filter.json", cfg.filter);
}

function delMasking(data) {
	delete (cfg.filter.masking[data.mask][data.id]);
	delete (cfg.filter.maskCoord[data.mask][data.id]);
	mask = {
		"maskCoord" : cfg.filter.maskCoord,
		"masking" : cfg.filter.masking
	}
	saveConfigJson(cfg.path.data+"/filter.json", cfg.filter);
}

function setSize(data) {
	var a = parseInt(data.a);
	var b = parseInt(data.b);
	if (a > b) {
		cfg.filter.size["min"] = b;
		cfg.filter.size["max"] = a;
	} else {
		cfg.filter.size["min"] = a;
		cfg.filter.size["max"] = b;
	}
	// saveConfigJson(cfg.path.data+"/filter.json", cfg.filter);
}

function setDue(data) {
	cfg.filter.hold.due = parseInt(data.dueTime);
	// saveConfigJson(cfg.path.data+"/filter.json", cfg.filter);
}

function setCont(data) {
	cfg.filter.hold.cont = parseInt(data.contQty);
	cfg.filter.hold.keep = data.contKeep;
	// saveConfigJson(cfg.path.data+"/filter.json", cfg.filter);
}

// function cmdGetInfoStatus() {
// 	// var cmd = 'wget -qO - http://root:RLS-3060V@192.168.168.30/api/info/status/get/'
// 	// {"profile":0,"usage":{"cpu":90,"memory":62},"windowSoiling":0,"temp":41.3}
// 	var cmd = 'wget -qO - http://'+cfg.sensor.user+':'+cfg.sensor.pass+'@'+cfg.sensor.addr+cfg.sensor.cmd.gInfoStatus;
// 	try {
// 		require('child_process').exec(cmd, function (error, stdout, stderr) {
// 			var events = JSON.parse(stdout);
// 			// console.log(events);
// 			cfg.gInfoStatus = events
// 			io.sockets.emit('cmdGetInfoStatus', cfg.gInfoStatus);
// 		});
// 	} catch {
// 		return;
// 	}
// }
// setInterval(cmdGetInfoStatus, 300000); // 60000(1분) 

function cmdGetInfoStatus() {
	// https://stackabuse.com/executing-shell-commands-with-node-js/
	// var cmd = 'wget -qO - http://root:RLS-3060V@192.168.168.30/api/info/status/get/'
	// {"profile":0,"usage":{"cpu":90,"memory":62},"windowSoiling":0,"temp":41.3}
	var cmd = 'wget -qO - http://'+cfg.sensor.user+':'+cfg.sensor.pass+'@'+cfg.sensor.addr+cfg.sensor.cmd.gInfoStatus;
	exec(cmd, (err, stdout, stderr) => {
		if (err) {
			return;
		}
		var events = JSON.parse(stdout);
		cfg.gInfoStatus = events
		io.sockets.emit('cmdGetInfoStatus', cfg.gInfoStatus);
		// console.log(`stdout: ${stdout}`);
		// console.log(`stderr: ${stderr}`);
	});
}
setInterval(cmdGetInfoStatus, 300000); // 60000(1분) 

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
		console.log(`stdout: ${stdout}`);
	});
}

app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 파이선(realtime_html)에서 받은 정보를 파싱한 후 사용하거나 Html 클라이언트로 전달한다.
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
		// events: {'id': 0, 'kind': 'candidate', 'initialPos': {'x': -2440, 'y': 3651}, 'currentPos': {'x': -2440, 'y': 3651}, 'distance': 4392, 'step': 515, 'size': 76}
		var events = JSON.parse(data);
		// console.log(events);
		io.sockets.emit('liveEventData', events);
		// io.sockets.emit('liveLocation', {events: [ (events.initialPos.x * events.initialPos.y), events.currentPos.x, events.currentPos.y, events.size ]});
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');

///////////////////////////////////////////////////////////////////////////////
// 클라이언트(portOut)의 명령 정보를 파싱한후 작업하고 결과 전달하거나 내용을 저장한다.
///////////////////////////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) { // 내부 Client로 부터 받은 작업 실행
	//////////////////////////////////////////////////////////
	// var address = socket.handshake.address;
	var clientIP = socket.handshake.address.split(':').pop(); // ::ffff:192.168.0.4 -> 192.168.0.4
	var allow = cfg["permission"]["filterIP"]["allow"].includes(clientIP); // 정상 IP가 접근 하는지 판단 True or False
	var deny = cfg["permission"]["filterIP"]["deny"].includes(clientIP); // 정상 IP가 접근 하는지 판단 True or False

	// console.log(cfg.permission.filterIP.allow.length, allow, deny)
	// console.log(clientIP);
	if (deny) process.exit(); // 부정 접근

	io.sockets.emit('global_var', cfg); // 초기화 - 전역변수 값을 itsAPI.html로 전송

	// push_gLog('<font color=cyan>Connection from</font> '+clientIP); // Log -> index.html, 로그전송

	// 클라이언트 아이피 전송()
	socket.on('findClientIP', function(data) {
		// admin 사용자로 등록되었거나 콘솔 브라우저로 접근시 ..
		if (cfg.permission.filterIP.admin.split(',').indexOf(clientIP) > -1) { // admin 그룹이거나 Deaktop Server 인경우
			var userID = "admin";
		} else if (cfg.permission.filterIP.manager.split(',').indexOf(clientIP) > -1) { // manager 
			var userID = "manager";
		} else if (cfg.permission.filterIP.viewer.split(',').indexOf(clientIP) > -1) {
			var userID = "viewer";
		// } else if (clientIP == cfg.tcpIpPort.staticAddress) { // admin 그룹이거나 Deaktop Server 인경우
		// 	var userID = "admin";
		// } else if (data["myPWD"] == cfg.permission.password.admin) { // 게스트 상태에서 어드민 로그인 하기
		// 	var userID = "admin";
		} else {
			var userID = "guest";
		}
		// console.log(data["myPWD"]);
		io.sockets.emit('findClientIP', { myKey: data["myKey"], myIP: clientIP, myID: userID });
	});
	//////////////////////////////////////////////////////////

	socket.on('setMasking', function(data) { // SVG View Point 관련
		setMasking(data);
		readMasking(); // 클라이언트동기화 
		saveConfigJson('config_RLS3.json', cfg);
	});
	
	socket.on('delMasking', function(data) { // SVG View Point 관련
		// console.log('delMasking ' + data.id + ' ' + data.mask); 
		delMasking(data);
		readMasking(); // 클라이언트동기화 
		saveConfigJson('config_RLS3.json', cfg);
	});
	
	socket.on('readMasking', function() { // 환경값을 클라이언트로 전송()
		readMasking(); // 클라이언트동기화 
	});

	socket.on('setLevel', function(data) { // SVG View Point 관련
		// data.level, data.hold.cont, data.hold.cont, data.hold.cont, data.size.max, data.size.max
		cfg.level[data.level].hold=data.hold;
		cfg.level[data.level].size=data.size;
		cfg.level[data.level].reset=data.reset;
		saveConfigJson(cfg.path.data+"/level.json", cfg.level);
		saveConfigJson('config_RLS3.json', cfg);
	});

	socket.on('readLevel', function(data) { // 이벤트 등급값을 클라이언트로 전송()
		io.sockets.emit('readLevel', cfg.level[data]); // 클라이언트동기화 
	});
	
	// socket.on('setConfig', function(data) { // config.json 원본을 수정함
	// 	var config = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
	// 	config.server.ims.addr=data.imsIP;
	// 	config.permission.filterIP.manager=data.manager;
	// 	config.permission.filterIP.deny=data.denyIP;
	// 	saveConfigJson('config.json', config);
	// });

	// socket.on('readConfig', function() { // 이벤트 등급값을 클라이언트로 전송()
	// 	var data = {};
	// 	data["imsIP"] = cfg.server.ims.addr;
	// 	data["manager"] = cfg.permission.filterIP.manager;
	// 	data["denyIP"] = cfg.permission.filterIP.deny;
	// 	io.sockets.emit('readConfig', data); // 클라이언트동기화 
	// });

	socket.on('cmdGetInfoStatus', function() { // 센서 상태을 클라이언트로 전송()
		io.sockets.emit('cmdGetInfoStatus', cfg.gInfoStatus);
	});

	socket.on('reboot_self', function (data) {
		exec_command('sudo reboot');
	});

	socket.on('restart_self', function(data) {
		exec_command('python3 ./run_RLS3.pyc');
	});

});	
