///////////////////////////////////////////////////
// https://github.com/fivdi/onoff
// https://www.npmjs.com/package/onoff -- writeSync 모듈
// https://webofthings.org/2016/10/23/node-gpio-and-the-raspberry-pi/
///////////////////////////////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io')(app); // .listen(app);
var fs = require('fs');
var gpio = require('onoff').Gpio; 

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfg = JSON.parse(fs.readFileSync('/home/pi/GPWIO/gpwio.json', 'utf8')); // 환경 파일 읽기
var portIn = cfg.interface.portIn;
var portOut = cfg.interface.portOut;
var html = fs.readFileSync(cfg.file.html_target, 'utf8');



///////////////////////////////////////////////////////////
// Relay01 = { 1:18, 2:23, 3:24, 4:25 } # GPIO 논리:실제, 출력: 1 ~ 4
// Power01 = { 1:12 }
// Sensor01 = { 1:19, 2:13, 3:6, 4:5, 5:22, 6:27, 7:17, 8:4 } # GPIO 입력: 1 ~ 8 예) GPIN[3] -> 6
///////////////////////////////////////////////////////////

// Gpio 방향설정을 'OUT'으로 하면 기존에 실행하고 있는 프로그램에 영향을 끼침.(?)
// Watch 기능을 사용하려먼 Edge값을 설정 해야 한다. both가 아닌경우 센서값에 반을이 없을수 있다. values are: 'none', 'rising', 'falling', 'both'. 
var GPWIO = new Array();
GPWIO['R01'] = new gpio(18, 'out', 'both');
GPWIO['R02'] = new gpio(23, 'out', 'both');
GPWIO['R03'] = new gpio(24, 'out', 'both');
GPWIO['R04'] = new gpio(25, 'out', 'both');
GPWIO['P01'] = new gpio(12, 'out', 'both');
GPWIO['S01'] = new gpio(19, 'in', 'both');
GPWIO['S02'] = new gpio(13, 'in', 'both');
GPWIO['S03'] = new gpio(6,  'in', 'both');
GPWIO['S04'] = new gpio(5,  'in', 'both');
GPWIO['S05'] = new gpio(22, 'in', 'both');
GPWIO['S06'] = new gpio(27, 'in', 'both');
GPWIO['S07'] = new gpio(17, 'in', 'both');
GPWIO['S08'] = new gpio(4,  'in', 'both');

// 초기값 강제 설정 
GPWIO['R01'].writeSync(1)
GPWIO['R02'].writeSync(1)
GPWIO['R03'].writeSync(1)
GPWIO['R04'].writeSync(1)

var GPIO = new Array();
GPIO['S01'] = '19';
GPIO['S02'] = '13';
GPIO['S03'] = '6';
GPIO['S04'] = '5';
GPIO['S05'] = '22';
GPIO['S06'] = '27';
GPIO['S07'] = '17';
GPIO['S08'] = '4';

var portID = new Array();
portID['18'] = 'R01';
portID['23'] = 'R02';
portID['24'] = 'R03';
portID['25'] = 'R04';

portID['12'] = 'P01';

portID['19'] = 'S01';
portID['13'] = 'S02';
portID['6'] = 'S03';
portID['5'] = 'S04';
portID['22'] = 'S05';
portID['27'] = 'S06';
portID['17'] = 'S07';
portID['4'] = 'S08';

var linkID = new Array();
linkID['1'] = 'R01';
linkID['2'] = 'R02';
linkID['3'] = 'R03';
linkID['4'] = 'R04';

var relayDeny = new Array();
relayDeny['R01'] = 0;
relayDeny['R02'] = 0;
relayDeny['R03'] = 0;
relayDeny['R04'] = 0;

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

//////////////////////////////////////////////////////////
// 소켓을 통해 자료를 index.html로 전송한다.
//////////////////////////////////////////////////////////
function event_send(id, status, msg) {
	io.sockets.emit('io_status', { id: id, status: status, msg: msg });
}

