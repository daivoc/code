<?php
if (!defined('_GNUBOARD_')) exit;

// its_web 'OPTEX', its_webC 'Chinese', its_webE 'English', its_webJ 'Japaness', its_webK 'Korean'
$ITS_Lang = array( 'its_web' => 0,'its_webC' => 1,'its_webE' => 2,'its_webJ' => 3,'its_webK' => 4 );
// 사용자 manager의 예약필드 mb_7의 내용을 통해 언어를 선언 한다.
$sql = " select mb_7 from {$g5['member_table']} where mb_id = 'manager' ";
$row = sql_fetch($sql);
if ($row['mb_7']) {
	define('ITS_Lang', $ITS_Lang[$row['mb_7']]);
} else {
	define('ITS_Lang', 0);
}

$SK_BO_Accept_Boundary	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Accept Boundary',	3 =>'Japaness',	4 =>'허용범주');
$SK_BO_Accept_Range		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Accept Range',		3 =>'Japaness',	4 =>'허용범위');
$SK_BO_About			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'About',			3 =>'Japaness',	4 =>'대략');
$SK_BO_Advanced			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Advanced',			3 =>'Japaness',	4 =>'고급설정');
$SK_BO_Alarm_Cycle		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Alarm Cycle',		3 =>'Japaness',	4 =>'경보주기');
$SK_BO_Alert			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Alert',			3 =>'Japaness',	4 =>'경보');
$SK_BO_All				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'All',				3 =>'Japaness',	4 =>'전체');
$SK_BO_Allowable		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Allowable',		3 =>'Japaness',	4 =>'허용조건');
$SK_BO_Allowable_Dia	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Allowable Dia.',	3 =>'Japaness',	4 =>'허용직경');
$SK_BO_Angle			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Angle',			3 =>'Japaness',	4 =>'각도');
$SK_BO_Apply			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Apply',			3 =>'Japaness',	4 =>'즉시적용');
$SK_BO_Area_Block		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Area Block',		3 =>'Japaness',	4 =>'지역차단');
$SK_BO_Box				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Box',				3 =>'Japaness',	4 =>'함체');
$SK_BO_Basic			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Basic',			3 =>'Japaness',	4 =>'기본설정');
$SK_BO_Blocked			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Blocked',			3 =>'Japaness',	4 =>'상시차단');
$SK_BO_Camera			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Camera',			3 =>'Japaness',	4 =>'카메라');
$SK_BO_Cameraview		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Camera View',		3 =>'Japaness',	4 =>'카메라뷰');
$SK_BO_Capacity			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Capacity',			3 =>'Japaness',	4 =>'수용량');
$SK_BO_Cancel			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Cancel',			3 =>'Japaness',	4 =>'취소');
$SK_BO_Category			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Category',			3 =>'Japaness',	4 =>'분류');
$SK_BO_Choose			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Choose',			3 =>'Japaness',	4 =>'선택하세요');
$SK_BO_Chart			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Chart',			3 =>'Japaness',	4 =>'차트');
$SK_BO_Cmeter			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Cm',				3 =>'Japaness',	4 =>'센티미터');
$SK_BO_Created			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Created',			3 =>'Japaness',	4 =>'생성됨');
$SK_BO_Current			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Current',			3 =>'Japaness',	4 =>'현재');
$SK_BO_Day				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Day',				3 =>'Japaness',	4 =>'일');
$SK_BO_Daily			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Daily',			3 =>'Japaness',	4 =>'일간');
$SK_BO_Delete			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Delete',			3 =>'Japaness',	4 =>'삭제');
$SK_BO_Delay			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Delay',			3 =>'Japaness',	4 =>'지연');
$SK_BO_Detect_Range		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Detect. Range',	3 =>'Japaness',	4 =>'감지범위');
$SK_BO_Device_Name		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Device Name',		3 =>'Japaness',	4 =>'디바이스');
$SK_BO_Direction		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Direction',		3 =>'Japaness',	4 =>'방향');
$SK_BO_Disable			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Disable',			3 =>'Japaness',	4 =>'사용중지');
$SK_BO_Email			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Email',			3 =>'Japaness',	4 =>'이메일');
$SK_BO_Empty_Board		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Empty Board',		3 =>'Japaness',	4 =>'게시물이 없습니다');
$SK_BO_Encryption		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Encryption',		3 =>'Japaness',	4 =>'암호화');
$SK_BO_End				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'End',				3 =>'Japaness',	4 =>'종료');
$SK_BO_End_Coord		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'End Coord',		3 =>'Japaness',	4 =>'종료좌표');
$SK_BO_Event			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event',			3 =>'Japaness',	4 =>'이벤트');
$SK_BO_Event_Count		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event Count',		3 =>'Japaness',	4 =>'허용횟수');
$SK_BO_Event_Cycle		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event Cycle',		3 =>'Japaness',	4 =>'이벤트주기');
$SK_BO_Event_Hold		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Event Hold',		3 =>'Japaness',	4 =>'대기시간');
$SK_BO_Events			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Events',			3 =>'Japaness',	4 =>'이벤트');
$SK_BO_Events_Level		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Events Level',		3 =>'Japaness',	4 =>'이벤트레벨');
$SK_BO_Help				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Help',				3 =>'Japaness',	4 =>'도움말');
$SK_BO_History			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'History',			3 =>'Japaness',	4 =>'수정내역');
$SK_BO_Hold				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Hold',				3 =>'Japaness',	4 =>'대기');
$SK_BO_Hold_Distance	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Hold Distance',	3 =>'Japaness',	4 =>'거리고정');
$SK_BO_Home_Page		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Home Page',		3 =>'Japaness',	4 =>'홈페이지');
$SK_BO_Host_Main		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Host(Main)',		3 =>'Japaness',	4 =>'호스트(주)');
$SK_BO_Host_Mirror		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Host(Mirror)',		3 =>'Japaness',	4 =>'호스트(부)');
$SK_HD_Info				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Information',		3 =>'Japaness',	4 =>'정보수정');
$SK_BO_Ignore_Area		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Ignore Area',		3 =>'Japaness',	4 =>'무시영역');
$SK_BO_ID				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'ID',				3 =>'Japaness',	4 =>'아이디');
$SK_BO_IP				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'IP',				3 =>'Japaness',	4 =>'아이피');
$SK_BO_Keep_Cycle		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Keep Cycle',		3 =>'Japaness',	4 =>'주기고정');
$SK_BO_Keep_Location	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Hold Location',	3 =>'Japaness',	4 =>'위치고정');
$SK_BO_Key				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Key',				3 =>'Japaness',	4 =>'키');
$SK_BO_Level			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Level',			3 =>'Japaness',	4 =>'레벨');
$SK_BO_License			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'License',			3 =>'Japaness',	4 =>'라이센스');
$SK_BO_List				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'List',				3 =>'Japaness',	4 =>'목록');
$SK_BO_Location			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Location',			3 =>'Japaness',	4 =>'설치장소');
$SK_BO_Log				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Log',				3 =>'Japaness',	4 =>'로그');
$SK_HD_Login			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Login',			3 =>'Japaness',	4 =>'로그인');
$SK_HD_Logout			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Logout',			3 =>'Japaness',	4 =>'로그아웃');
$SK_BO_Map				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Map',				3 =>'Japaness',	4 =>'지도');
$SK_BO_Master			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Master',			3 =>'Japaness',	4 =>'마스터');
$SK_HD_Menu				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Menu',				3 =>'Japaness',	4 =>'메뉴');
$SK_BO_Meter			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Meter',			3 =>'Japaness',	4 =>'미터');
$SK_BO_Model_Name		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Model Name',		3 =>'Japaness',	4 =>'모델명');
$SK_BO_Modified			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Modified',			3 =>'Japaness',	4 =>'수정됨');
$SK_BO_Modify			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Modify',			3 =>'Japaness',	4 =>'수정');
$SK_BO_Monitor			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monitor',			3 =>'Japaness',	4 =>'모니터');
$SK_BO_Monitoring		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monitoring',		3 =>'Japaness',	4 =>'모니터링');
$SK_BO_Multiful_Check	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Multiful Check',	3 =>'Japaness',	4 =>'복수금지');
$SK_BO_Name				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Name',				3 =>'Japaness',	4 =>'이름');
$SK_BO_New				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'New',				3 =>'Japaness',	4 =>'신규');
$SK_BO_Next				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Next',				3 =>'Japaness',	4 =>'다음');
$SK_BO_Offset			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Offset',			3 =>'Japaness',	4 =>'오프셋');
$SK_HD_Oneway			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Oneway',			3 =>'Japaness',	4 =>'일방통행');
$SK_BO_Option			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Option',			3 =>'Japaness',	4 =>'옵션');
$SK_BO_Password			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'password',			3 =>'Japaness',	4 =>'비밀번호');
$SK_BO_Pause			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Pause',			3 =>'Japaness',	4 =>'일시정지');
$SK_BO_Port				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Port',				3 =>'Japaness',	4 =>'포트');
$SK_BO_Position			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Position',			3 =>'Japaness',	4 =>'위치');
$SK_BO_Previous			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Previous',			3 =>'Japaness',	4 =>'이전');
$SK_BO_Range			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Range',			3 =>'Japaness',	4 =>'영역');
$SK_HD_Reboot			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Reboot',			3 =>'Japaness',	4 =>'재부팅');
$SK_BO_Reservation		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Reservation',		3 =>'Japaness',	4 =>'예약차단');
$SK_BO_Reserve			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Reserve',			3 =>'Japaness',	4 =>'예약');
$SK_BO_Restart			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Restart',			3 =>'Japaness',	4 =>'재실행');
$SK_BO_Save2			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Save',				3 =>'Japaness',	4 =>'작성완료');
$SK_BO_Save				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Save',				3 =>'Japaness',	4 =>'저장');
$SK_BO_Schedule			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Schedule',			3 =>'Japaness',	4 =>'스케줄');
$SK_BO_Search			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Search',			3 =>'Japaness',	4 =>'검색');
$SK_BO_Second			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sec.',				3 =>'Japaness',	4 =>'초');
$SK_BO_Sensitivity		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensitivity',		3 =>'Japaness',	4 =>'허용감도');
$SK_BO_Sensing_Boundary	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensing Boundary',	3 =>'Japaness',	4 =>'감지지역');
$SK_BO_Sensor			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor',			3 =>'Japaness',	4 =>'센서');
$SK_BO_Sensor_Azimuth	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Azimuth',	3 =>'Japaness',	4 =>'센서방위');
$SK_BO_Sensor_Face		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Face',		3 =>'Japaness',	4 =>'센서방향');
$SK_BO_Sensor_Name		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Name',		3 =>'Japaness',	4 =>'센서관리명');
$SK_BO_Sensor_IP		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor IP',		3 =>'Japaness',	4 =>'센서아이피');
$SK_BO_Sensor_Type		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor Type',		3 =>'Japaness',	4 =>'센서형태');
$SK_BO_Setup			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Setup',			3 =>'Japaness',	4 =>'설정');
$SK_BO_Serial_Number	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Serial Number',	3 =>'Japaness',	4 =>'고유번호');
$SK_HD_Shutdown			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Shutdown',			3 =>'Japaness',	4 =>'종료');
$SK_BO_Shot_Per_Event	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Shot / Event',		3 =>'Japaness',	4 =>'사진수');
$SK_BO_Snapshot			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Snapshot',			3 =>'Japaness',	4 =>'스넵샷');
$SK_BO_Speed_Limit		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Speed Limit',		3 =>'Japaness',	4 =>'허용속도');
$SK_BO_Start			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Start',			3 =>'Japaness',	4 =>'시작');
$SK_BO_Start_Coord		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Start Coord',		3 =>'Japaness',	4 =>'시작좌표');
$SK_BO_Stop_Alarm		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Stop Alarm',		3 =>'Japaness',	4 =>'알람정지');
$SK_BO_Streaming		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Streaming',		3 =>'Japaness',	4 =>'스트리밍');
$SK_HD_Sync_Clock		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sync Clock',		3 =>'Japaness',	4 =>'시간동기');
$SK_BO_Submit			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Submit',			3 =>'Japaness',	4 =>'전송');
$SK_BO_Times			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Times',			3 =>'Japaness',	4 =>'회');
$SK_BO_Trace			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Trace',			3 =>'Japaness',	4 =>'리뷰');
$SK_BO_Update			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Update',			3 =>'Japaness',	4 =>'등록');
$SK_BO_URL_Main			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'URL(Main)',		3 =>'Japaness',	4 =>'URL(주)');
$SK_BO_URL_Mirror		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'URL(Json)',		3 =>'Japaness',	4 =>'URL(Json)');
$SK_BO_Week				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Week',				3 =>'Japaness',	4 =>'주');
$SK_BO_Weekly			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Weekly',			3 =>'Japaness',	4 =>'주간');
$SK_BO_Write			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Write',			3 =>'Japaness',	4 =>'글쓰기');
$SK_BO_Zone				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Zone',				3 =>'Japaness',	4 =>'지역');
	
