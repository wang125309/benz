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
    setInterval(function(){
        for(i=0 ; i<children.length-1 ;i++) {
            n = Math.random()*200;
            m = Math.random()*200;
            $(children[i]).animate({
                "left":initPos[i][0]+n,
                "top":initPos[i][1]+m,
                "-webkit-transform":"scale("+initPos[i][2]+")"
            },3000);
        }
    },3000);
});
