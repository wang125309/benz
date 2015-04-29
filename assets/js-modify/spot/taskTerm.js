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
        var userno = $('#userno').val();
        $.ajax({type:'post',url:'/benz/spot/addUser/',data: {username: username, userno: userno},
            success:function(result){
                if(result.status=='success')location.href=location.href;
            },
            error:function(){
                handAdd.hide();
            }
        });
    });
    $(".user-tr").on("click", function(e){
        var score = $(e.target).find('#td-score').text();
        console.log($(e.target).find('#td-score'));
        console.log(score);
        if(typeof(score)!="undefined")$('#score').val(score);
        $('.scoreAdd').show();
    });
    $("#editscore-cancel").on("click", function(){
        $('#score').val("");
        $('.scoreAdd').hide();
    })
});
