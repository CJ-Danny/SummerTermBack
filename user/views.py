import json

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from group.models import *
from user.models import *
from user.send_email import *
from project.models import *


@csrf_exempt
def register(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        code = request.POST.get('code')

        if User.objects.filter(email=email).exists():
            result = {'result': 2, 'message': '邮箱已注册!'}
        else:
            emialID, edu = email.split('@')
            if not checkCode(code, email):
                result = {'result': 3, 'message': '邮箱验证码错误!'}
                return HttpResponse(json.dumps(result), content_type="application/json")
            all = User.objects.all()
            count = len(all)
            chars = '01234567'
            random = Random()
            i = random.randint(0, 7)
            newUser = User(ID=count, nickname=nickname, password=password, email=email)
            newUser.save()
            newUserInfo = UserInfo(userID=newUser.ID, selfAvatar=0, avatar='publicAvatar/public' + chars[i] + '.jpg')
            newUserInfo.save()
            result = {'result': 0, 'message': '注册成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(email=email).exists():
            result = {'result': 2, 'message': '邮箱不存在!'}
        else:
            user = User.objects.get(email=email)
            if user.password != password:
                result = {'result': 3, 'message': '密码不正确!'}
            else:
                request.session['email'] = email
                userInfo = UserInfo.objects.get(userID=user.ID)
                avatarUrl = userInfo.avatar.url
                result = {'result': 0, 'message': '登录成功!', 'nickname': user.nickname, 'avatarUrl': avatarUrl}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def logout(request):
    request.session.flush()
    result = {'result': 0, 'message': '登出成功!'}
    return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        newPassword = request.POST.get('newPassword')
        if User.objects.filter(email=email).exists():
            if not checkCode(code, email):
                result = {'result': 3, 'message': '邮箱验证码错误!'}
                return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                user = User.objects.get(email=email)
                user.password = newPassword
                user.save()
                result = {'result': 0, 'message': '修改密码成功!'}
                return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            result = {'result': 2, 'message': '邮箱不存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def registerEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            result = {'result': 2, 'message': '邮箱已注册!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        send_result = sendCodeEmail(email)
        if not send_result:
            result = {'result': 3, 'message': '发送失败，请检查邮箱是否正确!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            result = {'result': 0, 'message': '发送成功，请及时查收!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def forgetPasswordEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            result = {'result': 2, 'message': '邮箱未注册!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        send_result = sendPasswordCodeEmail(email)
        if not send_result:
            result = {'result': 3, 'message': '发送失败，请检查邮箱是否正确!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            result = {'result': 0, 'message': '发送成功，请及时查收!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def changeAvatar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')
        user = User.objects.get(email=email)
        userInfo = UserInfo.objects.get(userID=user.ID)
        if userInfo.selfAvatar == 1:
            userInfo.avatar.delete()
        userInfo.avatar = avatar
        userInfo.selfAvatar = 1
        userInfo.save()
        result = {'result': 0, 'message': '上传成功!', 'avatarUrl': userInfo.avatar.url}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkUserInfo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        userInfo = UserInfo.objects.get(userID=user.ID)
        result = {'result': 0,
                  'message': '查看个人信息成功!',
                  'description': userInfo.description,
                  'nickname': user.nickname,
                  'realname': userInfo.realname}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def changeUserInfo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        description = request.POST.get('description')
        nickname = request.POST.get('nickname')
        realname = request.POST.get('realname')
        user = User.objects.get(email=email)
        userInfo = UserInfo.objects.get(userID=user.ID)
        userInfo.description = description
        user.nickname = nickname
        userInfo.realname = realname
        user.save()
        userInfo.save()
        result = {'result': 0,
                  'message': '修改个人信息成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def changePassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        user = User.objects.get(email=email)
        if user.password != oldPassword:
            result = {'result': 2,
                      'message': '密码错误，请检查输入!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        elif oldPassword == newPassword:
            result = {'result': 3,
                      'message': '新密码不能与旧密码相同!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            user.password = newPassword
            user.save()
            result = {'result': 0,
                      'message': '修改密码成功!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkBrowseProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        proNames = []
        groups = []
        checkTimes = []
        for i in CheckProject.objects.filter(userID=user.ID).order_by('-checkTime'):
            project = Project.objects.get(ID=i.projectID)
            if project.isDelete == 0:
                proNames.append(project.proName)
                groups.append(Group.objects.get(ID=project.groupID).groupName)
                checkTimes.append(i.checkTime.strftime('%Y-%m-%d %H:%M:%S'))
        result = {'result': 0, 'message': '查看成功!',
                  'proNames': proNames,
                  'groups': groups,
                  'checkTimes': checkTimes}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkCollections(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        proNames = []
        groups = []
        for i in CollectProject.objects.filter(userID=user.ID):
            project = Project.objects.get(ID=i.projectID)
            if project.isDelete == 0:
                proNames.append(project.proName)
                groups.append(Group.objects.get(ID=project.groupID).groupName)
        result = {'result': 0, 'message': '查看成功!',
                  'proNames': proNames,
                  'groups': groups}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
