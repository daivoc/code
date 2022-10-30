<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

$isITS_M = $_POST['isITS_M'];
$theme_url = "/theme/ecos-its_optex";

if($isITS_M) {
	$cfgJson = file_get_contents("/home/pi/MONITOR/config.json");
	if ($cfgJson) {
		print '<script>var config = ' . $cfgJson . ';</script>';
	}
} else {
	die();
}
?>

<script>
// function upload() {
$('#upload').on('click', function () {
	var r = confirm("Monitoring Map Uploading.");
	if (r == true) {
		var file_data = $('#file').prop('files')[0];
		var form_data = new FormData();
		form_data.append('file', file_data);
		$.ajax({
			url: '<?php echo $theme_url?>/utility/systemExec/upload.php', // point to server-side PHP script 
			type: 'POST',
			data: form_data,
			dataType: 'text', // what to expect back from the PHP script
			cache: false,
			contentType: false,
			processData: false,
			success: function (response) {
				$('#msg').html(response); // display success response from the PHP script
			},
			error: function (response) {
				$('#msg').html(response); // display error response from the PHP script
			}
		});
	}
});
// function upload() {
$('#uploadLogo').on('click', function () {
	var r = confirm("Logo Uploading.");
	if (r == true) {
		var file_data = $('#fileLogo').prop('files')[0];
		var form_data = new FormData();
		form_data.append('file', file_data);
		$.ajax({
			url: '<?php echo $theme_url?>/utility/systemExec/uploadLogo.php', // point to server-side PHP script 
			dataType: 'text', // what to expect back from the PHP script
			cache: false,
			contentType: false,
			processData: false,
			data: form_data,
			type: 'post',
			success: function (response) {
				$('#msgLogo').html(response); // display success response from the PHP script
			},
			error: function (response) {
				$('#msgLogo').html(response); // display error response from the PHP script
			}
		});
	}
});

function openPop(title, msg){
	w = window.open('', title, "status=no,scrollbars=no,width=400,height=300");
	w.document.writeln('<html><head><title>'+title+'</title></head>');
	w.document.writeln('<body bgcolor=white onLoad="self.focus()">');
	w.document.writeln('<h3>'+title+'</h3><pre style="font-size: 9pt;color: gray;">'+msg+'</pre>');
	w.document.writeln('</body></html>');
	w.document.close()
	return false;
}
function its_log() {
	window.open("<?php echo $theme_url?>/utility/filemanager/fm.php?ID=its&PATH=data||log", "Log View", "width=640,height=400,scrollbars=no");
}
function ims_log() {
	window.open("<?php echo $theme_url?>/utility/status/list_IMS.php", "IMS Log View", "width=800,height=800,scrollbars=yes");
}
function test_out_relay() {
	var r = confirm("Testing Output Relay");
	if (r == true) {
		openPop("Testing Output Relay", "Please wait...");
		$.ajax({
			url : "<?php echo $theme_url?>/utility/systemExec/testOutRelay.php",
		}).done(function(data) {
			console.log(data);
			// alert(data);
			openPop("Testing Output Relay", data);
		});
	}
}
function test_power_control() {
	var r = confirm("Testing Power Control");
	if (r == true) {
		openPop("Testing Power Control", "Testing Power Control can take up to 60 seconds to 90 seconds.\nReboot the ITS after the sensor is in normal operation.\nPlease wait...");
		$.ajax({
			url : "<?php echo $theme_url?>/utility/systemExec/resetSensor.php",
		}).done(function(data) {
			console.log(data);
			// alert(data);
			openPop("Testing Power Control", data);
		});
	}
}
function find_optexDevice() {
	var r = confirm("Find Optex ITS and RLS, Camera");
	if (r == true) {
		openPop("Find Optex Device", "Finding now. It's take up to 30 sec. Please wait...");
		$.ajax({
			url : "<?php echo $theme_url?>/utility/systemExec/findOptexDevice.php",
		}).done(function(data) {
			console.log(data);
			// alert(data);
			openPop("Find Optex Device", data);
		});
	}
}
function its_power_off() {
	var r = confirm("Must be turn on power manually for using ITS operation.");
	if (r == true) {
		$.ajax({
			url : "<?php echo $theme_url?>/utility/systemExec/poweroff.php",
		}).done(function(data) {
			console.log(data);
			// alert(data);
			openPop("its_power_off", data);
		});
	}
}
function restart_ims() {
	var r = confirm("Restart IMS.");
	if (r == true) {
		$.ajax({
			url : "<?php echo $theme_url?>/utility/systemExec/restartIMS.php",
		}).done(function(data) {
			console.log(data);
			// alert(data);
			openPop("restart_ims", data);
		});
	}
}
</script>

