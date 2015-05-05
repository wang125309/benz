# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
import json
import requests
import logging
from backend.models import User as SpotUser
from backend.models import Task
from portal.models import *
import datetime
from functools import wraps
from django.core.cache import cache
import sys
import math
from django.db.models import Q
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)

def allowPri(func):
    def _allowPri(request):
        if request.session.get("spot_user",False) and not request.session.get("spot_allow") :
            if request.session.get("spot_user") == 'root':
                request.session["spot_allow"] = 'all'
            else:
                u = SpotUser.objects.get(username=request.session.get("spot_user"))
                request.session['spot_allow'] = int(u.taskid)
            return func(request)
        else:
            return func(request)
    return _allowPri

def loginNeed(func):
    def _loginNeed(request):
        if not request.session.get("spot_user",False):
            return HttpResponseRedirect("/benz/spot/login/")
        else:
            return func(request)
    return _loginNeed

def quitAction(request):
    if not request.session.get("spot_user",False):
        return JsonResponse({
            "status":"fail"
        })
    else:
        request.session['spot_user'] = ""
        return JsonResponse({
            "status":"success"
        })

def loginAction(request):
    user = request.POST['username']
    password = request.POST['password']
    try:
        u = SpotUser.objects.get(username=user)
        if(u.password == password):
            request.session['spot_user'] = u.username
        else :
            return JsonResponse({
                "status":"fail",
                "reason":u"密码错误"
            })
        return JsonResponse({
            "status":"success"
        })
    except Exception,e:
        return JsonResponse({
            "status":"fail",
            "reason":str(e)
        })

def login(request):
    return render(request,"spot/login.html")

@loginNeed
@allowPri
def chooseList(request):
    t = Task.objects.all()
    return render(request,"spot/chooseList.html",{
        "taskList":t,
        "spot_allow":request.session['spot_allow']
    })

@loginNeed
@allowPri
def chooseTask(request):
    task_id = request.GET.get('task_id')
    return render(request,"spot/chooseTask.html", {
        "task_id": task_id
    })

@loginNeed
def taskTerm(request):
    task_id = request.GET.get('task_id')
    term = request.GET.get('term')
    userList = []
    userListObjects = []
    term_dict = {
      'five-can': 'fiveCan',
      'driver-success': 'driveSuccess',
      'throw-money': 'throwMoney',
      'big-buy' : 'bigBuy',
      'hot-person' : 'hotPerson',
      'perfect-in' : 'perfectIn',
      'space-rebuild' : 'spaceRebuild',
      'little-cource' : 'littleCource',
      'get-first' : 'getFirst',
      'option' : 'option'
    }
    if term in term_dict.keys():
     try:
        if term == 'five-can':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, fiveCanJoined=1)
            userListObjects = []
        if term == 'driver-success':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id,driveSuccessJoined=1)
        if term == 'throw-money':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, throwMoneyJoined=1)
        if term == 'get-first':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, getFirstJoined=1)
            userListObjects = []
        if term == 'little-cource':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, littleCourceJoined=1)
            userListObjects = []
        if term == 'perfect-in':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, perfectInJoined=1)
            userListObjects = []
        if term == 'option':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, optionJoined=1)
            userListObjects = []
        if term == 'big-buy':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, bigBuyJoined=1)
        if term == 'hot-person':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, throwMoneyJoined=1)
        if term == 'space-rebuild':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, throwMoneyJoined=1)
            userListObjects = []
        userListObjects = userListObjects.order_by("giveNum")
        for userListObject in userListObjects:
            if userListObject.register == '1':
                userListObject.giveNum = '*'+userListObject.giveNum
            user_info ={
                'code': getattr(userListObject, 'giveNum') or '',
                'id': getattr(userListObject, 'id') or '',
                'score': getattr(userListObject, term_dict[term]) or 0,
                'nickname': userListObject.nickname,
                'register':userListObject.register
            }
            openid = getattr(userListObject, 'openid')
            print openid, 'openid'
            if openid:
                try:
                    user_json = cache.get(openid)
                    print 'user_json', user_json
                    user_json = json.loads(user_json)
                    user_info['name'] = user_json.get('username') or ''
                except Exception as e:
                    print str(e)
                    pass
            userList.append(user_info)
     except Exception as e:
        print str(e)
    return render(request, "spot/taskTerm.html", {'userList': userList, 'term': term, 'taskid': task_id})

