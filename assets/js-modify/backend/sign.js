$ = require("../../../bower_components/jquery/dist/jquery.js");

$(function(){
    var children = $(".wall-data").children();
    important = children[children.length-1];
    initPos = [[240,20,0.4],[20,30,0.4],[306,160,0.6],[201,290,0.5],[100,100,0.6],[20,100,0.6],[30,274,0.6],[120,20,0.8],[50,202,0.7],[120,45,0.8]];
    $(important).css({
        "left":"146px",
        "top":"188px"
    });
    for(i=0 ; i<children.length-1 ;i++) {
        $(children[i]).css({
            "left":initPos[i][0]+"px",
            "top":initPos[i][1]+"px",
            "-webkit-transform":"scale("+initPos[i][2]+")"
        });
    }
    var auto_refresh = function(){
        $.get('/benz/backend/sign/', function(result){
             $(".rank").html($($(result).children()[3]).html());
             console.log('ranking');
            }, "html");
    }

    var _time_refresh = function(){
        setTimeout(function(){
            auto_refresh();
            _time_refresh();
        }, 5000)
    }

    var auto_move = function(){
        for(i=0 ; i<children.length-1 ;i++) {
            n = Math.random()*200;
            m = Math.random()*200;
            $(children[i]).animate({
                "left":initPos[i][0]+n,
                "top":initPos[i][1]+m,
                "-webkit-transform":"scale("+initPos[i][2]+")"
            },3000);
        }
    };
    var _time_out = function(){
        setTimeout(function(){
            auto_move();
            _time_out();
        }, 3000);
    }
    _time_out();
    _time_refresh();
});