$SK_BO_Sun				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sun',				3 =>'Japaness',	4 =>'일');
$SK_BO_Mon				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Mon',				3 =>'Japaness',	4 =>'월');
$SK_BO_Tue				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Tue',				3 =>'Japaness',	4 =>'화');
$SK_BO_Wed				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Wed',				3 =>'Japaness',	4 =>'수');
$SK_BO_Thu				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Thu',				3 =>'Japaness',	4 =>'목');
$SK_BO_Fri				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Fri',				3 =>'Japaness',	4 =>'금');
$SK_BO_Sat				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sat',				3 =>'Japaness',	4 =>'토');

$SK_BO_Sunday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sunday',			3 =>'Japaness',	4 =>'일요일');
$SK_BO_Monday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monday',			3 =>'Japaness',	4 =>'월요일');
$SK_BO_Tuesday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Tuesday',			3 =>'Japaness',	4 =>'화요일');
$SK_BO_Wednesday		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Wednesday',		3 =>'Japaness',	4 =>'수요일');
$SK_BO_Thursday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Thursday',			3 =>'Japaness',	4 =>'목요일');
$SK_BO_Friday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Friday',			3 =>'Japaness',	4 =>'금요일');
$SK_BO_Saturday			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Saturday',			3 =>'Japaness',	4 =>'토요일');