<style>
textarea {resize: none;}
.s1 { margin: 28px 8px; padding: 8px;border: 1px solid silver;display: inline-grid; width:48%; float: left; font-size: 12pt; border-radius: 6px;background: #f8f8f8; }
.s2 { margin-left: 18px; font-size: 10pt; }
.s3 { background: silver;color: white;padding: 4px 10px;margin-bottom: 10px;border-radius: 4px;font-weight: bold; }
.s4 { font-weight: bold;color: gray;display: list-item;margin-left: 10px; }
.s5 { width: 100%;border: 1px solid silver;border-radius: 4px;padding: 0 4px;font-size: 8pt;color: gray; }
.s6 { display: flex;padding: 4px 8px;color: gray; }
.s7 { width: 100%;margin:6px 0; }
@media (max-width: 1000px) {
	.s1 { width: 100%;}
}
</style>

<div class = 's1'><div class = 's3'>Map and Logo Manager</div>
	<span class = 's2'>
		<div class = 's4'>Map Upload</div>
		<a class = 's6'><input type="file" id="file" name="file" /><button id="upload">Upload Map</button></a>
		<div style="color: green;" id="msg"></div>
	</span>
	<span class = 's2'>
		<div class = 's4'>Logo Upload(300/100)</div>
		<a class = 's6'><input type="file" id="fileLogo" name="fileLogo" /><button id="uploadLogo">Upload Logo</button></a>
		<div style="color: green;" id="msgLogo"></div>
	</span>
	<span class = 's2'>
		<a href="<?php echo $theme_url?>/utility/svgIMS/svgIMS.php"><button class = 's7'>Map Manager</button></a>
		<a href="<?php echo $g5_url?>/data/image/ims/ims_map.svg" download="currentMap.svg"><button class = 's7'>Download Map</button></a>
	</span>
</div>

<div class = 's1'><div class = 's3'>User IP Filtering</div>
	<span class = 's2'>
		<div class = 's4'>Admin</div>
		<textarea id="filterAdmin" class = 's5' placeholder="Ex) 192.168.0.10,192.168.0.20"></textarea>
	</span>
	<span class = 's2'>
		<div class = 's4'>Manager</div>
		<textarea id="filterManager" class = 's5' placeholder="Ex) 192.168.0.10,192.168.0.20"></textarea>
	</span>
	<span class = 's2'>
		<div class = 's4'>Viewer</div>
		<textarea id="filterViewer" class = 's5' placeholder="Ex) 192.168.0.10,192.168.0.20"></textarea>
	</span>
	<span class = 's2' style="text-align: right;">
		<button id="saveFilterID" onclick="setFilterIP()">Save</button>
	</span>
</div>

<script>
if(config) { // IMS
	$("#filterAdmin").text(config.filterIP.admin);
	$("#filterManager").text(config.filterIP.manager);
	$("#filterViewer").text(config.filterIP.viewer);

	function isValidIP(str) {
		return str.split('.').filter(function(v){return v==Number(v).toString() && Number(v)<256}).length==4;
	}
		
	function arrPush(id, val) {
		config.filterIP[id] = [];
		var str_array = document.getElementById(val).value.split(',');
		for(var i = 0; i < str_array.length; i++) {
			str_array[i] = str_array[i].replace(/^\s*/, "").replace(/\s*$/, "");
			if(isValidIP(str_array[i])) {
				config.filterIP[id].push(str_array[i]);
			}
		}
	}

	function setFilterIP() {
		arrPush("admin", "filterAdmin");
		arrPush("manager", "filterManager");
		arrPush("viewer", "filterViewer");
		// config.filterIP.admin = document.getElementById("filterAdmin").value;
		// config.filterIP.manager = document.getElementById("filterManager").value;
		// config.filterIP.viewer = document.getElementById("filterViewer").value;
		$.ajax({
			type: 'POST',
			url: '<?php echo $theme_url?>/utility/systemExec/imsConfigSave.php', // point to server-side PHP script 
			data: {'config': JSON.stringify(config)},
			success: function (data) {
				location.reload(true);;
			},
			error: function (data) {
				alert("error");
			}
		});
	}
}
</script>
