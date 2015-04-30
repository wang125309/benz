require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");

$(function(){
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
       var term = handAdd.data('term');
       var userno = $('#userno').val();
       var taskid = handAdd.data('taskid');
        $.ajax({type:'post',url:'/benz/spot/addUser',data: {username: username, userno: userno, term: term, taskid: taskid},
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
         $.ajax({type:'post',url:'/benz/spot/addScore',data: {user_id: id, score: score, term: term},
            success:function(result){
                if(result.success)location.href=location.href;
            },
            error: function(result){
                
            }
        });
    })
});
