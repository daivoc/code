<?php
$cfg = json_decode(file_get_contents("./SRF/config/config.json"), TRUE);
?>
<html><head>
<script>
<?php include $cfg["path"]["common"]."/jquery/jquery-3.1.1.min.js";?>
</script>
<script>
$(document).ready(function(){
	$("#logo").click(function(){
		// get the href attribute
		var newUrl = 'http://<?php echo $_SERVER['SERVER_NAME'].":".$cfg["interface"]["portOut"]?>';
		location = newUrl;
	});
	$("#upload").click(function(){
		if(confirm("Do you want upload your config.json?")){ 
			$("#selectJson").click();
		}
	});
	$("#selectJson").change(function(){
		$("#submitUpload").click();
	});
	$("#reset").click(function(){
		if(confirm("Do you want reset config?")){ 
			$("#submitReset").click();
		}
	});
	$("#restart").click(function(){
		if(confirm("Do you want restart system?")){ 
			$("#submitRestart").click();
		}
	});
});
</script>
<style>
body {height:100%;margin:0;padding:0; background-color:black; } 
form {display: none;} 
.config {position: absolute;top: 0;right: 0;}
.button { background-color: #00000080; color: silver; padding: 2px 6px; font-size: 8pt; text-align: center; text-decoration: none; display: block; cursor: pointer; margin:1px;} 
.button:hover { background-color: #00000040; color: white; }
#logo { background:white url(http://<?php echo $_SERVER['SERVER_NAME'].$cfg["path"]["img"].$cfg["file"]["img_logo_home"]?>) center center no-repeat; position: absolute; top:0; bottom: 0; left: 0; right: 0; margin: auto; }
</style>
</head>
<body>
<div id='logo'></div>
<a style='display:none;' href='http://<?php echo $_SERVER['SERVER_NAME'].":".$cfg["interface"]["portOut"]?> '><svg viewBox='0 0 1600 900'><rect fill='#ff7700' width='1600' height='900'/><polygon fill='#cc0000' points='957 450 539 900 1396 900'/><polygon fill='#aa0000' points='957 450 872.9 900 1396 900'/><polygon fill='#d6002b' points='-60 900 398 662 816 900'/><polygon fill='#b10022' points='337 900 398 662 816 900'/><polygon fill='#d9004b' points='1203 546 1552 900 876 900'/><polygon fill='#b2003d' points='1203 546 1552 900 1162 900'/><polygon fill='#d3006c' points='641 695 886 900 367 900'/><polygon fill='#ac0057' points='587 900 641 695 886 900'/><polygon fill='#c4008c' points='1710 900 1401 632 1096 900'/><polygon fill='#9e0071' points='1710 900 1401 632 1365 900'/><polygon fill='#aa00aa' points='1210 900 971 687 725 900'/><polygon fill='#880088' points='943 900 1210 900 971 687'/></svg></a>
<form action='SRF/upload.php' method='post' enctype='multipart/form-data' id='fileToUpload'>
	<input type='file' name='selectJson' id='selectJson'>
	<input type='submit' value='' name='submitUpload' id='submitUpload'>
</form>
<form action='SRF/reset.php' method='post' enctype='multipart/form-data' id='fileToUpload'>
	<input type='submit' value='' name='submitReset' id='submitReset'>
</form>
<form action='SRF/restart.php' method='post' enctype='multipart/form-data' id='fileToUpload'>
	<input type='submit' value='' name='submitRestart' id='submitRestart'>
</form>
<div class='config'>
<a href='<?php echo $cfg["path"]["config"].$cfg["file"]["config"]?>' download='config.json' class='button'>Save Config</a>
<a href='#' class='button' id="upload">Upload Config</a>
<a href='#' class='button' id="reset">Reset Config</a>
<a href='#' class='button' id="restart">Restart Server</a>
</div>
</body>
</html>