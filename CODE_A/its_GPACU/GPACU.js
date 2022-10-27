///////////////////////////////////////////////////
// https://github.com/fivdi/onoff
// https://www.npmjs.com/package/onoff -- writeSync 모듈
// https://webofthings.org/2016/10/23/node-gpio-and-the-raspberry-pi/
///////////////////////////////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var gpio = require('onoff').Gpio; 

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfg = JSON.parse(fs.readFileSync('/home/pi/GPACU/gpacu.json', 'utf8')); // 환경 파일 읽기
var portIn = cfg.interface.portIn;
var portOut = cfg.interface.portOut;
var html = fs.readFileSync(cfg.file.html_target, 'utf8');

///////////////////////////////////////////////////////////
// Relay01 = { 1:18, 2:23, 3:24, 4:25 } # GPIO 논리:실제, 출력: 1 ~ 4
// Poweio01 = { 1:12 }
// Sensoio01 = { 1:19, 2:13, 3:6, 4:5, 5:22, 6:27, 7:17, 8:4 } # GPIO 입력: 1 ~ 8 예) GPIN[3] -> 6
///////////////////////////////////////////////////////////

// Gpio 방향설정을 'OUT'으로 하면 기존에 실행하고 있는 프로그램에 영향을 끼침.(?)
// Watch 기능을 사용하려먼 Edge값을 설정 해야 한다. both가 아닌경우 센서값에 반을이 없을수 있다. values are: 'none', 'rising', 'falling', 'both'. 
var GPACU = new Array();
for (var key in cfg["setIO"]) {
	// check if the property/key is defined in the object itself, not in parent
	if (cfg["setIO"].hasOwnProperty(key)) {
		console.log(key, cfg["setIO"][key]);
		if (cfg["setIO"][key]) {
			GPACU[key] = new gpio(cfg["gpio"][key], 'out', 'both');
		} else {
			GPACU[key] = new gpio(cfg["gpio"][key], 'in', 'both');
		}
	} // cfg["gpio"][key] -> "io01"
}
GPACU['pw01'] = new gpio(12, 'out', 'both');
GPACU['pw02'] = new gpio(8,  'out', 'both');

// for (var key in cfg["setIO"]) {
// 	GPACU[key] = new gpio(cfg["gpio"][key], 'out', 'both');
// }
// GPACU['pw01'] = new gpio(12, 'out', 'both');
// GPACU['pw02'] = new gpio(8,  'out', 'both');

var GPIO = new Array();
GPIO['io01'] = '19';
GPIO['io02'] = '13';
GPIO['io03'] = '6';
GPIO['io04'] = '5';
GPIO['io05'] = '22';
GPIO['io06'] = '27';
GPIO['io07'] = '17';
GPIO['io08'] = '4';
GPIO['io09'] = '26';
GPIO['io10'] = '21';
GPIO['io11'] = '20';
GPIO['io12'] = '16';
GPIO['io13'] = '7';
GPIO['io14'] = '25';
GPIO['io15'] = '24';
GPIO['io16'] = '23';
GPIO['pw01'] = '12';
GPIO['pw02'] = '8';

var portID = new Array();
portID['1']	= 'io01';
portID['2']	= 'io02';
portID['3']	= 'io03';
portID['4']	= 'io04';
portID['5']	= 'io05';
portID['6']	= 'io06';
portID['7']	= 'io07';
portID['8']	= 'io08';
portID['9']	= 'io09';
portID['10']= 'io10';
portID['11']= 'io11';
portID['12']= 'io12';
portID['13']= 'io13';
portID['14']= 'io14';
portID['15']= 'io15';
portID['16']= 'io16';
portID['17']= 'pw01';
portID['18']= 'pw02';


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
	console.log(id)
}

