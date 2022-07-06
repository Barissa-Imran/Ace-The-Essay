from django.contrib.auth import get_user_model
import json
# from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):

    # Handle the websocket connection
    async def connect(self):
        # get the current user id from the url
        my_id = self.scope['user'].id
        # get the receipient user id from url route in scope
        other_user_id = self.scope['url_route']['kwargs']['id']

        # handle concatenation of user id's to create a room name
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        # create a group name from the room name without any escaping or quoting
        self.room_group_name = 'chat_%s' % self.room_name

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the websocket connection
        await self.accept()

    # Receive message from websocket
    async def recieve(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # call the save_message function and save the message
        await self.save_message(username, self.room_group_name, message)
        
        # send message to room Group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # recieve message from group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # send message to websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # Handle websocket disconnection
    async def disconnect(self, close_code):
        # Leave channel Group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # save message in a model instance
    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        ChatMessage.objects.create(
            sender=username,
            content=message,
            thread_name=thread_name
        )


# -----------------------------------------
# User = get_user_model()
# class ChatConsumer(WebsocketConsumer):

#     #get the messages from the db
#     def fetch_messages(self, data):
#         messages = Message.last_10_messages(self)
#         # print(messages)
#         content = {
#             'command': 'messages',
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_message(content)

#     #create a new message from websocket
#     def new_message(self, data):
#         author = data['from']
#         author_user = User.objects.filter(username=author)[0]
#         message = Message.objects.create(
#             author=author_user,
#             content=data['message'])
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         return self.send_chat_message(content)


#     # serialize individual messages
#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         # print(result)
#         return result

#     # produce the content from the serialised message - above
#     def message_to_json(self, message):
#         return {
#             'author': message.author.username,
#             'content': message.content,
#             'timestamp': str(message.timestamp)
#         }

#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }

#     def connect(self):
#         # get the room name from scope in routing
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         # create a group name from the room name without any escaping or quoting
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()  # accepts websocket connection

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)

#     def send_chat_message(self, message):

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # send messages from db
#     def send_message(self, message):
#         # Send message to WebSocket
#         self.send(text_data=json.dumps(message))

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps(message))
