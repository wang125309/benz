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

def getTaskId(request):
    taskId = 1
    #更新信息入缓存
    if not cache.get("taskInfo1"):
        t = TaskLocation.objects.all()
        for i in t:
            cache.set("taskInfo"+str(i.id),json.dumps({'date':i.date,'lon':i.lon,'lat':i.lat,'total':t.count()}),settings.NEVER_REDIS_TIMEOUT)
    else :
        pass
    #直接从缓存读取场次信息
    r = cache.get("taskInfo1")
    r = json.loads(r)
    minN = 100000000
    taskId = 0
    for i in xrange(1, int(r['total'])+1):
        t = cache.get("taskInfo"+str(i))
        t = json.loads(t)
        m = request.session.get("location")
        m = json.loads(m)
        dis = (float(m['lat']) - float(t['lat']))*(float(m['lat']) - float(t['lat'])) + (float(m['lon']) - float(t['lon'])) * (float(m['lon']) - float(t['lon']))
        if dis < minN:
            now = time.strftime('%Y/%m/%d')
            if t['date'] == str(now):
                minN = dis
                taskId = i
    return taskId

def getCode(func):
    def _getCode(request):
        if not request.session.get("code",False) :
            if request.session.get('location',False):
                pass
            else :
                return HttpResponseRedirect("/benz/portal/login/")
            #获取活动场次
            taskId = getTaskId(request)            
            #FIXME
            #对于这个id就行分配
            utp = UserTaskProject.objects.all().filter(taskid = taskId)
            if len(utp) :
                try:
                    user = UserTaskProject.objects.get(openid=request.session['openid'],taskid=taskId)
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
                    user = UserTaskProject(openid=request.session['openid'],nickname=u.nickname,headimgurl=u.headimgurl,taskid=taskId,fiveCan=0,bigBuy=0,hotPerson=0,driveSuccess=0,spaceRebuild=0,throwMoney=0,option=0,perfectIn=0,littleCource=0,getFirst=0,fiveCanJoined=0,bigBuyJoined=0,hotPersonJoined=0,driveSuccessJoined=0,spaceRebuildJoined=0,throwMoneyJoined=0,optionJoined=0,perfectInJoined=0,littleCourceJoined=0,getFirstJoined=0,giveNum=code,total_score=0,clear=0)
                    user.save()
                    request.session['code'] = code
            else :
                code = 'A1'
                u = User.objects.get(openid=request.session['openid'])
                user = UserTaskProject(openid=request.session['openid'],nickname=u.nickname,headimgurl=u.headimgurl,taskid=taskId,fiveCan=0,bigBuy=0,hotPerson=0,driveSuccess=0,spaceRebuild=0,throwMoney=0,option=0,perfectIn=0,littleCource=0,getFirst=0,fiveCanJoined=0,bigBuyJoined=0,hotPersonJoined=0,driveSuccessJoined=0,spaceRebuildJoined=0,throwMoneyJoined=0,optionJoined=0,perfectInJoined=0,littleCourceJoined=0,getFirstJoined=0,giveNum=code,total_score=0,clear=0)
                user.save()
                request.session['code'] = code
            return func(request)
        else:
            return func(request)
    return _getCode
        
def loginNeed(func):
    def _loginNeed(request):
        if not request.session.get("openid",False) :
            return HttpResponseRedirect("/benz/portal/wx_login_portal/")
        else:
            if (not cache.get(request.session['openid'],False)) or (not request.session.get("location",False)) :
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
    if not cache.get(request.session['openid']) and request.session.get('location',False):
        cache.set(request.session['openid'],json.dumps({'username':request.GET['username'],'phone':request.GET['phone']}), settings.NEVER_REDIS_TIMEOUT)
        return JsonResponse({
            "status":"success"
        })
    else:
        return JsonResponse({
            "status":"fail",
            "reason":u"请打开定位"
        })

@need_login
def login(request):
    if cache.get(request.session['openid']) and request.session.get("location",False):
        return HttpResponseRedirect("/benz/portal/portal/")
    else :
        return render(request,"portal/login.html")

