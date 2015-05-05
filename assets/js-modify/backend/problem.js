$ = require("../../../bower_components/jquery/dist/jquery.js");

$(function(){
    $.get("/benz/backend/getProblemId/?taskid="+$("#id").data("taskid"),function(d){
        console.log(d.problemId);
        if(d.problemId != $("#id").data("id")) {
            location.href = location.href; 
        }
        else {
            setInterval(function(){
                $(".s"+$(".num").html()).css({
                    "background":"#1f1f1f"
                });
                $(".num").html($(".num").html()-1);
                if($(".num").html() <= '0') {
                    $.get("/benz/backend/setProblemId/?taskid="+$("#id").data("taskid"),function(){
                        location.href = location.href;
                    });
                }
            },1000);
         }
    }); 
});
