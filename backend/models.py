from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=127,unique=True)
    password = models.CharField(max_length=127)
    pri = models.CharField(max_length=127)
    taskid = models.CharField(max_length=127)

class Task(models.Model):
    taskname = models.CharField(max_length=127,unique=True)
    taskdate = models.CharField(max_length=127)
    taskcity = models.CharField(max_length=127)
    dateline = models.CharField(max_length=127)

class UserTask(models.Model):
    user_id = models.CharField(max_length=127)
    task_id = models.CharField(max_length=127)
    dateline = models.CharField(max_length=127)

class Problem(models.Model):
    problem = models.CharField(max_length=127)
    A = models.CharField(max_length=127)
    B = models.CharField(max_length=127)
    C = models.CharField(max_length=127)
    D = models.CharField(max_length=127)
    answer = models.CharField(max_length = 127)
    