$SK_BO_January			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'January',			3 =>'Japaness',	4 =>'1월');
$SK_BO_February 		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'February',			3 =>'Japaness',	4 =>'2월');
$SK_BO_March			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'March',			3 =>'Japaness',	4 =>'3월');
$SK_BO_April			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'April',			3 =>'Japaness',	4 =>'4월');
$SK_BO_May				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'May',				3 =>'Japaness',	4 =>'5월');
$SK_BO_June				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'June',				3 =>'Japaness',	4 =>'6월');
$SK_BO_July				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'July',				3 =>'Japaness',	4 =>'7월');
$SK_BO_August			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'August',			3 =>'Japaness',	4 =>'8월');
$SK_BO_September		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'September',		3 =>'Japaness',	4 =>'9월');
$SK_BO_October			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'October',			3 =>'Japaness',	4 =>'10월');
$SK_BO_November			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'November',			3 =>'Japaness',	4 =>'11월');
$SK_BO_December			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'December',			3 =>'Japaness',	4 =>'12월');

$SK_BO_Jan				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Jan',				3 =>'Japaness',	4 =>'1월');
$SK_BO_Feb				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Feb',				3 =>'Japaness',	4 =>'2월');
$SK_BO_Mar				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Mar',				3 =>'Japaness',	4 =>'3월');
$SK_BO_Apr				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Apr',				3 =>'Japaness',	4 =>'4월');
$SK_BO_May				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'May',				3 =>'Japaness',	4 =>'5월');
$SK_BO_Jun				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Jun',				3 =>'Japaness',	4 =>'6월');
$SK_BO_Jul				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Jul',				3 =>'Japaness',	4 =>'7월');
$SK_BO_Aug				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Aug',				3 =>'Japaness',	4 =>'8월');
$SK_BO_Sep				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sep',				3 =>'Japaness',	4 =>'9월');
$SK_BO_Oct				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Oct',				3 =>'Japaness',	4 =>'10월');
$SK_BO_Nov				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Nov',				3 =>'Japaness',	4 =>'11월');
$SK_BO_Dec				= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Dec',				3 =>'Japaness',	4 =>'12월');

