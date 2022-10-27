/**
 * https://github.com/agsh/onvif
 */
var fs = require('fs');
var flow = require('nimble');

var cfg = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
var ims = JSON.parse(fs.readFileSync('./cfgIms.json', 'utf8')); // 환경 파일 읽기
var ipAddr = ims.camera[process.argv[2]].addr;
var port = ims.camera[process.argv[2]].port;
var username = ims.camera[process.argv[2]].user;
var password = ims.camera[process.argv[2]].pass;
var camPort = ims.camera[process.argv[2]].camPort;

// if(process.argv.length > 6) {
	// var ipAddr = process.argv[2];
	// var port = parseInt(process.argv[3]);
	// var username = process.argv[4];
	// var password = process.argv[5];
	// var camPort = parseInt(process.argv[6]);
// } else if(process.argv.length == 3){
	// var ipAddr = ims.camera[process.argv[2]].addr;
	// var port = ims.camera[process.argv[2]].port;
	// var username = ims.camera[process.argv[2]].user;
	// var password = ims.camera[process.argv[2]].pass;
	// var camPort = ims.camera[process.argv[2]].camPort;
	// // console.log(ipAddr, ims.camera[process.argv[2]].model, camPort);
// } else {
	// console.log("ex: node ", process.argv[1], ipAddr, port, username, password, camPort);
	// process.exit();
// }


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

var STOP_DELAY_MS = 50; // 이동(줌)의 연속성 인터벌

var Cam = require('onvif').Cam;
new Cam({
	hostname : ipAddr,
	username : username,
	password : password,
	port : port,
	timeout : 10000
}, function CamFunc(err) {
	if (err) {
		console.log(err);
		return;
	}
	var cam_obj = this;
	var stop_timer;
	var ignore_action = false;
	var preset_names = [];
	var preset_tokens = [];
	
	var getHostname;
	var getDateTime;
	
	flow.series([
		function(callback) {
			cam_obj.getSystemDateAndTime(function(err, date, xml) {
				if (!err) getDateTime = date;
				callback();
			});
		},
		function(callback) {
			cam_obj.getHostname(function(err, date, xml) {
				if (!err) getHostname = date.name;
				callback();
			});
		},
		function(callback) {
			cam_obj.getSystemDateAndTime(function(err, date, xml) {
				if (!err) getDateTime = date;
				callback();
			});
		},
		function(callback) {
			// console.log('Camera: ' + ipAddr + ' - ' + getHostname + ' - ' + getDateTime);
			callback();
		}
	]); // end flow
	
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

	require('net').createServer(function (socket) {
		socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
			// console.log(data.toString());
			if (ignore_action) {
				return;
			}
			try {
				/* socketCam.write("cmd:"+data.cmd+",pan:"+data.pan+",tilt:"+data.tilt+",zoom:"+data.zoom+",preset:"+data.preset+",option:"+data.option); */
				// camPort: ims.camera[id].camPort,
				// cmd:'',
				// pan: 0,
				// tilt: 0,
				// zoom: 0,
				// preset: 0,
				// option: ''
				var onvifInfo = data.toString();
				var obj = onvifInfo.split(",").reduce(function(o, c){
				   var arr = c.split(":");
				   return o[arr[0].trim()] = arr[1].trim(), o; // comma operator
				},{});
				
				if(obj['cmd'] == 'ptzMoveCont') {
					ptzMoveCont(obj['pan'], obj['tilt'], obj['zoom']);
				} else if(obj['cmd'] == 'absoluteMove') {
					// console.log("abs", obj['pan'], obj['tilt'], obj['zoom']);
					absoluteMove(obj['pan'], obj['tilt'], obj['zoom']);
				} else if(obj['cmd'] == 'relativeMove') {
					// console.log("rel", obj['pan'], obj['tilt'], obj['zoom']);
					relativeMove(obj['pan'], obj['tilt'], obj['zoom']);
				} else if(obj['cmd'] == 'gotoPresetNo'){
					gotoPresetNo(obj['preset']);
				} else if(obj['cmd'] == 'gotoHomePosition'){
					gotoHomePosition();
					// gotoPresetName('focusITS');
				} else if(obj['cmd'] == 'setHomePosition'){
					// setHomePosition();
					// removePresetName('focusITS');
					// setPresetName('focusITS');
				} else if(obj['cmd'] == 'gotoPresetName'){
					gotoPresetName(obj['option']);
				} else if(obj['cmd'] == 'setPresetName'){
					setPresetName(obj['option']);
				}
			} catch (e) {
				return;
			}
			logger("camPort:"+camPort+"cmd:"+obj['cmd']+",pan:"+obj['pan']+",tilt:"+obj['tilt']+",zoom:"+obj['zoom']+",preset:"+obj['preset']+",option:"+obj['option']);;

		});
	}).listen(camPort); // Receive server
	// console.log('Receive server running at http://localhost:'+camPort+'/');

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
		// console.log(number);
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
});
