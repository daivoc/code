<?php
include_once('./_common.php');

// Google API Key: AIzaSyDESbpI10ETJXB0DKgYV6PI_xnb68UPM98
// 센서 정보 테이블
$bo_table_info = 'g100t100';
// USB 드라이버 관련 device port
global $g5, $bo_table;
$write_table = $g5['write_prefix'] . $bo_table_info;
$sql = " SELECT * FROM $write_table ";
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
while ($row = sql_fetch_array($result)) {
	// ['동문 북능선 3번 센서', 37.5359859, 127.0885968],
	$location_info .= "['".$row['wr_subject']."', ".$row['w_sensor_lat_s'].", ".$row['w_sensor_lng_s']."],";
	$location_path .= "{lat: ".$row['w_sensor_lat_s'].", lng: ".$row['w_sensor_lng_s']."},";
	$w_sensor_lat_s += $row['w_sensor_lat_s'];
	$w_sensor_lng_s += $row['w_sensor_lng_s'];
}

if($num_rows) { // 지도 내용이 있을때 실행 한다.
	$myLat = $w_sensor_lat_s / $num_rows; // 중앙에 기본 지도 위치를
	$myLng = $w_sensor_lng_s / $num_rows;
} else { // GOP: 38.0151491,126.8313116
	$myLat = 38.0151491; // 중앙에 기본 지도 위치를
	$myLng = 126.8313116;
}

if (G5_IS_MOBILE) {
    include_once G5_MOBILE_PATH.'/index.php';
    return;
}
include_once G5_PATH.'/head.php';

$board['bo_subject'] = "Sensor Location";
?>
<section class="success" id="header" style="padding:0;">
    <div class="container">
        <div class="intro-text">
            <span class="name"><?php echo $board['bo_subject'] ?><span class="sound_only"> 목록</span></span>
            <hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>
<!-- 게시판 목록 시작 { -->
<div id="map" style="width:100%; height: 600px;"></div>
<div id="location"></div>
<script>
function initMap() {
	var myLatLng = {lat: <?php echo $myLat?>, lng: <?php echo $myLng?>}; // GOP: 38.0151491,126.8313116 Office: 37.5359859, 127.0885968
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 16,
		mapTypeId: google.maps.MapTypeId.SATELLITE, // 위성
		center: myLatLng
	});
	google.maps.event.addListener(map, 'click', function(event) {
		var curLoc = 'Lat: ' + event.latLng.lat() + ' Lon: ' + event.latLng.lng();
		document.getElementById("location").innerHTML = curLoc;
	});
	setMarkers(map);
	// var marker = new google.maps.Marker({
		// position: myLatLng,
		// map: map,
		// title: 'Hello World!'
	// });
	
	// 마크간 선으로 연결 기능
	var locationPath = [
	<?php echo $location_path ?>
	];
	var polylines = new google.maps.Polyline({
	path: locationPath,
	geodesic: true,
	strokeColor: '#FF0000',
	strokeOpacity: 1.0,
	strokeWeight: 2
	});
	polylines.setMap(map);

}

var locationInfo = [
<?php echo $location_info ?>
];
function setMarkers(map) {
	var wits_l_f = {
		url: 'img/wits_l_f.png',
		size: new google.maps.Size(34, 40),
		origin: new google.maps.Point(0, 0),
		anchor: new google.maps.Point(0, 34)
	};
	var wits_l_b = {
		url: 'img/wits_l_b.png',
		size: new google.maps.Size(34, 40),
		origin: new google.maps.Point(0, 0),
		anchor: new google.maps.Point(0, 34)
	};
	var wits_w_f = {
		url: 'img/wits_w_f.png',
		size: new google.maps.Size(40, 34),
		origin: new google.maps.Point(0, 0),
		anchor: new google.maps.Point(0, 40)
	};
	var wits_w_b = {
		url: 'img/wits_w_b.png',
		size: new google.maps.Size(40, 34),
		origin: new google.maps.Point(0, 0),
		anchor: new google.maps.Point(0, 40)
	};
	var shape = {
		coords: [1, 1, 1, 20, 18, 20, 18, 1],
		type: 'poly'
	};
	for (var i = 0; i < locationInfo.length; i++) {
		var beach = locationInfo[i];
		var marker = new google.maps.Marker({
			position: {lat: beach[1], lng: beach[2]},
			map: map,
			// icon: wits_w_f,
			// shape: shape,
			title: beach[0],
		});
	}
}
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDESbpI10ETJXB0DKgYV6PI_xnb68UPM98&signed_in=true&callback=initMap" async defer>
</script>

</section>
<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>