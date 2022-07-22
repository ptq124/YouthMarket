# # chat/consumers.py
from django.shortcuts import get_object_or_404, render, redirect
# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from post.models import Msg, User, ChatRoom, Message, Post

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        # messages_temp = Msg.last_10_messages()
        messages_temp = Message.last_10_messages(self.chatroom_idx)
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
        # message = Msg.objects.create(author=author_user, content=data['message'])
        chatroom = get_object_or_404(ChatRoom, idx = self.chatroom_idx)
        message = Message.objects.create(author=author_user, content=data['message'], chatroomIdx = chatroom)
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
        self.multi_idx = self.scope['url_route']['kwargs']['room_name']
        self.post_idx, self.seller_idx, self.buyer_idx =  map(int, self.multi_idx.split('-'))
        print(f'self.post_idx: {self.post_idx}, self.seller_idx : {self.seller_idx}, self.buyer_idx: {self.buyer_idx}')
        if self.seller_idx != self.buyer_idx:
            post = get_object_or_404(Post, idx = self.post_idx)
            buyer = get_object_or_404(User, idx = self.buyer_idx)
            seller = get_object_or_404(User, idx = self.seller_idx)
            chatroom = ChatRoom.objects.get_or_create(postIdx = post, sellerIdx = seller, buyerIdx = buyer)
            # print('connect()/chatroom_obj: ', chatroom) # (<ChatRoom: 1_3_1>, False)
            self.chatroom_idx = chatroom[0].idx
            
            print('connect()/chatroom_obj.idx: ', self.chatroom_idx)
            
        else:
            print(f'connect()/slef.seller_idx == self.buyer_idx with {self.seller_idx}')
            exit(0)
        # self.room_group_name = 'chat_%s' % self.post_idx
        self.room_group_name = 'chat_%s' % self.multi_idx
        # print(f'room_name: {self.room_name}, room_group_name: {self.room_group_name}')

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
        print(f'send_chat_message()/self.channel_name: ', self.channel_name)
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
        print('\nsend_message()/message: ', message)
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
