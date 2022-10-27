////////////////////////
// its가 호스트(Host:192.168.1.3 : 8000)에 보내는 정보
// 관련 내용의 파싱 값을 포트 9000으로 전송
// 참고 : https://openclassrooms.com/courses/ultra-fast-applications-using-node-js/socket-io-let-s-go-to-real-time
////////////////////////

var app = require('http').createServer(handler);
var io = require('socket.io')(app); // var io = require('socket.io')(app); // var io = require('socket.io').listen(app);
var fs = require('fs');
var path = require('path');
var net = require('net');
var os = require('os');

///////////////////
// config.json 파일을 읽어 환경설정 한다.
var cfg = JSON.parse(fs.readFileSync('/home/pi/MONITOR/config.json', 'utf8')); // 환경 파일 읽기
var ims = JSON.parse(fs.readFileSync('/home/pi/MONITOR/cfgIms.json', 'utf8')); // 환경 파일 읽기
var icc = JSON.parse(fs.readFileSync('/home/pi/MONITOR/camera.json', 'utf8')); // 환경 파일 읽기
// var lan = JSON.parse(fs.readFileSync('./language.json', 'utf8')); // 환경 파일 읽기

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

var deleteDue = 60; // 설정보다 과거 자료 삭제

///////////////////
// 자신의 아이피
// https://gist.github.com/sviatco/9054346
var myIpAddr, ifaces = os.networkInterfaces()
for (var dev in ifaces) {
	var iface = ifaces[dev].filter(function(details) {
		return details.family === 'IPv4' && details.internal === false;
	});
	if(iface.length > 0) myIpAddr = iface[0].address;
}
// console.log(myIpAddr);


// https://stackoverflow.com/questions/20210522/nodejs-mysql-error-connection-lost-the-server-closed-the-connection
// Error: Connection lost: The server closed the connection. - 오류 발생 제거: 
var con;
function handleDisconnect() {
	con = mysql.createConnection(db_config);// Recreate the con, since
											// the old one cannot be reused.
	con.connect(function(err) {	// The server is either down
		if(err) { 				// or restarting (takes a while sometimes).
			logger('error when connecting to db:', err);
			setTimeout(handleDisconnect, 2000); // We introduce a delay before attempting to reconnect,
		}										// to avoid a hot loop, and to allow our node script to
	});											// process asynchronous requests in the meantime.
												// If you're also serving http, display a 503 error.
	con.on('error', function(err) {
		logger('db error', err);
		if(err.code === 'PROTOCOL_CONNECTION_LOST') {	// con to the MySQL server is usually
		  handleDisconnect();							// lost due to either server restart, or a
		} else {										// connnection idle timeout (the wait_timeout
			// throw err;									// server variable configures this)
			logger('Function createConnection error:',err);
			setTimeout(handleDisconnect, 2000); // 2021-05-09 04:02:23 실험적 추가
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
			if (err) logger('Function insertEvent error:',err); //  throw err;
			// callback(null, result);
			// console.log(result);
		});
	});
}

function getEvtLog(sensorID, callback) { // 이벤트 검색 - MINUTE HOUR DAY
	con.connect(function(err) {
		// if (err) throw err;
		// var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_sensorId = '"+sensorID+"' AND w_stamp >= NOW() - INTERVAL 1 HOUR"; // MINUTE HOUR DAY
		var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_sensorId = '"+sensorID+"' ORDER BY w_id ASC LIMIT 100"; // LAST 100
		con.query(sql, function (err, result, fields) {
			if (err) logger('Function getEvtLog error:',err); //  throw err;
			callback(null, result);
			// console.log(result);
		});
	});
}

