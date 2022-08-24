from django.db import models

# Create your models here.
class Group(models.Model):
    ID = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=20, unique=True)
    ownerID = models.IntegerField()
    createTime = models.DateTimeField()


class UserGroup(models.Model):
    userID = models.IntegerField()
    groupID = models.IntegerField()
    position = models.IntegerField() #0~拥有者；1~管理员；2~成员