//////////////////////////////////////////////////////////
// 1. Client로 부터 이벤트를 받고 관련 작업 실행
//////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) {
	// 클라이언트 사이드에서 최초 접근시 현상태 전송
	socket.on('getCurrentStatus', function () {
		event_send('io01',GPACU['io01'].readSync(), '');
		event_send('io02',GPACU['io02'].readSync(), '');
		event_send('io03',GPACU['io03'].readSync(), '');
		event_send('io04',GPACU['io04'].readSync(), '');
		event_send('io05',GPACU['io05'].readSync(), '');
		event_send('io06',GPACU['io06'].readSync(), '');
		event_send('io07',GPACU['io07'].readSync(), '');
		event_send('io08',GPACU['io08'].readSync(), '');
		event_send('io09',GPACU['io09'].readSync(), '');
		event_send('io10',GPACU['io10'].readSync(), '');
		event_send('io11',GPACU['io11'].readSync(), '');
		event_send('io12',GPACU['io12'].readSync(), '');
		event_send('io13',GPACU['io13'].readSync(), '');
		event_send('io14',GPACU['io14'].readSync(), '');
		event_send('io15',GPACU['io15'].readSync(), '');
		event_send('io16',GPACU['io16'].readSync(), '');

		event_send('pw01',GPACU['pw01'].readSync(), '');
		event_send('pw02',GPACU['pw02'].readSync(), '');
	});

	// 클라이언트네서 버튼을 클릭하면 실행
	// 단 아이디 명에 따라 제한적 실행을 한다.
	socket.on('btnClick', function(id) {
		// console.log("Current Set " + GPACU[id].readSync());
		if(cfg["setIO"][id] || cfg["setPW"][id]) { //  S : 센서 입력 포트, P : 센서 전원
			try {
				// console.log(GPACU[id], id);
				GPACU[id].writeSync(GPACU[id].readSync() ^ 1); // 토글
			} catch (e) {
				console.log("writeSync error");
			}
			event_send(id,GPACU[id].readSync(), ''); // 현재 설정된 값을 반환 한다.
		} else { // R : 릴레이 입출력 포트
			// GPIO 테스트 포트확인후 관련 정보 적용
			if(cfg["lst_gpio"][GPIO[id]] != undefined) {

			}
		}
	});
});

app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 2. 외부로 부터 portIn(18040)을 통해 정보를 받아 관련작업 수행(파싱) / portOut 으로 전달한다.
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

		var id = portID[obj['id']]; // GPIO Port No.를 내부 사용명으로 변경
		
		if(id) {
			;
		} else {
			return 0;
		}
		var status = parseInt(obj['status']); // 숫자로 치환
		var msg = obj['msg']; // 메세지
		
		// console.log('\n'+id+'/'+status+'/'+msg);
		// console.log(GPACU[id].readSync());

		if (GPACU[id].readSync() != status) { // 현재 상태와 요청 상태가 다를시 실행
			try {
				GPACU[id].writeSync(status);
			} catch (e) {
				console.log("Relay#" + id + " GPIO#" + obj['id'] + " writeSync error");
			}
		}
		
		event_send(id, GPACU[id].readSync(), ''); // 현재 설정된 값을 반환 한다.

		socket.emit('received');
	});
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');

////////////////////////////////////////////////////
// 3. Watch 기능으로 부터 실행
///////////////////////////////////////////////////
GPACU['io01'].watch(function(err, state) { event_send('io01',state, ''); });
GPACU['io02'].watch(function(err, state) { event_send('io02',state, ''); });
GPACU['io03'].watch(function(err, state) { event_send('io03',state, ''); });
GPACU['io04'].watch(function(err, state) { event_send('io04',state, ''); });
GPACU['io05'].watch(function(err, state) { event_send('io05',state, ''); });
GPACU['io06'].watch(function(err, state) { event_send('io06',state, ''); });
GPACU['io07'].watch(function(err, state) { event_send('io07',state, ''); });
GPACU['io08'].watch(function(err, state) { event_send('io08',state, ''); });
GPACU['io09'].watch(function(err, state) { event_send('io09',state, ''); });
GPACU['io10'].watch(function(err, state) { event_send('io10',state, ''); });
GPACU['io11'].watch(function(err, state) { event_send('io11',state, ''); });
GPACU['io12'].watch(function(err, state) { event_send('io12',state, ''); });
GPACU['io13'].watch(function(err, state) { event_send('io13',state, ''); });
GPACU['io14'].watch(function(err, state) { event_send('io14',state, ''); });
GPACU['io15'].watch(function(err, state) { event_send('io15',state, ''); });
GPACU['io16'].watch(function(err, state) { event_send('io16',state, ''); });
GPACU['pw01'].watch(function(err, state) { event_send('pw01',state, ''); });
GPACU['pw02'].watch(function(err, state) { event_send('pw02',state, ''); });

// console.log(GPACU);
console.log('Start WebGPIO');