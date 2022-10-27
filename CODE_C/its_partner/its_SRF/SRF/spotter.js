///////////////////////////////////////////////////
// its가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
// 참고 : https://openclassrooms.com/courses/ultra-fast-applications-using-node-js/socket-io-let-s-go-to-real-time
///////////////////////////////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var net = require('net');

///////////////////////////////////////////////////////////////////////////////
// config.json 파일을 읽어 환경설정 한다.
///////////////////////////////////////////////////////////////////////////////
var cfg = JSON.parse(fs.readFileSync('config.json', 'utf8')); // 환경 파일 읽기
// var cfg = JSON.parse(fs.readFileSync(cfg.path.webRoot+'/'+cfg.path.config+'/config.json', 'utf8')); // 환경 파일 읽기
var lan = JSON.parse(fs.readFileSync('language.json', 'utf8')); // 환경 파일 읽기
var portIn = cfg.interface.portIn;
var portOut = cfg.interface.portOut;
var jsonPath = cfg.path.webRoot+cfg.path.json;
var loggerFile = cfg.path.webRoot+cfg.path.log+'/'+cfg.sensor.name+'.log';

var html = fs.readFileSync(cfg.path.spotter+cfg.file.html_dst, 'utf8');

var exec = require('child_process').exec;

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

/////////////////////
// asix 카메라 PTZ Control
// https://github.com/mafintosh/axis-camera
// https://www.npmjs.com/package/request
// ex) http://192.168.0.38/axis-cgi/com/ptz.cgi?pan=0&tilt=0&zoom=1&focus=1&iris=1&brightness=1&autofocus=on
/////////////////////
var request = require('request')
function ptzSetPos(query) { // 쿼리명령 수행
	request.get('http://'+cfg.camera.addr+cfg.camera.ptzCommand+query, {
		'auth': {
			'user': cfg.camera.user,
			'pass': cfg.camera.pass,
			'sendImmediately': false
		}
	}, function (error, response, body) {
		// console.log('error:', error); // Print the error if one occurred
		// console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
		// console.log('body:', body); // Print the HTML for the Google homepage.
	});
}

function setCamera() { // ptzGetInfo("query=position")
	// 기준위치 설정
	var query = "query=position";
	request.get('http://'+cfg.camera.addr+cfg.camera.ptzCommand+query, {
		'auth': {
			'user': cfg.camera.user,
			'pass': cfg.camera.pass,
			'sendImmediately': false
		}
	}, function (error, response, body) {
		// console.log('error:', error); // Print the error if one occurred
		// console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
		// console.log('body:', body); // Print the HTML for the Google homepage.

		if (body === undefined) { // 카메라 설정 오류 발생
			return 'Undefined setCamera';
		}	
		  
		var arr = body.split('\r\n');
		for (var i = 0; i < arr.length; i++) {
			data = arr[i].split('=');
			if(data[0]=="pan") {
				// console.log(data[1]);
				cfg.camera.calibration.angleOffset = data[1];
				cfg.camera.calibration.pan = data[1];
			} else if(data[0]=="tilt") {
				cfg.camera.calibration.tilt = data[1];
			}
		}
		saveConfigJson(); // 카메라 위치 값 저장
	});
}

//////////////////
// 시스템 명령

// function systemCmd(obj) {
// 	// exec('python spotter.pyc', (e, stdout, stderr)=> {
// 	exec(obj, (e, stdout, stderr)=> {
// 		if (e instanceof Error) {
// 			console.error(e);
// 			throw e;
// 		}
// 		console.log('stdout ', stdout);
// 		console.log('stderr ', stderr);
// 	});
// }
function executeCmd(cmd, callback) {
	try {
		exec(cmd, (error, stdout, stderr) => {
			if (error) {
				response = `{"error": ${error.message}}`;
				// console.log(response);
				logger('Error executeCmd '+response);
				return;
			}
			if (stderr) {
				response = `{"stderr": ${stderr}}`;
				// console.log(response);
				logger('Error executeCmd '+response);
				return;
			}
			response = `{"stdout": ${stdout}}`;
			// console.log(response);
			callback(response);
		});
	} catch (e) {
		// console.log('Error - exec ' + cmd);
		logger('executeCmd '+cmd);
		return 0;
	}
}