$SK_BO_Today			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Today',			3 =>'Japaness',	4 =>'오늘');
$SK_BO_Monthly			= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Monthly',			3 =>'Japaness',	4 =>'월간');



$SK_BO_Delete_event		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Delete the selected event.',		3 =>'XXX',			4 =>'선택한 이밴트를 삭제합니다.');
$SK_BO_Link_Interface	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor and linked interface.',		3 =>'XXX',			4 =>'센서와 연결된 인터페이스');
$SK_BO_Link_Alarm		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Sensor and linked alert.',			3 =>'XXX',			4 =>'센서와 연결된 알람');
$SK_BO_Conform_Reboot	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Do you want to restart the system?',3 =>'XXX',		4 =>'시스템을 재 시작 합니다.');
$SK_BO_Conform_Shutdown	= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Do you want to shutdown the system?',3 =>'XXX',		4 =>'시스템을 종료 합니다. 전원은 최소 20초 후에 제거 하시기 바랍니다.');
$SK_BO_Close_this_window		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Close_this_window',		3 =>'XXX',			4 =>'현재 창 닫기');
$SK_BO_Download_CSV		= array(0 =>'Optex',		1 =>'Chinese',		2 =>'Download_CSV',		3 =>'XXX',		4 =>'엑셀 다운로드');



