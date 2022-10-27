///////////////////////////////////////////////////
// https://github.com/fivdi/onoff
// https://www.npmjs.com/package/onoff -- writeSync 모듈
// https://webofthings.org/2016/10/23/node-gpio-and-the-raspberry-pi/
///////////////////////////////////////////////////

var fs = require('fs');
var qs  = require('querystring');
var gpio = require('onoff').Gpio; 
var net = require('net');
var http = require('http');
var app = http.createServer(handler); // app.listen(port);
var io = require('socket.io').listen(app);
// var app = require('http').createServer(handler);

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfg = JSON.parse(fs.readFileSync('/home/pi/API3/itsAPI.json', 'utf8')); // 환경 파일 읽기
var cfgCam = JSON.parse(fs.readFileSync('/home/pi/API3/streaming.json', 'utf8')); // 환경 파일 읽기
var portIn = cfg.tcpIpPort.portIn;
var portOut = cfg.tcpIpPort.portOut;
var html = fs.readFileSync(cfg.file.html_target, 'utf8');
var loggerPath = cfg.loggerPath;

var crypto = require('crypto');

///////////////////////////////////////////////////////////
// Relay01 = { 1:18, 2:23, 3:24, 4:25 } # GPIO 논리:실제, 출력: 1 ~ 4
// Poweio01 = { 1:12 }
// Sensoio01 = { 1:19, 2:13, 3:6, 4:5, 5:22, 6:27, 7:17, 8:4 } # GPIO 입력: 1 ~ 8 예) GPIN[3] -> 6
///////////////////////////////////////////////////////////

// Gpio 방향설정을 'OUT'으로 하면 기존에 실행하고 있는 프로그램에 영향을 끼침.(?)
// Watch 기능을 사용하려먼 Edge값을 설정 해야 한다. both가 아닌경우 센서값에 반을이 없을수 있다. values are: 'none', 'rising', 'falling', 'both'. 
var API = new Array();
for (var key in cfg["setBD"]["setIO"]) {
	// check if the property/key is defined in the object itself, not in parent
	if (cfg["setBD"]["setIO"].hasOwnProperty(key)) {
		// console.log(key, cfg["setBD"]["setIO"][key]);
		if (cfg["setBD"]["setIO"][key]) {
			API[key] = new gpio(cfg["setBD"]["gpio"][key], 'out');
		} else {
			// API[key] = new gpio(cfg["setBD"]["gpio"][key], 'in', 'rising', {debounceTimeout: 100});
			API[key] = new gpio(cfg["setBD"]["gpio"][key], 'in', 'both');
		}
		// console.log(API[key])
	} // cfg["setBD"]["gpio"][key] -> 'io01'
}
for (var key in cfg["setBD"]["setPW"]) {
	// check if the property/key is defined in the object itself, not in parent
	if (cfg["setBD"]["setPW"].hasOwnProperty(key)) {
		// console.log(key, cfg["setBD"]["setPW"][key]);
		if (cfg["setBD"]["setPW"][key]) {
			API[key] = new gpio(cfg["setBD"]["gppw"][key], 'out');
		} else {
			// API[key] = new gpio(cfg["setBD"]["gppw"][key], 'in', 'rising', {debounceTimeout: 100});
			API[key] = new gpio(cfg["setBD"]["gppw"][key], 'in', 'both');
		}
		// console.log(API[key])
	} // cfg["setBD"]["gpio"][key] -> 'pw01'
}

const { exec } = require('child_process');
// https://stackabuse.com/executing-shell-commands-with-node-js/
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

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
	res.end(html);
}

