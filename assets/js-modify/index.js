require('../../bower_components/zepto/zepto.js');
require('../../bower_components/zeptojs/src/touch.js');
require('../../bower_components/velocity/velocity.js');
require('./share.js');
window.onload = function() {
	var line_width = $(".finger-image").width();
	$(".line").css("width",line_width+"px");
	$(".line").css("margin-left","-"+line_width/2+"px");
	$(".touch-div").css("height",line_width+"px");
	$(".touch-div").css("margin-left","-"+line_width/2+"px");
	$(".touch-div").css("width",line_width+"px");
	$(".line").velocity({
		height:line_width+"px"
	},{
		duration:800,
		loop:true
	});
	$(".finger-area").tap(function(){
		location.href="/bonus";
	});
	var ih = document.documentElement.clientHeight*0.9;
	$(".instruction-close").css("margin-top",ih*0.08+"px");
	$(".instruct").tap(function(){
		$(".instruction").velocity("fadeIn");
	});
	$(".instruction-close").tap(function(){
		$(".instruction").velocity("fadeOut");
	});
	$(".touch-div").tap(function(){
		location.href="/bonus";
	});
	$(".line").tap(function(){
		location.href="/bonus";
	});
};