//////////////////////////////////////////////////////////
// Client로부터 이벤트를 받고 관련 작업 실행
//////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) {
	// 클라이언트 사이드에서 최초 접근시 현상태 전송
    socket.on('getCurrentStatus', function () {
		event_send('R01',GPWIO['R01'].readSync(), '');
		event_send('R02',GPWIO['R02'].readSync(), '');
		event_send('R03',GPWIO['R03'].readSync(), '');
		event_send('R04',GPWIO['R04'].readSync(), '');
		event_send('P01',GPWIO['P01'].readSync(), '');
		event_send('S01',GPWIO['S01'].readSync(), '');
		event_send('S02',GPWIO['S02'].readSync(), '');
		event_send('S03',GPWIO['S03'].readSync(), '');
		event_send('S04',GPWIO['S04'].readSync(), '');
		event_send('S05',GPWIO['S05'].readSync(), '');
		event_send('S06',GPWIO['S06'].readSync(), '');
		event_send('S07',GPWIO['S07'].readSync(), '');
		event_send('S08',GPWIO['S08'].readSync(), '');
    });
	
	// 클라이언트네서 버튼을 클릭하면 실행
	// 단 아이디 명에 따라 제한적 실행을 한다.
    socket.on('btnClick', function(id) {
		// console.log("Current Set " + GPWIO[id].readSync());
		if(id.charAt(0) == 'S') { //  S : 센서 입력 포트
			// GPIO 테스트 포트확인후 관련 정보 적용
			if(cfg["lst_gpio"][GPIO[id]] != undefined) {
				// console.log(cfg["lst_gpio"][GPIO[id]]["serial"]);
				var name = cfg["lst_gpio"][GPIO[id]]["name"];
				var addr1 = cfg["lst_gpio"][GPIO[id]]["addr1"];
				var addr2 = cfg["lst_gpio"][GPIO[id]]["addr2"];
				var port1 = cfg["lst_gpio"][GPIO[id]]["port1"];
				var port2 = cfg["lst_gpio"][GPIO[id]]["port2"];
				var id = cfg["lst_gpio"][GPIO[id]]["serial"];
				
				var data =('id='+id+',name='+name+',beep=1,status=1');
				if ( addr1 !== "null" && port1 !== 0) {
					var con1 = getConnection(addr1, port1); // TCP 포트 접속
					con1.write(data);
					con1.end();
				}
				if ( addr2 !== "null" && port2 !== 0) {
					var con2 = getConnection(addr2, port2); // TCP 포트 접속
					con2.write(data);
					con2.end();
				}
			}
		} else { // P, R : 센서 전원 또는 릴레이 입출력 포트
			try {
				// console.log(GPWIO[id], id);
				GPWIO[id].writeSync(GPWIO[id].readSync() ^ 1); // 토글
			} catch (e) {
				console.log("writeSync error");
			}
			event_send(id,GPWIO[id].readSync(), ''); // 현재 설정된 값을 반환 한다.
		}
    });
});

