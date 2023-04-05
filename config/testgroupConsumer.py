from channels.generic.websocket import WebsocketConsumer
import json
import ast
from asgiref.sync import async_to_sync
import psycopg2
from myproj.schannels.models import SChannel
from myproj.signals.models import Signals
from myproj.users.api.serializers import ChannelSerializer
from myproj.users.api.serializers import SignalsSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class MyConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(MyConsumer, self).__init__(*args, **kwargs)
        self.open_connections = set()
        self.addedChannelSignalsResult = False

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            self.server_name = message['server_name']
            self.room_name = message['channel']
            self.room_group_name = "signals_%s" % self.room_name
            if message.get('action') == 'join_group':
                self.room_action = 'join_group'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.send_group_joined_message()
            elif message.get('action') == 'leave_group':
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except Exception as e:
            print(f"error sending message: {e}")

    async def send_group_joined_message(self):
        message = await database_sync_to_async(self.getChannelData)()
        await self.channel_layer.group_send(self.room_group_name, {"type": 'client_join', "message": message})

    def getChannelData(self):
        channel_by_name = SChannel.objects.get(channel_name=self.room_name)
        app_channels = ChannelSerializer(channel_by_name)
        return app_channels.data

    async def client_join(self, event):
        await self.send(text_data=json.dumps({
            'action': 'group_joined',
            'message':event['message']
        }))

    async def client_leave(self, event):
        await self.send(text_data=json.dumps({
            'action': 'group_left',
            'message':event['message']
        }))

    async def updated_signal(self, event):
        await self.send(text_data=json.dumps({
            'action': 'new_signal',
            'message': event['message']
        }))