@loginNeed
def addTermList(request):
    term = request.GET.get('term')
    taskid = request.GET.get('taskid')
    ulist = UserTaskProject.objects.filter(taskid=taskid,register=1)
    if term == 'five-can':
        ulist = ulist.filter(fiveCanJoined=0)
    elif term == 'driver-success':
        ulist = ulist.filter(driveSuccessJoined=0)
    elif term == 'throw-money':
        ulist = ulist.filter(throwMoneyJoined=0)
    elif term == 'get-first':
        ulist = ulist.filter(getFirstJoined=0)
    elif term == 'little-cource':
        ulist = ulist.filter(littleCourceJoined=0)
    elif term == 'perfect-in':
        ulist = ulist.filter(perfectInJoined=0)
    elif term == 'option':
        ulist = ulist.filter(optionJoined=0)
    elif term == 'big-buy':
        ulist = ulist.filter(bigBuyJoined=0)
    elif term == 'hot-person':
        ulist = ulist.filter(hotPersonJoined=0)
    elif term == 'space-rebuild':
        ulist = ulist.filter(spaceRebuildJoined=0)
    print ulist
    return render(request, "spot/addTermList.html", {
        'taskid':taskid,
        'term':term,
        'user':ulist
    })

@loginNeed
def addToTerm(request):
    taskid = request.GET.get('taskid')
    term = request.GET.get('term')
    id = request.GET.get('id')
    u = UserTaskProject.objects.get(id=id,register=1,taskid=taskid)
    if term == 'five-can':
        u.fiveCan = 5
        u.total_score += 5
        u.fiveCanJoined = 1 
    elif term == 'driver-success':
        u.driveSuccessJoined = 1 
    elif term == 'throw-money':
        u.throwMoneyJoined = 1 
    elif term == 'get-first':
        u.getFirstJoined = 1 
    elif term == 'little-cource':
        u.littleCource = 1
        u.total_score += 1
        u.littleCourceJoined = 1 
    elif term == 'perfect-in':
        u.perfectIn = 1
        u.total_score += 1
        u.perfectInCanJoined = 1 
    elif term == 'option':
        u.option = 1
        u.total_score += 1
        u.optionJoined = 1 
    elif term == 'big-buy':
        u.bigBuyJoined = 1 
    elif term == 'hot-person':
        u.hotPerson = 2
        u.total_score += 2
        u.hotPersonJoined = 1 
    elif term == 'space-rebuild':
        u.spaceRebuildJoined = 1
        u.spaceRebuild = 1
        u.total_score += 1
    u.save()
    return JsonResponse({
        "status":"success"    
    })

@loginNeed
def addUser(request):
    status = {
        'success': False
    }
    #{username: username, userno: userno, term: term}
    username = request.POST.get('username')
    taskid = request.POST.get('taskid')
    phone = request.POST.get('phone')
    utp = UserTaskProject.objects.all().filter(taskid=taskid)
    if username and taskid :
        try:
            new_user = UserTaskProject(nickname=username,fiveCanJoined=0,driveSuccessJoined=0,throwMoneyJoined=0,getFirstJoined=0,littleCourceJoined=0,perfectInJoined=0,optionJoined=0,bigBuyJoined=0,hotPersonJoined=0,spaceRebuildJoined=0, taskid=taskid, register=1,phone=phone,total_score=0)
            if len(utp):
                cu = utp.count() + 1
            else :
                cu = 1
            if cu%4 == 1:
                code = 'A' + str(int(math.ceil(cu/4.0)))
            elif cu%4 == 2:
                code = 'B' + str(int(math.ceil(cu/4.0)))
            elif cu%4 == 3:
                code = 'C' + str(int(math.ceil(cu/4.0)))
            else:
                code = 'D' + str(int(math.ceil(cu/4.0)))
            new_user.giveNum = code
            new_user.save()
            status['success'] = True
        except Exception as e:
            print str(e)
    return JsonResponse(status)

