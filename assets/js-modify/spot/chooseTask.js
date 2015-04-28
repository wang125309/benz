require("../../../bower_components/zepto/zepto.js")
require("../../../bower_components/zeptojs/src/touch.js")

$(function(){
    $(".item").on("click", function(e){
        if(!$(e.target).data("term"))return;
        location.href = "/benz/spot/taskTerm?task_id="+$(e.target).data("task_id")+"&term="+$(e.target).data("term");
    })
})
