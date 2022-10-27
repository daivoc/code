<?php
include_once('./_common.php');
if ($is_guest) exit("Abnormal approach!");
include_once G5_PATH.'/head.php';

$DEVICE_alert = array( // Alert
	18 => 'Alert_01',
	23 => 'Alert_02',
	24 => 'Alert_03',
	25 => 'Alert_04',
	// 6 => 'Alert_05',
	// 7 => 'Alert_06',
	// 8 => 'Alert_07',
	// 9 => 'Alert_08'
);
$write['w_output1_group'] = "01010101";
?>
<script>
$(document).ready(function(){
	$('input:checkbox[name^="w_output"]').click(function () {
		var tmpVal = ""
		$('input:checkbox[name^="w_output1"]').each(function() {
			if ($(this).is(':checked')) {
				tmpVal = tmpVal + "1"
			} else {
				tmpVal = tmpVal + "0"
			}
		});
		$( "#w_output1_group" ).val(tmpVal);
		var tmpVal = ""
		$('input:checkbox[name^="w_output2"]').each(function() {
			if ($(this).is(':checked')) {
				tmpVal = tmpVal + "1"
			} else {
				tmpVal = tmpVal + "0"
			}
		});
		$( "#w_output2_group" ).val(tmpVal);
		var tmpVal = ""
		$('input:checkbox[name^="w_output3"]').each(function() {
			if ($(this).is(':checked')) {
				tmpVal = tmpVal + "1"
			} else {
				tmpVal = tmpVal + "0"
			}
		});
		$( "#w_output3_group" ).val(tmpVal);
		var tmpVal = ""
		$('input:checkbox[name^="w_output4"]').each(function() {
			if ($(this).is(':checked')) {
				tmpVal = tmpVal + "1"
			} else {
				tmpVal = tmpVal + "0"
			}
		});
		$( "#w_output4_group" ).val(tmpVal);
	});

	var setVal = "<?php echo $write['w_output1_group'] ?>";
	if (setVal) {
		var x = document.getElementsByName("w_output1[]"), iset;
		for (var iset = 0; iset < setVal.length; iset++) {
			if(setVal[iset] == "1"){
				x[iset].checked = true;
			} else {
				x[iset].checked = false;
			}
		}
	}
	var setVal = "<?php echo $write['w_output2_group'] ?>";
	if (setVal) {
		var x = document.getElementsByName("w_output2[]"), iset;
		for (var iset = 0; iset < setVal.length; iset++) {
			if(setVal[iset] == "1"){
				x[iset].checked = true;
			} else {
				x[iset].checked = false;
			}
		}		
	}
	var setVal = "<?php echo $write['w_output3_group'] ?>";
	if (setVal) {
		var x = document.getElementsByName("w_output3[]"), iset;
		for (var iset = 0; iset < setVal.length; iset++) {
			if(setVal[iset] == "1"){
				x[iset].checked = true;
			} else {
				x[iset].checked = false;
			}
		}		
	}
	var setVal = "<?php echo $write['w_output4_group'] ?>";
	if (setVal) {
		var x = document.getElementsByName("w_output4[]"), iset;
		for (var iset = 0; iset < setVal.length; iset++) {
			if(setVal[iset] == "1"){
				x[iset].checked = true;
			} else {
				x[iset].checked = false;
			}
		}		
	}	
	
});
</script>

<style>
.w_hide { display:none; }
.inputValue { "width:40px;text-align:right;padding:2px;" }
td { padding: 4px; }
input[type='checkbox'] { height: 30px;width: 30px; }
</style>

<section class="success" id="header" style="padding:0;">
    <div class="container" style="padding:100px 0 0 0;">
        <div class="intro-text">
            <span class="name wow fadeInDown shadow" data-wow-delay=".5s">GPWIO Config</span>
            <hr class="star-light wow zoomIn">
            <span class="skills wow fadeInUp" data-wow-delay="1s"></span>
        </div>
    </div>
</section>

<div class="container">
	<table style="color: gray;text-align: center;">
	<tr>
		<td></td>
		<td>Hold</td>
		<td>GPIO_1</td>
		<td>GPIO_2</td>
		<td>GPIO_3</td>
		<td>GPIO_4</td>
		<td>GPIO_5</td>
		<td>GPIO_6</td>
		<td>GPIO_7</td>
		<td>GPIO_8</td>
	</tr>
	<tr>
		<td>Relay 1</td>
		<td style="display: flex;">
			<input class="inputValue form-control" type="text" name="w_output1_relay" value="<?php echo array_search ('Alert_01', $DEVICE_alert); ?>" id="w_output1_relay">
			<input class="inputValue form-control" type="text" name="w_output1_value" value="<?php echo $write['w_output1_value'] ?>" id="w_output1_value">
			<input class="inputValue form-control" type="text" name="w_output1_group" value="<?php echo $write['w_output1_group'] ?>" id="w_output1_group">
		</td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
		<td><input type="checkbox" name="w_output1[]" value="1"></td>
	</tr>
	<tr>
		<td>Relay 2</td>
		<td style="display: flex;">
			<input class="inputValue form-control" type="text" name="w_output2_relay" value="<?php echo array_search ('Alert_02', $DEVICE_alert); ?>" id="w_output2_relay">
			<input class="inputValue form-control" type="text" name="w_output2_value" value="<?php echo $write['w_output2_value'] ?>" id="w_output2_value">
			<input class="inputValue form-control" type="text" name="w_output2_group" value="<?php echo $write['w_output2_group'] ?>" id="w_output2_group">
		</td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
		<td><input type="checkbox" name="w_output2[]" value="1"></td>
	</tr>
	<tr>
		<td>Relay 3</td>
		<td style="display: flex;">
			<input class="inputValue form-control" type="text" name="w_output3_relay" value="<?php echo array_search ('Alert_03', $DEVICE_alert); ?>" id="w_output3_relay">
			<input class="inputValue form-control" type="text" name="w_output3_value" value="<?php echo $write['w_output3_value'] ?>" id="w_output3_value">
			<input class="inputValue form-control" type="text" name="w_output3_group" value="<?php echo $write['w_output3_group'] ?>" id="w_output3_group">
		</td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
		<td><input type="checkbox" name="w_output3[]" value="1"></td>
	</tr>
	<tr>
		<td>Relay 4</td>
		<td style="display: flex;">
			<input class="inputValue form-control" type="text" name="w_output4_relay" value="<?php echo array_search ('Alert_04', $DEVICE_alert); ?>" id="w_output4_relay">
			<input class="inputValue form-control" type="text" name="w_output4_value" value="<?php echo $write['w_output4_value'] ?>" id="w_output4_value">
			<input class="inputValue form-control" type="text" name="w_output4_group" value="<?php echo $write['w_output4_group'] ?>" id="w_output4_group">
		</td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
		<td><input type="checkbox" name="w_output4[]" value="1"></td>
	</tr>
	</table>
</div>
<?php
include_once(G5_PATH.'/tail.php');
?>