////////////////////////
// its가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
// 참고 : https://openclassrooms.com/courses/ultra-fast-applications-using-node-js/socket-io-let-s-go-to-real-time
////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io')(app); // var io = require('socket.io').listen(app);
var fs = require('fs');
var path = require('path');

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfg = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
var ims = JSON.parse(fs.readFileSync('./cfgIms.json', 'utf8')); // 환경 파일 읽기
var icc = JSON.parse(fs.readFileSync('./camera.json', 'utf8')); // 환경 파일 읽기
// var lan = JSON.parse(fs.readFileSync(cfg.path.common+'/language.json', 'utf8')); // 환경 파일 읽기
var lan = JSON.parse(fs.readFileSync('./language.json', 'utf8')); // 환경 파일 읽기

var html = fs.readFileSync(cfg.file.html_target, 'utf8');
///////////////////
// 클라이언트 HTML 코드(cfg.file.html_target)를 읽어드린다.
function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

///////////////////
// 데이터베이스 관련
// https://stackoverflow.com/questions/20210522/nodejs-mysql-error-connection-lost-the-server-closed-the-connection
var mysql = require('mysql');
var db_config = {
	host: cfg.mysql.host,
	user: cfg.mysql.user,
	password: cfg.mysql.pass,
	database: cfg.mysql.name
};

// https://stackoverflow.com/questions/20210522/nodejs-mysql-error-connection-lost-the-server-closed-the-connection
// Error: Connection lost: The server closed the connection. - 오류 발생 제거: 
var con;
function handleDisconnect() {
	con = mysql.createConnection(db_config);// Recreate the con, since
											// the old one cannot be reused.
	con.connect(function(err) {	// The server is either down
		if(err) { 				// or restarting (takes a while sometimes).
			console.log('error when connecting to db:', err);
			setTimeout(handleDisconnect, 2000); // We introduce a delay before attempting to reconnect,
		}										// to avoid a hot loop, and to allow our node script to
	});											// process asynchronous requests in the meantime.
												// If you're also serving http, display a 503 error.
	con.on('error', function(err) {
		console.log('db error', err);
		if(err.code === 'PROTOCOL_CONNECTION_LOST') {	// con to the MySQL server is usually
		  handleDisconnect();							// lost due to either server restart, or a
		} else {										// connnection idle timeout (the wait_timeout
		  throw err;									// server variable configures this)
		}
	});
}
handleDisconnect();


// 모니터링 데이터베이스 자료등록
// w_id w_gr w_ca w_sensorId w_sensorName w_userName w_shot w_action w_description
// function insertEvent(w_gr, w_ca, w_sensorId, w_shot, w_action, w_description) { // 이벤트 등록
function insertEvent(w_gr, w_ca, w_sensorId, w_sensorName, w_userName, w_shot, w_action, w_description) { // 이벤트 등록
	con.connect(function(err) {
		// if (err) throw err;
		var sql = "INSERT INTO "+cfg.table.imsData+" (w_gr, w_ca, w_sensorId, w_sensorName, w_userName, w_shot, w_action, w_description) VALUES ("+w_gr+", "+w_ca+", '"+w_sensorId+"', '"+w_sensorName+"', '"+w_userName+"', '"+w_shot+"', '"+w_action+"', '"+w_description+"')";
		// console.log(sql);
		con.query(sql, function (err, result) {
			if (err) throw err;
			// callback(null, result);
			// console.log(result);
		});
	});
}

function getEvtLog(sensorID, callback) { // 이벤트 검색 - MINUTE HOUR DAY
	con.connect(function(err) {
		// if (err) throw err;
		var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_sensorId = '"+sensorID+"' AND w_stamp >= NOW() - INTERVAL 1 HOUR"; // MINUTE HOUR DAY
		con.query(sql, function (err, result, fields) {
			if (err) throw err;
			callback(null, result);
			// console.log(result);
		});
	});
}

