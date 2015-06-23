$(function(){
    $("#taskList").on("click",function(){
        location.href = "/benz/backend/taskList/";
    });
    $("#userList").on("click",function(){
        location.href = "/benz/backend/userList/";
    });
    $("#quit").on("click",function() {
        $.get("/benz/backend/quitAction/",function(d){
            if(d.status == "success") {
                location.href = "/benz/backend/login/";
            }
            else {
                alert("登出错误");
            }
        });
    });
});
