$ = require("../../../bower_components/jquery/dist/jquery.js");
require("./lib/logout.js");
$(function(){
    var edit_id = 0;
    var saved = 0;
    var del_id = 0;
    $(".del").on("click",function(){
        del_id = $(this).data("id"); 
        $(".name").text(del_id);
        $("#del-menu").fadeIn();
    });
    $(".delete").on("click",function(){

        $.get("/benz/backend/deleteUser/?id="+del_id,function(d){
            if(d.status == 'success') {
                location.href = location.href;
            }
            else {
                alert(d.reason);
            }
        });
    });
    $(".opt").on("click",function(){
        saved = 0;
        edit_id = $(this).data("id");
        $("#edit-user").fadeIn();
        $.get("/benz/backend/getUserMessage/?id="+$(this).data("id"),function(d){
            $("#username").val(d.data.username);
            $("#password").val(d.data.password);
            $("select.task").val(d.data.task);
            if(d.data.type == 1) {
                $("#normal").prop({"checked":"checked"});
            }
            else {
                $("#controller").prop({"checked":"checked"});
            }
        });
    });
    $("#addUser").on("click",function(){
        saved = 0;
        edit_id = 0
        $("#edit-user").fadeIn();
        $("#username").val("");
        $("#password").val("");
        $("#normal").prop("checked","");
        $("#controller").prop("checked","");
    });

    $(".save").on("click",function(){
        if(!saved) {
            first = $("#normal").prop("checked");
            if(first == true) {
                pri = 1;
            }
            else {
                pri = 2;
            }
            $.post("/benz/backend/saveUser/?id="+edit_id,{
                "username":$("#username").val(),
                "password":$("#password").val(),
                "pri":pri,
                "taskid":$("select.task").val()
            },function(d){
                if(d.status == "success") {
                    location.href = location.href;
                }
                else {
                    alert(d.reason);
                }
            });
            saved = 1;
        }
        $("#edit-user").fadeOut();
    });
    $(".cancel").on("click",function(){
        $(".menu").fadeOut();
    });
    
});
