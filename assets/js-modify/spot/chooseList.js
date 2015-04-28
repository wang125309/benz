require("../../../bower_components/zepto/zepto.js")
require("../../../bower_components/zeptojs/src/touch.js")

$(function(){
    $(".taskname").on("click", function(e){
        location.href = "/benz/spot/registerList/"+$(e.target).data("id");
    })
})
