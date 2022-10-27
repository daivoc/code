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
// $imsSvg = G5_URL.'/'.G5_DATA_DIR.'/image/ims/ims_map.svg';
?>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=0,maximum-scale=10,user-scalable=yes">
<script type="text/javascript" src="jquery/jquery-3.1.1.min.js"></script>
<script type="text/javascript" src="jquery/ui/jquery-ui.js"></script>
<link rel="stylesheet" type="text/css" href="jquery/ui/jquery-ui.css">
<script type="text/javascript" src="svg-pan-zoom/svg-pan-zoom.js"></script>

<script>

var curElementTitle;
var newElementTitle;
var curElementID;
var newElementID;

$(document).ready(function() {

	// $("#content").mousedown(function (e) {
	// $("#svg_id").mousedown(function (e) {
	$(".svg-pan-zoom_viewport").mousedown(function (e) {
		$("#coord").val("x:"+e.offsetX+", y:"+e.offsetY);
	});
	
	// $( "*", document.body ).click(function( event ) {
		// // var offset = $( this ).offset();
		// var offset = $( "#g200t210_192_168_0_202_0011" ).offset();
		// event.stopPropagation();
		// // $( "#result" ).text( this.tagName + " coords ( " + offset.left + ", " + offset.top + " )" );
		// $("#coord").val( " coords ( " + offset.left + ", " + offset.top + " )" );
		// // $("#coord").val( this.tagName + " coords ( " + offset.left + ", " + offset.top + " )" );
	// });


	// 참고 : https://openclassrooms.com/courses/ultra-fast-applications-using-node-js/socket-io-let-s-go-to-real-time
	$( "circle, path, polygon, rect, ellipse" ).on('click', function () { // 마우스 및 모바일(touchstart) 텝 적용
		curElementTitle = $(this).find('title').html();
		curElementID = $(this).attr('id');
		if (!curElementID){
			curElementID = Math.floor(Math.random() * 100000000);
			$(this).attr("id",curElementID);
		}
		$("#curTitle").val(curElementTitle);
		$("#curID").val(curElementID);
		$("#newTitle").val('');
		$("#newID").val(curElementID);
	});

	$('#log .newElements').on('click', function () {
		alert($(this).data( "id" ));
	});
		
	$('#infoUpload').on('click', function () {
		var r = confirm("Do you want upload?");
		if (r == true) {
			$.post("./upload.php", {
				svgCode: $('#content').html(),
			},
			function(data,status){
				$('#log').append("<div style='color:silver' >"+data+"</div>");
				// $("#log").prepend(status);
			});
		}
	});

	$('#infoUpdate').on('click', function () {
		newElementTitle = $("#newTitle").val();
		newElementID = $("#newID").val().replace(/\s/g, ''); // str.replace(/\s/g, '');
		if(newElementTitle || newElementID) {
			var r = confirm("Do you want update?");
			if (r == true) {
				if(newElementTitle) {
					$("#"+curElementID).html('<title>'+newElementTitle+'</title>');
					var el = $('<div class="newElements" style="color:silver" data-id="'+newElementID+'">Title:'+curElementTitle+' -> '+newElementTitle+'</div>');
					$("#log").append(el);
				}
				if(newElementID) {
					$("#"+curElementID).attr("id",newElementID);
					var el = $('<div class="newElements" style="color:silver" data-id="'+newElementID+'">ID:'+curElementID+' -> '+newElementID+'</div>');
					$("#log").append(el);
				}
				
				$("#curTitle").val('');
				$("#newTitle").val('');
				$("#curID").val('');
				$("#newID").val('');
				curElementTitle = '';
				newElementTitle = '';
				curElementID = '';
				newElementID = '';
			}
		} else {
			alert("Need Value!");
		}
	});

	$( "#resetID" ).click(function() {
		var r = confirm("실행하면 모든 요소의 ID가 새롭게 정열합니다?");
		if (r == true) {
			$( "circle" ).each(function( index ) {
			  // console.log( index + ": " + $( this ).attr("id") );
			  $( this ).attr("id","circ_"+(100000+index));
			});
			$( "path" ).each(function( index ) {
			  // console.log( index + ": " + $( this ).attr("id") );
			  $( this ).attr("id","path_"+(100000+index));
			});
			$( "polygon" ).each(function( index ) {
			  // console.log( index + ": " + $( this ).attr("id") );
			  $( this ).attr("id","poly_"+(100000+index));
			});
			$( "rect" ).each(function( index ) {
			  // console.log( index + ": " + $( this ).attr("id") );
			  $( this ).attr("id","rect_"+(100000+index));
			});
			$( "ellipse" ).each(function( index ) {
			  // console.log( index + ": " + $( this ).attr("id") );
			  $( this ).attr("id","elli_"+(100000+index));
			});
		}
	});

	////// SVG ID 자동 수정 ////
	// $("svg").attr("id","svg_id");
	// $('#log').append("<div style='color:silver' >Auto setted that SVG_ID.</div>");
});