function socket_write(host, port, data) {
	//////////////////////////////////////////////////////////
	// 전송용 코드
	// 네트워크상의 itsAPI.py로 전송
	// IP, Port, Data(Json), 센서감지에 따른 데이터를 
	//////////////////////////////////////////////////////////

	if(!host || !port) {
		host = cfg.tcpIpPort.staticAddress;
		port = cfg.portAPI;
	}

	data.forEach(function(value) {
		if(typeof value.server !== "undefined" && value.server.host && value.server.port) {
			// 사용자(custom) 스크립트만은 예외(전송시 관련 서버정보를 포함)
			if(typeof value.custom === "undefined") { // value.custom 인경우 변경없이 전송 한다.
				host = value.server.host;
				port = value.server.port;
			}
		}

		push_gLog('<font color=gray>Sent to '+host+':'+port+'</font> '+value); // Log -> index.html, 로그전송
		logger('Sent to '+host+':'+port+' '+JSON.stringify([value]));

		// delete value.server; // 더이상에 서버정보가 필요하지 않음(리소스 절약)

		var client = new net.Socket();
		// client.setTimeout(500);
		client.connect(port, host, function(){
			// console.log('CONNECTED TO: ' + host + ':' + port);
			client.write(JSON.stringify([value])); // JSON을 문자로
			client.destroy();
		});
		client.on('error', function(e) {
			if(e.code == 'ECONNREFUSED') {
				push_gLog('<font color=red>ERROR socket_write</font> '+' to ' + host + ':' + port);
				console.log('ERROR socket_write to ' + e.code + ' ' + host + ':' + port);
				// // 타이머 설정후 재시도 한다.
				// console.log('Is the server running at ' + port + '?');
				// client.setTimeout(4000, function() {
				// 	client.connect(port, host, function(){
				// 		console.log('CONNECTED TO: ' + host + ':' + port);
				// 		client.write(JSON.stringify([value]));
				// 	});
				// });
				// console.log('Timeout for 5 seconds before trying port:' + port + ' again');
			}   
		});
		client.on('data', function(data) {
			// console.log('DATA: ' + data);
			client.destroy();
		});
		client.on('close', function() {
			// console.log('Connection closed');
		});

	});
}

function btn_status_gpio(id, status, source) { // 예: id:io01/pw01/.., status:0/1, source:source
	//////////////////////////////////////////////////////////
	// 1. 외부 명령은 itsAPI.py로 전송한다.
	// 2. 버튼 상태를 index.html로 전송한다.
	//////////////////////////////////////////////////////////

	// 센서 이벤트에 외부명령이 존재하면 
	// 내용을 socket_write를 통해 itsAPI.py로 전송한다.
	if(source == 'watch' && cfg["command"][id] && cfg["execution"][id]) { // (센서이벤트발생 && 명령어가 있고 && 실행이 활성)
		if((status == cfg["trigger"][id])) { // 트리거와 상태값이 같으면 
			try {
				obj = JSON.parse(cfg["command"][id]); // String -> JSON
				socket_write(obj["host"], obj["port"], obj["data"]); // 명령은 itsAPI.py로 전송
				// console.log(obj["host"], obj["port"], obj["data"]);
				push_gLog('<font color=white>Sensor '+id+'</font> '+cfg["command"][id]); // Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red><font color=red>Json Format Error</font></font>(btn_status_gpio): '+e+' : '+id+' - '+cfg["command"][id]);
				return;
			}
		}
	}
	// 버튼 상태(status)를 index.html로 전송한다.
	try {
		// io.sockets.emit('btn_status_gpio', { id: id, status: status, source: source });
		io.sockets.emit('btn_status_gpio', { id: id, status: status });
		// console.log(id, status, source);
	} catch (e) {
		console.log('error btn_status_gpio');
	}
}

function btn_enable(myKey, myID, status) {
	if(myID == 'admin') {
		var btn_group = "<button id='save' type='button' class='btn btn-light ctrlBtn'>Save</button><button id='restart' type='button' class='btn btn-info ctrlBtn'>Restart</button><button id='reboot' type='button' class='btn btn-info ctrlBtn'>Reboot</button><div class='topBtn'><span id='gLogBtn' class='gLogBtn'>Log</span><span id='cfgSet' class='cfgSet'>Config</span><span id='setup' class='setup'>Setup</span></div>";
	} else if(myID == 'manager') {
		var btn_group = "<button id='save' type='button' class='btn btn-light ctrlBtn'>Save</button><button id='restart' type='button' class='btn btn-info ctrlBtn'>Restart</button><button id='reboot' type='button' class='btn btn-info ctrlBtn'>Reboot</button><div class='topBtn'><span id='gLogBtn' class='gLogBtn'>Log</span><span id='cfgSet' class='cfgSet'>Config</span></div>";
	} else {
		var btn_group = "";
	}
	try {
		io.sockets.emit('btn_enable', { myKey: myKey, code: btn_group, status: status } );
	} catch (e) {
		console.log('error btn_enable')
	}
}

// 로그 등록
function push_gLog(data) {
	// 로그 -> Client
	io.sockets.emit('push_gLog', data);
}

