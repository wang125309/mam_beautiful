require('../../bower_components/zepto/zepto.js');
require('../../bower_components/zeptojs/src/touch.js');
require('../../bower_components/velocity/velocity.js');

$(function(){
    map_width = $(".map").width();
    map_height = $(".map").height();
    console.log(map_width+" "+map_height);
    point = new Array();
    point[0] = [0.855,0.89,"go"]; 
    point[1] = [0.523,0.671,"bag_100"];
    point[2] = [0.285,0.752,"bag_20"];
    point[3] = [0.040,0.663,"bag_0"];
    point[4] = [0.122,0.438,"apple"];
    point[5] = [0.010,0.158,"iphone6"];
    point[6] = [0.133,0.169,"bag_20"];
    point[7] = [0.095,0.016,"bag_100"];
    point[8] = [0.308,-0.039,"bag_20"];
    point[9] = [0.477,0.074,"bag_0"];
    point[10] = [0.737,0.033,"bag_200"];
    point[11] = [0.662,0.152,"apple"];
    point[12] = [0.846,0.282,"bag_20"];
    point[13] = [0.799,0.442,"bag_100"];
    point[14] = [0.870,0.615,"bag_20"];
    for(i=0;i<15;i++){
        $("<div id='p_"+i+"'><img style='width:"+map_width*0.1325+"px' src='/static/image/"+point[i][2]+".png'/></div>").insertAfter($(".map"));
        $("#p_"+i).css({
            "position":"absolute",
            "left":"5%",
            "margin-left":point[i][0]*map_width+"px",
            "top":point[i][1]*map_height+"px"
        });
    }
    pos = $("#move").val();
    $(".roo").css({
        "margin-left":point[pos][0]*map_width+"px",
        "top":(point[pos][1]-0.19)*map_height+"px"
    });
    var move = function(point,now,num) {
        if(num == 0) {
            return ;
        }
        $(".roo").velocity({
            "margin-left":point[now+1][0]*map_height+"px",
            "top":(point[now+1][1]-0.19)*map_height + "px"
        },1500,function(){
            $("#move").val(now+1);
            move(point,now+1,num-1);
        });
        
    }
    $(".finger").tap(function(){
        pos = $("#move").val();
        move(point,parseInt(pos),2);
    });
});