function getEvtLastLog(callback) { // 최근 이벤트 검색후 지역상황 파악
	con.connect(function(err) {
		// 속도개선을 위해 SUB-QUERY 사용함 - https://stackoverflow.com/questions/12125904/select-last-n-rows-from-mysql
		// 최근 Limit 갯수만큼 읽은후 정열한다(차이가 많이남).
		var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_id IN ( SELECT MAX(w_id) FROM ( SELECT * FROM "+cfg.table.imsData+" ORDER BY w_id DESC LIMIT 1000 ) sub WHERE w_stamp >= NOW() - INTERVAL 1 DAY GROUP BY w_sensorId )";
		con.query(sql, function (err, result, fields) {
			// if (err) throw err;
			if (err) logger('Function getEvtLastLog error:',err);
			callback(null, result);
			// console.log(result);
		});
	});
}

function getEvtLogOneDay(sensorID='', callback) { // 팬스별 하루치 로그 읽기 
	con.connect(function(err) {
		// if (err) throw err;
		// var sql = "SELECT DISTINCT w_stamp FROM "+cfg.table.imsData+" WHERE w_stamp >= NOW() - INTERVAL 1 DAY"; // MINUTE HOUR DAY
		if(sensorID)
			var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_sensorId = '"+sensorID+"' AND w_stamp >= NOW() - INTERVAL 1 DAY"; // MINUTE HOUR DAY
		else
			var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_stamp >= NOW() - INTERVAL 1 HOUR"; // MINUTE HOUR DAY
		con.query(sql, function (err, result, fields) {
			// if (err) throw err;
			if (err) logger('Function getEvtLogOneDay error:',err);
			callback(null, result);
			// console.log(result);
		});
	});
}

///////////////////
// 이벤트 값(event) 저장
// 숫자를 0으로 채움 예: (3).pad(2) -> 03


Number.prototype.pad = function(size) {
  var s = String(this);
  while (s.length < (size || 2)) {s = "0" + s;}
  return s;
}
function saveEvent(event) {
	var dt = new Date();
	var m = (dt.getMonth()+1).pad(2);
	var d = dt.getDate().pad(2);
	var eventFile = cfg.path.log+cfg.path.event+'/'+m+d+'.event';
	var eventIs = dt+':'+event+'\n';
	fs.appendFile(eventFile, eventIs, function (err) {
		// if (err) throw err;
		if(err) logger('Function saveEvent error:',err);
	});	
}


///////////////////
// 환경변수(config.json) 저장
function saveConfigJson() {
	fs.writeFile(cfg.path.monitor+'/config.json', JSON.stringify(cfg, null, 4), (err) => {
		if (err) throw err;
		// console.log('The file has been saved!');
	});
}

///////////////////
// 로그 등록 예: logger(clientIP + ' findClientIP ' + data);
var loggerFile = cfg.path.log+cfg.path.home+cfg.path.home+'.log';
function logger(log) {
	var dt = new Date();
	var eventIs = dt+' > '+log+'\n';
	fs.appendFile(loggerFile, eventIs, function (err) {
		// if (err) throw err;
		if(err) console.log('Function logger Error');
	});	
}

///////////////////
// 카메라 PTZ Control - https://github.com/mafintosh/axis-camera
// request - https://www.npmjs.com/package/request
var request = require('request')
function ptzSetPos(addr, user, pass, ptzControl, query) { // 쿼리명령 수행
	request.get('http://'+addr+ptzControl+query, {
		'auth': {
			'user': user,
			'pass': pass,
			'sendImmediately': false
		}
	}, function (error, response, body) {
		if(error) logger('Function ptzSetPos error:', error); // Print the error if one occurred
		// logger('statusCode:', response && response.statusCode); // Print the response status code if a response was received
		// logger('body:', body); // Print the HTML for the Google homepage.
	});
}

