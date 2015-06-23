$ = require("../../../bower_components/jquery/dist/jquery.js");
$(function(){
    h = $(window).height();
    w = $(window).width();
    ph = (h-100)/30;
    function getQueryParams(name,url) {
        if(!url)url = location.href;
        name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
         var regexS = "[\\?&]"+name+"=([^&#]*)";
         var regex = new RegExp( regexS );
         var results = regex.exec( url );
         return results == null ? null : results[1];
    };
    res = {};
    var type = 1;
    $.get('/benz/backend/getSignWall/?id='+getQueryParams("id",location.href),function(result){
        res = result;
    },"json");
    setInterval(function(){
        if (type==1) {
            type = 2;
        }
        else {
            type = 1;
        }
    },20000);
    var auto_refresh = function(){
        $.get('/benz/backend/sign/?id='+getQueryParams("id",location.href)+'&type='+type, function(result){
            $(".right-rank").html($($(result)[5]).html());
        }, "html");
    }

    var _time_refresh = function(){
        setTimeout(function(){
            auto_refresh();
            _time_refresh();
        }, 7000)
    }
    
    var _time_out = function(){
        setTimeout(function(){
            _time_out();
        }, 5000);
    }
    _time_out();
    _time_refresh();
});