function logger(log) {
	// 로그 -> loggerPath
	var logIs = '[JS Log] ' + new Date().getTime() + ' > ' + log + '\n';
	fs.appendFile(loggerPath, logIs, function (err) {
	  if (err) throw err;
	  // console.log('Saved!');
	});	
}

function password_unmatch(myKey, clientIP) { // { myKey: data["myKey"], ip: clientIP }
	io.sockets.emit('password_unmatch', { myKey: myKey, clientIP: clientIP });
}

io.sockets.on('connection', function (socket) {
	//////////////////////////////////////////////////////////
	// 1. Client로 부터 이벤트를 받고 관련 작업 실행
	//////////////////////////////////////////////////////////
	// var address = socket.handshake.address;
	var clientIP = socket.handshake.address.split(':').pop(); // ::ffff:192.168.0.4 -> 192.168.0.4
	var allow = cfg["permission"]["filterIP"]["allow"].includes(clientIP); // 정상 IP가 접근 하는지 판단 True or False
	var deny = cfg["permission"]["filterIP"]["deny"].includes(clientIP); // 정상 IP가 접근 하는지 판단 True or False
	// console.log(clientIP);
	// if (deny) return; // 부정 접근

	// 클라이언트 사이드에서 최초 접근시 현상태 전송
	for (var key in cfg["setBD"]["setIO"]) { // cfg["setBD"]["gpio"][key] -> 'io01'
		btn_status_gpio(key,API[key].readSync(), '');
	}
	for (var key in cfg["setBD"]["setPW"]) { // cfg["setBD"]["gpio"][key] -> 'io01'
		btn_status_gpio(key,API[key].readSync(), '');
	}

	io.sockets.emit('global_var', cfg); // 초기화 - 전역변수 값을 itsAPI.html로 전송

	push_gLog('<font color=cyan>Connection from</font> '+clientIP); // Log -> index.html, 로그전송

	// 클라이언트 아이피 전송()
	socket.on('findClientIP', function(data) {
		// admin 사용자로 등록되었거나 콘솔 브라우저로 접근시 ..
		if (cfg.permission.filterIP.admin.split(',').indexOf(clientIP) > -1) { // admin 그룹이거나 Deaktop Server 인경우
			var userID = "admin";
		} else if (cfg.permission.filterIP.manager.split(',').indexOf(clientIP) > -1) { // manager 
			var userID = "manager";
		} else if (cfg.permission.filterIP.viewer.split(',').indexOf(clientIP) > -1) {
			var userID = "viewer";
		} else if (clientIP == cfg.tcpIpPort.staticAddress) { // admin 그룹이거나 Deaktop Server 인경우
			var userID = "admin";
		} else if (data["myPWD"] == cfg.permission.password.admin) { // 게스트 상태에서 어드민 로그인 하기
			var userID = "admin";
		} else {
			var userID = "guest";
		}

		// console.log(data["myPWD"]);
		io.sockets.emit('findClientIP', { myKey: data["myKey"], myIP: clientIP, myID: userID });
		if(userID == "admin") {
			io.sockets.emit('camera_var', cfgCam); // 초기화 - 카메라 아이템 값을 itsAPI.html로 전송
		}

	});

	// 클라이언트네서 버튼을 클릭하면 실행, 단 아이디 명에 따라 제한적 실행을 한다.
	socket.on('btnRelayClick', function(data) { // 릴레이컨트롤
		var id = data["id"]
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			if(cfg["setBD"]["setIO"][id] || cfg["setBD"]["setPW"][id]) { //  S : 센서 입력 포트, P : 센서 전원
				try {
					API[id].writeSync(API[id].readSync() ^ 1); // 토글
				} catch (e) {
					logger('writeSync error');
					console.log('writeSync error');
				}
			}
		} else {
			password_unmatch(data["myKey"], clientIP); // { myKey: data["myKey"], ip: clientIP }
		}
		btn_status_gpio(id,API[id].readSync(), ''); // 현재 설정된 값을 반환 한다.
	});

	socket.on('btnSensorClick', function(data) { // 센서 이벤트 강제 발생
		// console.log(data);
		logger(data["command"]);
		var id = data["id"]
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			try {
				obj = JSON.parse(data["command"]); // String -> JSON
				obj["data"].forEach(function(element){
					for (var key in element) {
						// console.log([element[key]][0].actID = id);
						[element[key]][0].actID = id;
					}
				});
				socket_write(obj["host"], obj["port"], obj["data"]); // 명령은 itsAPI.py로 전송
				push_gLog('<font color=green>btnSensorClick</font> '+data["command"]); // Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red>Json Format Error</font>(btnSensorClick): '+' '+e+' : '+data["command"]);
				return;
			}
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});

	socket.on('btnAlarmClick', function(data) { // 센서 이벤트 강제 발생
		var id = data["id"]
		logger(data["command"]);
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			// console.log(data["command"]);
			try {
				obj = JSON.parse(data["command"]); // String -> JSON
				socket_write(obj["host"], obj["port"], obj["data"]); // 명령은 itsAPI.py로 전송
				// console.log(obj["host"], obj["port"], obj["data"]);
				push_gLog('<font color=green>btnAlarmClick</font> '+data["command"]); // Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red>Json Format Error</font>(btnAlarmClick): '+' '+e+' : '+data["command"]);
				return;
			}
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});

	socket.on('btnTimerClick', function(data) { // 센서 이벤트 강제 발생
		logger(data["command"]);
		var id = data["id"]
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			// console.log(data["command"]);
			try {
				obj = JSON.parse(data["command"]); // String -> JSON
				socket_write(obj["host"], obj["port"], obj["data"]); // 명령은 itsAPI.py로 전송
				// console.log(obj["host"], obj["port"], obj["data"]);
				push_gLog('<font color=green>btnTimerClick</font> '+data["command"]); // Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red>Json Format Error</font>(btnTimerClick): '+' '+e+' : '+data["command"]);
				return;
			}
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});
	
	socket.on('btnStopAudioClick', function(data) { // 센서 이벤트 강제 발생
		logger(data["command"]);
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			// { myKey:myKey, myID:myID, password:$('#password').val(), command:[{"system":{"command":"stop_audio","value":"0"}}]}
			try {
				socket_write(cfg.tcpIpPort.staticAddress, cfg.portAPI, data["command"]); // 명령은 itsAPI.py로 전송
				// console.log(cfg.tcpIpPort.staticAddress, cfg.portAPI, data["command"]);
				push_gLog('<font color=green>btnStopAudioClick</font> '+data["command"]); // 데이터가 오브잭트이어서 JSON.stringify해줌 Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red>Json Format Error</font>(btnStopAudioClick): '+' '+e+' : '+data["command"]);
				return;
			}
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});

	socket.on('btnTalkingClick', function(data) { // 센서 이벤트 강제 발생
		logger(data["command"]);
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			try {
				socket_write(cfg.tcpIpPort.staticAddress, cfg.portAPI, data["command"]); // 명령은 itsAPI.py로 전송
				push_gLog('<font color=green>btnTalkingClick</font> '+data["command"]); // 데이터가 오브잭트이어서 JSON.stringify해줌 Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red>Json Format Error</font>(btnTalkingClick): '+' '+e+' : '+data["command"]);
				return;
			}
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});

	socket.on('btnSetTimeClick', function(data) { // 센서 이벤트 강제 발생
		logger(data["command"]);
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
			// { myKey:myKey, myID:myID, password:$('#password').val(), command:[{"system":{"command":"set_time","value":"2021-10-18 04:54:45"}}]}
			try {
				socket_write(cfg.tcpIpPort.staticAddress, cfg.portAPI, data["command"]); // 명령은 itsAPI.py로 전송
				// console.log(cfg.tcpIpPort.staticAddress, cfg.portAPI, data["command"]);
				push_gLog('<font color=green>btnSetTimeClick</font> '+data["command"]); // 데이터가 오브잭트이어서 JSON.stringify해줌 Log -> index.html, 로그전송
			} catch (e) {
				push_gLog('<font color=red>Json Format Error</font>(btnSetTimeClick): '+' '+e+' : '+data["command"]);
				return;
			}
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});

	socket.on('reboot_self', function (data) {
		logger('reboot_self');
		exec_command('sudo reboot');
	});

	socket.on('restart_self', function(data) {
		logger('restart_self');
		exec_command('python3 ./run_itsAPI.pyc');
	});

	socket.on('save_self', function (data) { // itsAPI.html로 부터 변경된 값을 config.json에 저장 한다.
		// console.log(data["config"]);
		var own = JSON.parse(fs.readFileSync('/home/pi/API3/config.json', 'utf8')); // 환경 파일 읽기
		for (var key in data["config"]) {
			if (data["config"].hasOwnProperty(key)) {
				if(key == 'password') {
					own["permission"][key][data["config"]["myID"]] = data["config"][key];
				} else if(key == 'alarmCmds') { 
					// console.log(data["config"]["alarmCmds"]);
					for (var key_a in data["config"]["alarmCmds"]) {
						for (var key_b in data["config"]["alarmCmds"][key_a]) {
							own["alarmCmds"][key_a][key_b] = data["config"]["alarmCmds"][key_a][key_b];
						}
					}
				} else if(key == 'timerCmds') { 
					// console.log(data["config"]["timerCmds"]);
					for (var key_t in data["config"]["timerCmds"]) {
						for (var key_b in data["config"]["timerCmds"][key_t]) {
							own["timerCmds"][key_t][key_b] = data["config"]["timerCmds"][key_t][key_b];
						}
					}
				} else if(key == 'command') {
					// own["command"] = data["config"]["command"]; // ioBoard 변경 -> 재실행시 오류
					for (var key_c in data["config"]["command"]) {
						// own_key_c = key_c.replace('cmd_', '');     
						own["command"][key_c] = data["config"]["command"][key_c];
					}
				} else if(key == 'trigger') {
					// own["trigger"] = data["config"]["trigger"];
					for (var key_c in data["config"]["trigger"]) {
						// own_key_c = key_c.replace('trg_', '');     
						own["trigger"][key_c] = data["config"]["trigger"][key_c];
					}
				} else if(key == 'execution') {
					// own["execution"] = data["config"]["execution"];
					for (var key_c in data["config"]["execution"]) {
						// own_key_c = key_c.replace('exe_', '');     
						own["execution"][key_c] = data["config"]["execution"][key_c];
					}
				} else if(key == 'description') {
					// own["description"] = data["config"]["description"];
					for (var key_c in data["config"]["description"]) {
						// own_key_c = key_c.replace('des_', '');     
						own["description"][key_c] = data["config"]["description"][key_c];
					}
				} else if(key == 'location') {
					own["location"] = data["config"]["location"];
				} else if(key == 'audioPlayer_set') {
					own["audio"]["player"] = data["config"]["audioPlayer_set"];
				} else if(key == 'audioEnable') {
					own["audio"]["enable"] = data["config"]["audioEnable"];
				} else if(key == 'talkEnable') {
					own["talk"]["enable"] = data["config"]["talkEnable"];
				} else if(key == 'mDVREnable') {
					own["mDVR"]["enable"] = data["config"]["mDVREnable"];
				} else if(key == 'ioBoard_set') {
					own["ioBoard"]["set"] = data["config"]["ioBoard_set"]; 
				} else if(key == 'camera_setName') {
					own["camera"]["name"] = data["config"]["camera_setName"];
				} else if(key == 'camera_setConfig') {
					own["camera"]["config"] = data["config"]["camera_setConfig"];
				} else if(key == 'staticAddress') {
					own["tcpIpPort"]["staticAddress"] = data["config"]["staticAddress"];
				} else if(key == 'staticNetMask') {
					own["tcpIpPort"]["staticNetMask"] = data["config"]["staticNetMask"];
				} else if(key == 'staticGateway') {
					own["tcpIpPort"]["staticGateway"] = data["config"]["staticGateway"];
				} else if(key == 'filterIP') {
					own["permission"]["filterIP"] = data["config"]["filterIP"];
				} else if(key == 'telegramBot01_token') {
					own["telegram"]["bot01"]["token"] = data["config"]["telegramBot01_token"];
				} else if(key == 'telegramBot01_chatID') {
					own["telegram"]["bot01"]["chatID"] = data["config"]["telegramBot01_chatID"];
				} else if(key == 'telegramBot02_token') {
					own["telegram"]["bot02"]["token"] = data["config"]["telegramBot02_token"];
				} else if(key == 'telegramBot02_chatID') {
					own["telegram"]["bot02"]["chatID"] = data["config"]["telegramBot02_chatID"];
				} else if(key == 'keySource') {
					own["permission"]["accessKey"]["keySource"] = data["config"]["keySource"];
					// 암호코드 생성
					own["permission"]["accessKey"]["keyCode"] = crypto.createHash('sha256').update(data["config"]["keySource"]).digest('hex');
				} else if(key == 'reportMail') {
					own["reportMail"] = data["config"]["reportMail"];
				} else {
					;
				}
			}
		}
		fs.writeFileSync('/home/pi/API3/config.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
		// var dateTime = new Date();
		// fs.writeFileSync('/home/pi/API3/'+dateTime+'.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
		
		cfg["command"] = own["command"]; // 변동값 적용
		cfg["trigger"] = own["trigger"]; // 변동값 적용
		cfg["execution"] = own["execution"]; // 변동값 적용
		cfg["description"] = own["description"]; // 변동값 적용

		cfg["alarmCmds"] = own["alarmCmds"]; // 변동값 적용 - 재시작
		cfg["timerCmds"] = own["timerCmds"]; // 변동값 적용 - 재시작

		cfg["location"] = own["location"];
		cfg["audio"]["player"] = own["audio"]["player"]; // 변동값 적용
		cfg["audio"]["enable"] = own["audio"]["enable"]; // 변동값 적용
		cfg["talk"]["enable"] = own["talk"]["enable"]; // 변동값 적용
		cfg["mDVR"]["enable"] = own["mDVR"]["enable"]; // 변동값 적용
		cfg["ioBoard"]["set"] = own["ioBoard"]["set"]; // 변동값 적용
		cfg["camera"]["name"] = own["camera"]["name"];

		cfg["tcpIpPort"]["staticAddress"] = own["tcpIpPort"]["staticAddress"];
		cfg["tcpIpPort"]["staticNetMask"] = own["tcpIpPort"]["staticNetMask"];
		cfg["tcpIpPort"]["staticGateway"] = own["tcpIpPort"]["staticGateway"];

		cfg["telegram"]["bot01"]["token"] = own["telegram"]["bot01"]["token"];
		cfg["telegram"]["bot01"]["chatID"] = own["telegram"]["bot01"]["chatID"];
		cfg["telegram"]["bot01"]["run"] = own["telegram"]["bot01"]["run"];
		cfg["telegram"]["bot02"]["token"] = own["telegram"]["bot02"]["token"];
		cfg["telegram"]["bot02"]["chatID"] = own["telegram"]["bot02"]["chatID"];
		cfg["telegram"]["bot02"]["run"] = own["telegram"]["bot02"]["run"];

		cfg["permission"]["filterIP"] = own["permission"]["filterIP"] ; // 적용
		cfg["permission"]["password"][data["config"]["myID"]] = own["permission"]["password"][data["config"]["myID"]]; // 비밀번호 적용
		cfg["permission"]["accessKey"] = own["permission"]["accessKey"] ; // 적용
		
		cfg["reportMail"] = own["reportMail"];
		
		io.sockets.emit('global_var', cfg); // 전역변수 값을 itsAPI.html로 전송
		// socket_write(cfg.tcpIpPort.staticAddress, cfg.portAPI, [{'global_var':cfg}]); // 전역변수 값을 itsAPI.py로 전송
		socket_write(cfg.tcpIpPort.staticAddress, cfg.portAPI, [{'global_var':own}]); // 전역변수 값을 itsAPI.py로 전송
	});

	socket.on('edit_self', function(data) { // { myKey:myKey, myID:myID, password:$('#password').val(), status:$(this).hasClass('active') });
		if(data["password"] == cfg["permission"]["password"][data["myID"]]) {
				btn_enable(data["myKey"], data["myID"], data["status"]);
		} else {
			password_unmatch(data["myKey"], clientIP);
		}
	});

});

