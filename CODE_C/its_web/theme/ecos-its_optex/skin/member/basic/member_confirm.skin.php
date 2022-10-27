<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

// add_stylesheet('css 구문', 출력순서); 숫자가 작을 수록 먼저 출력됨
add_stylesheet('<link rel="stylesheet" href="'.$member_skin_url.'/style.css">', 0);

$g5['title'] = "Please enter your password again."
?>
<style>
/* BY_ECOS */
#mb_login { width: 100%; }
#mb_login #login_fs { padding:0; border:0; }
</style>
<div class="full-height">
    <div class="valign30">
    <div class="container">
        <div class="row">
            <div id="mb_login">
                <div class="col-md-6 col-md-offset-3">
					<h1><?php echo $g5['title'] ?></h1>

					<p>Check your password again for security.
						<?php /* if ($url == 'member_leave.php') { ?>
						비밀번호를 재 입력하시면 회원탈퇴가 완료됩니다.
						<?php }else{ ?>
						Check your password again for security.
						<?php } */ ?>
					</p>

					<form name="fmemberconfirm" action="<?php echo $url ?>" onsubmit="return fmemberconfirm_submit(this);" method="post">
						<fieldset id="login_fs">
							<input type="hidden" name="mb_id" value="<?php echo $member['mb_id'] ?>">
							<input type="hidden" name="w" value="u">
							ID : 
							<span id="mb_confirm_id"><h1><?php echo $member['mb_id'] ?></h1></span>

							<div class="form-group">
							<input type="password" name="mb_password" id="confirm_mb_password" required  class="form-control " size="15" maxLength="20" placeholder="Reconfirm password">
							</div>
							<div class="form-group">
								<input type="submit" value="Submit" class="btn btn-primary btn-block" id="btn_submit">
							</div>
						</fieldset>
					</form>

                </div>
                <div class="col-md-12">
                    <div class="btn_confirm pad-top-half">
                        <a href="<?php echo G5_URL ?>/">GO MAIN<span class="glyphicon glyphicon-chevron-right"></span></a>
                    </div>
                </div>

            </div>
        </div>
    </div>
    </div>
</div>

<script>
document.title = 'Confirm Password';
function fmemberconfirm_submit(f)
{
    document.getElementById("btn_submit").disabled = true;

    return true;
}
</script>
