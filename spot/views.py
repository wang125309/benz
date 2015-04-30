# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
import json
import requests
import logging
from backend.models import *
from portal.models import *
import datetime
from functools import wraps
from django.core.cache import cache
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)

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
        u = User.objects.get(username=user)
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
    if request.session.get('spot_user',False):
        return HttpResponseRedirect("/benz/spot/chooseList/")
    else:
        return render(request,"spot/login.html")

@loginNeed
def chooseList(request):
    t = Task.objects.all()
    return render(request,"spot/chooseList.html",{
        "taskList":t
    })

@loginNeed
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
      'driver-success': 'driverSuccess',
      'throw-money': 'throwMoney'
    }
    if term in term_dict.keys():
     try:
        if term == 'five-can':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, fiveCanJoined=1).all()
        if term == 'driver-success':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, driveSuccessJoined=1).all()
        if term == 'throw-money':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, throwMoneyJoined=1).all()
        for userListObject in userListObjects:
            user_info ={
                'id': getattr(userListObject, 'id') or '',
                'score': getattr(userListObject, term_dict[term]) or 0,
                'nickname': userListObject.nickname,
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
def addUser(request):
    status = {
        'success': False
    }
    #{username: username, userno: userno, term: term}
    username = request.POST.get('username')
    taskid = request.POST.get('taskid')
    term = request.POST.get('term')
    if username and taskid and term:
       try:
         if term == 'five-can':
             new_user = UserTaskProject(nickname=username, taskid=taskid, fiveCanJoined=1)
         new_user.save()
         status['success'] = True
       except Exception as e:
         print str(e)
    return JsonResponse(status)

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
        if term in ['five-can', 'driver-success', 'throw-money']:
            user = UserTaskProject.objects.filter(openid=user_id).first()
            if term == 'five-can':
                user.fiveCan = score
            if term == 'driver-success':
                user.driverSuccess = score
            if term == 'throw-Money':
                user.throwMoney = score
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
