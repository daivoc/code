<?php
include_once('./_common.php');
// alert(G5_URL.'/'.G5_DATA_DIR.'/image/ims/ims_map.svg');
// Ex: http://192.168.0.47/theme/ecos-its_optex/utility/svgIMS/svgIMS.php
// /var/www/html/its_web/data/image/ims

if ($is_guest) exit("Abnormal approach!");
if (file_exists(G5_CU_MAP_PATH.'/ims_map.svg')) {
	$imsSvg = G5_CU_MAP_URL.'/ims_map.svg';
} else {
	exit(G5_CU_MAP_URL.'/ims_map.svg');
}

$imsConfig = json_decode(file_get_contents("/home/pi/MONITOR/config.json"), TRUE);
$group1st = $imsConfig['groupLayer']['1st']; // "◇"
$group2st = $imsConfig['groupLayer']['2st']; // "◈"
$group3st = $imsConfig['groupLayer']['3st']; // "◆"
?>

<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes">
<script type="text/javascript" src="jquery/jquery-3.1.1.min.js"></script>
<script type="text/javascript" src="jquery/ui/jquery-ui.js"></script>
<link rel="stylesheet" type="text/css" href="jquery/ui/jquery-ui.css">
<script type="text/javascript" src="svg-pan-zoom/svg-pan-zoom.js"></script>

