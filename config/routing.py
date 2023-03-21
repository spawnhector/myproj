# config/routing.py
from django.urls import re_path
# from the_pub.chat import consumers
from config.consumer import SignalConsumer
from config.testgroupConsumer import MyConsumer
from config.channelData import ChannelDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/signals/(?P<room_name>\w+)/$', SignalConsumer.as_asgi()),
    re_path(r'ws/test_signals/(?P<room_name>\w+)/(?P<server_name>\w+)/$', MyConsumer.as_asgi()),
    re_path(r'ws/channel/all/$', ChannelDataConsumer.as_asgi())
]
