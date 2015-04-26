require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");

window.onload = function() {
    $("#login-btn").on("click",function(){
        $.post("/benz/spot/loginAction/",{
            "username":$(".user-text").val(),
            "password":$(".password-text").val()
            },function(d){
            if(d.status == 'success') {
                location.href = location.href;    
            }
            else {
                alert(d.reason); 
            }
        });
    });
}
