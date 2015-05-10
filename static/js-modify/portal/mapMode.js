require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");
$(function(){
    w = $(window).width();
    h = $(window).height();
    $(".littleCource").css({
        "left":w/320*221+"px",
        "bottom":w/320*247+"px"
    });
    $(".fiveCan").css({
        "left":w/320*94 +"px",
        "bottom":w/320*230 +"px"
    });
    $(".getFirst").css({
        "left":w/320*188 +"px",
        "bottom":w/320*224 +"px"
    });
    $(".bigBuy").css({
        "left":w/320*107+"px",
        "bottom":w/320*217+"px",
        "height":"9vw"
    });
    $(".hotPerson").css({
        "left":w/320*205+"px",
        "bottom":w/320*206+"px",
    });
    $(".spaceRebuild").css({
        "left":w/320*76+"px",
        "bottom":w/320*285+"px",
    });
    $(".option").css({
        "left":w/320*106+"px",
        "bottom":w/320*300+"px",
    });
    $(".perfectIn").css({
        "left":w/320*141+"px",
        "bottom":w/320*285+"px",
    });
    $(".driveSuccess").css({
        "left":w/320*168+"px",
        "bottom":w/320*307+"px",
    });
    $(".throwMoney").css({
        "left":w/320*206+"px",
        "bottom":w/320*257+"px",
        "height":"9vw"
    });
    $(".littleCource").on("tap",function(){
        location.href = '/benz/portal/littleCource/';     
    });
    $(".fiveCan").on("tap",function(){
        location.href = '/benz/portal/fiveCan/';     
    });
    $(".getFirst").on("tap",function(){
        location.href = '/benz/portal/getFirst/';     
    });
    $(".bigBuy").on("tap",function(){
        location.href = '/benz/portal/bigBuy/';     
    });
    $(".hotPerson").on("tap",function(){
        location.href = '/benz/portal/hotPerson/'; 
    });
    $(".spaceRebuild").on("tap",function(){
        location.href = '/benz/portal/spaceRebuild/';     
    });
    $(".option").on("tap",function(){
        location.href = '/benz/portal/option/';     
    });
    $(".perfectIn").on("tap",function(){
        location.href = '/benz/portal/perfectIn/';     
    });
    $(".driveSuccess").on("tap",function(){
        location.href = '/benz/portal/driveSuccess/';     
    });
    $(".throwMoney").on("tap",function(){
        location.href = '/benz/portal/throwMoney/';     
    });
    $(".know-more").on("tap",function(){
        location.href = "/benz/portal/knowMore/";
    });
    $(".tab-map").on("tap",function(){
        location.href = '/benz/portal/portal/#menu';
    });
    $(".score-rank").on("tap",function(){
        location.href = '/benz/portal/scoreRank/';
    });
});
