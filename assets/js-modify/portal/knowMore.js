require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");
$(function() {
    $(".go-score").on("click",function(){
        window.scrollTo(0,0);
    });
    $(".go-area").on("click",function(){
        window.scrollTo(0,400);  
    });
});
