require('../../bower_components/zepto/zepto.js');
var wx_login = function() {
	var call_back_uri = "http%3A%2F%2Fbl.limijiaoyin.com%2Findex%2F";
	var grant_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa57abe5e5e6fae56&redirect_uri="+call_back_uri+"&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect";
	location.href=grant_url;
}
$(function(){
	wx_login();
});
