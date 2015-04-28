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
        $.get("/benz/backend/deleteTask/?id="+del_id,function(d){
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
        $("#edit-task").fadeIn();
        $.get("/benz/backend/getTaskMessage/?id="+$(this).data("id"),function(d){
            $("#taskname").val(d.data.taskname);
            $("#taskcity").val(d.data.taskcity);
            $("#taskdate").val(d.data.taskdate);
        });
    });
    $("#addTask").on("click",function(){
        saved = 0;
        edit_id = 0
        $("#edit-task").fadeIn();
        $("#taskname").val("");
        $("#taskdate").val("");
        $("#taskcity").val("");
    });

    $(".save").on("click",function(){
        if(!saved) {
            $.post("/benz/backend/saveTask/?id="+edit_id,{
                "taskname":$("#taskname").val(),
                "taskcity":$("#taskcity").val(),
                "taskdate":$("#taskdate").val(),
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
        $("#edit-task").fadeOut();
    });
    $(".cancel").on("click",function(){
        $(".menu").fadeOut();
    });
});