//////////////////////////////////////
// 리눅스 시스템 명령 넷켓을 통해 TCP 전송을 하는 기능
// 원격지에서 실행되는 API 소켓을 통해 
// 사전에 선언된 센서(8개)의 내용을 실행 한다
// 예: key값인 io01 ~ io08 내에 사전 선언된 명령의 실행을 요청함
// var url = "http://192.168.0.50:8022/SVMS/Event/optexfd";
// http://192.168.0.50/SRF/get_post_receiver.php?data=<EventMessage><Type>1700</Type><AlarmGroup>9</AlarmGroup><ID>1</ID><AlarmTime></AlarmTime></EventMessage>
function tcpipNetCat() {
	// http://192.168.0.90/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"1","count":"4","interval":"3"},"debug":true}]
	// http://192.168.0.90/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0"},"debug":true}]
	// "enUsr_0": true,
	// "enUsr_1": true,
	if (cfg.userEnv.enableAPI) {
		for (var key in cfg.userEnv.callAPI) {
			// check if the property/key is defined in the object itself, not in parent
			if (cfg.userEnv.callAPI.hasOwnProperty(key)) {
				// console.log(key, cfg.userEnv.callAPI[key]);
				if(cfg.userEnv.callAPI[key]) {
					logger("tcpipNetCat to itaAPI Server: "+key);
					triggerAPI(key);
				}
			}
		}
	}
}

//////////////////////////////////////
// HTTP Request
// 필요에 따라 수정이 필요한 
// 사용자 요청에 따른 데이터 전송 
function requestPost() { 
	for (item in cfg.userEnv.userSrvRequest) { // 사용자 Http Request는 기본적으로 4개 까지(config.json) 허용 한다.
		if(cfg.userEnv.enUsrRequest[item] && cfg.userEnv.userSrvRequest[item] && cfg.userEnv.usrReqData[item]) { // 활성화 && URL && 데이터
			var url = cfg.userEnv.userSrvRequest[item];
			// var body = JSON.stringify({"key":cfg.userEnv.usrReqData[item]});
			var body = cfg.userEnv.usrReqData[item];

			if(cfg.userEnv.usrReqPost[item]) 
				method = 'POST'; 
			else 
				method = 'GET'; 

			request({
				headers: {"content-type" : "application/x-www-form-urlencoded"},
				url:     url,
				method:  method,
				body:    body
			}, function(error, response, body){
				// console.log(error);
				// console.log(response);
				// console.log("user Response is: "+body);
				// console.log("userRequest: "+url);
				// console.log(error, body, response);
				// console.log(response.statusCode, response.request.method, response.request.body);
				logger('requestPost: ' + response.statusCode + " " + response.request.method + " " + response.request.body);
			});
			// console.log(method+" --- "+url+" --- "+body);
		}
	}
}


function triggerAPI(ioID) {
	// itsAPI.pyc로 명령어(ioID = "io02")를 직접 전송 한다.
	// 형식 value = [{"callAPI":{"id":ioID}}];
	// triggerAPI("io01"); // API 요청
	// echo '{"trigger":{"id":"io08"}}' | nc 192.168.0.50 34001 -q 0 > /dev/null 2>&1

	// host = cfg.interface.its.address; // 자기자신 아이피
	// port = cfg.interface.portAPI; // 34001; // API Port
	var command = 'echo \'{"trigger":{"id":"'+ioID+'"}}\' | nc ' + cfg.interface.its.address + ' ' + cfg.interface.portAPI + ' -q 0 > /dev/null 2>&1';
	executeCmd(command, function (response) {
		// console.log(response, command);
	});
}


////////////////////
// 데이터베이스 관련
////////////////////
// https://stackoverflow.com/questions/20210522/nodejs-mysql-error-connection-lost-the-server-closed-the-connection
var mysql = require('mysql');
var db_config = { host: 'localhost', user: 'its', password: 'GXnLRNT9H50yKQ3G', database: 'its_web' };
var con = mysql.createConnection(db_config); // Create the con.

