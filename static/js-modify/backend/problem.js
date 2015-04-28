$ = require("../../../bower_components/jquery/dist/jquery.js");

$(function(){
    $.get("/benz/backend/getProblemId/",function(d){
        console.log(d.problemId);
        if(d.problemId != $("#id").data("id")) {
            location.href = "/benz/backend/problem/?id="+d.problemId; 
        }
        else {
            setInterval(function(){
                $(".s"+$(".num").html()).css({
                    "background":"#1f1f1f"
                });
                $(".num").html($(".num").html()-1);
                if($(".num").html() <= '0') {
                    $.get("/benz/backend/setProblemId/?id="+parseInt($("#id").data("id")+1),function(){
                        location.href = "/benz/backend/problem/?id="+parseInt($("#id").data("id")+1);
                    });
                }
            },1000);
         }
    }); 
});
