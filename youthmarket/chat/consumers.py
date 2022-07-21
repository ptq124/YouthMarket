# # chat/consumers.py
from distutils import text_file
from email import message
# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from post.models import Msg, User

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages_temp = Msg.last_10_messages()
        messages = []
        for i in range(len(messages_temp)-1, -1, -1):
            messages.append(messages_temp[i])
        print('fetch_messages()/messages: ', messages)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_chat_message(content)
        
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(userName = author)[0] # Msg의 첫번째 field가 author라서 [0]
        message = Msg.objects.create(author=author_user, content=data['message'])
        print('new_message()/author_user: ', author_user)
        print('new_message()/message:', message)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self, message):
        print('message_to_json()/message: ', message)
        print('message_to_json()/message.author: ', message.author)
        print('message_to_json()/message.author.userName: ', message.author.userName)
        return {
            'author': message.author.userName,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # lobby
        self.room_group_name = 'chat_%s' % self.room_name # chat_lobby
        # print(f'room_name: {self.room_name}, room_group_name: {self.room_group_name}')
        print(f'connect()/self: {self}')
        print(f'connect()/self.channel_name: ', self.channel_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
            # self.room_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
            # self.room_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        '''보내는 쪽에서만 recevie()함수 호출됨'''
        text_data_json = json.loads(text_data)
        print(f'receive()/text_data_json: {text_data_json}')
        self.commands[text_data_json['command']](self, text_data_json) # Jsonify를 통해 온 명령어에 따라 적절한 함수호출함
    
    def send_chat_message(self, message):
        print(f'receive()/self.channel_name: ', self.channel_name)
        # Send message to room group
        '''sender_channel_name는 보내는 사람의 channel_name을 나타냄'''
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel_name': self.channel_name.split('.')[1] # specific.yYLgENvP!PsNmnCeQiyBI 를 뒤에만 쪼갬
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        '''접속해있는 브라우저의 개수만큼 출력이 반복된다'''
        print('chat_mag()/self.channel_name: ', self.channel_name)
        print(f"chat_msg()/event.sender_channel_name: {event['sender_channel_name']}")
        print('consumers.py/chat_message()/message: ', message)
        # {'command': 'new_message', 'message': {'author': '고경환2', 'content': '오른쪽이야2', 'timestamp': '2022-07-21 02:47:33.255798'}}
        print('consumers.py/chat_message()/event: ', event) 
        # {'type': 'chat_message', 'message': {'command': 'new_message', 'message': {'author': '고경환2', 'content': '오른쪽이야2', 'timestamp': '2022-07-21 02:47:33.255798'}}, 'sender_channel_name': 'LMCbvVhA!ItYMOJiEJPRe'}
        
        self.send(text_data=json.dumps(message))
