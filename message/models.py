from django.db import models


# Create your models here.
class Message(models.Model):
    ID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    time = models.DateTimeField()
    type = models.IntegerField()
    isRead = models.IntegerField()  # 0~未读，1~已读
    sender = models.CharField(max_length=50)
