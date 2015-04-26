require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");

window.onload = function() {
    $(".little-cource").on("click",function(){
        location.href = "/benz/portal/littleCource/";
    });
    $(".space-rebuild").on("click",function(){
        location.href = "/benz/portal/spaceRebuild/";
    });
    $(".get-first").on("click",function(){
        location.href = "/benz/portal/getFirst/";
    });
    $(".five-can").on("click",function(){
        location.href = "/benz/portal/fiveCan/";
    });
    $(".option").on("click",function(){
        location.href = "/benz/portal/option/";
    });
    $(".perfect-in").on("click",function(){
        location.href = "/benz/portal/perfectIn/";
    });
    $(".drive-success").on("click",function(){
        location.href = "/benz/portal/driveSuccess/";
    });
    $(".big-buy").on("click",function(){
        location.href = "/benz/portal/bigBuy/";
    });
    $(".hot-person").on("click",function(){
        location.href = "/benz/portal/hotPerson/";
    });
    $(".throw-money").on("click",function(){
        location.href = "/benz/portal/throwMoney/";
    });
}
