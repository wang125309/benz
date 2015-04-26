(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
require("../../../bower_components/jquery/src/jquery.js");

$(function(){
    $(".login-btn > .btn").on("click",function(){
        if( $(".username").val().length > 0 && $(".password").val().length > 0 ) {
            $.post({
                "username":$(".username").val(),
                "password":$(".password").val()
            },function(data){
                if(data.status == "success") {
                    location.href = "/backend/userList";
                }
                else {
                    alert("后台请求处理出现异常");
                }
            });
        }
        else {
            alert("请确保输入了您的用户名或密码");
        }
    });
});


},{"../../../bower_components/jquery/src/jquery.js":2}],2:[function(require,module,exports){
define([
	"./core",
	"./selector",
	"./traversing",
	"./callbacks",
	"./deferred",
	"./core/ready",
	"./data",
	"./queue",
	"./queue/delay",
	"./attributes",
	"./event",
	"./event/alias",
	"./manipulation",
	"./manipulation/_evalUrl",
	"./wrap",
	"./css",
	"./css/hiddenVisibleSelectors",
	"./serialize",
	"./ajax",
	"./ajax/xhr",
	"./ajax/script",
	"./ajax/jsonp",
	"./ajax/load",
	"./event/ajax",
	"./effects",
	"./effects/animatedSelector",
	"./offset",
	"./dimensions",
	"./deprecated",
	"./exports/amd",
	"./exports/global"
], function( jQuery ) {

return jQuery;

});

},{}]},{},[1])