// 데이터베이스 테이블 생성
function createTable() {
	con.connect(function(err) {
		// if (err) throw err;
		var sql = "SELECT COUNT(*) AS tableExist FROM information_schema.tables WHERE table_schema = 'its_web' AND table_name = 'w_log_sensor_M'";
		con.query(sql, function (err, result, fields) {
			if (err) throw err;
			// callback(null, result);
			// console.log(result);
			var sql = "CREATE TABLE IF NOT EXISTS w_log_sensor_M ( w_id int(11) NOT NULL AUTO_INCREMENT, w_sensorId varchar(64) NULL DEFAULT '', w_shot varchar(255) NULL DEFAULT '', w_action varchar(32) NULL DEFAULT '', w_description varchar(64) NULL DEFAULT '', w_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (w_id) ) ENGINE=InnoDB  DEFAULT CHARSET=utf8"; 
			con.query(sql, function (err, result) {
				if (err) throw err;
			});
		});
	});
}

// 데이터베이스 이벤트 등록
function insertEvent(w_sensorId, w_shot, w_action, w_description) {
	con.connect(function(err) {
		// if (err) throw err;
		// 오류 발생 var shotURL = "<a href="+w_shot+" target=shotImage>Snapshot</a>";
		var sql = "INSERT INTO w_log_sensor_M (w_sensorId, w_shot, w_action, w_description) VALUES ('"+w_sensorId+"', '"+w_shot+"', '"+w_action+"', '"+w_description+"')";
		con.query(sql, function (err, result) {
			if (err) throw err;
			// callback(null, result);
			// console.log(result);
		});
	});
}

// 데이터베이스 이벤트 검색 - MINUTE HOUR DAY
function getEvtLog(sensorID, callback) {
	con.connect(function(err) {
		// if (err) throw err;
		var sql = "SELECT * FROM w_log_sensor_M WHERE w_sensorId = '"+sensorID+"' AND w_stamp >= NOW() - INTERVAL 1 HOUR"; // MINUTE HOUR DAY
		con.query(sql, function (err, result, fields) {
			if (err) throw err;
			callback(null, result);
			// console.log(result);
		});
	});
}

// 환경변수(config.json)에 저장된 마스킹 정보
function readMasking() {
	var masking = '';
	var classmem = cfg.masking;
	for (item in classmem) {
		for (subItem in classmem[item]) {
			// 텍스트 위치 보정 500, 1500 -  주프로그램에서 클릭시 path 를 우선하기 위해 text를 먼저 출력한다.
			masking += "<text class='"+subItem+"' x='"+(cfg.maskCoord[item][subItem][0]+500)+"' y='"+(cfg.maskCoord[item][subItem][1]+1500)+"' text-anchor='right' style='fill:gray; font-size:40cm;' >"+subItem+"</text>";
			masking += '<path class="'+item+'" id="'+subItem+'" d="'+classmem[item][subItem]+'"></path>';
		}
	}
	return masking; 
}

function setMasking(data) {
	cfg.masking[data.mask][data.id] = data.value;
	coord = data.value.split(" ");
	coordS = coord[0].substring(1).split(","); // M32761.745962445624,54930.81088586822 -> 32761.745962445624,54930.81088586822 -> 32761, 54930
	
	coordSx = parseInt(coordS[0]);
	coordSy = parseInt(coordS[1]);
	coordEx = coordSx + parseInt(coord[1].substring(1).split(",")[0]); // l16682.344050231957,0 -> 16682.344050231957,0 -> 16682.344050231957 -> 16682
	coordEy = coordSy + parseInt(coord[2].split(",")[1]); // 0,19295.24131111164 -> 19295.24131111164 -> 19295
	
	cfg.maskCoord[data.mask][data.id] = [coordSx,coordSy,coordEx,coordEy];
}

// 환경변수(config.json) 저장
function saveConfigJson() {
	var cfg_target = './config.json'; // 환경 파일 읽기
	// var cfg_target = cfg.path.webRoot+'/'+cfg.path.config+'/config.json'; // 환경 파일 읽기
	fs.writeFile(cfg_target, JSON.stringify(cfg, null, 4), (err) => {
		if (err) throw err;
		console.log('The file has been saved!');
	});
}

