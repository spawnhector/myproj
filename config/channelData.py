# config/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChannelDataConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'data'
        self.room_group_name = "channel_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        # # # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "channel_data"}
        )

    # Receive message from room group
    def channel_data(self, event):
        self.send(text_data=json.dumps({"message": 'here'}))

    def disconnect(self, close_code):
        pass
