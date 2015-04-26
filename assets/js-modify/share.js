$(function(){
    $.post("/portal/wxconfig/",{
		"url":location.href
	},
	function(data){
		wx.config(data);

        $.get("/nabob/openid/",function(openid){
            $.get("/nabob/bonus_or_not/",function(d){
                link = "http://www.360youtu.com/nabob/index/";
                if(d.status == 'true') {
                    link += ("?openid="+openid.openid);
                }
		        wx.ready(function(){
                    wx.hideOptionMenu();
                });
            });
        });
		wx.error(function(res){
			$.get("/nabob/update_access_token/",function(data){
				$.post("/wxconfig/",{
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


});