@loginNeed
@getCode
def portal(request):
    code = request.session['code']
    type = code[0]
    try:
        u = UserTaskProject.objects.get(openid = request.session['openid'])
    except Exception,e:
        u = ""
    return render(request,"portal/portal.html",{
        "code":request.session['code'],
        "type":type,
        "user":u
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
    u = UserTaskProject.objects.get(openid=request.session['openid'],taskid=getTaskId(request))
    return render(request,"portal/mapMode.html",{
        "code":code,
        "type":type,
        "u":u
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
    taskid = getTaskId(request)
    
    pid = cache.get("problemId"+str(taskid))
    while True:
        if pid != cache.get("problemId"+str(taskid)):
            return JsonResponse({
                "status":"success",
                "problemId":cache.get("problemId"+str(taskid))
            })
        else :
            time.sleep(2)

def answer(request):
    taskid = getTaskId(request)
    problemId = cache.get("problemId"+str(taskid))
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
        if not request.session.get('problemScored',False):
            request.session['problemScored'] = '1'
            u = UserTaskProject.objects.get(openid=request.session['openid'])
            u.getFirst = 3
            u.total_score += 2
            u.getFirstJoined = 1
            u.save() 
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
    taskid = getTaskId(request)
    problemId = cache.get("problemId"+str(taskid))
    u = UserTaskProject.objects.get(openid=request.session['openid'])
    if not u.getFirstJoined:

        u.total_score += 1
        u.getFirst = 1
    u.save()
    return render(request,"portal/problem.html",{
        "code":request.session['code'],
        "type":type,
        "problemId":problemId
    })

@loginNeed
@getCode
def scoreRank(request):
    code = request.session['code']
    type = code[0]
    try:
        u = UserTaskProject.objects.get(openid=request.session.get("openid"))
        user = UserTaskProject.objects.all().filter(taskid=u.taskid).order_by("-total_score")
        cnt = 0
        rank = 0
        for i in user:
            cnt += 1
            if i.openid == request.session.get('openid'):
                rank = cnt
        score = u.total_score
    except Exception,e :
        print e
        score = 0
        rank = 0
    return render(request,"portal/scoreRank.html",{
        "code":request.session['code'],
        "type":type,
        "score":score,
        "rank":rank
    })
    

def upload_location(request):
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    if not request.session.get('location',False):
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        request.session['location'] = json.dumps({'lon':longitude,'lat':latitude})
        return JsonResponse({
            "status":"success",
            "reason":u"获取地址信息成功"
        })
    else:
        return JsonResponse({
            "status":"success",
            "reason":u"当前地址在"+request.session['location']
        })

@loginNeed
@getCode
def addScore(request):
    q = request.GET['taskname']
    u = UserTaskProject.objects.get(openid=request.session['openid'])
    if q == 'littleCource':
        if not u.littleCourceJoined :
            u.littleCourceJoined = 1
            u.total_score += 1
            u.littleCource = 1
        u.littleCourceJoined = 1
    elif q == 'bigBuy':
        u.bigBuyJoined = 1
    elif q == 'spaceRebuild':
        if not u.spaceRebuildJoined :
            u.spaceRebuildJoined = 1
            u.total_score += 1
            u.spaceRebuild = 1
        u.spaceRebuildJoined = 1
    elif q == 'hotPerson':
        if not u.hotPersonJoined :
            u.hotPerson = 2
            u.total_score += 2
            u.hotPersonJoined = 1
        u.hotPersonJoined = 1
    elif q == 'driveSuccess':
        u.driveSuccessJoined = 1
    elif q == 'fiveCan':
        if not u.fiveCanJoined:
            u.fiveCanJoined = 1
            u.total_score += 5
            u.fiveCan = 5
        u.fiveCanJoined = 1
    elif q == 'option':
        if not u.optionJoined:
            u.optionJoined = 1
            u.total_score += 1
            u.option = 1
        u.optionJoined = 1
    elif q == 'throwMoney':
        u.throwMoneyJoined = 1
    elif q == 'perfectIn':
        if not u.perfectIn:
            u.perfectInJoined = 1
            u.total_score += 1
            u.perfectIn = 1
        u.perfectInJoined = 1
    u.save()
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
    taskid = getTaskId(request)
    u = UserTaskProject.objects.get(openid=request.session['openid'],taskid=taskid)
    if q == 'littleCource':
        needScan = True
        joined = u.littleCourceJoined
        
    elif q == 'bigBuy':
        needScan = False
        joined = u.bigBuyJoined
    elif q == 'fiveCan':
        joined = u.fiveCanJoined
        needScan = True
    elif q == 'hotPerson':
        needScan = True
        joined = u.hotPersonJoined
    elif q == 'driveSuccess':
        needScan = True
        joined = u.driveSuccessJoined
    elif q == 'spaceRebuild':
        needScan = True
        joined = u.spaceRebuildJoined
    elif q == 'throwMoney':
        needScan = False
        joined = u.throwMoneyJoined
    elif q == 'option':
        needScan = True
        joined = u.optionJoined
    elif q == 'perfectIn':
        needScan = True
        joined = u.perfectInJoined
    elif q == 'getFirst':
        needScan = True
        joined = u.getFirstJoined
    u.save() 
    return render(request,"portal/result.html",{
        "code":request.session['code'],
        "type":type,
        "taskname":taskname,
        "needScan":needScan,
        "joined":joined
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

