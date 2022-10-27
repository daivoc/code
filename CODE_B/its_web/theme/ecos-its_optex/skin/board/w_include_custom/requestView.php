<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>

<?php
if($view['wr_4']) {
    list($wr4_Addr, $wr4_Para, $wr4_Encry, $wr4_Type) = explode("||", $view['wr_4']);
    if($wr4_Encry) $wr4_Encry = "checked";
    if($wr4_Type) $wr4_Type = "checked";
}
if($view['wr_5']) {
    list($wr5_Addr, $wr5_Para, $wr5_Encry, $wr5_Type) = explode("||", $view['wr_5']);
    if($wr5_Encry) $wr5_Encry = "checked";
    if($wr5_Type) $wr5_Type = "checked";
}
?>

<style>
hr { border: none;margin-top: 4px;margin-bottom: 4px;clear: both; }
.wr4_Group, .wr5_Group { float:left; display: grid; }
#wr4_Addr, #wr5_Addr { width: 40%; }
#wr4_Para, #wr5_Para { text-align: right;width: 40%; margin-right:4px; }
#wr4_Encry, #wr5_Encry, #wr4_Type, #wr5_Type { height:20px; width:20px;}
.wr_Encry, .wr_Type { width: 8%; margin-left: 4px; height:20px; }
.wr_Encry label, .wr_Type label { font-weight: normal; }
</style>

<tr class="w_detail_tr">
    <th scope="row"><label for="wr_4">Http Request</label></th>
    <td>
        <div style="width: 100%;">
        <input type='text' class='form-control wr4_Group' disabled id='wr4_Addr' value='<?php echo $wr4_Addr; ?>' >
        <input type='text' class='form-control wr4_Group' disabled id='wr4_Para' value='<?php echo $wr4_Para; ?>' >
        <span class='wr4_Group wr_Encry'><input type="checkbox" class="form-control wr4_Group" disabled id="wr4_Encry" <?php echo $wr4_Encry ?> value="1"><label>Post</label></span>
        <span class='wr4_Group wr_Type'><input type="checkbox" class="form-control wr4_Group" disabled id="wr4_Type" <?php echo $wr4_Type ?> value="1"><label>XML</label></span>
        <hr>
        <input type='text' class='form-control wr5_Group' disabled id='wr5_Addr' value='<?php echo $wr5_Addr; ?>' >
        <input type='text' class='form-control wr5_Group' disabled id='wr5_Para' value='<?php echo $wr5_Para; ?>' >
        <span class='wr5_Group wr_Encry'><input type="checkbox" class="form-control wr5_Group" disabled id="wr5_Encry" <?php echo $wr5_Encry ?> value="1"><label>Post</label></span>
        <span class='wr5_Group wr_Type'><input type="checkbox" class="form-control wr5_Group" disabled id="wr5_Type" <?php echo $wr5_Type ?> value="1"><label>XML</label></span>
        </div>
    </td>
</tr>