// 마지막 1000개의 이밴트중 최근 24시간 이밴트를 추출 함 - 이유 퍼포먼스 이슈
function getEvtLastLog(callback) { // 최근 이벤트 검색후 지역상황 파악
	con.connect(function(err) {
		// 속도개선을 위해 SUB-QUERY 사용함 - https://stackoverflow.com/questions/12125904/select-last-n-rows-from-mysql
		// 최근 Limit 갯수만큼 읽은후 정열한다(차이가 많이남).
		var sql = "SELECT * FROM "+cfg.table.imsData+" WHERE w_id IN ( SELECT MAX(w_id) FROM ( SELECT * FROM "+cfg.table.imsData+" ORDER BY w_id DESC LIMIT 1000 ) sub WHERE w_stamp >= NOW() - INTERVAL 1 DAY GROUP BY w_sensorId )";
		con.query(sql, function (err, result, fields) {
			// if (err) throw err;
			if (err) logger('Function getEvtLastLog error:',err); //  throw err;
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

// 특정일 이후 로그 자료 삭제
function deleteOlderDays(days=deleteDue) {
	con.connect(function(err) {
		var sql = "DELETE FROM "+cfg.table.imsData+" WHERE `w_stamp` < NOW() -INTERVAL "+days+" DAY ";
		con.query(sql, function (err, result) {
			// if (err) throw err;
			if (err) logger('No more Logs that older then '+days+'days'); //  throw err;
			if (result) logger('Remove Logs that older then '+days+'days'); //  throw err;
			// console.log(sql,result);
		});
	});
}
// 최초 실행시 한번 실행한다.
deleteOlderDays();


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
		if (err) logger('Function saveConfigJson error:',err); //  throw err;
		// console.log('The file has been saved!');
	});
}

///////////////////
// 로그 등록 예: logger(clientIP + ' findClientIP ' + data);
var loggerFile = cfg.path.log+cfg.path.home+cfg.path.home+'.log';
function logger(log) {
	var timezoneOffset = new Date().getTimezoneOffset() * 60000; 
	var timezoneDate = new Date(Date.now() - timezoneOffset); // 서울시간 대
	var dt = timezoneDate.toISOString().replace(/T/, '_').replace(/Z/, ''); // .replace(/\..+/, '')
	var eventIs = dt+' > '+log+'\n';
	if(fs.statSync(loggerFile).size > 9999999) {
		fs.rename(loggerFile, loggerFile+'.'+dt, function(err) {
			if ( err ) console.log('ERROR: ' + err);
		});
		fs.closeSync(fs.openSync(loggerFile, 'w'));
	}; // 파일 사이즈
	fs.appendFile(loggerFile, eventIs, function (err) {
		// if (err) throw err;
		if(err) console.log('Function logger Error');
	});	
}


///////////////////
// 카메라 Onvif Control
// function ptzOnvifCtl(data) {
	// console.log(data);
	// // data.camPort: ims.camera[id].camPort,
	// // data.cmd:'',
	// // data.pan: 0,
	// // data.tilt: 0,
	// // data.zoom: 0,
	// // data.preset: 0,
	// // data.option: ''
	// // camPort 센서 서브프로세스(procOnvif.js) 접속
	// var socketCam = net.connect({port : data.camPort});
	// socketCam.on('connect', function(){
		// // console.log("cmd:"+data.cmd+",pan:"+data.pan+",tilt:"+data.tilt+",zoom:"+data.zoom+",preset:"+data.preset+",option:"+data.option);
		// socketCam.write("cmd:"+data.cmd+",pan:"+data.pan+",tilt:"+data.tilt+",zoom:"+data.zoom+",preset:"+data.preset+",option:"+data.option);
		// socketCam.destroy();
	// });
// };
var ipCam = require('onvif').Cam;
var STOP_DELAY_MS = 50; // 이동(줌)의 연속성 인터벌
function ptzOnvifCtl(data) {
	// console.log(data);
	if(icc[data.model].isPTZ) {
		new ipCam({
			hostname: data.addr,
			username: data.user,
			password: data.pass,
			port: data.port
		}, function(err) {
			if (err) {
				// console.log('Connection Failed for ' + data.addr + ' Port: ' + data.port + ' Username: ' + data.user + ' Password: ' + data.pass);
				// console.log(err);
				return
			}
			
			var cam_obj = this;
			var stop_timer;
			var ignore_action = false;
			var preset_names = [];
			var preset_tokens = [];
			
			cam_obj.getPresets({}, // use 'default' profileToken
				// Completion callback function
				// This callback is executed once we have a list of presets
				function (err, stream, xml) {
					if (err) {
						// console.log("GetPreset Error "+err);
						return;
					} else {
						// loop over the presets and populate the arrays
						// Do this for the first 9 presets
						// console.log("GetPreset Reply");
						// console.log('\n');
						var count = 1;
						for(var item in stream) {
							var name = item;          //key
							var token = stream[item]; //value
							// It is possible to have a preset with a blank name so generate a name
							if (name.length == 0) name='no name ('+token+')';
							preset_names.push(name);
							preset_tokens.push(token);
							// Show first 9 preset names to user
							if (count < 9) {
								// console.log('\tKey: '+count+ ' name: "' + name + '" token:' + token);
								count++;
							}
						}
					}
				}
			);
			function ptzMoveCont(x, y, zoom) {
				// Step 1 - Turn off the keyboard processing (so keypresses do not buffer up)
				// Step 2 - Clear any existing 'stop' timeouts. We will re-schedule a new 'stop' command in this function 
				// Step 3 - Send the Pan/Tilt/Zoom 'move' command.
				// Step 4 - In the callback from the PTZ 'move' command we schedule the ONVIF Stop command to be executed after a short delay and re-enable the keyboard

				// Pause keyboard processing
				ignore_action = true;

				// Clear any pending 'stop' commands
				if (stop_timer) clearTimeout(stop_timer);

				// Move the camera
				// console.log('sending ptzMoveCont ' + x + " " + y + " " + zoom);
				cam_obj.continuousMove({x : x, y : y, zoom : zoom }, function (err, stream, xml) {
					if (err) {
						console.log(err);
					} else {
						// console.log('ptzMoveCont sent');
						// schedule a Stop command to run in the future 
						stop_timer = setTimeout(stop,STOP_DELAY_MS);
					}
					// Resume keyboard processing
					ignore_action = false;
				});
			}
			function gotoHomePosition() {
				cam_obj.gotoHomePosition({'ProfileToken': 'homeIMS', 'Speed': 0.5}, function (err, data, xml){
					if (err) {
						console.log(err);
					}
				});
			}
			function setHomePosition() {
				cam_obj.setHomePosition({'ProfileToken': 'homeIMS'}, function (err, data, xml){
					if (err) {
						console.log(err);
					}
				});
			}
			function gotoPresetNo(number) {
				if (number > preset_names.length) {
					console.log ("No preset " + number);
					return;
				}
				// console.log('sending preset: ' + preset_names[number-1]);
				cam_obj.gotoPreset({ preset : preset_tokens[number-1] }, function (err, stream, xml) {
					if (err) {
						console.log(err);
					}
				});
			}
			function gotoPresetName(presetName) {
				var idxPreset = preset_names.indexOf(presetName);
				cam_obj.gotoPreset({'preset': preset_tokens[idxPreset]}, function (err, data, xml){
					if (err) {
						console.log(err);
					}
				});
			}
			function setPresetName(presetName) {
				cam_obj.setPreset({'presetName': presetName}, function (err, data, xml){
					if (err) {
						console.log(err);
					}
				});
			}
			function removePresetName(presetName) { // ProfileToken
				var idxPreset = preset_names.indexOf(presetName);
				console.log(presetName, idxPreset, preset_tokens[idxPreset]);
				if(idxPreset >= 0) {
					cam_obj.removePreset({'PresetToken:': preset_tokens[idxPreset]}, function (err, data, xml){
						if (err) {
							console.log(err);
						}
					});
				}
			}
			function absoluteMove(x, y, zoom) {
				cam_obj.absoluteMove({x:x, y:y, zoom:zoom});
			}
			function relativeMove(x, y, zoom) {
				cam_obj.relativeMove({x:x/4, y:y/4, zoom:zoom/2}); // 2 나 4 로 나누는 것은 이동폭을 줄이기 위함
			}
			function getStatus() {
				cam_obj.getStatus(function(err, status) { // RETURN - position:, moveStatus:, error:, utcTime:
					if (err) {
						console.log("CAM:"+ipAddr+" getStatus Error "+err);			
					} else {
						// console.log(status);
					}
				});
			}
			function stop() {
				// send a stop command, stopping Pan/Tilt and stopping zoom
				// console.log('\tsending stop');
				cam_obj.stop({panTilt: true, zoom: true}, function (err, stream, xml){
					if (err) {
						console.log(err);
					} else {
						// console.log('\tstop sent');
					}
				});
			}
			
			if(data.cmd == 'ptzMoveCont') {
				ptzMoveCont(data.pan, data.tilt, data.zoom);
			} else if(data.cmd == 'absoluteMove') {
				// console.log("abs", data.pan, data.tilt, data.zoom);
				absoluteMove(data.pan, data.tilt, data.zoom);
			} else if(data.cmd == 'relativeMove') {
				// console.log("rel", data.pan, data.tilt, data.zoom);
				relativeMove(data.pan, data.tilt, data.zoom);
			} else if(data.cmd == 'gotoPresetNo'){
				gotoPresetNo(data.preset);
			} else if(data.cmd == 'gotoHomePosition'){
				gotoHomePosition();
			} else if(data.cmd == 'setHomePosition'){
				setHomePosition();
			} else if(data.cmd == 'gotoPresetName'){
				gotoPresetName(data.option);
			} else if(data.cmd == 'setPresetName'){
				setPresetName(data.option);
			}
			
		});
	} else {
		console.log('Model ' + data.model + ' is not PTZ function.');
	}
}

function ptzOnvifCtlGroup(client, senId, actionPTZ=1) {
	// console.log(client, senId);
	// 연관된 [카메라 프리셋] 정보가 있으면 카메라에 프리섹값 전송
	var presetIs = ims.sensor[senId].camera; // 관련 카메라 목록
	presetIs.forEach(function(camID) {
		// 센서로 부터의 이벤트는 선언된 카메라 위치로 무조건 이동 한다.
		// 멥에서 사용자 클릭에 의한 이벤트는 허용체크박스 값에 의존 한다.
		if(actionPTZ) {
			var ptzOn = 1;
		} else {
			// var ptzOn = ims.sensor[senId].pSetOn[camID];
			var ptzOn = ims.zone[ims.sensor[senId].zoneID].pSetOn[camID];
		}
		if(ptzOn && ims.sensor[senId].preset[camID]) { // 위치 값이 있으면
			var ptzoom = ims.sensor[senId].preset[camID].split(",");
			if(ptzoom[0] && ptzoom[1] && ptzoom[2]) { // PTZ 값이 모두 있으면
				var data = {
					addr: ims.camera[camID].addr,
					user: ims.camera[camID].user,
					pass: ims.camera[camID].pass,
					port: ims.camera[camID].port,
					model: ims.camera[camID].model,
					camPort: ims.camera[camID].camPort,
					cmd:'absoluteMove',
					pan: ptzoom[0],
					tilt: ptzoom[1],
					zoom: ptzoom[2],
					preset: 0,
					option: ''
				}
				ptzOnvifCtl(data);
				logger('from:'+client+' to(port):'+data.camPort+' cmd:'+data.cmd);
			}
		}
	});
};

function ptzOnvifCtlGroupBox(boxId) {
	// console.log(boxId);
	// 연관된 [카메라 프리셋] 정보가 있으면 카메라에 프리섹값 전송
	var presetIs = ims.box[boxId].camera; // 관련 카메라 목록
	presetIs.forEach(function(camID) {
		if(ims.box[boxId].preset[camID]) { // 위치 값이 있으면
			var ptzoom = ims.box[boxId].preset[camID].split(",");
			if(ptzoom[0] && ptzoom[1] && ptzoom[2]) { // PTZ 값이 모두 있으면
				var data = {
					addr: ims.camera[camID].addr,
					user: ims.camera[camID].user,
					pass: ims.camera[camID].pass,
					port: ims.camera[camID].port,
					model: ims.camera[camID].model,
					camPort: ims.camera[camID].camPort,
					cmd:'absoluteMove',
					pan: ptzoom[0],
					tilt: ptzoom[1],
					zoom: ptzoom[2],
					preset: 0,
					option: ''
				}
				ptzOnvifCtl(data);
				logger('from: IMS to(port):'+data.camPort+' cmd:'+data.cmd);
			}
		}
	});
};

////////////////////////
// IP Relay 출력
// TCP/IP Socket Write
// 192.168.0.202:8040
// id=ID, status=STATUS, msg=MSG

// ipRelayWrite("192.168.0.202", 8040, 18, 0, "message");

function ipRelayWrite(addr, port, id, state, msg) {
	// console.log('Start <<< Func: ipRelayWrite');
	var client = new net.Socket();
	var relayData = 'id='+id+', status='+state+', msg='+msg;
	client.connect(port, addr, function(err){
		if(err) {
			logger('Connect erro ipRelayWrite: '+relayData);
			return 0;
		}
	});
	
	// events.js:160
	// throw er; // Unhandled 'error' event
	// Error: connect ECONNREFUSED 192.168.0.202:8040
	// connect 루틴에 write, destroy를 분리해서 사용해야 함 - 포함시 랜덤하게 오류(events.js:160) 발생
	
	client.write(relayData);
	client.destroy();
	// console.log('End >>> Func: ipRelayWrite');
	logger('Sent ipRelay: '+addr+' '+port+' '+relayData);
}

// function ipRelayWrite(addr, port, id, state, msg) {
	// console.log('Start <<< Func: ipRelayWrite');
	// var client = new net.Socket();
	// var relayData = 'id='+id+', status='+state+', msg='+msg;
	// client.connect(port, addr, function(){
		// console.log('connected to ', addr, port, relayData);
		// client.write(relayData);
		// client.destroy();
	// });
	// console.log('End >>> Func: ipRelayWrite');
// }


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

// ITS 측에 전원이나 네트워크 오류로 인한 상황에 따른 대음
function customIpPort_diviNVR(boxId) { // 쿼리명령 수행
	ims.box[boxId].customIpPort.forEach(function(value){
		// console.log('Func: customIpPort_diviNVR');
		if (!value.opt1.length) {
			return 0;
		}
		
		// opt2가 비어있는경우 99로 치환 한다.
		if (!value.opt2.length) {
			value.opt2 = "99";			
		}
		
		var	data = '\x02' + value.opt1.toString(16) + '\x3b' + value.opt2.toString(16) + '\x03';
		
		try {
			var client = require('net').connect({port:value.port, host:value.host}, function() {
				this.setEncoding('utf8'); 
				this.setTimeout(5000); // timeout : 1분 = 60000, 10분 = 600000
			});

			client.write(data);
			client.end();
			logger('IMS send preset to NVR '+value.host+' '+value.port+' '+value.opt1+' '+value.opt2);
		} catch (e) {
			console.log('Error - Func: customIpPort_diviNVR');
			return 0;
		}

		// client.on('error', function(err) { console.log('client Socket Error: '+ JSON.stringify(err)); }); 
		// client.on('timeout', function() { console.log('client Socket timeout: '); }); 
		// client.on('drain', function() { console.log('client Socket drain: '); }); 
		// client.on('lookup', function() { console.log('client Socket lookup: '); }); 
	});	
}

//////////////////////////////////////
// 아이피와 포트를 통해 온라인 확인기능
// ITS(센서) 접속(네트웨크) 오류 확인 기능

// On Line 테스트
function onlineTest() {
	setTimeout(function () {
		// 관련 아이피 목록 스켄
		if(!ims.online.its) return;
		Object.keys(ims.online.its).forEach(function(addr) {
			
			// https://stackoverflow.com/questions/10723393/nodejs-pinging-ports
			// console.log(addr, ims.online.its[addr].port);
			var port = ims.online.its[addr].port;
			var sock = new net.Socket();
			sock.setTimeout(1000); // 1000 = 1 sec
			sock.on('connect', function() {
				// console.log(addr+':'+port+' is up.');
				sock.destroy();
			}).on('error', function(e) {
				// console.log(addr+':'+port+' is down: ' + e.message);
				logger(addr+':'+port+' is down: ' + e.message);				

			}).on('timeout', function(e) {
				io.sockets.emit('sendOfflineITS', { addr: addr });
				console.log(addr+':'+port+' is down: timeout');
				logger(addr+':'+port+' is down: timeout');				
				
				boxKey = ims.online.its[addr].boxID;
				// console.log(boxKey);
				if(boxKey) { //  "7":"ERR_CONNECT"
					if(cfg.filterIP.deny.indexOf(boxKey) === -1) { // 예외된 박스 정보가 아니면
						if(cfg.runProgram.procOnvif) { // 온비프 프로세서가 구동중이면 
							ptzOnvifCtlGroupBox(boxKey); // 박스(함체) 선언이 있으면 관련 프리셋 그룹 전송
						}
						io.sockets.emit('sendEventBox', { id: boxKey, name: ims.box[boxKey].subj, beep: '1', status: '7', shot: '' });
						// 이벤트를 데이터베이스에 저장
						insertEvent(ims.box[boxKey].group, ims.box[boxKey].cate, boxKey, ims.box[boxKey].subj, 'IMS', '', '7', 'Disconnected(timeout)'); 
						
						// IP Relay 실행
						if(ims.box[boxKey].relayAddr && ims.box[boxKey].relayPort && ims.box[boxKey].relayNumber) {
							ipRelayWrite(ims.box[boxKey].relayAddr, ims.box[boxKey].relayPort, ims.box[boxKey].relayNumber, 1, "message");
						}
						
						// 로그파일 등록
						saveEvent(boxKey+','+ims.box[boxKey].subj+','+'1'+','+'7'+','+'Disconnected(timeout)'+','+''); 
						
						// wr_8, wr_9 사용자 ipPort
						customIpPort_diviNVR(boxKey)
						
					} else { // 관리자에 의해 거부된 박스 이벤트이면 "5":"WARNING"
						io.sockets.emit('sendEventDeny', { id: boxKey, mapId: ims.box[boxKey].mapID, subj: ims.box[boxKey].subj, status: 5 });
					}
					
				} else { // 박스(함체) 선언이 없으면 관련 아이피에 연관된 모든 센서 정보를 표시 한다.
					senID = ims.online.its[addr].senID;
					senID.forEach(function(key) {
						// console.log(key);
						if(cfg.filterIP.deny.indexOf(key) === -1) { // 예외된 센서 정보가 아니면
							io.sockets.emit('sendEventLog', { id: key, name: ims.sensor[key].subj, beep: '1', status: '7', shot: '' });
							// 이벤트를 데이터베이스에 저장
							insertEvent(ims.sensor[key].group, ims.sensor[key].cate, key, ims.sensor[key].subj, 'IMS', '', '7', 'Disconnected(timeout)'); 
							
							// IP Relay 실행
							if(ims.sensor[key].relayAddr && ims.sensor[key].relayPort && ims.sensor[key].relayNumber) {
								ipRelayWrite(ims.sensor[key].relayAddr, ims.sensor[key].relayPort, ims.sensor[key].relayNumber, 1, "message");
							}
							
							// 로그파일 등록
							saveEvent(key+','+ims.sensor[key].subj+','+'1'+','+'7'+','+'Disconnected(timeout)'+','+''); 
						} else { // 관리자에 의해 거부된 센서 이벤트이면 
							io.sockets.emit('sendEventDeny', { id: key, mapId: ims.sensor[key].mapID, subj: ims.sensor[key].subj, status: 5 });
						}
					});
				}
				
			}).connect(port, addr); // 아이피:포트 접속 시도

		});		
		onlineTest();
    }, 5000);
}
// 아래 커멘트 제거시 실행됨
onlineTest(); // 실행
 

//////////////////////////////////////
// 예약된 접속 시간 초과를 비교한 온라인 확인기능
// ITS(센서) 접속(네트웨크) 오류 확인 기능

var zones = {}
// 이벤트 발생한 최종 시간과 이전 발생시간 간의 차이값(미리초) 등록
function aliveVerify(senId, beep) {
	try {
		// 이벤트 발생은 비규칙적이어서 발생시간의 차이를 등록하지 않는다.
		// 만일 등록하면 알람 이벤트 이후 시간차 계산시 diff 값의 변화로 오류를 발생시킬수 있다.
		// 하트비트인 경우만 시간차이 등록
		if(!parseInt(beep)) 
			zones[senId]['diff'] = Date.now() - zones[senId]['time'];
		zones[senId]['time'] = Date.now();
	} catch (e) {
		zones[senId] = {};
		zones[senId]['diff'] = [];
		zones[senId]['time'] = [];
		zones[senId]['diff'] = 0;
		zones[senId]['time'] = Date.now();
	}
}

// 시간초과된 센서 필터링후 알람발생
// ITS 간 통신오류 발생시 - Heartbeat
function connectionTest() {
	setTimeout(function () {
		Object.keys(zones).forEach(function(key) {
			if(zones[key]['diff']) {
				// 최종 이벤트 접속시간이 이전 시간과 비교
				var diff = Date.now() - zones[key]['time'];
				// console.log(diff,zones[key]['diff'],zones[key]['diff'] * 2.5)
				if(diff > zones[key]['diff'] * 2) { // 시간차가 2배가 넘어 오류발생 시킴 "7":"ERR_CONNECT"
					boxKey = ims.sensor[key].boxID;
					if(boxKey) {
						if(cfg.filterIP.deny.indexOf(boxKey) === -1) { // 예외된 박스 정보가 아니면
							if(cfg.runProgram.procOnvif) { // 온비프 프로세서가 구동중이면 
								ptzOnvifCtlGroupBox(boxKey); // 박스(함체) 선언이 있으면 관련 프리셋 그룹 전송
							}
							io.sockets.emit('sendEventBox', { id: boxKey, name: ims.box[boxKey].subj, beep: '1', status: '7', shot: '' });
							// 이벤트를 데이터베이스에 저장
							insertEvent(ims.box[boxKey].group, ims.box[boxKey].cate, boxKey, ims.box[boxKey].subj, 'IMS', '', '7', 'Disconnected(timeout)'); 
							
							// IP Relay 실행
							if(ims.box[boxKey].relayAddr && ims.box[boxKey].relayPort && ims.box[boxKey].relayNumber) {
								ipRelayWrite(ims.box[boxKey].relayAddr, ims.box[boxKey].relayPort, ims.box[boxKey].relayNumber, 1, "message");
							}
							
							// 로그파일 등록
							saveEvent(boxKey+','+ims.box[boxKey].subj+','+'1'+','+'7'+','+'Disconnected(timeout)'+','+''); 
							
							// wr_8, wr_9 사용자 ipPort
							customIpPort_diviNVR(boxKey)
							
						} else { // 관리자에 의해 거부된 박스 이벤트이면 
							io.sockets.emit('sendEventDeny', { id: boxKey, mapId: ims.box[boxKey].mapID, subj: ims.box[boxKey].subj, status: 5 });
						}
						
					} else { // 박스(함체) 선언이 없으면 관련 아이피에 연관된 모든 센서 정보를 표시 한다. "7":"ERR_CONNECT"
						if(cfg.filterIP.deny.indexOf(key) === -1) { // 예외된 센서 정보가 아니면 
							io.sockets.emit('sendEventLog', { id: key, name: ims.sensor[key].subj, beep: '1', status: '7', shot: '' });
							// 이벤트를 데이터베이스에 저장
							insertEvent(ims.sensor[key].group, ims.sensor[key].cate, key, ims.sensor[key].subj, 'IMS', '', '7', 'Disconnected(timeout)'); 
							
							// IP Relay 실행
							if(ims.sensor[key].relayAddr && ims.sensor[key].relayPort && ims.sensor[key].relayNumber) {
								ipRelayWrite(ims.sensor[key].relayAddr, ims.sensor[key].relayPort, ims.sensor[key].relayNumber, 1, "message");
							}
							
							// 로그파일 등록
							saveEvent(key+','+ims.sensor[key].subj+','+'1'+','+'7'+','+'Disconnected(timeout)'+','+''); 
						} else { // 관리자에 의해 거부된 센서 이벤트이면 
							io.sockets.emit('sendEventDeny', { id: key, mapId: ims.sensor[key].mapID, subj: ims.sensor[key].subj, status: 5 });
						}
					}
					logger('from: IMS : Disconnected(timeout error) '+key);
				}
				// console.log(key);
				// console.log(zones[key]['diff']);
				// console.log(zones[key]['time']);
			}
		});		
		connectionTest();
    }, 2000);
}
// 아래 커멘트 제거시 실행됨
// connectionTest();


///////////////////
// 시스템 명령
const { exec } = require("child_process");
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
			if (stdout) {
				response = `{"stdout": ${stdout}}`;
				// console.log(response);
				callback(response);
			}
		});

	} catch (e) {
		// console.log('Error - exec ' + cmd);
		logger('executeCmd '+cmd);
		return 0;
	}
}