// 로그 등록
function logger(log) {
	var logIs = new Date().getTime() + ' > ' + log + '\n';
	fs.appendFile(loggerFile, logIs, function (err) {
	  if (err) throw err;
	  // console.log('Saved!');
	});	
}

// 이벤트 값(json) 저장
function saveEventJson(event) {
	var jsonFile = jsonPath + '/' + String(new Date().getMonth()+1).padStart(2, '0') + String(new Date().getDate()).padStart(2, '0') + '.json';
	var eventIs = '"' + new Date().getTime() + '":' + event + '\n';
	// console.log('Saved!');
	fs.appendFile(jsonFile, eventIs, function (err) {
	  if (err) throw err;
	});	
}

// 자료내용 확인 및 클라이언트 전송
function parseObj(obj) {
	for(var i = 0; i < obj.result.length; i++) {
		var id = obj.result[i].id;
		var speed = obj.result[i].geolocation.speed;
		var hAngle = obj.result[i].observation.horizontalAngle;
		var aAngle = obj.result[i].observation.azimuthAngle;
		var range = obj.result[i].observation.range;
		var rcs = obj.result[i].stats.rcs;
		
		// console.log('id:', id, 'speed:', speed, 'hAngle:', hAngle, 'aAngle:', aAngle, 'range:', range, 'rcs:', rcs);
		
		// Pre filter 최소값 이하나 최대값 이상은 사전에 제거 한다.
		if(rcs < cfg.sensor.rcsValue.min || rcs > cfg.sensor.rcsValue.max || speed < cfg.sensor.spdValue.min || speed > cfg.sensor.spdValue.max) return 0;
		
		// 감도레벨 변수 선언
		if(cfg.sensor.rcsValue.cMin < rcs && cfg.sensor.rcsValue.cMax > rcs) { 
			var alarmRcs = 1; 
		} else { 
			var alarmRcs = 0; 
		}
		// 속도레벨 변수 선언
		if(cfg.sensor.spdValue.cMin < speed && cfg.sensor.spdValue.cMax > speed) {
			var alarmSpd = 1; 
		} else { 
			var alarmSpd = 0; 
		}

		////////////////////////////////////////////////
		// 마스킹 규칙 - 동시에 수용과 거부가 존재할수 없다
		// 마스킹 유무 확인
		// 각도(aAngle)와 거리(range) 값에서 X, Y 거리 계산
		var angle = (aAngle) / 180 * Math.PI; // compensate angle -90°, conv. to radian
		var x = range * Math.sin(angle) * 1000; // Math.floor(testnum)
		var y = range * Math.cos(angle) * 1000;
		// console.log(x, y)
		var maskIs = 0;
		var maskID = '';
		if(cfg.maskSelect) {
			if(cfg.maskSelect ==  1) {
				item = 'allowGroup';
			} else {
				item = 'denyGroup';
			}
			for (subItem in cfg.maskCoord[item]) { // subItem -> { "627_103", "890_340", ... }
				if((cfg.maskCoord[item][subItem][0] < x) && (cfg.maskCoord[item][subItem][2] > x)) {
					if((cfg.maskCoord[item][subItem][1] < y) && (cfg.maskCoord[item][subItem][3] > y)) {
						maskIs = 1;
						maskID = subItem;
					}	
				}
			}
		}
		
		if(cfg.maskSelect == 0 || (cfg.maskSelect == 1 && maskIs == 1) || (cfg.maskSelect == 2 && maskIs == 0)) {
			// // 마스킹 조건과 알람조건 모두를 만족할때 실행
			// if(alarmRcs && alarmSpd && cfg.camera.tracking) { // 알람레벨 변수 선언
			// 	cAngle = parseFloat(cfg.camera.calibration.angleOffset) + parseFloat(aAngle);// 센서의 정면을 기준각도로 카메라 각을 보정한다.
			// 	cZoom = (range * cfg.camera.calibration.zoomStep) + cfg.camera.calibration.zoomValue.cMin;
			// 	ptzSetPos("pan="+cAngle+"&zoom="+cZoom+"&tilt=0");
			// 	// 소켓을 통해 자료를  Client인 spotter_tmplet.html로 전송한다.
			// }

			if(alarmRcs && alarmSpd) {
				// 이밴트 로그 저장(일자기중 최대 365개 파일)
				saveEventJson('1,'+id+','+maskID+','+speed+','+hAngle+','+aAngle+','+range+','+rcs);
				// 클라이언트에 이벤트 전송
				io.sockets.emit('sendEventLog', { 
					id: id, speed: speed, hAngle: hAngle, aAngle: aAngle, range: range, rcs: rcs, alarmRcs: alarmRcs, alarmSpd: alarmSpd, alarmIs: 1
				});

				// 외부명령 실행 요청
				tcpipNetCat(); // S1(에스원)
				requestPost()
			} else {
				// 이밴트 로그 저장(일자기중 최대 365개 파일)
				saveEventJson('0,'+id+','+maskID+','+speed+','+hAngle+','+aAngle+','+range+','+rcs);
					// 클라이언트에 이벤트 전송
				io.sockets.emit('sendEventLog', { 
					id: id, speed: speed, hAngle: hAngle, aAngle: aAngle, range: range, rcs: rcs, alarmRcs: alarmRcs, alarmSpd: alarmSpd, alarmIs:0
				});
			}
		} else { // 조건에 일치하지 않으면 비알람으로 전송 
			// 이밴트 로그 저장(일자기중 최대 365개 파일)
			saveEventJson('0,'+id+','+maskID+','+speed+','+hAngle+','+aAngle+','+range+','+rcs);
				// 클라이언트에 이벤트 전송
			io.sockets.emit('sendEventLog', { 
				id: id, speed: speed, hAngle: hAngle, aAngle: aAngle, range: range, rcs: rcs, alarmRcs: alarmRcs, alarmSpd: alarmSpd, alarmIs:0
			});
		}
	}
}