function copyClipboard() {
	/* Get the text field */
	var copyText = document.getElementById("newID");

	/* Select the text field */
	copyText.select();

	/* Copy the text inside the text field */
	document.execCommand("copy");

	/* Alert the copied text */
	//alert("Copied the text: " + copyText.value);
}
</script>

<style>

body { padding:0;margin:0; background:black;}
svg { display: inline; width: 100%; min-width: inherit; max-width: inherit; height: 100%; min-height: inherit; max-height: inherit; }
input, button { font-size: 12px; margin: 10px; border: 0; color: gray; padding: 4px; }

circle, path, polygon, rect, ellipse { cursor: pointer; }
circle:hover, path:hover, polygon:hover, rect:hover, ellipse:hover{stroke:white;stroke-width:2;}

.hide { display:none; }
.center { text-align: center; }
.relative { position: relative; }
.charts { margin: 10px; }
.readonly { color: white; background: gray; }

#curID, #newID { background: gray; color: white; }

#log { background-color: #000000; font-size: 8pt; width: auto; height: auto; float: right; position: absolute; top: 36px; overflow: hidden; overflow-y: -webkit-paged-x; margin: 10px; padding: 6px; }
#logDetail_form { display:none; position: relative; }
#logMonitor_form { float: right; position: relative; }
#list { background-color: #00000080; font-size: 8pt; height: 200px; float: left; line-height: 12px; position: relative; overflow: hidden; overflow-y: auto; margin: 10px; padding: 6px; }
#desc { position: absolute; border: 1px solid gray;margin: 10px;background: linear-gradient(145deg, black, transparent);; }
#content { position: absolute; top: 0; right: 0; bottom: 0; left: 0; overflow: hidden; border-top: 1px solid silver;}
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
	<div id="desc">
		<input type="hidden" class="readonly" id="coord" readonly />
		<input type="hidden" class="readonly" id="curTitle" readonly />
		<input type="hidden" class="readonly" id="curID" readonly />
		<input type="text" id="newID" value="" placeholder="New ID" />
		<button class="clip" onclick="copyClipboard()">Copy</button>
		<button class="resetID" id="resetID">Reset ID</button>
		<input type="hidden" id="newTitle" placeholder="New Title" />
		<button id="infoUpdate" name="infoUpdate" class="hide">Update</button>
		<button id="infoUpload" name="infoUpload" class="hide">Upload</button>
	</div>
<?php } ?>

<script>
window.onload = function() {
	// var panZoom = svgPanZoom('#svg_id', {
	var panZoom = svgPanZoom('svg', {
		viewportSelector: '.svg-pan-zoom_viewport',
		zoomEnabled: true,
		maxZoom: 100,
		controlIconsEnabled: false,
		fit: true,
		center: true,
	});
};
</script>

</body>
</html>