<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

add_stylesheet('<link rel="stylesheet" href="'.$member_skin_url.'/style.css">', 0);
?>
<style>
/* BY_ECOS */
#mb_login { width: 100%; }
#mb_login #login_fs { padding:0; border:0; }
</style>
<!-- 로그인 시작 { -->
<div class="full-height">
    <div class="valign30">
    <div class="container">
        <div class="row">
            <div id="mb_login">
                <div class="col-md-6 col-md-offset-3">
                    <form name="flogin" action="<?php echo $login_action_url ?>" onsubmit="return flogin_submit(this);" method="post">
                        <input type="hidden" name="url" value="<?php echo $login_url ?>">
                        <fieldset id="login_fs">
                            <legend class="text-center"><i class="fa fa-lock"></i> Login</legend>
                            <div class="form-group">
                            <input type="text" name="mb_id" id="login_id" required class="form-control " size="20" maxLength="20" placeholder="ID">
                            </div>
                            <div class="form-group">
                            <input type="password" name="mb_password" id="login_pw" required class="form-control" size="20" maxLength="20" placeholder="PASSWORD">
                            </div>
                            <div class="form-group">
                                <input type="submit" value="Login" class="btn btn-primary btn-block">
                            </div>
                        </fieldset>
                    </form>
                </div>
                <div class="col-md-12">
                    <div class="btn_confirm pad-top-half">
                        <a href="<?php echo G5_URL ?>/">GO MAIN <span class="glyphicon glyphicon-chevron-right"></span></a>
                    </div>
                </div>

            </div>
        </div>
    </div>
    </div>
</div>

<script>
document.title = 'Login';
function flogin_submit(f)
{
    return true;
}
</script>
<!-- } 로그인 끝 -->