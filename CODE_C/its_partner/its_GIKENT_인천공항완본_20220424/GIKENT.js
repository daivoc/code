///////////////////////////////////////////////////
// https://github.com/fivdi/onoff
// https://www.npmjs.com/package/onoff -- writeSync 모듈
///////////////////////////////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var mysql = require('mysql');
var net = require('net');

var client_PY = new net.Socket();

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfgJson = process.argv[2];
var cfg = JSON.parse(fs.readFileSync(cfgJson, 'utf8')); // 환경 파일 읽기
var port_JS_in = cfg.interface.port_JS_in;
var port_JS_out = cfg.interface.port_JS_out;
var port_PY_in = cfg.interface.port_PY_in;
var html = fs.readFileSync(cfg.file.html_target, 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
	res.end(html);
}
function today_total() { // 오늘의 합계 (approved, unknown)
	var con = mysql.createConnection({host:cfg["mysql"]["host"], user:cfg["mysql"]["user"], password:cfg["mysql"]["pass"], database:cfg["mysql"]["name"]});
	con.connect(function(err) {
		if (err) {
			console.log('Retry today_total(con.connect)', err);
			// setTimeout(today_total(), 2000); // 접속 재시도
			return;
		} else {
			// 승인 합계
			// 오늘의 통계 (approved)
			query_approved = "SELECT IFNULL(SUM(w_ax_cnt),0)AS todaySumA FROM "+cfg['log_table']['tbl_live']+" WHERE DATE(`w_stamp`) = CURDATE() AND `w_approved` > 0 "
			con.query(query_approved, function (err, result, fields) {
				if (err) throw err;
				for(key in result[0]) {
					if(result[0][key]>0) {
						io.sockets.emit('totalEventOn', { id: key, value: result[0][key] }); 
					}
				}
			});

			// 오늘의 통계 (unknown)
			query_unknown = "SELECT IFNULL(SUM(w_ax_cnt),0)AS todaySumU,IFNULL(SUM(w_xa_cnt),0)AS todaySumR FROM "+cfg['log_table']['tbl_live']+" WHERE DATE(`w_stamp`) = CURDATE() AND `w_unknown` > 0 "
			con.query(query_unknown, function (err, result, fields) {
				if (err) throw err;
				for(key in result[0]) {
					if(result[0][key]>0) {
						io.sockets.emit('totalEventOn', { id: key, value: result[0][key] }); 
					}
				}
			});

			// 오늘의 통계 (denial)
			query_denial = "SELECT IFNULL(SUM(w_multiple),0)AS todaySumD FROM "+cfg['log_pmt']['tbl_live']+" WHERE DATE(`w_stamp`) = CURDATE() "
			con.query(query_denial, function (err, result, fields) {
				if (err) throw err;
				for(key in result[0]) {
					if(result[0][key]>0) {
						io.sockets.emit('totalEventOn', { id: key, value: result[0][key] }); 
					}
				}
			});
		}
		con.end();
	});
}
// 전체합계 - 모든 이벤트 취합후 합산한후 전송(totalEventOn)
function grand_total() {
	var con = mysql.createConnection({host:cfg["mysql"]["host"], user:cfg["mysql"]["user"], password:cfg["mysql"]["pass"], database:cfg["mysql"]["name"]});
	con.connect(function(err) {
		if (err) {
			console.log('Retry today_total(con.connect)', err);
			// setTimeout(grand_total(), 2000); // 접속 재시도
			return;
		} else {
			// 승인 합계
			queryTotal = "SELECT IFNULL(SUM(w_ax_cnt),0)AS aT_0,IFNULL(SUM(w_xa_cnt),0)AS aT_1,IFNULL(SUM(w_bx_cnt),0)AS aT_2,IFNULL(SUM(w_xb_cnt),0)AS aT_3,IFNULL(SUM(w_cx_cnt),0)AS aT_4,IFNULL(SUM(w_xc_cnt),0)AS aT_5,IFNULL(SUM(w_dx_cnt),0)AS aT_6,IFNULL(SUM(w_xd_cnt),0)AS aT_7 FROM " + cfg['log_table']['tbl_live'] + " WHERE w_approved > 0 "
			con.query(queryTotal, function (err, result, fields) {
				if (err) throw err;
				for(key in result[0]) {
					if(result[0][key]>0) {
						io.sockets.emit('totalEventOn', { id: key, value: result[0][key] }); 
					}
				}
			});
			// 비승인 합계
			queryTotal = "SELECT IFNULL(SUM(w_ax_cnt),0)AS uT_0,IFNULL(SUM(w_xa_cnt),0)AS uT_1,IFNULL(SUM(w_bx_cnt),0)AS uT_2,IFNULL(SUM(w_xb_cnt),0)AS uT_3,IFNULL(SUM(w_cx_cnt),0)AS uT_4,IFNULL(SUM(w_xc_cnt),0)AS uT_5,IFNULL(SUM(w_dx_cnt),0)AS uT_6,IFNULL(SUM(w_xd_cnt),0)AS uT_7 FROM " + cfg['log_table']['tbl_live'] + " WHERE w_unknown > 0 "
			con.query(queryTotal, function (err, result, fields) {
				if (err) throw err;
				for(key in result[0]) {
					if(result[0][key]>0) {
						io.sockets.emit('totalEventOn', { id: key, value: result[0][key] }); 
					}
				}
			});
			// 전체 합계
			queryTotal = "SELECT IFNULL(SUM(w_ax_cnt),0)AS gT_0,IFNULL(SUM(w_xa_cnt),0)AS gT_1,IFNULL(SUM(w_bx_cnt),0)AS gT_2,IFNULL(SUM(w_xb_cnt),0)AS gT_3,IFNULL(SUM(w_cx_cnt),0)AS gT_4,IFNULL(SUM(w_xc_cnt),0)AS gT_5,IFNULL(SUM(w_dx_cnt),0)AS gT_6,IFNULL(SUM(w_xd_cnt),0)AS gT_7 FROM "+cfg['log_table']['tbl_live']
			con.query(queryTotal, function (err, result, fields) {
				if (err) throw err;
				for(key in result[0]) {
					if(result[0][key]>0) {
						io.sockets.emit('totalEventOn', { id: key, value: result[0][key] }); 
					}
				}
			});
		}
		con.end();
	});
}

