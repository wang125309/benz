# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
import json
import requests
import logging
from models import *
import datetime
from functools import wraps
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.
logger = logging.getLogger(__name__)
appid = "wx91e4c1925de9ff50"
secret = "f2f564ea79ff43f7ed3004821ac3b2b8"

def createSession(user):
    if not request.session.get(user,False):
        request.session['spot_user'] = user
    else:
        return False
    return True

def loginNeed(func):
    def _loginNeed(request):
        if not request.session.get("spot_user",False):
            return HttpResponseRedirect("/spot/login/")
        else:
            return func(request)

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
    user = request.GET['spot_user']
    password = request.GET['password']
    try:
        u = User.objects.get(username=user)
        if(u.password == password):
            createSession(user)
        else :
            return JsonResponse({
                "status":"wrong password"
            })
        return JsonResponse({
            "status":"success"
        })
    except Exception,e:
        return JsonResponse({
            "status":"fail"
        })

def login(request):
    return render(request,"spot/login.html")

@loginNeed
def index(request):
    return render(request,"spot/index.html")

@loginNeed
def chooseList(request):
    return render(request,"spot/chooseList.html")

@loginNeed
def chooseTask(request):
    return render(request,"spot/chooseTask.html")

@loginNeed
def register(request):
    return render(request,"spot/register.html")

@loginNeed
def showTaskScore(request):
    return render(request,"spot/showTaskScore.html")

@loginNeed
def superUserAdd(request):
    return render(request,"/spot/superUserAdd.html")

@loginNeed
def testArea(request):
    return render(request,"spot/testArea.html")
