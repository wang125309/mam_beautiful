$(function(){
	$.post("/wxconfig/",{
		"url":location.href
	},
	function(data){
		wx.config(data);
		wx.ready(function(){
			$.get("/click/",function(data){
				wx.onMenuShareTimeline({
					title:'我是第'+data.num+'位加⼊入“和妈妈⼀起美丽下厨”的参与者,我为妈妈赢取六月鲜新年礼包',
					link:'http://beauty.limijiaoyin.com/login/',
					imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
				});
				wx.onMenuShareAppMessage({
					title:'和妈妈一起美丽下厨',
					desc:'我是第'+data.num+'位加⼊入“和妈妈⼀起美丽下厨”⾏动的参与者,我为妈妈赢取六⽉月鲜新年礼包',
					link:'http://beauty.limijiaoyin.com/login/',
					imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
				});
			});
			wx.error(function(res){
				$.get("/update_access_token/",function(data){
					$.post("/wxconfig/",{
						"url":location.href
						},function(data){
							wx.config(data);
							wx.ready(function(){
							$.get("/click/",function(data){
								wx.onMenuShareTimeline({
									title:'我是第'+data.num+'位加⼊入“和妈妈⼀起美丽下厨”的参与者,我为妈妈赢取六月鲜新年礼包',
									link:'http://beauty.limijiaoyin.com/login/',
									imgUrl:'http://beauty.limijiaoyin.com/static/image/share-center.png'
								});
								wx.onMenuShareAppMessage({
									title:'和妈妈一起美丽下厨',
									desc:'我是第'+data.num+'位加⼊入“和妈妈⼀起美丽下厨”⾏动的参与者,我为妈妈赢取六⽉月鲜新年礼包',
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
});

