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
var cfgJson = './gikenc.json';
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

function get_date(type='full') {
	let date_ob = new Date();
	let year = date_ob.getFullYear(); // current year
	let month = ("0" + (date_ob.getMonth() + 1)).slice(-2); // current month
	let date = ("0" + date_ob.getDate()).slice(-2); // current date
	let hours = date_ob.getHours(); // current hours
	let minutes = date_ob.getMinutes(); // current minutes
	let seconds = date_ob.getSeconds(); // current seconds

	if (type == 'full') {
		return(year + "-" + month + "-" + date + " " + hours + ":" + minutes + ":" + seconds);
	} else if (type == 'day') {
		return(year + "-" + month + "-" + date);
	} else if (type == 'time') {
		return(hours + ":" + minutes);
	} else {
		return type;
	}

	// console.log(year + "-" + month + "-" + date + " " + hours + ":" + minutes + ":" + seconds); // prints date & time in YYYY-MM-DD HH:MM:SS format
	// console.log(year + "-" + month + "-" + date); // prints date in YYYY-MM-DD format
	// console.log(hours + ":" + minutes); // prints time in HH:MM format

}


function dateTotal(subDate = 0) { // 오늘의 합계 JSON 집계: 저장위치 "/var/www/html/its_web/theme/ecos-its_optex/user/image/gikenC/counting"
	var con = mysql.createConnection({host:cfg["mysql"]["host"], user:cfg["mysql"]["user"], password:cfg["mysql"]["pass"], database:cfg["mysql"]["name"]});
	con.connect(function(err) {
		if (err) {
			console.log('Retry date Total(con.connect)', err);
			return;
		} else {
			query_approved = "SELECT \
			IFNULL(SUM(w_ax_cnt),0)AS sum_ax, \
			IFNULL(SUM(w_xa_cnt),0)AS sum_xa, \
			IFNULL(SUM(w_bx_cnt),0)AS sum_bx, \
			IFNULL(SUM(w_xb_cnt),0)AS sum_xb, \
			IFNULL(SUM(w_cx_cnt),0)AS sum_cx, \
			IFNULL(SUM(w_xc_cnt),0)AS sum_xc, \
			IFNULL(SUM(w_dx_cnt),0)AS sum_dx, \
			IFNULL(SUM(w_xd_cnt),0)AS sum_xd \
			FROM "+cfg['log_table']['tbl_live']+" WHERE DATE(`w_stamp`) = SUBDATE(CURRENT_DATE, "+ subDate +")" // CURDATE()-오늘, SUBDATE(CURRENT_DATE, 1)-어제
			con.query(query_approved, function (err, result, fields) {
				if (err) throw err;
				dateTotalOn = {};
				for(key in result[0]) {
					if(result[0][key]>0) {
						dateTotalOn[key] = result[0][key];
					}
				}
				io.sockets.emit('dateTotalOn', dateTotalOn); 
				// var cfgPath = cfg.file.image_counting+'/'+dateIs; // dateIs - 날짜가 바뀐후 어제 일자 통계 처리
				// fs.writeFileSync(cfgPath, JSON.stringify(dateTotalOn, null, 4), 'utf8'); // 환경 파일 저장
			});
		}
		con.end();
	});
}
// 전체합계 - 모든 이벤트 취합후 합산한후 전송(eventTotalOn)
function grandTotal() {
	var con = mysql.createConnection({host:cfg["mysql"]["host"], user:cfg["mysql"]["user"], password:cfg["mysql"]["pass"], database:cfg["mysql"]["name"]});
	con.connect(function(err) {
		if (err) {
			console.log('Retry grand Total(con.connect)', err);
			// setTimeout(grandTotal(), 2000); // 접속 재시도
			return;
		} else {
			// 전체 합계
			queryTotal = "SELECT \
			IFNULL(SUM(w_ax_cnt),0)AS gT_0, \
			IFNULL(SUM(w_xa_cnt),0)AS gT_1, \
			IFNULL(SUM(w_bx_cnt),0)AS gT_2, \
			IFNULL(SUM(w_xb_cnt),0)AS gT_3, \
			IFNULL(SUM(w_cx_cnt),0)AS gT_4, \
			IFNULL(SUM(w_xc_cnt),0)AS gT_5, \
			IFNULL(SUM(w_dx_cnt),0)AS gT_6, \
			IFNULL(SUM(w_xd_cnt),0)AS gT_7 FROM "+cfg['log_table']['tbl_live']
			con.query(queryTotal, function (err, result, fields) {
				if (err) throw err;
				eventTotalOn = {};
				for(key in result[0]) {
					if(result[0][key]>0) {
						eventTotalOn[key] = result[0][key];
					}
				}
				io.sockets.emit('eventTotalOn', eventTotalOn); 
			});
		}
		con.end();
	});
}

//////////////////////////////////////////////////////////
// 부모 프로세서(GIKENC.py)에 접속
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
	} else {
		console.log('New connection from ' + clientIp);
	}

	// 클라이언트서 요청한 명령에 따라 제한적 실행을 한다.
	// 저장된 전체 이벤트 합계
	socket.on('date_total', function(data) {
		// dateTotal(0); // Today
		// dateTotal(1); // Yesterday
		dateTotal(data); // Yesterday
	});
	
	socket.on('gChkBox', function(data) { // 상태 업데이트
		client_PY.write(JSON.stringify({'gChkBox':data})); // .pyc에 전송
		var cfgPath = cfg.path.gikenc+'/config.json';
		var config = JSON.parse(fs.readFileSync(cfgPath, 'utf8')); // 환경 파일 읽기
		config['gChkBox'] = data;
		fs.writeFileSync(cfgPath, JSON.stringify(config, null, 4), 'utf8'); // 환경 파일 저장
		cfg['gChkBox'] = data; // 실행중인 변수값에 적용
	});
	
	socket.on('status_chkBox', function(data) { // 상태 업데이트
		io.sockets.emit('statusChkBox', cfg['gChkBox']); // 정의된 환경 변수 클라이언트에 전송
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
		try {
			json = JSON.parse(data);
			for(key in json){
				// console.log(key, json[key]);
				if(key == 'dateTotal') {
					dateTotal(json[key]); // 어제의 합계를 JSON형식으로 오늘 방에 저장 한다.
				} else { // 조건 이외의 모든 요청은 Client(브라우저)로 전송
					io.sockets.emit(key, json[key]);
				}
			}
		} catch(e) {
			console.log(e, "Error : JSON.parse"); // error in the above string (in this case, yes)!
			return "Error : JSON.parse";
		}
	});
}).listen(port_JS_in); // Receive server
console.log('\tReceive server running at http://localhost:'+port_JS_in+'/');