# coding:utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
import json
import requests
from django.conf import settings
from django.core.cache import cache

import logging
from models import *
from portal.models import User as portalUser
from portal.models import UserTaskProject as usertaskProject
import datetime
import sys
import time
reload(sys)
sys.setdefaultencoding('UTF-8')

# Create your views here.

logger = logging.getLogger(__name__)

def allowPri(func):
    def _allowPri(request):
        if request.session.get("username",False) and not request.session.get("allow") :
            if request.session.get("username") == 'root':
                request.session["allow"] = 'all'
            else:
                u = User.objects.get(username=request.session.get("username"))
                request.session['allow'] = int(u.taskid)
            return func(request)
        else:
            return func(request)
    return _allowPri

def login(request):
    if request.session.get("username",False):
        return HttpResponseRedirect("/benz/backend/userList/")
    return render(request,"backend/login.html")

def createSession(request,user):
    if not request.session.get("username",False):
        request.session['username'] = user
    else:
        return False
    return True

def loginNeed(func):
    def _loginNeed(request):
        if not request.session.get("username",False):
            return HttpResponseRedirect("/benz/backend/login/")
        else:
            return func(request)
    return _loginNeed

@loginNeed
def quitAction(request):
    if not request.session.get("username",False):
        return JsonResponse({
            "status":"fail"
        })
    else:
        request.session['username'] = ""
        request.session['allow'] = ''
        return JsonResponse({
            "status":"success"
        })


@loginNeed
def getUserMessage(request):
    id = request.GET['id']
    try:
        user = User.objects.get(id = id)
        pri = user.pri
        if user.taskid :
            t = Task.objects.get(id=user.taskid)
            return JsonResponse({
                "status":"success",
                "data": {
                    "username":user.username,
                    "password":user.password,
                    "pri":user.pri,
                    "taskid":str(t.id)+"、"+t.taskname
                }
            })
        else :
            return JsonResponse({
                "status":"success",
                "data": {
                    "username":user.username,
                    "password":user.password,
                    "pri":user.pri
                }
            })
    except Exception,e:
        print e
        return JsonResponse({
            "status":"no such user"
        })

@loginNeed
def getTaskMessage(request):
    id = request.GET['id']
    try:
        task = Task.objects.get(id = id)
        return JsonResponse({
            "status":"success",
            "data": {
                "taskname":task.taskname,
                "taskcity":task.taskcity,
                "taskdate":task.taskdate
            }
        })
    except Exception,e:
        return JsonResponse({
            "status":"no such task"
        })

def loginAction(request):
    user = request.GET['username']
    password = request.GET['password']
    try:
        u = User.objects.get(username=user)
        if(u.password == password):
            createSession(request,user)
        else :
            return JsonResponse({
                "status":"wrong password"
            })
        return JsonResponse({
            "status":"success"
        })
    except Exception,e:
        return JsonResponse({
            "status":"no such user"
        })

@loginNeed
def problem(request):
    if request.GET.get("taskid",False):
        taskid = request.GET['taskid']
        if not cache.get("problemId"+taskid):
            cache.set("problemId"+taskid,1,settings.NEVER_REDIS_TIMEOUT)
        problemId = cache.get("problemId"+taskid)
        p = Problem.objects.get(id=problemId)
        imgid = int(problemId)%10+1
        return render(request,"backend/problem.html",{
            "id":problemId,
            "taskid":taskid,
            "problem":p.problem,
            "A":p.A,
            "B":p.B,
            "C":p.C,
            "D":p.D,
            "imgid":imgid
        })
    else :
        return HttpResponseRedirect("/benz/backend/userList/")

@loginNeed
@allowPri
def userList(request):
    u = User.objects.all()
    res = []
    for i in u:
        if i.taskid :
            t = Task.objects.get(id=i.taskid)
            a = {"id":i.id,"username":i.username,"pri":i.pri,"task":t.taskname}
        else :
            a = {"id":i.id,"username":i.username,"pri":i.pri}
        res.append(a)
    u = User.objects.get(username = request.session['username'])
    t = Task.objects.all()
    task = []
    for i in t:
        a = {"id":i.id,"taskname":i.taskname}
        task.append(a)
    return render(request,"backend/userList.html",{
        "user":res,
        "userPri":u.pri,
        "allow":request.session['allow'],
        "task":task
    })