function globalConfig() {
	// 정의된 환경 변수
	io.sockets.emit('globalConfig', cfg); 
}

//////////////////////////////////////////////////////////
// 부모 프로세서(GIKENT.py)에 접속
// client_PY.write('open_gate');
//////////////////////////////////////////////////////////
client_PY.connect(port_PY_in, 'localhost', function() {
    console.log('\tClient connected to: ' + 'localhost' + ':' + port_PY_in);
});
client_PY.on('data', function(data) {
    console.log('Received: ' + data);
});
client_PY.on('error', function(err) {
    console.error(err);
});

//////////////////////////////////////////////////////////
// 브라우저로부터 이벤트를 받고 관련 작업 실행
//////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) {
	// var address = socket.handshake.address;
	var clientIp = socket.request.connection.remoteAddress.split(":")[3]; // ::ffff:192.168.0.2

	// 외부 접근가능한 아이피 필터링
	if(cfg.server.accessible.length) {
		if(cfg.server.accessible.includes(clientIp)){
			console.log('New connection from ' + clientIp);
		} else {
			console.log('Rejected connection of ' + clientIp);
			io.sockets.emit('kill_client'); // 크라이언트 접속 거부
		}
	}

	socket.on('disconnect', function() {
		console.log('Disconnection from ' + clientIp);
	});

	// 클라이언트서 요청한 명령에 따라 제한적 실행을 한다.
	// 저장된 전체 이벤트 합계
	socket.on('read_total', function(data) {
		globalConfig();
		grand_total();
		today_total();
	});

	// 관리자 요청에 따른 명령 (to GIKENT.py)
	socket.on('command_open', function(data) { // 게이트 열기
		client_PY.write('command_open');
	});
	socket.on('command_renewal', function(data) { // 베이스 이미지 재 생성
		client_PY.write('command_renewal');
	});
	socket.on('command_antiDenial', function(data) { // 게이트 잠금
		client_PY.write('command_antiDenial');
	});
	socket.on('command_antiTailing', function(data) { // 게이트 잠금
		client_PY.write('command_antiTailing');
	});
	socket.on('command_setLock', function(data) { // 게이트 잠금
		client_PY.write('command_setLock');
	});
	socket.on('command_setOpen', function(data) { // 게이트 풀림
		client_PY.write('command_setOpen');
	});
	socket.on('command_release', function(data) { // 게이트 멸령 해지
		client_PY.write('command_release');
	});
	socket.on('command_status', function(data) { // 상태 업데이트
		client_PY.write('command_status');
	});
});

app.listen(port_JS_out); // Display server
console.log('\tService server running at http://localhost:'+port_JS_out+'/');

//////////////////////////////////////////////////////////
// 외부에서 port_JS_in을 통해 정보를 받아 관련작업 수행(파싱) / port_JS_out 으로 전달한다.
// 예: id=ID : relay 번호, status=STATUS 0:off 1:on, msg=MSG
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
	socket.on('data', function (data) { // 외부 port_JS_in 으로 부터 받은 정보를 data 변수에 저장
		// var json;
		// try {
		// 	json = JSON.parse(data);
		// 	for(key in json){
		// 		// console.log(key, json[key]);
		// 		io.sockets.emit(key, json[key]); // 오늘합계
		// 	}
		// } catch(e) {
		// 	return console.error(e, "Error : JSON.parse");
		// 	// console.log(e, "Error : JSON.parse"); // error in the above string (in this case, yes)!
		// }

		var json = JSON.parse(data);
		for(key in json){
			// console.log(key, json[key]);
			io.sockets.emit(key, json[key]); // 오늘합계
		}
	});
}).listen(port_JS_in); // Receive server
console.log('\tReceive server running at http://localhost:'+port_JS_in+'/');