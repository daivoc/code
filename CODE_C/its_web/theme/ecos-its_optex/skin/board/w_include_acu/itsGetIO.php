<?php
$configACU = json_decode(file_get_contents('/home/pi/common/config.json', true), true);
?>

<link href="<?php echo G5_THEME_URL.'/js/bootstrap-toggle-master/css/bootstrap-toggle.min.css' ?>" rel="stylesheet">
<script src="<?php echo G5_THEME_URL.'/js/bootstrap-toggle-master/js/bootstrap-toggle.min.js' ?>"></script>
<style>
	.toggle.acuBtn {margin:4px 2px;}
	.groupSetACU {text-align: center;}
	.groupSetPOW {text-align: center;}
</style>
<div class="groupSetACU">
	<input id="io01" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S01" data-off="S01" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io01"])?"checked":"";?>>
	<input id="io02" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S02" data-off="S02" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io02"])?"checked":"";?>>
	<input id="io03" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S03" data-off="S03" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io03"])?"checked":"";?>>
	<input id="io04" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S04" data-off="S04" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io04"])?"checked":"";?>>
	<input id="io05" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S05" data-off="S05" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io05"])?"checked":"";?>>
	<input id="io06" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S06" data-off="S06" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io06"])?"checked":"";?>>
	<input id="io07" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S07" data-off="S07" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io07"])?"checked":"";?>>
	<input id="io08" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S08" data-off="S08" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io08"])?"checked":"";?>>
	<input id="io09" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R01" data-off="R01" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io09"])?"checked":"";?>>
	<input id="io10" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R02" data-off="R02" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io10"])?"checked":"";?>>
	<input id="io11" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R03" data-off="R03" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io11"])?"checked":"";?>>
	<input id="io12" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R04" data-off="R04" <?php echo ($configACU["ioBoard"]["its"]["setIO"]["io12"])?"checked":"";?>>
</div>
<div class="groupSetPOW">
	<input id="pw01" class="setPOW" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="danger" data-on="V12" data-off="0V" <?php echo ($configACU["ioBoard"]["its"]["setPW"]["pw01"])?"checked":"";?>>
</div>

<script>
$(function() {
	$('.setACU').change(function() {
		$('#console-event').html('Toggle: ' + $(this).prop('checked'))
	});
	$('#confirm').click(function() {
		if (confirm('Are you sure you want to save this thing into the configuration?')) {
		// Save it!
		// console.log('Thing was saved to the database.');
		updateJSON()
		} else {
		location.reload();
		// Do nothing!
		// console.log('Thing was not saved to the database.');
		}
	});
});

function updateJSON(data) {
	$.ajax({
		url: '<?php echo $board_skin_url."/../w_include_acu/acuSetIO.php" ?>',
		type: "POST",
		// data: { setIO : createJSON() },
		data: createJSON(),
		success : function(data) {
			if(data) alert(data);
		}
	});
}

function createJSON() {
	var jsonObj = '{ "setIO" : {';
	$(".setACU").each(function() {
		jsonObj += '"'+$(this).attr("id")+'":'+$(this).is(":checked")+',';
		// jsonObj += $(this).attr("id")+':'+$(this).is(":checked")+',';
	});
	jsonObj = jsonObj.slice(0, -1);
	jsonObj += '}, "setPW" : {';

	$(".setPOW").each(function() {
		jsonObj += '"'+$(this).attr("id")+'":'+$(this).is(":checked")+',';
		// jsonObj += $(this).attr("id")+':'+$(this).is(":checked")+',';
	});
	jsonObj = jsonObj.slice(0, -1);
	jsonObj += '} }';
	jsonArr = JSON.parse(jsonObj);
	// console.log(jsonArr);
	return jsonArr;
}

</script>
