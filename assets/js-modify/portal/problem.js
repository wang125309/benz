require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");

$(function(){
    $(".A").on("click",function(){
           
    });
    $(".B").on("click",function(){
            
    });
    $(".C").on("click",function(){
            
    });
    $(".D").on("click",function(){
            
    });
    setInterval(function(){

        $.get("/benz/backend/getProblemId/",function(d){
            if(d.status == 'success') {

                if(d.problemId != $(".num").text()) {

                    location.href = location.href;
                }
            }
        });        
    },1000);
});
