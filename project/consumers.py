import re

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from project.models import *
from group.models import *
from user.models import *


class SaveDocument(WebsocketConsumer):
    def connect(self):
        docURL = self.scope['url_route']['kwargs']['docURL']
        docURL = re.sub('_', '/', docURL)
        document = Document.objects.get(URL=docURL)
        self.room_name = 'doc_' + str(document.ID)
        self.room_group_name = 'group_' + self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        # pass

    def receive(self, text_data):
        # print(text_data)
        # self.send('hello')
        text_data_json = json.loads(text_data)
        email = text_data_json['email']
        URL = text_data_json['URL']
        content = text_data_json['content']
        print(content)
        document = Document.objects.get(URL=URL)
        document.content = content
        document.save()
        result = {'result': 0, 'content': content}
        event = {
            'type': 'chat_message',
            'message': result
        }
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, event)

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))


# class SavePrototype(WebsocketConsumer):
#     def connect(self):
#         proURL = self.scope['url_route']['kwargs']['proURL']
#         names = proURL.split('_')
#         groupName = names[0]
#         proName = names[1]
#         protoName = names[2]
#         group = Group.objects.get(groupName=groupName)
#         project = Project.objects.get(groupID=group.ID, proName=proName)
#         prototype = Prototype.objects.get(projectID=project.ID, protoName=protoName)
#         self.room_name = 'proto_' + str(prototype.ID)
#         self.room_group_name = 'group_' + self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#         # pass
#
#     def receive(self, text_data):
#         # print(text_data)
#         # self.send('hello')
#         text_data_json = json.loads(text_data)
#         email = text_data_json['email']
#         groupName = text_data_json['groupName']
#         proName = text_data_json['proName']
#         protoName = text_data_json['protoName']
#         canvasData = text_data_json['canvasData']
#         canvasStyle = text_data_json['canvasStyle']
#         canvasHeight = text_data_json['canvasHeight']
#         canvasWidth = text_data_json['canvasWidth']
#         user = User.objects.get(email=email)
#         group = Group.objects.get(groupName=groupName)
#         project = Project.objects.get(groupID=group.ID, proName=proName)
#         prototype = Prototype.objects.get(projectID=project.ID, protoName=protoName)
#         prototype.canvasData = canvasData
#         prototype.canvasStyle = canvasStyle
#         prototype.canvasHeight = canvasHeight
#         prototype.canvasWidth = canvasWidth
#         prototype.save()
#         result = {'result': 0, 'content': content}
#         event = {
#             'type': 'chat_message',
#             'message': result
#         }
#         async_to_sync(self.channel_layer.group_send)(self.room_group_name, event)
#
#     def chat_message(self, event):
#         message = event['message']
#         self.send(text_data=json.dumps(message))
