from django.db import models

# Create your models here.

class User(models.Model):
    openid = models.CharField(max_length=127)
    nickname = models.CharField(max_length=127,null=True)
    headimgurl = models.CharField(max_length=255,null=True)
    code = models.CharField(max_length=127)
    phone = models.CharField(max_length=127,null=True)
    times = models.IntegerField(null=True)
    dateline = models.CharField(max_length=64)
    total_height = models.IntegerField()
class Wx(models.Model):
    access_token = models.CharField(max_length=127)
    js_ticket = models.CharField(max_length=127)

class UserTaskProject(models.Model):
    openid = models.CharField(max_length=127, null=True)
    nickname = models.CharField(max_length=127, null=True)
    headimgurl = models.CharField(max_length=255, null=True)
    taskid = models.CharField(max_length=127)
    fiveCan = models.IntegerField(null=True)
    bigBuy = models.IntegerField(null=True)
    hotPerson = models.IntegerField(null=True)
    driveSuccess = models.IntegerField(null=True)
    spaceRebuild = models.IntegerField(null=True)
    throwMoney = models.IntegerField(null=True)
    option = models.IntegerField(null=True)
    perfectIn = models.IntegerField(null=True)
    littleCource = models.IntegerField(null=True)
    getFirst = models.IntegerField(null=True)
    fiveCanJoined = models.IntegerField(null=True)
    bigBuyJoined = models.IntegerField(null=True)
    hotPersonJoined = models.IntegerField(null=True)
    driveSuccessJoined = models.IntegerField(null=True)
    spaceRebuildJoined = models.IntegerField(null=True)
    throwMoneyJoined = models.IntegerField(null=True)
    optionJoined = models.IntegerField(null=True)
    perfectInJoined = models.IntegerField(null=True)
    littleCourceJoined = models.IntegerField(null=True)
    getFirstJoined = models.IntegerField(null=True)
    giveNum = models.CharField(max_length=127, null=True)
    total_score = models.IntegerField(null=True)