////////////////////
// Start Program //
////////////////////
io.sockets.setMaxListeners(0);

///////////////////////////////////////////////////////////////////////////////
// 센서 포트(portIn)로 부터 받은 정보를 파싱한후 클라이언트(portOut)으로 전달한다.
///////////////////////////////////////////////////////////////////////////////
app.listen(portOut); // Display server
logger('Service server running at http://localhost:'+portOut)
console.log('\nService server running at http://localhost:'+portOut);

require('net').createServer(function (socket) {
	jsonPacket = '';
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
		// var alarmInfo = data.toString();
		// console.log('Buffer size : ' + socket.bufferSize);
		// console.log(data);
		// console.log(data.toString());
		try {
			obj = JSON.parse(data); // data.toString() data.toString('utf8')
			parseObj(obj); // 자료내용 확인 및 클라이언트 전송
			jsonPacket = '';
		} catch (e) {
			if(jsonPacket) { // (자료가 잘린 패킷문제 해결) 이전 데이터에 오류가 있었으면 현재 자료와 묵어서 재시도 함
				try { // 합쳐진 자료의 분석
					obj = JSON.parse(jsonPacket+data);
					parseObj(obj); // 자료내용 확인 및 클라이언트 전송
				} catch (e) { // 연속 두번 오류가 생기면 자료를 버린다.
					console.log("\tJSON.parse Error");
					jsonPacket = ''; // 페기
					// process.exit();
				}
			} else { // 최초오류, 저장후 다음에 오는 자료를 기다림
				jsonPacket = data;
			}
			// console.log(data.toString());
			// process.exit();
			// return console.error(e);
		}
    });	
}).listen(portIn); // Receive server
logger('Receive server running at http://localhost:'+portIn)
console.log('Receive server running at http://localhost:'+portIn);

