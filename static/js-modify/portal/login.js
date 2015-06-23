require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");

window.onload = function() {
    cansubmit = false;
    $(".phone input").on("keyup",function(){
        if($(this).val().length == 11 && $(".name input").val().length > 0 &&$(".name input").val().length < 127) {
            if(cansubmit == false) {
                $(".submit-btn").css("background","url('/static/image/submit-active.png') no-repeat cover;");
                cansubmit = true;
            }
        }
        else {
            if(cansubmit == true) {
                $(".submit-btn").css("background","url('/static/image/sure-submit.png') no-repeat cover;");
                cansubmit = false;
            }
        }
    });
    $(".name input").on("keyup",function(){
        if($(".phone input").val().length == 11 && $(this).val().length > 0 &&$(this).val().length < 127) {
            if(cansubmit == false) {
                $(".submit-btn").css("background","url('/static/image/submit-active.png') no-repeat cover;");
                cansubmit = true;
            }
        }
        else {
            if(cansubmit == true) {
                $(".submit-btn").css("background","url('/static/image/sure-submit.png') no-repeat cover;");
                cansubmit = false;
            }
        }
    });
    $(".submit-btn").on("click",function(){
        if($(".phone input").val() && $(".name input").val()) {
            $.get("/benz/portal/loginAction/?phone="+$(".phone input").val()+"&username="+$(".name input").val(),function(d){
                if(d.status == 'success') {
                    location.href = "/benz/portal/portal/";
                }
                else {
                    alert(d.reason);
                }
            });
        }
        else {
            return false;
        }
    });
}
