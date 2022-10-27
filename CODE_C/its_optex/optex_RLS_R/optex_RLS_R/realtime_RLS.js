///////////////////////////////////////////////////
// REQUIRED:
// npm i socket.io
// npm i mysql
///////////////////////////////////////////////////

const app = require('http').createServer(handler);
// var io = require('socket.io').listen(app);
const io = require('socket.io')(app);
const fs = require('fs');

///////////////////////////////////////////////////////////////////////////////
// config.json 파일을 읽어 환경설정 한다.
///////////////////////////////////////////////////////////////////////////////
var configName = '/home/pi/optex_RLS_R/config_'+process.argv[2]+'.json';
var cfg = JSON.parse(fs.readFileSync(configName, 'utf8')); // 환경 파일 읽기
var portIn = cfg["interface"]["portIn"];
var portOut = cfg["interface"]["portOut"];

///////////////////////////////////////////////////////////////////////////////
// Html 파일, Client
///////////////////////////////////////////////////////////////////////////////
var html = fs.readFileSync('/home/pi/optex_RLS_R/realtime_RLS_'+portIn+'.html', 'utf8');
// var html = fs.readFileSync('/home/pi/optex_RLS_R/realtime_RLS_'+portIn+'_IMS.html', 'utf8');

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}


// 환경변수(config.json) 저장
function saveConfigJson() {
	fs.writeFile('/home/pi/optex_RLS_R/config_'+portIn+'.json', JSON.stringify(cfg, null, 4), (err) => {
		if (err) throw err;
		// console.log('The file has been saved!');
	});
}

