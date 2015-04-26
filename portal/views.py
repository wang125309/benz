# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from django.conf import settings
import json
import requests
import logging
from models import *
from plugin import *
import datetime
from django.core.cache import cache
from functools import wraps
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)
appid = "wxd4f684d8f3edc620"
secret = "5b361b69fb998e0db1be2d873ed85326"

def loginNeed(func):
    def _loginNeed(request):
        if not request.session.get("phone",False):
            return HttpResponseRedirect("/benz/portal/login/")
        else:
            return func(request)
    return _loginNeed

def need_login(func):
    def _need_login(request):
        if not request.session.get("openid",False):
            if request.GET.get("code",False):
                w = wx_login(appid,secret,request.GET['code'])
                request.session['openid'] = w['openid']
                try:
                    u = User.objects.get(openid=request.session['openid'])
                except Exception,e:
                    u = User(openid = request.session['openid'],headimgurl=w['headimgurl'].encode("utf8"),nickname=w['nickname'].encode('utf8'),dateline=str(time.time()),total_height=0)
                    u.save()
                return func(request)
            else:
                if request.GET.get("openid",False):
                    return HttpResponseRedirect("/benz/login/?openid="+request.GET['openid'])
                return HttpResponseRedirect("/benz/login/") 
        else:
            return func(request)
    return _need_login

def loginAction(request):
    if(request.session.get("phone",False)):
        return HttpResponseRedirect("/benz/portal/portal/")
    else :
        request.session['phone'] = request.GET['phone']
        cache.set(request.session['phone'],request.GET['username'], settings.NEVER_REDIS_TIMEOUT)
        return JsonResponse({
            "status":"success"
        })

def login(request):
    if request.session.get("phone",False):
        return HttpResponseRedirect("/benz/portal/portal/")
    else :
	    return render(request,"portal/login.html")

@loginNeed
def portal(request):
	return render(request,"portal/portal.html")

@loginNeed
def littleCource(request):
	return render(request,"portal/littleCource.html")

@loginNeed
def bigBuy(request):
	return render(request,"portal/bigBuy.html")

@loginNeed
def option(request):
	return render(request,"portal/option.html")

@loginNeed
def hotPerson(request):
	return render(request,"portal/hotPerson.html")

@loginNeed
def spaceRebuild(request):
	return render(request,"portal/spaceRebuild.html")

@loginNeed
def throwMoney(request):
	return render(request,"portal/throwMoney.html")

@loginNeed
def getFirst(request):
	return render(request,"portal/getFirst.html")

@loginNeed
def fiveCan(request):
	return render(request,"portal/fiveCan.html")

@loginNeed
def perfectIn(request):
	return render(request,"portal/perfectIn.html")

@loginNeed
def driveSuccess(request):
	return render(request,"portal/driveSuccess.html")

@loginNeed
def taskList(request):
	return render(request,"portal/taskList.html")

@loginNeed
def mapMode(request):
	return render(request,"portal/mapMode.html")

def wxconfig(request):
	url = request.POST['url']
	js_ticket = Wx.objects.get(id=1).js_ticket
	s = sign(js_ticket,url)
	json = {
		"appId":appid,
		"timestamp":s['timestamp'],
		"nonceStr":'nameLR9969',
		"signature":s['hash'],
		"jsApiList":['onMenuShareAppMessage','onMenuShareTimeline']
	}
	return JsonResponse(json)

def update_access_token(request):
	get_js_ticket(get_access_token(appid,secret),appid,secret)
	return JsonResponse({
		"status":"success"
	})

