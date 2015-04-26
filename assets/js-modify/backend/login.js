$ = require("../../../bower_components/jquery/dist/jquery.js");
$(function(){
    $(".login-btn > .btn").on("click",function(){
        if( $(".userinput").val().length > 0 && $(".passwordinput").val().length > 0 ) {
            $.get('/benz/backend/loginAction/',{
                "username":$(".userinput").val(),
                "password":$(".passwordinput").val()
            },function(data){
                console.log(data);
                if(data.status == "success") {
                    location.href = "/benz/backend/userList";
                }
                else {
                    alert("请核对您的用户名密码");
                }
            });
        }
        else {
            alert("请确保输入了您的用户名或密码");
        }
    });
});