///////////////////
// Start Program 
///////////////////

var portIn = cfg.interface.portIn;
var portOut = cfg.interface.portOut;
var portHealth = cfg.interface.health;

//////////////////////////////////////////////////////////
// ITS 진단 내용 클라이언트로 전송
// 외부(ITS)에서 ~/common/watchdog.py를 통해 정보를 받아(cfg.interface.health)
//////////////////////////////////////////////////////////
require('net').createServer(function (client) {
	
	// /* 지우지 말것, 실시간 접속되는 모든 클라이언트 정보 */
	// console.log('Client connection: ');
	// console.log('\tHealth check from = %s:%s', client.remoteAddress, client.remotePort);
	// // console.log('\tlocal = %s:%s', client.localAddress, client.localPort);

	client.setTimeout(500);
	client.setEncoding('utf8');

	client.on('data', function (data) { // 이미 Json 형태로 외부 portHealth 으로 부터 받은 정보(data)
		try {
			sendEventHealth = JSON.parse(data);
			sendEventHealth['srvDTime'] = Date.now();
			io.sockets.emit('sendEventHealth', sendEventHealth);
			// console.log(sendEventHealth);
		} catch(e) {
			return console.error(e, "Error : JSON.parse");
			// console.log(e, "Error : JSON.parse"); // error in the above string (in this case, yes)!
		}
	});

	// /* 지우지 말것, 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음 */
	// client.on('end', function() {
	// 	console.log('Client disconnected');
	// });
	// client.on('error', function(err) {
	// 	console.log('Socket Error: ', JSON.stringify(err));
	// });
	// client.on('timeout', function() {
	// 	console.log('Socket Timed out');
	// });

}).listen(portHealth); // Receive server
console.log('Listen Health at http://localhost:'+portHealth+'/');