/*

<?php echo $SK_BO_Delete_event[ITS_Lang]?>

일 <?php echo $SK_BO_Sun[ITS_Lang]?>
월 <?php echo $SK_BO_Mon[ITS_Lang]?>
화 <?php echo $SK_BO_Tue[ITS_Lang]?>
수 <?php echo $SK_BO_Wed[ITS_Lang]?>
목 <?php echo $SK_BO_Thu[ITS_Lang]?>
금 <?php echo $SK_BO_Fri[ITS_Lang]?>
토 <?php echo $SK_BO_Sat[ITS_Lang]?>

월별		<?php echo $SK_BO_Monthly[ITS_Lang]?>
>사용중지<   ><?php echo $SK_BO_Disable[ITS_Lang]?><
>일시정지<   ><?php echo $SK_BO_Pause[ITS_Lang]?><
>알람정지<   ><?php echo $SK_BO_Stop_Alarm[ITS_Lang]?><
>즉시적용<   ><?php echo $SK_BO_Apply[ITS_Lang]?><
>모델명<    ><?php echo $SK_BO_Model_Name[ITS_Lang]?><
>디바이스<   ><?php echo $SK_BO_Device_Name[ITS_Lang]?><
>고유번호<   ><?php echo $SK_BO_Serial_Number[ITS_Lang]?><
>감지범위<   ><?php echo $SK_BO_Detect_Range[ITS_Lang]?><
> 미터      > <?php echo $SK_BO_Meter[ITS_Lang]?>
>허용직경<   ><?php echo $SK_BO_Allowable_Diameter[ITS_Lang]?><
> 센티미터   > <?php echo $SK_BO_Cmeter[ITS_Lang]?>
>허용회수< >허용횟수<   ><?php echo $SK_BO_Event_Count[ITS_Lang]?><
> 회 >회      > <?php echo $SK_BO_Times[ITS_Lang]?>
>무시영역<   ><?php echo $SK_BO_Ignore_Area[ITS_Lang]?><
>시작좌표<   ><?php echo $SK_BO_Start_Coord[ITS_Lang]?><
>종료좌표<   ><?php echo $SK_BO_End_Coord[ITS_Lang]?><
>예약차단<   ><?php echo $SK_BO_Reservation[ITS_Lang]?><
>대기시간<   ><?php echo $SK_BO_Event_Hold[ITS_Lang]?><
>센서방향<   ><?php echo $SK_BO_Sensor_Face[ITS_Lang]?><
>센서방위<   ><?php echo $SK_BO_Sensor_Azimuth[ITS_Lang]?><
> 도       > <?php echo $SK_BO_Angle[ITS_Lang]?>
'수정':'신규'		'<?php echo $SK_BO_Modify[ITS_Lang]?>':'<?php echo $SK_BO_New[ITS_Lang]?>'	

관리명	고유 번호	센서 IP	호스트 A	호스트 B
시리얼	방향	수용량	현재량


>감지횟수<     ><?php echo $SK_BO_Event_Count[ITS_Lang]?><
>감지지역<     ><?php echo $SK_BO_Sensing_Boundary[ITS_Lang]?><
>경보유지<     ><?php echo $SK_BO_Event_Hold[ITS_Lang]?><
>거리고정<     ><?php echo $SK_BO_Hold_Distance[ITS_Lang]?><
>등록<     ><?php echo $SK_BO_Update[ITS_Lang]?><
기본설정     <?php echo $SK_BO_Basic[ITS_Lang]?>
고급설정     <?php echo $SK_BO_Advanced[ITS_Lang]?>
>관리/센서타입<     ><?php echo $SK_BO_Name[ITS_Lang]?><
>관리/모델명<     ><?php echo $SK_BO_Name[ITS_Lang]?><
"저장"     "<?php echo $SK_BO_Save[ITS_Lang]?>"
>취소<     ><?php echo $SK_BO_Cancel[ITS_Lang]?><
>허용조건<     ><?php echo $SK_BO_Allowable[ITS_Lang]?><

>시작<     ><?php echo $SK_BO_Start[ITS_Lang]?><
>종료<     ><?php echo $SK_BO_End[ITS_Lang]?><
>허용감도<     ><?php echo $SK_BO_Sensitivity[ITS_Lang]?><
>허용범주<     ><?php echo $SK_BO_Accept_Boundary[ITS_Lang]?><
>경보주기<     ><?php echo $SK_BO_Alarm_Cycle[ITS_Lang]?><
>주기고정<     ><?php echo $SK_BO_Fix_Cycle[ITS_Lang]?><
>위치<     ><?php echo $SK_BO_Location[ITS_Lang]?><
>예약<     ><?php echo $SK_BO_Reserve[ITS_Lang]?><
>사진<     ><?php echo $SK_BO_Snapshot[ITS_Lang]?><
>알람로그<     ><?php echo $SK_BO_Log[ITS_Lang]?><
>알람위치<     ><?php echo $SK_BO_Position[ITS_Lang]?><
>시작편차<     ><?php echo $SK_BO_Offset[ITS_Lang]?><
>레벨/지연<     ><?php echo $SK_BO_Level[ITS_Lang]?>/<?php echo $SK_BO_Delay[ITS_Lang]?><
(약 대략  (<?php echo $SK_BO_About[ITS_Lang]?>






허용범위  <?php echo $SK_BO_Accept_Range[ITS_Lang]?>
메뉴  <?php echo $SK_HD_Menu[ITS_Lang]?>
시간동기  <?php echo $SK_HD_Sync_Clock[ITS_Lang]?>
재부팅  <?php echo $SK_HD_Reboot[ITS_Lang]?>
정보수정  <?php echo $SK_HD_Info[ITS_Lang]?>
로그아웃  <?php echo $SK_HD_Logout[ITS_Lang]?>
로그인  <?php echo $SK_HD_Login[ITS_Lang]?>
URL(부)   <?php echo $SK_BO_URL_Mirror[ITS_Lang]?>
URL(주)   <?php echo $SK_BO_URL_Main[ITS_Lang]?>
검색  <?php echo $SK_BO_Search[ITS_Lang]?>
경보   <?php echo $SK_BO_Alert[ITS_Lang]?>
글쓰기  <?php echo $SK_BO_Write[ITS_Lang]?>
다음   <?php echo $SK_BO_Next[ITS_Lang]?>
대기  <?php echo $SK_BO_Hold[ITS_Lang]?>
라이센스   <?php echo $SK_BO_License[ITS_Lang]?>
마스터   <?php echo $SK_BO_Master[ITS_Lang]?>
모니터   <?php echo $SK_BO_Monitor[ITS_Lang]?>
목록  <?php echo $SK_BO_List[ITS_Lang]?>
방향   <?php echo $SK_BO_Direction[ITS_Lang]?>
분류  <?php echo $SK_BO_Category[ITS_Lang]?>
비밀번호  <?php echo $SK_BO_password[ITS_Lang]?>
삭제  <?php echo $SK_BO_Delete[ITS_Lang]?>
상시차단  <?php echo $SK_BO_Blocked[ITS_Lang]?>
선택하세요  <?php echo $SK_BO_Choose[ITS_Lang]?>
센서관리명  <?php echo $SK_BO_Sensor_Name[ITS_Lang]?>
수정  <?php echo $SK_BO_Modify[ITS_Lang]?>
스케줄   <?php echo $SK_BO_Schedule[ITS_Lang]?>
스트리밍   <?php echo $SK_BO_Streaming[ITS_Lang]?>
신규  <?php echo $SK_BO_New[ITS_Lang]?>
암호화   <?php echo $SK_BO_Encryption[ITS_Lang]?>
영역   <?php echo $SK_BO_Range[ITS_Lang]?>
옵션  <?php echo $SK_BO_Option[ITS_Lang]?>
이름  <?php echo $SK_BO_Name[ITS_Lang]?>
이메일  <?php echo $SK_BO_Email[ITS_Lang]?>
이벤트   <?php echo $SK_BO_Events[ITS_Lang]?>
이벤트  <?php echo $SK_BO_Event[ITS_Lang]?>
이벤트주기  <?php echo $SK_BO_Event_Cycle[ITS_Lang]?>
이전   <?php echo $SK_BO_Previous[ITS_Lang]?>
일  <?php echo $SK_BO_Day[ITS_Lang]?>
작성완료  <?php echo $SK_BO_Save2[ITS_Lang]?>
재실행  <?php echo $SK_BO_Restart[ITS_Lang]?>
주  <?php echo $SK_BO_Week[ITS_Lang]?>
지역   <?php echo $SK_BO_Zone[ITS_Lang]?>
지역차단  <?php echo $SK_BO_Area_Block[ITS_Lang]?>?>
초  <?php echo $SK_BO_Second[ITS_Lang]?>
키   <?php echo $SK_BO_Key[ITS_Lang]?>
포트  <?php echo $SK_BO_Port[ITS_Lang]?>
호스트(부)   <?php echo $SK_BO_Host_Mirror[ITS_Lang]?>
호스트(주)   <?php echo $SK_BO_Host_Main[ITS_Lang]?>
홈페이지  <?php echo $SK_BO_Home_Page[ITS_Lang]?>
*/

?>