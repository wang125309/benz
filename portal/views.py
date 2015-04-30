# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from django.conf import settings
import json
import requests
import logging
from models import *
from backend.models import Task,Problem
from plugin import *
import datetime
from django.core.cache import cache
from functools import wraps
import sys
import re
import math
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)
appid = "wxd4f684d8f3edc620"
secret = "5b361b69fb998e0db1be2d873ed85326"

def getCode(func):
    def _getCode(request):
        if not request.session.get("code",False):
            t = Task.objects.all().filter(taskcity=request.session['location'])
            taskId = 0
            for i in t:
                if i.taskcity is not u'泉州市' :
                    taskId = i.id
            #FIXME
            #对于这个id就行分配
            utp = UserTaskProject.objects.all().filter(taskid = taskId)
            if len(utp) :
                try:
                    user = UserTaskProject.objects.get(openid=request.session['openid'])
                    request.session['code'] = user.giveNum
                except Exception,e:
                    u = User.objects.get(openid=request.session['openid'])
                    cu = utp.count()+1
                    code = ""
                    if cu%4 == 1:
                        code = 'A'+str(int(math.ceil(cu/4.0)))
                    elif cu%4 == 2:
                        code = 'B'+str(int(math.ceil(cu/4.0)))
                    elif cu%4 == 3:
                        code = 'C'+str(int(math.ceil(cu/4.0)))
                    else:
                        code = 'D'+str(int(math.ceil(cu/4.0)))
                    user = UserTaskProject(openid=request.session['openid'],nickname=u.nickname,headimgurl=u.headimgurl,taskid=taskId,fiveCan=0,bigBuy=0,hotPerson=0,driveSuccess=0,spaceRebuild=0,throwMoney=0,option=0,perfectIn=0,littleCource=0,getFirst=0,fiveCanJoined=0,bigBuyJoined=0,hotPersonJoined=0,driveSuccessJoined=0,spaceRebuildJoined=0,throwMoneyJoined=0,optionJoined=0,perfectInJoined=0,littleCourceJoined=0,getFirstJoined=0,giveNum=code)
                    user.save()
                    request.session['code'] = code
            else :
                code = 'A1'
                u = User.objects.get(openid=request.session['openid'])
                user = UserTaskProject(openid=request.session['openid'],nickname=u.nickname,headimgurl=u.headimgurl,taskid=taskId,fiveCan=0,bigBuy=0,hotPerson=0,driveSuccess=0,spaceRebuild=0,throwMoney=0,option=0,perfectIn=0,littleCource=0,getFirst=0,fiveCanJoined=0,bigBuyJoined=0,hotPersonJoined=0,driveSuccessJoined=0,spaceRebuildJoined=0,throwMoneyJoined=0,optionJoined=0,perfectInJoined=0,littleCourceJoined=0,getFirstJoined=0,giveNum=code)
                user.save()
                request.session['code'] = code
            return func(request)
        else:
            return func(request)
    return _getCode
        
def loginNeed(func):
    def _loginNeed(request):
        if not request.session.get("openid",False):
            return HttpResponseRedirect("/benz/portal/wx_login_portal/")
        else:
            if not cache.get(request.session['openid'],False):
                return HttpResponseRedirect("/benz/portal/login/")
            else:
                return func(request)
    return _loginNeed

def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def need_login(func):
    def _need_login(request):
        if not request.session.get("openid",False):
            if request.GET.get("code",False):
                w = wx_login(appid,secret,request.GET['code'])
                request.session['openid'] = w['openid']

                try:
                    u = User.objects.get(openid=request.session['openid'])
                except Exception,e:
                    w['nickname'] = filter_emoji(w['nickname'])
                    u = User(openid = request.session['openid'],headimgurl=w['headimgurl'].encode("utf8"),nickname=w['nickname'].encode('utf8'),dateline=str(time.time()),total_height=0)
                    u.save()
                return func(request)
            else:
                return HttpResponseRedirect("/benz/portal/wx_login_portal/") 
        else:
            return func(request)
    return _need_login

def wx_login_portal(request):
    if request.session.get("openid",False):
        return HttpResponseRedirect("/benz/portal/login/")
    else :
        return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid="+appid+"&redirect_uri=http%3A%2F%2Fbenz.wxpages.com%2Fbenz%2Fportal%2Flogin%2F&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect");    

def loginAction(request):
    if cache.get(request.session['openid']):
        return HttpResponseRedirect("/benz/portal/portal/")
    else :
        cache.set(request.session['openid'],json.dumps({'username':request.GET['username'],'phone':request.GET['phone']}), settings.NEVER_REDIS_TIMEOUT)
        return JsonResponse({
            "status":"success"
        })

@need_login
def login(request):
    if cache.get(request.session['openid']):
        return HttpResponseRedirect("/benz/portal/portal/")
    else :
        return render(request,"portal/login.html")

