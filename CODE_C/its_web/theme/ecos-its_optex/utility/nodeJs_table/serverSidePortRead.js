var portIn = 8010;

//////////////////////////////////////////////////////////
// 포트 8000으로 부터 받은 정보를 파싱한후 포트 9000으로 전달한다.
//////////////////////////////////////////////////////////
require('net').createServer(function (socket) {
    // console.log("connected");
    socket.on('data', function (data) { // data 변수에 포트로부터 입력된 값을 저장 하다.
        console.log(data.toString());
    });
}).listen(portIn); // Receive server
console.log('Receive server running at http://localhost:'+portIn+'/');