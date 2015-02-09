require('../../bower_components/zepto/zepto.js');
require('../../bower_components/zeptojs/src/touch.js');
require('../../bower_components/velocity/velocity.js');
window.onload = function() {
	var coner_width = $(".coner").width();
	var text_height = $(".bouns-center").height();
	$(".coner").css({
		"margin-top":-(coner_width-text_height)/2 + "px",
		"margin-left":-coner_width/2 + "px"
	});
	bigger = 5;
	$(".coner").velocity({
		"height":2*bigger+coner_width + "px",
		"width":2*bigger+coner_width + "px",
		"margin-left":-(coner_width/2 + bigger) + "px",
		"margin-top":-(coner_width-text_height + bigger)/2 + "px"
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
