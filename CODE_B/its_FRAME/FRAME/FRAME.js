///////////////////////////////////////////////////
///////////////////////////////////////////////////

const app = require("http").createServer(handler);
const io = require("socket.io")(app);
const fs = require("fs");
const os = require('os');

// // https://www.npmjs.com/package/node-rtsp-stream
// Stream = require('node-rtsp-stream')
// stream = new Stream({
// 	name: 'name',
// 	// streamUrl: 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov',
// 	streamUrl: 'rtsp://admin:admin@96.48.233.195:5550',
// 	wsPort: 9999,
// 	ffmpegOptions: { // options ffmpeg flags
// 	'-stats': '', // an option with no neccessary value uses a blank string
// 	'-r': 30 // options with required values specify the value after the key
// 	}
// })
// ffmpeg -i rtsp://admin:admin@96.48.233.195:5550 -f mpeg1video -b 800k -r 30 http://localhost:8082
// ffmpeg -i rtsp://admin:admin@96.48.233.195:5550 -f mpeg1video -r 30 -b:a http://localhost:8082
// ffmpeg -i rtsp://admin:admin@96.48.233.195:5550 -f mpeg1video -r 30 -b:v http://localhost:8082
// ffmpeg -i rtsp://admin:admin@96.48.233.195:5550 -c copy -map 0 -f mpeg1video http://localhost:8082

var cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf8")); // COMMON -> config.json 파일 읽기
var local = JSON.parse(fs.readFileSync("config.json", "utf8")); // FRAME -> config.json 파일 읽기
var camera = JSON.parse(fs.readFileSync("camera.json", "utf8")); // FRAME -> templet.json 파일 읽기
var templet = JSON.parse(fs.readFileSync("templet.json", "utf8")); // FRAME -> templet.json 파일 읽기

var html = fs.readFileSync(cfg.file.html_target, "utf8");
var portIn = cfg.interface.port_in;
var portOut = cfg.interface.port_out;

// 자신의 아이피 https://gist.github.com/sviatco/9054346
var serverIP, ifaces = os.networkInterfaces()
for (var dev in ifaces) {
	var iface = ifaces[dev].filter(function(details) {
		return details.family === 'IPv4' && details.internal === false;
	});
	if(iface.length > 0) serverIP = iface[0].address;
}
// console.log(serverIP);

function handler(req, res) {
	res.setHeader("Content-Type", "text/html");
	res.setHeader("Content-Length", Buffer.byteLength(html,"utf8"));
	res.end(html);
}

//////////////////////////////////////////////////////////
// 환경변수(config.json) 저장
//////////////////////////////////////////////////////////
function saveConfigJson() {
	fs.writeFile("config.json", JSON.stringify(local, null, 4), (err) => {
		if (err) throw err;
		// console.log("The file has been saved!");
	});
}

//////////////////////////////////////////////////////////
// 소켓을 통해 자료를 index.html로 전송한다.
//////////////////////////////////////////////////////////
function event_send(id, status) {
	io.sockets.emit(id, status);
}

//////////////////////////////////////////////////////////
// Client로부터 이벤트를 받고 관련 작업 실행
//////////////////////////////////////////////////////////
io.sockets.on("connection", function (socket) {
	var clientIP = socket.handshake.address.replace(/^.*:/, ""); //  접근자 아이피 
	// console.log(clientIP,local.filterIP.admin.includes(clientIP));

	socket.on("setGrid", function(data) {
		// 허용된 아이피에게 만 적용하기 위해 어래이 내에 일치하는 값이 있는 확인
		if(local.filterIP.admin.includes(clientIP)) { 
			// console.log("Allow User " + clientIP);
			local.client[data.framePageID] = {};
			local.client[data.framePageID] = data;
			saveConfigJson();
			// io.sockets.emit("curPage", local.client[data.framePageID]);
			// console.log("setGrid", data);
		}
	});

	socket.on("getPage", function (data) { // 	{"id": myID, "framePageID": pageID}
		if (data.framePageID in local.client){
			io.sockets.emit("curPage", { id: data.id, fPage: local.client[data.framePageID]});
		}
	});


	socket.on("getDesign", function (data) { // 	{"id": myID, "framePageID": pageID}
		if (data.frameDesignID in templet){
			io.sockets.emit("curPage", { id: data.id, fPage: templet[data.frameDesignID]});
		}
	});
	
	socket.on("setCamera", function (data) { // 	{"id": myID, "framePageID": pageID}
		io.sockets.emit("setCamera", { id: data.id, camera: camera});
	});

	socket.on("setCamID", function(data) {
		var camID = "";
		for (var key in camera){
			if(camera.hasOwnProperty(key)){
				// console.log(key, camera[key])
				camID += "<div class='camera' id='cam_"+key+"'>"+key+"</div>";
			}
		}
		io.sockets.emit("setCamID", { id: data, camID: camID});
	});

	// 클라이언트 아이피 전송()
	socket.on("getUserInfo", function(data) {
		// admin 사용자로 등록되었거나 콘솔 브라우저로 접근시 ..
		if(local.filterIP.admin.includes(clientIP)) {var className = "admin"; var classID = 9;}
		else if (local.filterIP.manager.includes(clientIP)) {var className = "manager"; var classID = 7;} 
		else if (local.filterIP.viewer.includes(clientIP)) {var className = "viewer"; var classID = 5;} 
		else {var className = "guest"; var classID = 1;}
		
		io.sockets.emit("getUserInfo", { ipS: serverIP, ipC: clientIP, id: data, className: className, classID: classID });
		// console.log(clientIP + " " + data + " " + className);
	});

});

app.listen(portOut); // Display server
console.log("\nService server running at http://localhost:"+portOut+"/");

//////////////////////////////////////////////////////////
// 외부에서 portIn을 통해 정보를 받아 관련작업 수행(파싱) / portOut 으로 전달한다.
// 예: id=ID : relay 번호, status=STATUS 0:off 1:on, msg=MSG
//////////////////////////////////////////////////////////
require("net").createServer(function (socket) {
	// console.log("connected");
	socket.on("data", function (data) { // 외부 portIn 으로 부터 받은 정보를 data 변수에 저장
		console.log(data);
		// socket.emit("received");
	});
}).listen(portIn); // Receive server
// console.log("Receive server running at http://localhost:"+portIn+"/");


