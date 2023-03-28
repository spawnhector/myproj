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
from channels.layers import get_channel_layer

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
        message = json.loads(text_data)
        self.server_name = message['server_name']
        # # Send message to room group
        if self.server_name == "trade_socket":
            self.dict_obj = eval(message['data'])
            self.room_name = self.dict_obj['currency']
            self.room_group_name = "signals_%s" % self.room_name
            if self.dict_obj['trade_status'] == 'Open':
                self.addedChannelSignalsResult = await database_sync_to_async(self.addChannelSignals)()
                await self.send_group_updated_message()
            else:
                self.addedChannelSignalsResult = await database_sync_to_async(self.updateChannelSignals)()
                await self.send_group_updated_message()
            self.room_group_name = "signals_%s" % self.dict_obj['currency']
        else:
            self.room_name = message['channel']
            self.room_group_name = "signals_%s" % self.room_name
            if message.get('action') == 'join_group':
                self.room_action = 'join_group'
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.send_group_joined_message()
            elif message.get('action') == 'leave_group':
                await self.send_group_left_message()
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def leave_all_groups(self):
        # Disconnect from the WebSocket if no more groups are joined
        groups = await self.channel_layer.group_channels(self.room_group_name)
        if len(groups) == 0:
            await self.close()

    async def send_group_joined_message(self):
        message = await database_sync_to_async(self.getChannelData)()
        await self.channel_layer.group_send(self.room_group_name, {"type": 'client_join', "message": message})

    async def send_group_left_message(self):
        message = {'action': 'group_left', 'group_name': self.room_group_name}
        await self.send(text_data=json.dumps({
            'action': 'group_left',
            'message':message
        }))
        # await self.channel_layer.group_send(self.room_group_name, {"type": 'client_leave', "message": message})

    async def send_group_updated_message(self):
        message = {'signals':{
                'id':self.addedChannelSignalsResult.id,
                'take_profit': self.addedChannelSignalsResult.take_profit,
                'trade_date': self.addedChannelSignalsResult.trade_date.strftime('%Y-%m-%d %H:%M:%S.%f%z'),
                'trade_price':self.addedChannelSignalsResult.trade_price,
                'trade_status': self.addedChannelSignalsResult.trade_status,
                'trade_ticket':self.addedChannelSignalsResult.trade_ticket,
                'trade_type': self.addedChannelSignalsResult.trade_type
            }
        }
        await self.channel_layer.group_send(self.room_group_name, {"type": 'updated_signal', "message": message})

    def addChannelSignals(self):
        channel_by_name = SChannel.objects.get(channel_name=self.dict_obj['currency'])
        if channel_by_name:
            result_id = channel_by_name.id
            app_channel = SChannel(id=result_id)
            signal = Signals.objects.add_signal(result_id,self.dict_obj)
            app_channel.signals.add(signal.id)
            app_channels = SignalsSerializer(channel_by_name)
            return signal

    def updateChannelSignals(self):
        signal_by_ticket = Signals.objects.get(trade_ticket=self.dict_obj['trade_ticket'])
        if signal_by_ticket:
            result_id = signal_by_ticket.id
            app_signal = Signals(id=result_id)
            print(app_signal)

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