// function getQueryModel(model, query, callback) {
	// console.log("model:%s, query:%s", model, query);
	// // model:AXIS_VAPIX_V3, query:rzoom=-500
	// // model:AXIS_VAPIX_V3, query:center=420,513
	// // model:Hanwha_V2_5_3, query:msubmenu=relative&ZoomPulse=-500
	// // model:Hanwha_V2_5_3, query:msubmenu=absolute&Pan=420&Tilt=513
	// if(model == 'AXIS_VAPIX_V3') {
		// // AXIS인경우 쿼리 내용 자체가 명령어임
		// ;
	// } else if(model == 'Hanwha_V2_5_3') {
		// // 쿼리정보내에 rzoom이 있으면 'rzoom=' -> 'msubmenu=relative&ZoomPulse=' 변환 
		// // 쿼리정보내에 center가 있으면 'center=' -> 'msubmenu=absolute&Pan='로 그리고 ',' -> '&Tilt='로 변환
		// if(query.indexOf("rzoom") == 0) {
			// query = query.replace("rzoom=", "msubmenu=relative&ZoomPulse=");
			// query = query.replace("500", "0.5");
		// } else if(query.indexOf("center") == 0) {
			// query = query.replace("center=", "msubmenu=absolute&Pan=");
			// query = query.replace(",", "&Tilt=");
		// }
	// } else if(model == 'Vision_V2_4') {
		// ;
	// } else if(model == 'Dahua_API') {
		// ;
	// } else {
		// query = '';
	// }
	// callback(query);
// }

///////////////////
// 시스템 명령
var exec = require('child_process').exec;
function systemCmd(obj) {
	var cmd = cfg.systemCmd[obj];
	// exec('python spotter.pyc', (e, stdout, stderr)=> {
	exec(cmd, (e, stdout, stderr)=> {
		if (e instanceof Error) {
			console.error(e);
			throw e;
		}
		console.log('stdout ', stdout);
		console.log('stderr ', stderr);
	});
}

///////////////////
// Start Program 
///////////////////

var portIn = cfg.interface.portIn;
var portOut = cfg.interface.portOut;

///////////////////
// ITS -> IMS(8087) -> [Do it] -> IMS(38088) -> PC(Browser)
// 외부의 ITS로 부터 IMS포트 38087(portIn)로 접수(listen(portIn))
// 분석된 정보를 포트 38088(portOut)을 통해 사용자브라우저에 전달(sendEventLog)한다.
// https://namik.tistory.com/114
require('net').createServer(function (client) {

	/* 실시간 접속되는 모든 클라이언트 정보
	console.log('Client connection: ');
	console.log('   local = %s:%s', client.localAddress, client.localPort);
	console.log('   remote = %s:%s', client.remoteAddress, client.remotePort);
	*/
	
	client.setTimeout(500);
	client.setEncoding('utf8');
	
	client.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
		// w_gr w_ca w_sensorId w_sensorName w_userName w_shot w_action w_description
		// var id = '';
		// var name = '';
		var senId = '';
		var senName = '';
		var userName = 'ITS';
		var beep = '';
		var status = '';
		var msg = '';
		var shot = '';
		var subzone = '';
		var video = '';
		
		var alarmInfo = data.toString();
		var objInfo = alarmInfo.split(",");  
		for (var i in objInfo) {
			var objField = objInfo[i].split("=");
			if (objField[0].trim() == 'id') senId = objField[1];
			if (objField[0].trim() == 'name') senName = objField[1];
			if (objField[0].trim() == 'beep') beep = objField[1];
			if (objField[0].trim() == 'status') status = objField[1]; 
			if (objField[0].trim() == 'msg') msg = objField[1]; 
			// if (objField[0].trim() == 'subzone') subzone = objField[1]; 
			if (objField[0].trim() == 'shot') shot = objField[1]; 
			// if (objField[0].trim() == 'video') video = decodeURIComponent(objField[1]); // URI 디코딩(내용에 = 등과 같은 기호 처리)
		// console.log(data);
		}
		if(ims.sensor[senId] !== undefined){ // 등록이 된 센서 이벤트만 필터링 한다.
			senName = ims.sensor[senId].subj;
			// 소켓을 통해 자료를 클라이언트(its_M_map_tmplet.html)로 전송한다.
			io.sockets.emit('sendEventLog', { id: senId, name: senName, beep: beep, status: status, shot: shot });

			if (parseInt(beep)) 
				insertEvent(ims.sensor[senId].group, ims.sensor[senId].cate, senId, senName, userName, shot, status, msg); // 이벤트를 데이터베이스에 저장
			saveEvent(senId+','+senName+','+beep+','+status+','+msg+','+shot);
		}
		/* 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음
		client.write('received');
		*/

    });
	
	/* 지우지 말것, 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음
	client.on('end', function() {
		console.log('Client disconnected');
	});
	client.on('error', function(err) {
		console.log('Socket Error: ', JSON.stringify(err));
	});
	client.on('timeout', function() {
		console.log('Socket Timed out');
	});
	*/
	
}).listen(portIn); // Receive from ITS -> IMS(38087)
console.log('\nlisten from http://localhost:'+portIn+'/');

