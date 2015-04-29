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
    try:
        if term == 'five-can':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, fiveCanJoined=1).all()
        if term == 'driver-success':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, driveSuccessJoined=1).all()
        if term == 'throw-money':
            userListObjects = UserTaskProject.objects.all().filter(taskid=task_id, throwMoneyJoined=1).all()
        for userListObject in userListObjects:
            userList.append({
                'id': userListObject.openid,
                'name': '',
                'score': userListObject.getFirst,
                'nickname': userListObject.nickname,
            })
    except Exception as e:
        print str(e)
    return render(request, "spot/taskTerm.html", {'userList': userList, 'term': term})


@loginNeed
def addUser(request):
    status = {
        'success': False
    }
    #{username: username, userno: userno, term: term}
    username = request.POST.get('username')
    term = request.POST.get('term')
    userno = request.POST.get('userno')
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
        term = request.POST.get('term')
        print user_id, score, term
        user = UserTaskProject.objects.filter(openid=user_id).first()
        if term == 'get-first':
            user.getFirst = int(score)
        user.save()
        status['success'] = True
    except Exception as e:
        print str(e)
    return JsonResponse(status)


@loginNeed
def addUser(request):
    return

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
