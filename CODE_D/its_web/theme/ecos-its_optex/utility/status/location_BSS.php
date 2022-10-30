<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// Google API Key: AIzaSyDESbpI10ETJXB0DKgYV6PI_xnb68UPM98



// 목록보기 링크
$list_view_link = 'list_BSS.php';

// USB 드라이버 관련 device port
global $g5, $bo_table;

// 목록보기 링크
$write_table = $g5['write_prefix'] . G5_CU_CONF_BSS;
$sql = " SELECT * FROM $write_table WHERE w_sensor_disable = 0 ORDER BY w_device_id ASC";
$result = sql_query($sql);
$num_rows = sql_num_rows($result); // 자료 갯수
while ($row = sql_fetch_array($result)) {
	// ['동문 북능선 3번 센서', 37.5359859, 127.0885968, URL],
	$location_info .= "['".$row['wr_subject']."', ".$row['w_sensor_lat_s'].", ".$row['w_sensor_lng_s'].", ".$row['w_sensor_lat_e'].", ".$row['w_sensor_lng_e'].",'./".$list_view_link."?commType=ttyUSB&devideID=".$row['w_device_id']."&w_id=".$row['w_id']."&subject=".$row['wr_subject']."'],";
	// $location_path .= "{lat: ".$row['w_sensor_lat_s'].", lng: ".$row['w_sensor_lng_s']."},";
	$w_sensor_lat += $row['w_sensor_lat_s']; 
	$w_sensor_lat += $row['w_sensor_lat_e'];
	$w_sensor_lng += $row['w_sensor_lng_s'];
	$w_sensor_lng += $row['w_sensor_lng_e'];
}


if($num_rows) { // 지도의 위치값을 평균 내어 중앙에 위치하는 좌표를 검출한다.
	$myLat = $w_sensor_lat / $num_rows / 2; // 중앙에 위치하는 좌표를 검출을 위한 평균값
	$myLng = $w_sensor_lng / $num_rows / 2; // 중앙에 위치하는 좌표를 검출을 위한 평균값
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
		zoom: 18,
		// mapTypeId: google.maps.MapTypeId.SATELLITE, // 위성
		center: myLatLng
	});
	google.maps.event.addListener(map, 'click', function(event) {
		var curLoc = 'Lat: ' + event.latLng.lat() + ' Lon: ' + event.latLng.lng();
		document.getElementById("location").innerHTML = curLoc;
	});

	// 여러 마커 위치 기능 
	var locationInfo = [
	<?php echo $location_info ?>
	];
	for (var i = 0; i < locationInfo.length; i++) {
		var beach = locationInfo[i];
		var marker = new google.maps.Marker({
			title: beach[0],
			position: {lat: beach[1], lng: beach[2]},
			url: beach[5],
			map: map,
			icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
			animation: google.maps.Animation.DROP,
		});
		google.maps.event.addListener(marker, 'click', function() {
		  window.location.href = this.url;
		});
		var beach = locationInfo[i];
		var marker = new google.maps.Marker({
			title: beach[0],
			position: {lat: beach[3], lng: beach[4]},
			url: beach[5],
			map: map,
			icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
			animation: google.maps.Animation.DROP,
		});
		google.maps.event.addListener(marker, 'click', function() {
		  window.location.href = this.url;
		});
		
		var locationPath = [{lat: beach[1], lng: beach[2]},{lat: beach[3], lng: beach[4]}];
		var polylines = new google.maps.Polyline({
			path: locationPath,
			geodesic: true,
			strokeColor: '#FFFF00',
			strokeOpacity: 0.6,
			strokeWeight: 8
		});
		polylines.setMap(map);
	}	
	marker.setMap(map);
	
	// // 마커간 선 연결 기능
	// var locationPath = [
	// <?php echo $location_path ?>
	// ];
	// var polylines = new google.maps.Polyline({
		// path: locationPath,
		// geodesic: true,
		// strokeColor: '#FFFF00',
		// strokeOpacity: 1.0,
		// strokeWeight: 2
	// });
	// polylines.setMap(map);
}

</script>
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDESbpI10ETJXB0DKgYV6PI_xnb68UPM98&signed_in=true&callback=initMap" async defer>
</script>

<?php
// include_once(G5_THEME_PATH.'/tail.php');
include_once(G5_PATH.'/tail.php');
?>