<script>
	var curMapID;
	var curBlinkOJ;
	var curColorFill;
	var curAttrib;
	var curElementID;
	var newElementID;
	var selectedGrpID;

	$(document).ready(function() {

		var panZoom = svgPanZoom('svg');
		// 시작시 스크린 잠금
		panZoom.setMinZoom(0.01);
		panZoom.setMaxZoom(100);
		panZoom.enablePan();
		panZoom.enableZoom();
		panZoom.enableDblClickZoom();
		panZoom.enableMouseWheelZoom();
		panZoom.fit();
		panZoom.center();


		// var svgElement = document.querySelector("svg");
		// var sE = svgElement.getBoundingClientRect(); 
		// // console.log("svgBox", sE.x, sE.y, sE.width, sE.height)

		// var vB=panZoom.getSizes().viewBox;
		// // console.log("viewBox", vB.x, vB.y, vB.width, vB.height)

		// var grpElement = document.querySelector("#"+selectedGrpID);
		// var gE = grpElement.getBoundingClientRect(); 
		// // console.log("grpElement", gE.x, gE.y, gE.width, gE.height)

		// var x=sE.width/2-gE.x-gE.width/2;
		// var y=sE.height/2-gE.y-gE.height/2;
		// panZoom.panBy({x:x,y:y});

		// var cP = panZoom.getPan(); 
		// // console.log("currentPan", cP.x, cP.y)

		// var rZ=panZoom.getSizes().realZoom;
		// // console.log("realZoom", rZ)

		// if(sE.width/sE.height < gE.width/gE.height){
		// 	var zoomSvg=sE.width/gE.width;
		// } else {
		// 	var zoomSvg=sE.height/gE.height;
		// }

		// if(vB.width/vB.height < gE.width/gE.height){
		// 	var zoomView=vB.width/gE.width;
		// } else {
		// 	var zoomView=vB.height/gE.height;
		// }

		// panZoom.zoom(zoomView*rZ);

		// console.log("groupZoom:"+zoomView,"realZoom:"+rZ,"groupZoom x realZoom:"+zoomView*rZ);
		// console.log("----------------------");

		// // https://stackoverflow.com/questions/10298658/mouse-position-inside-autoscaled-svg
		// // Find your root SVG element
		// var svgEdit = document.querySelector('svg');
		// // Create an SVGPoint for future math
		// var ptEdit = svgEdit.createSVGPoint();
		// // Get point in global SVG space
		// function cursorPoint(evt){
		// ptEdit.x = evt.clientX; ptEdit.y = evt.clientY;
		// console.log(ptEdit);
		// return ptEdit.matrixTransform(svgEdit.getScreenCTM().inverse());
		// }
		// svgEdit.addEventListener('mousemove',function(evt){
		// var loc = cursorPoint(evt);
		// console.log(loc.x, loc.y);
		// },false);

		$("#svgFit").on('click', function() { 
			panZoom.resize(); // update SVG cached size and controls positions
			panZoom.fit();
			panZoom.center();
			$(".objectFit").each(function() { // 전체보기(FIT) 요청시 모두 보이기 표시 한다.
				// $("#"+$(this).val()).css("display", "inline"); // "inline"
				$("#"+$(this).attr('data-target')).css("display", "inline"); // "inline"
			});
		});	
		// $("#svgFit").on('click', function() { 
		// 	panZoom.resize(); // update SVG cached size and controls positions
		// 	panZoom.fit();
		// 	panZoom.center();
		// 	$(".objectFit").each(function() {
		// 		$("#"+$(this).attr('data-target')).css("display", "inline"); // "inline"
		// 	});
		// });	
		
		// // 그룹수 확인후 선택기능 실행버튼 추가 ['groupLayer']['1st'] "◇"
		// $("[id^='<?php echo $group1st ?>']").each(function() {
		// 	console.log(this.id);
		// });	
		
		// var cntGroup = $("[id^='<?php echo $group1st ?>']").length; // "◇"
		// // 그룹의 갯수가 한개 이상일 경우 버튼보기 표시
		// if (cntGroup > 1) {
		// 	$("#svgGroup").html('<button class="showGroup" id="showGroup">Show Group</button>');
		// }
		$("#svgGroup").html('<button class="showGroup" id="showGroup">Show Group</button>');

		$("#showGroup").on('click', function() {
			var svgGroup = '';
			// 그룹수 확인후 선택기능 실행버튼 추가 ['groupLayer']['1st'] "◇"
			$("[id^='<?php echo $group1st ?>']").each(function() { // "◇"
				if($(this).attr('data-group_hide')) {
					svgGroup += '<input type="button" class="objectFit" style="background-color:maroon" data-target="'+this.id+'" value="'+this.id.substring(1)+'">';
					// svgGroup += '<input type="button" class="objectFit" style="background-color:maroon" data-target="'+this.id+'" value="'+this.id+'">';
				} else {
					svgGroup += '<input type="button" class="objectFit" style="background-color:navy" data-target="'+this.id+'" value="'+this.id.substring(1)+'">';
					// svgGroup += '<input type="button" class="objectFit" style="background-color:navy" data-target="'+this.id+'" value="'+this.id+'">';
				}
			});
			$("#svgGroupList").html(svgGroup);
			// console.log(svgGroup);

			// 정의 되지 않은 그룹 리스트 출력
			var groupList = '';
			$("svg > g > g").each(function() {
				groupList += '<input type="button" class="objectFit" style="background-color:maroon" data-target="'+this.id+'" value="'+this.id+'">';
				// console.log(this.id);
			});
			$("#groupList").html(groupList);

			$(".objectFit").on("click", function() {
				// https://developer.mozilla.org/en-US/docs/Web/API/SVGGraphicsElement/getBBox
				// id="svgGroup" 그룹 내에 class="objectFit" 요소의 value="테그 <g>의 ID 명"
				// 예 : <input type="button" class="objectFit" value="T2-4F">
				// 현재의 화면에 선택된 요소를 Fitting(Pan + Zoom)한다.

				curElementID = $(this).attr('data-target');
				selectedGrpID = $(this).attr('data-target');

				curMapID = $("#"+curElementID).attr('data-group_map');
				curBlinkOJ = $("#"+curElementID).attr('class');
				curColorFill = $("#"+curElementID).css('fill');
				$("#groupMapID").val(curMapID);
				$("#blinkOJ").val(curBlinkOJ);
				$("#colorFill").css('background-color', curColorFill);

				// var curViewID = $("#"+selectedGrpID).attr('data-group_hide');

				$("#newID, #curID").val(selectedGrpID); // 입력창에 넣기
				
				// 선택된 그룹(".objectFit")을 제외한 일반그룹(효과)은 감추기에서 제외시킴
				$(".objectFit").each(function() {
					if (selectedGrpID == $(this).attr('data-target')) {
						$("#"+$(this).attr('data-target')).css("display", "inline"); // "inline"
					} else {
						$("#"+$(this).attr('data-target')).css("display", "none"); // "inline"
					}
				});

				fitToGroup(selectedGrpID,2.4);
			});
		});

		// $("#content").mousedown(function (e) {
		// $("#svg_id").mousedown(function (e) {

		$(".svg-pan-zoom_viewport").mousedown(function (e) {
			$("#coord").val("x:"+e.offsetX+", y:"+e.offsetY);
			// console.log(e);
		});

		////////////////////////////////////////////
		// 마우스오버 기능
		$( "circle, path, polygon, rect, ellipse, image, text" ).mouseover(function(){
			if($(this).attr('data-group_map') === undefined) { // data-group_map은 기존의 SVG 요소를 바탕이미지로 간주한다.
				$(this).css('cursor', 'pointer');
				$(this).css("stroke", "white");
			}
		});

		$( "circle, path, polygon, rect, ellipse, image, text" ).mouseout(function(){
			if($(this).attr('data-group_map') === undefined) { // data-group_map은 기존의 SVG 요소를 바탕이미지로 간주한다.
				// $(this).css("stroke", "unset");
			}
		});

		// 참고 : https://openclassrooms.com/courses/ultra-fast-applications-using-node-js/socket-io-let-s-go-to-real-time
		$("circle, path, polygon, rect, ellipse, image, text").on('click', function () { // 마우스 및 모바일(touchstart) 텝 적용
			curElementID = $(this).attr('id');
			curMapID = $(this).attr('data-group_map');
			curBlinkOJ = $(this).attr('class');
			curColorFill = $(this).css('fill');

			curAttrib = $(this).attr('d');

			$("#groupMapID").val(curMapID);
			$("#blinkOJ").val(curBlinkOJ);
			$("#colorFill").css('background-color', curColorFill);

			$("#newID, #curID").val(curElementID);
		});

		$('#infoUpload').on('click', function () {
			var r = confirm("Do you want upload?");
			if (r == true) {
				$.post("./upload.php", {
					svgCode: $('#content').html(),
					dataType: 'text',
				},
				function(data,status){
					$('#log').append("<div style='color:silver' >"+data+"</div>");
					// $("#log").prepend(status);
				});
			}
		});

		// 선택된 요소의 아이디명을 등록또는 수정 한다.
		$('#setID').on('click', function () {
			if (curElementID) {
				newElementID = $("#newID").val().replace(/\s/g, ""); // 화이트 스페이스 삭제
				$("[data-target='"+curElementID+"']").val(newElementID);
				$("[data-target='"+curElementID+"']").attr("data-target",newElementID);
				$("#"+curElementID).attr("id",newElementID);
				var el = $('<div class="newElements" style="color:silver">ID:'+curElementID+' -> '+newElementID+'</div>');
				$("#log").append(el);
				$("#newID, #curID").val('');
				$("#showGroup").click();
				curElementID = '';
			} else {
				$("#log").append('<div style="color:crimson">Select target first.</div>');
			}
		});

		// 선택된 요소의 아이디명에 ◇($group1st)를 포함또는 제거 한다.
		$('#setMark').on('click', function () {
			if (curElementID) {
				if($("#newID").val().charAt(0) == "<?php echo $group1st ?>") { // 아이디에 화면 전환을 위한 구분자 추가 또는 제거함
					newElementID = $("#newID").val().substring(1);
				} else {
					newElementID = "<?php echo $group1st ?>"+$("#newID").val();
				}
				$("[data-target='"+curElementID+"']").val(newElementID);
				$("[data-target='"+curElementID+"']").attr("data-target",newElementID);
				$("#"+curElementID).attr("id",newElementID);
				var el = $('<div class="newElements" style="color:silver">ID:'+curElementID+' -> '+newElementID+'</div>');
				$("#log").append(el);
				$("#newID, #curID").val('');
				$("#showGroup").click();
				curElementID = '';
			} else {
				$("#log").append('<div style="color:crimson">Select target first.</div>');
			}
		});

		// 선택한 요소관련 보드테이블이 있는지 확인후 팝업
		$('.regist').on('click', function (id) { //Zone, Box, Camera 등록
			if (curElementID) {
				// copyClipboard();  // 선택된 아이디 복사
				copyToClipboard("#newID");
				$.post("./registration.php", { // 선택한 요소관련 보드테이블이 있는지 확인후 팝업
					boardTableID: this.id,
					curElementID: curElementID,
				},
				function(data,status){
					window.open(data+"#header", "IMS Registration", "width=500,height=500,scrollbars=yes");
					$('#log').append("<div style='color:cyan'>Registration "+status+" :"+curElementID+"</div>");
					$("#newID, #curID").val('');
					curElementID = '';
				});
			} else {
				$("#log").append('<div style="color:crimson">Select target first.</div>');
			}
		});

		// 선택기능한 요소를 맵으로 선언 또는 반대로 합니다.
		$("#groupMapID").change(function() {
			if(curElementID) {
				if($("#groupMapID").val()) {
					$("#"+curElementID).attr("data-group_map",1);
					var curMap = "Set to Map";
				} else {
					$("#"+curElementID).removeAttr("data-group_map");
					var curMap = "Set to Element";
				}
				$("#log").append('<div style="color:silver">Object Mapping :'+curElementID+' -> '+curMap+'</div>');
				$("#newID, #curID").val('');
				curElementID = '';
				curMapID = '';
			} else {
				$("#log").append('<div style="color:crimson">Select target first.</div>');
			}
		});

		$("#blinkOJ").change(function() {
			if(curElementID) {
				if($("#blinkOJ").val()) {
					$("#"+curElementID).removeClass().addClass($("#blinkOJ").val());
				} else {
					$("#"+curElementID).removeClass();
				}
				$("#log").append('<div style="color:silver">Object Blink :'+curElementID+' -> '+$("#blinkOJ").val()+'</div>');
				$("#newID, #curID").val('');
				curElementID = '';
				curBlinkOJ = '';
			} else {
				$("#log").append('<div style="color:crimson">Select target first.</div>');
			}
		});

		$("#colorFill").change(function() {
			if(curElementID) {
				// console.log("fill", $("#colorFill").val());
				$("#"+curElementID).css("fill", $("#colorFill").val());
				$("#log").append('<div style="color:silver">Object Fill :'+curElementID+' -> '+$("#colorFill").val()+'</div>');
				$("#newID, #curID").val('');
				curElementID = '';
				curColorFill = '';
			} else {
				$("#log").append('<div style="color:crimson">Select target first.</div>');
			}
		});

		// 실행하면 모든 요소의 ID가 새롭게 정열합니다.
		$("#resetID").click(function() {
			var r = confirm("실행하면 모든 요소의 ID가 새롭게 정열합니다.");
			if (r == true) {
				$("circle").each(function(index) {
					// console.log(index + ": " + $(this).attr("id"));
					$(this).attr("id","circ_"+(10000+index));
				});
				if($("circle").length) { $("#log").append('<div style="color:green">Number of circle :'+$("circle").length+'</div>') }

				$("path").each(function(index) {
					// console.log(index + ": " + $(this).attr("id"));
					$(this).attr("id","path_"+(10000+index));
				});
				if($("path").length) { $("#log").append('<div style="color:green">Number of path :'+$("path").length+'</div>') }

				$("polygon").each(function(index) {
					// console.log(index + ": " + $(this).attr("id"));
					$(this).attr("id","poly_"+(10000+index));
				});
				if($("polygon").length) { $("#log").append('<div style="color:green">Number of polygon :'+$("polygon").length+'</div>') }

				$("rect").each(function(index) {
					// console.log(index + ": " + $(this).attr("id"));
					$(this).attr("id","rect_"+(10000+index));
				});
				if($("rect").length) { $("#log").append('<div style="color:green">Number of rect :'+$("rect").length+'</div>') }

				$("ellipse").each(function(index) {
					// console.log(index + ": " + $(this).attr("id"));
					$(this).attr("id","elli_"+(10000+index));
				});
				if($("ellipse").length) { $("#log").append('<div style="color:green">Number of ellipse :'+$("ellipse").length+'</div>') }

				$("image").each(function(index) {
						// console.log(index + ": " + $(this).attr("id"));
						$(this).attr("id","img_"+(10000+index));
					});
				if($("image").length) { $("#log").append('<div style="color:green">Number of image :'+$("image").length+'</div>') }

				$("text").each(function(index) {
						// console.log(index + ": " + $(this).attr("id"));
						$(this).attr("id","text_"+(10000+index));
					});
				if($("text").length) { $("#log").append('<div style="color:green">Number of text :'+$("text").length+'</div>') }
			}

		});

		// 실행하면 모든 요소의 ID가 맵으로 선언 합니다.
		$("#mapAll").click(function() {
			var r = confirm("실행하면 모든 요소의 ID가 맵으로 선언 합니다.");
			if (r == true) {
				$("circle, path, polygon, rect, ellipse, image, text").each(function(index) {
					$(this).attr("data-group_map",1);
				});
				$("image, text").each(function(index) {
					$(this).removeAttr("style");
					// $(this).removeAttr("class");
				});
				$("#log").append('<div style="color:yellow">Number of Total Mapped :'+$("circle, path, polygon, rect, ellipse, image, text").length+'</div>');
			}
		});

		////// SVG ID 자동 수정 ////
		// $("svg").attr("id","svg_id");
		// $('#log').append("<div style='color:silver' >Auto setted that SVG_ID.</div>");

		// 요소를 화면에 꽉 채운다.
		function fitToGroup(groupID, scale=1) { // (요소의 아이디, 스케일 - 1:기본, 1이하:축소, 1이상:확대)
			var svgElement = document.querySelector("svg");
			var sE = svgElement.getBoundingClientRect(); 
			// console.log("svgBox", sE.x, sE.y, sE.width, sE.height)

			var vB=panZoom.getSizes().viewBox;
			// console.log("viewBox", vB.x, vB.y, vB.width, vB.height)

			var grpElement = document.querySelector("#"+groupID);
			var gE = grpElement.getBoundingClientRect(); 
			// console.log("grpElement", gE.x, gE.y, gE.width, gE.height)

			var x=sE.width/2-gE.x-gE.width/2;
			var y=sE.height/2-gE.y-gE.height/2;
			panZoom.panBy({x:x,y:y});

			var cP = panZoom.getPan(); 
			// console.log("currentPan", cP.x, cP.y)

			var rZ=panZoom.getSizes().realZoom;
			// console.log("realZoom", rZ)

			if(sE.width/sE.height < gE.width/gE.height){
				var zoomSvg=sE.width/gE.width;
			} else {
				var zoomSvg=sE.height/gE.height;
			}

			if(vB.width/vB.height < gE.width/gE.height){
				var zoomView=vB.width/gE.width;
			} else {
				var zoomView=vB.height/gE.height;
			}
			panZoom.zoom(zoomView*rZ*scale);
		}
	});
	
	function copyToClipboard(element) {
		var $temp = $("<input>");
		$("body").append($temp);
		$temp.val($(element).val()).select();
		document.execCommand("copy");
		$temp.remove();
	}
	function getFormattedTime() {
		var today = new Date();
		var y = today.getFullYear();
		// JavaScript months are 0-based.
		var m = today.getMonth() + 1;
		var d = today.getDate();
		var h = today.getHours();
		var mi = today.getMinutes();
		var s = today.getSeconds();
		return y + "-" + m + "-" + d + " " + h + "_" + mi + "_" + s;
	}
