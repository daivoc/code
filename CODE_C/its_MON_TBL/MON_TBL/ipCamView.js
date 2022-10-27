/**
 * Created by Andrew D.Laptev<a.d.laptev@gmail.com> on 1/21/15.
 * https://github.com/agsh/onvif/blob/6210848128b34b1d2a54dfc328cf7c05b299d4b4/example.js
 */

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var ipCam = require('onvif').Cam;
var fs = require('fs');
var request = require('request');

var cfg = JSON.parse(fs.readFileSync('./config.json', 'utf8')); // 환경 파일 읽기
var ims = JSON.parse(fs.readFileSync('./cfgIms.json', 'utf8')); // 환경 파일 읽기
var icc = JSON.parse(fs.readFileSync('./camera.json', 'utf8')); // 환경 파일 읽기

var camList = [];
for(var k in ims["camera"]) { // 카메라 정보만을 cam_list에 저장
	camList.push({ camID: k, subj: ims["camera"][k]["subj"], model: ims["camera"][k]["model"], addr: ims["camera"][k]["addr"], user: ims["camera"][k]["user"], pass: ims["camera"][k]["pass"], port: ims["camera"][k]["port"] });
}
if(camList.length == 0) {
	console.log("No Camera Info..");
	process.exit();
}

var __global_variables_ims__ = '<script>var ims = '+ fs.readFileSync('./cfgIms.json', 'utf8') +'</script>';
var __global_variables_icc__ = '<script>var icc = '+ fs.readFileSync('./camera.json', 'utf8') +'</script>';

var __script_jquery_js__ = '<script>'+fs.readFileSync('/home/pi/common/jquery/jquery-3.1.1.min.js', 'utf8')+'</script>';
var __script_jquery_ui_js__ = '<script>'+fs.readFileSync('/home/pi/common/jquery/ui/jquery-ui.js', 'utf8')+'</script>';
var __style_jquery_ui_css__ = '<style>'+fs.readFileSync('/home/pi/common/jquery/ui/jquery-ui.css', 'utf8')+'</style>';

//////////////////////////////////////
var html = '';
fs.readFile('ipCamView.html', 'utf8', function (err,data) {
	if (err) {
		return console.log(err);
	}
	var data = data.replace(/__script_jquery_js__/g, __script_jquery_js__);
	var data = data.replace(/__script_jquery_ui_js__/g, __script_jquery_ui_js__);
	var data = data.replace(/__style_jquery_ui_css__/g, __style_jquery_ui_css__);
	var data = data.replace(/__global_variables_ims__/g, __global_variables_ims__);
	var data = data.replace(/__global_variables_icc__/g, __global_variables_icc__);
	html = data;
});

function handler(req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

function getStatus(data) {
	new ipCam({
		hostname: data.addr,
		username: data.user,
		password: data.pass,
		port: 80
	}, function(err) {
		if (err) {
			console.log('Connection Failed for ' + data.addr + ' Port: ' + 80 + ' Username: ' + data.user + ' Password: ' + data.pass);
			return console.log(err);
		}
		
		if(icc[data.model].isPTZ) {
			this.getStatus(function(error, status) {
				if (error) {
					console.error('GetStatus error', error)
				} else {
					// var x = status['position']['x'];
					// var y = status['position']['y'];
					// var z = status['position']['zoom'];
					// console.log(x,y,z);
					io.sockets.emit('getStatus', status);
				}
			});
		}
		// 블렛카메라인경우 시간만 추출한다.
		this.getSystemDateAndTime(function(error, data) {
			if (!error) {
				io.sockets.emit('getSystemDateAndTime', data);
			}
		});
	});
}

function getSnapshot(data) {
	new ipCam({
		hostname: data.addr,
		username: data.user,
		password: data.pass,
		port: 80
	}, function(err) {
		if (err) {
			console.log('Connection Failed for ' + data.addr + ' Port: ' + 80 + ' Username: ' + data.user + ' Password: ' + data.pass);
			return console.log(err);
		}

		// 이하는 서브에 이미지를 바로 추출 및 전송하는 기능
		// 실행 되지 않는다.
		this.getSnapshotUri(function(err, snapshot) {
			request({
				method: 'GET',
				uri: snapshot.uri,
				gzip: true,
				encoding: 'binary',
				'auth': {
					'user': data.user,
					'pass': data.pass,
					'sendImmediately': false
				}
			}, function (error, response, body) {
				if (error) {
					console.error('FetchSnapshot error', error)
				} else {
					var mimeType = response.headers['content-type']
					var b64encoded = Buffer.from(body, 'binary').toString('base64')
					var image = 'data:' + mimeType + ';base64,' + b64encoded
					
					io.sockets.emit('getSnapshot', image);
				}
			})
		});
	});
}

function ptzOnvifCtl(data) {
	if(icc[data.model].isPTZ) {
		new ipCam({
			hostname: data.addr,
			username: data.user,
			password: data.pass,
			port: 80
		}, function(err) {
			if (err) {
				console.log('Connection Failed for ' + data.addr + ' Port: ' + 80 + ' Username: ' + data.user + ' Password: ' + data.pass);
				return console.log(err);
			}
			// this.relativeMove({x:data.pan, y:data.tilt, zoom:data.zoom}); // 2 나 4 로 나누는 것은 이동폭을 줄이기 위함
			this.absoluteMove({x:data.pan, y:data.tilt, zoom:data.zoom}); // 2 나 4 로 나누는 것은 이동폭을 줄이기 위함
		});
	} else {
		console.log('Model ' + data.model + ' is not PTZ function.');
	}
}

// ///////////////////
// // 카메라 Onvif Control https://mylko72.gitbooks.io/node-js/content/chapter8/chapter8_2.html
// var net = require("net");
// function ptzOnvifCtl(data) {
	// var socketCam = net.connect({port : data.camPort});
	// socketCam.on('connect', function(){
		// console.log("cmd:"+data.cmd+",pan:"+data.pan+",tilt:"+data.tilt+",zoom:"+data.zoom+",preset:"+data.preset+",option:"+data.option);
		// socketCam.write("cmd:"+data.cmd+",pan:"+data.pan+",tilt:"+data.tilt+",zoom:"+data.zoom+",preset:"+data.preset+",option:"+data.option);
		// socketCam.destroy();
	// });
	// socketCam.on('data', function(data){
		// console.log(data.toString());
		// socketCam.end();
	// });
	// socketCam.on('end', function(){
		// console.log('Client disconnected');
	// });
// };

io.sockets.on('connection', function (socket) {
	var clientIP = socket.handshake.address.replace(/^.*:/, ''); //  접근자 아이피 

	socket.on('getCamList', function(data) { 
		console.log(clientIP, 'getCamList');
		io.sockets.emit('getCamList', camList);
	});
	socket.on('getCamStatus', function(data) { 
		console.log(clientIP, 'getCamStatus');
		getStatus(data);
		getSnapshot(data);
	});
	// 카메라 컨트롤
	socket.on('ptzOnvifCtl', function(data) { // 시스템 어카운트 정보 저장
		console.log(clientIP, 'Pan:' + data.pan + ' Tilt:' + data.tilt + ' Zoom:' + data.zoom);
		ptzOnvifCtl(data);
		setTimeout(function(){ 
			getStatus(data);
			getSnapshot(data); 
		}, 2000);
	});
});

var portOut = cfg["interface"]["camPort"];
app.listen(portOut); // Display server
console.log('Open Port http://localhost:'+portOut+'/');
