# config/consumers.py

import json
from asgiref.sync import async_to_sync
import psycopg2
from channels.generic.websocket import WebsocketConsumer

class SignalConsumer(WebsocketConsumer):
    def connect(self):
        self.server_name = self.scope["url_route"]["kwargs"]["server_name"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "signals_%s" % self.room_name
        # # Join room group
        if self.server_name == "client":
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )
        pass

    # Receive message from WebSocket
    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # # # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": text_data}
        )

    def get_connection(self):
        try:
            return psycopg2.connect(
                database="myproj",
                user="MPYzyNUJMZCyzCVdzvItYfIBzoXODgUT",
                password="rpc99B22yoHZJgHczZXxV5uyZDpekj0j6vVsx444xPEMUmJAXSieiGrhbSGVCino",
                host="postgres", port="5432"
            )
        except:
            return False

    def getPairId(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT pair_id FROM public.pairs WHERE pair_symbol = '{self.room_name}';")
        row = cur.fetchall()
        cur.close()
        id = False
        for data in row:
            id = data[0]
        return id

    def channelChat(self):
        id = self.getPairId()
        if id:
            print(id)
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT pairs.pair_symbol, signals.trade_type, signals.trade_price, signals.take_profit, signals.trade_date,signals.trade_status FROM public.pairs INNER JOIN pair_signal on pair_signal.pair_id = pairs.pair_id INNER JOIN signals ON signals.signal_id = pair_signal.signal_id WHERE pair_signal.pair_id = {id};")
            row = cur.fetchall()
            cur.close()
            print(row)
            return row
        return False

    # Receive message from room group
    def chat_message(self, event):
        # message = event["message"]
        # print(self.room_name)

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": self.channelChat()}))
