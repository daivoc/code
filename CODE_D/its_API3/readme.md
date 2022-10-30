# **ITS API User Manual**
<div style="page-break-after: always"></div>

# Table of Contents
- [**ITS API User Manual**](#its-api-user-manual)
- [Table of Contents](#table-of-contents)
- [FORMATS](#formats)
	- [**이벤트 발생**](#이벤트-발생)
		- [**센서 이벤트**](#센서-이벤트)
		- [**스케즐러 이벤트**](#스케즐러-이벤트)
		- [**타이머 이벤트**](#타이머-이벤트)
	- [**Action Script**](#action-script)
		- [**Format**](#format)
		- [**data**](#data)
		- [**command**](#command)
		- [**options**](#options)
	- [**복합명령(Complexed Action Script)**](#복합명령complexed-action-script)
		- [**Format**](#format-1)
- [Commands](#commands)
	- [**GPIO**](#gpio)
		- [**Format**](#format-2)
		- [**Hold**](#hold)
		- [Example: 이벤트 발생시 릴레이 R01 Off](#example-이벤트-발생시-릴레이-r01-off)
		- [Example: 이벤트 발생시 릴레이 R01 On](#example-이벤트-발생시-릴레이-r01-on)
		- [Example: 이벤트 발생시 릴레이 R01 Toggle(즉각반응)](#example-이벤트-발생시-릴레이-r01-toggle즉각반응)
		- [Example: 이벤트 발생시 릴레이 R01 1.5초간 On 후 Off](#example-이벤트-발생시-릴레이-r01-15초간-on-후-off)
		- [Example: 이벤트 발생시 릴레이 R01 0.5초간 반전 유지 후 재반전](#example-이벤트-발생시-릴레이-r01-05초간-반전-유지-후-재반전)
		- [**Count, Interval 간의 상관관계**](#count-interval-간의-상관관계)
		- [**Count 기능**](#count-기능)
		- [Example: 이벤트 발생이 3회이상 발생시 릴레이 R01 On](#example-이벤트-발생이-3회이상-발생시-릴레이-r01-on)
		- [Example: 이벤트 발생이 10회이상 발생시 릴레이 R01 반전](#example-이벤트-발생이-10회이상-발생시-릴레이-r01-반전)
		- [**Interval 기능**](#interval-기능)
		- [Example:  이벤트 발생이 1초이상 연속으로 발생시 릴레이 R01 On](#example--이벤트-발생이-1초이상-연속으로-발생시-릴레이-r01-on)
		- [Example:  이벤트 발생이 10초이상 연속으로 발생시 릴레이 R01 반전](#example--이벤트-발생이-10초이상-연속으로-발생시-릴레이-r01-반전)
		- [**Count 와 Interval 조합 기능**](#count-와-interval-조합-기능)
		- [Example:  이벤트 발생이 1초이내에 연속으로 3회이상 발생시 릴레이 R01 On](#example--이벤트-발생이-1초이내에-연속으로-3회이상-발생시-릴레이-r01-on)
	- [**Audio**](#audio)
		- [**Format**](#format-3)
		- [**Audio System**](#audio-system)
		- [Example: 사전정의된 음원 4번을 40%의 볼륨으로 플레이 요청](#example-사전정의된-음원-4번을-40의-볼륨으로-플레이-요청)
		- [Example: 사용자 오디오 Warning을 100%의 볼륨으로 10번 재생 요청](#example-사용자-오디오-warning을-100의-볼륨으로-10번-재생-요청)
		- [Example: 웹 오디오 nocturne을 70%의 볼륨으로 2번 플레이 요청](#example-웹-오디오-nocturne을-70의-볼륨으로-2번-플레이-요청)
	- [**Talk**](#talk)
		- [**Format**](#format-4)
		- [Example: speaking](#example-speaking)
		- [Example: listening](#example-listening)
		- [Example: disconnect](#example-disconnect)
	- [**Camera**](#camera)
		- [**Format**](#format-5)
		- [Footprint(Blackbox) System](#footprintblackbox-system)
		- [Example: Camera footprint Test](#example-camera-footprint-test)
	- [**Trigger**](#trigger)
		- [**Format**](#format-6)
		- [Example: trigger](#example-trigger)
	- [**Messenger**](#messenger)
		- [**Format**](#format-7)
		- [SNS Messenger](#sns-messenger)
		- [Example: sendMessage](#example-sendmessage)
	- [**Custom**](#custom)
		- [**Format - tcp\_socket**](#format---tcp_socket)
		- [Example: tcp\_sockert - JSON](#example-tcp_sockert---json)
		- [Example: tcp\_sockert - Non JSON](#example-tcp_sockert---non-json)
		- [Example: tcp\_sockert - Non JSON - IMS protocol](#example-tcp_sockert---non-json---ims-protocol)
		- [**Format - http\_get/http\_post**](#format---http_gethttp_post)
		- [Example: http\_get](#example-http_get)
		- [Example: http\_post](#example-http_post)
	- [**System**](#system)
		- [**Format**](#format-8)
		- [Example: sleep](#example-sleep)
		- [Example: get\_name](#example-get_name)
		- [Example: set\_name](#example-set_name)
		- [Example: get\_time](#example-get_time)
		- [Example: set\_time](#example-set_time)
		- [Example: list\_audio](#example-list_audio)
		- [Example: stop\_audio](#example-stop_audio)
		- [Example: enable\_audio](#example-enable_audio)
		- [Example: disable\_audio](#example-disable_audio)
		- [Example: trigger\_io](#example-trigger_io)
		- [Example: health\_check](#example-health_check)
		- [Example: enable\_io](#example-enable_io)
		- [Example: disable\_io](#example-disable_io)
		- [Example: restart](#example-restart)
		- [Example: reboot](#example-reboot)
	- [**Debug**](#debug)
		- [Example: Debug](#example-debug)
	- [**KeyCode**](#keycode)
		- [Example: KeyCode](#example-keycode)
	- [**Complexed Script**](#complexed-script)
		- [Example: 이벤트 발생시 릴레이 n초 대기 후 Toggle](#example-이벤트-발생시-릴레이-n초-대기-후-toggle)
		- [Example: 이벤트 발생시 릴레이(R01), 릴레이(R02) 동시 반전, n초 후 복귀](#example-이벤트-발생시-릴레이r01-릴레이r02-동시-반전-n초-후-복귀)
		- [Example: 이벤트 발생시 릴레이(R01) 반전, n초 후 릴레이(R02) 반전](#example-이벤트-발생시-릴레이r01-반전-n초-후-릴레이r02-반전)
		- [Example: 단일 이벤트 릴레이(R01, R0, R03, R04) 전체 반전](#example-단일-이벤트-릴레이r01-r0-r03-r04-전체-반전)
		- [Example: 재생되는 오디오를 n초후, 정지시키고 새 음원 재생](#example-재생되는-오디오를-n초후-정지시키고-새-음원-재생)
		- [Example: 재생되는 오디오를 즉시 정지시키고 새 음원 재생(**비상경보**)](#example-재생되는-오디오를-즉시-정지시키고-새-음원-재생비상경보)
	- [**Server**](#server)
		- [**Format**](#format-9)
		- [Example: Server](#example-server)
		- [Example: CLI Test](#example-cli-test)
		- [Example: CLI vs Inline vs URI](#example-cli-vs-inline-vs-uri)
	- [**Scheduler(Crontab)**](#schedulercrontab)
		- [Example: Scheduler Time Set](#example-scheduler-time-set)
	- [**Timer(Threading)**](#timerthreading)
	- [**Log**](#log)
	- [**Database Query**](#database-query)
- [Programming Examples](#programming-examples)
	- [python Code Example - **pyCode.py**](#python-code-example---pycodepy)
	- [PHP Code Example - **phpCode.php**](#php-code-example---phpcodephp)
<div style="page-break-after: always"></div>

ITS API는 Console(http://API_IP:28080)을 통해 관리된다.

인라인 명령(Inline command)이나 코멘드라인인터프리터(CLI) 또는 브라우저(URI)로 테스트 및 제어가 가능하다.
<div style="page-break-after: always"></div>

# FORMATS
기본적으로 ITS API는 3가지 형식의 이벤트에 대응한다.

## **이벤트 발생**
센서, 스케즐러, 타이머에 따른 이벤트가 발생된다. 

### **센서 이벤트**
- 8개의 Sensor : Dry Contact 신호기반
> **IO Table**
> |Sensor|S01|S02|S03|S04|S05|S06|S07|S08|
> |:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
> |ID|io01|io02|io03|io04|io05|io06|io07|io08|

### **스케즐러 이벤트**
- 4개의 Crontab : Linux Crontab 기반
> **Scheduler Table**
> |Cron|C01|C02|C03|C04|
> |:----:|:----:|:----:|:----:|:----:|
> |ID|am01|am02|am03|am04|

### **타이머 이벤트**
- 1개의 Heartbeat : Linux Timer 기반
  - Heartbeat
  
사용자는 이벤트 발생시 관련 항목에 JSON 형식의 명령문 요청이 가능한데 이러한 명령문을 ITS 액션스크립트(ITS Action Script)라 한다.
<div style="page-break-after: always"></div>

## **Action Script**

### **Format**
딕셔너리 형식의 JSON으로 구성은 host, port, data 이다.
```
{ 
	"host":"", 
	"port":"", 
	"data": [ { command }, ... ] 
}
```
- hos(Option)t, port(Option) : Master Server
  - "data"내의 명령이 실행될 원격 IP 및 Port이며 미설정시 자신에게 요청한다.
  - ITS API port는 34001로 고정이다.
- data : Command List
  - 배열(list[ ])로 구성되며 명령문의 집합체 이다.

### **data**
리스트 형식의 JSON으로 다양한 명령문의 배열이다.
```
{ 
	"data": [
		{ command },
		{ command },
		...
	] 
}
```
<div style="page-break-after: always"></div>

### **command**
gpio, audio, camera, messenger, custom, system ...
```
{ 
	"data": [
		{
			"command": { 
				"name": value,
				...
			},
			...
		}
	] 
}

{ 
	"data": [
		{ 
			"command": { "name": value, ... }
		}
	] 
}
```
<div style="page-break-after: always"></div>

### **options**
server, keycode, debug
```
{ 
	"data": [
		{ 
			"command": { "name": value, ... }, 
			"server": { host:addr, port:no. }, 
			"keyCode": sha256, 
			"debug": true / false
		}
	] 
}
```
- server(Option) : remote IP and Port
  - Command단위 명령을 원격(IP:Port)으로 실행 요청한는 기능이다.
  - server": { "host":"192.168.0.100","port":"34001" }
- keyCode(Option) : keySource
  - 설정: API > Setup > API Key > keySource 값이 설정 되어 있으면 요청되는 모든 명령문에 API > Setup > API Key > keyCode(License) 값이 동반되어야 하며 그 값이 일치되어야만 명령이 실행된다.
- debug(Option) : true / false
  - 오류검증이 필요할때 사용되며 참이면 실행에 따른 결과를 반환한다.
<div style="page-break-after: always"></div>

## **복합명령(Complexed Action Script)**
단일명령을 콤마로 구분하여 복수의 명령을 동시에 요청할수 있다.

명령문수는 이론적으로 무제한으로 복수명령문의 실행 순서는 정열순으로 진행된다.

각각의 명령문은 subprocess 및 threading 기반으로 실행되어 이미 요청된 명령은 사용자및 시스템으로 부터 독립적으로 행동한다.

### **Format**
```
{ 
	"data": [
		{ command_01 },
		{ command_02 },
		{ command_03 },
		...
	] 
}
```
<div style="page-break-after: always"></div>

# Commands
릴레이제어(GPIO), 방송(Audio), 스넵샷(Camera), 대화(Talk), 문자메시지(Messenger), 네트워크통신(Custom), 시스템제어(System), 원격실행(Server), 디버그(Debug)모드등 다양한 기능을 포함한다.

특히 해시코드를 통한 보안키(KeyCode)명령과 센서전원제어, 핼스체크 및 하트비트 발생기능또한 포함한다.
<div style="page-break-after: always"></div>

## **GPIO**
ITS Device는 4개의 Relay Out과 1개의 12v 전원을 제어 한다.
> **Table**
> |Relay|R01|R02|R03|R04|
> |:----:|:----:|:----:|:----:|:----:|
> |ID|io09|io10|io11|io12|
> 
> |Power|P01|
> |:----:|:----:|
> |ID|pw01|

### **Format**
```
{
	"data":[
	{
		"gpio":{
			"status":"status",
			"id":"id",
			"hold":"Second",
			"count":"Number",
			"interval":"Second"
		}
	}
}
```
- status :
	- '0:Off', '1:On', '2:Toggle', '3:Status', '7:Status Power', '8:Status Relay and Sensor', '9:Status All'
- id : Relay ID
  - Table 참조
- hold (float) : 
  - 대기시간 후 반전
  - 0인 경우 상태 유지
- count (int) :
  - 센서이벤트(감지) 횟수
- interval (float) :
  - 센서이벤트(감지) 대기시간
<div style="page-break-after: always"></div>

### **Hold**
Hold는 출력단(Relay)의 기능이다.
  - 요청된 상태를 Hold 시간만큼 유지한후 반전 한다.
  - 0초로 선언된 경우엔 요청된 상태를 그대로 유지한다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="601px" viewBox="-0.5 -0.5 601 181" content="&lt;mxfile&gt;&lt;diagram id=&quot;rdKp0REcOZbG9A3bbCPo&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;1538&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;7&quot; style=&quot;edgeStyle=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; parent=&quot;1&quot; source=&quot;2&quot; target=&quot;4&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;2&quot; value=&quot;ON&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#000000;fontColor=#F0F0F0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;190&quot; y=&quot;40&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;6&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;3&quot; target=&quot;2&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;3&quot; value=&quot;Off&amp;lt;br&amp;gt;Hold = 0&quot; style=&quot;shape=step;perimeter=stepPerimeter;whiteSpace=wrap;html=1;fixedSize=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;45&quot; width=&quot;110&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;8&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;4&quot; target=&quot;5&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;4&quot; value=&quot;OFF&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;310&quot; y=&quot;40&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;9&quot; style=&quot;edgeStyle=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; parent=&quot;1&quot; source=&quot;5&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;530&quot; y=&quot;65&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;5&quot; value=&quot;OFF&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;420&quot; y=&quot;40&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;10&quot; style=&quot;edgeStyle=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; parent=&quot;1&quot; source=&quot;11&quot; target=&quot;15&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;11&quot; value=&quot;ON&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#000000;fontColor=#F0F0F0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;190&quot; y=&quot;115&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;12&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;13&quot; target=&quot;11&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;13&quot; value=&quot;Off&amp;lt;br&amp;gt;Hold = 2&quot; style=&quot;shape=step;perimeter=stepPerimeter;whiteSpace=wrap;html=1;fixedSize=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;120&quot; width=&quot;110&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;14&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;15&quot; target=&quot;17&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;15&quot; value=&quot;OFF&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;310&quot; y=&quot;115&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;16&quot; style=&quot;edgeStyle=none;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; parent=&quot;1&quot; source=&quot;17&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;530&quot; y=&quot;140&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;17&quot; value=&quot;OFF&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;420&quot; y=&quot;115&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;18&quot; value=&quot;OFF&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;530&quot; y=&quot;40&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;19&quot; value=&quot;ON&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#000000;fontColor=#F0F0F0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;530&quot; y=&quot;115&quot; width=&quot;50&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;24&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;20&quot; target=&quot;21&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;20&quot; value=&quot;1 Sec&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;360&quot; y=&quot;90&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;25&quot; style=&quot;edgeStyle=none;html=1;&quot; parent=&quot;1&quot; source=&quot;21&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;590&quot; y=&quot;105&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;21&quot; value=&quot;2 Sec&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;470&quot; y=&quot;90&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;23&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;22&quot; target=&quot;20&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;22&quot; value=&quot;0 Sec&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;250&quot; y=&quot;90&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;26&quot; value=&quot;Event Action&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry width=&quot;600&quot; height=&quot;180&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:181px;"><defs/><g><path d="M 240 65 L 303.63 65" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 308.88 65 L 301.88 68.5 L 303.63 65 L 301.88 61.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="215" cy="65" rx="25" ry="25" fill="#000000" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 65px; margin-left: 191px;"><div data-drawio-colors="color: #F0F0F0; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(240, 240, 240); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ON</div></div></div></foreignObject><text x="215" y="69" fill="#F0F0F0" font-family="Helvetica" font-size="12px" text-anchor="middle">ON</text></switch></g><path d="M 130 65 L 183.63 65" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 188.88 65 L 181.88 68.5 L 183.63 65 L 181.88 61.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 20 45 L 110 45 L 130 65 L 110 85 L 20 85 L 40 65 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 108px; height: 1px; padding-top: 65px; margin-left: 21px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Off<br />Hold = 0</div></div></div></foreignObject><text x="75" y="69" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Off...</text></switch></g><path d="M 360 65 L 413.63 65" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 418.88 65 L 411.88 68.5 L 413.63 65 L 411.88 61.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="335" cy="65" rx="25" ry="25" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 65px; margin-left: 311px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">OFF</div></div></div></foreignObject><text x="335" y="69" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">OFF</text></switch></g><path d="M 470 65 L 523.63 65" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 528.88 65 L 521.88 68.5 L 523.63 65 L 521.88 61.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="445" cy="65" rx="25" ry="25" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 65px; margin-left: 421px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">OFF</div></div></div></foreignObject><text x="445" y="69" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">OFF</text></switch></g><path d="M 240 140 L 303.63 140" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 308.88 140 L 301.88 143.5 L 303.63 140 L 301.88 136.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="215" cy="140" rx="25" ry="25" fill="#000000" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 140px; margin-left: 191px;"><div data-drawio-colors="color: #F0F0F0; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(240, 240, 240); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ON</div></div></div></foreignObject><text x="215" y="144" fill="#F0F0F0" font-family="Helvetica" font-size="12px" text-anchor="middle">ON</text></switch></g><path d="M 130 140 L 183.63 140" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 188.88 140 L 181.88 143.5 L 183.63 140 L 181.88 136.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 20 120 L 110 120 L 130 140 L 110 160 L 20 160 L 40 140 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 108px; height: 1px; padding-top: 140px; margin-left: 21px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Off<br />Hold = 2</div></div></div></foreignObject><text x="75" y="144" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Off...</text></switch></g><path d="M 360 140 L 413.63 140" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 418.88 140 L 411.88 143.5 L 413.63 140 L 411.88 136.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="335" cy="140" rx="25" ry="25" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 140px; margin-left: 311px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">OFF</div></div></div></foreignObject><text x="335" y="144" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">OFF</text></switch></g><path d="M 470 140 L 523.63 140" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 528.88 140 L 521.88 143.5 L 523.63 140 L 521.88 136.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="445" cy="140" rx="25" ry="25" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 140px; margin-left: 421px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">OFF</div></div></div></foreignObject><text x="445" y="144" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">OFF</text></switch></g><ellipse cx="555" cy="65" rx="25" ry="25" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 65px; margin-left: 531px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">OFF</div></div></div></foreignObject><text x="555" y="69" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">OFF</text></switch></g><ellipse cx="555" cy="140" rx="25" ry="25" fill="#000000" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 140px; margin-left: 531px;"><div data-drawio-colors="color: #F0F0F0; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(240, 240, 240); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ON</div></div></div></foreignObject><text x="555" y="144" fill="#F0F0F0" font-family="Helvetica" font-size="12px" text-anchor="middle">ON</text></switch></g><path d="M 420 105 L 463.63 105" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 468.88 105 L 461.88 108.5 L 463.63 105 L 461.88 101.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="360" y="90" width="60" height="30" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 105px; margin-left: 361px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">1 Sec</div></div></div></foreignObject><text x="390" y="109" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">1 Sec</text></switch></g><path d="M 530 105 L 583.63 105" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 588.88 105 L 581.88 108.5 L 583.63 105 L 581.88 101.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="470" y="90" width="60" height="30" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 105px; margin-left: 471px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">2 Sec</div></div></div></foreignObject><text x="500" y="109" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">2 Sec</text></switch></g><path d="M 310 105 L 353.63 105" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 358.88 105 L 351.88 108.5 L 353.63 105 L 351.88 101.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="250" y="90" width="60" height="30" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 105px; margin-left: 251px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">0 Sec</div></div></div></foreignObject><text x="280" y="109" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">0 Sec</text></switch></g><path d="M 0 23 L 0 0 L 600 0 L 600 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 0 23 L 0 180 L 600 180 L 600 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 600 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="299.5" y="16">Event Action</text></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

### Example: 이벤트 발생시 릴레이 R01 Off
```
{
	"data":[
		{
			"gpio":{
				"status":"0",
				"id":"io09",
				"hold":"0"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"0","id":"io09","hold":"0"}}]
```

### Example: 이벤트 발생시 릴레이 R01 On
```
{
	"data":[
		{
			"gpio":{
				"status":"1",
				"id":"io09",
				"hold":"0"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"1","id":"io09","hold":"0"}}]
```
<div style="page-break-after: always"></div>

### Example: 이벤트 발생시 릴레이 R01 Toggle(즉각반응)
```
{
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0"}}]
```

### Example: 이벤트 발생시 릴레이 R01 1.5초간 On 후 Off
```
{
	"data":[
		{
			"gpio":{
				"status":"1",
				"id":"io09",
				"hold":"1.5"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"0","id":"io09","hold":"1.5"}}]
```
<div style="page-break-after: always"></div>

### Example: 이벤트 발생시 릴레이 R01 0.5초간 반전 유지 후 재반전
```
{
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0.5"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0.5"}}]
```
<div style="page-break-after: always"></div>

### **Count, Interval 간의 상관관계**
카운터와 인터벌은 입력단의 기능이다.
- A: 일반적으로 센서에서 감지신호가 오면 감지 유무에 따라 명령을 실행한다.
- B: Count(횟수)가 선언되면
  - 선언된 횟수 이상의 신호가 들어올 경우 명령을 실행한다.
  - 이후 카운터는 리셋된다.
- C: Interval(시간)이 선언되면
  - 감지되는 신호를 선언된 시간까지 무시하고 선언시간을 넘긴 신호가 감지될때 명령을 실행한다.
  - 이후 인터벌은 리셋된다.
- D: Count와 Interval이 같이 선언되면
  - Interval 시간안에 Count 횟수를 넘기면 남은 인터벌 시간동안 매 회 명령을 실행한다.
  - 인터벌을 주기로 카운터는 리셋된다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="661px" viewBox="-0.5 -0.5 661 371" content="&lt;mxfile&gt;&lt;diagram id=&quot;nyVjmS6cdddfDmABYKn2&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;1466&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; background=&quot;#FFFFFF&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;24&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;36&quot; target=&quot;35&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;595&quot; y=&quot;222&quot; as=&quot;sourcePoint&quot;/&gt;&lt;mxPoint x=&quot;595&quot; y=&quot;252&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;25&quot; style=&quot;edgeStyle=none;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;36&quot; target=&quot;28&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;715&quot; y=&quot;172&quot; as=&quot;targetPoint&quot;/&gt;&lt;mxPoint x=&quot;680&quot; y=&quot;172&quot; as=&quot;sourcePoint&quot;/&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;705&quot; y=&quot;167&quot;/&gt;&lt;mxPoint x=&quot;705&quot; y=&quot;67&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;27&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;28&quot; target=&quot;36&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;595&quot; y=&quot;132&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;28&quot; value=&quot;SENSOR&amp;lt;br&amp;gt;D&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;557.5&quot; y=&quot;42&quot; width=&quot;75&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;30&quot; value=&quot;RELAY&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;555&quot; y=&quot;372&quot; width=&quot;80&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;37&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;35&quot; target=&quot;30&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;35&quot; value=&quot;EVENT_SUM&amp;amp;nbsp; &amp;amp;gt; COUNT&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#FFFFFF;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;530&quot; y=&quot;222&quot; width=&quot;130&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;36&quot; value=&quot;TIME&amp;amp;nbsp;&amp;amp;gt; INTERVAL&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#FFFFFF;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;530&quot; y=&quot;137&quot; width=&quot;130&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;40&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;48&quot; target=&quot;45&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;215&quot; y=&quot;222&quot; as=&quot;sourcePoint&quot;/&gt;&lt;mxPoint x=&quot;215&quot; y=&quot;242&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;41&quot; style=&quot;edgeStyle=none;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;48&quot; target=&quot;43&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;335&quot; y=&quot;172&quot; as=&quot;targetPoint&quot;/&gt;&lt;mxPoint x=&quot;300&quot; y=&quot;172&quot; as=&quot;sourcePoint&quot;/&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;325&quot; y=&quot;167&quot;/&gt;&lt;mxPoint x=&quot;325&quot; y=&quot;67&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;42&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;43&quot; target=&quot;48&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;215&quot; y=&quot;132&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;43&quot; value=&quot;SENSOR&amp;lt;br&amp;gt;B&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;177.5&quot; y=&quot;42&quot; width=&quot;75&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;44&quot; value=&quot;Reset COUNT&quot; style=&quot;text;html=1;strokeColor=none;fillColor=#F0F0F0;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;shadow=0;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;162.5&quot; y=&quot;232&quot; width=&quot;105&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;45&quot; value=&quot;RELAY&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;175&quot; y=&quot;372&quot; width=&quot;80&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;48&quot; value=&quot;&amp;lt;span&amp;gt;EVENT_&amp;lt;/span&amp;gt;SUM&amp;amp;nbsp; &amp;amp;gt; COUNT&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#FFFFFF;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;150&quot; y=&quot;137&quot; width=&quot;130&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;53&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;54&quot; target=&quot;56&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;90&quot; y=&quot;137&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;54&quot; value=&quot;SENSOR&amp;lt;br&amp;gt;A&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;52.5&quot; y=&quot;42&quot; width=&quot;75&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;56&quot; value=&quot;RELAY&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;50&quot; y=&quot;372&quot; width=&quot;80&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;64&quot; style=&quot;edgeStyle=none;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;35&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;632.5&quot; y=&quot;67&quot; as=&quot;targetPoint&quot;/&gt;&lt;mxPoint x=&quot;650&quot; y=&quot;262&quot; as=&quot;sourcePoint&quot;/&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;705&quot; y=&quot;272&quot;/&gt;&lt;mxPoint x=&quot;705&quot; y=&quot;67&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;65&quot; value=&quot;No&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fontColor=#333333;shadow=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;650&quot; y=&quot;162&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;67&quot; value=&quot;No&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fontColor=#333333;shadow=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;650&quot; y=&quot;253&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;68&quot; value=&quot;No&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fontColor=#333333;shadow=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;270&quot; y=&quot;162&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;69&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;75&quot; target=&quot;74&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;405&quot; y=&quot;222&quot; as=&quot;sourcePoint&quot;/&gt;&lt;mxPoint x=&quot;405&quot; y=&quot;242&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;70&quot; style=&quot;edgeStyle=none;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;75&quot; target=&quot;72&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;525&quot; y=&quot;172&quot; as=&quot;targetPoint&quot;/&gt;&lt;mxPoint x=&quot;490&quot; y=&quot;172&quot; as=&quot;sourcePoint&quot;/&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;515&quot; y=&quot;167&quot;/&gt;&lt;mxPoint x=&quot;515&quot; y=&quot;67&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;71&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;rounded=1;curved=1;labelBorderColor=none;labelBackgroundColor=none;strokeColor=#000000;shadow=0;fillColor=none;fontColor=#333333;&quot; parent=&quot;1&quot; source=&quot;72&quot; target=&quot;75&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;405&quot; y=&quot;132&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;72&quot; value=&quot;SENSOR&amp;lt;br&amp;gt;C&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;367.5&quot; y=&quot;42&quot; width=&quot;75&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;74&quot; value=&quot;RELAY&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#CCCCCC;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;365&quot; y=&quot;372&quot; width=&quot;80&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;75&quot; value=&quot;TIME&amp;amp;nbsp;&amp;amp;gt; INTERVAL&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;labelBorderColor=none;labelBackgroundColor=none;fillColor=#FFFFFF;shadow=0;strokeColor=#000000;fontColor=#333333;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;340&quot; y=&quot;137&quot; width=&quot;130&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;76&quot; value=&quot;No&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;fontColor=#333333;shadow=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;460&quot; y=&quot;162&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;77&quot; value=&quot;Reset INTERVAL&quot; style=&quot;text;html=1;strokeColor=none;fillColor=#F0F0F0;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;shadow=0;fontColor=#333333;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;352.5&quot; y=&quot;232&quot; width=&quot;105&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;78&quot; value=&quot;Reset &amp;lt;br&amp;gt;COUNT&amp;amp;nbsp; &amp;amp;amp; INTERVAL&quot; style=&quot;text;html=1;strokeColor=none;fillColor=#F0F0F0;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;labelBorderColor=none;labelBackgroundColor=none;shadow=0;fontColor=#333333;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;542.5&quot; y=&quot;300&quot; width=&quot;105&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:371px;"><defs/><g><path d="M 545 155 Q 545 155 545 173.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 545 178.88 L 541.5 171.88 L 545 173.63 L 548.5 171.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 610 125 Q 655 125 655 75 Q 655 25 588.87 25" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 583.62 25 L 590.62 21.5 L 588.87 25 L 590.62 28.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 545 50 Q 545 50 545 88.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 545 93.88 L 541.5 86.88 L 545 88.63 L 548.5 86.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="545" cy="25" rx="37.5" ry="25" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 73px; height: 1px; padding-top: 25px; margin-left: 509px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">SENSOR<br />D</div></div></div></foreignObject><text x="545" y="29" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">SENSOR...</text></switch></g><rect x="505" y="330" width="80" height="40" rx="6" ry="6" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 78px; height: 1px; padding-top: 350px; margin-left: 506px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">RELAY</div></div></div></foreignObject><text x="545" y="354" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">RELAY</text></switch></g><path d="M 545 240 Q 545 240 545 323.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 545 328.88 L 541.5 321.88 L 545 323.63 L 548.5 321.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><rect x="480" y="180" width="130" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 210px; margin-left: 481px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">EVENT_SUM  &gt; COUNT</div></div></div></foreignObject><text x="545" y="214" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">EVENT_SUM  &gt; COUNT</text></switch></g><rect x="480" y="95" width="130" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 125px; margin-left: 481px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">TIME &gt; INTERVAL</div></div></div></foreignObject><text x="545" y="129" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">TIME &gt; INTERVAL</text></switch></g><path d="M 165 155 Q 165 155 165 323.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 165 328.88 L 161.5 321.88 L 165 323.63 L 168.5 321.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 230 125 Q 275 125 275 75 Q 275 25 208.87 25" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 203.62 25 L 210.62 21.5 L 208.87 25 L 210.62 28.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 165 50 Q 165 50 165 88.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 165 93.88 L 161.5 86.88 L 165 88.63 L 168.5 86.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="165" cy="25" rx="37.5" ry="25" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 73px; height: 1px; padding-top: 25px; margin-left: 129px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">SENSOR<br />B</div></div></div></foreignObject><text x="165" y="29" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">SENSOR...</text></switch></g><rect x="112.5" y="190" width="105" height="30" rx="4.5" ry="4.5" fill="#f0f0f0" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 103px; height: 1px; padding-top: 205px; margin-left: 114px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Reset COUNT</div></div></div></foreignObject><text x="165" y="209" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">Reset COUNT</text></switch></g><rect x="125" y="330" width="80" height="40" rx="6" ry="6" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 78px; height: 1px; padding-top: 350px; margin-left: 126px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">RELAY</div></div></div></foreignObject><text x="165" y="354" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">RELAY</text></switch></g><rect x="100" y="95" width="130" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 125px; margin-left: 101px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;"><span>EVENT_</span>SUM  &gt; COUNT</div></div></div></foreignObject><text x="165" y="129" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">EVENT_SUM  &gt; COUNT</text></switch></g><path d="M 40 50 Q 40 50 40 323.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 40 328.88 L 36.5 321.88 L 40 323.63 L 43.5 321.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="40" cy="25" rx="37.5" ry="25" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 73px; height: 1px; padding-top: 25px; margin-left: 4px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">SENSOR<br />A</div></div></div></foreignObject><text x="40" y="29" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">SENSOR...</text></switch></g><rect x="0" y="330" width="80" height="40" rx="6" ry="6" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 78px; height: 1px; padding-top: 350px; margin-left: 1px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">RELAY</div></div></div></foreignObject><text x="40" y="354" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">RELAY</text></switch></g><path d="M 610 210 Q 655 230 655 127.5 Q 655 25 588.87 25" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 583.62 25 L 590.62 21.5 L 588.87 25 L 590.62 28.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><rect x="600" y="120" width="60" height="30" rx="4.5" ry="4.5" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 135px; margin-left: 601px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">No</div></div></div></foreignObject><text x="630" y="139" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">No</text></switch></g><rect x="600" y="211" width="60" height="30" rx="4.5" ry="4.5" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 226px; margin-left: 601px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">No</div></div></div></foreignObject><text x="630" y="230" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">No</text></switch></g><rect x="220" y="120" width="60" height="30" rx="4.5" ry="4.5" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 135px; margin-left: 221px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">No</div></div></div></foreignObject><text x="250" y="139" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">No</text></switch></g><path d="M 355 155 Q 355 155 355 323.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 355 328.88 L 351.5 321.88 L 355 323.63 L 358.5 321.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 420 125 Q 465 125 465 75 Q 465 25 398.87 25" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 393.62 25 L 400.62 21.5 L 398.87 25 L 400.62 28.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 355 50 Q 355 50 355 88.63" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 355 93.88 L 351.5 86.88 L 355 88.63 L 358.5 86.88 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><ellipse cx="355" cy="25" rx="37.5" ry="25" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 73px; height: 1px; padding-top: 25px; margin-left: 319px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">SENSOR<br />C</div></div></div></foreignObject><text x="355" y="29" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">SENSOR...</text></switch></g><rect x="315" y="330" width="80" height="40" rx="6" ry="6" fill="#cccccc" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 78px; height: 1px; padding-top: 350px; margin-left: 316px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">RELAY</div></div></div></foreignObject><text x="355" y="354" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">RELAY</text></switch></g><rect x="290" y="95" width="130" height="60" rx="9" ry="9" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 125px; margin-left: 291px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">TIME &gt; INTERVAL</div></div></div></foreignObject><text x="355" y="129" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">TIME &gt; INTERVAL</text></switch></g><rect x="410" y="120" width="60" height="30" rx="4.5" ry="4.5" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 135px; margin-left: 411px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">No</div></div></div></foreignObject><text x="440" y="139" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">No</text></switch></g><rect x="302.5" y="190" width="105" height="30" rx="4.5" ry="4.5" fill="#f0f0f0" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 103px; height: 1px; padding-top: 205px; margin-left: 304px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Reset INTERVAL</div></div></div></foreignObject><text x="355" y="209" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">Reset INTERVAL</text></switch></g><rect x="492.5" y="258" width="105" height="50" rx="7.5" ry="7.5" fill="#f0f0f0" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 103px; height: 1px; padding-top: 283px; margin-left: 494px;"><div data-drawio-colors="color: #333333; " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(51, 51, 51); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Reset <br />COUNT  &amp; INTERVAL</div></div></div></foreignObject><text x="545" y="287" fill="#333333" font-family="Helvetica" font-size="12px" text-anchor="middle">Reset...</text></switch></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

### **Count 기능**
센서 이벤트 횟수가 설정값 이상일떄 명령실행

이벤트가 연속으로 감지될때는 카운터 설정값을 주기로 반복됨
### Example: 이벤트 발생이 3회이상 발생시 릴레이 R01 On
```
{
	"data":[
		{
			"gpio":{
				"status":"1",
				"id":"io09",
				"hold":"0",
				"count":"3"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"1","id":"io09","hold":"0","count":"3"}}]
```
### Example: 이벤트 발생이 10회이상 발생시 릴레이 R01 반전
```
{
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0",
				"count":"10"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0","count":"10"}}]
```
<div style="page-break-after: always"></div>

### **Interval 기능**
최초 이벤트 발생후 인터벌시간 이내에 이벤트는 무시되고 이후 발생시 명령실행

이벤트가 연속으로 감지될때는 인터벌 설정값을 주기로 반복됨

### Example:  이벤트 발생이 1초이상 연속으로 발생시 릴레이 R01 On
```
{
    "data": [
        {
            "gpio": {
                "status": "1",
                "id": "io09",
                "hold": "0",
                "interval": "1"
            }
        }
    ]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"1","id":"io09","hold":"0","interval":"1"}}]
```
### Example:  이벤트 발생이 10초이상 연속으로 발생시 릴레이 R01 반전
```
{
    "data": [
        {
            "gpio": {
                "status": "2",
                "id": "io09",
                "hold": "0",
                "interval": "10"
            }
        }
    ]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0","interval":"10"}}]
```
<div style="page-break-after: always"></div>

### **Count 와 Interval 조합 기능**

인터벌 시간이내 카운터 설정값 이상 감지시 명령실행 

이때 명령실행은 인터벌 종료시간 까지 매 회 발생

인터벌이 종료 되면 카운터도 초기화됨

### Example:  이벤트 발생이 1초이내에 연속으로 3회이상 발생시 릴레이 R01 On
```
{
    "data": [
        {
            "gpio": {
                "status": "1",
                "id": "io09",
                "hold": "0",
				"count":"3",
                "interval": "1"
            }
        }
    ]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"1","id":"io09","hold":"0","count":"3","interval":"1"}}]
```

> Count나 Interval만 선언된 경우 각각의 설정값을 주기로 명령이 실행되지만 Count와 Interval이 동시에 설정된경우 종료시간 까지 연속적으로 명령이 실행된다.
<div style="page-break-after: always"></div>

## **Audio**
ITS Device Audio 제어 한다.
- 방송중 연속적인 재생 요청은 무시된다. 
- 제공되는 오디오 플레이어는 omxplayer과 mplayer이 있다.
- 플레이어 특성에 따라 볼륨레벨이 다를 수 있다.
- omxplayer 선택시 반복(loop)기능은 무시된다.
- mplayer는 omxplayer보다 재생 직전 초기화 시간이 길다.
- 플레이어에 따라 불륨레벨에 차이도 참고 해야한다.
- 음원은 사전정의된 순서로 재생 가능한 음원과 사용자 업로드 재생 기능이 있다.
- 설정: API > Config > File Manager > Audio Manager
- 사용자 업로드 한 음원을 이웃하는 ITS API(**server 기능** 참조)로 재생시 네트워크 복사후 재생된다.
### **Format**
```
{
	"data":[
		{
			"audio":{
				"source":"Internal(No./Full Path), External(URI)",
				"volume":"volume(%): 0 - 100",
				"loop":"0 ~ Int"
			}
		}
	]
}
```
- source: Internal(No/Full Path), External(URI)
- volume(%): 0 - 100
- loop: 0 ~ Int.
<div style="page-break-after: always"></div>

### **Audio System**
모든 오디오형식은 MP3이다.
- Internal Audio : 빠른 응답속도
  - 사전에 등록된 음원으로 번호로 호출 가능 하다.
  - 환경설정(Config > File Manager > Audio Manager)을 통해 검색 및 등록 가능 하다.
  - 순서는 등록된 파일명의 정렬순이다.
- User Audio : 음원에 따라 재생시간 지연가능
  - 사용자가 업로드한 오디오의 전체경로(Full Path)를 지정해야 한다.
- URL Audio
  - 네트워크(또는 웹)상에 있는 오디오파일의 URL을 지정해야 한다.
- Network Audio : 재생 속도가 상대적으로 느림
  - 이웃하는 스피커로 오디오 재생이 필요할때 관련 디바이스로 명령문 전송이 가능하다.
  - 이는 브로드캐스팅 기능으로 재생속도를 감안해 Internal Audio 재생을 권장 한다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="581px" viewBox="-0.5 -0.5 581 351" content="&lt;mxfile&gt;&lt;diagram id=&quot;dnKfnCRTLss6fdz7es3q&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;1538&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;21&quot; value=&quot;&quot; style=&quot;ellipse;shape=cloud;whiteSpace=wrap;html=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;230&quot; y=&quot;212&quot; width=&quot;360&quot; height=&quot;140&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;14&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; target=&quot;2&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;200&quot; y=&quot;135&quot; as=&quot;sourcePoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;6&quot; value=&quot;&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;40&quot; y=&quot;60&quot; width=&quot;160&quot; height=&quot;220&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;15&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;2&quot; target=&quot;12&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;20&quot; style=&quot;edgeStyle=none;html=1;entryX=0.4;entryY=0.1;entryDx=0;entryDy=0;entryPerimeter=0;sketch=0;dashed=1;&quot; parent=&quot;1&quot; source=&quot;2&quot; target=&quot;21&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;2&quot; value=&quot;ITS API&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;250&quot; y=&quot;105&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;3&quot; value=&quot;URL Audio&quot; style=&quot;ellipse;shape=cloud;whiteSpace=wrap;html=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;50&quot; y=&quot;200&quot; width=&quot;140&quot; height=&quot;70&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;4&quot; value=&quot;User Audio&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;60&quot; y=&quot;140&quot; width=&quot;120&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;5&quot; value=&quot;Internal&amp;lt;br&amp;gt;Audio&quot; style=&quot;shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;60&quot; y=&quot;80&quot; width=&quot;120&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;7&quot; value=&quot;Audio Sources&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;90&quot; y=&quot;290&quot; width=&quot;60&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;12&quot; value=&quot;Audio Out&quot; style=&quot;html=1;whiteSpace=wrap;container=1;recursiveResize=0;collapsible=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;420&quot; y=&quot;100&quot; width=&quot;150&quot; height=&quot;70&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;13&quot; value=&quot;&quot; style=&quot;triangle;html=1;whiteSpace=wrap;&quot; parent=&quot;12&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;20&quot; width=&quot;20&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;16&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;1&quot; source=&quot;17&quot; target=&quot;18&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;17&quot; value=&quot;ITS API&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;300&quot; y=&quot;260&quot; width=&quot;90&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;18&quot; value=&quot;Audio Out&quot; style=&quot;html=1;whiteSpace=wrap;container=1;recursiveResize=0;collapsible=0;align=right;spacingRight=11;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;420&quot; y=&quot;255&quot; width=&quot;110&quot; height=&quot;55&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;19&quot; value=&quot;&quot; style=&quot;triangle;html=1;whiteSpace=wrap;&quot; parent=&quot;18&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;17&quot; y=&quot;18&quot; width=&quot;10&quot; height=&quot;20&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;22&quot; value=&quot;Network Audio&amp;amp;nbsp;&quot; style=&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;375&quot; y=&quot;310&quot; width=&quot;90&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;23&quot; value=&quot;Event Action&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;20&quot; width=&quot;580&quot; height=&quot;350&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:351px;"><defs/><g><path d="M 300 227 C 228 227 210 262 267.6 269 C 210 284.4 274.8 318 321.6 304 C 354 332 462 332 498 304 C 570 304 570 276 525 262 C 570 234 498 206 435 220 C 390 199 318 199 300 227 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 180 115 L 223.63 115" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 228.88 115 L 221.88 118.5 L 223.63 115 L 221.88 111.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="20" y="40" width="160" height="220" rx="24" ry="24" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><path d="M 350 115 L 393.63 115" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 398.88 115 L 391.88 118.5 L 393.63 115 L 391.88 111.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 311.1 145 L 350.34 200.79" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" stroke-dasharray="3 3" pointer-events="stroke"/><path d="M 353.36 205.09 L 346.47 201.37 L 350.34 200.79 L 352.19 197.35 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="230" y="85" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 115px; margin-left: 231px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ITS API</div></div></div></foreignObject><text x="290" y="119" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">ITS API</text></switch></g><path d="M 65 197.5 C 37 197.5 30 215 52.4 218.5 C 30 226.2 55.2 243 73.4 236 C 86 250 128 250 142 236 C 170 236 170 222 152.5 215 C 170 201 142 187 117.5 194 C 100 183.5 72 183.5 65 197.5 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 138px; height: 1px; padding-top: 215px; margin-left: 31px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">URL Audio</div></div></div></foreignObject><text x="100" y="219" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">URL Audio</text></switch></g><ellipse cx="100" cy="145" rx="60" ry="25" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 145px; margin-left: 41px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">User Audio</div></div></div></foreignObject><text x="100" y="149" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">User Audio</text></switch></g><path d="M 60 60 L 140 60 L 160 80 L 140 100 L 60 100 L 40 80 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 80px; margin-left: 41px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Internal<br />Audio</div></div></div></foreignObject><text x="100" y="84" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Internal...</text></switch></g><rect x="70" y="270" width="60" height="30" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 285px; margin-left: 71px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Audio Sources</div></div></div></foreignObject><text x="100" y="289" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Audio Sour...</text></switch></g><rect x="400" y="80" width="150" height="70" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 148px; height: 1px; padding-top: 115px; margin-left: 401px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Audio Out</div></div></div></foreignObject><text x="475" y="119" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Audio Out</text></switch></g><path d="M 420 100 L 440 115 L 420 130 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 370 261.5 L 393.64 262.29" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 398.88 262.46 L 391.77 265.73 L 393.64 262.29 L 392 258.73 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="280" y="240" width="90" height="40" rx="6" ry="6" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 88px; height: 1px; padding-top: 260px; margin-left: 281px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ITS API</div></div></div></foreignObject><text x="325" y="264" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">ITS API</text></switch></g><rect x="400" y="235" width="110" height="55" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe flex-end; width: 97px; height: 1px; padding-top: 263px; margin-left: 400px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: right;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Audio Out</div></div></div></foreignObject><text x="497" y="266" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="end">Audio Out</text></switch></g><path d="M 417 253 L 427 263 L 417 273 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><rect x="355" y="290" width="90" height="30" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 88px; height: 1px; padding-top: 305px; margin-left: 356px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">Network Audio </div></div></div></foreignObject><text x="400" y="309" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Network Audio </text></switch></g><path d="M 0 23 L 0 0 L 580 0 L 580 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 0 23 L 0 350 L 580 350 L 580 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 580 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="289.5" y="16">Event Action</text></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

### Example: 사전정의된 음원 4번을 40%의 볼륨으로 플레이 요청
```
{
	"data":[
		{
			"audio":{
				"source":"4",
				"volume":"40",
				"loop":"0"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"audio":{"source":"4","volume":"40","loop":"0"}}]
```

### Example: 사용자 오디오 Warning을 100%의 볼륨으로 10번 재생 요청
```
{
	"data":[
		{
			"audio":{
				"source":"./audio/Warning.mp3",
				"volume":"100",
				"loop":"10"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"audio":{"source":"./audio/Warning.mp3","volume":"100","loop":"10"}}]
```
<div style="page-break-after: always"></div>

### Example: 웹 오디오 nocturne을 70%의 볼륨으로 2번 플레이 요청
```
{
	"data":[
		{
			"audio":{
				"source":"https://www.mfiles.co.uk/mp3-downloads/chopin-nocturne-op9-no2.mp3",
				"volume":"70",
				"loop":"1"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"audio":{"source":"https://www.mfiles.co.uk/mp3-downloads/chopin-nocturne-op9-no2.mp3","volume":"70","loop":"1"}}]
```
<div style="page-break-after: always"></div>

## **Talk**
마이크를 통한 음성을 원격으로 실시간 전송하는 기능이다.
- 서버 클라이언트간 파이프라인(Redirection)을 연결하는 방식으로 1:n은 불가능하다.
- [speaking]과 [listening]을 개별 및 동시 실행이 가능하다
- 동시에 실행하는 경우 상대방과의 실시간 대화가 가능하게 된다.
- [speaking]은 마이크를 통한 자신의 음성을 원격으로 송신하는 방식이다.
- [listening]은 원격의 마이크를 구동시켜 음성을 수신하는 방식이다.
- [disconnect]는 실행되고 있는 [speaking] 또는 [listening]프로세서를 죽인다.
- 구동되는 processor 종류는 arecord, oggenc, sshpass, mplayer 이다.
- 종료는 threading기능을 이용해 버퍼링시간(3~4초)을 대기한 후 관련프로세서를 죽인다.
- 접속을 위한 클라이언트 IP는 환경설정을 통해 사전등록 되어야 한다.
### **Format**
```
{
	"data":[
		{
			"talk":{
				"command":"",
				"remoteIP":""
			}
		}
	]
}
```
- command :
  - speaking, listening, disconnect
- remoteIP : Target IP
### Example: speaking
Local System의 마이크를 통한 Audio Streamming을 원격으로 송신한다.
```
{
	"data":[
		{
			"talk":{
				"command":"speaking",
				"remoteIP":"ip_address"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"talk":{"command":"speaking","remoteIP":"192.168.0.2"},"debug":true}]
```

### Example: listening
Remote System의 마이크를 통한 Audio Streamming을 Local System으로 수신한다.
```
{
	"data":[
		{
			"talk":{
				"command":"listening",
				"remoteIP":"ip_address"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"talk":{"command":"listening","remoteIP":"192.168.0.2"},"debug":true}]
```
### Example: disconnect
실행되고있는 관련 프로세서를 죽인다.
```
{
	"data":[
		{
			"talk":{
				"command":"disconnect",
				"remoteIP":"ip_address"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"talk":{"command":"disconnect","remoteIP":"192.168.0.2"},"debug":true}]
```
<div style="page-break-after: always"></div>

## **Camera**
이벤트 발생시점을 기준으로 이전과 이후 영상을 저장하는 기능이다.(Blackbox)
- ITS microDVR(mDVR)과 연동
- 설정: API > Setup > Camera(mDVR)
- CCTV의 스트리밍을 일정량(maxCntPrev)의 스넵샷으로 저장하는 기능
- 스넵샷을 maxCntPrev 횟수까지 저장하는 주기는 환경에 따라 시간이 변동적이다.
- CCTV의 성능에 따라 저장속도나 크기가 가변적임으로 상황에 따른 튜닝이 필요하다.
- 이미지는 http://its.ip/mDVR/ 에 저장되며 확인 가능 하다.
- 스트리밍 프로토클은 Local Camera(/dev/video0) 외에 RTSP, AVI, MJPG가 가능 하다.
- 웹켐인 경우 기본 640 X 480 초당 20장 정도를 일반적으로 저장 한다.
- 현재 가능한 기능은 footprint(mDVR) 이다.
- 그외 still_shot, motion_shot(due_time), list_shot(interval, count), download_shot 기능은 추후 기능
### **Format**
```
{
	"data":[
		{
			"camera":{
				"command":"",
				"value":""
			}
		}
	]
}
```
- command :
  - footprint, still_shot, motion_shot, list_shot, download_shot
- value : Not Use(Current)
<div style="page-break-after: always"></div>

### Footprint(Blackbox) System
센서이벤트 발생 시점이전의 일정량(사전정의됨)과 시점이후의 일정량은 저장보관 하는 블랙박스 기능이다.
- Normal
  - 사전정의된 일정량의 스넵샷을 지속적으로 저장(FIFO)한다.
  - 설정량을 넘은 스냅샷을 버려서 설정량을 유지한다.
- Event
  - 센서이벤트 발생시 그 시점까지 저장된 스넵샷(cntPreShotMax:20)과 그 이후 일정시간(cntPostShotMax:10)의 스넵샷을 저장하는 기능이다.
  - 이기능은 이벤트 이전시점(cntPreShotMax) + 이벤트이후시간(cntPostShotMax) 동안 저장된 스넵 샷이다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="701px" viewBox="-0.5 -0.5 701 646" content="&lt;mxfile&gt;&lt;diagram id=&quot;bTc2n4uOvW-dyqWiW9PF&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;519&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;22&quot; value=&quot;Normal&quot; style=&quot;swimlane;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;130&quot; y=&quot;25&quot; width=&quot;500&quot; height=&quot;225&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;2&quot; value=&quot;&amp;lt;span style=&amp;quot;font-weight: 700&amp;quot;&amp;gt;Network&amp;lt;br&amp;gt;Camera&amp;lt;/span&amp;gt;&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; parent=&quot;22&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;50&quot; y=&quot;90&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;8&quot; value=&quot;CCTV&quot; style=&quot;swimlane;&quot; parent=&quot;22&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;40&quot; width=&quot;180&quot; height=&quot;140&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;10&quot; value=&quot;ITS API&quot; style=&quot;swimlane;&quot; parent=&quot;22&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;250&quot; y=&quot;40&quot; width=&quot;230&quot; height=&quot;160&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;5&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;10&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;40&quot; y=&quot;50&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;6&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;22&quot; source=&quot;2&quot; target=&quot;5&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;11&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;22&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;300&quot; y=&quot;100&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;12&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;22&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;310&quot; y=&quot;110&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;13&quot; value=&quot;Current&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;22&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;320&quot; y=&quot;120&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;23&quot; value=&quot;Event Action&quot; style=&quot;swimlane;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;130&quot; y=&quot;280&quot; width=&quot;700&quot; height=&quot;390&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle x=&quot;130&quot; y=&quot;310&quot; width=&quot;120&quot; height=&quot;23&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;15&quot; value=&quot;&amp;lt;span style=&amp;quot;font-weight: 700&amp;quot;&amp;gt;Network&amp;lt;br&amp;gt;Camera&amp;lt;/span&amp;gt;&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;50&quot; y=&quot;92.5&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;16&quot; value=&quot;CCTV&quot; style=&quot;swimlane;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;42.5&quot; width=&quot;180&quot; height=&quot;140&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;17&quot; value=&quot;ITS API&quot; style=&quot;swimlane;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;250&quot; y=&quot;42.5&quot; width=&quot;430&quot; height=&quot;327.5&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;24&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;17&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;250&quot; y=&quot;40&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;25&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;17&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;260&quot; y=&quot;50&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;26&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;17&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;270&quot; y=&quot;60&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;27&quot; value=&quot;Before&amp;lt;br&amp;gt;Alarm&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;17&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;280&quot; y=&quot;70&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;14&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; parent=&quot;23&quot; source=&quot;15&quot; target=&quot;20&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;290&quot; y=&quot;122.5&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;20&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;280&quot; y=&quot;92.5&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;34&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;&quot; parent=&quot;23&quot; source=&quot;21&quot; target=&quot;28&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;350&quot; y=&quot;200&quot;/&gt;&lt;mxPoint x=&quot;445&quot; y=&quot;200&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;21&quot; value=&quot;After&amp;lt;br&amp;gt;Alarm&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;290&quot; y=&quot;102.5&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;35&quot; style=&quot;edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;&quot; parent=&quot;23&quot; source=&quot;27&quot; target=&quot;28&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;590&quot; y=&quot;200&quot;/&gt;&lt;mxPoint x=&quot;445&quot; y=&quot;200&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;28&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;385&quot; y=&quot;240&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;29&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;395&quot; y=&quot;250&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;30&quot; value=&quot;Live&amp;lt;br&amp;gt;Shot&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;405&quot; y=&quot;260&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;31&quot; value=&quot;&amp;lt;span style=&amp;quot;font-weight: 700&amp;quot;&amp;gt;Footprint&amp;lt;/span&amp;gt;&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; parent=&quot;23&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;415&quot; y=&quot;270&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;36&quot; value=&quot;&quot; style=&quot;endArrow=classic;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; parent=&quot;23&quot; source=&quot;21&quot; target=&quot;24&quot; edge=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;415&quot; y=&quot;152.5&quot; as=&quot;sourcePoint&quot;/&gt;&lt;mxPoint x=&quot;515&quot; y=&quot;152.5&quot; as=&quot;targetPoint&quot;/&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;440&quot; y=&quot;133&quot;/&gt;&lt;mxPoint x=&quot;470&quot; y=&quot;123&quot;/&gt;&lt;mxPoint x=&quot;480&quot; y=&quot;113&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;37&quot; value=&quot;&amp;amp;nbsp;Alarm&quot; style=&quot;edgeLabel;resizable=0;html=1;align=center;verticalAlign=middle;&quot; parent=&quot;36&quot; connectable=&quot;0&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;38&quot; value=&quot;&amp;lt;span style=&amp;quot;font-weight: 700&amp;quot;&amp;gt;Footprint&amp;lt;/span&amp;gt;&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;555&quot; y=&quot;560&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;39&quot; value=&quot;&amp;lt;span style=&amp;quot;font-weight: 700&amp;quot;&amp;gt;Footprint&amp;lt;/span&amp;gt;&quot; style=&quot;shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;size=0.25;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;565&quot; y=&quot;570&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:646px;"><defs/><g><path d="M 0 23 L 0 0 L 500 0 L 500 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 0 23 L 0 225 L 500 225 L 500 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 500 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="249.5" y="16">Normal</text></g><rect x="50" y="90" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 120px; margin-left: 51px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;"><span style="font-weight: 700">Network<br />Camera</span></div></div></div></foreignObject><text x="110" y="124" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Network...</text></switch></g><path d="M 20 63 L 20 40 L 200 40 L 200 63" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 20 63 L 20 180 L 200 180 L 200 63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 20 63 L 200 63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="109.5" y="56">CCTV</text></g><path d="M 250 63 L 250 40 L 480 40 L 480 63" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 250 63 L 250 200 L 480 200 L 480 63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 250 63 L 480 63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="364.5" y="56">ITS API</text></g><rect x="290" y="90" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 320 90 L 320 150 M 380 90 L 380 150" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 120px; margin-left: 321px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="350" y="124" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><path d="M 170 120 L 283.63 120" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 288.88 120 L 281.88 123.5 L 283.63 120 L 281.88 116.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><rect x="300" y="100" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 330 100 L 330 160 M 390 100 L 390 160" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 130px; margin-left: 331px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="360" y="134" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="310" y="110" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 340 110 L 340 170 M 400 110 L 400 170" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 140px; margin-left: 341px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="370" y="144" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="320" y="120" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 350 120 L 350 180 M 410 120 L 410 180" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 150px; margin-left: 351px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Current<br />Shot</div></div></div></foreignObject><text x="380" y="154" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Current...</text></switch></g><path d="M 0 278 L 0 255 L 700 255 L 700 278" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 278 L 0 645 L 700 645 L 700 278" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 278 L 700 278" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="349.5" y="271">Event Action</text></g><rect x="50" y="347.5" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 378px; margin-left: 51px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;"><span style="font-weight: 700">Network<br />Camera</span></div></div></div></foreignObject><text x="110" y="381" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Network...</text></switch></g><path d="M 20 320.5 L 20 297.5 L 200 297.5 L 200 320.5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 20 320.5 L 20 437.5 L 200 437.5 L 200 320.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 20 320.5 L 200 320.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="109.5" y="313.5">CCTV</text></g><path d="M 250 320.5 L 250 297.5 L 680 297.5 L 680 320.5" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 250 320.5 L 250 625 L 680 625 L 680 320.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 250 320.5 L 680 320.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="464.5" y="313.5">ITS API</text></g><rect x="500" y="337.5" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 530 337.5 L 530 397.5 M 590 337.5 L 590 397.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 368px; margin-left: 531px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="560" y="371" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="510" y="347.5" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 540 347.5 L 540 407.5 M 600 347.5 L 600 407.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 378px; margin-left: 541px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="570" y="381" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="520" y="357.5" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 550 357.5 L 550 417.5 M 610 357.5 L 610 417.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 388px; margin-left: 551px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="580" y="391" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="530" y="367.5" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 560 367.5 L 560 427.5 M 620 367.5 L 620 427.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 398px; margin-left: 561px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Before<br />Alarm</div></div></div></foreignObject><text x="590" y="401" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Before...</text></switch></g><path d="M 170 377.5 L 273.63 377.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 278.88 377.5 L 271.88 381 L 273.63 377.5 L 271.88 374 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><rect x="280" y="347.5" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 310 347.5 L 310 407.5 M 370 347.5 L 370 407.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 378px; margin-left: 311px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="340" y="381" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><path d="M 350 417.5 L 350 445 Q 350 455 360 455 L 435 455 Q 445 455 445 465 L 445 488.63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 445 493.88 L 441.5 486.88 L 445 488.63 L 448.5 486.88 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><rect x="290" y="357.5" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 320 357.5 L 320 417.5 M 380 357.5 L 380 417.5" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 388px; margin-left: 321px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">After<br />Alarm</div></div></div></foreignObject><text x="350" y="391" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">After...</text></switch></g><path d="M 590 427.5 L 590 445 Q 590 455 580 455 L 455 455 Q 445 455 445 465 L 445 488.63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 445 493.88 L 441.5 486.88 L 445 488.63 L 448.5 486.88 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><rect x="385" y="495" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 415 495 L 415 555 M 475 495 L 475 555" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 525px; margin-left: 416px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="445" y="529" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="395" y="505" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 425 505 L 425 565 M 485 505 L 485 565" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 535px; margin-left: 426px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="455" y="539" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="405" y="515" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 435 515 L 435 575 M 495 515 L 495 575" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 545px; margin-left: 436px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Live<br />Shot</div></div></div></foreignObject><text x="465" y="549" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Live...</text></switch></g><rect x="415" y="525" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 445 525 L 445 585 M 505 525 L 505 585" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 555px; margin-left: 446px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;"><span style="font-weight: 700">Footprint</span></div></div></div></foreignObject><text x="475" y="559" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Footprint</text></switch></g><path d="M 410 387.5 L 430 387.83 Q 440 388 449.49 384.84 L 460.51 381.16 Q 470 378 475 373 L 477.5 370.5 Q 480 368 486.82 367.83 L 493.63 367.66" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 498.88 367.53 L 491.97 371.2 L 493.63 367.66 L 491.8 364.2 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 383px; margin-left: 458px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; background-color: rgb(255, 255, 255); white-space: nowrap;"> Alarm</div></div></div></foreignObject><text x="458" y="386" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Alarm</text></switch></g><rect x="425" y="535" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 455 535 L 455 595 M 515 535 L 515 595" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 565px; margin-left: 456px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;"><span style="font-weight: 700">Footprint</span></div></div></div></foreignObject><text x="485" y="569" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Footprint</text></switch></g><rect x="435" y="545" width="120" height="60" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 465 545 L 465 605 M 525 545 L 525 605" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 575px; margin-left: 466px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;"><span style="font-weight: 700">Footprint</span></div></div></div></foreignObject><text x="495" y="579" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Footprint</text></switch></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

### Example: Camera footprint Test
```
{
	"data":[
		{
			"camera":{
				"command":"footprint",
				"value":""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"camera":{"command":"footprint","value":""}}]
```
- 저장된 자료 조회경로: http://ip_address/mDVR 
<div style="page-break-after: always"></div>

## **Trigger**
인위적으로 센서포트를 트리거링 하는 기능이다.
- Soft Sensing (Hardware Event가 아닌 인라인 명령)
- 주의: Action Script 내에 자신을 Call하게되면 무한루프 오류 발생 우려
- System Command의 trigger_io와 유사한 기능
- No Reponse
### **Format**
```
{
	"data":[
		{
			"trigger":{
				"id":"Sensor ID"
			}
		}
	]
}
```
- Sensor ID: io01 ~ io08
	|Sensor|S01|S02|S03|S04|S05|S06|S07|S08|
	|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
	|ID|io01|io02|io03|io04|io05|io06|io07|io08|
<div style="page-break-after: always"></div>

### Example: trigger 
```
{
	"data":[
		{
			"trigger":{
				"id":"io02"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"trigger":{"id":"io02"},"debug":true}]
```
<div style="page-break-after: always"></div>

## **Messenger**
본서비스를 통해 관리영역의 감지이벤트를 ITS API를 통해 문자로 통보 받는다.
- 텔레그렘을 통한 SMS Report Service 사전작업
  - 설정: API > Telegram > Token, ChatID
  - Telegram Bot Token은 ITS API단에서 제공하는 키값
  - Group ChatID는 사용자가 만들어 제공해야하는 그룹ID
    - 취득방법: 관리자에게 문의

### **Format**
```
{
	"data":[
		{
			"messenger":{
				"sendMessage":"any Message"
			}
		}
	]
}
```
- sendMessage : 전송할 Message
<div style="page-break-after: always"></div>

### SNS Messenger
- 텔레그램
  
<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="641px" viewBox="-0.5 -0.5 641 331" content="&lt;mxfile&gt;&lt;diagram id=&quot;MiJx4strCP__x4ldr4Hv&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;1538&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;7&quot; value=&quot;Public IP&quot; style=&quot;edgeStyle=none;html=1;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;2&quot; target=&quot;6&quot;&gt;&lt;mxGeometry x=&quot;0.4&quot; relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint as=&quot;offset&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;2&quot; value=&quot;ITS API&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;520&quot; y=&quot;400&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;4&quot; value=&quot;&amp;amp;nbsp;Alarm&amp;amp;nbsp;&quot; style=&quot;endArrow=classic;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;21&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;420&quot; y=&quot;429.5&quot; as=&quot;sourcePoint&quot;/&gt;&lt;mxPoint x=&quot;520&quot; y=&quot;429.5&quot; as=&quot;targetPoint&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;19&quot; value=&quot;&amp;amp;nbsp;SNS&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;6&quot; target=&quot;9&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;20&quot; value=&quot;&amp;amp;nbsp;SNS&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;6&quot; target=&quot;14&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;6&quot; value=&quot;WEB&quot; style=&quot;ellipse;shape=cloud;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;520&quot; y=&quot;560&quot; width=&quot;120&quot; height=&quot;80&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;9&quot; value=&quot;Telegram Group&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;780&quot; y=&quot;420&quot; width=&quot;140&quot; height=&quot;120&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;10&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;9&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;40&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;11&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;820&quot; y=&quot;460&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;12&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;840&quot; y=&quot;460&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;13&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;860&quot; y=&quot;460&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;14&quot; value=&quot;Telegram Group&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;780&quot; y=&quot;570&quot; width=&quot;140&quot; height=&quot;120&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;15&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;14&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;40&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;16&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;820&quot; y=&quot;610&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;17&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;840&quot; y=&quot;610&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;18&quot; value=&quot;&quot; style=&quot;shape=actor;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;860&quot; y=&quot;610&quot; width=&quot;40&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;21&quot; value=&quot;Sensor&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;300&quot; y=&quot;400&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;22&quot; value=&quot;Event Action&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;280&quot; y=&quot;360&quot; width=&quot;380&quot; height=&quot;120&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:331px;"><defs/><g><path d="M 300 100 L 300 193.63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 300 198.88 L 296.5 191.88 L 300 193.63 L 303.5 191.88 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 170px; margin-left: 300px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;">Public IP</div></div></div></foreignObject><text x="300" y="173" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle">Public IP</text></switch></g><rect x="240" y="40" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 70px; margin-left: 241px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ITS API</div></div></div></foreignObject><text x="300" y="74" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">ITS API</text></switch></g><path d="M 140 70 L 233.63 69.53" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 238.88 69.51 L 231.9 73.04 L 233.63 69.53 L 231.86 66.04 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 70px; margin-left: 190px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;"> Alarm </div></div></div></foreignObject><text x="190" y="73" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Alarm </text></switch></g><path d="M 344.6 213.24 L 494.54 123.28" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 499.04 120.58 L 494.84 127.18 L 494.54 123.28 L 491.24 121.18 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 166px; margin-left: 423px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;"> SNS </div></div></div></foreignObject><text x="423" y="170" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> SNS </text></switch></g><path d="M 358.54 248.78 L 493.7 269.06" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 498.89 269.83 L 491.45 272.26 L 493.7 269.06 L 492.49 265.33 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 259px; margin-left: 430px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;"> SNS </div></div></div></foreignObject><text x="430" y="263" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> SNS </text></switch></g><path d="M 270 220 C 246 220 240 240 259.2 244 C 240 252.8 261.6 272 277.2 264 C 288 280 324 280 336 264 C 360 264 360 248 345 240 C 360 224 336 208 315 216 C 300 204 276 204 270 220 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 240px; margin-left: 241px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">WEB</div></div></div></foreignObject><text x="300" y="244" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">WEB</text></switch></g><path d="M 500 83 L 500 60 L 640 60 L 640 83" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 500 83 L 500 180 L 640 180 L 640 83" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 500 83 L 640 83" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="569.5" y="76">Telegram Group</text></g><path d="M 520 160 C 520 136 520 124 540 124 C 526.67 124 526.67 100 540 100 C 553.33 100 553.33 124 540 124 C 560 124 560 136 560 160 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 540 160 C 540 136 540 124 560 124 C 546.67 124 546.67 100 560 100 C 573.33 100 573.33 124 560 124 C 580 124 580 136 580 160 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 560 160 C 560 136 560 124 580 124 C 566.67 124 566.67 100 580 100 C 593.33 100 593.33 124 580 124 C 600 124 600 136 600 160 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 580 160 C 580 136 580 124 600 124 C 586.67 124 586.67 100 600 100 C 613.33 100 613.33 124 600 124 C 620 124 620 136 620 160 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 500 233 L 500 210 L 640 210 L 640 233" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 500 233 L 500 330 L 640 330 L 640 233" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 500 233 L 640 233" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="569.5" y="226">Telegram Group</text></g><path d="M 520 310 C 520 286 520 274 540 274 C 526.67 274 526.67 250 540 250 C 553.33 250 553.33 274 540 274 C 560 274 560 286 560 310 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 540 310 C 540 286 540 274 560 274 C 546.67 274 546.67 250 560 250 C 573.33 250 573.33 274 560 274 C 580 274 580 286 580 310 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 560 310 C 560 286 560 274 580 274 C 566.67 274 566.67 250 580 250 C 593.33 250 593.33 274 580 274 C 600 274 600 286 600 310 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 580 310 C 580 286 580 274 600 274 C 586.67 274 586.67 250 600 250 C 613.33 250 613.33 274 600 274 C 620 274 620 286 620 310 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><rect x="20" y="40" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 70px; margin-left: 21px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Sensor</div></div></div></foreignObject><text x="80" y="74" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Sensor</text></switch></g><path d="M 0 23 L 0 0 L 380 0 L 380 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 0 120 L 380 120 L 380 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 380 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="189.5" y="16">Event Action</text></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

### Example: sendMessage
```
{
	"data":[
		{
			"messenger":{
				"sendMessage":"ITS API System Message"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"messenger": {"sendMessage": "http request Message"}}]
```
```
echo '[{"messenger": {"sendMessage": "Commend Line Message"}}]' | nc ip_address 34001 -q 0
```
<div style="page-break-after: always"></div>

## **Custom**
tcp_socket, http_get, http_post를 통한 네트워크상의 이기종 서버에 명령을 전송함

본 기능은 API가 제공되는 독립된 디바이스나 시스템의 직접제어가 가능하다.

예를 들면 IP Camera, IP Audio, Monitoring System, Factory Automation System, etc..

### **Format - tcp_socket**
```
{
	"data":[
		{
			"custom":{
				"method":"tcp_socket",
				"isJson": true / false,
				"data": {}
			},
			"count": "0",
			"interval": "0"
		},
		"server": {
			"host": "server ip",
			"port": "server port"
		}
	]
}
```
- method 
- isJson : 데이터 타입
- count
- interval
- server : Remote Server Info
<div style="page-break-after: always"></div>

### Example: tcp_sockert - JSON
```
{
	"data": [
		{
			"custom": {
				"method": "tcp_socket",
				"isJson": true,
				"data": {
					"id_01": "name_01",
					"id_02": "name_02"
				},
				"count": "3",
				"interval": "3"
			},
			"server": {
				"host": "ip_address",
				"port": "34001"
			},
			"debug": true
		}
	]
}
```
```
http://ip_address/api.php?api=[{"custom":{"method":"tcp_socket","isJson":true,"data":{"id_01":"name_01","id_02":"name_02"},"count":"3","interval":"3"},"server":{"host":"192.168.0.50","port":"34001"},"debug":true}]

```
<div style="page-break-after: always"></div>

### Example: tcp_sockert - Non JSON
```
{
	"data": [
		{
			"custom": {
				"method": "tcp_socket",
				"isJson": false,
				"data": "id_01=name_01, id_02=name_02",
				"count": "0",
				"interval": "0"
			},
			"server": {
				"host": "ip_address",
				"port": "34001"
			},
			"debug": true
		}
	]
}
```
```
http://ip_address/api.php?api=[{"custom":{"method":"tcp_socket","isJson":false,"data":"id_01=name_01, id_02=name_02","count":"3","interval":"3"},"server":{"host":"192.168.0.50","port":"34001"},"debug":true}]

```
<div style="page-break-after: always"></div>

### Example: tcp_sockert - Non JSON - IMS protocol 
```
{
	"data": [
		{
			"custom": {
				"method": "tcp_socket",
				"isJson": false,
				"data": "id=g300t100_192_168_0_90_0012,name=R01,beep=1,shot=,latS=0.0,lngS=0.0,latE=0.0,lngE=0.0,count=1,block=0,status=1,msg=Active_Event",
				"count": "0",
				"interval": "0"
			},
			"server": {
				"host": "192.168.0.90",
				"port": "38087"
			},
			"debug": true
		}
	]
}
```
```
http://ip_address/api.php?api=[{"custom":{"method":"tcp_socket","isJson":false,"data":"id=g300t100_192_168_0_90_0012,name=R01,beep=1,shot=,latS=0.0,lngS=0.0,latE=0.0,lngE=0.0,count=1,block=0,status=1,msg=Active_Event","count":"3","interval":"3"},"server":{"host":"192.168.0.90","port":"38087"},"debug":true}]

```
<div style="page-break-after: always"></div>

### **Format - http_get/http_post**
```
{
	"data":[
		{
			"custom":{
				"method":"http_get/http_post",
				"data": {
					data
					...
				},
				"count": "0",
				"interval": "0"
			},
		},
		"server":{
			"url":"server url",
			"username":"",
			"password":""
		}
	]
}
```
- method : http_get 또는 http_post
- count
- interval
- server : Remote Server URL, Username, Password
<div style="page-break-after: always"></div>

### Example: http_get
```
{
	"data":[
		{
			"custom":{
				"method":"http_get", 
				"data":{
					"id_01":"name_01",
					"id_02":"name_02"
				},
				"count": "0",
				"interval": "0"
			},
			"server":{
				"url":"http://ip_address/api.php"
				"username":"",
				"password":""
			},
		}
	]
}
```
```
http://ip_address/api.php?api=[{"custom":{"method":"http_get","data":{"id_01":"name_01","id_02":"name_02"},"count":"0","interval":"0"},"server":{"url":"http://ip_address/api.php"},"debug":true}]
http://ip_address/api.php?api=[{"custom":{"method":"http_get","data":{"id_01":"name_01","id_02":"name_02"},"count":"0","interval":"0"},"server":{"url":"http://ip_address/api.php","username":"","password":""},"debug":true}]
http://192.168.0.50/api.php?api=[{"custom":{"method":"http_get","data":{"id_01":"name_01","id_02":"name_02"},"count":"0","interval":"0"},"server":{"url":"http://192.168.0.50/api.php","username":"","password":""},"debug":true}]

```
<div style="page-break-after: always"></div>

### Example: http_post
```
{
	"data":[
		{
			"custom":{
				"method":"http_post", 
				"data":{
					"id_01":"name_01",
					"id_02":"name_02"
				},
				"count": "3",
				"interval": "3"
			},
			"server":{
				"url":"http://ip_address/api.php",
				"username":"",
				"password":""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"custom":{"method":"http_post","data":{"id_01":"name_01","id_02":"name_02"},"count":"3","interval":"3"},"server":{"url":"http://ip_address/api.php"},"debug":true}]
http://192.168.0.50/api.php?api=[{"custom":{"method":"http_post","data":{"id_01":"name_01","id_02":"name_02"},"count":"0","interval":"0"},"server":{"url":"http://192.168.0.50/api.php","username":"","password":""},"debug":true}]

```
<div style="page-break-after: always"></div>

## **System**
부가 명령어 기능이다.
- 주로 ITS API Device 관련 명령들로 디바이스명, 오디오, 센서, 시간 설정및 시그템 재부팅 이나 프로그램 재실행관련 명령으로 이루어져 있다.
- 사용자의 피드백에 따른 필요한 명령을 지속적으로 개발 중이다.

### **Format**
```
{
	"data":[
		{
			"system":{
				"command":"[names]",
				"value": ""
			}
		}
	]
}
```
- names : 
  - sleep, set_name, get_name, set_time, get_time, stop_audio, list_audio, enable_audio, disable_audio, health_check, disable_io, enable_io, trigger_io, restart, reboot
<div style="page-break-after: always"></div>

### Example: sleep
- 특정시간 대기
```
{
	"data":[
		{
			"system":{
				"command":"sleep",
				"value": "1.5"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"sleep","value":"1.5"},"debug":true}]

Return:
{
  "ip": "ip_address",
  "category": "system",
  "command": "sleep",
  "msg": "sleep 1sec"
}
```
<div style="page-break-after: always"></div>

### Example: get_name
- 디바이스명 불러오기
```
{
	"data":[
		{
			"system":{
				"command":"get_name",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"get_name","value":""},"debug":true}]

Return:
{
  "ip": "ip_address",
  "category": "system",
  "command": "get_name",
  "msg": "Location"
}
```
<div style="page-break-after: always"></div>

### Example: set_name
- 디바이스명 설정하기
```
{
	"data":[
		{
			"system":{
				"command":"set_name",
				"value": "New Title"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"set_name","value":"New Title"},"debug":true}]

Return:
{
  "ip": "ip_address",
  "category": "system",
  "command": "set_name",
  "msg": "New location name is New Title"
}
```
<div style="page-break-after: always"></div>

### Example: get_time
- 디바이스 시간 불러오기
```
{
	"data":[
		{
			"system":{
				"command":"get_time",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"set_name","value":""},"debug":true}]

Return:
{
  "ip": "ip_address",
  "category": "system",
  "command": "set_name",
  "msg": "2022-06-29 22:02:52"
}
```
<div style="page-break-after: always"></div>

### Example: set_time
- 디바이스 시간 설정하기
```
{
	"data":[
		{
			"system":{
				"command":"set_time",
				"value": "2021-10-18 10:12:40"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"set_time","value":"2021-10-18 10:12:40"},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "set_time",
	"msg": "Success set_time Mon 18 Oct 10:12:40 KST 2021\n"
} 
```
<div style="page-break-after: always"></div>

### Example: list_audio
- 내부음원 목록 반환
```
{
	"data":[
		{
			"system":{
				"command":"list_audio",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"list_audio","value":""},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "list_audio",
	"msg": [
		"Air_Horn.mp3",
		"Fire_Truck.mp3",
		"Industrial.mp3",
		"Siren.mp3",
		"Smoke.mp3",
		"Whistle.mp3"
	]
}
```
<div style="page-break-after: always"></div>

### Example: stop_audio
- 오디오 출력 중지
```
{
	"data":[
		{
			"system":{
				"command":"stop_audio",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"stop_audio","value":""},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "stop_audio",
	"msg": "Success stop_audio"
}
```
<div style="page-break-after: always"></div>

### Example: enable_audio
- 오디오 기능 활성
```
{
	"data":[
		{
			"system":{
				"command":"enable_audio",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"enable_audio","value":""},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "enable_audio",
	"msg": "Now audio is enabled"
}
```
<div style="page-break-after: always"></div>

### Example: disable_audio
- 오디오 기능 비활성
```
{
	"data":[
		{
			"system":{
				"command":"disable_audio",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"disable_audio","value":""},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "disable_audio",
	"msg": "Now audio is disabled"
}
```
<div style="page-break-after: always"></div>

### Example: trigger_io
- Soft Sensing (Dry Contact이 아닌 인라인 명령)
- io01 ~ io08
	|Sensor|S01|S02|S03|S04|S05|S06|S07|S08|
	|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
	|ID|io01|io02|io03|io04|io05|io06|io07|io08|
- 주의: Action Script 내에 자신을 Call하게되면 무한루프 오류 발생
```
{
	"data":[
		{
			"system":{
				"command":"trigger_io",
				"value": "io01"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"trigger_io","value":"io01"},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "trigger_io",
	"msg": "trigger io01"
}
```
<div style="page-break-after: always"></div>

### Example: health_check
- ITS API 시스템 정보 반환
- IP Address, CPU Temp., CPI Useage, Storage Useage, Memory Useage, Systeme Time, Last Start Time, Live Time, License Key
```
{
	"data":[
		{
			"system":{
				"command":"health_check",
				"value": ""
			}
		}
	]
}
```
<div style="page-break-after: always"></div>

```
http://ip_address/api.php?api=[{"system":{"command":"health_check","value":""},"debug":true}]

Return:
{
  "ip": "ip_address",
  "category": "system",
  "command": "health_check",
  "msg": {
    "cpuPcent": {
      "idle": "94.9",
      "system": "3.8",
      "user": "1.3"
    },
    "cpuTemp": 52.078,
    "diskGb": {
      "avail": "10G",
      "pcent": "28%",
      "size": "15G",
      "used": "3.8G"
    },
    "fixed": {
      "dateTime": "2022-06-29 23:04:19.697769",
      "diskSize": "15G",
      "execTime": "0:00:00.284039",
      "ioBoard": "ITS STD",
      "ipAddr": "ip_address",
      "lastStart": "2022-06-02 18:16:14",
      "licenseStatus": "Approved",
      "liveTime": "2347848.96",
      "macAddr": "0xb827eb2af733L",
      "noLicense": 2592000,
      "run": "SRF",
      "serialKey": "000000000f2af733",
      "systemTitle": "ecos"
    },
    "memUseKb": {
      "free": "73.7",
      "total": "924.2"
    }
  }
}
```
<div style="page-break-after: always"></div>

### Example: enable_io
- GPIO 기능 활성
  - io01 ~ io08
	|Sensor|S01|S02|S03|S04|S05|S06|S07|S08|
	|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
	|ID|io01|io02|io03|io04|io05|io06|io07|io08|
  - io01 ~ io08
	|Relay|R01|R02|R03|R04|
	|:----:|:----:|:----:|:----:|:----:|
	|ID|io09|io10|io11|io12|
  - pw01
	|Power|P01|
	|:----:|:----:|
	|ID|pw01|
```
{
	"data":[
		{
			"system":{
				"command":"enable_io",
				"value": "io01"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"enable_io","value":"io01"},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "enable_io",
	"msg": "Now io01 is enabled"
}
```
<div style="page-break-after: always"></div>

### Example: disable_io
- GPIO 기능 비활성
```
{
	"data":[
		{
			"system":{
				"command":"disable_io",
				"value": "io01"
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"disable_io","value":"io01"},"debug":true}]

Return:
{
	"category": "system",
	"ip": "ip_address",
	"command": "disable_io",
	"msg": "Now io01 is disabled"
}
```
<div style="page-break-after: always"></div>

### Example: restart
- API 재실행
```
{
	"data":[
		{
			"system":{
				"command":"restart",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"restart","value":""},"debug":true}]

No Return:
```
<div style="page-break-after: always"></div>

### Example: reboot
- 디바이스 재부팅
```
{
	"data":[
		{
			"system":{
				"command":"reboot",
				"value": ""
			}
		}
	]
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"reboot","value":""},"debug":true}]

No Return:
```
<div style="page-break-after: always"></div>

## **Debug**
명령문에 결과갑을 반환한다.
- debug(Option) : true or false
### Example: Debug
```
{
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0.6"
			},
			"debug":true
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0.6"},"debug":true}]

Return:
{
	"ip": "ip_address",
	"category": "gpio",
	"status": "2",
	"response": {
		"io09": 0
	}
}
```
<div style="page-break-after: always"></div>

## **KeyCode**
모든 명령문의 암호화(Encryption) 인증(Authentication) 기능
- 키(Keycode) 생성은 관리자 권한이며 생성후 모든 명령문에 적용됨
- 전송시 명령어 레벨에 [keyCode]항목에 첨부 (SHA256 - Hex)
- 키값의 위치는 API > Setup > API Key > keyCode(License)이다.

### Example: KeyCode
```
{
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0.6"
			},
			"keyCode":"e3b0c44298fc1c...",
			"debug":true
		}
	]
}
```
```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09"},"keyCode":"e3b0c44298fc1c...","debug":true}]

Return:
{
  "ip": "ip_address",
  "category": "keyCode",
  "msg": "Missing keyCode value"
}
```
<div style="page-break-after: always"></div>


## **Complexed Script**
하나 이상의 명령을 동시에 요청할수 있다. 이는 콤마로 구분 명령문의 배열로 조합수는 무제한이다.

이벤트 발생시 주변 환경에 따라 경고 또는 안내방송과 동시에 경광등을 조작해야 하는등 복수의 작업이 필요한 때 사용한다.

또는 관제시스템에 알람을 보냄과 동시에 관련자에게 문자전송이나 Camera 제어등 다양한 응용이 가능 하다.


- 단일명령외 복합명령(Complexed Action Script) 사용시 중복되는 Debug mode 선언은 권장하지 않는다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="841px" viewBox="-0.5 -0.5 841 291" content="&lt;mxfile&gt;&lt;diagram id=&quot;dOEn6QzR0ujtc6Qldwkt&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;1538&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;2&quot; value=&quot;ITS API&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;440&quot; y=&quot;60&quot; width=&quot;220&quot; height=&quot;210&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;3&quot; value=&quot;Complexed Command&quot; style=&quot;shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;2&quot;&gt;&lt;mxGeometry x=&quot;20&quot; y=&quot;40&quot; width=&quot;180&quot; height=&quot;150&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;4&quot; value=&quot;&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;collapsible=0;dropTarget=0;pointerEvents=1;fillColor=none;top=0;left=0;bottom=1;right=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;&quot; vertex=&quot;1&quot; parent=&quot;3&quot;&gt;&lt;mxGeometry y=&quot;30&quot; width=&quot;180&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;5&quot; value=&quot;1&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;4&quot;&gt;&lt;mxGeometry width=&quot;40&quot; height=&quot;30&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle width=&quot;40&quot; height=&quot;30&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;6&quot; value=&quot;Command Value 1&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;overflow=hidden;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;4&quot;&gt;&lt;mxGeometry x=&quot;40&quot; width=&quot;140&quot; height=&quot;30&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle width=&quot;140&quot; height=&quot;30&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;7&quot; value=&quot;&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;collapsible=0;dropTarget=0;pointerEvents=1;fillColor=none;top=0;left=0;bottom=0;right=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;&quot; vertex=&quot;1&quot; parent=&quot;3&quot;&gt;&lt;mxGeometry y=&quot;60&quot; width=&quot;180&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;8&quot; value=&quot;2&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;7&quot;&gt;&lt;mxGeometry width=&quot;40&quot; height=&quot;30&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle width=&quot;40&quot; height=&quot;30&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;9&quot; value=&quot;Command&amp;amp;nbsp;Value 2&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;overflow=hidden;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;7&quot;&gt;&lt;mxGeometry x=&quot;40&quot; width=&quot;140&quot; height=&quot;30&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle width=&quot;140&quot; height=&quot;30&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;10&quot; value=&quot;&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;collapsible=0;dropTarget=0;pointerEvents=1;fillColor=none;top=0;left=0;bottom=0;right=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;&quot; vertex=&quot;1&quot; parent=&quot;3&quot;&gt;&lt;mxGeometry y=&quot;90&quot; width=&quot;180&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;11&quot; value=&quot;3&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;10&quot;&gt;&lt;mxGeometry width=&quot;40&quot; height=&quot;30&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle width=&quot;40&quot; height=&quot;30&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;12&quot; value=&quot;Command&amp;amp;nbsp;Value 3&quot; style=&quot;shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;overflow=hidden;pointerEvents=1;&quot; vertex=&quot;1&quot; parent=&quot;10&quot;&gt;&lt;mxGeometry x=&quot;40&quot; width=&quot;140&quot; height=&quot;30&quot; as=&quot;geometry&quot;&gt;&lt;mxRectangle width=&quot;140&quot; height=&quot;30&quot; as=&quot;alternateBounds&quot;/&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;13&quot; value=&quot;ITS API 1&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;780&quot; y=&quot;50&quot; width=&quot;90&quot; height=&quot;100&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;28&quot; value=&quot;&quot; style=&quot;shape=mxgraph.signs.tech.video_camera;html=1;pointerEvents=1;fillColor=#000000;strokeColor=none;verticalLabelPosition=bottom;verticalAlign=top;align=center;&quot; vertex=&quot;1&quot; parent=&quot;13&quot;&gt;&lt;mxGeometry x=&quot;12&quot; y=&quot;50&quot; width=&quot;68&quot; height=&quot;30&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;14&quot; value=&quot;ITS API 2&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;900&quot; y=&quot;150&quot; width=&quot;90&quot; height=&quot;100&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;23&quot; value=&quot;&quot; style=&quot;pointerEvents=1;verticalLabelPosition=bottom;shadow=0;dashed=0;align=center;html=1;verticalAlign=top;shape=mxgraph.electrical.electro-mechanical.loudspeaker;&quot; vertex=&quot;1&quot; parent=&quot;14&quot;&gt;&lt;mxGeometry y=&quot;30&quot; width=&quot;60&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;15&quot; value=&quot;ITS API 3&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;780&quot; y=&quot;240&quot; width=&quot;90&quot; height=&quot;100&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;24&quot; value=&quot;&quot; style=&quot;verticalLabelPosition=bottom;align=center;html=1;verticalAlign=top;pointerEvents=1;dashed=0;shape=mxgraph.pid2valves.valve;valveType=ball;defState=closed&quot; vertex=&quot;1&quot; parent=&quot;15&quot;&gt;&lt;mxGeometry x=&quot;15&quot; y=&quot;40&quot; width=&quot;60&quot; height=&quot;40&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;17&quot; value=&quot;&amp;amp;nbsp;Camera Control&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;4&quot; target=&quot;13&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;690&quot; y=&quot;145&quot;/&gt;&lt;mxPoint x=&quot;730&quot; y=&quot;100&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;18&quot; value=&quot;&amp;amp;nbsp;Audio Control&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;7&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;mxPoint x=&quot;900&quot; y=&quot;210&quot; as=&quot;targetPoint&quot;/&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;690&quot; y=&quot;175&quot;/&gt;&lt;mxPoint x=&quot;730&quot; y=&quot;210&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;19&quot; value=&quot;&amp;amp;nbsp;Gate Control&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;10&quot; target=&quot;15&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;690&quot; y=&quot;205&quot;/&gt;&lt;mxPoint x=&quot;730&quot; y=&quot;290&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;26&quot; value=&quot;&amp;amp;nbsp;Detect event&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;entryX=0;entryY=0.25;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;25&quot; target=&quot;2&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;&gt;&lt;Array as=&quot;points&quot;&gt;&lt;mxPoint x=&quot;310&quot; y=&quot;130&quot;/&gt;&lt;mxPoint x=&quot;400&quot; y=&quot;113&quot;/&gt;&lt;/Array&gt;&lt;/mxGeometry&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;25&quot; value=&quot;Sensor&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;150&quot; y=&quot;100&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:291px;"><defs/><g><path d="M 290 33 L 290 10 L 510 10 L 510 33" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 290 33 L 290 220 L 510 220 L 510 33" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 290 33 L 510 33" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="399.5" y="26">ITS API</text></g><path d="M 310 80 L 310 50 L 490 50 L 490 80" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 310 80 L 310 200 L 490 200 L 490 80" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 310 80 L 490 80" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 350 80 L 350 110 L 350 140 L 350 170" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="399.5" y="69.5">Complexed Command</text></g><path d="M 310 80 M 490 80 M 490 110 L 310 110" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><path d="M 310 80 M 350 80 M 350 110 M 310 110" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 38px; height: 1px; padding-top: 95px; margin-left: 311px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center; max-height: 26px; overflow: hidden;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">1</div></div></div></foreignObject><text x="330" y="99" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">1</text></switch></g><path d="M 350 80 M 490 80 M 490 110 M 350 110" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe flex-start; width: 132px; height: 1px; padding-top: 95px; margin-left: 358px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: left; max-height: 26px; overflow: hidden;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Command Value 1</div></div></div></foreignObject><text x="358" y="99" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px">Command Value 1</text></switch></g><path d="M 310 110 M 490 110 M 490 140 M 310 140" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><path d="M 310 110 M 350 110 M 350 140 M 310 140" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 38px; height: 1px; padding-top: 125px; margin-left: 311px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center; max-height: 26px; overflow: hidden;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">2</div></div></div></foreignObject><text x="330" y="129" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">2</text></switch></g><path d="M 350 110 M 490 110 M 490 140 M 350 140" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe flex-start; width: 132px; height: 1px; padding-top: 125px; margin-left: 358px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: left; max-height: 26px; overflow: hidden;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Command Value 2</div></div></div></foreignObject><text x="358" y="129" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px">Command Value 2</text></switch></g><path d="M 310 140 M 490 140 M 490 170 M 310 170" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><path d="M 310 140 M 350 140 M 350 170 M 310 170" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 38px; height: 1px; padding-top: 155px; margin-left: 311px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center; max-height: 26px; overflow: hidden;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">3</div></div></div></foreignObject><text x="330" y="159" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">3</text></switch></g><path d="M 350 140 M 490 140 M 490 170 M 350 170" fill="none" stroke="rgb(0, 0, 0)" stroke-linecap="square" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe flex-start; width: 132px; height: 1px; padding-top: 155px; margin-left: 358px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: left; max-height: 26px; overflow: hidden;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Command Value 3</div></div></div></foreignObject><text x="358" y="159" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px">Command Value 3</text></switch></g><path d="M 630 23 L 630 0 L 720 0 L 720 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 630 23 L 630 100 L 720 100 L 720 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 630 23 L 720 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="674.5" y="16">ITS API 1</text></g><path d="M 693.23 65 L 693.23 80 L 642 80 L 642 50 L 693.23 50 Z" fill="#000000" stroke="none" pointer-events="none"/><path d="M 693.23 65 L 710 77.38 L 710 65 L 710 52.62 Z" fill="#000000" stroke="none" pointer-events="none"/><path d="M 750 123 L 750 100 L 840 100 L 840 123" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 750 123 L 750 200 L 840 200 L 840 123" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 750 123 L 840 123" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="794.5" y="116">ITS API 2</text></g><path d="M 810 190 L 810 130 L 786 148 L 774 148 L 774 172 L 786 172 Z M 750 166 L 774 166 M 750 154 L 774 154" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 786 148 L 786 172" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 630 213 L 630 190 L 720 190 L 720 213" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 630 213 L 630 290 L 720 290 L 720 213" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 630 213 L 720 213" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="674.5" y="206">ITS API 3</text></g><ellipse cx="675" cy="250" rx="12" ry="12.8" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 645 230 L 675 250 L 645 270 Z M 705 230 L 675 250 L 705 270 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-linejoin="round" stroke-miterlimit="10" pointer-events="none"/><ellipse cx="675" cy="250" rx="12" ry="12.8" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><path d="M 490 95 L 530 95 Q 540 95 546.64 87.53 L 573.36 57.47 Q 580 50 590 50 L 623.63 50" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 628.88 50 L 621.88 53.5 L 623.63 50 L 621.88 46.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 73px; margin-left: 560px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; background-color: rgb(255, 255, 255); white-space: nowrap;"> Camera Control </div></div></div></foreignObject><text x="560" y="76" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Camera Control </text></switch></g><path d="M 490 125 L 530 125 Q 540 125 547.53 131.59 L 572.47 153.41 Q 580 160 590 160 L 743.63 160" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 748.88 160 L 741.88 163.5 L 743.63 160 L 741.88 156.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 160px; margin-left: 614px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; background-color: rgb(255, 255, 255); white-space: nowrap;"> Audio Control </div></div></div></foreignObject><text x="614" y="163" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Audio Control </text></switch></g><path d="M 490 155 L 530 155 Q 540 155 544.26 164.05 L 575.74 230.95 Q 580 240 590 240 L 623.63 240" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 628.88 240 L 621.88 243.5 L 623.63 240 L 621.88 236.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 198px; margin-left: 560px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; background-color: rgb(255, 255, 255); white-space: nowrap;"> Gate Control </div></div></div></foreignObject><text x="560" y="201" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Gate Control </text></switch></g><path d="M 120 80 L 150 80 Q 160 80 169.83 78.14 L 240.17 64.86 Q 250 63 260 62.88 L 283.63 62.58" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 288.88 62.51 L 281.93 66.1 L 283.63 62.58 L 281.84 59.1 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 71px; margin-left: 205px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; background-color: rgb(255, 255, 255); white-space: nowrap;"> Detect event </div></div></div></foreignObject><text x="205" y="75" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Detect event </text></switch></g><rect x="0" y="50" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="none"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 80px; margin-left: 1px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: none; white-space: normal; overflow-wrap: normal;">Sensor</div></div></div></foreignObject><text x="60" y="84" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">Sensor</text></switch></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

### Example: 이벤트 발생시 릴레이 n초 대기 후 Toggle
```
{ 
	"data": [
		{
			"system":{
				"command":"sleep",
				"value":"1.0"
			}
		},
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0.1"
			}
		}
	] 
}
```
```
http://ip_address/api.php?api=[{"system":{"command":"sleep","value":"1.0"}},{"gpio":{"status":"2","id":"io09","hold":"0.1"}},{"system":{"command":"sleep","value":"1.0"}},{"gpio":{"status":"2","id":"io09","hold":"0.1"},"debug":true}]

Return: 1초후에 반환값이 표시된다.
{
  "ip": "ip_address",
  "category": "gpio",
  "status": "2",
  "response": {
    "io09": 0
  }
}
```
<div style="page-break-after: always"></div>

### Example: 이벤트 발생시 릴레이(R01), 릴레이(R02) 동시 반전, n초 후 복귀
- http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"1"}},{"gpio":{"status":"2","id":"io10","hold":"1"}}]

### Example: 이벤트 발생시 릴레이(R01) 반전, n초 후 릴레이(R02) 반전
- http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0.1"},"debug":true},{"system":{"command":"sleep","value":"1.0"}},{"gpio":{"status":"2","id":"io10","hold":"0.1"},"debug":true}]

### Example: 단일 이벤트 릴레이(R01, R0, R03, R04) 전체 반전
- http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io09","hold":"0.2"}},{"gpio":{"status":"2","id":"io10","hold":"0.4"}},{"gpio":{"status":"2","id":"io11","hold":"0.6"}},{"gpio":{"status":"2","id":"io12","hold":"0.8"}}]

### Example: 재생되는 오디오를 n초후, 정지시키고 새 음원 재생
- http://ip_address/api.php?api=[{"system":{"command":"sleep","value":"2"},"debug":true},{"system":{"command":"stop_audio","value":""},"debug":true},{"audio":{"source":"5","volume":"40","loop":"0"},"debug":true}]
- 
### Example: 재생되는 오디오를 즉시 정지시키고 새 음원 재생(**비상경보**)
- http://ip_address/api.php?api=[{"system":{"command":"stop_audio","value":""},"debug":true},{"audio":{"source":"5","volume":"40","loop":"0"},"debug":true}]
<div style="page-break-after: always"></div>


## **Server**
- Server 기능을 통해 각기다른 API(ITS)로 명령 요청
- Master와 Sub("server"명 소속)로 구분
### **Format**
```
{
	"host":"master ip",
	"port":"master port",
	"data":[
		{
			"gpio":{
				...
			},
			"server":{
				"host":"sub ip",
				"port":"sub port"
			}
		}
	]
}
```
- Master Server측에 Data를 전송
- Data측에서 Sub Server측에 GPIO 명령을 요청 한다.
<div style="page-break-after: always"></div>

### Example: Server
```
{
	"host":"master ip",
	"port":"master port",
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io12",
				"hold":"0.6",
				"interval":"4"
			},
			"server":{
				"host":"A_ip_address",
				"port":"34001"
			},
			"debug":true
		},
		{
			"audio":{
				"source":"5",
				"volume":"40",
				"loop":"0"
			},
			"server":{
				"host":"B_ip_address",
				"port":"34001"
			},
			"debug":true
		}
	]
}

```
- 설명: 마스터서버가 모든 명령을 일괄로 접수한다.
- 접수된 명령을 슬레이브 서버 A_ip_address에는 gpio 명령을 요청하고 
- 서버 B_ip_address에는 audio 명령을 요청한다.
<div style="page-break-after: always"></div>

```
http://ip_address/api.php?api=[{"gpio":{"status":"2","id":"io12","hold":"0.6","interval":"4"},"server":{"host":"192.168.0.50","port":"34001"},"debug":true},{"audio":{"source":"5","volume":"40","loop":"0"},"server":{"host":"192.168.0.80","port":"34001"},"debug":true}]

Return:
- Ignore "SyntaxError: JSON.parse ..."
{
	"ip": "192.168.0.50",
	"category": "gpio",
	"status": "2",
	"response": {
		"io12": 0
}
}{
	"ip": "192.168.0.50",
	"category": "audio",
	"response": {
		"sent": "5"
	}
}
```
<div style="page-break-after: always"></div>

### Example: CLI Test
이상의 모든 명령은 CLI에서도 실행 가능하다. 다음의 예를 참조
```
$ echo '[{"gpio":{"status":"2","id":"io12","hold":"0.6","interval":"4"},"server":{"host":"192.168.0.50","port":"34001"},"debug":true},{"audio":{"source":"5","volume":"40","loop":"0"},"server":{"host":"192.168.0.80","port":"34001"},"debug":true}]' | nc 192.168.0.70 34001 -q 0 
```
- 설명(CLI Test): 서버 A_ip_address에는 gpio 명령은 보내고 서버 B_ip_address에는 audio 명령을 실행하는 예 이다.

### Example: CLI vs Inline vs URI
다음은 CLI명령과 인라인 명령(Inline command), 브라우저(URI)요청간 명령어 차이로 3가지 모두 같은 명령문 이다.
- 인라인 명령(Inline command)
```
{
	"data":[
		{
			"gpio":{
				"status":"2",
				"id":"io09",
				"hold":"0"
			}
		}
	]
}
```
- CLI
```
	$ echo '[{"gpio":{"status":"2","id":"io12","hold":"0"}}]' | nc ip_address 34001 -q 0 

```
- 브라우저(URI)
```
	http://192.168.0.50/api.php?api=[{"gpio":{"status":"2","id":"io12","hold":"0"}}]

```
<div style="page-break-after: always"></div>


## **Scheduler(Crontab)**
콘솔 윈도 내에 알람 설정을 실행 한다.

본 기능은 리눅스 Crontab 룰을 따른다.

실행명령(스크립트)은 기존 센서룰과 같다.

설정된 명령문은 **프로그램 재실행 시 적용** 된다.

최소 1분단위 설정 가능하다.

오류가 발생된 명령은 무시 한다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="491px" viewBox="-0.5 -0.5 491 131" content="&lt;mxfile&gt;&lt;diagram id=&quot;FUVu_jIS-9bslkopNPLP&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;984&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;2&quot; value=&quot;&quot; style=&quot;sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#505050;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;outlineConnect=0;align=center;shape=mxgraph.office.concepts.calendar;&quot; parent=&quot;1&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;33&quot; y=&quot;59&quot; width=&quot;67&quot; height=&quot;61&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;5&quot; value=&quot;ITS API&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;380&quot; y=&quot;45&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;7&quot; value=&quot;&amp;amp;nbsp;Request Event Action&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;6&quot; target=&quot;5&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;6&quot; value=&quot;Scheduler&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;10&quot; y=&quot;10&quot; width=&quot;180&quot; height=&quot;130&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;4&quot; value=&quot;&quot; style=&quot;sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#505050;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;outlineConnect=0;align=center;shape=mxgraph.office.concepts.clock;&quot; parent=&quot;6&quot; vertex=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;100&quot; y=&quot;49&quot; width=&quot;60&quot; height=&quot;61&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:131px;"><defs/><g><rect x="23" y="49" width="67" height="61" fill="none" stroke="none" pointer-events="all"/><path d="M 40.93 70.25 L 40.93 61.94 L 49.42 61.94 L 49.42 70.25 Z M 52.25 70.25 L 52.25 61.94 L 60.75 61.94 L 60.75 70.25 Z M 63.58 70.25 L 63.58 61.94 L 72.07 61.94 L 72.07 70.25 Z M 74.91 70.25 L 74.91 61.94 L 83.39 61.94 L 83.39 70.25 Z M 74.91 81.34 L 74.91 73.02 L 83.39 73.02 L 83.39 81.34 Z M 63.58 81.34 L 63.58 73.02 L 72.07 73.02 L 72.07 81.34 Z M 52.25 81.34 L 52.25 73.02 L 60.75 73.02 L 60.75 81.34 Z M 40.93 81.34 L 40.93 73.02 L 49.42 73.02 L 49.42 81.34 Z M 29.61 81.34 L 29.61 73.02 L 38.1 73.02 L 38.1 81.34 Z M 29.61 103.52 L 29.61 95.2 L 38.1 95.2 L 38.1 103.52 Z M 40.93 103.52 L 40.93 95.2 L 49.42 95.2 L 49.42 103.52 Z M 52.25 103.52 L 52.25 95.2 L 60.75 95.2 L 60.75 103.52 Z M 63.58 103.52 L 63.58 95.2 L 72.07 95.2 L 72.07 103.52 Z M 74.91 92.43 L 74.91 84.11 L 83.39 84.11 L 83.39 92.43 Z M 63.58 92.43 L 63.58 84.11 L 72.07 84.11 L 72.07 92.43 Z M 52.25 92.43 L 52.25 84.11 L 60.75 84.11 L 60.75 92.43 Z M 40.93 92.43 L 40.93 84.11 L 49.42 84.11 L 49.42 92.43 Z M 29.61 92.43 L 29.61 84.11 L 38.1 84.11 L 38.1 92.43 Z M 25.83 107.23 L 87.17 107.23 L 87.17 58.24 L 25.83 58.24 Z M 23 110 L 23 52.76 C 23 50.47 24.91 49 26.71 49 L 86.26 49 C 88.43 49 90 50.81 90 52.62 L 90 110 Z" fill="#505050" stroke="none" pointer-events="all"/><rect x="370" y="35" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 65px; margin-left: 371px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ITS API</div></div></div></foreignObject><text x="430" y="69" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">ITS API</text></switch></g><path d="M 180 65 L 363.63 65" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 368.88 65 L 361.88 68.5 L 363.63 65 L 361.88 61.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 65px; margin-left: 275px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;"> Request Event Action </div></div></div></foreignObject><text x="275" y="68" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Request Event Action </text></switch></g><path d="M 0 23 L 0 0 L 180 0 L 180 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 0 23 L 0 130 L 180 130 L 180 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 180 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="89.5" y="16">Scheduler</text></g><path d="M 143.56 90.1 C 144.13 90.6 144.22 91.52 143.64 92.21 C 143.17 92.7 142.37 92.94 141.68 92.47 L 128.58 82.22 C 128.29 81.92 128.02 81.61 128.03 80.97 L 128.03 58.64 C 128.03 57.73 128.83 57.14 129.54 57.14 C 130.47 57.14 131.03 58.02 131.03 58.64 L 131.03 80.32 Z M 130.15 104.96 C 144.93 104.96 155 92.29 155 79.53 C 155 64.02 142.45 54.08 130.07 54.08 C 113.64 54.08 105.02 68.54 105.02 78.83 C 105.02 96.16 118.57 104.96 130.15 104.96 Z M 129.85 110 C 115.06 110 100.36 98.5 100 79.14 C 100 64.32 112.27 49 129.89 49 C 145.37 49 160 61.19 160 79.67 C 160 96.05 146.98 110 129.85 110 Z" fill="#505050" stroke="none" pointer-events="none"/></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
``` 
* * * * *  수행할 명령어
┬ ┬ ┬ ┬ ┬
│ │ │ │ │
│ │ │ │ │
│ │ │ │ └───────── 요일 (0 - 6) (0:일, 1:월, 2:화, ..., 6:토)
│ │ │ └───────── 월 (1 - 12)
│ │ └───────── 일 (1 - 31)
│ └───────── 시 (0 - 23)
└───────── 분 (0 - 59)
```
### Example: Scheduler Time Set
|Time Set|Comment|
|----:|:----|
| * * * * * | 매 분 마다|
| 45 5 * * 5 | 매 주 금요일 오전 5시 45분에 |
| 0,20,40 * * * * | 매 일 매 시간 0분, 20분, 40분에 |
| 0-30 1 * * * | 매 일 1시 0분 부터 30분까지 매 분 마다 |
| */10 * * * * | 매 10분 마다 |
| */10 2,3,4 5-6 * * | 5일, 6일간 2,3,4시 대 매 10분 마다 |
<div style="page-break-after: always"></div>

``` 
설정값 확인 방법
$ crontab -l
* * * * * echo '[{"gpio":{"status":"2","id":"io09","hold":"0"}}]' | nc ip_address 34001 -q 0 > /dev/null 2>&1
0 * * * * echo '[{"debug": true, "audio": {"volume": "77", "source": "1", "loop": "0"}}]' | nc ip_address 34001 -q 0 > /dev/null 2>&1
```
<div style="page-break-after: always"></div>

## **Timer(Threading)**
콘솔 윈도 내에 타이머 설정을 실행 한다.

실행명령은 기존 센서룰과 같다.

설정된 명령문은 **프로그램 재실행 시 적용** 된다.

최소 초단위 설정이 가능하다.

타이머 갯수는 config.json -> timerCmds 내 항목 추가로 가능 하다.

[타이머 버튼]의 이름을 'Heartbeat'라고 선언 하면 콘솔화면애 정해진 시간을 주기로 깜빡인다.

<br><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="491px" viewBox="-0.5 -0.5 491 131" content="&lt;mxfile&gt;&lt;diagram id=&quot;ShJSgmk8VOW3iCTNVhs6&quot; name=&quot;페이지-1&quot;&gt;&lt;mxGraphModel dx=&quot;984&quot; dy=&quot;841&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;600&quot; pageHeight=&quot;450&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;2&quot; value=&quot;ITS API&quot; style=&quot;rounded=1;whiteSpace=wrap;html=1;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;380&quot; y=&quot;45&quot; width=&quot;120&quot; height=&quot;60&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;3&quot; value=&quot;&amp;amp;nbsp;Request Event Action&amp;amp;nbsp;&quot; style=&quot;edgeStyle=none;html=1;&quot; edge=&quot;1&quot; parent=&quot;1&quot; source=&quot;4&quot; target=&quot;2&quot;&gt;&lt;mxGeometry relative=&quot;1&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;4&quot; value=&quot;Timer&quot; style=&quot;swimlane;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;10&quot; y=&quot;10&quot; width=&quot;180&quot; height=&quot;130&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;mxCell id=&quot;5&quot; value=&quot;&quot; style=&quot;html=1;verticalLabelPosition=bottom;align=center;labelBackgroundColor=#ffffff;verticalAlign=top;strokeWidth=2;strokeColor=#0080F0;shadow=0;dashed=0;shape=mxgraph.ios7.icons.gauge;&quot; vertex=&quot;1&quot; parent=&quot;4&quot;&gt;&lt;mxGeometry x=&quot;53.8&quot; y=&quot;40&quot; width=&quot;72.4&quot; height=&quot;71.5&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;" onclick="(function(svg){var src=window.event.target||window.event.srcElement;while (src!=null&amp;&amp;src.nodeName.toLowerCase()!='a'){src=src.parentNode;}if(src==null){if(svg.wnd!=null&amp;&amp;!svg.wnd.closed){svg.wnd.focus();}else{var r=function(evt){if(evt.data=='ready'&amp;&amp;evt.source==svg.wnd){svg.wnd.postMessage(decodeURIComponent(svg.getAttribute('content')),'*');window.removeEventListener('message',r);}};window.addEventListener('message',r);svg.wnd=window.open('https://viewer.diagrams.net/?client=1&amp;page=0&amp;edit=_blank');}}})(this);" style="cursor:pointer;max-width:100%;max-height:131px;"><defs/><g><rect x="370" y="35" width="120" height="60" rx="9" ry="9" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 65px; margin-left: 371px;"><div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">ITS API</div></div></div></foreignObject><text x="430" y="69" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">ITS API</text></switch></g><path d="M 180 65 L 363.63 65" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 368.88 65 L 361.88 68.5 L 363.63 65 L 361.88 61.5 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 65px; margin-left: 275px;"><div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;"><div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;"> Request Event Action </div></div></div></foreignObject><text x="275" y="68" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle"> Request Event Action </text></switch></g><path d="M 0 23 L 0 0 L 180 0 L 180 23" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/><path d="M 0 23 L 0 130 L 180 130 L 180 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><path d="M 0 23 L 180 23" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="none"/><g fill="rgb(0, 0, 0)" font-family="Helvetica" font-weight="bold" pointer-events="none" text-anchor="middle" font-size="12px"><text x="89.5" y="16">Timer</text></g><ellipse cx="90.13" cy="73.99" rx="33.34561532792926" ry="33.88946819603754" fill="rgb(255, 255, 255)" stroke="none" pointer-events="none"/><path d="M 90.13 46.88 L 90.13 40.1 C 106.05 40 119.81 51.34 123.01 67.19 C 126.2 83.03 117.94 98.96 103.27 105.23 C 88.6 111.5 71.61 106.36 62.71 92.96 C 53.8 79.55 55.45 61.62 66.66 50.13" fill="none" stroke="#0080f0" stroke-width="2" stroke-miterlimit="10" pointer-events="none"/><path d="M 70.13 53.66 L 90.8 73.31 C 90.98 73.7 90.9 74.17 90.6 74.47 C 90.31 74.78 89.85 74.85 89.47 74.67 Z" fill="none" stroke="#0080f0" stroke-width="2" stroke-linejoin="round" stroke-miterlimit="10" pointer-events="none"/></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
<div style="page-break-after: always"></div>

## **Log**
- 실시간 로그는 콘솔 상단 우측 [log]를 통해 확인 가능 하다.
- 로그테이터는 파일 기반으로 대략 10만 라인기준으로 10개의 파일로 보관 된다.
- 약 100만 라인 이상의 로그는 자동 삭제된다.
- URL: http://ip_address/data/log/API3/API3.log

## **Database Query** 
- Database
<div style="page-break-after: always"></div>


# Programming Examples
<div style="page-break-after: always"></div>

## python Code Example - **pyCode.py**
``` python
# 특정 릴레이(io09)를 토글링 한후 1초후 되돌린다.
# 디버그 모드를 활성화("debug":True)해서 반환값을 받는다.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json

host = 'ip_address'
port = 34001
obj = [{"gpio":{"status":"2","id":"io09","hold":"1"},"debug":True}]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1) # settimeout
try:
	s.connect((host,port))
	s.send(json.dumps(obj).encode('utf-8'))
	print(s.recv(1024))
except socket.error:
	print('socket.error')
except socket.timeout:
	print('socket.timeout')
finally:
	s.close()

```

- Python Code Test (Linux Terminal)

```  bash
$
$ python pyCode.py
{"category": "gpio", "ip": "ip_address", "status": "2", "response": {"io09_desc": 0}}
$
```
<div style="page-break-after: always"></div>

## PHP Code Example - **phpCode.php**
``` php
// 특정 릴레이(io11)를 활성화(1:On) 한후 3초 후 비 활성화("hold":"3" -> Off) 시킨다.
// 디버그 모드를 활성화("debug":True)해서 반환값을 받는다.

<?php
	$obj = '[{"gpio":{"status":"1","id":"io11","hold":"3"},"debug":true}]';
	
	try {
		// socket_create
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($socket === false) {
			echo "socket_create() failed: " . socket_strerror(socket_last_error());
		}
		// socket_connect
		$result = socket_connect($socket, "ip_address", "34001");
		if ($result === false) {
			echo "socket_connect() failed. " . socket_strerror(socket_last_error($socket));
		} 
		// socket_write
		socket_write($socket, $obj, strlen($obj));
		// socket_read when "debug":true
		print socket_read($socket, 1024);
	} finally {
		socket_close($socket);
	}

?>
```
- PHP Code Test (Linux Terminal)
``` bash
$ php phpCode.php
{"category": "gpio", "ip": "ip_address", "status": "2", "response": {"io11_desc": 1}}
$
```
<div style="page-break-after: always"></div>

```
/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
/_/   Daivoc Kim (Developer)  /_/
/_/         daivoc@gmail.com  /_/
/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
```
2022-10-31 06:37:24