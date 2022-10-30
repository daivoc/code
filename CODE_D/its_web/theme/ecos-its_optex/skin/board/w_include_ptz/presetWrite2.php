<?php
if (!defined("_GNUBOARD_")) exit; // 개별 페이지 접근 불가
?>
<tr class="w_detail_tr">
	<th scope="row"><label for="wr_4">Request 1/2</label></th>
	<td>
		<input type='text' name='wr_4' value='<?php echo $write['wr_4'] ?>' id='wr_4' class='form-control input50P' placeholder='Format:User||Pass||http://URL||0(1:Encription) for Request GET or POST Connect.'>
		<input type='text' name='wr_5' value='<?php echo $write['wr_5'] ?>' id='wr_5' class='form-control input50P' placeholder='Format:User||Pass||http://URL||0(1:Encription) for Request GET or POST Connect.'>
	</td>
</tr>
