"""SummerTermBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from SummerTermBack.settings import MEDIA_ROOT
from user.views import *
from group.views import *
from project.views import *
from message.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    path('back/user/register/', register, name='register'),
    path('back/user/login/', login, name='login'),
    path('back/user/logout/', logout, name='logout'),
    path('back/user/forgetPassword/', forgetPassword, name='forgetPassword'),
    path('back/user/registerEmail/', registerEmail, name='registerEmail'),
    path('back/user/forgetPasswordEmail/', forgetPasswordEmail, name='forgetPasswordEmail'),
    path('back/user/changeAvatar/', changeAvatar, name='changeAvatar'),
    path('back/user/checkUserInfo/', checkUserInfo, name='checkUserInfo'),
    path('back/user/changeUserInfo/', changeUserInfo, name='changeUserInfo'),
    path('back/user/changePassword/', changePassword, name='changePassword'),
    path('back/user/checkBrowseProject/', checkBrowseProject, name='checkBrowseProject'),
    path('back/user/checkCollections/', checkCollections, name='checkCollections'),

    path('back/group/checkGroups/', checkGroups, name='checkGroups'),
    path('back/group/createGroup/', createGroup, name='createGroup'),
    path('back/group/deleteGroup/', deleteGroup, name='deleteGroup'),
    path('back/group/quitGroup/', quitGroup, name='quitGroup'),
    path('back/group/checkGroupMember/', checkGroupMember, name='checkGroupMember'),
    path('back/group/inviteGroupMember/', inviteGroupMember, name='inviteGroupMember'),
    path('back/group/deleteGroupMember/', deleteGroupMember, name='deleteGroupMember'),
    path('back/group/appointAdmin/', appointAdmin, name='appointAdmin'),
    path('back/group/cancelAdmin/', cancelAdmin, name='cancelAdmin'),
    path('back/group/checkGroupProject/', checkGroupProject, name='checkGroupProject'),
    path('back/group/createProject/', createProject, name='createProject'),
    path('back/group/collectProject/', collectProject, name='collectProject'),
    path('back/group/cancelCollection/', cancelCollection, name='cancelCollection'),
    path('back/group/deleteProject/', deleteProject, name='deleteProject'),
    path('back/group/renameProject/', renameProject, name='renameProject'),
    path('back/group/checkRecycleBin/', checkRecycleBin, name='checkRecycleBin'),
    path('back/group/recoverProject/', recoverProject, name='recoverProject'),
    path('back/group/removeProject/', removeProject, name='removeProject'),
    path('back/group/updateProjectCheckTime/', updateProjectCheckTime, name='updateProjectCheckTime'),
    path('back/group/copyProject/', copyProject, name='copyProject'),
    path('back/group/changeProState/', changeProState, name='changeProState'),

    path('back/message/checkMessages/', checkMessages, name='checkMessages'),
    path('back/message/checkMessageContent/', checkMessageContent, name='checkMessageContent'),
    path('back/message/deleteMessage/', deleteMessage, name='deleteMessage'),
    path('back/message/deleteMessages/', deleteMessages, name='deleteMessages'),
    path('back/message/joinTeam/', joinTeam, name='joinTeam'),

    path('back/project/createPrototype/', createPrototype, name='createPrototype'),
    path('back/project/checkPrototypes/', checkPrototypes, name='checkPrototypes'),
    path('back/project/checkPrototype/', checkPrototype, name='checkPrototype'),
    path('back/project/savePrototype/', savePrototype, name='savePrototype'),
    path('back/project/removePrototype/', removePrototype, name='removePrototype'),
    path('back/project/createDocument/', createDocument, name='createDocument'),
    path('back/project/checkDocuments/', checkDocuments, name='checkDocuments'),
    path('back/project/checkDocument/', checkDocument, name='checkDocument'),
    path('back/project/saveDocument/', saveDocument, name='saveDocument'),
    path('back/project/removeDocument/', removeDocument, name='removeDocument'),
    path('back/project/checkFileTree/', checkFileTree, name='checkFileTree'),
    path('back/project/changeDocumentInfo/', changeDocumentInfo, name='changeDocumentInfo'),
    path('back/project/sharePrototype/', sharePrototype, name='sharePrototype'),
    path('back/project/cancelSharePrototype/', cancelSharePrototype, name='cancelSharePrototype'),
    path('back/project/checkSharedPrototype/', checkSharedPrototype, name='checkSharedPrototype'),
    path('back/project/htmlToMarkdowm/', htmlToMarkdowm, name='htmlToMarkdowm'),
    path('back/project/checkUML/', checkUML, name='checkUML'),
    path('back/project/saveUML/', saveUML, name='saveUML'),
]
