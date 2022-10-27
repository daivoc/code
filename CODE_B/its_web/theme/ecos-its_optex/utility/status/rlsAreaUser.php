<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");

// nodeIn=50198&devideID=ETH1_192.168.168.10&sensorID=g200t210_192_168_0_201_0004&bo_table=g200t210&wr_id=&subject=RLS2020I

if (!file_exists(G5_CU_MAP_PATH)) {
    mkdir(G5_CU_MAP_PATH, 0755, true);
}
$targetFile = G5_CU_MAP_PATH . "/" . "$nodeIn.svg";
$targetURL = G5_CU_MAP_URL . "/" . "$nodeIn.svg";
echo $targetURL
?>

<?php
if(isset($_POST['submit'])) {
	if ($_FILES["fileIS"]["error"] > 0) {
		echo "Error: " . $_FILES["fileIS"]["error"] . "<br />";
	} else {
		if (move_uploaded_file($_FILES["fileIS"]["tmp_name"], $targetFile)) {
			echo "<a href=$targetURL style='text-decoration-line: none;color:gray;font-size:8pt;'>The file has been uploaded.</a>";
		} else {
			echo "<pre>".$targetFile."<br />Sorry, there was an error uploading... - ".$_FILES["fileIS"]["name"]."</pre>";
		}
		
		// echo "<pre>";
		// echo "Name: " . $_FILES["fileIS"]["name"] . "<br />";
		// echo "Type: " . $_FILES["fileIS"]["type"] . "<br />";
		// echo "Size: " . ($_FILES["fileIS"]["size"] / 1024) . " Kb<br />";
		// echo "Stored in: " . $_FILES["fileIS"]["tmp_name"];
		// echo "</pre>";


	}
}
?>

<script src="<?php echo G5_THEME_JS_URL; ?>/jquery.min.js"></script>
	
<script type="text/javascript">
$(document).ready(function(){
	
	$("#frameURL").attr("src","<?php echo G5_THEME_URL ?>/utility/nodeJs_table/realtime_RLS_<?php echo $nodeIn ?>_Area.html");
	
	// Iframe내에 출력된 목록의 자료를 표시한다.
	var iframe = $('#frameURL');
	iframe.load(function () {
		console.log('iframe loaded');
		var frame = iframe.contents().find('#rls_event');
		console.log('frame html = ' + frame.html("<?php echo $svg_element ?>")); // This works!
	});

});
</script>

<form enctype="multipart/form-data" method="post">
	<input type="file" name="fileIS" id="fileIS" style="font-size: 8pt;" /> 
	<input type="submit" name="submit" value="Submit" style="font-size: 8pt; color: gray;" />
</form>


<div style='width: 100%;text-align: center;'>
<iframe id="frameURL" name="frameURL" src="" scrolling="no" style="width: 99%;border-width: 0;height: 99%;"></iframe>
</div>
