$(function(){
	$.post("/wxconfig/",{
		"url":location.href
	},
	function(data){
		wx.config(data);
		wx.ready(function(){
			$.get("/click/",function(data){
				wx.onMenuShareTimeline({
					title:'我是第'+data.num+'位加入“和妈妈⼀起美丽下厨”的参与者,我为妈妈赢取六月鲜新年礼包',
					link:'http://slide.limijiaoyin.com/slides/mama#p0',
					imgUrl:'https://mmbiz.qlogo.cn/mmbiz/dlicpJRTtH14ogKDC0hbXyjNibtqsYmxA0CdRfibzsMj0AbACLg6hia858sUJ3gkMSuxJQkKl62gDS7SwlHj7nKVEg/0',
					success: function(){
						$("#sharebox").velocity("fadeOut");
						$(".edit-body").velocity("fadeOut");
					},
				});
				wx.onMenuShareAppMessage({
					title:'和妈妈一起美丽下厨',
					desc:'我是第'+data.num+'位加入“和妈妈⼀起美丽下厨”⾏动的参与者,我为妈妈赢取六月鲜新年礼包',
					link:'http://slide.limijiaoyin.com/slides/mama#p0',
					imgUrl:'https://mmbiz.qlogo.cn/mmbiz/dlicpJRTtH14ogKDC0hbXyjNibtqsYmxA0CdRfibzsMj0AbACLg6hia858sUJ3gkMSuxJQkKl62gDS7SwlHj7nKVEg/0',
					success:function(){
						$("#sharebox").velocity("fadeOut");	
						$(".edit-body").velocity("fadeOut");

					},
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
									title:'我是第'+data.num+'位加入“和妈妈⼀起美丽下厨”的参与者,我为妈妈赢取六月鲜新年礼包',
									link:'http://slide.limijiaoyin.com/slides/mama#p0',
									imgUrl:'https://mmbiz.qlogo.cn/mmbiz/dlicpJRTtH14ogKDC0hbXyjNibtqsYmxA0CdRfibzsMj0AbACLg6hia858sUJ3gkMSuxJQkKl62gDS7SwlHj7nKVEg/0',
									success:function(){
										$("#sharebox").velocity("fadeOut");	
						$(".edit-body").velocity("fadeOut");

									},
								});
								wx.onMenuShareAppMessage({
									title:'和妈妈一起美丽下厨',
									desc:'我是第'+data.num+'位加入“和妈妈⼀起美丽下厨”⾏动的参与者,我为妈妈赢取六月鲜新年礼包',
									link:'http://slide.limijiaoyin.com/slides/mama#p0',
									imgUrl:'https://mmbiz.qlogo.cn/mmbiz/dlicpJRTtH14ogKDC0hbXyjNibtqsYmxA0CdRfibzsMj0AbACLg6hia858sUJ3gkMSuxJQkKl62gDS7SwlHj7nKVEg/0',
									success:function(){
											$("#sharebox").velocity("fadeOut");	
						$(".edit-body").velocity("fadeOut");

									},
								});
							
							});	
						});
					});
				});
			});

		});


	});
});

