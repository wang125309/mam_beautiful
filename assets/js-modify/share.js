$(function(){
    $.post("/nabob/wxconfig/",{
		"url":location.href
	},
	function(data){
		wx.config(data);

        $.get("/nabob/openid/",function(openid){
            $.get("/nabob/bonus_or_not/",function(d){
                link = "http://www.360youtu.com/nabob/index/";
                if(d.status == 'true') {
                    link += ("?openid="+openid.openid);
                }
		        wx.ready(function(){
                    wx.hideOptionMenu();
			        wx.onMenuShareTimeline({
                        link:link,
                        imgUrl:"http://www.360youtu.com/nabob/static/image/share.jpg",
                        title:"大学生！不！看！后！悔！一大波压岁钱和苹果机来袭……",
                        success: function(){
				         
                        },
			        });
			        wx.onMenuShareAppMessage({
                        link:link,
                        imgUrl:"http://www.360youtu.com/nabob/static/image/share.jpg",
                        title:"大学生！不！看！后！悔！一大波压岁钱和苹果机来袭……",
                        desc:"这个发给同学，TA会感激你",
				        success:function(){
                        },
			        });
                });
            });
        });
		wx.error(function(res){
			$.get("/nabob/update_access_token/",function(data){
				$.post("/wxconfig/",{
					"url":location.href
				},function(data){
					wx.config(data);
					wx.ready(function(){
						wx.onMenuShareTimeline({
							success:function(){

							},
					    });
						wx.onMenuShareAppMessage({
							success:function(){

							},
						});
							
					});
				});
			});
		});

	});


});
