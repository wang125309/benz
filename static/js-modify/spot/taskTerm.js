require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.js");

$(function(){
    $(".submit").on("click",function(){
        $.get("/benz/spot/submitScore/?term="+$(".scoreAdd").data("term")+"&taskid="+$(".body").data("taskid"),function(d){
            if(d.status == 'success') {
                location.href=location.href;
            }
        });
    });
    $(".ok").on("click",function(){
        location.href = "/benz/spot/taskTerm/?task_id="+$(".body").data("taskid")+"&term="+$(".body").data("term");
    });
    $(".register").on("click",function(){
        location.href = "/benz/spot/addTermList/?term="+$(".scoreAdd").data("term")+"&taskid="+$(".body").data("taskid");
    });
    $(".addtoterm").on("click",function(){
        $(".addMenu").show();
        $(".addMenu .title-spot").data("id",$(this).data("id"));
        $(".addMenu .title-spot .username").html($($(this).children()[1]).html());

    });
    $(".sure").on("click",function(){
        $.get("/benz/spot/addToTerm/?taskid="+$(".body").data("taskid")+"&term="+$(".body").data("term")+"&id="+$(".title-spot").data("id"),function(d){
            if (d.status == 'success') {
                location.href = location.href ;
            }
        });
    });
    $(".cancel").on("click",function(){
        $(".addMenu").hide();
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
       var term = handAdd.data('term');
       var phone = $('#phone').val();
       var taskid = handAdd.data('taskid');
        $.ajax({type:'post',url:'/benz/spot/addUser',data: 
            {"username": username, "phone":phone, "term": term, "taskid": taskid},
            success:function(result){
                if(result.success)location.href=location.href;
            },
            error:function(){
                handAdd.hide();
            }
        });
    });
    $(".user-tr").on("click", function(e){
        var scoreAdd = $('.scoreAdd');
        var score ='';
        var id = '';
        if($(e.target).parent('.user-tr').length){
            id = $(e.target).parent('.user-tr').data('id');
            score = $(e.target).parent('.user-tr').data('score');
        }
        if(!id)return;
        if(id)scoreAdd.data('id', id);
        if(score)scoreAdd.data('score', score);
        if(typeof(score)!="undefined")$('#score').val(score);
        scoreAdd.show();
    });
    $("#editscore-cancel").on("click", function(){
        $('#score').val("");
        $('.scoreAdd').hide();
    });
    $("#editscore-btn").on("click", function(){
         var scoreAdd = $('.scoreAdd');
         var score_input = $('#score');
         var id = scoreAdd.data('id');
         var score = scoreAdd.data('score');
         var term = scoreAdd.data('term');

         if(!id)return;
         if(score == score_input.val())return;
         score = score_input.val();
         flag = false;
         if(term == 'driver-success') {
            if (score > 6)
            {   
                flag = true;
                alert("非凡驾驶项目不允许超过6积分");
            }
         }
         if(term == 'throw-money') {
            if(score>70) {
                flag = true;
                alert("千金一掷项目不允许超过70积分");
            }
         }
         if (term == 'big-buy') {
            if(score>10) {
                flag = true;
                alert("大富翁项目不允许超过10积分");
            }
         }
         if(!flag){
         $.ajax({type:'post',url:'/benz/spot/addScore',data: {user_id: id, score: score, term: term},
            success:function(result){
                if(result.success)location.href=location.href;
            },
            error: function(result){
                
            }
        });
         }
    })
});
