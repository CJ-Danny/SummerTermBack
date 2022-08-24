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
from user.send_email import *
import markdownify


# Create your views here.
@csrf_exempt
def createPrototype(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        protoName = request.POST.get('protoName')
        canvasData = request.POST.get('canvasData')
        canvasStyle = request.POST.get('canvasStyle')
        canvasHeight = request.POST.get('canvasHeight')
        canvasWidth = request.POST.get('canvasWidth')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        if Prototype.objects.filter(projectID=project.ID, protoName=protoName).exists():
            result = {'result': 2, 'message': '原型名称已存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        prototype = Prototype(protoName=protoName,
                              projectID=project.ID,
                              canvasData=canvasData,
                              canvasStyle=canvasStyle,
                              canvasHeight=canvasHeight,
                              canvasWidth=canvasWidth,
                              createTime=timezone.now())
        prototype.save()
        result = {'result': 0, 'message': '创建成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkPrototypes(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        protoNames = []
        createTimes = []
        for i in Prototype.objects.filter(projectID=project.ID).order_by('createTime'):
            protoNames.append(i.protoName)
            createTimes.append(i.createTime.strftime('%Y-%m-%d %H:%M:%S'))
        result = {'result': 0, 'message': '查看成功!',
                  'protoNames': protoNames,
                  'createTimes': createTimes}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkPrototype(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        protoName = request.POST.get('protoName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        prototype = Prototype.objects.get(projectID=project.ID, protoName=protoName)
        result = {'result': 0, 'message': '查看成功!',
                  'canvasData': prototype.canvasData,
                  'canvasStyle': prototype.canvasStyle,
                  'canvasHeight': prototype.canvasHeight,
                  'canvasWidth': prototype.canvasWidth}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def savePrototype(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        protoName = request.POST.get('protoName')
        canvasData = request.POST.get('canvasData')
        canvasStyle = request.POST.get('canvasStyle')
        canvasHeight = request.POST.get('canvasHeight')
        canvasWidth = request.POST.get('canvasWidth')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        prototype = Prototype.objects.get(projectID=project.ID, protoName=protoName)
        prototype.canvasData = canvasData
        prototype.canvasStyle = canvasStyle
        prototype.canvasHeight = canvasHeight
        prototype.canvasWidth = canvasWidth
        prototype.save()
        result = {'result': 0, 'message': '保存成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def removePrototype(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        protoName = request.POST.get('protoName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        Prototype.objects.filter(projectID=project.ID, protoName=protoName).delete()
        result = {'result': 0, 'message': '删除成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkUML(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        result = {'result': 0, 'message': '查看成功!',
                  'content': project.UMLContent,}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def saveUML(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        content = request.POST.get('content')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        project.UMLContent = content
        project.save()
        result = {'result': 0, 'message': '保存成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def createDocument(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        URL = request.POST.get('URL')
        content = request.POST.get('content')
        names = URL.split('/')
        fatherURL = ""
        docName = ""
        if URL[-1] == '/':
            docName = names[-2]
            for i in names[0:-2]:
                fatherURL += i + '/'
        else:
            docName = names[-1]
            for i in names[0:-1]:
                fatherURL += i + '/'
        user = User.objects.get(email=email)
        if Document.objects.filter(URL=URL).exists():
            result = {'result': 2, 'message': '文档名称已存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        document = Document(docName=docName,
                            fatherURL=fatherURL,
                            URL=URL,
                            content=content,
                            createTime=timezone.now())
        document.save()
        result = {'result': 0, 'message': '创建成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkDocuments(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        URL = request.POST.get('URL')
        names = URL.split('/')
        fatherURL = names[0] + '/' + names[1] + '/' + names[2] + '/'
        user = User.objects.get(email=email)
        docNames = []
        createTimes = []
        for i in Document.objects.filter(fatherURL=fatherURL).order_by('createTime'):
            docNames.append(i.docName)
            createTimes.append(i.createTime.strftime('%Y-%m-%d %H:%M:%S'))
        result = {'result': 0, 'message': '查看成功!',
                  'docNames': docNames,
                  'createTimes': createTimes}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkDocument(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        URL = request.POST.get('URL')
        user = User.objects.get(email=email)
        document = Document.objects.get(URL=URL)
        result = {'result': 0, 'message': '查看成功!',
                  'content': document.content,
                  'docID': document.ID}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def saveDocument(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        URL = request.POST.get('URL')
        content = request.POST.get('content')
        user = User.objects.get(email=email)
        document = Document.objects.get(URL=URL)
        document.content = content
        document.save()
        result = {'result': 0, 'message': '保存成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def removeDocument(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        URL = request.POST.get('URL')
        user = User.objects.get(email=email)
        if URL[-1] == '/':
            for i in Document.objects.all():
                if not re.match(URL, i.fatherURL) is None:
                    i.delete()
        Document.objects.filter(URL=URL).delete()
        result = {'result': 0, 'message': '删除成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


def dfs(url, groupName):
    tree = []
    for i in Document.objects.filter(fatherURL=url):
        if i.URL[-1] == '/':
            if i.fatherURL == groupName + '/项目文件夹/':
                group = Group.objects.get(groupName=groupName)
                project = Project.objects.get(groupID=group.ID, proName=i.docName)
                if project.isDelete == 1:
                    continue
            tree.append({'label': i.docName + '/', 'children': dfs(i.URL, groupName)})
    for i in Document.objects.filter(fatherURL=url):
        if i.URL[-1] != '/':
            tree.append({'label': i.docName})
    return tree


@csrf_exempt
def checkFileTree(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        fileTree = dfs(groupName + '/', groupName)
        result = {'result': 0, 'message': '查看成功!', 'fileTree': fileTree}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def changeDocumentInfo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        oldURL = request.POST.get('oldURL')
        newURL = request.POST.get('newURL')
        user = User.objects.get(email=email)
        if Document.objects.filter(URL=newURL):
            result = {'result': 2, 'message': '该名称已被使用!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        if oldURL[-1] == '/':
            for i in Document.objects.all():
                if not re.match(oldURL, i.fatherURL) is None:
                    i.fatherURL = re.sub(oldURL, newURL, i.fatherURL, 1)
                    i.URL = re.sub(oldURL, newURL, i.URL, 1)
                    i.save()
        document = Document.objects.get(URL=oldURL)
        document.URL = newURL
        document.save()
        result = {'result': 0, 'message': '修改成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def sharePrototype(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        project.isShare = 1
        project.shareCode = random_str(13) + str(project.ID)
        project.save()
        result = {'result': 0, 'message': '分享成功!',
                  'URL': 'http://81.70.16.241/#/getPreviews/?code=' + project.shareCode}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def cancelSharePrototype(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        groupName = request.POST.get('groupName')
        proName = request.POST.get('proName')
        user = User.objects.get(email=email)
        group = Group.objects.get(groupName=groupName)
        project = Project.objects.get(groupID=group.ID, proName=proName)
        project.isShare = 0
        project.save()
        result = {'result': 0, 'message': '取消分享成功!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def checkSharedPrototype(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        ID = int(code[13:])
        project = Project.objects.get(ID=ID)
        group = Group.objects.get(ID=project.groupID)
        if project.isShare == 0:
            result = {'result': 2, 'message': '页面不存在!'}
            return HttpResponse(json.dumps(result), content_type="application/json")
        protoNames = []
        for i in Prototype.objects.filter(projectID=ID):
            protoNames.append(i.protoName)
        result = {'result': 0, 'message': '查看成功!',
                  'protoNames': protoNames,
                  'groupName': group.groupName,
                  'proName': project.proName,
                  'email': '1249116871@qq.com',
                  'avatar': 'publicAvatar/public0.jpg'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def htmlToMarkdowm(request):
    if request.method == 'POST':
        htmlContent = request.POST.get('htmlContent')
        print(htmlContent)
        markdownContent = markdownify.markdownify(htmlContent, heading_style="ATX")
        result = {'result': 0, 'message': '转换成功!',
                  'markdownContent': markdownContent}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result = {'result': 1, 'message': '错误的请求!'}
        return HttpResponse(json.dumps(result), content_type="application/json")
