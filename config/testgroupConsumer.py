from channels.generic.websocket import WebsocketConsumer
import json
import ast
from asgiref.sync import async_to_sync
import psycopg2
from myproj.schannels.models import SChannel
from myproj.signals.models import Signals
from myproj.users.api.serializers import ChannelSerializer

class MyConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(MyConsumer, self).__init__(*args, **kwargs)
        self.addedChannelSignalsResult = False


    def connect(self):
        self.server_name = self.scope["url_route"]["kwargs"]["server_name"]
        # # Join room group
        if self.server_name == "client":
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "signals_%s" % self.room_name
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # # # Send message to room group
        if self.server_name == "trade_socket":
            self.dict_obj = eval(text_data)
            if self.dict_obj['trade_status'] == 'Open':
                self.addedChannelSignalsResult = self.addChannelSignals(self.dict_obj)
            else:
                self.addedChannelSignalsResult = self.updateChannelSignals(self.dict_obj)

            self.room_group_name = "signals_%s" % self.dict_obj['currency']
        else:
            self.addedChannelSignalsResult = self.getChannelData(self.room_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": 'client', "message": self.addedChannelSignalsResult}
        )

    def addChannelSignals(self,tradeData):
        channel_by_name = SChannel.objects.get(channel_name=tradeData['currency'])
        if channel_by_name:
            result_id = channel_by_name.id
            app_channel = SChannel(id=result_id)
            signal = Signals.objects.add_signal(result_id,tradeData)
            app_channel.signals.add(signal.id)
            app_channels = ChannelSerializer(channel_by_name)
            return app_channels.data

    def updateChannelSignals(self,tradeData):
        signal_by_ticket = Signals.objects.get(trade_ticket=tradeData['trade_ticket'])
        if signal_by_ticket:
            result_id = signal_by_ticket.id
            app_signal = Signals(id=result_id)
            print(app_signal)

    def getChannelData(self,channel_name):
        channel_by_name = SChannel.objects.get(channel_name=channel_name)
        app_channels = ChannelSerializer(channel_by_name)
        return app_channels.data

    def client(self, event):
        self.send(text_data=json.dumps({
            'message':event['message']
        }))
