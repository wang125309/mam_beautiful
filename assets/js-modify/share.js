$(function(){
	$.post("/wxconfig/",{
		"url":location.href
	},
	function(data){
		wx.config(data);
		wx.ready(function(){
			$.get("/click/",function(data){
				wx.onMenuShareTimeline({
					title:'我是第'+data.num+'位加⼊入“和妈妈⼀一起 美丽下厨”⾏行动的参与者,我 为妈妈赢取六⽉月鲜新年礼包',
					link:'http://beauty.limijiaoyin.com/login/',
					imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
				});
				wx.onMenuShareAppMessage({
					title:'我是第'+data.num+'位加⼊入“和妈妈⼀一起 美丽下厨”⾏行动的参与者,我 为妈妈赢取六⽉月鲜新年礼包',
					link:'http://beauty.limijiaoyin.com/login/',
					imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
				});
			});
		});
		wx.success(function(){
			
		});
		wx.error(function(){
			$.get("/update_access_token/",function(data){
				$.get("/wxconfig/",function(data){
					wx.config(data);
					wx.ready(function(){
						$.get("/click/",function(data){
							wx.onMenuShareTimeline({
								title:'我是第'+data.num+'位加⼊入“和妈妈⼀一起 美丽下厨”⾏行动的参与者,我 为妈妈赢取六⽉月鲜新年礼包',
								link:'http://beauty.limijiaoyin.com/login/',
								imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
							});
							wx.onMenuShareAppMessage({
								title:'我是第'+data.num+'位加⼊入“和妈妈⼀一起 美丽下厨”⾏行动的参与者,我 为妈妈赢取六⽉月鲜新年礼包',
								link:'http://beauty.limijiaoyin.com/login/',
								imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
							});
						});	
					});
				});
			});
		});

	});
	
});

