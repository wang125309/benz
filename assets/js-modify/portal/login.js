require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");

window.onload = function() {
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