@loginNeed
@getCode
def portal(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/portal.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def littleCource(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/littleCource.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def bigBuy(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/bigBuy.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def option(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/option.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def hotPerson(request):
    code = request.session['code']
    type = code[0]
    print type
    return render(request,"portal/hotPerson.html",{
        "code":request.session['code'],
        "type":type,
    })

@loginNeed
@getCode
def spaceRebuild(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/spaceRebuild.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def throwMoney(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/throwMoney.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def getFirst(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/getFirst.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def fiveCan(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/fiveCan.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def perfectIn(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/perfectIn.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def driveSuccess(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/driveSuccess.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def taskList(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/taskList.html",{
        "code":request.session['code'],
        "type":type
    })

@loginNeed
@getCode
def mapMode(request):
    code = request.session['code']
    type = code[0]
    return render(request,"portal/mapMode.html",{
        "code":code,
        "type":type
    })

@loginNeed
@getCode
def knowMore(request):
    code = request.session['code']
    type = code[0]

    return render(request,"portal/knowMore.html",{
        "code":code,
        "type":type
    })

@loginNeed
@getCode
def menu(request):
    code = request.session['code']
    type = code[0]

    return render(request,"portal/menu.html",{
        "code":code,
        "type":type
    })

def getProblemId(request):
    pid = cache.get("problemId")
    while True:
        if pid != cache.get("problemId"):
            return JsonResponse({
                "status":"success",
                "problemId":cache.get("problemId")
            })
        else :
            time.sleep(2)

def answer(request):
    problemId = cache.get("problemId")
    p = Problem.objects.get(id=problemId)
    if request.GET['answer'] == 'A':
        if p.answer == 'A':
            return JsonResponse({
                "status":"success",
                "correct":"true"
            })
        else :
            return JsonResponse({
                "status":"success",
                "correct":"false"
            })
    elif request.GET['answer'] == 'B':
        if p.answer == 'B':
            return JsonResponse({
                "status":"success",
                "correct":"true"
            })
        else :
            return JsonResponse({
                "status":"success",
                "correct":"false"
            })
        
    elif request.GET['answer'] == 'C':
        if p.answer == 'C':
            return JsonResponse({
                "status":"success",
                "correct":"true"
            })
        else :
            return JsonResponse({
                "status":"success",
                "correct":"false"
            })
        
    else :
        if p.answer == 'D':
            return JsonResponse({
                "status":"success",
                "correct":"true"
            })
        else :
            return JsonResponse({
                "status":"success",
                "correct":"false"
            })

def right(request):
    if request.session.get('problemRight',False):
        request.session['problemRight'] = int(request.session['problemRight']) + 1
    else :
        request.session['problemRight'] = 1
    if request.session['problemRight'] >= 5:
        if not request.session.get('problemScored'.False):
            request.session['problemScored'] = '1'
            u = UserTaskProject.objcects.get(openid=request.session['openid'])
            u.getFirst = 2
            return JsonResponse({
                "status":"true"    
            })
        else :
            return JsonResponse({
                "status":"fail"
            })
    else:
        return JsonResponse({
            "status":"fail"    
        })

            
@loginNeed
@getCode
def problem(request):
    code = request.session['code']
    type = code[0]
    problemId = cache.get("problemId")
    return render(request,"portal/problem.html",{
        "code":request.session['code'],
        "type":type,
        "problemId":problemId
    })

def upload_position(request):
    if not request.session.get('location',False):
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        r = requests.get("http://api.map.baidu.com/geocoder/v2/?ak=pmCgmADsAsD9rEXkqWNcTzjd&location="+latitude+","+longitude+"&output=json&pois=1")
        r.encoding = "utf8"
        res = r.json()
        request.session['location'] = res['result']['addressComponent']['city'].encode("utf8")
        print request.session['location']
    return JsonResponse({
        "status":"success"    
    })
    
@loginNeed
@getCode
def result(request):
    q = request.GET['task']
    code = request.session['code']
    type = code[0]
    taskname = q
    if q == 'littleCource':
        needScan = True
    
    elif q == 'bigBuy':
        needScan = False
    elif q == 'fiveCan':
        needScan = True
    elif q == 'hotPerson':
        needScan = True
    elif q == 'driveSuccess':
        needScan = True
    elif q == 'spaceRebuild':
        needScan = True
    elif q == 'throwMoney':
        needScan = False
    elif q == 'option':
        needScan = True
    elif q == 'perfectIn':
        needScan = True
    elif q == 'getFirst':
        needScan = True
    return render(request,"portal/result.html",{
        "code":request.session['code'],
        "type":type,
        "taskname":taskname,
        "needScan":needScan
    })


def wxconfig(request):
    url = request.POST['url']
    js_ticket = cache.get('js_ticket')
    print js_ticket
    s = sign(js_ticket,url)
    json = {
        "appId":appid,
        "timestamp":s['timestamp'],
        "nonceStr":'nameLR9969',
        "signature":s['hash'],
        "jsApiList":['onMenuShareAppMessage','onMenuShareTimeline','scanQRCode']
    }
    print json
    return JsonResponse(json)

def update_access_token(request):
    get_js_ticket(get_access_token(appid,secret),appid,secret)
    return JsonResponse({
        "status":"success"
    })

