require('../../bower_components/zepto/zepto.js');
require('../../bower_components/zeptojs/src/touch.js');
require('../../bower_components/velocity/velocity.js');
window.onload = function() {
	var coner_width = $(".coner").width();
	var text_height = $(".bouns-center").height();
	$(".coner").css({
		"width":2*(coner_width-text_height) + text_height + "px",
		"height":2*(coner_width-text_height) + text_height + "px",
		"margin-top":"-"+(coner_width-text_height) + "px"
	});
	bigger = 5;
	$(".coner").velocity({
		"height":(2*(coner_width-text_height) + text_height) + 2*bigger + "px",
		"width":(2*(coner_width-text_height) + text_height) + 2*bigger + "px",
		"margin-left":-bigger + "px",
		"margin-top":-(coner_width-text_height)-bigger + "px"
	},{
		"during":150,
		"loop":true
	});
	$(".help-mom").tap(function(){
		$(".edit-body").velocity("fadeIn");
	});
	$(".again-mom").tap(function(){
		location.href = "/index";
	});
	$(".right-btn").tap(function(){
		$("#sharebox").velocity("fadeIn");
	});
}
