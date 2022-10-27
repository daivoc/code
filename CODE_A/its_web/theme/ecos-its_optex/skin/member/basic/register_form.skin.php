<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// add_stylesheet('css 구문', 출력순서); 숫자가 작을 수록 먼저 출력됨
add_stylesheet('<link rel="stylesheet" href="'.$member_skin_url.'/style.css">', 0);

// 휴대폰관련 정보 강제 출력
$config['cf_use_hp'] = 1;

function select_option($cur_value, $option_val) {
	$select_select_option = '';
	while (list($key, $value) = each($option_val)) { 
		if($cur_value == $key)
			$select_select_option .='<option selected value="'.$key.'">'.$value.'</option>';
		else
			$select_select_option .='<option value="'.$key.'">'.$value.'</option>';
	} 
	$select_select_option .= '</select>';
	return $select_select_option;
}

?>

<!-- 회원정보 입력/수정 시작 { -->
<div class="mbskin" id="mb_confirm">

	<script src="<?php echo G5_JS_URL ?>/jquery.register_form.js"></script>
	<?php if($config['cf_cert_use'] && ($config['cf_cert_ipin'] || $config['cf_cert_hp'])) { ?>
	<script src="<?php echo G5_JS_URL ?>/certify.js"></script>
	<?php } ?>


	<form id="fregisterform" name="fregisterform" action="<?php echo $register_action_url ?>" onsubmit="return fregisterform_submit(this);" method="post" enctype="multipart/form-data" autocomplete="off">
	<input type="hidden" name="w" value="<?php echo $w ?>">
	<input type="hidden" name="url" value="<?php echo $urlencode ?>">
	<input type="hidden" name="agree" value="<?php echo $agree ?>">
	<input type="hidden" name="agree2" value="<?php echo $agree2 ?>">
	<input type="hidden" name="cert_type" value="<?php echo $member['mb_certify']; ?>">
	<input type="hidden" name="cert_no" value="">
	<?php if (isset($member['mb_sex'])) {  ?><input type="hidden" name="mb_sex" value="<?php echo $member['mb_sex'] ?>"><?php }  ?>
	<?php if (isset($member['mb_nick_date']) && $member['mb_nick_date'] > date("Y-m-d", G5_SERVER_TIME - ($config['cf_nick_modify'] * 86400))) { // 닉네임수정일이 지나지 않았다면  ?>
	<input type="hidden" name="mb_nick_default" value="<?php echo get_text($member['mb_nick']) ?>">
	<input type="hidden" name="mb_nick" value="<?php echo get_text($member['mb_nick']) ?>">
	<?php } ?>


	<?php if($member['mb_id'] == 'its' ) { ?>
		<div class="tbl_frm01 tbl_wrap">
			<table>
			<caption>Sound Info
			</caption>
			<tbody><?php include_once(G5_THEME_PATH.'/skin/board/w_include_audio/write_ims_common_sound.php'); ?></tbody>
			</table>
		</div>
		<?php /*
		<div class="tbl_frm01 tbl_wrap">
			<table>
			<caption>IP Relay
			<div style="font-size: 6pt; color: #ed143d78;"><?php // echo G5_THEME_PATH ?></div>
			</caption>
			<tbody>
			<?php include_once(G5_THEME_PATH.'/skin/board/w_include_light/write_ims_common_light.php'); ?>
			</tbody>
			</table>
		</div>
		*/ ?>
		<div class="tbl_frm01 tbl_wrap">
			<table>
			<caption>IO Board
			</caption>
			<tbody>
			<tr>
				<th scope="row"><label for="reg_mb_id">Type<strong class="sound_only"></strong></label></th>
				<td>
					<select name="mb_4" id="mb_4" class="form-control" placeholder="IO Board">
						<option value="">Select</option>
						<?php echo select_option($member['mb_4'], $g5_cu_ioBoard) ?>
					</select>
				</td>
			</tr>
			</tbody>
			</table>
		</div>

		<div class="tbl_frm01 tbl_wrap">
			<table>
			<caption>System Type
			</caption>
			<tbody>
			<tr>
				<th scope="row"><label for="reg_mb_id">Name<strong class="sound_only"></strong></label></th>
				<td>
					<select name="cf_10" id="cf_10" class="form-control" placeholder="IO Board">
						<option value="">Select</option>
						<?php echo select_option($config['cf_10'], $g5_cu_systemType) ?>
					</select>
				</td>
			</tr>
			</tbody>
			</table>
		</div>		

		<div class="tbl_frm01 tbl_wrap">
			<table>
			<caption>Company
			</caption>
			<tbody>
			<tr>
				<th scope="row"><label for="reg_mb_id">Name<strong class="sound_only"></strong></label></th>
				<td>
					<input type="text" id="cf_title" name="cf_title" value="<?php echo $config['cf_title'] ?>" class="form-control" placeholder="ITS Title">
				</td>
			</tr>
			</tbody>
			</table>
		</div>

		<div class="tbl_frm01 tbl_wrap">
			<table>
			<caption>Filter IP
			<div style="font-size: 6pt; color: #141bed78;">123.123.+ Can also be entered. (Divided by Enter)</div>
			</caption>
			<tbody>
			<tr>
				<th scope="row"><label for="reg_mb_id">IP Address<br><span style='font-size:10pt;'>Allow / Deny</span><strong class="sound_only"></strong></label></th>
				<td>
					<textarea class="form-control" name="cf_possible_ip" id="cf_possible_ip"><?php echo $config['cf_possible_ip'] ?></textarea>
				</td>
				<td>
					<textarea class="form-control" name="cf_intercept_ip" id="cf_intercept_ip"><?php echo $config['cf_intercept_ip'] ?></textarea>
				</td>
			</tr>
			</tbody>
			</table>
		</div>

	<?php } ?>
	<?php if($member['mb_id'] == 'manager' ) { ?>
	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>Language
		</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">Country<strong class="sound_only"></strong></label></th>
			<td>
				<select name="mb_7" id="mb_7" class="form-control" placeholder="Language">
					<option value="">Select</option>
					<?php echo select_option($member['mb_7'], $g5_cu_language) ?>
				</select>
		   </td>
		</tr>
		 </tbody>
		</table>
	</div>
	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>NTP Server
		</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">Server URL<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_8" name="mb_8" value="<?php echo ($member['mb_8'])?$member['mb_8']:''; ?>" class="form-control" placeholder="192.168.0.128||time.nist.gov">
		   </td>
		</tr>
		 </tbody>
		</table>
	</div>
	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>System Information
		</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">IP Address<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_4" name="mb_4" value="<?php echo ($member['mb_4'])?$member['mb_4']:$_SERVER['HTTP_HOST']; ?>" class="form-control required" required>
			</td>
		</tr>
	   <tr>
			<th scope="row"><label for="reg_mb_id">Netmask<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_5" name="mb_5" value="<?php echo ($member['mb_5'])?$member['mb_5']:''; ?>" class="form-control">
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="reg_mb_id">Gateway<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_6" name="mb_6" value="<?php echo ($member['mb_6'])?$member['mb_6']:''; ?>" class="form-control">
			</td>
		</tr>
		</tbody>
		</table>
	</div>
	<?php // mb_3:Watchdog Server IP ?>
	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>Watchdog Server IP
		<div style="font-size: 6pt; color: #ed143d78;"><?php // echo G5_THEME_PATH ?></div>
		</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">IP Address<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_3" name="mb_3" value="<?php echo ($member['mb_3'])?$member['mb_3']:''; ?>" class="form-control" placeholder="192.168.0.4">
			</td>
		</tr>
		</tbody>
		</table>
	</div>
	<?php // mb_9:가상 아이피 사용 ?>
	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>Virtual IP
		<div style="font-size: 6pt; color: #ed143d78;"><?php // echo G5_THEME_PATH ?></div>
		</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">IP Address<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_9" name="mb_9" value="<?php echo ($member['mb_9'])?$member['mb_9']:''; ?>" class="form-control">
			</td>
		</tr>
		</tbody>
		</table>
	</div>

	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>Contract Information
		<div style="font-size: 6pt; color: #ed143d78;"><?php echo G5_CU_ITS_SERIAL ?></div>
		</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">Customer<strong class="sound_only"></strong></label></th>
			<td>
			<input type="text" id="cu_name" readonly value="<?php echo $config['cf_title'] ?>" class="form-control readonly" placeholder="Customer Name">
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="reg_mb_id">License<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_1" name="mb_1" value="<?php echo ($member['mb_1'])?$member['mb_1']:''; ?>" class="form-control" placeholder="License(mb_1)">
			</td>
		</tr>
		<!-- <tr style="display:none;">
			<th scope="row"><label for="reg_mb_id">keyCode<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" id="mb_2" name="mb_2" value="<?php echo ($member['mb_2'])?$member['mb_2']:''; ?>" class="form-control">
			</td>
		</tr> -->
		<!-- <tr>
			<th scope="row"><label for="reg_mb_id">Request <strong class="sound_only"></strong></label></th>
			<td>
				<?php // include_once(G5_THEME_PATH.'/skin/board/w_include_license/system.php'); ?>
			</td>
		</tr> -->
		</tbody>
		</table>
	</div>
	<?php } ?>


	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>User Password</caption>
		<tbody>
		<tr>
			<th scope="row"><label for="reg_mb_id">ID<strong class="sound_only"></strong></label></th>
			<td>
				<input type="text" name="mb_id" value="<?php echo $member['mb_id'] ?>" id="reg_mb_id" <?php echo $required ?> <?php echo $readonly ?> class="form-control <?php echo $required ?> <?php echo $readonly ?>" minlength="3" maxlength="20">
				<span id="msg_mb_id"></span>
			</td>
		</tr>
		<tr>
			<th scope="row"><label for="reg_mb_password">Password<strong class="sound_only"></strong></label></th>
			<td><input type="password" name="mb_password" id="reg_mb_password" <?php echo $required ?> class="form-control <?php echo $required ?>" minlength="3" maxlength="20" autocomplete="off"></td>
		</tr>
		<tr>
			<th scope="row"><label for="reg_mb_password_re">Conform<strong class="sound_only"></strong></label></th>
			<td><input type="password" name="mb_password_re" id="reg_mb_password_re" <?php echo $required ?> class="form-control <?php echo $required ?>" minlength="3" maxlength="20"></td>
		</tr>
		</tbody>
		</table>
	</div>

	<div class="tbl_frm01 tbl_wrap" style="display:none;">
		<table>
		<caption>User Information</caption>
		<tbody>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_name">이름<strong class="sound_only">필수</strong></label></th>
			<td>
				<?php if ($config['cf_cert_use']) { ?>
				<span class="frm_info">아이핀 본인확인 후에는 이름이 자동 입력되고 휴대폰 본인확인 후에는 이름과 휴대폰번호가 자동 입력되어 수동으로 입력할수 없게 됩니다.</span>
				<?php } ?>
				<input type="text" id="reg_mb_name" name="mb_name" value="<?php echo get_text($member['mb_name']) ?>" <?php echo $required ?> <?php echo $readonly; ?> class="form-control <?php echo $required ?> <?php echo $readonly ?>" size="10">
				<?php
				if($config['cf_cert_use']) {
					if($config['cf_cert_ipin'])
						echo '<button type="button" id="win_ipin_cert" class="btn_frmline">아이핀 본인확인</button>'.PHP_EOL;
					if($config['cf_cert_hp'])
						echo '<button type="button" id="win_hp_cert" class="btn_frmline">휴대폰 본인확인</button>'.PHP_EOL;

					echo '<noscript>본인확인을 위해서는 자바스크립트 사용이 가능해야합니다.</noscript>'.PHP_EOL;
				}
				?>
				<?php
				if ($config['cf_cert_use'] && $member['mb_certify']) {
					if($member['mb_certify'] == 'ipin')
						$mb_cert = '아이핀';
					else
						$mb_cert = '휴대폰';
				?>
				<div id="msg_certify">
					<strong><?php echo $mb_cert; ?> 본인확인</strong><?php if ($member['mb_adult']) { ?> 및 <strong>성인인증</strong><?php } ?> 완료
				</div>
				<?php } ?>
			</td>
		</tr>
		<?php if ($req_nick) {  ?>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_nick">닉네임<strong class="sound_only">필수</strong></label></th>
			<td>
				<span class="frm_info">
					공백없이 한글,영문,숫자만 입력 가능 (한글2자, 영문4자 이상)<br>
					닉네임을 바꾸시면 앞으로 <?php echo (int)$config['cf_nick_modify'] ?>일 이내에는 변경 할 수 없습니다.
				</span>
				<input type="hidden" name="mb_nick_default" value="<?php echo isset($member['mb_nick'])?get_text($member['mb_nick']):''; ?>">
				<input type="text" name="mb_nick" value="<?php echo isset($member['mb_nick'])?get_text($member['mb_nick']):''; ?>" id="reg_mb_nick" required class="form-control required nospace" size="10" maxlength="20">
				<span id="msg_mb_nick"></span>
			</td>
		</tr>
		<?php }  ?>

		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_email">이메일<strong class="sound_only">필수</strong></label></th>
			<td>
				<?php if ($config['cf_use_email_certify']) {  ?>
				<span class="frm_info">
					<?php if ($w=='') { echo "E-mail 로 발송된 내용을 확인한 후 인증하셔야 회원가입이 완료됩니다."; }  ?>
					<?php if ($w=='u') { echo "E-mail 주소를 변경하시면 다시 인증하셔야 합니다."; }  ?>
				</span>
				<?php }  ?>
				<input type="hidden" name="old_email" value="<?php echo $member['mb_email'] ?>">
				<input type="text" name="mb_email" value="<?php echo isset($member['mb_email'])?$member['mb_email']:''; ?>" id="reg_mb_email" required class="form-control email required" size="70" maxlength="100">
			</td>
		</tr>

		<?php if ($config['cf_use_homepage']) {  ?>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_homepage">홈페이지<?php if ($config['cf_req_homepage']){ ?><strong class="sound_only">필수</strong><?php } ?></label></th>
			<td><input type="text" name="mb_homepage" value="<?php echo get_text($member['mb_homepage']) ?>" id="reg_mb_homepage" <?php echo $config['cf_req_homepage']?"required":""; ?> class="form-control <?php echo $config['cf_req_homepage']?"required":""; ?>" size="70" maxlength="255"></td>
		</tr>
		<?php }  ?>

		<?php if ($config['cf_use_tel']) {  ?>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_tel">전화번호<?php if ($config['cf_req_tel']) { ?><strong class="sound_only">필수</strong><?php } ?></label></th>
			<td><input type="text" name="mb_tel" value="<?php echo get_text($member['mb_tel']) ?>" id="reg_mb_tel" <?php echo $config['cf_req_tel']?"required":""; ?> class="form-control <?php echo $config['cf_req_tel']?"required":""; ?>" maxlength="20"></td>
		</tr>
		<?php }  ?>

		<?php if ($config['cf_use_hp'] || $config['cf_cert_hp']) {  ?>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_hp">휴대폰<?php if ($config['cf_req_hp']) { ?><strong class="sound_only">필수</strong><?php } ?></label></th>
			<td>
				<input type="text" name="mb_hp" value="<?php echo get_text($member['mb_hp']) ?>" id="reg_mb_hp" <?php echo ($config['cf_req_hp'])?"required":""; ?> class="form-control <?php echo ($config['cf_req_hp'])?"required":""; ?>" maxlength="20">
				<?php if ($config['cf_cert_use'] && $config['cf_cert_hp']) { ?>
				<input type="hidden" name="old_mb_hp" value="<?php echo get_text($member['mb_hp']) ?>">
				<?php } ?>
			</td>
		</tr>
		<?php }  ?>

		<?php if ($config['cf_use_addr']) { ?>
		<tr>
			<th scope="row">
				주소
				<?php if ($config['cf_req_addr']) { ?><strong class="sound_only">필수</strong><?php }  ?>
			</th>
			<td>
				<label for="reg_mb_zip" class="sound_only">우편번호<?php echo $config['cf_req_addr']?'<strong class="sound_only"> 필수</strong>':''; ?></label>
				<input type="text" name="mb_zip" value="<?php echo $member['mb_zip1'].$member['mb_zip2']; ?>" id="reg_mb_zip" <?php echo $config['cf_req_addr']?"required":""; ?> class="form-control <?php echo $config['cf_req_addr']?"required":""; ?>" size="5" maxlength="6">
				<button type="button" class="btn_frmline" onclick="win_zip('fregisterform', 'mb_zip', 'mb_addr1', 'mb_addr2', 'mb_addr3', 'mb_addr_jibeon');">주소 검색</button><br>
				<input type="text" name="mb_addr1" value="<?php echo get_text($member['mb_addr1']) ?>" id="reg_mb_addr1" <?php echo $config['cf_req_addr']?"required":""; ?> class="form-control frm_address <?php echo $config['cf_req_addr']?"required":""; ?>" size="50">
				<label for="reg_mb_addr1">기본주소<?php echo $config['cf_req_addr']?'<strong class="sound_only"> 필수</strong>':''; ?></label><br>
				<input type="text" name="mb_addr2" value="<?php echo get_text($member['mb_addr2']) ?>" id="reg_mb_addr2" class="form-control frm_address" size="50">
				<label for="reg_mb_addr2">상세주소</label>
				<br>
				<input type="text" name="mb_addr3" value="<?php echo get_text($member['mb_addr3']) ?>" id="reg_mb_addr3" class="form-control frm_address" size="50" readonly="readonly">
				<label for="reg_mb_addr3">참고항목</label>
				<input type="hidden" name="mb_addr_jibeon" value="<?php echo get_text($member['mb_addr_jibeon']); ?>">
			</td>
		</tr>
		<?php }  ?>
		</tbody>
		</table>
	</div>

	<div class="tbl_frm01 tbl_wrap">
		<table>
		<caption>Security Check</caption>
		<tbody>
		<?php if ($config['cf_use_signature']) {  ?>
		<tr>
			<th scope="row"><label for="reg_mb_signature">서명<?php if ($config['cf_req_signature']){ ?><strong class="sound_only">필수</strong><?php } ?></label></th>
			<td><textarea name="mb_signature" id="reg_mb_signature" <?php echo $config['cf_req_signature']?"required":""; ?> class="<?php echo $config['cf_req_signature']?"required":""; ?>"><?php echo $member['mb_signature'] ?></textarea></td>
		</tr>
		<?php }  ?>

		<?php if ($config['cf_use_profile']) {  ?>
		<tr>
			<th scope="row"><label for="reg_mb_profile">자기소개</label></th>
			<td><textarea name="mb_profile" id="reg_mb_profile" <?php echo $config['cf_req_profile']?"required":""; ?> class="<?php echo $config['cf_req_profile']?"required":""; ?>"><?php echo $member['mb_profile'] ?></textarea></td>
		</tr>
		<?php }  ?>

		<?php if ($config['cf_use_member_icon'] && $member['mb_level'] >= $config['cf_icon_level']) {  ?>
		<tr>
			<th scope="row"><label for="reg_mb_icon">회원아이콘</label></th>
			<td>
				<span class="frm_info">
					이미지 크기는 가로 <?php echo $config['cf_member_icon_width'] ?>픽셀, 세로 <?php echo $config['cf_member_icon_height'] ?>픽셀 이하로 해주세요.<br>
					gif만 가능하며 용량 <?php echo number_format($config['cf_member_icon_size']) ?>바이트 이하만 등록됩니다.
				</span>
				<input type="file" name="mb_icon" id="reg_mb_icon" class="form-control">
				<?php if ($w == 'u' && file_exists($mb_icon_path)) {  ?>
				<img src="<?php echo $mb_icon_url ?>" alt="회원아이콘">
				<input type="checkbox" name="del_mb_icon" value="1" id="del_mb_icon">
				<label for="del_mb_icon">삭제</label>
				<?php }  ?>
			</td>
		</tr>
		<?php }  ?>

		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_mailling">메일 수신</label></th>
			<td>
				<input type="checkbox" name="mb_mailling" value="1" id="reg_mb_mailling" <?php echo ($w=='' || $member['mb_mailling'])?'checked':''; ?>>이메일 알림을 받겠습니다.
												 
			</td>
		</tr>

		<?php if ($config['cf_use_hp']) {  ?>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_sms">문자 수신</label></th>
			<td>
				<input type="checkbox" name="mb_sms" value="1" id="reg_mb_sms" <?php echo ($w=='' || $member['mb_sms'])?'checked':''; ?>>
				문자메세지를 받겠습니다.
			</td>
		</tr>
		<?php }  ?>

		<?php if (isset($member['mb_open_date']) && $member['mb_open_date'] <= date("Y-m-d", G5_SERVER_TIME - ($config['cf_open_modify'] * 86400)) || empty($member['mb_open_date'])) { // 정보공개 수정일이 지났다면 수정가능  ?>
		<tr style="display:none;">
			<th scope="row"><label for="reg_mb_open">정보공개</label></th>
			<td>
				<span class="frm_info">
					정보공개를 바꾸시면 앞으로 <?php echo (int)$config['cf_open_modify'] ?>일 이내에는 변경이 안됩니다.
				</span>
				<input type="hidden" name="mb_open_default" value="<?php echo $member['mb_open'] ?>">
				<input type="checkbox" name="mb_open" value="1" <?php echo ($w=='' || $member['mb_open'])?'checked':''; ?> id="reg_mb_open">
				다른분들이 나의 정보를 볼 수 있도록 합니다.
			</td>
		</tr>
		<?php } else {  ?>
		<tr  style="display:none;">
			<th scope="row">정보공개</th>
			<td>
				<span class="frm_info">
					정보공개는 수정후 <?php echo (int)$config['cf_open_modify'] ?>일 이내, <?php echo date("Y년 m월 j일", isset($member['mb_open_date']) ? strtotime("{$member['mb_open_date']} 00:00:00")+$config['cf_open_modify']*86400:G5_SERVER_TIME+$config['cf_open_modify']*86400); ?> 까지는 변경이 안됩니다.<br>
					이렇게 하는 이유는 잦은 정보공개 수정으로 인하여 쪽지를 보낸 후 받지 않는 경우를 막기 위해서 입니다.
				</span>
				<input type="hidden" name="mb_open" value="<?php echo $member['mb_open'] ?>">
			</td>
		</tr>
		<?php }  ?>

		<?php if ($w == "" && $config['cf_use_recommend']) {  ?>
		<tr>
			<th scope="row"><label for="reg_mb_recommend">추천인아이디</label></th>
			<td><input type="text" name="mb_recommend" id="reg_mb_recommend" class="form-control"></td>
		</tr>
		<?php }  ?>

		<tr>
			<th scope="row">Prevent auto registration</th>
			<td><?php echo captcha_html(); ?></td>
		</tr>
		</tbody>
		</table>
	</div>

	<div class="form-group">
		<input type="submit" value="Submit" class="btn btn-primary btn-block" id="btn_submit" accesskey="s">
	</div>
		<div class="btn_confirm pad-top-half">
			<a href="<?php echo G5_URL ?>/">GO MAIN <span class="glyphicon glyphicon-chevron-right"></span></a>
		</div>


	</form>

	<script>
	$(function() {
		$("#reg_zip_find").css("display", "inline-block");

		<?php if($config['cf_cert_use'] && $config['cf_cert_ipin']) { ?>
		// 아이핀인증
		$("#win_ipin_cert").click(function() {
			if(!cert_confirm())
				return false;

			var url = "<?php echo G5_OKNAME_URL; ?>/ipin1.php";
			certify_win_open('kcb-ipin', url);
			return;
		});

		<?php } ?>
		<?php if($config['cf_cert_use'] && $config['cf_cert_hp']) { ?>
		// 휴대폰인증
		$("#win_hp_cert").click(function() {
			if(!cert_confirm())
				return false;

			<?php
			switch($config['cf_cert_hp']) {
				case 'kcb':
					$cert_url = G5_OKNAME_URL.'/hpcert1.php';
					$cert_type = 'kcb-hp';
					break;
				case 'kcp':
					$cert_url = G5_KCPCERT_URL.'/kcpcert_form.php';
					$cert_type = 'kcp-hp';
					break;
				case 'lg':
					$cert_url = G5_LGXPAY_URL.'/AuthOnlyReq.php';
					$cert_type = 'lg-hp';
					break;
				default:
					echo 'alert("기본환경설정에서 휴대폰 본인확인 설정을 해주십시오");';
					echo 'return false;';
					break;
			}
			?>

			certify_win_open("<?php echo $cert_type; ?>", "<?php echo $cert_url; ?>");
			return;
		});
		<?php } ?>
	});

	// submit 최종 폼체크
	function fregisterform_submit(f)
	{
		// 회원아이디 검사
		if (f.w.value == "") {
			var msg = reg_mb_id_check();
			if (msg) {
				alert(msg);
				f.mb_id.select();
				return false;
			}
		}

		if (f.w.value == "") {
			if (f.mb_password.value.length < 3) {
				alert("비밀번호를 3글자 이상 입력하십시오.");
				f.mb_password.focus();
				return false;
			}
		}

		if (f.mb_password.value != f.mb_password_re.value) {
			alert("비밀번호가 같지 않습니다.");
			f.mb_password_re.focus();
			return false;
		}

		if (f.mb_password.value.length > 0) {
			if (f.mb_password_re.value.length < 3) {
				alert("비밀번호를 3글자 이상 입력하십시오.");
				f.mb_password_re.focus();
				return false;
			}
		}

		// 이름 검사
		if (f.w.value=="") {
			if (f.mb_name.value.length < 1) {
				alert("이름을 입력하십시오.");
				f.mb_name.focus();
				return false;
			}

			/*
			var pattern = /([^가-힣\x20])/i;
			if (pattern.test(f.mb_name.value)) {
				alert("이름은 한글로 입력하십시오.");
				f.mb_name.select();
				return false;
			}
			*/
		}

		<?php if($w == '' && $config['cf_cert_use'] && $config['cf_cert_req']) { ?>
		// 본인확인 체크
		if(f.cert_no.value=="") {
			alert("회원가입을 위해서는 본인확인을 해주셔야 합니다.");
			return false;
		}
		<?php } ?>

		// 닉네임 검사
		if ((f.w.value == "") || (f.w.value == "u" && f.mb_nick.defaultValue != f.mb_nick.value)) {
			var msg = reg_mb_nick_check();
			if (msg) {
				alert(msg);
				f.reg_mb_nick.select();
				return false;
			}
		}

		// E-mail 검사
		if ((f.w.value == "") || (f.w.value == "u" && f.mb_email.defaultValue != f.mb_email.value)) {
			var msg = reg_mb_email_check();
			if (msg) {
				alert(msg);
				f.reg_mb_email.select();
				return false;
			}
		}

		<?php if (($config['cf_use_hp'] || $config['cf_cert_hp']) && $config['cf_req_hp']) {  ?>
		// 휴대폰번호 체크
		var msg = reg_mb_hp_check();
		if (msg) {
			alert(msg);
			f.reg_mb_hp.select();
			return false;
		}
		<?php } ?>

		if (typeof f.mb_icon != "undefined") {
			if (f.mb_icon.value) {
				if (!f.mb_icon.value.toLowerCase().match(/.(gif)$/i)) {
					alert("회원아이콘이 gif 파일이 아닙니다.");
					f.mb_icon.focus();
					return false;
				}
			}
		}

		if (typeof(f.mb_recommend) != "undefined" && f.mb_recommend.value) {
			if (f.mb_id.value == f.mb_recommend.value) {
				alert("본인을 추천할 수 없습니다.");
				f.mb_recommend.focus();
				return false;
			}

			var msg = reg_mb_recommend_check();
			if (msg) {
				alert(msg);
				f.mb_recommend.select();
				return false;
			}
		}

		<?php echo chk_captcha_js();  ?>

		document.getElementById("btn_submit").disabled = "disabled";

		return true;
	}
	</script>

</div>
		  
<!-- } 회원정보 입력/수정 끝 -->