# Redscan Pro를 위한 ITS 설정
- [Redscan Pro를 위한 ITS 설정](#redscan-pro를-위한-its-설정)
	- [폴더 및 파일 구성](#폴더-및-파일-구성)
		- [구조 및 파일 기능](#구조-및-파일-기능)
	- [프로그램 실행](#프로그램-실행)
	- [환경설정(Setup)](#환경설정setup)
		- [프로그램 실행](#프로그램-실행-1)
		- [Sensor Access Information : 센서 정보 등록](#sensor-access-information--센서-정보-등록)
		- [IMS_IP_Address_1ST : IMS IP 등록](#ims_ip_address_1st--ims-ip-등록)
		- [User Server Information : 사용자 모니터링 서버정보 등록](#user-server-information--사용자-모니터링-서버정보-등록)
		- [Access IP Filtering : 센서모니터링 프로그램 접근제한](#access-ip-filtering--센서모니터링-프로그램-접근제한)
		- [Sensor Test and Other Links : 센서 테스트 기능](#sensor-test-and-other-links--센서-테스트-기능)
	- [Area(Masking) Setup Tools](#areamasking-setup-tools)
		- [RLS 센서 모니터링](#rls-센서-모니터링)
		- [영역설정(Area Set) 프로그램](#영역설정area-set-프로그램)
		- [설정방법 예시](#설정방법-예시)
	- [API3 Interface - Click and Action!!](#api3-interface---click-and-action)
	- [IMS Protocol](#ims-protocol)


## 폴더 및 파일 구성

### 구조 및 파일 기능
	pi@ecos:~/RLS3 $ ls
	config.json  data  node_modules  readme.md  realtime_RLS.js  realtime_RLS_templet.html  RLS3.pyc  run_RLS3.pyc  setup.pyc  static  templates
	pi@ecos:~/RLS3 $

	config.json
		실행시 필요한 설정값을 저장 한다. - 내용 수정은 setup.pyc 프로그램을 이용한다.

	data
		폴더이며 임시파일과 프로그램 실행시 발생하는 로그를 저장한다.

		로그의 경로(~/RLS3/data/log/RLSV)내 파일구성은 아래와 같다.
			pi@ecos:~/RLS3/data/log/RLSV $ ls -l
			total 67704
			-rwxrwxrwx 1 pi pi  6384177 Sep 30 17:19 RLSV.log
			-rwxrwxrwx 1 pi pi 10485674 Sep 27 09:36 RLSV.log.1
			-rwxrwxrwx 1 pi pi 10485678 Sep 27 05:49 RLSV.log.2

		팁: 실시간 로그보는 방법
			$ tail -f ~/RLS3/data/log/RLSV/RLSV.log

	node_modules
		자바프로그램용 라이브러리

	realtime_RLS.js - Area Set(Masking) Setup Tools
		센서 모니터링 및 Area Set(Masking) 프로그램

		URI : http://its_ipAddress:51198/

	realtime_RLS_templet.html
		realtime_RLS.js 프로그램용 템플릿

	RLS3.pyc
		주 프로그램

	run_RLS3.pyc
		실행: $ python3 run_RLS3.pyc
		중지: Kill 명령으로 만 가능

		주 프로그램(RLS3.pyc)을 위한 사전작업을 하며 그내용은 아래와 같다. 

		기능
			- 센서와 통신 테스트
			- 데이터베이스 유무 테스트 및 테이블 생성
			- 센서의 설정값 확인
			- Area Set(Masking) 프로그램 구동 및 기존 설정값 표시
			- config_RLS3.json 생성
			- realtime_RLS_live.html 생성
			- RLS3.pyc 실행

	setup.pyc
		실행: $ python3 setup.pyc
		중지: Ctrl + C

		config.json 설정을 위한 GUI

		URI : http://its_ipAddress:8080/
		
	static
		setup.pyc 보조 프로그램

	templates
		setup.pyc 보조 프로그램

## 프로그램 실행
	기존 프로그램 실행방법과 동일
	단 필요에 따라 Plugin으로 API3를 필요로 한다.

	pi@ecos:~/utility $ python productKey.pyc
	Select Program
	1:api       2:api3      3:bss       4:camera
	5:fsi       6:gikenc    7:gikenp    8:gikent
	9:gpacu     10:gpio     11:gpwio    12:monitor
	13:rls3     14:rls_r    15:rls_v    16:speed
	17:srf      18:streaming 19:table
	Select number(order) with space:

	-> api3, rls3 선택
	-> 재부팅

## 환경설정(Setup)
	그림 참조
### 프로그램 실행
	$ cd /home/pi/RLS3
	$ python3 setup.pyc
		....

	- 실행후 Ctrl+C를 치기전까지 백그라운드로 동작된다.
	- 사용방법은 브리우저를 통한 포트접속으로 가능하다.
    	URI : http://its_ipAddress:8080/

### Sensor Access Information : 센서 정보 등록
	Sensor Access Information
	IP_Address : 센서 아이피 주소 - (필수)
		192.168.168.30
	Login_ID : 센서 접속 아이디 - (필수)
		root
	Password : 센서 접속 비밀번호 - (필수)
		RLS-0000
	Pickup_Cycle : 명령 요청 주기(Sec) - (필수)
		0.4
	Heartbeat : 하트비트 발생 주기(Sec) - (필수)
		60
		
### IMS_IP_Address_1ST : IMS IP 등록
	IMS Server Information
	IMS_IP_Address : IMS 아이피 주소(선택사항)
		192.168.0.91
		
### User Server Information : 사용자 모니터링 서버정보 등록
	User Server Information
	IMS_IP_Address : IMS 아이피 주소(선택사항)
		192.168.0.91

### Access IP Filtering : 센서모니터링 프로그램 접근제한
	Access IP Filtering
	Admin_Group_List : 어드민 아이피 그룹 - 이벤트 레벨 권한 설정 권한
		192.168.0.201,192.168.0.203
	Manager_Group_List : 메니저 아이피 그룹

	Denial_Group_List : 접속 제한 아이피 그룹
		192.168.0.10,192.168.0.20

### Sensor Test and Other Links : 센서 테스트 기능
	Sensor Test and Other Links
	센서테스트
		gInfoDevice
		gInfoStatus
		gInOutCurr
		gInOutDiff
		gMounting
		wsDetectObj
		wsDetectArea
		wsDetectMask
		wsDetectEvent
		ovSystemReboot
		ovGetDeviceInformation

	미디어테스트
		rtsp : 예약
		mjpg : 스트리밍 서비스
		shot : 스넵샷 서비스

	링크 및 재실행
		sensor : 제조사 센서 설정 프로그램 실행
		zoning : 센서모니터링 프로그램 실행
		api3 : ITS API3와 GPIO 컨트롤 프로그램
		restart : RLS3 프로그램 실행
		reboot : ITS 재실행

## Area(Masking) Setup Tools
	그림 참조

### RLS 센서 모니터링
	실시간 이벤트 발생이 표시되며 발생시점 위치에 따라 색이 결정되며 이벤트가 소멸될떄 까지 색이 유지 된다.
	크기와 센서로부터 거리가 표시된다.
	센서가 사전 설정한 영역(Area Set or Masking)이 표시되며 줌과 페닝기능이 가능하다.

### 영역설정(Area Set) 프로그램
	수용 및 거부 영역을 설정한다.

	기능
		Filter : Allow, Deny, Delete
			수용 또는 거부를 위한 Area Set(Masking) 및 삭제
		Trigger : T1 ~ T8
			Plugin API3의 io01 ~ io08과 결합
			ZoneID의 100단위 자리수와 동일시됨
			예: T3 -> ZoneID 301 ~ 399
		ZoneID : 101 ~ 999
			최대 898가지의 영역ID 구분
			100단위(300, 400, ..) ZoneID는 Heartbeat ID로 예약 되어 있음
		Level : 0 ~ 4
			Min, Max, Count, Keep의 조합
	
	영상 참조

### 설정방법 예시
	1. 감도(Level)설정은 횟수와 크기로 각각의 조합으로 총 5등급(0~4)으로 이루워진다.
	2. 영역ID(ZoneID)설정은 이벤트 발생의 예측 좌표로 총 898개의 ID로 구분 된다.
	3. 감도(Level)와 영역ID(ZoneID)의 조합으로 이루워지며 Area Set(Masking)의 갯수 제한은 없다.
	4. 이는 898개의 영역ID와 5가지 Level의 집합이다.
	5. 작업순서는 감도(Level)와 영역ID(ZoneID)설정 후(Admin 권한) Area Set(Masking) 순서이다.
	6. 감도(Level) 설정 - Admin
      	1. 0부터 4까지의 레벨에 필요한 감도값(크기, 횟수)을 선택한후 저장한다.
      	2. 레벨 설정값의 저장은 영역ID 설정과 무관하다.
      	3. 설정된 레벨의 감도를 보려면 기존의 레벨버튼을 클릭하면 실시간으로 보여진다.
	7. Area Set(Masking) - Admin, Manager
      	1. Allow, ZoneID(필요에 따른 ID), Level(사전 정의한 감도레벨)을 모두 선택한다.
      	2. 마우스를 통해 멥상에 위치를 정한다.(자동저장)

## API3 Interface - Click and Action!!
	특정 Zone에서 이벤트가 발생하면 API3 GPIO Input으로 Triggering하는 기능이다.

	예를 들어 T2가 활성화(Checked)되어 있으면
		- ZoneID 201에서 299로 선언된 영역ID에서 이벤트 발생시
		- API3의 io02를 트리거링하게 되고 동시에 사용자 명령을 실행하게 된다.
    사용자 명령을 통해 릴레이 작동나 멀티미디어 작업이 가능하다.
    또한 근접서버(예:Monitoring)와의 통신등의 원격작업을 실행한다.
   
## IMS Protocol
	RLS3의 이벤트 아이디는 Area Set(Masking)설정 프로그램에서 결정 된다.

	기본형식은
		Key+"_"+IP ADDRESS+"_"+ZoneID
          - Key : "g200t240" - Redscan Pro
          - IP : 192_168_0_70
          - ZoneID : Zone + "Z" + Level
           	- ZoneID: 101 ~ 999
           	- 구분자: "Z"
           	- Level: 0 ~ 4
          - Heartbeat : 100Z0

	예: g200t240_192_168_0_70_101Z1
	설명: Redscan Pro로 부터 ITS IP 192.168.0.70을 통해 존 101에서 레벨 1의 이벤트 발생

	예: g200t240_192_168_0_70_100Z0
	설명: Heartbeat