app.listen(portOut); // Display server
console.log('\nGUI running at http://localhost:'+portOut+'/');

require('net').createServer(function (socket) {
	//////////////////////////////////////////////////////////
	// 수신용 코드
	// 2. 외부(itsAPI.py) -> portIn(18040) -> itsAPI.js -> itsAPI.html -> portOut(18080)
	// 예: id=ID : relay 번호, status=STATUS 0:off 1:on, source=source
	//////////////////////////////////////////////////////////
	
	// // 송신측에서 응답을 기다릴 경우를 대비 해서
	// socket.write("From .js - Received");

	// console.log('connected');
	socket.on('data', function (data) { // 외부 portIn 으로 부터 받은 데이터(예:'gpioID=io01,source=message')
		// console.log(JSON.parse(data));
		obj = JSON.parse(data)
		if(obj.name == 'gpioID') {
			// itsAPI.py로 부터 변화된 릴레이 상태를 적용 한다.
			if(cfg["setBD"]["setIO"][obj.value] || cfg["setBD"]["setPW"][obj.value]) { //  S/R : 센서 IO 포트, P : 센서 전원
				btn_status_gpio(obj.value, API[obj.value].readSync(), 'from portIn'); // 현재 설정된 값을 반환 한다.
			} else {
				console.log('error port not found');
			}
		} else if(obj.name == 'push_gLog') {
			push_gLog('<font color=orange>From Server(py)</font> '+obj.value); // Log -> index.html, 로그전송
		} else if(obj.name == 'heartbeat') {
			io.sockets.emit('heartbeat', obj.value);
		} else if(obj.name == 'btn_status_audio') {
			// btn_status_audio(obj.value); // Log -> index.html, 로그전송
			io.sockets.emit('btn_status_audio', obj.value);
		} else if(obj.name == 'btn_status_talk') {
			// btn_status_talk(obj.value); // Log -> index.html, 로그전송
			io.sockets.emit('btn_status_talk', obj.value);
		} else if(obj.name == 'btn_status_mDVR') {
			// btn_status_mDVR(obj.value); // Log -> index.html, 로그전송
			io.sockets.emit('btn_status_mDVR', obj.value);
		} else if(obj.name == 'btn_status_set_time') {
			// btn_status_set_time(obj.value); // Log -> index.html, 로그전송
			io.sockets.emit('btn_status_set_time', obj.value);
		} else if(obj.name == 'set_name') { // 센서 이벤트 활성
			var own = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
			own["location"] = obj.value;
			fs.writeFileSync('./config.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
			cfg["location"] = obj.value;
			io.sockets.emit('global_var', cfg); // 전역변수 값을 itsAPI.html로 전송
		} else if(obj.name == 'enable_audio') { // 센서 이벤트 활성
			var own = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
			own["audio"]["enable"] = 1
			fs.writeFileSync('./config.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
			cfg["audio"]["enable"] = 1;
			io.sockets.emit('global_var', cfg); // 전역변수 값을 itsAPI.html로 전송
		} else if(obj.name == 'disable_audio') { // 센서 이벤트 비활성
			var own = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
			own["audio"]["enable"] = 0
			fs.writeFileSync('./config.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
			cfg["audio"]["enable"] = 0;
			io.sockets.emit('global_var', cfg); // 전역변수 값을 itsAPI.html로 전송
		} else if(obj.name == 'enable_io') { // 센서 이벤트 활성
			var own = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
			own["execution"][obj.value] = 1;
			fs.writeFileSync('./config.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
			cfg["execution"][obj.value] = 1;
			io.sockets.emit('global_var', cfg); // 전역변수 값을 itsAPI.html로 전송
		} else if(obj.name == 'disable_io') { // 센서 이벤트 비활성
			var own = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
			own["execution"][obj.value] = 0;
			fs.writeFileSync('./config.json', JSON.stringify(own, null, 4), 'utf8'); // 환경 파일 저장
			cfg["execution"][obj.value] = 0;
			io.sockets.emit('global_var', cfg); // 전역변수 값을 itsAPI.html로 전송
		} else if(obj.name == 'trigger_io') { // 센서이벤트 발생시 또다른 센서 이벤트를 콜한다.  
			btn_status_gpio(obj.value, cfg["trigger"][obj.value], 'watch');
		} else if(obj.name == 'restart_self') { // 시스템 재실행
			exec_command('python3 ./run_itsAPI.pyc');
		} else {
			return;
		}
	});

	// socket.on('end',function(){
	// 	console.log('Client connection ended');
	// });

}).listen(portIn); // Receive server
// console.log('Receive server running at http://localhost:'+portIn+'/');

////////////////////////////////////////////////////
// 3. 물리적 변환 값 Watch 기능으로 부터 실행
// Object.entries 사용해야만 적용됨(이유는 모름 - 고생함)
// 기본값 - API["io01"].watch(function(err, state) { btn_status_gpio('io01',state, ''); });
// 모든 활성화된 포트를 감지함
///////////////////////////////////////////////////
Object.entries(cfg["setBD"]["gppw"]).forEach(([key, value]) => API[`${key}`].watch(function(err, state) { btn_status_gpio(`${key}`,state, 'watch'); }));
Object.entries(cfg["setBD"]["gpio"]).forEach(([key, value]) => API[`${key}`].watch(function(err, state) { btn_status_gpio(`${key}`,state, 'watch'); }));

// console.log(API);
console.log('Start ITS API');