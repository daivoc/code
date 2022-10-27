// 본 소스파일이 있는 폴더에서 소켓아이오를 설치 한다.
// $ npm i socket.io
// 노드를 통해 프로그램을 실행 한다
// $node clock.js 
// 브라우저를 통해 index.html을 구동 한다(포트를 확인 할것 
// 브라우져에서 192.168.0.10:8080

var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var html = fs.readFileSync('click.html', 'utf8');
// var time = require('time');

function handler (req, res) {
	res.setHeader('Content-Type', 'text/html');
	res.setHeader('Content-Length', Buffer.byteLength(html,'utf8'));
    res.end(html);
}

function tick () {
	// var now = new time.Date();
	// now.setTimezone('Europe/Amsterdam');
	// io.sockets.send(now);

	// var now = new Date().toUTCString();
	// var nowUtc = new Date( now.getTime() + (now.getTimezoneOffset() * 60000));
	var now = ' '+ new Date()
	io.sockets.send(now);
}

setInterval(tick, 1000);

app.listen(8080);