// 환경변수(config.json)에 저장된 마스킹 정보
function readMasking() {
	var masking = '';
	var classmem = cfg.masking;
	for (item in classmem) {
		for (subItem in classmem[item]) {
			// 텍스트 위치 보정 500, 1500 -  주프로그램에서 클릭시 path 를 우선하기 위해 text를 먼저 출력한다.
			masking += "<text class='"+subItem+"' x='"+(cfg.maskCoord[item][subItem][0]+200)+"' y='"+(cfg.maskCoord[item][subItem][1]+800)+"' text-anchor='right' style='fill:gray; font-size:20cm;' >"+subItem+"</text>";
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
	// 실제 Vector 값으로 변환한 값을 maskCoord에 저장
	cfg.maskCoord[data.mask][data.id] = [coordSx,coordSy,coordEx,coordEy];
}

////////////////////
// 데이터베이스 관련
////////////////////
var mysql = require('mysql');
var db_config = {
	host: cfg.mysql.host,
	user: cfg.mysql.user,
	password: cfg.mysql.pass,
	database: cfg.mysql.name
};

// https://stackoverflow.com/questions/20210522/nodejs-mysql-error-connection-lost-the-server-closed-the-connection
// Error: Connection lost: The server closed the connection. - 오류 발생 제거: 
// 고질적인 오류임 디비 서버 연결이 끈어지는 현상
var con;
function handleDisconnect() {
	con = mysql.createConnection(db_config);// Recreate the con, since the old one cannot be reused.

	con.connect(function(err) {	// The server is either down
		if(err) { 				// or restarting (takes a while sometimes).
			console.log('ECOS(2021-03-31 05:02:41) Error when connecting to db:', err);
			setTimeout(handleDisconnect, 2000); // We introduce a delay before attempting to reconnect, to avoid a hot loop, and to allow our node script to process asynchronous requests in the meantime.
		}
	});

	con.on('error', function(err) {
		console.log('ECOS(2021-03-31 05:07:40) db error', err);
		if(err.code === 'PROTOCOL_CONNECTION_LOST') {	// con to the MySQL server is usually lost due to either server restart, or a connnection idle timeout (the wait_timeout server variable configures this)
			handleDisconnect();
		} else {
			console.log('ECOS(2021-03-31 05:16:02)강제로 2초후 재접속 시도');
			setTimeout(handleDisconnect, 2000); // 2초후 재접속 시도
			// 원본 throw err;
		}
	});
}
handleDisconnect();

	
// 데이터베이스 마스킹 정보 등록
function updateMask() {
	var allowZone = "";
	// 150:2400_190:3000,1500:2800_1700:2900
	// 1_253_155-229:438_5320:4611,1_300_180-4152:2525_10913:9286
	for (var key in cfg.maskCoord.allowGroup) {
		allowZone += key+"|"+cfg.maskCoord.allowGroup[key][0]+":"+cfg.maskCoord.allowGroup[key][1]+"_"+cfg.maskCoord.allowGroup[key][2]+":"+cfg.maskCoord.allowGroup[key][3]+",";
	}

	var ignoreZone = "";
	// 150:2400_190:3000,1500:2800_1700:2900
	for (var key in cfg.maskCoord.denyGroup) {
		ignoreZone += key+"|"+cfg.maskCoord.denyGroup[key][0]+":"+cfg.maskCoord.denyGroup[key][1]+"_"+cfg.maskCoord.denyGroup[key][2]+":"+cfg.maskCoord.denyGroup[key][3]+",";
	}

	var sql = "UPDATE "+cfg.table.rls_r+" SET w_sensor_allowZone='"+allowZone.replace(/,\s*$/, '')+"', w_sensor_ignoreZone='"+ignoreZone.replace(/,\s*$/, '')+"' WHERE wr_id="+cfg.sensor.tableID;
	
	// console.log(sql);
	con.connect(function(err) {
		// if (err) throw err;
		con.query(sql, function (err, result) {
			if (err) throw err;
			// callback(null, result);
			// console.log(result);
		});
	});
}

// 소켓을 통해 자료를 realtime_RLS.html로 전송한다.
function obj_location(objInfo) {
	io.sockets.emit('message_to_client', { objInfo: objInfo });
}

app.listen(portOut); // Display server
console.log('\nService server running at http://localhost:'+portOut+'/');

//////////////////////////////////////////////////////////
// 포트 8000으로 부터 받은 정보를 파싱한후 포트 9000으로 전달한다.
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
		// 예: '4294967279654,1085,788,116|4294967279654,493,732,452|4294967279654,228,836,104| ~ 1,2,3,4|1,2,3,4|
		var objInfo = data.toString();
		// console.log(objInfo);
		// obj_location(objInfo); // 자료 전송
		
		var objInfoAll = objInfo.split('|');
		for(i = 0; i < objInfoAll.length; i++) {
			var cood_xyr = objInfoAll[i].split(',');
			// 이유는 모르겠으나 4개의 요소를 전송해야 하는데 첫번째 요소가 제거되는 상황을 피하기 위함
			if (cood_xyr.length == 4) {
				obj_location(objInfoAll[i]); // 자료 전송
				// console.log("cood_xyr",objInfoAll[i]);
			}
		}
		
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');

///////////////////////////////////////////////////////////////////////////////
// 클라이언트(portOut)의 명령 정보를 파싱한후 작업하고 결과 전달하거나 내용을 저장한다.
///////////////////////////////////////////////////////////////////////////////
io.sockets.on('connection', function (socket) { // 내부 Client로 부터 받은 작업 실행
	
	socket.on('setMasking', function(data) { // SVG View Point 관련
		console.log(' setMasking ' + data.id + ' ' + data.mask + ' ' + data.value); 
		setMasking(data);
		io.sockets.emit('readMasking', readMasking());; // 클라이언트동기화 
		saveConfigJson();
		updateMask();
	}); // svgView
	
	socket.on('readMasking', function(data) { // 환경값을 클라이언트로 전송()
		// console.log(' readMasking ' + data); 
		io.sockets.emit('readMasking', readMasking());; // 클라이언트동기화 
	});
	
	socket.on('delMasking', function(data) { // SVG View Point 관련
		console.log(' delMasking ' + data.id + ' ' + data.mask); 
		delete (cfg.masking[data.mask][data.id]);
		delete (cfg.maskCoord[data.mask][data.id]);
		io.sockets.emit('readMasking', readMasking());; // 클라이언트동기화 
		saveConfigJson();
		updateMask();
	}); // svgView
});	
