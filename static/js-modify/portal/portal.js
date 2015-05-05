require("../../../bower_components/zepto/zepto.js");
require("../../../bower_components/zeptojs/src/touch.js");
require("../../../bower_components/velocity/velocity.min.js");
require("./wx_plugin.js");
window.onload = function() {
    document.addEventListener('touchmove', function (event) {
            event.preventDefault();
            }, false);
    $(".bottom-banner-view").velocity("fadeIn",function(){
            setTimeout(function(){
                $(".bottom-banner-view").velocity("fadeOut",function(){
                    $(".bottom-banner-view-text").velocity("fadeIn");
                    });        
                },2000);
            });
    w = $(window).width();
    h = $(window).height();
    p = location.href.substring(location.href.indexOf("#")+1);
    active = 1;
    if(p == 'instruction') {
            $(".page2").css({
                "top":"0"
                });
            $(".page1").css({
                "top":"-"+h+"px"
                });
            $(".page3").css({
                "top":h+"px"
                });
            $(".page4").css({
                "top":2*h+"px"
                });
            active = 2;
            $(".title").velocity("fadeIn");
    
    }
    if(p == 'menu') {
                $(".page4").css({
                        "top":"0"
                        });
                $(".page3").css({
                        "top":"-"+h+"px"
                        });
                $(".page2").css({
                        "top":"-"+2*h+"px"
                        });
                $(".page1").css({
                        "top":"-"+3*h+"px"
                        });
                $(".left-menu").css({
                        "width":"20vw",
                        "height":"20vw",
                        });
                $(".title-background").css({
                        "background-size":"100%"
                        },1000);
                $(".right-number").css({
                        "width":"20vw",
                        "height":"20vw"
                        });
                active = 4;
    
            $(".title").velocity("fadeIn");
    }

    $(".move").on("swipeUp",function(e){
            if(active == 1) {
            $(".page2").velocity({
                "top":"0"
                },400);
            $(".page1").velocity({
                "top":"-"+h+"px"
                },400);
            $(".page3").velocity({
                "top":h+"px"
                },400);
            $(".page4").velocity({
                "top":2*h+"px"
                },400);
            active = 2;
            $(".title").velocity("fadeIn");
            }
            else if(active == 2) {
            $(".page4").velocity({
                "top":h+"px"
                },400);
            $(".page3").velocity({
                    "top":"0"
                    },400);
            $(".page2").velocity({
                    "top":"-"+h+"px"
                    },400);
            $(".page1").velocity({
                    "top":"-"+2*h+"px"
                    },400);
            setTimeout(function(){
                    $(".bottom-banner").velocity("fadeIn");
                    },1500);

            active = 3;
            }
            else if(active == 3) {
                $(".page4").velocity({
                        "top":"0"
                        },400);
                $(".page3").velocity({
                        "top":"-"+h+"px"
                        },400);
                $(".page2").velocity({
                        "top":"-"+2*h+"px"
                        },400);
                $(".page1").velocity({
                        "top":"-"+3*h+"px"
                        },400);
                $(".left-menu").css({
                        "width":"20vw",
                        "height":"20vw",
                        });
                $(".title-background").velocity({
                        "background-size":"100%"
                        },1000);
                $(".right-number").css({
                        "width":"20vw",
                        "height":"20vw"
                        });
                active = 4;
            }
    });
    $(".move").on("swipeDown",function(e){
            if(active == 2) {
            $(".page1").velocity({
                "top":"0"
                },400);
            $(".page2").velocity({
                "top":h+"px"
                },400);
            $(".page3").velocity({
                "top":h*2+"px"
                },400);
            $(".page4").velocity({
                "top":h*3+"px"
                },400);
            active = 1;
            $(".title").velocity("fadeOut");
            }
            else if(active == 3) {
            $(".page2").velocity({
                "top":"0"
                },400);
            $(".page3").velocity({
                    "top":h+"px"
                    },400);
            $(".page1").velocity({
                    "top":"-"+h+"px"
                    },400);
            $(".page4").velocity({
                    "top":2*h+"px"
                    },400);
            active = 2;
            }
            else if(active == 4) {
                $(".page3").velocity({
                        "top":"0"
                        },400);
                $(".page2").velocity({
                        "top":"-"+h+"px"
                        },400);
                $(".page1").velocity({
                        "top":"-"+2*h+"px"
                        },400);
                $(".page4").velocity({
                        "top":h+"px"
                        },400);

                $(".left-menu").css({
                        "width":"0",
                        "height":"0",
                        });
                $(".title-background").velocity({
                        "background-size":"150%"
                        },1000);
                $(".right-number").css({
                        "width":"0",
                        "height":"0"
                        });
                active = 3;
            }
    });

    $(".little-cource").on("click",function(){
            location.href = "/benz/portal/littleCource/";
            });
    $(".space-rebuild").on("click",function(){
            location.href = "/benz/portal/spaceRebuild/";
            });
    $(".get-first").on("click",function(){
            location.href = "/benz/portal/getFirst/";
            });
    $(".five-can").on("click",function(){
            location.href = "/benz/portal/fiveCan/";
            });
    $(".option").on("click",function(){
            location.href = "/benz/portal/option/";
            });
    $(".perfect-in").on("click",function(){
            location.href = "/benz/portal/perfectIn/";
            });
    $(".drive-success").on("click",function(){
            location.href = "/benz/portal/driveSuccess/";
            });
    $(".big-buy").on("click",function(){
            location.href = "/benz/portal/bigBuy/";
            });
    $(".hot-person").on("click",function(){
            location.href = "/benz/portal/hotPerson/";
            });
    $(".throw-money").on("click",function(){
            location.href = "/benz/portal/throwMoney/";
            });
    $(".know-more").on("click",function(){
            location.href = "/benz/portal/knowMore/";
            });
    $(".tab-map").on("click",function(){
            location.href = "/benz/portal/mapMode/";
            });
    $(".score-rank").on("click",function(){
            location.href = "/benz/portal/scoreRank/";
            });
}

