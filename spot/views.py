# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
import json
import requests
import logging
from backend.models import *
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
    return render(request,"spot/chooseTask.html")

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
