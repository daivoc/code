<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

include_once('./sql.php'); // 최초에 한번만 실행 한다

// 언어 정의 파일 열기
include_once G5_THEME_PATH.'/its_web_lan.php';

if(!$bo_table || !$wr_id || !$wr_subject) exit; // 변수없이 접근 불가
$windowTitle = $_GET['wr_subject'];
?>

<html lang="ko">
<head>
<title><?php echo $windowTitle?></title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes">
<link href='assets/css/fullcalendar.css' rel='stylesheet' />
<link href='assets/css/fullcalendar.print.css' rel='stylesheet' media='print' />
<script src='assets/js/moment.min.js'></script>
<script src='assets/js/jquery.min.js'></script>
<script src='assets/js/jquery-ui.min.js'></script>
<script src='assets/js/fullcalendar.min.js'></script>
<script>
$(document).ready(function() {
	
	var bo_table = '<?php echo $bo_table?>';
	var wr_id = '<?php echo $wr_id?>';
	var wr_subject = '<?php echo $wr_subject?>';
	var w_sensor_serial = '<?php echo $w_sensor_serial?>';

	// 기존의 예약 정보를 json_events로 가지고 온다.
	// events: JSON.parse(json_events) - 달력에 출력
	$.ajax({
		url: 'process.php',
		type: 'POST', // Send post data
		// data: 'type=fetch&bo_table='+bo_table+'&wr_id='+wr_id+'&wr_subject='+wr_subject,
		data: 'type=fetch&bo_table='+bo_table+'&wr_id='+wr_id+'&wr_subject='+wr_subject+'&w_sensor_serial='+w_sensor_serial,
		async: false,
		success: function(s){
			json_events = s;
		}
	});

	calendar = $('#calendar').fullCalendar({
		// fetch한 내용을 화면에 보여준다.
		events: JSON.parse(json_events),

		lang: 'en',
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek'
		},
        monthNames: ['<?php echo $SK_BO_January[ITS_Lang]?>','<?php echo $SK_BO_February[ITS_Lang]?>','<?php echo $SK_BO_March[ITS_Lang]?>','<?php echo $SK_BO_April[ITS_Lang]?>','<?php echo $SK_BO_May[ITS_Lang]?>','<?php echo $SK_BO_June[ITS_Lang]?>','<?php echo $SK_BO_July[ITS_Lang]?>','<?php echo $SK_BO_August[ITS_Lang]?>','<?php echo $SK_BO_September[ITS_Lang]?>','<?php echo $SK_BO_October[ITS_Lang]?>','<?php echo $SK_BO_November[ITS_Lang]?>','<?php echo $SK_BO_December[ITS_Lang]?>'],
        monthNamesShort: ['<?php echo $SK_BO_Jan[ITS_Lang]?>','<?php echo $SK_BO_Feb[ITS_Lang]?>','<?php echo $SK_BO_Mar[ITS_Lang]?>','<?php echo $SK_BO_Apr[ITS_Lang]?>','<?php echo $SK_BO_May[ITS_Lang]?>','<?php echo $SK_BO_Jun[ITS_Lang]?>','<?php echo $SK_BO_Jul[ITS_Lang]?>','<?php echo $SK_BO_Aug[ITS_Lang]?>','<?php echo $SK_BO_Sep[ITS_Lang]?>','<?php echo $SK_BO_Oct[ITS_Lang]?>','<?php echo $SK_BO_Nov[ITS_Lang]?>','<?php echo $SK_BO_Dec[ITS_Lang]?>'],
		dayNames: ['<?php echo $SK_BO_Sunday[ITS_Lang]?>','<?php echo $SK_BO_Monday[ITS_Lang]?>','<?php echo $SK_BO_Tuesday[ITS_Lang]?>','<?php echo $SK_BO_Wednesday[ITS_Lang]?>','<?php echo $SK_BO_Thursday[ITS_Lang]?>','<?php echo $SK_BO_Friday[ITS_Lang]?>','<?php echo $SK_BO_Saturday[ITS_Lang]?>'],
		dayNamesShort: ['<?php echo $SK_BO_Sun[ITS_Lang]?>','<?php echo $SK_BO_Mon[ITS_Lang]?>','<?php echo $SK_BO_Tue[ITS_Lang]?>','<?php echo $SK_BO_Wed[ITS_Lang]?>','<?php echo $SK_BO_Thu[ITS_Lang]?>','<?php echo $SK_BO_Fri[ITS_Lang]?>','<?php echo $SK_BO_Sat[ITS_Lang]?>'],
		buttonText: {
			prev:     '<', // <
			next:     '>', // >
			prevYear: '<<',  // <<
			nextYear: '>>',  // >>
			today:    '<?php echo $SK_BO_Today[ITS_Lang]?>', // '오늘',
			month:    '<?php echo $SK_BO_Monthly[ITS_Lang]?>', // '월간',
			week:     '<?php echo $SK_BO_Weekly[ITS_Lang]?>', // '주별',
			day:      '<?php echo $SK_BO_Daily[ITS_Lang]?>', // '일별'
		},
		editable: true,
		droppable: true, 
		selectable: true,
		allDaySlot: false,
		slotDuration: '00:30:00',

		select: function(start, end, jsEvent, view) {
			var curCalView = calendar.fullCalendar('getView');
			if (curCalView.name == "month") { // 월간 달력이면 All Day등록을 맏기위해 그 날짜가 포함된 주간 달력으로 이동 한다
				calendar.fullCalendar('gotoDate',start); // 날짜로 이동
				calendar.fullCalendar('changeView','agendaWeek'); // 화면 변경
			} else {
				var today = new Date();
				// 과거 비활성
				if (start <= today.getTime()) {
					alert("Past Days");
				} else {
					var title = wr_subject;
					var startdate = start.format("YYYY-MM-DD[T]HH:mm:SS");
					var enddate = end.format("YYYY-MM-DD[T]HH:mm:SS");
					var allDay = !start.hasTime() && !end.hasTime();

					$.ajax({
						url: 'process.php',
						data: 'type=newSelect&title='+title+'&startdate='+startdate+'&enddate='+enddate+'&allDay='+allDay+'&bo_table='+bo_table+'&wr_id='+wr_id+'&wr_subject='+wr_subject+'&w_sensor_serial='+w_sensor_serial+'&w_week=0',
						type: 'POST',
						dataType: 'json',
						success: function(response){
							console.log(response)
							var event={id:response.eventid, title:title, start:startdate, end:enddate};
							calendar.fullCalendar('renderEvent', event, true);
						},
						error: function(e){
							console.log(e.responseText);
						}
					});
				}
			}
		},

		eventDrop: function(event, delta, revertFunc, jsEvent, ui, view) {
			var id = event.id;
			var title = event.title;
			var startdate = event.start.format();
			var enddate = event.end.format();
			var allDay = !event.start.hasTime() && !event.end.hasTime();
			if (jsEvent.shiftKey) { // 복사
				var curCalView = calendar.fullCalendar('getView');
				if (curCalView.name == "month") { // 월간 달력이면 All Day등록을 맏기위해 그 날짜가 포함된 주간 달력으로 이동 한다
					$.ajax({
						url: 'process.php',
						data: 'type=newSelect&title='+title+'&startdate='+startdate+'&enddate='+enddate+'&allDay='+allDay+'&bo_table='+bo_table+'&wr_id='+wr_id+'&wr_subject='+wr_subject+'&w_week=0',
						type: 'POST',
						dataType: 'json',
						success: function(response){
							console.log(response)
							if(response.status != 'success') {
								revertFunc();
							} else {
								location.reload(); // 페이지를 새로고침
							}
						},
						error: function(e){
							console.log(e.responseText);
						}
					});
				} else {
					revertFunc();
					alert('Copy Function Will Not Work In Week View');
					location.reload(); // 페이지를 새로고침
				}
			} else {
				$.ajax({
					url: 'process.php',
					data: 'type=moveEvent&title='+title+'&startdate='+startdate+'&enddate='+enddate+'&eventid='+id,
					type: 'POST',
					dataType: 'json',
					success: function(response){
						console.log(response)
						if(response.status != 'success')		    				
							revertFunc();
					},
					error: function(e){		    			
						revertFunc();
						alert('Error processing your request: '+e.responseText);
					}
				});
			}			
		},
		
		eventResize: function(event, delta, revertFunc) {
			var title = event.title;
			var startdate = event.start.format();
			var enddate = event.end.format();
			var allDay = !event.start.hasTime() && !event.end.hasTime();
			$.ajax({
				url: 'process.php',
				data: 'type=resizeEvent&title='+title+'&startdate='+startdate+'&enddate='+enddate+'&eventid='+event.id,
				type: 'POST',
				dataType: 'json',
				success: function(response){
					console.log(response)
					if(response.status != 'success')	    				
					revertFunc();
				},
				error: function(e){		    			
					revertFunc();
					alert('Error processing your request: '+e.responseText);
				}
			});
		},

		// https://fullcalendar.io/docs1/event_data/Event_Object/
		eventClick: function(event, jsEvent, view) {
			var con = confirm('<?php echo $SK_BO_Delete_event[ITS_Lang]?> ID: '+event.id);
			if(con == true) {
				$.ajax({
					url: 'process.php',
					data: 'type=remove&eventid='+event.id,
					type: 'POST',
					dataType: 'json',
					success: function(response){
						console.log(response);
						if(response.status == 'success'){
							calendar.fullCalendar('removeEvents', event.id);
						}
					},
					error: function(e){	
						alert('Error processing your request: '+e.responseText);
					}
				});
			}   
		},
	});
});
</script>
<style>
.wr_subject { font-weight: bold; border-radius:3px; margin:4px 0; padding:4px 0;color:white; }
</style>
</head>
<body>
<div id="bo_list" class="container">
	<div style="margin:10px;text-align:center;">
		<div id='wrap'>
			<div class='fc-event wr_subject'><?php echo $wr_subject?></div>
			<div id='calendar'></div>
			<div style='clear:both'></div>
		</div>
	</div>
</div>
</body>
</html>
<?php
// include_once(G5_THEME_PATH.'/tail.php');
// include_once(G5_PATH.'/tail.php');
?>