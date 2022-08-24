import json

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from group.models import *
from user.models import *
from message.models import *
from project.models import *


@csrf_exempt
def checkMessages(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        titles = []
        types = []
        times = []
        isRead = []
        senders = []
        IDs = []
        for i in Message.objects.filter(userID=user.ID).order_by('-time'):
            titles.append(i.title)
            types.append(i.type)
            times.append(i.time.strftime('%Y-%m-%d %H:%M:%S'))
            isRead.append(i.isRead)
            senders.append(i.sender)
            IDs.append(i.ID)
        result = {'result': 0, 'message': '查看成功!',
                  'titles': titles,
                  'types': types,
                  'times': times,
                  'isRead': isRead,
                  'senders': senders,
                  'IDs': IDs}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '前端裂开了!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkMessageContent(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ID = request.POST.get('ID')
        user = User.objects.get(email=email)
        message = Message.objects.get(ID=ID, userID=user.ID)
        message.isRead = 1
        content = message.content
        sender = message.sender
        title = message.title
        type = message.type
        message.save()
        result = {'result': 0, 'message': '查看成功!',
                  'content': content,
                  'sender': sender,
                  'title': title,
                  'type': type
                  }
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '前端裂开了!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def deleteMessage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ID = request.POST.get('ID')
        user = User.objects.get(email=email)
        time = request.POST.get('time')
        for i in Message.objects.filter(userID=user.ID, ID=ID):
            if i.time.strftime('%Y-%m-%d %H:%M:%S') == time:
                i.delete()
        result = {'result': 0, 'message': '删除成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '前端裂开了!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def deleteMessages(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        Message.objects.filter(userID=user.ID).delete()
        result = {'result': 0, 'message': '删除成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '前端裂开了!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def joinTeam(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        user = User.objects.get(email=email)
        if not Group.objects.filter(groupName=groupName).exists():
            result = {'result': 2, 'message': '改团队已解散'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        group = Group.objects.get(groupName=groupName)
        if UserGroup.objects.filter(userID=user.ID, groupID=group.ID).exists():
            result = {'result': 3, 'message': '您已在此团队中!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        userGroup = UserGroup(userID=user.ID, groupID=group.ID, position=2)
        userGroup.save()
        result = {'result': 0, 'message': '成员添加成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '前端裂开了!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
