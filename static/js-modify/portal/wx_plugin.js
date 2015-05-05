$(function(){
    function handleSuccess(position){
        var lng = position.coords.longitude; 
        var lat = position.coords.latitude; 
        $.post("/benz/portal/upload_location/",{
            "latitude":lat,
            "longitude":lng
        },function(d){
            if(d.status == 'success') {
            }
        });
    }
    function handleError() {
    }
    if (window.navigator.geolocation) {
        var options = {
            enableHighAccuracy:true,
        };
        window.navigator.geolocation.getCurrentPosition(handleSuccess,handleError,options);
    }
    else {
        alert("浏览器定位失败");
    }

    $.post("/benz/portal/wxconfig/",{
		"url":location.href
	},function(data){
		wx.config(data);
		wx.ready(function(){
            wx.hideOptionMenu();
        });
        wx.error(function(){
            $.get("/benz/portal/update_access_token/",function(){
                $.post("/benz/portal/wxconfig/",{
                    "url":location.href
                    },function(data){
                    wx.config(data);
                    wx.ready(function(){
                        wx.hideOptionMenu();
                    });
                });
            });
        });
    });
    $(".left-menu").on("click",function(){
        location.href = '/benz/portal/menu/' ;   
    }); 
});
