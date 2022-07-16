# # chat/consumers.py
from distutils import text_file
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # lobby
        self.room_group_name = 'chat_%s' % self.room_name # chat_lobby
        # print(f'room_name: {self.room_name}, room_group_name: {self.room_group_name}')
        print(f'self: {self}')
        print(f'self.channel_name: ', self.channel_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            # self.room_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            # self.room_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        '''보내는 쪽에서만 recevie()함수 호출됨'''
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f'receive()/self.channel_name: ', self.channel_name)
        print('consumers.py/receive() text_data_json: ', text_data_json)
        # Send message to room group
        '''sender_channel_name는 보내는 사람의 channel_name을 나타냄'''
        '''xxx는 자기   자신의 channel_name을 나타냄'''
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel_name': self.channel_name.split('.')[1] # specific.yYLgENvP!PsNmnCeQiyBI 를 뒤에만 쪼갬
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        '''접속해있는 브라우저의 개수만큼 출력이 반복된다'''
        print('chat_mag()/self.channel_name: ', self.channel_name)
        print(f"chat_msg()/event.sender_channel_name: {event['sender_channel_name']}")
        print('consumers.py/chat_message()/message: ', message) # welcome
        print('consumers.py/chat_message()/event: ', event) # {'type': 'chat_message', 'message': 'welcome'}
        # 누구로 부터 온것인지 어떻게 알 수 있을까??
        
        await self.send(text_data=json.dumps({
            'message': message,
            'my_channel_name': self.channel_name.split('.')[1],
            'sender_channel_name': event['sender_channel_name']
        }))
