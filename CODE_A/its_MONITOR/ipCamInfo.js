/**
 * Created by Roger Hardiman <opensource@rjh.org.uk>
 *
 * Brute force scan of the network looking for ONVIF devices
 * Displays the time and date of each device
 *          the make and model
 *          the default RTSP address
 * This DOES NOT use ONVIF Discovery. This softweare tries each IP address in
 * turn which allows it to work on networks where ONVIF Discovery does not work
 * (eg on Layer 3 routed networks)
 * https://github.com/agsh/onvif
 *
 * https://www.npmjs.com/package/onvif
 * 카메라 정보를 파악하여 ipCam.json파일로 저장 하는 기능
 */

var Cam = require('onvif').Cam;
var flow = require('nimble');
var fs = require('fs');

// Onvif 정보를 생산하기의해 등록된 카메라정보(Account Info) 읽어들임
var cfg = JSON.parse(fs.readFileSync('cfgIms.json', 'utf8')); // 환경 파일 읽기

var ipCam = {};

// cam_list = [ { "addr":"192.168.0.130", "user":"admin", "pass":"admin", "port":80 } ];
var cam_list = [];

// hide error messages
console.error = function() {};

// 환경변수(config.json) 저장
function saveConfigJson(name, json) {
	fs.writeFile(name+'.json', JSON.stringify(json, null, 4), (err) => {
		if (err) throw err;
	});
}

// 카메라 정보만을 cam_list에 저장
for(var k in cfg["camera"]) {
	cam_list.push({ addr: cfg["camera"][k]["addr"], user: cfg["camera"][k]["user"], pass: cfg["camera"][k]["pass"], port: cfg["camera"][k]["port"] });
}

// 카메라 정보 cam_list로 부터 관련정보를 추출후 변수선언
// function ipCamInfo(host,user,pass,port) {
// getSystemDateAndTime(callback)
// getDeviceInformation(callback)
// getServices(callback)
// getServiceCapabilities(callback)
// getStreamUri(options, callback)
// getPresets(options, callback)
// gotoPreset(options, callback)
// setPreset(options, callback)
// removePreset(options, callback)
// gotoHomePosition(options, callback)
// setHomePosition(options, callback)
// getNodes(callback)
// relativeMove(options, callback)
// absoluteMove(options, callback)
// continuousMove(options, callback)
// stop(options, callback)
// getStatus(options, callback)
// getConfigurations(callback)
// getConfigurationOptions(configurationToken, callback)
cam_list.forEach(function (camList) {
	new Cam({
		// hostname: host,
		// username: user,
		// password: pass,
		// port: port,
		hostname: camList["addr"],
		username: camList["user"],
		password: camList["pass"],
		port: camList["port"],
		timeout : 5000
	}, function CamFunc(err) {
		if (err) return;

		var cam_obj = this;

		var got_date;
		var got_info;
		var got_snapshot;
		var got_live_stream_tcp;
		var got_live_stream_udp;
		var got_live_stream_multicast;
		var got_recordings;
		var got_replay_stream;
		var get_presets;
		var get_nodes;
		var get_status;
		var get_configurations;

		// Use Nimble to execute each ONVIF function in turn
		// This is used so we can wait on all ONVIF replies before
		// writing to the console
		flow.series([
			function(callback) {
				cam_obj.getSystemDateAndTime(function(err, date, xml) {
					if (!err) got_date = date;
					callback();
				});
			},
			function(callback) {
				cam_obj.getDeviceInformation(function(err, info, xml) {
					if (!err) got_info = info;
					callback();
				});
			},

			function(callback) {
				cam_obj.getSnapshotUri(function(err, snapshot) {
					if (!err) got_snapshot = snapshot;
					callback();
				});
			},
			
			function(callback) {
				try {
					cam_obj.getStreamUri({
						protocol: 'RTSP',
						stream: 'RTP-Unicast'
					}, function(err, stream, xml) {
						if (!err) got_live_stream_tcp = stream;
						callback();
					});
				} catch(err) {callback();}
			},
			function(callback) {
				try {
					cam_obj.getStreamUri({
						protocol: 'UDP',
						stream: 'RTP-Unicast'
					}, function(err, stream, xml) {
						if (!err) got_live_stream_udp = stream;
						callback();
					});
				} catch(err) {callback();}
			},
			function(callback) {
				try {
					cam_obj.getStreamUri({
						protocol: 'UDP',
						stream: 'RTP-Multicast'
					}, function(err, stream, xml) {
						if (!err) got_live_stream_multicast = stream;
						callback();
					});
				} catch(err) {callback();}
			},
			
			function(callback) {
				cam_obj.getRecordings(function(err, recordings, xml) {
					if (!err) got_recordings = recordings;
					callback();
				});
			},
			
			function(callback) {
				// Get Recording URI for the first recording on the NVR
				if (got_recordings) {
					cam_obj.getReplayUri({
						protocol: 'RTSP',
						recordingToken: got_recordings[0].recordingToken
					}, function(err, stream, xml) {
						if (!err) got_replay_stream = stream;
						callback();
					});
				} else {
					callback();
				}
			},

			function(callback) {
				cam_obj.getPresets(function(err, preset) {
					if (!err) get_presets = preset;
					callback();
				});
			},
			
			function(callback) {
				cam_obj.getNodes(function(err, nodes) {
					if (!err) get_nodes = nodes;
					callback();
				});
			},

			function(callback) {
				cam_obj.getStatus(function(err, status) {
					if (!err) get_status = status;
					callback();
				});
			},
			
			function(callback) {
				cam_obj.getConfigurations(function(err, configurations) {
					if (!err) get_configurations = configurations;
					callback();
				});
			},
			
			function(callback) {
				
				ipCam[camList["addr"]] = {};
				ipCam[camList["addr"]]["user"] = camList["user"];
				ipCam[camList["addr"]]["pass"] = camList["pass"];
				ipCam[camList["addr"]]["port"] = camList["port"];
				ipCam[camList["addr"]]["date"] = got_date;
				ipCam[camList["addr"]]["info"] = got_info;
				ipCam[camList["addr"]]["snapshot"] = got_snapshot;
				ipCam[camList["addr"]]["stream"] = {};
				ipCam[camList["addr"]]["stream"]["tcp"] = got_live_stream_tcp;
				ipCam[camList["addr"]]["stream"]["udp"] = got_live_stream_udp;
				ipCam[camList["addr"]]["stream"]["multicast"] = got_live_stream_multicast;
				ipCam[camList["addr"]]["stream"]["replay"] = got_replay_stream;
				
				ipCam[camList["addr"]]["preset"] = get_presets;
				ipCam[camList["addr"]]["nodes"] = get_nodes;
				ipCam[camList["addr"]]["status"] = get_status;
				ipCam[camList["addr"]]["config"] = get_configurations;

				saveConfigJson('ipCamInfo', ipCam)
				
				console.log('------------------------------');
				console.log('IPCAM: ' + camList["addr"] + ' - ' + ipCam[camList["addr"]]["info"]["model"]);

				callback();
			},
		]); // end flow
	});
});


