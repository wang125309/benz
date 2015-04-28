$(function(){
    $.post("/benz/portal/wxconfig/",{
		"url":location.href
	},
	function(data){
		wx.config(data);
		wx.ready(function(){
            wx.hideOptionMenu();
            wx.getLocation({
                success: function (res) {
                        var latitude = res.latitude; // 纬度，浮点数，范围为90 ~ -90
                        var longitude = res.longitude; // 经度，浮点数，范围为180 ~ -180。
                        $.post("/benz/portal/upload_location/",{
                            "latitude":latitude,
                            "longitude":longitude
                        },function(d){
                        });
                    }
                });
            });
        wx.error(function(){
            $.get("/benz/portal/update_access_token/",function(){
                $.post("/benz/portal/wxconfig/",{
                    "url":location.href
                    },function(data){
                    wx.config(data);
                    wx.ready(function(){
                        wx.hideOptionMenu();
                        wx.getLocation({
                            success: function (res) {
                                    var latitude = res.latitude; // 纬度，浮点数，范围为90 ~ -90
                                    var longitude = res.longitude; // 经度，浮点数，范围为180 ~ -180。
                                    $.post("/benz/portal/upload_location/",{
                                        "latitude":latitude,
                                        "longitude":longitude
                                        },function(d){
                                        });
                            }
                        });
                    });
                });
            });
        });
});
});
