from django.db import models


# Create your models here.
class Project(models.Model):
    ID = models.AutoField(primary_key=True)
    proName = models.CharField(max_length=20)
    groupID = models.IntegerField()
    isDelete = models.IntegerField()  # 0表示没被删除，1表示被删除
    deleteTime = models.DateTimeField()
    status = models.CharField(max_length=20)  # 0表示未开始，1表示进行中，2表示已完成
    createTime = models.DateTimeField()
    isShare = models.IntegerField()  # 0~未分享；1~已分享
    shareCode = models.CharField(max_length=50)
    UMLContent = models.TextField()


class CheckProject(models.Model):
    projectID = models.IntegerField()
    userID = models.IntegerField()
    checkTime = models.DateTimeField()


class CollectProject(models.Model):
    projectID = models.IntegerField()
    userID = models.IntegerField()


class Prototype(models.Model):
    ID = models.AutoField(primary_key=True)
    protoName = models.CharField(max_length=20)
    projectID = models.IntegerField()
    canvasData = models.TextField()
    canvasStyle = models.TextField()
    canvasHeight = models.IntegerField()
    canvasWidth = models.IntegerField()
    createTime = models.DateTimeField()


class Document(models.Model):
    ID = models.AutoField(primary_key=True)
    docName = models.CharField(max_length=20)
    fatherURL = models.CharField(max_length=100)
    URL = models.CharField(max_length=100)
    content = models.TextField()
    createTime = models.DateTimeField()