@loginNeed
def deleteUser(request):
    if request.GET.get("id",False):
        if request.GET['id'] != 0:
            u = User.objects.get(id = request.GET['id'])
            if u.username == request.session['username']:
                return JsonResponse({
                    "status":"fail",
                    "reason":"您不能删除自己"
                })
            else :
                me = User.objects.get(username = request.session['username'])
                if me.pri == '2':
                    u.delete()
                    return JsonResponse({
                        "status":"success"
                    })
                else :
                    return JsonResponse({
                        "status":"fail",
                        "reason":"您不是管理员不能进行此操作"
                    })
        else:
            return JsonResponse({
                "status":"fail",
                "reason":"求别闹"
            })
    else:
        return JsonResponse({
            "status":"fail",
            "reason":"用户id不能为0"
        })
    
@loginNeed
def deleteTask(request):
    if request.GET.get("id",False):
        if request.GET['id'] != 0:
            try:
                t = Task.objects.get(id = request.GET['id'])
                t.delete()
                return JsonResponse({
                    "status":"success"
                })
            except Exception,e:
                return JsonResponse({
                    "status":"fail",
                    "reason":"没有这个活动或数据库出现异常"
                })
        else:
            return JsonResponse({
                "status":"fail",
                "reason":"id 不能为0"
            })
    else:
        return JsonResponse({
            "status":"fail",
            "reason":"活动id不能为0"
        })

def getProblemId(request):
    taskid = request.GET['taskid']
    
    if cache.get("problemId"+taskid) and int(cache.get("problemId"+taskid)) < 44:
        return JsonResponse({
            "status":"success",
            "problemId":cache.get("problemId"+taskid)
        })
    else :
        cache.set("problemId"+taskid,1,settings.NEVER_REDIS_TIMEOUT)
        return JsonResponse({
            "status":"success",
            "problemId":1
        })

@loginNeed
def setProblemId(request):
    taskid = request.GET['taskid']
    if not cache.get("problemId"+taskid):
        cache.set("problemId"+taskid,1,settings.NEVER_REDIS_TIMEOUT)
    else :
        if int(cache.get("problemId"+taskid)) < 43:
            cache.set("problemId"+taskid,cache.get("problemId"+taskid)+1,settings.NEVER_REDIS_TIMEOUT)
        else :
            cache.set("problemId"+taskid,1,settings.NEVER_REDIS_TIMEOUT)
    return JsonResponse({
        "status":"success",
    })

@loginNeed
def userSource(request):
    u = User.objects.all()
    res = []
    for i in u:
        a = {"id":i.id,"username":i.username,"pri":i.pri}
        res.append(a)
    return JsonResponse({
        "user":res,

    })

@loginNeed
@allowPri
def saveUser(request):
    if request.GET.get("id",False) and request.GET['id'] != '0':
        username = request.POST['username']
        password = request.POST['password']
        pri = request.POST['pri']
        task = request.POST['taskid']
        if username and password and pri:
            u = User.objects.get(id = request.GET['id'])
            u.username = username
            u.password = password
            u.pri = pri
            u.taskid = task.split("、")[0]
            u.save()
            return JsonResponse({
                "status":"success"
            })
        else :
            return JsonResponse({
                "status":"fail",
                "reason":u"请填写正确信息"
            })
    else:
        try:
            u = User(username=request.POST['username'],password=request.POST['password'],pri=request.POST['pri'])
            if request.POST.get("username",False) and request.POST.get("password",False) and request.POST.get("pri",False) and request.POST['username'] and request.POST['password'] and request.POST['pri']:
                u.save()
                return JsonResponse({
                    "status":"success"
                })
            else :
                return JsonResponse({
                    "status":"fail",
                    "reason":u"请填写正确信息"
                })
        except Exception,e:
            print e
            return JsonResponse({
                "status":"fail",
                "reason":u"请填写正确信息，不要填写重复信息"
            })

@loginNeed
@allowPri
def taskList(request):
    taskList = Task.objects.all()
    me = User.objects.get(username = request.session['username'])
    userPri = me.pri
    return render(request,"backend/taskList.html",{
        "taskList":taskList,
        "userPri":userPri,
        "allow":request.session['allow']
    })

