from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    pri = models.CharField(max_length=255)

class Task(models.Model):
    taskname = models.CharField(max_length=255,unique=True)
    taskdate = models.CharField(max_length=255)
    taskcity = models.CharField(max_length=255)
    dateline = models.CharField(max_length=255)

class UserTask(models.Model):
    user_id = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    dateline = models.CharField(max_length=255)

