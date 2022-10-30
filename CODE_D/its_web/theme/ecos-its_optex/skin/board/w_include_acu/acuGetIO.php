<?php
include_once('./_common.php');

$configACU = json_decode(file_get_contents('/home/pi/common/config.json', true), true);

// 설정 보드 타입 its 또는 acu
$sql = " SELECT `mb_4` FROM `g5_member` WHERE mb_id = 'its'";
$row = sql_fetch($sql);
$ipBoard = $row['mb_4'];

?>

<link href="<?php echo G5_THEME_URL.'/js/bootstrap-toggle-master/css/bootstrap-toggle.min.css' ?>" rel="stylesheet">
<script src="<?php echo G5_THEME_URL.'/js/bootstrap-toggle-master/js/bootstrap-toggle.min.js' ?>"></script>
<style>
	.toggle.acuBtn {margin:4px 2px;}
	.groupSetACU {text-align: center;}
	.groupSetPOW {text-align: center;}
</style>
<?php if ($ipBoard == 'acu') { ?>
<div class="groupSetACU">
	<input id="io01" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R01" data-off="S01" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io01"])?"checked":"";?>>
	<input id="io02" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R02" data-off="S02" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io02"])?"checked":"";?>>
	<input id="io03" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R03" data-off="S03" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io03"])?"checked":"";?>>
	<input id="io04" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R04" data-off="S04" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io04"])?"checked":"";?>>
	<input id="io05" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R05" data-off="S05" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io05"])?"checked":"";?>>
	<input id="io06" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R06" data-off="S06" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io06"])?"checked":"";?>>
	<input id="io07" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R07" data-off="S07" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io07"])?"checked":"";?>>
	<input id="io08" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="R08" data-off="S08" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io08"])?"checked":"";?>>
	<input id="io09" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R09" data-off="S09" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io09"])?"checked":"";?>>
	<input id="io10" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R10" data-off="S10" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io10"])?"checked":"";?>>
	<input id="io11" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R11" data-off="S11" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io11"])?"checked":"";?>>
	<input id="io12" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R12" data-off="S12" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io12"])?"checked":"";?>>
	<input id="io13" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R13" data-off="S13" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io13"])?"checked":"";?>>
	<input id="io14" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R14" data-off="S14" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io14"])?"checked":"";?>>
	<input id="io15" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R15" data-off="S15" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io15"])?"checked":"";?>>
	<input id="io16" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R16" data-off="S16" <?php echo ($configACU["ioBoard"]["acu"]["setIO"]["io16"])?"checked":"";?>>
</div>
<div class="groupSetPOW">
	<input id="pw01" class="setPOW" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="danger" data-on="V12" data-off="0V" <?php echo ($configACU["ioBoard"]["acu"]["setPW"]["pw01"])?"checked":"";?>>
	<input id="pw02" class="setPOW" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="danger" data-on="V24" data-off="0V" <?php echo ($configACU["ioBoard"]["acu"]["setPW"]["pw02"])?"checked":"";?>>
	<button id="confirm" type="button" style="height: 22px;font-size: 8pt;line-height: 0;" class="btn btn-primary btn-sm">Confirm</button>
</div>
<?php } else { ?>
	<div class="groupSetACU">
	<input id="io01" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S01" data-off="S01" checked disabled>
	<input id="io02" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S02" data-off="S02" checked disabled>
	<input id="io03" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S03" data-off="S03" checked disabled>
	<input id="io04" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S04" data-off="S04" checked disabled>
	<input id="io05" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S05" data-off="S05" checked disabled>
	<input id="io06" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S06" data-off="S06" checked disabled>
	<input id="io07" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S07" data-off="S07" checked disabled>
	<input id="io08" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="success" data-on="S08" data-off="S08" checked disabled>
	<input id="io09" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R01" data-off="R01" checked disabled>
	<input id="io10" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R02" data-off="R02" checked disabled>
	<input id="io11" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R03" data-off="R03" checked disabled>
	<input id="io12" class="setACU" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="warning" data-on="R04" data-off="R04" checked disabled>
</div>
<div class="groupSetPOW">
	<input id="pw01" class="setPOW" data-style="acuBtn" type="checkbox" data-toggle="toggle" data-size="mini" data-onstyle="danger" data-on="V12" data-off="0V" checked disabled>
</div>
<?php } ?>
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