@loginNeed
def submitScore(request):
    term = request.GET.get("term")
    taskid = request.GET.get("taskid")
    if term == 'little-cource':
        u = UserTaskProject.objects.filter(littleCourceJoined=1,taskid=taskid).exclude(littleCource=0)
    elif term == 'five-can':
        u = UserTaskProject.objects.filter(fiveCanJoined=1,taskid=taskid).exclude(fiveCan=0)
    elif term == 'get-first':
        u = UserTaskProject.objects.filter(getFirstJoined=1,taskid=taskid).exclude(getFirst=0)
    elif term == 'big-buy':
        u = UserTaskProject.objects.filter(bigBuyJoined=1,taskid=taskid).exclude(bigBuy=0)
    elif term == 'hot-person':
        u = UserTaskProject.objects.filter(hotPersonJoined=1,taskid=taskid).exclude(hotPerson=0)
    elif term == 'throw-money':
        u = UserTaskProject.objects.filter(throwMoneyJoined=1,taskid=taskid).exclude(throwMoney=0)
    elif term == 'perfect-in':
        u = UserTaskProject.objects.filter(perfectInJoined=1,taskid=taskid).exclude(perfectIn=0)
    elif term == 'driver-success':
        u = UserTaskProject.objects.filter(driveSuccessJoined=1,taskid=taskid).exclude(driveSuccess=0)
    elif term == 'space-rebuild':
        u = UserTaskProject.objects.filter(spaceRebuildJoined=1,taskid=taskid).exclude(spaceRebuild=0)
    elif term == 'option':
        u = UserTaskProject.objects.filter(optionJoined=1,taskid=taskid).exclude(option=0)
    if term == 'little-cource':
        for i in u:
            i.littleCourceJoined = 2
            i.save()
    elif term == 'five-can':
        for i in u:
            i.fiveCanJoined = 2
            i.save()
    elif term == 'get-first':
        for i in u:
            i.getFirstJoined = 2
            i.save()
    elif term == 'big-buy':
        for i in u:
            i.bigBuyJoined = 2
            i.save()
    elif term == 'hot-person':
        for i in u:
            i.hotPersonJoined = 2
            i.save()
    elif term == 'throw-money':
        for i in u:
            i.throwMoneyJoined = 2
            i.save()
    elif term == 'perfect-in':
        for i in u:
            i.perfectInJoined = 2
            i.save()
    elif term == 'driver-success':
        for i in u:
            i.driveSuccessJoined = 2
            i.save()
    elif term == 'space-rebuild':
        for i in u:
            i.spaceRebuildJoined = 2
            i.save()
    elif term == 'option':
        for i in u:
            i.optionJoined = 2
            i.save()
    return JsonResponse({
        "status":"success"    
    })

@loginNeed
def addScore(request):
    status = {
        'success': False
    }
    #user_id: id, score: score, term: term
    try:
        user_id = request.POST.get('user_id')
        score = request.POST.get('score')
        score = int(score)
        term = request.POST.get('term')
        if term in ['five-can', 'driver-success', 'throw-money', 'big-buy']:
            user = UserTaskProject.objects.filter(id=user_id).first()
            if term == 'driver-success':
                if user.total_score :
                    if user.driveSuccess:
                        user.total_score -= user.driveSuccess
                    user.total_score += score
                else :
                    user.total_score = score
                user.driveSuccess = score
            if term == 'throw-money':
                print user.total_score
                if user.total_score :
                    if user.throwMoney:
                        user.total_score -= user.throwMoney
                    user.total_score += score
                else :
                    user.total_score = score
                user.throwMoney = score
            if term == 'big-buy':
                user.bigBuy = score
                if user.total_score :
                    if user.bigBuy:
                        user.total_score -= user.bigBuy
                    user.total_score += score
                else :
                    user.total_score = score
                user.bigBuy = score
            user.save()
            status['success'] = True
    except Exception as e:
        print str(e)
    return JsonResponse(status)


@loginNeed
def register(request):
    return render(request,"spot/register.html")

@loginNeed
def editScore(request):
    return render(request,"spot/editScore.html")

@loginNeed
def superUserAdd(request):
    return render(request,"/spot/superUserAdd.html")

@loginNeed
def testArea(request):
    return render(request,"spot/testArea.html")
