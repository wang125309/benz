require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");

$(function(){
    var answered = false;
    var result = function(res) {
        if(res.status == 'true') {
            alert("您已经答对5道题，并且获得积分");
            setTimeout(function(){
                location.href = '/benz/portal/portal/';    
            },1000);
        }
    };
    $(".A").on("click",function(){
        if(answered == false) {
            answered = true;
            $.get("/benz/portal/answer/?answer=A",function(d){
                if(d.status == 'success') {
                    if(d.correct == 'true') {
                        $(".A").css({
                            "background-image":"url('/static/image/correct.png')"
                        });
                        $.get("/benz/portal/right/",function(res) {
                            result(res);             
                        });
                    }
                    else {
                        $(".A").css({
                            "background-image":"url('/static/image/error.png')"
                        });
                    
                    }
                }
            });
        }
    });
    $(".B").on("click",function(){
        if(answered == false) {
            answered = true;
            $.get("/benz/portal/answer/?answer=B",function(d){
                if(d.status == 'success') {
                    if(d.correct == 'true') {
                        $(".B").css({
                            "background-image":"url('/static/image/correct.png')"
                        });
                        $.get("/benz/portal/right/",function(res) {
                            result(res);             
                        });
                    }
                    else {
                        $(".B").css({
                            "background-image":"url('/static/image/error.png')"
                        });
                    }
                }
            });
        }
    });
    $(".C").on("click",function(){
        if(answered == false) {
            answered = true;
            $.get("/benz/portal/answer/?answer=C",function(d){
                if(d.status == 'success') {
                    if(d.correct == 'true') {
                        $(".C").css({
                            "background-image":"url('/static/image/correct.png')"
                        });
                        $.get("/benz/portal/right/",function(res) {
                        
                            result(res);             
                        });
                    }
                    else {
                        $(".C").css({
                            "background-image":"url('/static/image/error.png')"
                        });
                    }
                }
            });
        }
    });
    $(".D").on("click",function(){
        if(answered == false) {
            answered = true;
            $.get("/benz/portal/answer/?answer=D",function(d){
                if(d.status == 'success') {
                    if(d.correct == 'true') {
                        $(".D").css({
                            "background-image":"url('/static/image/correct.png')"
                        });
                        $.get("/benz/portal/right/",function(res) {
                        
                            result(res);             
                        });
                    }
                    else {
                        $(".D").css({
                            "background-image":"url('/static/image/error.png')"
                        });
                    }
                }
            });
        }
    });
    var u = navigator.userAgent;
    if(u.indexOf('iPhone')>-1) {
        $.get("/benz/portal/getProblemId/?taskid="+$(".body").data("taskid"),function(d){
            if(d.status == 'success') {
                if(d.problemId != $(".num").text()) {
                    location.href = location.href;
                }
            }
        });        
    }
    else {
        var s = function() {
            setTimeout(function(){
                $.get("/benz/backend/getProblemId/",function(d){
                    if(d.status == 'success') {
                        if(d.problemId != $(".num").text()) {
                            location.href = location.href;
                        }
                    }
                    s();

                });
                console.log("I do");

            },5000);
        }
        s();
    }
});
