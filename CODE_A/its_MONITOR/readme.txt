    Product Name: ECOS IMS
    Product Maker: ECOS Korea
    Product WEB: WWW.ECOSKOREA.CO.KR
    Product Version: 2022-04-16 05:11:00
    Product Detail: ECOS Intelligent Monitoring Server

    Company Name: ECOS KOREA CO., LTD.
    Company Address: Seoul Korea
    Company Phone: 82-10-9168-2267
    Company Email: support@ECOSKOREA.CO.KR

    Copyright(©) 2018 ECOS KOREA CO., LTD. All Rights Reserved.

- IMS 정의
    - 가상의 맵을 이용한 현장 상황의 실시간 감독
    - 다양한 형태의 센서상황을 관제 화면(SVG File)에 표시
    - 감지 이벤트와 관련된 위치 및 정보의 화면 표시 와 관련 카메라 팝업
    - 감지 이벤트 위치 정보를 카메라에 전송(Preset, PTZ)
- IMS 기능
    - 화면 관리
        - 지도의 확대(스크롤인), 축소(스크롤아웃), 좌우이동(드레깅)
        - 지난 한시간의 전체이벤트 관련 타임라인 그레프
        - 센서별 24시간 타임라인 그래프
        - 주야간 맵(배경화면) 밝기 변경 기능
        - 이벤트관련 스넵샷 보기
        - 실시간 전체 센서 상태 보기
        - 실시간 ITS Health Check 보기
            - 카메라 정보 보기 (카메라 클릭시)
            - 감지영역 최근 로그 보기 (감지영역 클릭시)
            - 자동 및 수동 상태로그 기록 기능
    - 데이터베이스
        - 400만 레코드 이상의 빅데이터 수집
            - 기간별 리스트 보기 및 엑셀데이터 생성
            - 기간별 차트 보기: 일별, 주간, 시간대
            - 전체 또는 센서별 구분검색
            - 이벤트 형태별 검색가능: 알람, 사용자로그, 오류
        - 사용자 관리 
            - 등급 -> admin, manager, viewer
        - 접근권한
            - admin -> 제어(PTZ), 설정, 실시간 모니터링
            - manager -> 설정, 실시간 모니터링
            - viewer -> 실시간 모니터링
- IMS 동작
    - 정상 상태시
        - 센서의 오작동 확인을 위한 하트비트 표시(지도 및 테이블)
    - 이벤트 발생시
        - 감지영역 화면 표시 
            - 발생 장소에 따른 오디오 재생(사용자 오디오 등록)
            - 동시에 최대 4대의 카메라 팝업 
            - 카메라 프리셋 작동 : 동시에 최대 4대의 PTZ 카메라
            - 실시간 로그 저장
        - 추적모드(Tracking)
            - 감지이벤트(1)일때만 실행
            - 감지영역 화면확대(Zoom In)
            - 요소가 속해 있는 부모 레이어를 화면에 채움(Scale참도: config.json)
                - "guiScreen":{
  					"fitGroup":1,
  					"fitObject":1
  				}
            - 줌상태는 일정시간(기본 10초)이상 이밴트가 없으면 전체화면 보기로 돌아옴 
            - 정보창과 카메라 팝업이 중지됨
    - 이벤트 필터링(Blocking)
        - Admin 권한으로 수신되는 이벤트 무시
            - 단선에 따른 복구시 일시적 무시
            - 확인된 알람의 일시적인 무시
        - Zone(센서)단위로 가능
            - 무시된 이벤트는 일반 이벤트와 색으로 구분
            - 관련된 알람(Sound)은 묵음 처리 됨 
    - 이벤트 상태(Status)
        - status == 1 : 이벤트 발생 - [A] color: 'red'
        - status == 0 : 센서레이디 - [H] color: 'green'
        - status == 2 : 하트비트 - [H] color: 'green'
        - status == 7 : 통신 오류 - [e] color: 'violet'
        - status == 8 : 함체열림 - [e] color: 'blue'
        - status == 9 : 센서 오류 - [E] color: 'orange'
- IMS 특징
    - 센서 진단
        - 센서와 관제사이의 물리적 접속진단
        - 전원 및 통신 장애 실시간 알람기능
    - NVR 또는 DVR 인터페이스
        - NVR / DVR Protocol에 따른 이벤트 전송
        - HTTP Request, TCP Socket, JSON
    - 브라우저(Html5)기반
        - 다양한 디바이스 접속 허용(PC, Tablet, Mobile)
        - 허가된 사용자 동시 접속
        - Agentless
    - 현장상황 변경에 따른 간단한 맵(배경화면)적용
        - 맵(배경화면) 편집툴 제공 -> Inkscape SVG Editor
    - 각각의 Zone(센서)을 바라보는 자체 카메라 프리셋 저장
        - 최대 4대의 카메라 PTZ 값 저장
    - 카메라 인터페이스
        - Onvif Interface
        - 실시간 카메라 컨트롤(PTZ), 프리셋 및 홈포지션 이동
- 기타 센서간 단전 단선에 따른 알람
    - 단전 단선된 디바이스는 아이피:포트 접속 시도로 확인 함
    - 기본적으로 Box Table에 선언된 멥 정보에 표시됨
    - 박스(함체) 선언이 없으면 관련 아이피에 연관된 모든 센서 정보를 표시 함
    - Health 상태 창을 통해 실시간 확인 가능
    - 이 알람(단전, 단선)은 별도의 알고리즘 과정을 포함하여 일반 알람에 비해 약 1.5배정도 늦게 반응한다.
- DB Table: 주요항목
    - Camera Table -> g500t100
        - Camera Login Info., URL(Video, Snapshot), Model
        - X, Y 해상도 - 선택 
        - PTZ Camera 인경우 마우스로 카메라 컨트롤 가능
            - Dbl Click : 좌우 상하 이동
            - Wheel Scroll : 줌 인, 아웃
        - MapID Link - 필수
        - Sensor Link - 선택(예약)
        - Box(함체) Link - 선택(예약)
    - Zone(센서) Table -> g500t200
        - MapID Link - 필수
        - Sensor Link - 필수
        - Box(함체) Link - 선택
            - 센서와 통신 장에시 관련 함체정보를 표시를 위함
        - 최대 4대의 관련 카메라 PTZ 값 - 선택
        - MP3 Audio Upload - 선택
    - Box(함체) Table -> g500t300
        - MapID Link - 필수
        - 최대 4대의 관련 카메라 PTZ 값 - 선택
        - MP3 Audio Upload - 선택
- SVG Editor
    - Inkscape
- Image Editor
    - GIMP
