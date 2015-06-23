require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");

$(function() {
    $(".complate-btn").on("tap",function(){
        task = $(".main-area").data("task");
        $.get("/benz/portal/addScore/?taskname="+task,function(d){
            if (d.status == 'success') {
                location.href = location.href;               
            }
            else {
                
            }
        });
    });
});