///////////////////
// PC(Browser) -> IMS(8088) -> [Do it] -> IMS(8088) -> PC(Browser)
// 사용자로부터 명령을 접수한후 실행함. 필요에 따라 결과값 회신
// 클라이언트(its_M_map_tmplet.html)로부터 받은 명령을 수행한다.
// io.sockets.setMaxListeners(0);
var connectedIP = {}; // 실시간 접속 로그
io.sockets.on('connection', function (socket) {
	var clientIP = socket.handshake.address.replace(/^.*:/, ''); //  접근자 아이피 
	connectedIP[clientIP] = 'Connect' + " " + Date(); // 실시간 접속 로그

	// // 아이피 접근 제한.
	// if(typeof(cfg.filterIP.allow[clientIP]) !== "undefined") process.exit(); // && icc[model].ptzControl !== null ) 
	// if(typeof(cfg.filterIP.deny[clientIP]) !== "undefined") process.exit(); // && icc[model].ptzControl !== null ) 
	
	// // 관리자 아이피(cfg.license.ownerIp)가 정의 되었으면 다른 아이피의 접근을 제한 한다.
	// if ((cfg.license.ownerIp) && (cfg.license.ownerIp != clientIP)) {
		// return 0;
	// } // return 0; // 접근제한

	// 시스템 명령 관련
	socket.on('systemCmd', function(data) { 
		systemCmd(data); 
		logger(clientIP + ' systemCmd ' + data);
	});

	// 실시간 접속자 로그
	socket.on('connectedIP', function() { 
		// console.log(connectedIP);
		io.sockets.emit('connectedIP', connectedIP );
	});
	
	// 클라이언트 셋업 관련
	socket.on('sysAccInfo', function(data) { // 시스템 어카운트 정보 전송
		io.sockets.emit('sysAccInfo', { 
			ownerIp: cfg.license.ownerIp,
			ownerPass: cfg.license.ownerPass,
			key: cfg.license.key,
			address: cfg.interface.its.address,
			netmask: cfg.interface.its.netmask,
			gateway: cfg.interface.its.gateway,
			portIn: cfg.interface.portIn,
			portOut: cfg.interface.portOut
		});
		logger(clientIP + ' sysAccInfo ');
	});
	
	socket.on('sysAccSave', function(data) { // 시스템 어카운트 정보 저장
		// console.log(clientIP + ' sysAccSave ' + data); 
		cfg.license.ownerIp = data.ownerIp;
		cfg.license.ownerPass = data.ownerPass;
		cfg.license.key = data.key;
		// cfg.interface.its.address = data.address;
		// cfg.interface.its.netmask = data.netmask;
		// cfg.interface.its.gateway = data.gateway;
		// cfg.interface.portIn = data.portIn;
		// cfg.interface.portOut = data.portOut;
		saveConfigJson();
		logger(clientIP + ' sysAccSave ');
	});
	
	// 클라이언트 아이피 전송()
	socket.on('findClientIP', function(data) { 
		io.sockets.emit('findClientIP', { 
			ip: clientIP,
			oIp: cfg.license.ownerIp,
			id: data 
		});
		logger(clientIP + ' findClientIP ' + data);
	});

    // // 이벤트 확인절차 actionClear
    // socket.on('actionClear', function (data) {
		// var arr = data.split("_||_");
		// insertEvent(ims.sensor[arr[0]].group, ims.sensor[arr[0]].cate, arr[0], arr[1], arr[2], '', 0, arr[3]); 
		// // 클라이언트에 해제 이벤트 전송: id, name, beep, status, shot, video, subzone
		// io.sockets.emit('sendEventLog', { id: arr[0], name: arr[1], beep: 2, status: 2, shot: '' });
		// logger(clientIP + ' actionClear ' + data);
	// }); 

    // 이벤트 확인절차 actionClear 센서
    socket.on('actionClearS', function (data) {
		var arr = data.split("_||_");
		insertEvent(ims.sensor[arr[0]].group, 300, arr[0], arr[1], arr[2], '', 4, arr[3]); 
		// 클라이언트에 해제 이벤트 전송: id, name, beep, status, shot, video, subzone
		io.sockets.emit('sendEventLog', { id: arr[0], name: arr[1], beep: 2, status: 4, shot: '' });
		logger(clientIP + ' actionClear Sensor ' + data);
	}); 

    // 이벤트 확인절차 actionClear 카메라
    socket.on('actionClearC', function (data) {
		var arr = data.split("_||_");
		insertEvent(0, 500, arr[0], arr[1], arr[2], '', 4, arr[3]); 
		// 클라이언트에 해제 이벤트 전송: id, name, beep, status, shot, video, subzone
		io.sockets.emit('sendAddLog', { id: arr[0], name: arr[1], beep: 2, status: 4, shot: '' });
		logger(clientIP + ' actionClear Camera ' + data);
	}); 
	
    // 사용자 수동 등록 manualAdd 메뉴얼
    socket.on('actionClearM', function (data) {
		// sensorName, userName, actionDesc
		var arr = data.split("_||_");
		insertEvent(0, 900, 'NA', arr[1], arr[2], '', 4, arr[3]); 
		io.sockets.emit('sendAddLog', { name: arr[1], status: 4 });
		logger(clientIP + ' actionClear Manual ' + data);
	}); 
	
    // 클라이언트 요청(팬스클릭)시 한시간 동안 센서에서 발생된 로그를 보내준다.
    socket.on('sensorLog', function (data) { // sensorLog : SVG에 선언된 센서의 ID
		var sensorID = data;
		getEvtLog(sensorID, function(err, row) { // 데이터베이스 내 테이블 읽어오기
			if (err) {
				console.log(err);
			} else {
				io.sockets.emit('sendListLog', {logList:row}); // Client로 전송
			}
		});
 		logger(clientIP + ' sensorLog ' + data);
	}); 

	// 지난 하루치 또는 한시간 로그
    socket.on('sensorLogRequest', function (data) {
		var sensorID = data;
		// 센서아이디(sensorID)가 있으면 센서관련 하루치 정보 전송
		// 없으면 전체로그중 한시간 동안의 정보 전송
		getEvtLogOneDay(sensorID, function(err, row) { 
			if (err) {
				console.log(err);
			} else {
				if(sensorID)
					io.sockets.emit('sensorLogOneDay', {logList:row});
				else
					io.sockets.emit('sensorLogOneHour', {logList:row});
			}
		});
 		logger(clientIP + ' sensorLogRequest ' + data);
	}); 
	
	// 펜스 최종상태 데이터베이스 정보로 클라이인트가 시작되거나 새로 고침시 실행
    socket.on('getLastSituation', function (data) { 
		getEvtLastLog(function(err, row) { 
			if (err) {
				console.log(err);
			} else {
				io.sockets.emit('getLastSituation', {logList:row});
				// console.log(row);
			}
		});
 		logger(clientIP + ' getLastSituation ');
	}); 
	
	// 카메라 컨트롤
	socket.on('ptzSetPos', function(data) { // 시스템 어카운트 정보 저장
		var addr = data.addr;
		var user = data.user;
		var pass = data.pass;
		var model = data.model;
		var query = data.query;
		if ( typeof(icc[model]) !== "undefined" && icc[model].ptzControl !== null ) { 
			logger(clientIP + ' ptzSetPos ' + addr+','+user+','+pass+','+icc[model].ptzControl+','+query);
			ptzSetPos(addr, user, pass, icc[model].ptzControl, query); // 쿼리명령 수행
			// console.log(data); // 로그등록
		}
	});
});
app.listen(portOut); // Display server
console.log('Open Port http://localhost:'+portOut+'/');

