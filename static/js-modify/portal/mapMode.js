require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");
$(function(){
    w = $(window).width();
    h = $(window).height();
    $(".littleCource").css({
        "left":w/320*221+"px",
        "bottom":w/320*247+"px"
    });
    $(".fiveCan").css({
        "left":w/320* +"px",
        "bottom":w/320* +"px"
    });
});
