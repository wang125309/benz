require("../../../bower_components/zepto/zepto.js")
require("../../../bower_components/zeptojs/src/touch.js")

$(function(){
    $(".item").on("click", function(e){
        if(!$(e.target).data("term"))return;
        location.href = "/benz/spot/taskTerm?task_id="+$(e.target).data("task_id")+"&term="+$(e.target).data("term");
    });

    $(".register").on("click", function(){
        var handAdd = $('.handAdd');
        if(handAdd.css("display")!="none")return;
//        handAdd.velocity("fadeIn");
        handAdd.show();
    });
    $("#adduser-cancel").on("click", function(){
        var handAdd = $('.handAdd');
        $('#username').val("");
        $('#userno').val("");
        handAdd.hide();
    });
    $("#adduser-btn").on("click", function(){
       var handAdd = $('.handAdd');
       var username = $('#username').val();
       var phone = $('#phone').val();
       var taskid = handAdd.data('taskid');
        $.ajax({type:'post',url:'/benz/spot/addUser',data: {username: username,phone:phone, taskid: taskid},
            success:function(result){
                if(result.success)location.href=location.href;
            },
            error:function(){
                handAdd.hide();
            }
        });
    });
});
