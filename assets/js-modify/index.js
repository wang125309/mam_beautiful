require('../../bower_components/zepto/zepto.js');
require('../../bower_components/zeptojs/src/touch.js');
require('../../bower_components/velocity/velocity.js');
require('./share.js');
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

window.onload = function(){
    $.get("/nabob/first_title/",function(data){
        $(".money-count").text(data.total);
        $(".friend-count").text(data.help_count);
        $(".power-rank").text(data.rank);
    });

    map_width = $(".map").width();
    map_height = $(".map").height();
    console.log(map_width+" "+map_height);
    point = new Array();
    point[0] = [0.855,0.89,"go"]; 
    point[1] = [0.870,0.615,"bag_20"];
    point[2] = [0.799,0.442,"bag_100"];
    point[3] = [0.846,0.282,"bag_20"];
    point[4] = [0.662,0.152,"apple_100"];
    point[5] = [0.737,0.033,"bag_200"];
    point[6] = [0.477,0.074,"bag_0"];
    point[7] = [0.308,-0.039,"bag_20"];
    point[8] = [0.095,0.016,"bag_100"];
    point[9] = [0.133,0.169,"bag_20"];
    point[10] = [0.010,0.158,"iphone6"];
    point[11] = [0.122,0.438,"apple_100"];
    point[12] = [0.040,0.663,"bag_0"];
    point[13] = [0.285,0.752,"bag_20"];
    point[14] = [0.523,0.671,"bag_100"];

    for(i=0;i<15;i++){
        $("<div id='p_"+i+"'><img style='width:"+map_width*0.1325+"px' src='/nabob/static/image/"+point[i][2]+".png'/></div>").insertAfter($(".map"));
        $("#p_"+i).css({
            "position":"absolute",
            "left":"5%",
            "margin-left":point[i][0]*map_width+"px",
            "top":point[i][1]*map_height+"px"
        });
    }
    pos = $("#move").val();
    $(".roo").css({
        "margin-left":(point[pos][0])*map_width+"px",
        "top":(point[pos][1]-0.09)*map_height+"px"
        
    });
    $(".join").tap(function(){
        location.href="/nabob/index/?code="+getQueryString("code");
    });
    $(".x a").tap(function(){
        $("#bottom-bar").css("display","none"); 
    });
    total_height = $(".title").height() + $(".middle").height();
    $(".footer").css("top",total_height+"px");
    var move = function(point,now,num) {
        if(num == 0) {
            return ;
        }
        $(".roo").velocity({
            "margin-left":point[now+1][0]*map_height+"px",
            "top":(point[now+1][1]-0.19)*map_height + "px"
        },500,function(){
            $("#move").val((now+1)%14);
            move(point,(now+1)%14,num-1);
        });
        
    }
    if(getQueryString("openid")) {
        
        $.get("/nabob/help_or_not/?openid="+getQueryString("openid"),function(data){
            if(data.status == "true") {
                $("#tip img").attr("src","/nabob/static/image/leifeng.png");
            }
        });
    }

    if($("#tip").data("mode") == "help") {
        $("#tip").velocity("fadeIn");
    }
    w = document.documentElement.clientWidth;
    h = w*0.8*33.1/18.7*0.70;
    $(".message-form").css("top",h*1.1+"px");
    $(".message-form-disable").css("top",h+"px");
    finger_w = $(".zw-outer").height();
    $.get("/nabob/getChance/",function(data){
        $(".num-left").text(data.num);
    });
    $(".cover").css({
        "height":finger_w + "px",
        "width":finger_w + "px",
        "top":"23%",
        "left":w/2-finger_w/2 + "px"
    });
    var coverLongTap = function() {
        $(".cover").velocity({
                "opacity":"1"
                },1000,function(){
                    $(".cover").velocity({
                        "opacity":"0.8"
                        },1000);
                });
        if($("#tip").data("mode") == 'self') {
            $.get("/nabob/num_plus/",function(data){
            });
        }

        $.get("/nabob/getChance/",function(data){
            $(".num-left").text(data.num);
        });
        $(".zw-img").css({
            "-webkit-transform":"rotate(720deg) translateZ(0)",
            "-webkit-transition":"all 2s ease-out"
        }); 
        setTimeout(function(){
            $(".zw-img").css({      
                "-webkit-transition":"initial",
                "-webkit-transform":"rotate(0deg)",
            });  
            pos = $("#move").val();
            queryString = getQueryString("openid");
            url = "/nabob/move/";
            if(queryString) {
                url += ("?openid="+queryString);
            }
            $.get(url,function(data){
                p = data.move;
                if(p > pos) {
                    m = p - pos;
                }
                else {
                    m = p + 14 -pos;
                }
                $(".zw-div span").text(m);
                move(point,parseInt(pos%14),m);
                $("#move").attr("data-prize",data.prize);
                if(data.prize == 1) {
                    $("#text").text("20元");
                    $("#apple").css("display","none");
                    $(".background").attr("src","/nabob/static/image/p_background_20money.png");
                }
                else if(data.prize == 2) {
                    $("#text").text("100元");
                    $("#apple").css("display","none");
                    $(".background").attr("src","/nabob/static/image/p_background_100money.png");
                }
                else if(data.prize == 3) {
                    $("#text").text("100元");
                    $("#apple").css("display","initial");
                    $(".background").attr("src","/nabob/static/image/p_background_100apple.png");
                }
                else if(data.prize == 4) {
                    $("#apple").css("display","none");
                    $("#tip img").attr("src","/nabob/static/image/tick0self.png");
                }
                else if(data.prize == 5) {
                    $("#text").text("200元");
                    $("#apple").css("display","none");
                    $(".background").attr("src","/nabob/static/image/p_background_200.png");
                }
                if(data.prize != 4) {
                    setTimeout(function(){
                        $(".prize").velocity("fadeIn");
                    },m*500+2000);
                }
                if(getQueryString("openid")) {
                    
                    phone = $(".phone").val();
                    vcode = $(".vcode").val();
                    prize = $("#move").data("prize");
                    type = 'ticket';
                    num = 0;
                    if(prize == 1) {
                        type = 'ticket';
                        num = 20;
                    }
                    else if(prize == 2){
                        type = 'ticket';
                        num =  100;
                    }
                    else if(prize == 3) {
                        type = 'apple';
                        num = 100;
                    }
                    else if(prize == 4) {
                        type = 'ticket';
                        num = 0;
                    }
                    else if(prize == 5) {
                        type = 'ticket';
                        num = 200;
                    }
                    queryUrl ="/nabob/commit_prize/?type="+type+"&num="+num+"&prize="+prize+"&openid="+getQueryString("openid");
                    $.get(queryUrl,function(d){
                        
                            if(d.status == 'help success') {
                        
                            if(d.prize == 1) {
                                $("#help-success > img").attr("src","/nabob/static/image/help-20.png");
                            setTimeout(function(){
                                $("#help-success").velocity("fadeIn");
                            },m*500+4000);
                            }
                            else if(d.prize == 2) {
                                $("#help-success > img").attr("src","/nabob/static/image/help-100.png");
                            setTimeout(function(){
                                $("#help-success").velocity("fadeIn");
                            },m*500+4000);
                            }
                            else if(d.prize == 3) {
                                $("#help-success > img").attr("src","/nabob/static/image/help-apple-100.png");
                            setTimeout(function(){
                                $("#help-success").velocity("fadeIn");
                            },m*500+4000);
                            }
                            else if(d.prize == 4) {
                                
                                $("#tip img").attr("src","/nabob/static/image/zero-tip.png");
                            }
                            else if(d.prize == 5) {
                                $("#help-success > img").attr("src","/nabob/static/image/help-200.png");
                            setTimeout(function(){
                                $("#help-success").velocity("fadeIn");
                            },m*500+4000);
                            }

                        }

                    });
                }
                else {
                    if(data.prize != 4) {
                        setTimeout(function(){
                            $("#message").velocity("fadeIn");
                        },m*500+4000);
                    }
                    else {
                    
                        setTimeout(function(){
                            $("#tip").velocity("fadeIn");
                        },m*500+4000);
                    }
                }
            });
        },2000);
        
    }
    $(".cover").longTap(function(){
        
        if(getQueryString("openid")) {
        
            $.get("/nabob/help_or_not/?openid="+getQueryString("openid"),function(t){
                if(t.status == "true") {
                    return;
                }
                else if(t.status == "false") {
                    coverLongTap();
                }
            });
        }
        else {
            $.get("/nabob/getChance/",function(t){
                if(t.num > 0) {
                    coverLongTap();
                }
                else {
                    return ;
                }
            });
        }


    });
    $(".show-me-ticket").tap(function(){
        location.href="http://www.aixuedai.com/yasuiquan";
    });
    $(".continue-game").tap(function(){
        location.href="/nabob/index/?code="+getQueryString("code");
    });
    $("#ijoin").tap(function(){
        location.href="/nabob/index/";
    });
    if($("#tip").data("mode") == "self") {
        $("#tip img").attr("src","/nabob/static/image/tick0self.png");
    }
    $("#tip img").tap(function(){
        $("#tip").velocity("fadeOut");        
    });
    $("#instruction img").tap(function(){
        $(".instruction-field").velocity("fadeIn");        
    });
    $("#close").tap(function(){
        $(".instruction-field").velocity("fadeOut");
    });
    $(".getcode").tap(function(){
        phone_number = $(".phone").val();
        if(phone_number) {
            $.get("/nabob/sendmsg/?phone="+phone_number,function(data){
                if(data) {
                    $(".vcode").attr("placeholder","验证码已发送");
                }
            });        
        }
    });
    
    $(".click-get").tap(function(){
        phone = $(".phone").val();
        vcode = $(".vcode").val();
        prize = $("#move").data("prize");
        type = 'ticket';
        num = 0;
        if(prize == 1) {
             type = 'ticket';
             num = 20;
        }
        else if(prize == 2){
             type = 'ticket';
             num =  100;
        }
        else if(prize == 3) {
             type = 'apple';
             num = 100;
        }
        else if(prize == 4) {
            type = 'ticket';
            num = 0;
        }
        else if(prize == 5) {
            type = 'ticket';
            num = 200;
        }
        $.get("/nabob/checkcode/?phone="+phone+"&vcode="+vcode+"&type="+type+"&num="+num+"&prize="+prize,function(data){
            if(data.status == 'self success') {
            $.get("/nabob/openid/",function(openid){
            $.get("/nabob/bonus_or_not/",function(d){
                $("#get-success-area").velocity("fadeIn");
                link = "http://www.360youtu.com/nabob/index/";
                if(d.status == 'true') {
                    link += ("?openid="+openid.openid);
                }
		        wx.ready(function(){
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

            }
            else if(data.status == 'self failed') {
                location.href = location.href;
            }
        });

    });

    $(".click-nophone-get").tap(function(){
        prize = $("#move").data("prize");
        type = 'ticket';
        num = 0;
        if(prize == 1) {
             type = 'ticket';
             num = 20;
        }
        else if(prize == 2){
             type = 'ticket';
             num =  100;
        }
        else if(prize == 3) {
             type = 'apple';
             num = 100;
        }
        else if(prize == 4) {
            type = 'ticket';
            num = 0;
        }
        else if(prize == 5) {
            type = 'ticket';
            num = 200;
        }
        
        queryUrl ="/nabob/commit_prize/?type="+type+"&num="+num+"&prize="+prize;
        $.get(queryUrl,function(data){
            if(data.status == 'self success') {
                if(data.prize) {
                    $("#get-success-area").velocity("fadeIn");
                }
            }

        });
    });
    $(".invite").tap(function(){
        $("#share-background").velocity("fadeIn");        
        wx.showOptionMenu();
    });
    $("#share-background").tap(function(){
        $("#share-background").velocity("fadeOut");
    });
}