///////////////////
// ITS -> IMS(38087) -> [Do it] -> IMS(38088) -> PC(Browser)
// 외부의 ITS로 부터 IMS포트 38087(portIn)로 접수(listen(portIn))
// 분석된 정보를 포트 38088(portOut)을 통해 사용자브라우저에 전달(sendEventLog)한다.
// https://namik.tistory.com/114
require('net').createServer(function (client) {

	// /* 실시간 접속되는 모든 클라이언트 정보 */
	// console.log('Client connection: ');
	// console.log('\tSensor event from = %s:%s', client.remoteAddress, client.remotePort);
	// // console.log('\tlocal = %s:%s', client.localAddress, client.localPort);
	
	client.setTimeout(500);
	client.setEncoding('utf8');
	
	client.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.

		var senId = '';
		var senName = '';
		var beep = '';
		var status = '';
		var msg = '';
		var shot = '';
		var level = [];
		var userName = 'ITS';

		try {
			objField = JSON.parse(data);
			// console.log("its JSON");
			senId = objField.id;
			senName = objField.name;
			beep = objField.beep;
			status = objField.status; 
			msg = objField.msg; 
			shot = objField.shot; 
			level = objField.level; 
			// pickTime = objField.pickTime; 
			// holdTime = objField.holdTime; 
		} catch (e) {
			// console.log("not JSON");
			var alarmInfo = data.toString();
			var objInfo = alarmInfo.split(",");  
			for (var i in objInfo) {
				var objField = objInfo[i].split("=");
				if (objField[0].trim() == 'id') senId = objField[1];
				if (objField[0].trim() == 'name') senName = objField[1];
				if (objField[0].trim() == 'beep') beep = objField[1];
				if (objField[0].trim() == 'status') status = objField[1]; 
				if (objField[0].trim() == 'msg') msg = objField[1]; 
				if (objField[0].trim() == 'shot') shot = objField[1]; 
			}
		}
		// console.log(senId, senName, beep, status, msg, shot, level);
		
		// var alarmInfo = data.toString();
		// var objInfo = alarmInfo.split(",");  
		// for (var i in objInfo) {
		// 	var objField = objInfo[i].split("=");
		// 	if (objField[0].trim() == 'id') senId = objField[1];
		// 	if (objField[0].trim() == 'name') senName = objField[1];
		// 	if (objField[0].trim() == 'beep') beep = objField[1];
		// 	if (objField[0].trim() == 'status') status = objField[1]; 
		// 	if (objField[0].trim() == 'msg') msg = objField[1]; 
		// 	if (objField[0].trim() == 'shot') shot = objField[1]; 
		// }
		// console.log(data);

		if(ims.sensor[senId] !== undefined) { // 등록이 된 센서 이벤트만 필터링 한다.
			if(cfg.filterIP.deny.indexOf(senId) === -1) { //  거부(블럭)되지 않은 이벤트 정보면 추가함
				senName = ims.sensor[senId].subj;
				// 소켓을 통해 자료를 클라이언트(its_M_map_tmplet.html)로 전송한다.
				io.sockets.emit('sendEventLog', { id: senId, name: senName, beep: beep, status: status, shot: shot, level: level });

				/////////////////////////////////
				// 알람 이벤트 발생시
				if (parseInt(beep)) { // 출력 데이터 예: 17 300100 'g300t100_192_168_0_202_0035' 'FENCE04' 'ITS' '' '2' 'Idle_Event'
					// 이벤트를 데이터베이스에 저장
					insertEvent(ims.sensor[senId].group, ims.sensor[senId].cate, senId, senName, userName, shot, status, msg); 
					
					// 연관된 [카메라 프리셋] 정보가 있으면 카메라에 프리섹값 전송
					var presetIs = ims.sensor[senId].camera; // 관련 카메라 목록
					// 카메라 포커스 이동
					if(cfg.runProgram.procOnvif) { // 온비프 프로세서가 구동중이면 
						ptzOnvifCtlGroup(client.remoteAddress, senId); // 프리셋 그룹 전송
					}
					
					// 로그파일 등록
					saveEvent(senId+','+senName+','+beep+','+status+','+msg+','+shot); 

					// IP Relay 실행
					if(ims.sensor[senId].relayAddr && ims.sensor[senId].relayPort && ims.sensor[senId].relayNumber) {
						ipRelayWrite(ims.sensor[senId].relayAddr, ims.sensor[senId].relayPort, ims.sensor[senId].relayNumber, 1, "message");
					}
				}
				// aliveVerify(senId, beep); // 이벤트 발생한 최종 시간과 이전 발생시간 간의 차이값(미리초) 등록
			} else { // 관리자에 의해 거부(블럭)된 이벤트이면 
				io.sockets.emit('sendEventDeny', { id: senId, mapId: ims.sensor[senId].mapID, subj: ims.sensor[senId].subj, status: 5 }); // "5":"WARNING",
				// aliveVerify(senId, beep); // 이벤트 발생한 최종 시간과 이전 발생시간 간의 차이값(미리초) 등록
			}
		}
		/* 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음
		client.write('received');
		*/

    });
	
	// /* 지우지 말것, 오류 분석 목적이 아니면 굳이 클라이언트에 보낼필요 없음 */
	// client.on('end', function() {
	// 	console.log('Client disconnected');
	// });
	// client.on('error', function(err) {
	// 	console.log('Socket Error: ', JSON.stringify(err));
	// });
	// client.on('timeout', function() {
	// 	console.log('Socket Timed out');
	// });
	
	
}).listen(portIn); // Receive from ITS -> IMS(38087)
console.log('\nListen ITS from http://localhost:'+portIn+'/');

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
	// if(typeof(cfg.filterIP.allow[clientIP]) !== "undefined") process.exit(); ) 
	// if(typeof(cfg.filterIP.deny[clientIP]) !== "undefined") process.exit(); ) 
	
	// // 관리자 아이피(cfg.license.ownerIp)가 정의 되었으면 다른 아이피의 접근을 제한 한다.
	// if ((cfg.license.ownerIp) && (cfg.license.ownerIp != clientIP)) {
		// return 0;
	// } // return 0; // 접근제한

	// 시스템 명령 관련
	socket.on('systemCmd', function(data) {
		cmd = cfg.systemCmd[data];
		logger(clientIP + ' systemCmd ' + data);
		executeCmd(cmd, function (response) {
			logger(response);
			// console.log(response);
		});
	});

	// 사용자 명령 관련
	// data.cmd는 String 형식의 linux bash 명령으로 구성 된다.
	socket.on('userCmd', function(data) {
		logger(clientIP + ' userCmd ' + data.cmd);
		executeCmd(data.cmd, function (response) {
			logger(response);
			// console.log(response);
		});
	});

	// 시스템 명령 관련
	socket.on('apiAction', function(data) {
		// logger(clientIP + ' apiAction ' + data);
		// console.log(clientIP + ' apiAction ' + data);
		var curMapID = data.mapID;
		executeCmd(data.cmd, function (response) {
			// logger(response);
			/////////////////////// 릴레이 상태 요청
			// response -> stdout: {"category": "gpio", "ip": "192.168.0.100", "status": "9", "response": {"R01": 0, "S09": 0, "R03": 1, "R02": 1, "R05": 0, "R04": 0, "R07": 0, "R06": 0, "S13": 0, "S12": 0, "S11": 0, "S10": 0, "S16": 0, "S15": 0, "S14": 0, "P02": 1, "P01": 1, "R08": 0}}
			try {
				var data = JSON.parse(response);
				if("stdout" in data) { // gpio의 전체 상태요청(status:9)이며 그에 따른 정보가 확인되면 자식에게 gpioStatus 전송
					if(data["stdout"]["category"] == "gpio") {
						io.sockets.emit('gpioStatus', { mapID: curMapID, status: data["stdout"]["response"]}); // 자식에게 gpioStatus 전송
						// if(data["stdout"]["status"] == "9") { 
						// 	console.log(data["stdout"]["response"]);
						// 	io.sockets.emit('gpioStatus', { mapID: curMapID, status: data["stdout"]["response"]}); // 자식에게 gpioStatus 전송
						// }
					}
				}
			} catch(e) {
				logger(e); // error in the above string (in this case, yes)!
			}
		});
		// echo '[{ "audio": { "source": "2", "volume": "80", "loop": "1" } }]' | nc 192.168.0.60 34001 -q 0
		// echo '[{ "gpio": { "status": "2", "id": "R01", "hold": "", "msg": ""}}]' | nc 192.168.0.60 34001 -q 0
		// echo '[{ "system": { "command": "stop_audio", "value": "" }}]' | nc 192.168.0.60 34001 -q 0
	});

	// 실시간 접속자 로그
	socket.on('connectedIP', function() { 
		// console.log(connectedIP);
		io.sockets.emit('connectedIP', connectedIP );
		logger(clientIP + ' connectedIP ');
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
		saveConfigJson();
		logger(clientIP + ' sysAccSave ');
	});
	
	socket.on('blockZone', function(data) { // 시스템 어카운트 정보 저장 "4":"BLOCK"
		// if (cfg.filterIP.admin.indexOf(clientIP) > -1 && data.id) { // admin 사용자만 필터링 기능 허용
			if (cfg.filterIP.deny.indexOf(data.id) === -1) { // 미등록 정보면 추가함
				cfg.filterIP.deny.push(data.id); // 등록
				saveConfigJson();
				// console.log(clientIP + ' blockZone ' + data.name + ' ' + data.id); 
				logger(clientIP + ' blockZone ' + data.name + ' ' + data.id);
				// w_gr, w_ca, w_sensorId, w_sensorName, w_userName, w_shot, w_action, w_description
				insertEvent(0, 900, data.id, data.name, clientIP, '', 4, 'Set Block'); 

			}
			io.sockets.emit('denyZoneList', { denyList:cfg.filterIP.deny }); // 현재 선언된 필터정보 전송
		// }
	});
	
	socket.on('clearZone', function(data) { // "4":"BLOCK"
		// if (cfg.filterIP.admin.indexOf(clientIP) > -1 && data.id) { // admin 사용자만 필터링 기능 허용
			if (cfg.filterIP.deny.indexOf(data.id) > -1) { // 등록 정보면 삭제함
				cfg.filterIP.deny.splice(cfg.filterIP.deny.indexOf(data.id), 1); // 제거
				saveConfigJson();
				// console.log(clientIP + ' clearZone ' + data.name + ' ' + data.id); 
				logger(clientIP + ' clearZone ' + data.name + ' ' + data.id);
				insertEvent(0, 900, data.id, data.name, clientIP, '', 4, 'Clear Block'); 
			}
			io.sockets.emit('denyZoneList', { denyList:cfg.filterIP.deny }); // 현재 선언된 필터정보 전송
		// }
	});

	socket.on('denyZoneList', function(data) { 
		// if (cfg.filterIP.admin.indexOf(clientIP) > -1) { // admin 사용자만 필터링 기능 허용
			io.sockets.emit('denyZoneList', { denyList:cfg.filterIP.deny }); // 현재 선언된 필터정보 전송
		// }
	});
	
	// 클라이언트 아이피 전송()
	socket.on('findClientIP', function(data) {
		// admin 사용자로 등록되었거나 콘솔 브라우저로 접근시 ..
		if (cfg.filterIP.admin.indexOf(clientIP) > -1 || clientIP == myIpAddr) { // admin 사용자만 PTZ 기능 허용
			var userLv = "admin";
		} else if (cfg.filterIP.manager.indexOf(clientIP) > -1) { // manager 사용자만 PTZ 불가
			var userLv = "manager";
		} else if (cfg.filterIP.viewer.indexOf(clientIP) > -1) {
			var userLv = "viewer";
		} else {
			var userLv = "guest";
		}
		
		io.sockets.emit('findClientIP', { 
			ip: clientIP,
			oIp: cfg.license.ownerIp,
			id: data,
			lv: userLv
		});
		logger(clientIP + ' findClientIP ' + userLv);
	});

    // 이벤트 확인절차 actionClear 센서 "3":"USER_LOG"
    socket.on('actionClearS', function (data) {
		var arr = data.split("_||_");
		insertEvent(ims.sensor[arr[0]].group, 200, arr[0], arr[1], arr[2], '', 3, arr[3]); 
		// 클라이언트에 해제 이벤트 전송: id, name, beep, status, shot
		io.sockets.emit('sendEventLog', { id: arr[0], name: arr[1], beep: 2, status: 3, shot: '' });
		
		// IP Relay 해지 실행 
		if(ims.sensor[arr[0]].relayAddr && ims.sensor[arr[0]].relayPort && ims.sensor[arr[0]].relayNumber) {
			ipRelayWrite(ims.sensor[arr[0]].relayAddr, ims.sensor[arr[0]].relayPort, ims.sensor[arr[0]].relayNumber, 0, "message");
		}

		logger(clientIP + ' actionClear Sensor ' + data);
	}); 
	
    // 이벤트 확인절차 actionClear 함체 "3":"USER_LOG"
    socket.on('actionClearB', function (data) {
		var arr = data.split("_||_");
		insertEvent(ims.box[arr[0]].group, 300, arr[0], arr[1], arr[2], '', 3, arr[3]); 
		// 클라이언트에 해제 이벤트 전송: id, name, beep, status, shot
		io.sockets.emit('sendEventLog', { id: arr[0], name: arr[1], beep: 2, status: 3, shot: '' });
		
		// IP Relay 해지 실행 
		if(ims.box[arr[0]].relayAddr && ims.box[arr[0]].relayPort && ims.box[arr[0]].relayNumber) {
			ipRelayWrite(ims.box[arr[0]].relayAddr, ims.box[arr[0]].relayPort, ims.box[arr[0]].relayNumber, 0, "message");
		}
		
		logger(clientIP + ' actionClear Box ' + data);
	}); 
	
    // 사용자 수동 등록 manualAdd 메뉴얼 "3":"USER_LOG"
    socket.on('actionClearM', function (data) {
		// sensorName, userName, actionDesc
		var arr = data.split("_||_");
		insertEvent(0, 900, 'NA', arr[1], arr[2], '', 3, arr[3]); 
		io.sockets.emit('sendAddLog', { name: arr[1], status: 3, from: 'M' });
		logger(clientIP + ' actionClear Manual ' + data);
	}); 

    // 이벤트 확인절차 actionClose 종료 "0":"NORMAL"
    socket.on('actionClose', function (data) {
		var arr = data.split("_||_");
		// 주의 : 현재의 요소가 박스인지 센서인지 확인후
		
		if (ims.sensor.hasOwnProperty(arr[0])) { // defined된 등록 정보
			var groupIs = ims.sensor[arr[0]].group;
		} else if (ims.box.hasOwnProperty(arr[0])) { // 등록 정보
			var groupIs = ims.box[arr[0]].group;
		} else {
			return;
		}
		// insertEvent(ims.sensor[arr[0]].group, 900, arr[0], arr[1], clientIP, '', 0, 'Close Alarm'); 
		insertEvent(groupIs, 900, arr[0], arr[1], clientIP, '', 0, 'Close Alarm'); 
		// 클라이언트에 해제 이벤트 전송: id, name, beep, status, shot
		io.sockets.emit('sendEventLog', { id: arr[0], name: arr[1], beep: 2, status: 0, shot: '' });
		
		// // IP Relay 해지 실행 
		// if(ims.sensor[arr[0]].relayAddr && ims.sensor[arr[0]].relayPort && ims.sensor[arr[0]].relayNumber) {
			// ipRelayWrite(ims.sensor[arr[0]].relayAddr, ims.sensor[arr[0]].relayPort, ims.sensor[arr[0]].relayNumber, 0, "message");
		// }

		logger(clientIP + ' action close ' + data);
	}); 
	
    // 클라이언트 요청(팬스클릭)시 한시간 동안 센서에서 발생된 로그를 보내준다.
    socket.on('sensorLog', function (data) { // sensorLog : SVG에 선언된 센서의 ID
		var sensorID = data;
		getEvtLog(sensorID, function(err, row) { // 데이터베이스 내 테이블 읽어오기
			if (err) {
				console.log(err);
			} else {
				io.sockets.emit('sendListLog', { logList:row }); // Client로 전송
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
				if(sensorID) {
					io.sockets.emit('sensorLogOneDay', { logList:row });
					logger(clientIP + ' sensorLogRequest - view 24 hour live log ');
				} else {
					io.sockets.emit('sensorLogOneHour', { logList:row });
					logger(clientIP + ' sensorLogRequest - view 1 hour live log ');
				}
			}
		});
	}); 
	
	// 펜스 최종상태 데이터베이스 정보로 클라이인트가 시작되거나 새로 고침시 실행
    socket.on('getLastSituation', function (data) { 
		getEvtLastLog(function(err, row) { 
			if (err) {
				console.log(err);
			} else {
				io.sockets.emit('getLastSituation', { logList:row });
				// console.log(row);
			}
		});
 		logger(clientIP + ' getLastSituation - Connected Monitoring ..');
	}); 

	// 카메라 컨트롤
	socket.on('ptzOnvifCtl', function(data) { // 시스템 어카운트 정보 저장
		// 접속한 현재의 아이피가 어드민그룹에 포함되어 있으면 PTX 허용
		if (cfg.filterIP.admin.indexOf(clientIP) > -1) { // admin 사용자만 PTZ 기능 허용
			ptzOnvifCtl(data);
			logger(clientIP + ' ptzOnvifCtl ' + data.camPort+' '+data.cmd);
		}
	});

	// 카메라 컨트롤 그룹
	socket.on('ptzOnvifCtlGroup', function(data) { // 시스템 어카운트 정보 저장
		// 접속한 현재의 아이피가 어드민그룹에 포함되어 있으면 PTX 허용
		if (cfg.filterIP.admin.indexOf(clientIP) > -1) { // admin 사용자만 PTZ 기능 허용
			ptzOnvifCtlGroup(clientIP, data, 0); // 사용자 요청
			logger(clientIP + ' ptzOnvifCtlGroup ' + data);
		}
	});

	// 카메라 컨트롤 그룹
	socket.on('ptzOnvifCtlGroupBox', function(data) { // 시스템 어카운트 정보 저장
		// 접속한 현재의 아이피가 어드민그룹에 포함되어 있으면 PTX 허용
		if (cfg.filterIP.admin.indexOf(clientIP) > -1) { // admin 사용자만 PTZ 기능 허용
			ptzOnvifCtlGroupBox(data);
			logger(clientIP + ' ptzOnvifCtlGroupBox ' + data);
		}
	});
});
app.listen(portOut); // Display server
console.log('Listen Open Port http://localhost:'+portOut+'/');
