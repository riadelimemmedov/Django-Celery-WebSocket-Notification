import json
from channels.generic.websocket import AsyncWebsocketConsumer

#!NotificationConsumer
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('scope data ', self.scope['url_route'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification%s' % self.room_name
        
        print('group name ', self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)#~convert python dictionary
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    async def send_notification(self,event):
        message = json.loads(event['message'])
        print('message value ', message)
        # Send message to WebSocket well Js websocket
        await self.send(text_data=json.dumps({"message":message}))
