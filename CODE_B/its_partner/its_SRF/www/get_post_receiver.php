<?php
	// foreach ($_GET as $key => $value) {
	// 	echo "Field ".htmlspecialchars($key)." is ".htmlspecialchars($value)."<br>";
	// }
	// foreach ($_POST as $key => $value) {
	// 	echo "Field ".htmlspecialchars($key)." is ".htmlspecialchars($value)."<br>";
	// }

	// echo $_SERVER['QUERY_STRING'];
	// echo $_SERVER['REQUEST_URI'];
	foreach ($_GET as $key => $value) {
		echo "GET Key - ".$key.", Value - ".$value;
	}
	foreach ($_POST as $key => $value) {
		// echo "POST_Field [".$key."] --- ".$value;
		echo "POST Key - ".$key.", Value - ".$value;
	}
?>