from django.db import models


# Create your models here.
class User(models.Model):
    ID = models.IntegerField(primary_key=True)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True)


class EmailCode(models.Model):
    email = models.CharField(max_length=30)
    code = models.CharField(max_length=50)


class UserInfo(models.Model):
    userID = models.IntegerField(primary_key=True)
    selfAvatar = models.IntegerField()  # 0~默认头像；1~自定义头像
    avatar = models.FileField(upload_to='avatars/', default='publicAvatar/public0.jpg')
    description = models.CharField(max_length=150)
    realname = models.CharField(max_length=20)
