<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
$acuZoneID = array( // Alert
    0 => 'All Zone',
    1 => 'Zone 01',
    2 => 'Zone 02',
    3 => 'Zone 03',
    4 => 'Zone 04'
);

$itsOutID = array( // Alert
	18 => 'Relay 01',
	23 => 'Relay 02',
	24 => 'Relay 03',
	25 => 'Relay 04'
);

$acuOutID = array( // Alert
    1 => 'Relay 01',
    2 => 'Relay 02',
    3 => 'Relay 03',
    4 => 'Relay 04',
    5 => 'Relay 05',
    6 => 'Relay 06',
    7 => 'Relay 07',
    8 => 'Relay 08',
    9 => 'Relay 09',
   10 => 'Relay 10',
   11 => 'Relay 11',
   12 => 'Relay 12',
   13 => 'Relay 13',
   14 => 'Relay 14',
   15 => 'Relay 15',
   16 => 'Relay 16'
);

if($view['wr_10']) {
    list($acuIP, $acuPort, $acuID, $acuZone, $acuTime, $acuEncryption) = explode("||", $view['wr_10']);
    if($acuEncryption) $acuEncryption = "checked";
}
?>

<style>
.acuGroup { float:left; display: grid; margin-right:4px;}
#acuIP { width:25%; }
#acuPort, #acuTime { text-align: right;width: 10%; }
#acuID, #acuZone { text-align: right;width: 15%; }
#acuEncryption { margin-left: 6px; width:20px;height:20px; }
.acuEncry { width: 10%; }
</style>

<tr class="w_detail_tr">
	<th scope="row"><label for="wr_10">ITS_ACU</label></th>
	<td style="display: flex;">
        <input type='hidden' name='wr_10' value='<?php echo $view['wr_10'] ?>' id='wr_10'>
        <input type='text' class='form-control acuGroup' disabled id='acuIP' value='<?php if ($acuIP) echo $acuIP; else echo ""; ?>' placeholder='ACU IP'>
        <input type='text' class='form-control acuGroup' disabled id='acuPort' value='<?php if ($acuPort) echo $acuPort; else echo "0"; ?>' placeholder='ACU Port'>
        <input type='text' class='form-control acuGroup' disabled id='acuID' value='<?php if ($acuID) echo $itsOutID[$acuID]; else echo "0"; ?>' placeholder='ACU ID'>
        <input type='text' class='form-control acuGroup' disabled id='acuZone' value='<?php if ($acuZone) echo $acuZoneID[$acuZone]; else echo "0"; ?>' placeholder='ACU ID'>
        <input type='text' class='form-control acuGroup' disabled id='acuTime' value='<?php if ($acuTime) echo $acuTime; else echo "0"; ?>' placeholder='ACU Time'>
        <span class='acuGroup acuEncry'><input type="checkbox" class="form-control acuGroup" disabled id="acuEncryption" <?php echo $acuEncryption ?> value="1"><label>암호화</label></span>
	</td>
</tr>
