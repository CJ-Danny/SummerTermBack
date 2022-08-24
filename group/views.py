import json
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from group.models import *
from user.models import *
from message.models import *
from project.models import *
from user.send_email import random_str


@csrf_exempt
def checkGroups(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        groupNames = []
        ownerNames = []
        membersNumber = []
        createTimes = []
        positions = []
        for i in UserGroup.objects.filter(userID=user.ID):
            group = Group.objects.get(ID=i.groupID)
            groupNames.append(group.groupName)
            ownerNames.append(User.objects.get(ID=group.ownerID).nickname)
            membersNumber.append(UserGroup.objects.filter(groupID=group.ID).count())
            createTimes.append(group.createTime.strftime('%Y-%m-%d %H:%M:%S'))
            positions.append(i.position)
        result = {'result': 0,
                  'message': '查看成功!',
                  'groupNames': groupNames,
                  'ownerNames': ownerNames,
                  'membersNumber': membersNumber,
                  'createTimes': createTimes,
                  'positions': positions}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def createGroup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        if Group.objects.filter(groupName=groupName).exists():
            result = {'result': 2, 'message': '团队名称已存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            user = User.objects.get(email=email)
            group = Group(groupName=groupName, ownerID=user.ID, createTime=timezone.now())
            group.save()
            userGroup = UserGroup(userID=user.ID, groupID=group.ID, position=0)
            userGroup.save()
            groupDir = Document(docName=group.groupName,
                                fatherURL='',
                                URL=group.groupName + '/',
                                content='',
                                createTime=timezone.now())
            groupDir.save()
            proDir = Document(docName='项目文件夹',
                              fatherURL=groupDir.URL,
                              URL=groupDir.URL + '项目文件夹/',
                              content='',
                              createTime=timezone.now())
            proDir.save()
            result = {'result': 0, 'message': '创建团队成功!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def deleteGroup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        for i in Project.objects.filter(groupID=group.ID):
            CheckProject.objects.filter(projectID=i.ID).delete()
            CollectProject.objects.filter(projectID=i.ID).delete()
            Prototype.objects.filter(projectID=i.ID).delete()
        Project.objects.filter(groupID=group.ID).delete()
        UserGroup.objects.filter(groupID=group.ID).delete()
        delURL = groupName + '/'
        for i in Document.objects.all():
            if not re.match(delURL, i.URL) is None:
                i.delete()
        group.delete()
        result = {'result': 0, 'message': '解散成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def quitGroup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        for i in Project.objects.filter(groupID=group.ID):
            CheckProject.objects.filter(projectID=i.ID, userID=user.ID).delete()
            CollectProject.objects.filter(projectID=i.ID, userID=user.ID).delete()
        UserGroup.objects.filter(userID=user.ID, groupID=group.ID).delete()
        result = {'result': 0, 'message': '退出成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkGroupMember(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        members = []
        positions = []
        selfPosition = UserGroup.objects.get(userID=user.ID, groupID=group.ID).position
        realnames = []
        emails = []
        avatarUrls = []
        for i in UserGroup.objects.filter(groupID=group.ID).order_by('position'):
            tempUser = User.objects.get(ID=i.userID)
            userinfo = UserInfo.objects.get(userID=tempUser.ID)
            members.append(tempUser.nickname)
            positions.append(i.position)
            emails.append(tempUser.email)
            realnames.append(UserInfo.objects.get(userID=tempUser.ID).realname)
            avatarUrls.append(userinfo.avatar.url)
        result = {'result': 0, 'message': '查看成功!',
                  'members': members,
                  'positions': positions,
                  'selfPosition': selfPosition,
                  'realnames': realnames,
                  'emails': emails,
                  'avatarUrls': avatarUrls}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def inviteGroupMember(request):
    if request.method == 'POST':
        ownerEmail = request.POST.get('ownerEmail')
        targetEmail = request.POST.get('targetEmail')
        groupName = request.POST.get('groupName')
        owner = User.objects.get(email=ownerEmail)
        group = Group.objects.get(groupName=groupName)
        if not User.objects.filter(email=targetEmail).exists():
            result = {'result': 2, 'message': '对应成员不存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        user = User.objects.get(email=targetEmail)
        if UserGroup.objects.filter(groupID=group.ID, userID=user.ID).exists():
            result = {'result': 3, 'message': '该成员已在团队中!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        message = Message(userID=user.ID,
                          title='邀请加入团队通知',
                          content='' + owner.nickname + '邀请你加入团队：' + groupName + '。祝你们合作愉快。',
                          time=timezone.now(),
                          type=0,
                          isRead=0,
                          sender=groupName)
        message.save()
        result = {'result': 0, 'message': '邀请成功，请耐心等待对方确认!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def deleteGroupMember(request):
    if request.method == 'POST':
        ownerEmail = request.POST.get('ownerEmail')
        targetEmail = request.POST.get('targetEmail')
        groupName = request.POST.get('groupName')
        group = Group.objects.get(groupName=groupName)
        ownerUser = User.objects.get(email=ownerEmail)
        targetUser = User.objects.get(email=targetEmail)
        for i in Project.objects.filter(groupID=group.ID):
            CheckProject.objects.filter(projectID=i.ID, userID=targetUser.ID).delete()
            CollectProject.objects.filter(projectID=i.ID, userID=targetUser.ID).delete()
        UserGroup.objects.filter(userID=targetUser.ID, groupID=group.ID).delete()
        result = {'result': 0, 'message': '成员删除成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def appointAdmin(request):
    if request.method == 'POST':
        ownerEmail = request.POST.get('ownerEmail')
        targetEmail = request.POST.get('targetEmail')
        groupName = request.POST.get('groupName')
        group = Group.objects.get(groupName=groupName)
        ownerUser = User.objects.get(email=ownerEmail)
        targetUser = User.objects.get(email=targetEmail)
        userGroup = UserGroup.objects.get(userID=targetUser.ID, groupID=group.ID)
        userGroup.position = 1
        userGroup.save()
        result = {'result': 0, 'message': '设置成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def cancelAdmin(request):
    if request.method == 'POST':
        ownerEmail = request.POST.get('ownerEmail')
        targetEmail = request.POST.get('targetEmail')
        groupName = request.POST.get('groupName')
        group = Group.objects.get(groupName=groupName)
        ownerUser = User.objects.get(email=ownerEmail)
        targetUser = User.objects.get(email=targetEmail)
        userGroup = UserGroup.objects.get(userID=targetUser.ID, groupID=group.ID)
        userGroup.position = 2
        userGroup.save()
        result = {'result': 0, 'message': '设置成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkGroupProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        proNames = []
        createTimes = []
        status = []
        isCollect = []
        isShared = []
        for i in Project.objects.filter(groupID=group.ID, isDelete=0).order_by('-createTime'):
            proNames.append(i.proName)
            createTimes.append(i.createTime.strftime('%Y-%m-%d %H:%M:%S'))
            status.append(i.status)
            isShared.append(i.isShare)
            if CollectProject.objects.filter(projectID=i.ID, userID=user.ID):
                isCollect.append(1)
            else:
                isCollect.append(0)
        result = {'result': 0, 'message': '查看成功!',
                  'proNames': proNames,
                  'createTimes': createTimes,
                  'status': status,
                  'isCollect': isCollect,
                  'isShared': isShared}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def changeProState(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        state = request.POST.get('state')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        project.status = state
        project.save()
        result = {'result': 0, 'message': '创建项目成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def createProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        if Project.objects.filter(proName=proName, groupID=group.ID).exists():
            result = {'result': 2, 'message': '项目名称已存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            project = Project(proName=proName,
                              isDelete=0,
                              deleteTime=timezone.now(),
                              status='未开始',
                              createTime=timezone.now(),
                              groupID=group.ID,
                              isShare=0,
                              shareCode='',
                              UMLContent='')
            project.save()
            document = Document(docName=proName,
                                fatherURL=groupName + '/项目文件夹/',
                                URL=groupName + '/项目文件夹/' + proName + '/',
                                content='',
                                createTime=timezone.now())
            document.save()
            result = {'result': 0, 'message': '创建项目成功!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


"""
    项目名总长度最大20
    复制前项目名长度大于16时先检查末尾是否为"-副本x"
        末尾匹配则修改x为合适的值或报错
        末尾不匹配则截取前16字符，再加上合适的"-副本x"或报错
    项目名长度小于等于16时先检查末尾是否为"-副本x"
        末尾匹配则修改x为合适的值或报错
        末尾不匹配则加上合适的"-副本x"或报错
"""


@csrf_exempt
def copyProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        newProNameL = ''
        newProNameR = ''
        pattern = re.compile('-副本[0-9]$')
        if len(proName) > 16:
            if pattern.search(proName) is None:
                newProNameL = proName[:16]
                newProNameR = '-副本'
                for i in range(10):
                    tmpProName = newProNameL + newProNameR + str(i)
                    if not Project.objects.filter(groupID=group.ID, proName=tmpProName).exists():
                        newProNameR += str(i)
                        break
                    if i == 9:
                        result = {'result': 2, 'message': '已达复制上限，请手动重命名后再复制!'}
                        return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                names = proName.split('-')
                for i in names[:-1]:
                    newProNameL += i + '-'
                newProNameL = newProNameL[:-1]
                newProNameR = '-副本'
                for i in range(10):
                    tmpProName = newProNameL + newProNameR + str(i)
                    if not Project.objects.filter(groupID=group.ID, proName=tmpProName).exists():
                        newProNameR += str(i)
                        break
                    if i == 9:
                        result = {'result': 2, 'message': '已达复制上限，请手动重命名后再复制!'}
                        return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            if pattern.search(proName) is None:
                newProNameL = proName
                newProNameR = '-副本'
                for i in range(10):
                    tmpProName = newProNameL + newProNameR + str(i)
                    if not Project.objects.filter(groupID=group.ID, proName=tmpProName).exists():
                        newProNameR += str(i)
                        break
                    if i == 9:
                        result = {'result': 2, 'message': '已达复制上限，请手动重命名后再复制!'}
                        return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                names = proName.split('-')
                for i in names[:-1]:
                    newProNameL += i + '-'
                newProNameL = newProNameL[:-1]
                newProNameR = '-副本'
                for i in range(10):
                    tmpProName = newProNameL + newProNameR + str(i)
                    if not Project.objects.filter(groupID=group.ID, proName=tmpProName).exists():
                        newProNameR += str(i)
                        break
                    if i == 9:
                        result = {'result': 2, 'message': '已达复制上限，请手动重命名后再复制!'}
                        return HttpResponse(json.dumps(result), content_type="application/json")
        newProName = newProNameL + newProNameR
        if Project.objects.filter(groupID=group.ID, proName=newProName).exists():
            result = {'result': 2, 'message': '已达复制上限，请手动重命名后再复制!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        newProject = Project(proName=newProName,
                             isDelete=0,
                             deleteTime=timezone.now(),
                             status='未开始',
                             createTime=timezone.now(),
                             groupID=group.ID,
                             isShare=0,
                             shareCode='')
        newProject.save()
        for i in Prototype.objects.filter(projectID=project.ID):
            prototype = Prototype(protoName=i.protoName,
                                  projectID=newProject.ID,
                                  canvasData=i.canvasData,
                                  canvasStyle=i.canvasStyle,
                                  canvasHeight=i.canvasHeight,
                                  canvasWidth=i.canvasWidth,
                                  createTime=timezone.now())
            prototype.save()
        newDocument = Document(docName=newProject.proName,
                               fatherURL=groupName + '/项目文件夹/',
                               URL=groupName + '/项目文件夹/' + newProject.proName + '/',
                               content='',
                               createTime=timezone.now())
        newDocument.save()
        oldFatherURL = groupName + '/项目文件夹/' + project.proName + '/'
        newFatherURL = newDocument.URL
        for i in Document.objects.filter(fatherURL=oldFatherURL):
            document = Document(docName=i.docName,
                                fatherURL=newFatherURL,
                                URL=re.sub(oldFatherURL, newFatherURL, i.URL, 1),
                                content=i.content,
                                createTime=timezone.now())
            document.save()
        result = {'result': 0, 'message': '复制成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def collectProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(proName=proName, groupID=group.ID)
        collectProject = CollectProject(userID=user.ID, projectID=project.ID)
        collectProject.save()
        result = {'result': 0, 'message': '收藏成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def cancelCollection(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(proName=proName, groupID=group.ID)
        CollectProject.objects.filter(userID=user.ID, projectID=project.ID).delete()
        result = {'result': 0, 'message': '取消收藏成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def deleteProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(proName=proName, groupID=group.ID)
        project.isDelete = 1
        project.deleteTime = timezone.now()
        project.save()
        result = {'result': 0, 'message': '删除成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def renameProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        oldProName = request.POST.get('oldProName')
        newProName = request.POST.get('newProName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        if Project.objects.filter(proName=newProName, groupID=group.ID).exists():
            result = {'result': 2, 'message': '项目名称已存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        project = Project.objects.get(proName=oldProName, groupID=group.ID)
        project.proName = newProName
        project.save()
        oldURL = groupName + '/项目文件夹/' + oldProName + '/'
        newURL = groupName + '/项目文件夹/' + newProName + '/'
        for i in Document.objects.filter(fatherURL=oldURL):
            i.fatherURL = newURL
            i.URL = newURL + i.docName
            i.save()
        document = Document.objects.get(URL=oldURL)
        document.URL = newURL
        document.docName = newProName
        document.save()
        result = {'result': 0, 'message': '重命名成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkRecycleBin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        proNames = []
        deleteTimes = []
        for i in Project.objects.filter(isDelete=1, groupID=group.ID).order_by('deleteTime'):
            proNames.append(i.proName)
            deleteTimes.append(i.deleteTime.strftime('%Y-%m-%d %H:%M:%S'))
        result = {'result': 0, 'message': '查看成功!',
                  'proNames': proNames,
                  'deleteTimes': deleteTimes}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def recoverProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(proName=proName, groupID=group.ID)
        project.isDelete = 0
        project.save()
        result = {'result': 0, 'message': '恢复项目成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def removeProject(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(proName=proName, groupID=group.ID)
        CheckProject.objects.filter(projectID=project.ID).delete()
        CollectProject.objects.filter(projectID=project.ID).delete()
        Prototype.objects.filter(projectID=project.ID).delete()
        delURL = groupName + '/项目文件夹/' + proName + '/'
        Document.objects.filter(fatherURL=delURL).delete()
        Document.objects.filter(URL=delURL).delete()
        Project.objects.filter(proName=proName, groupID=group.ID).delete()
        result = {'result': 0, 'message': '彻底删除项目成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def updateProjectCheckTime(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(proName=proName, groupID=group.ID)
        if CheckProject.objects.filter(projectID=project.ID, userID=user.ID):
            checkproject = CheckProject.objects.get(projectID=project.ID, userID=user.ID)
            checkproject.checkTime = timezone.now()
            checkproject.save()
        else:
            checkproject = CheckProject(projectID=project.ID, userID=user.ID, checkTime=timezone.now())
            checkproject.save()
        result = {'result': 0, 'message': '更新成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
