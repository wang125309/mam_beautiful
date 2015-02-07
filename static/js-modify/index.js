require('../../bower_components/zepto/zepto.js');
require('../../bower_components/zeptojs/src/touch.js');
require('../../bower_components/velocity/velocity.js');
window.onload = function() {
	var line_width = $(".finger-image").width();
	$(".line").css("width",line_width+"px");
	$(".line").css("margin-left","-"+line_width/2+"px");
	$(".line").velocity({
		height:line_width+"px"
	},{
		duration:800,
		loop:true
	});
	$(".finger-area").tap(function(){
		location.href="/bonus";
	});
	$(".instruct").tap(function(){
		$(".instruction").velocity("fadeIn");
	});
	$(".instruction-close").tap(function(){
		$(".instruction").velocity("fadeOut");
	});
};
