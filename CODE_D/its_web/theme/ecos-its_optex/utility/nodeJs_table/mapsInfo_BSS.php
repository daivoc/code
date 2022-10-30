<?php
/*::  This routine calculates the distance between two points    :*/
function distance($lat1, $lon1, $lat2, $lon2, $unit) {
	$theta = $lon1 - $lon2;
	$dist = sin(deg2rad($lat1)) * sin(deg2rad($lat2)) +  cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * cos(deg2rad($theta));
	$dist = acos($dist);
	$dist = rad2deg($dist);
	$miles = $dist * 60 * 1.1515;
	$unit = strtoupper($unit);
	if ($unit == "K") {
		return ($miles * 1.609344);
	} else if ($unit == "N") {
		return ($miles * 0.8684);
	} else {
		return $miles;
	}
}

// echo distance(32.9697, -96.80322, 29.46786, -98.53506, "M") . " Miles<br>";
// echo distance(32.9697, -96.80322, 29.46786, -98.53506, "K") . " Kilometers<br>";
// echo distance(32.9697, -96.80322, 29.46786, -98.53506, "N") . " Nautical Miles<br>";

// if($num_rows) { // 지도 내용이 있을때 실행 한다.
	// $myLatS = $w_sensor_lat_s / $num_rows; // 중앙에 기본 지도 위치를
	// $myLngS = $w_sensor_lng_s / $num_rows;
// } else { // GOP: 38.0151491,126.8313116
	// $myLatS = 38.0151491; // 중앙에 기본 지도 위치를
	// $myLngS = 126.8313116;
// }

$myLatS = $_GET['myLatS'];
$myLngS = $_GET['myLngS'];
$myLatE = $_GET['myLatE'];
$myLngE = $_GET['myLngE'];
$get_location = $_GET['get_location'];
$windowTitle = $_GET['wr_subject'];

?>

<!DOCTYPE html>
<html>
<head>
<title><?php echo $windowTitle?></title>
<meta name="viewport" content="initial-scale=1.0">
<meta charset="utf-8">
<style>
html, body { height: 100%; margin: 0; padding: 0; }
#map { height: 100%; }
#location { font-size: small; }
</style>
</head>
<body>
<div id="location"></div>
<div id="map"></div>
<?php
if($myLatS && $myLngS && $myLatE && $myLngE) {
	$myLatC = ($myLatS + $myLatE) / 2; // 중심
	$myLngC = ($myLngS + $myLngE) / 2; // 중심
} else {
	$myLatS = 36.361625637870866; // 중앙에 기본 지도 위치를
	$myLngS = 127.38476189814764;
	$myLatE = 36.361625637870866; // 중앙에 기본 지도 위치를
	$myLngE = 127.385049390213;
	$myLatC = ($myLatS + $myLatE) / 2; // 중심
	$myLngC = ($myLngS + $myLngE) / 2; // 중심
}
?>
<script>
// function angleFromCoordinate() {
	// double lat1 = window.opener.document.getElementById('w_sensor_lat_s').value;
	// double long1 = window.opener.document.getElementById('w_sensor_lng_s').value;
	// double lat2 = window.opener.document.getElementById('w_sensor_lat_e').value;
	// double long2 = window.opener.document.getElementById('w_sensor_lng_e').value;

    // double dLon = (long2 - long1);

    // double y = Math.sin(dLon) * Math.cos(lat2);
    // double x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);

    // double brng = Math.atan2(y, x);

    // brng = Math.toDegrees(brng);
    // brng = (brng + 360) % 360;
    // brng = 360 - brng;

    // // return brng;
    // alert(brng);
// }

function initMap() {
	// var myLatLngS = {lat: <?php echo $myLatS?>, lng: <?php echo $myLngS?>}; // GOP: 38.0151491,126.8313116 Office: 37.5359859, 127.0885968
	var myLatLngS = new google.maps.LatLng(<?php echo $myLatS?>, <?php echo $myLngS?>);
	var myLatLngE = new google.maps.LatLng(<?php echo $myLatE?>, <?php echo $myLngE?>);
	var myLatLngC = new google.maps.LatLng(<?php echo $myLatC?>, <?php echo $myLngC?>);
	var map = new google.maps.Map(document.getElementById('map'), {
		// mapTypeId: google.maps.MapTypeId.SATELLITE, // 위성
		center: myLatLngC,
		zoom: 18
	});
	var markerS = new google.maps.Marker({
		position: myLatLngS,
		map: map,
		icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
		// title: 'Hello World!'
		<?php if($get_location) { // 입력 모드에서 자신을 실행했다면 부모에게 정보 전달 ?>
		draggable: true,
		<?php } ?>
		animation: google.maps.Animation.DROP,
	});
	
	var markerE = new google.maps.Marker({
		position: myLatLngE,
		map: map,
		icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
		// title: 'Hello World!'
		<?php if($get_location) { // 입력 모드에서 자신을 실행했다면 부모에게 정보 전달 ?>
		draggable: true,
		<?php } ?>
		animation: google.maps.Animation.DROP,
	});
	google.maps.event.addListener(map, 'click', function(event) {
		var curLoc = 'Lat: ' + event.latLng.lat() + ' Lng: ' + event.latLng.lng();
		document.getElementById("location").innerHTML = curLoc;
	});
	
	var locationPath = [{lat: <?php echo $myLatS?>, lng: <?php echo $myLngS?>},{lat: <?php echo $myLatE?>, lng: <?php echo $myLngE?>}];
	var polylines = new google.maps.Polyline({
		path: locationPath,
		geodesic: true,
		strokeColor: '#FFFF00',
		strokeOpacity: 0.6,
		strokeWeight: 8
	});
	polylines.setMap(map);

	<?php if($get_location) { // 입력 모드에서 자신을 실행했다면 부모에게 정보 전달 ?>
	google.maps.event.addListener(markerS,'dragend',function(event){
		window.opener.document.getElementById('w_sensor_lat_s').value = event.latLng.lat();
		window.opener.document.getElementById('w_sensor_lng_s').value = event.latLng.lng();
    });
	google.maps.event.addListener(markerE,'dragend',function(event){
		window.opener.document.getElementById('w_sensor_lat_e').value = event.latLng.lat();
		window.opener.document.getElementById('w_sensor_lng_e').value = event.latLng.lng();
		// angleFromCoordinate();
    });
	<?php } ?>
}
</script>

<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAztSXHe3LZ9oUinN0jPdCBPjGiP_EDWzI&signed_in=true&callback=initMap"></script>
</body>
</html>