///////////////////////////////////////////////////////////////////////////////
// 클라이언트(portOut)의 명령 정보를 파싱한후 작업하고 결과 전달하거나 내용을 저장한다.
///////////////////////////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) { // 내부 Client로 부터 받은 작업 실행
	var clientIP = socket.handshake.address.replace(/^.*:/, ''); //  접근자 아이피 
	
	// 관리자 아이피(cfg.license.ownerIp)가 정의 되었으면 다른 아이피의 접근을 제한 한다.
	if ((cfg.license.ownerIp) && (cfg.license.ownerIp != clientIP)) return 0; // 접근제한

	// 시스템 명령 관련
	socket.on('systemCmd', function(data) { 
		logger(clientIP + ' systemCmd ' + data);
		console.log(clientIP + ' systemCmd ' + data); 
		executeCmd(data, function (response) {
			console.log(response);
		});
	});
	
	// 클라이언트 셋업 관련
	socket.on('sysAccInfo', function(data) { // 시스템 어카운트 정보 전송
		io.sockets.emit('sysAccInfo', { 
			ownerIp: cfg.license.ownerIp,
			ownerPass: cfg.license.ownerPass,
			portIn: cfg.interface.portIn,
			portOut: cfg.interface.portOut,
			address: cfg.interface.its.address,
			netmask: cfg.interface.its.netmask,
			gateway: cfg.interface.its.gateway,
			key: cfg.license.key
		});
	});
	socket.on('sysAccSave', function(data) { // 시스템 어카운트 정보 저장
		logger(clientIP + ' sysAccSave ' + data);
		console.log(clientIP + ' sysAccSave ' + data); 
		cfg.license.ownerIp = data.ownerIp;
		cfg.license.ownerPass = data.ownerPass;
		cfg.interface.portIn = data.portIn;
		cfg.interface.portOut = data.portOut;
		cfg.interface.its.address = data.itsAddress;
		cfg.interface.its.netmask = data.itsNetmask;
		cfg.interface.its.gateway = data.itsGateway;
		cfg.license.key = data.key;
		cfg.language.selected = data.language;
		saveConfigJson();
	});
	socket.on('camAccInfo', function(data) { // 카메라 어카운트 정보 전송
		io.sockets.emit('camAccInfo', { 
			addr: cfg.camera.addr,
			user: cfg.camera.user,
			pass: cfg.camera.pass
		});
	});
	socket.on('camAccSave', function(data) { // 카메라 어카운트 정보 저장
		logger(clientIP + ' camAccSave ' + data);
		console.log(clientIP + ' camAccSave ' + data); 
		cfg.camera.addr = data.addr;
		cfg.camera.user = data.user;
		cfg.camera.pass = data.pass;
		saveConfigJson();		
	});
	socket.on('userEnvInfo', function(data) { // 사용자 환경 정보 전송
		io.sockets.emit('userEnvInfo', { 
			enUsr_0: cfg.userEnv.enUsrRequest.url_0,
			enUsr_1: cfg.userEnv.enUsrRequest.url_1,
			typeReq_0: cfg.userEnv.usrReqPost.url_0,
			typeReq_1: cfg.userEnv.usrReqPost.url_1,
			url_0: cfg.userEnv.userSrvRequest.url_0,
			url_1: cfg.userEnv.userSrvRequest.url_1,
			dataReq_0: cfg.userEnv.usrReqData.url_0,
			dataReq_1: cfg.userEnv.usrReqData.url_1,
			enableAPI: cfg.userEnv.enableAPI,
			io01: cfg.userEnv.callAPI.io01,
			io02: cfg.userEnv.callAPI.io02,
			io03: cfg.userEnv.callAPI.io03,
			io04: cfg.userEnv.callAPI.io04,
			io05: cfg.userEnv.callAPI.io05,
			io06: cfg.userEnv.callAPI.io06,
			io07: cfg.userEnv.callAPI.io07,
			io08: cfg.userEnv.callAPI.io08
		});
	});
	socket.on('userEnvSave', function(data) { // 사용자 환경 정보 저장
		logger(clientIP + ' userEnvSave ' + data);
		console.log(clientIP + ' userEnvSave ' + data); 
		cfg.userEnv.enUsrRequest.url_0 = data.enUsr_0;
		cfg.userEnv.enUsrRequest.url_1 = data.enUsr_1;
		cfg.userEnv.usrReqPost.url_0 = data.typeReq_0;
		cfg.userEnv.usrReqPost.url_1 = data.typeReq_1;
		cfg.userEnv.userSrvRequest.url_0 = data.url_0;
		cfg.userEnv.userSrvRequest.url_1 = data.url_1;
		cfg.userEnv.usrReqData.url_0 = data.dataReq_0;
		cfg.userEnv.usrReqData.url_1 = data.dataReq_1;
		cfg.userEnv.enableAPI = data.enableAPI;
		cfg.userEnv.callAPI.io01 = data.io01;
		cfg.userEnv.callAPI.io02 = data.io02;
		cfg.userEnv.callAPI.io03 = data.io03;
		cfg.userEnv.callAPI.io04 = data.io04;
		cfg.userEnv.callAPI.io05 = data.io05;
		cfg.userEnv.callAPI.io06 = data.io06;
		cfg.userEnv.callAPI.io07 = data.io07;
		cfg.userEnv.callAPI.io08 = data.io08;
		saveConfigJson();		
	});
	socket.on('senAccInfo', function(data) { // 센서 어카운트 정보 전송
		io.sockets.emit('senAccInfo', { 
			addr: cfg.sensor.addr,
			user: cfg.sensor.user,
			pass: cfg.sensor.pass
		});
	});
	socket.on('senAccSave', function(data) { // 센서 어카운트 정보 저장
		logger(clientIP + ' senAccSave ' + data);
		console.log(clientIP + ' senAccSave ' + data); 
		cfg.sensor.addr = data.addr;
		cfg.sensor.user = data.user;
		cfg.sensor.pass = data.pass;
		saveConfigJson();
	});
	
	socket.on('rcsRangePre', function(data) { // 샌서 임계치 관련
		logger(clientIP + ' rcsRangePre ' + data);
		console.log(clientIP + ' rcsRangePre ' + data); 
		cfg.sensor.rcsValue.min = data[0]; 
		cfg.sensor.rcsValue.max = data[1]; 
		saveConfigJson(); // 설정값 저장
		io.sockets.emit('sendSetValue', cfg); // 클라이언트동기화 
	}); // rcsLvl 감도제한
	socket.on('spdRangePre', function(data) {
		logger(clientIP + ' spdRangePre ' + data);
		console.log(clientIP + ' spdRangePre ' + data); 
		cfg.sensor.spdValue.min = data[0]; 
		cfg.sensor.spdValue.max = data[1]; 
		saveConfigJson();
		io.sockets.emit('sendSetValue', cfg); // 클라이언트동기화 
	}); // spdLvl 속도제한
	
	socket.on('rcsRange', function(data) { // 샌서 임계치 관련
		logger(clientIP + ' rcsRange ' + data);
		console.log(clientIP + ' rcsRange ' + data); 
		cfg.sensor.rcsValue.cMin = data[0]; 
		cfg.sensor.rcsValue.cMax = data[1]; 
		saveConfigJson(); // 설정값 저장
		io.sockets.emit('sendSetValue', cfg); // 클라이언트동기화 
	}); // rcsLvl 감도제한
	socket.on('spdRange', function(data) {
		logger(clientIP + ' spdRange ' + data);
		console.log(clientIP + ' spdRange ' + data); 
		cfg.sensor.spdValue.cMin = data[0]; 
		cfg.sensor.spdValue.cMax = data[1]; 
		saveConfigJson();
		io.sockets.emit('sendSetValue', cfg); // 클라이언트동기화 
	}); // spdLvl 속도제한
	
	socket.on('zoomRange', function(data) { // 카메라 줌 관련
		logger(clientIP + ' zoomRange ' + data);
		console.log(clientIP + ' zoomRange ' + data); 
		cfg.camera.calibration.zoomValue.cMin = data[0]; 
		cfg.camera.calibration.zoomValue.cMax = data[1]; 
		cfg.camera.calibration.zoomStep = (data[1] - data[0]) / cfg.sensor.rangeMax;
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
		saveConfigJson();
	}); // zoomLvl 
	
	socket.on('objectsTag', function(data) {
		console.log(clientIP + ' objectsTag ' + data); 
		cfg.screen.objectsTag = data; 
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
		saveConfigJson();
	}); // objectsTag
	
	socket.on('bgOpacityTag', function(data) {
		console.log(clientIP + ' bgOpacityTag ' + data); 
		cfg.screen.bgOpacityTag = data; 
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
		saveConfigJson();
		tcpipNetCat(); // 테스트
		requestPost(); // 테스트
	}); // bgOpacityTag

	socket.on('svgView', function(data) { // SVG View Point 관련
		console.log(clientIP + ' svgView ' + data); 
		cfg.screen.svg.matrix = data; 
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
		saveConfigJson();
	}); // svgView
	
	socket.on('readMasking', function(data) { // 환경값을 클라이언트로 전송()
		console.log(clientIP + ' readMasking ' + data); 
		io.sockets.emit('readMasking', readMasking());; // 클라이언트동기화 
	});
	
	socket.on('setMasking', function(data) { // SVG View Point 관련
		console.log(clientIP + ' setMasking ' + data.id + ' ' + data.mask + ' ' + data.value); 
		setMasking(data);
		io.sockets.emit('readMasking', readMasking());; // 클라이언트동기화 
		saveConfigJson();
	}); // svgView
	
	socket.on('delMasking', function(data) { // SVG View Point 관련
		console.log(clientIP + ' delMasking ' + data.id + ' ' + data.mask); 
		delete (cfg.masking[data.mask][data.id]);
		delete (cfg.maskCoord[data.mask][data.id]);
		io.sockets.emit('readMasking', readMasking());; // 클라이언트동기화 
		saveConfigJson();
	}); // svgView

	socket.on('readMaskSelect', function(data) { // 환경값을 클라이언트로 전송()
		console.log(clientIP + ' readMaskSelect ' + data); 
		io.sockets.emit('readMaskSelect', cfg.maskSelect);; // 클라이언트동기화 
	});

	socket.on('setMaskSelect', function(data) { //
		console.log(clientIP + ' setMaskSelect ' + data);
		cfg.maskSelect = data
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
		saveConfigJson();
	});
	
	socket.on('ptzSetPos', function(data) { // 카메라 [데이터위치] 요청위치로 이동
		console.log(clientIP + ' ptzSetPos ' + data); 
		ptzSetPos(data) // Set Camera Action
	});
	
	socket.on('gotoHome', function(data) { // 카메라 [기준위치] 홈위치로 이동
		console.log(clientIP + ' gotoHome ' + data);
		query = 'pan='+cfg.camera.calibration.pan+'&tilt='+cfg.camera.calibration.tilt;
		ptzSetPos(query) // Set Camera Action
	});
	
	socket.on('camTrac', function(data) { // 카메라 [기준위치] 홈위치로 이동
		console.log(clientIP + ' camTrac ' + data);
		cfg.camera.tracking = data
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
		saveConfigJson();
	});

	socket.on('setCamera', function(data) { // 카메라 [위치설정] 현재 방향을 센서의 중심으로
		logger(clientIP + ' setCamera ' + data);
		console.log(clientIP + ' setCamera ' + data); 
		setCamera();
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
	});
	
	socket.on('findClientIP', function(data) { // 클라이언트 아이피 전송()
		console.log(clientIP + ' findClientIP ' + data); 
		io.sockets.emit('findClientIP', { 
			ip: clientIP,
			oIp: cfg.license.ownerIp,
			id: data 
		});
	});

	socket.on('sendSetValue', function(data) { // 환경값을 클라이언트로 전송()
		console.log(clientIP + ' sendSetValue ' + data); 
		io.sockets.emit('sendSetValue', cfg);; // 클라이언트동기화 
	});
	
	socket.on('sendLanValue', function(data) { // 환경값을 클라이언트로 전송()
		console.log(clientIP + ' sendLanValue ' + data); 
		io.sockets.emit('sendLanValue', { 
			language: lan, // 언어 리스트
			selected: cfg.language.selected // 선택된 언어
		});
	});
	
	socket.on('startSetEnv', function(data) { // 환경값을 클라이언트로 전송()
		console.log(clientIP + ' startSetEnv ' + data); 
		io.sockets.emit('startSetEnv', { 
			config: cfg, // 언어 리스트
			language: lan // 선택된 언어
		});
	});
	
});	


