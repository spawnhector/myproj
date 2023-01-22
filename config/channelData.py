# config/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core import serializers
# from myproj.schannels.serializers import ChannelSerializer
from myproj.schannels.models import SChannel

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
        app_channel = SChannel.objects.all()
        serialized_obj = serializers.serialize('python', app_channel)
        channel_data= []
        for dat in serialized_obj:
            dat = list(dat.values())[1:]
            channel_data.append(dat)
        self.send(text_data=json.dumps(channel_data))

    def disconnect(self, close_code):
        pass
