require('../../bower_components/zepto/zepto.js');
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}
var wx_login = function() {
    var address = 'blow';
	var call_back_uri = "http%3A%2F%2Fwww.360youtu.com%2F"+address+"%2Fpublic%2F";
    if(getQueryString("openid")) {
        call_back_uri += "?openid="+getQueryString("openid");
    }
	var grant_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx91e4c1925de9ff50&redirect_uri="+call_back_uri+"&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect";
	location.href=grant_url;
    
}
$(function(){
	wx_login();
});