</script>

<style>
	body { padding:0;margin:0; background:black;}
	svg { display: inline; width: 100%; min-width: inherit; max-width: inherit; height: 100%; min-height: inherit; max-height: inherit; }
	input, button, select { font-size: 9pt; margin: unset;color: silver; padding:2px; font-family: unset; }
	circle:hover, path:hover, polygon:hover, rect:hover, ellipse:hover{stroke:white;stroke-width:2;}

	.hide { display:none; }
	.center { text-align: center; }
	.relative { position: relative; }
	.charts { margin: 10px; }
	.readonly { color: white; background: gray; }
	.inputGrp { position: absolute; display: unset; background: linear-gradient(145deg, black, transparent); color: silver; }
	.resetID {background: linear-gradient(145deg, #860909, transparent);border: 1px solid #a26c74;}
	.setID {background: linear-gradient(145deg, #4018e0, transparent);border: 1px solid #6c72e4;}
	.infoGrp {background: linear-gradient(145deg, #586704, transparent); border: 1px solid #478c8e;}
	.updateGrp {background: linear-gradient(145deg, silver, transparent); border: 1px solid #0a0a0a;}
	.showGroup {background: linear-gradient(145deg, #841060, transparent); border: 1px solid #9c559b;margin: 2px;}
	.objectFit {border: 1px solid #008c8e;margin: 2px;}
	.regist {margin-left: 0px; margin-right: 4px;border-radius: 2px;background-color: black;color: silver;border: 1px solid silver;}

	#curID, #newID { background: gray; color: white; }

	#log { background-color: #000000AA; font-size: 8pt; width: auto; height: auto; float: right; position: absolute; top: 36px; overflow: hidden; overflow-y: -webkit-paged-x; margin: 10px; padding: 6px; }
	#logDetail_form { display:none; position: relative; }
	#logMonitor_form { float: right; position: relative; }
	#list { background-color: #00000080; font-size: 8pt; height: 200px; float: left; line-height: 12px; position: relative; overflow: hidden; overflow-y: auto; margin: 10px; padding: 6px; }
	#content { position: absolute; top: 0; right: 0; bottom: 0; left: 0; overflow: hidden; border-top: 1px solid silver;}
	#groupList {background-color: #00000000;font-size: 10pt;width: 100%;height:26px;position: absolute;bottom:0;overflow: auto; color: silver;}

	.blink01 { animation: blinker01 3s linear infinite; }
	@keyframes blinker01 { 50% { opacity: 0.2 } }
	.blink02 { animation: blinker02 2s linear infinite; }
	@keyframes blinker02 { 50% { opacity: 0.2 } }
	.blink03 { animation: blinker03 1s linear infinite; }
	@keyframes blinker03 { 50% { opacity: 0.2 } }
	.blink04 { animation: blinker04 0.5s linear infinite; }
	@keyframes blinker04 { 50% { opacity: 0.2 } }
	.blink05 { animation: blinker05 0.3s linear infinite; }
	@keyframes blinker05 { 50% { opacity: 0.2 } }
	.blink06 { animation: blinker06 0.1s linear infinite; }
	@keyframes blinker06 { 50% { opacity: 0.2 } }


/* 사용자 데코레이션 */
/* 기차 움직임 에니메이션 */
/* https://artificial.design/archives/2018/05/23/svg-animation.html */

	#불빛, #불빛-1, #불빛-6, #불빛-7, #불빛-9 {
		animation-name: trainMovesBack;
		animation-duration: 6s;
		animation-iteration-count: infinite;
		transform-origin: 50% 50%;
		animation-direction: normal; // alternate-reverse;
	}
	@keyframes trainMovesBack {
		0%   { transform: translate(0, -160px); }
		100% { transform: translate(0, 120px); }
	}

	#g12989, #g32, #g32-2, #g31, #g13104-1 {
		animation-name: trainMovesFront;
		animation-duration: 4s;
		animation-iteration-count: infinite;
		transform-origin: 50% 50%;
		animation-direction: normal; // alternate-reverse;
	}
	@keyframes trainMovesFront {
		0%   { transform: translate(0, 180px); }
		100% { transform: translate(0, -100px); }
	}

	@keyframes trainBlur {
		0%,
		90% {
		-webkit-filter: blur(0px);
		-moz-filter: blur(0px);
		-o-filter: blur(0px);
		-ms-filter: blur(0px);
		}
		50% {
			-webkit-filter: blur(50px);
			-moz-filter: blur(50px);
			-o-filter: blur(50px);
			-ms-filter: blur(50px);
		}
	}

</style>
</head> 

<body>
<div id="content"><?php echo file_get_contents($imsSvg) ?></div>

<?php if($selectedID) { ?>
	<script>
	var selectedID = document.getElementById('<?php echo $selectedID?>');
	selectedID.style.fill = "red";
	selectedID.style.opacity = 1;
</script>
<?php } else { ?>
	<script> // document.getElementById('content').style.top = '40px';</script>
	<div id="log"></div>
	<div class="inputGrp">
		<input type="hidden" id="coord" value="" placeholder="coord" readonly />
		<input type="hidden" id="curID" value="" placeholder="curID" readonly/>
		<input type="text" id="newID" value="" placeholder="New ID"/>
		<button class="regist" id="zone">Z</button>
		<button class="regist" id="box">B</button>
		<button class="regist" id="camera">C</button>
		<button class="setID" id="setID" title="선택된 요소의 아이디명을 수정 한다.">Reset ID</button>
		<button class="updateGrp" id="setMark" name="setMark" title="선택된 요소의 아이디명에 ◇(Prefix)를 포함 또는 제거 한다.">Mark Group</button>
		<span style="margin-left: 10px;"></span>
		<button class="resetID" id="resetID" title="모든 요소의 ID를 새롭게 정열한다.">Reset All ID</button>
		<button class="infoGrp" id="mapAll" name="mapAll" title="모든 요소를 맵으로 선언 한다.">Reset All Map</button>
		<span style="margin-left: 10px;"></span>
		<select class="infoGrp" name="groupMapID" id="groupMapID">
			<option value="">Object</option>
			<option value="1">Map</option>
			<!-- <option value="2">Zone</option>
			<option value="3">Camera</option>
			<option value="4">Box</option> -->
		</select>
		<select class="infoGrp" name="blinkOJ" id="blinkOJ">
			<option value="">No Blink</option>
			<option value="blink01">Blink 3.0 sec</option>
			<option value="blink02">Blink 2.0 sec</option>
			<option value="blink03">Blink 1.0 sec</option>
			<option value="blink04">Blink 0.5 sec</option>
			<option value="blink05">Blink 0.3 sec</option>
			<option value="blink06">Blink 0.1 sec</option>
		</select>

		<input type="color" id="colorFill" name="colorFill" style="height: 26px;">
		<span style="margin-left: 10px;"></span>
		<button class="updateGrp" id="infoUpload" name="infoUpload">Upload</button>
		<span style="margin-left: 10px;"></span>
		<a href="/data/image/ims/ims_map.svg" download="imsMap_.svg" onclick="this.download='imsMap_' + getFormattedTime() + '.svg'"><button>Save</button></a>

		<button id="svgFit">Fit</button>
		<div style ="display: inline;" id="svgGroup"></div>
		<div style ="display: block;" id="svgGroupList">Grpup List that ID With Prefix</div>
	</div>
	<div id="groupList">Show All Second Grpup List(svg > g > g)</div>
<?php } ?>
</body>
</html>