app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 외부에서 portIn을 통해 정보를 받아 관련작업 수행(파싱) / portOut 으로 전달한다.
// 예: id=ID : relay 번호, status=STATUS 0:off 1:on, msg=MSG
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    // console.log("connected");
    socket.on('data', function (data) { // 외부 portIn 으로 부터 받은 정보를 data 변수에 저장
		var alarmInfo = data.toString();
		var obj = alarmInfo.split(",").reduce(function(o, c){
		   var arr = c.split("=");
		   return o[arr[0].trim()] = arr[1].trim(), o; // comma operator
		},{});
		
		// console.log(obj);
	
		// var id = linkID[obj['id']]; // GPIO Port No.를 내부 사용명으로 변경
		var id = portID[obj['id']]; // GPIO Port No.를 내부 사용명으로 변경
		
		if(id) {
			;
		} else {
			return 0;
		}
		var status = parseInt(obj['status']); // 숫자로 치환
		var msg = obj['msg']; // 메세지
		
		// console.log('\n'+id+'/'+status+'/'+msg);
		// console.log(GPWIO[id].readSync());

		if (GPWIO[id].readSync() != status) { // 현재 상태와 요청 상태가 다를시 실행
			try {
				GPWIO[id].writeSync(status);
			} catch (e) {
				console.log("writeSync error");
			}
		}
		
		event_send(id, GPWIO[id].readSync(), ''); // 현재 설정된 값을 반환 한다.

		socket.emit('received');
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');


//////////////////////////////////////////////////////////
// TCP 서버 및 클라이언트 - https://namik.tistory.com/114
// IMS 또는 외부 과제 서버로 상태 전송
// F:\Development\ecos_its-OPTEX\its_MONITOR\its_M_map.js
//////////////////////////////////////////////////////////
function getConnection(host, port){
	//서버에 해당 포트로 접속 
	var client = ""; 
	var local_port = ""; 
	
	client = require('net').connect({port:port, host:host}, function() {
		local_port = this.localPort; 
		this.setEncoding('utf8'); 
		this.setTimeout(60000); // timeout : 1분 = 60000, 10분 = 600000
		/* 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음
		console.log("connect log ================================="); 
		console.log('connect success'); 
		console.log('local = ' + this.localAddress + ':' + this.localPort); 
		console.log('remote = ' + this.remoteAddress + ':' +this.remotePort); 
		console.log("client setting Encoding:binary, timeout:600000" ); 
		console.log("client connect localport : " + local_port);
		*/
	});
	
	/* 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음
	
	// 데이터 수신 후 처리 
	var recvData = [];  
	client.on('data', function(data) { 
		console.log("data recv log ================================="); 
		recvData.push(data); 
		console.log("data.length : " + data.length);
		console.log("data recv : " + data);
		client.end(); // 접속된 소켓을 제거 한다.
	}); 
	*/
	// client.on('close', function() { console.log("closed localport : " + local_port); }); // 접속 종료 시 처리 
	// client.on('end', function() { console.log('client Socket End'); }); // 소켓 종료
	client.on('error', function(err) { console.log('client Socket Error: '+ JSON.stringify(err)); }); 
	client.on('timeout', function() { console.log('client Socket timeout: '); }); 
	client.on('drain', function() { console.log('client Socket drain: '); }); 
	client.on('lookup', function() { console.log('client Socket lookup: '); }); 
	
	return client;
}

// DIVI Sys Api 서버에 해당 포트로 접속후 데이터 전송
// ########################################
// ## NVR(Server) 서버는 센서서버(client)의 연결을 기다립니다.
// ## 센서서버에 NVR 서버의 IP와 PORT를 설정합니다. (기본포트: 2154, 변경가능)
// ## 센서서버는 NVR서버의 IP:PORT에 접속합니다.(연결유지)
// ## 각 구간의 센서에서 이벤트가 발생하면 센서서버는 NVR서버에 해당 코드를 전송합니다.
// ## NVR서버는 수신한 데이터를 동일하게 센서서버로 전송합니다.
// ## 1) 시작코드     : 0x02
// ## 2) 알람발생구간 : "1"  "12" "999"  char형으로 1자리부터 최대 3자리 까지 0x31  0x31 0x32   0x39 0x39 0x39
// ## 3) 구분코드     : 0x3b
// ## 4) 위치코드     : "1"  "2"  ~ "9"     =>  "0"으로 보냅니다.           
// ## 5) 종료코드     : 0x03
// ##    (주의) 알람발생구간 값이 '0'(0x30) 값이면 live 신호입니다.
// ## 예)
// ## PC-MAP  ->  NVR서버
// ## 0x02 "5"   0x3b "2" 0x03   =    5번구간의 2번위치에 이벤트발생
// ## 0x02 "15"  0x3b "3" 0x03   =   15번구간의 3번위치에 이벤트발생
// ## 0x02 "215" 0x3b "1" 0x03   =  215번구간의 1번위치에 이벤트발생
// ## NVR서버는 수신한 내용을 동일하게 리턴합니다.
// ## 구간내에 위치가 지정되지 않기때문에 위치값은 "0"으로 처리 합니다.
// ## 테스트 - /home/pi/utility/customPopupDIVISYS.py
// ## content = 'Format: USER||PASS||IP||Port||opt1||opt2'

// G:\Development\ecos_its-OPTEX\its_GPWIO\GPWIO.js	
// G:\Development\ecos_its-OPTEX\its_MONITOR\its_M_map.js
// # G:\Development\ecos_its-OPTEX\its_GPIO\module.py

function customIpPort_diviNVR(gID) { // 쿼리명령 수행
	cfg.group[gID].customIpPort.forEach(function(value){
		// console.log(value);
		if (!value.opt1.length) {
			return 0;
		}
		
		// opt2가 비어있는경우 99로 치환 한다.
		if (!value.opt2.length) {
			value.opt2 = "99";			
		}
		
		// packet = '\x02' + opt1 + '\x3b' + opt2 + '\x03' 
		var	data = '\x02' + value.opt1.toString(16) + '\x3b' + value.opt2.toString(16) + '\x03';
		
		var client = getConnection(value.host, value.port);
		client.write(data);
		client.end();

		// client.on('error', function(err) { console.log('client Socket Error: '+ JSON.stringify(err)); }); 
		// client.on('timeout', function() { console.log('client Socket timeout: '); }); 
		// client.on('drain', function() { console.log('client Socket drain: '); }); 
		// client.on('lookup', function() { console.log('client Socket lookup: '); }); 
	});	
}

	
/////////////////////
// ITS_SRF 참조
// https://github.com/mafintosh/axis-camera
// https://www.npmjs.com/package/request
// ex) http://192.168.0.38/axis-cgi/com/ptz.cgi?pan=0&tilt=0&zoom=1&focus=1&iris=1&brightness=1&autofocus=on
/////////////////////
var request = require('request')
function customRequest(gID) { // 쿼리명령 수행
	cfg.group[gID].customRequest.forEach(function(value){
		// console.log(value.url);
		if(value.url.indexOf('http://') < 0)
			value.url = 'http://'+value.url;
		request.get(value.url, {
			'auth': {
				'user': value.user,
				'pass': value.pass,
				'sendImmediately': false
			}
		}, function (error, response, body) {
			// console.log('error:', error); // Print the error if one occurred
			// console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
			// console.log('body:', body); // Print the HTML for the Google homepage.
			return ('statusCode:', response && response.statusCode);
		});
	});	
}

// 이밴트 요청에 따른 릴레이 출력제어
// 변수 relayDeny[rID]값이 0일떄만 동작
// setTimeout 기능을 이용 일정시간 단위로 On/Off
function relayOnOff(rID, rTime){
	if(relayDeny[rID]) {
		return;
	} else {
		relayDeny[rID] = 1;
		setTimeout(function(){
			relayDeny[rID] = 0;
			GPWIO[rID].writeSync(0); // 상태 변경
			event_send(rID, GPWIO[rID].readSync(), ''); // 상태 화면 표시
		}, parseInt(rTime * 1000));
		GPWIO[rID].writeSync(1); // 상태 변경
		event_send(rID, GPWIO[rID].readSync(), ''); // 상태 화면 표시
	}
}

// 릴레이 관찰(watch)에 의한 명령 실행
function acAlarm(gID) {
	if ( typeof(cfg.group[gID]) !== "undefined" ) { // 상태가 gpwio의 정의 값과 같으면 관련명령 실행
		// console.log(cfg.status[cfg.group[gID]["status"]],gID);
		var rID = portID[cfg.group[gID]["alertP"]];
		var rTime = cfg.group[gID]["alertV"];

		if ( cfg.group[gID]["sensor"] ) {
			var id = cfg.group[gID]["sensor"];
		} else {
			var id = cfg.group[gID]["gpwio"];
		}
		var name = cfg.group[gID]["name"];
		var beep = 1;
		var status = cfg.group[gID]["status"];
		var data =('id='+id+',name='+name+',beep='+beep+',status='+status);

		// if ( typeof(cfg.group[gID]["alertP"]) !== "null" && cfg.group[gID]["alertP"]) ) { 
		if ( rID && rTime > 0 ) { // rID 값이 있고 rTime이 존재 하면
			// console.log(rID, rTime);
			// 관련 릴레이(rID)을 일정시간(rTime) 활성상태 유지한다.
			relayOnOff(rID, rTime);
		}
		
		if ( cfg.group[gID]["addr1"] !== "null" && cfg.group[gID]["port1"] !== 0) {
			var host = cfg.group[gID]["addr1"];
			var port = cfg.group[gID]["port1"];
			var client_01 = getConnection(host, port);
			client_01.write(data);
			client_01.end();
		}
		if ( cfg.group[gID]["addr2"] !== "null" && cfg.group[gID]["port2"] !== 0) {
			var host = cfg.group[gID]["addr2"];
			var port = cfg.group[gID]["port2"];
			var client_02 = getConnection(host, port);
			client_02.write(data);
			client_02.end();
		}
		customIpPort_diviNVR(gID); // 디비시스 NVR 팝업
		customRequest(gID); // 예를 들어 카메라 프리셋 전송
	}
}

function ckAlarm() {
	var rS = new Array(); // 현재의 이밴트를 저장 한다.
	rS[0] = GPWIO['S01'].readSync();
	rS[1] = GPWIO['S02'].readSync();
	rS[2] = GPWIO['S03'].readSync();
	rS[3] = GPWIO['S04'].readSync();
	rS[4] = GPWIO['S05'].readSync();
	rS[5] = GPWIO['S06'].readSync();
	rS[6] = GPWIO['S07'].readSync();
	rS[7] = GPWIO['S08'].readSync();
	
    /************
	"cover": {
        "00011100": "00010100",
        "10000100": "10000100",
        "11000000": "10000000",
        "11111111": "00000001"
    },
	************/
	Object.keys(cfg.cover).forEach(function(key) {
		var gID = '';
		// 저장된 이벤트를 Key 값 형식으로 변환
		for (var i = 0; i < key.length; i++) {
			// console.log('Key : ' + key + ', Value : ' + cfg.cover[key])
			if (parseInt(key.charAt(i))) { // 한자씩 분할후 숫자 변환alert(key.charAt(i)); 
				gID += rS[i];
			} else {
				gID += '0';
			}
		}
		// console.log(gID);
		// 변환한 이밴트와 Value를 비교, 같으면 acAlarm(gID) 실행
		if(gID == cfg.cover[key]) {
			// console.log(rS);
			acAlarm(gID); // 릴레이 관찰(watch)에 의한 명령 실행
		} else {
			;
		}
	});
}
setInterval(function(){ // 상단 시간 그래프 초기값 0으로 설정
	ckAlarm();
}, 1000);

// Watch 기능 실행
////////////////////////////////////////////////////
GPWIO['P01'].watch(function(err, state) { event_send('P01',state, ''); });
///////////////////////////////////////////////////                     
GPWIO['R01'].watch(function(err, state) { event_send('R01',state, ''); });
GPWIO['R02'].watch(function(err, state) { event_send('R02',state, ''); });
GPWIO['R03'].watch(function(err, state) { event_send('R03',state, ''); });
GPWIO['R04'].watch(function(err, state) { event_send('R04',state, ''); });
////////////////////////////////////////////////////                               
GPWIO['S01'].watch(function(err, state) { event_send('S01',state, ''); });
GPWIO['S02'].watch(function(err, state) { event_send('S02',state, ''); });
GPWIO['S03'].watch(function(err, state) { event_send('S03',state, ''); });
GPWIO['S04'].watch(function(err, state) { event_send('S04',state, ''); });
GPWIO['S05'].watch(function(err, state) { event_send('S05',state, ''); });
GPWIO['S06'].watch(function(err, state) { event_send('S06',state, ''); });
GPWIO['S07'].watch(function(err, state) { event_send('S07',state, ''); });
GPWIO['S08'].watch(function(err, state) { event_send('S08',state, ''); });
///////////////////////////////////////////////////

// // Watch 기능 실행
// ////////////////////////////////////////////////////
// GPWIO['P01'].watch(function(err, state) { event_send('P01',state, ''); });
// ///////////////////////////////////////////////////                     
// GPWIO['R01'].watch(function(err, state) { event_send('R01',state, ''); });
// GPWIO['R02'].watch(function(err, state) { event_send('R02',state, ''); });
// GPWIO['R03'].watch(function(err, state) { event_send('R03',state, ''); });
// GPWIO['R04'].watch(function(err, state) { event_send('R04',state, ''); });
// ////////////////////////////////////////////////////                               
// GPWIO['S01'].watch(function(err, state) { event_send('S01',state, ''); ckAlarm(); });
// GPWIO['S02'].watch(function(err, state) { event_send('S02',state, ''); ckAlarm(); });
// GPWIO['S03'].watch(function(err, state) { event_send('S03',state, ''); ckAlarm(); });
// GPWIO['S04'].watch(function(err, state) { event_send('S04',state, ''); ckAlarm(); });
// GPWIO['S05'].watch(function(err, state) { event_send('S05',state, ''); ckAlarm(); });
// GPWIO['S06'].watch(function(err, state) { event_send('S06',state, ''); ckAlarm(); });
// GPWIO['S07'].watch(function(err, state) { event_send('S07',state, ''); ckAlarm(); });
// GPWIO['S08'].watch(function(err, state) { event_send('S08',state, ''); ckAlarm(); });
// ///////////////////////////////////////////////////


console.log('Start WebGPIO');