@loginNeed
def sign(request):
    users = usertaskProject.objects.all().filter(taskid=request.GET['id'],clear=0).order_by("-id").exclude(clear=1)[0:20].reverse()
    rank_lists = []
    def get_rank_list(rank_user_list):
        rank_list = []
        for key, item in enumerate(rank_user_list):
            rank = {'color': 'red'}
            if (key)%3==1:
                rank['color'] = 'green'
            elif (key)%3==2:
                rank['color'] = 'gray'
            rank['nickname'] = getattr(item, 'nickname') 
            rank['rank'] = key + 1
            rank['total_score'] = getattr(item, 'total_score') or 0
            rank_list.append(rank)
        return rank_list
    try:
        rank_users = usertaskProject.objects.all().filter(taskid=request.GET['id']).order_by("-total_score").exclude(clear=1)[0:60]
        rank_first = get_rank_list(rank_users[:30])
        if rank_first:
            rank_lists.append(rank_first)
        rank_second = get_rank_list(rank_users[30:])
        for i in xrange(len(rank_second)):
            rank_second[i]['rank'] += 30
        if rank_second:
            rank_lists.append(rank_second)
    except Exception as e:
        print str(e)
    return render(request,"backend/sign.html",{
        "user": users,
        "rankLists": rank_lists
    })


@loginNeed
def sign_rank(request):
    users = usertaskProject.objects.all().filter(taskid=request.GET['id'],clear=0).order_by("-id")[0:10].reverse()
    rank_lists = []
    def get_rank_list(rank_user_list):
        rank_list = []
        for key, item in enumerate(rank_user_list):
            rank = {'color': 'red'}
            if key%3==1:
                rank['color'] = 'green'
            elif key%3==2:
                rank['color'] = 'gray'
            rank['nickname'] = getattr(item, 'nickname')
            rank['rank'] = key + 1
            rank['total_score'] = getattr(item, 'total_score', 0)
            rank_list.append(rank)
        return rank_list

    try:
        rank_users = usertaskProject.objects.all().filter(taskid=request.GET['id'],clear=0).order_by("total_score")[0:40]
        rank_first = get_rank_list(rank_users[:20])
        if rank_first:
            rank_lists.append(rank_first)
        rank_second = get_rank_list(rank_users[20:])
        if rank_second:
            rank_lists.append(rank_second)
    except Exception as e:
        print str(e)
    return JsonResponse({
        "user": users,
        "rankLists": rank_lists
    })

def getSignWall(request):
    user = usertaskProject.objects.all().filter(taskid=request.GET['id'],clear=0).exclude(register=1).order_by("-id")[0:20]
    userall = usertaskProject.objects.all().filter(taskid=request.GET['id'],clear=0)
    users = []
    cnt = 0
    for i in user:
        cnt += 1
        a = {}
        a['nickname'] = i.nickname
        a['headimgurl'] = i.headimgurl
        a['id'] = cnt
        users.append(a)
    return JsonResponse({
        "user": users,
    })

@loginNeed
def clear(request):
    taskId = request.GET.get("id")
    u = usertaskProject.objects.all().filter(taskid = taskId)
    for i in u:
        i.clear = 1
        i.save()
    return JsonResponse({
        "status":"success"
    })

@loginNeed
def signMessage(request):
    users = portalUser.objects.all()
    u = []
    for i in users:
        u.append({"nickname":i.nickname,"headimgurl":i.headimgurl})
    return JsonResponse({
        "user":u    
    })

@loginNeed
def saveTask(request):
    taskname = request.POST['taskname']
    taskcity = request.POST['taskcity']
    taskdate = request.POST['taskdate']
    if request.GET['id'] != '0':
        t = Task.objects.get(id = request.GET['id'])
        if taskname and taskcity and taskdate:
            t.taskname = taskname
            t.taskcity = taskcity
            t.taskdate = taskdate
            t.save()
            return JsonResponse({
                "status":"success"
            })
        else :
            return JsonResponse({
                "status":"fail",
                "reason":u"请保证正确输入活动名称，日期及活动城市"
            })
    else:
        if taskname and taskcity and taskdate:
            try:
                t = Task.objects.get(taskname = taskname)
                return JsonResponse({
                    "status":"fail",
                    "reason":u"活动已经存在"
                })
            except Exception,e:
                t = Task(taskname=taskname,taskcity=taskcity,taskdate=taskdate,dateline=time.time())
                t.save()
                return JsonResponse({
                    "status":"success",
                })
        else :
            return JsonResponse({
                "status":"fail",
                "reason":"请输入正确的活动名称，日期和城市"
            })
