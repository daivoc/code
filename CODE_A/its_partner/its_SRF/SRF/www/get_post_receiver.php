<?php
	// foreach ($_GET as $key => $value) {
	// 	echo "Field ".htmlspecialchars($key)." is ".htmlspecialchars($value)."<br>";
	// }
	// foreach ($_POST as $key => $value) {
	// 	echo "Field ".htmlspecialchars($key)." is ".htmlspecialchars($value)."<br>";
	// }
	foreach ($_GET as $key => $value) {
		echo "GET_Field [".$key."] --- ".$value;
	}
	foreach ($_POST as $key => $value) {
		echo "POST_Field [".$key."] --- ".$value;
	}
?>