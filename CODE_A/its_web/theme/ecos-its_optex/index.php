<?php
define('_INDEX_', true);
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

if (G5_IS_MOBILE) {
	include_once G5_THEME_MOBILE_PATH.'/index.php';
	return;
}
include_once G5_THEME_PATH.'/head.php';

?>
<?php if($is_guest) { ?>
<style>
html, body { text-align: center; margin:0; padding:0; background: #000000; color: #666666; line-height: 1.25em; }
#outer { position: absolute; top: 50%; left: 50%; width: 1px; height: 1px; overflow: visible;}
#canvasContainer { position: absolute; width: 1000px; height: 560px; top: -290px; left: -500px; }
canvas { border: 1px solid #333333; }
a { color: #00CBCB; text-decoration: none; font-weight: bold; }
a:hover { color: #FFFFFF; }
#output { font-family: Arial, Helvetica, sans-serif; font-size: 0.75em; margin-top: 4px; }
.container { z-index: 1; position: relative; }
</style>
<script type="text/javascript">
(function(){function C(){e.globalCompositeOperation="source-over";e.fillStyle="rgba(8,8,12,0.65)";e.fillRect(0,0,f,p);e.globalCompositeOperation="lighter";x=q-u;y=r-v;u=q;v=r;for(var d=0.86*f,l=0.125*f,m=0.5*f,t=Math.random,n=Math.abs,o=z;o--;){var h=A[o],i=h.x,j=h.y,a=h.a,b=h.b,c=i-q,k=j-r,g=Math.sqrt(c*c+k*k)||0.001,c=c/g,k=k/g;if(w&&g<m)var s=14*(1-g/m),a=a+(c*s+0.5-t()),b=b+(k*s+0.5-t());g<d&&(s=0.0014*(1-g/d)*f,a-=c*s,b-=k*s);g<l&&(c=2.6E-4*(1-g/l)*f,a+=x*c,b+=y*c);a*=B;b*=B;c=n(a);k=n(b);g=0.5*(c+k);0.1>c&&(a*=3*t());0.1>k&&(b*=3*t());c=0.45*g;c=Math.max(Math.min(c,3.5),0.4);i+=a;j+=b;i>f?(i=f,a*=-1):0>i&&(i=0,a*=-1);j>p?(j=p,b*=-1):0>j&&(j=0,b*=-1);h.a=a;h.b=b;h.x=i;h.y=j;e.fillStyle=h.color;e.beginPath();e.arc(i,j,c,0,D,!0);e.closePath();e.fill()}}function E(d){d=d?d:window.event;q=d.clientX-m.offsetLeft-n.offsetLeft;r=d.clientY-m.offsetTop-n.offsetTop}function F(){w=!0;return!1}function G(){return w=!1}function H(){this.color="rgb("+Math.floor(255*Math.random())+","+Math.floor(255*Math.random())+","+Math.floor(255*Math.random())+")";this.b=this.a=this.x=this.y=0;this.size=1}var D=2*Math.PI,f=1E3,p=560,z=600,B=0.96,A=[],o,e,n,m,q,r,x,y,u,v,w;window.onload=function(){o=document.getElementById("mainCanvas");if(o.getContext){m=document.getElementById("outer");n=document.getElementById("canvasContainer");e=o.getContext("2d");for(var d=z;d--;){var l=new H;l.x=0.5*f;l.y=0.5*p;l.a=34*Math.cos(d)*Math.random();l.b=34*Math.sin(d)*Math.random();A[d]=l}q=u=0.5*f;r=v=0.5*p;document.onmousedown=F;document.onmouseup=G;document.onmousemove=E;setInterval(C,33);}else document.getElementById("output").innerHTML="Sorry, needs a recent version of Chrome, Firefox, Opera, Safari, or Internet Explorer 9."}})();
</script>
<div id="outer">
	<div id="canvasContainer">
		<canvas id="mainCanvas" width="1000" height="560">
		</canvas>
	</div>
</div>

<?php } else if($member['mb_id'] == 'its') { ?>
<style> #header { filter: drop-shadow(2px 4px 6px black); }</style>
<!-- Header -->
<header id="header">
	<div class="container">
		<div class="row">
			<div class="col-lg-12">
				<div class="intro-text">
					<?php if($isITS_M) { ?>
						<style> #header .container { background: #896d2e; }</style>
						<span class="name">Intelligent Monitoring Server(IMS)</span>
					<?php } else { ?>
						<span class="name">Intelligent Terminal Server(ITS)</span>
					<?php } ?>
					<hr>
					<span>Technology by ECOS</span>
				</div>
			</div>
		</div>
</div>
</header>

<div id="menu_ITS" class="container"></div>
<?php } else if($member['mb_id'] == 'manager' && $isITS_M) {
	// 모니터링 데몬이 있는상태에서 매니저로 로그인 하면 바로 모니터링으로 화면 전환
	exec("ps aux | grep 'node .*its_M_map.js' | grep -v grep | awk '{ print $2 }' | head -1", $outM);
	// print "The PID is: " . $outM[0];
	if ($outM[0]) {
		$urlMonotoring = "http://".$_SERVER['HTTP_HOST'].":".G5_CU_IMS_PORT;
		header("Location: ".$urlMonotoring);
	} else {
		echo '<div style="position:absolute;top:30vh;left:40vw;text-align:center;"><img style="width:20vw;height:20vw;animation: spin 10s linear infinite;filter: invert(1);" src="'.G5_THEME_IMG_URL.'/profile.png" alt=""><div style="color:gray; text-align:center;">모니터링 서버간 일시적 접속 오류가 발생했습니다.<br>복구를 위해 상단 <span class="glyphicon glyphicon-refresh"></span>[재부팅]을 실행 하십시오.</div></div>';
	}

} else { 
	$urlMonotoring = "http://".$_SERVER['HTTP_HOST']."/theme/ecos-its_optex/utility/status/status_union.php";
	header("Location: ".$urlMonotoring);
} ?>

<?php
include_once(G5_THEME_PATH.'/tail.php');
?>