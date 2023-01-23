from django.contrib.auth import get_user_model
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from knox.auth import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view
from django.core import serializers
from myproj.schannels.models import SChannel
from myproj.subscriber.models import Subscriber
from .serializers import UserSerializer, RegisterSerializer, ChannelSerializer
from datetime import datetime
import psycopg2
import json

User = get_user_model()

class UserView(generics.CreateAPIView):
    def get(self, request, format=None):
        serializer_class = UserSerializer
        queryset = User.objects.all()
        lookup_field = "username"
        def get_queryset(self, *args, **kwargs):
            assert isinstance(self.request.user.id, int)
            return self.queryset.filter(id=self.request.user.id)

        serializer = UserSerializer(request.user, context={"request": request})
        return Response({
            'status': 200,
            'data': {
                'user': serializer.data
            }
        })

class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _,token = AuthToken.objects.create(user)
        return Response({
            'status': 200,
            'data': {
                'message': 'user created',
                'token': token
            }
        })

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class SignalsView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        conn = None
        def get_connection():
            try:
                return psycopg2.connect(
                    database="myproj",
                    user="MPYzyNUJMZCyzCVdzvItYfIBzoXODgUT",
                    password="rpc99B22yoHZJgHczZXxV5uyZDpekj0j6vVsx444xPEMUmJAXSieiGrhbSGVCino",
                    host="postgres", port="5432"
                )
            except:
                return False

        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT pairs.pair_id, pairs.pair_symbol, signals.trade_price FROM public.pairs INNER JOIN pair_signal on pair_signal.pair_id = pairs.pair_id INNER JOIN signals ON signals.signal_id = pair_signal.signal_id;")
            row = cur.fetchall()
            cur.close()
            return Response({
                'status': 200,
                'message': f"Connection to the PostgreSQL established successfully." f"The number of pairs: {cur.rowcount}",
                'data': {
                    'pairs': row,
                }
            })
        else:
            return Response({
                'status': 400,
                'data': {
                    'error': "Connection to the PostgreSQL encountered and error.",
                }
            })

class ChannelsView(generics.CreateAPIView):
    def get(self, request, format=None):
        app_channel = SChannel.objects.all()
        # serialized_obj = serializers.serialize('python', app_channel)
        # channel_data= []
        # for dat in serialized_obj:
        #     dat = list(dat.values())[1:]
        #     channel_data.append(dat)
        channels = ChannelSerializer(app_channel,many=True)
        return Response({
            'status': 200,
            'data': {
                'channels': channels.data,
            }
        })

class ChannelsSubscribeView(generics.CreateAPIView):
    def post(self, request, format=None):
        channel  = request.data['channel']
        channel_type = request.data['channel_type']
        app_channel = SChannel(id=channel)
        subscriber = Subscriber.objects.add_subscriber(channel,request.user.id,channel_type)
        app_channel.subscribers.add(subscriber.id)
        return Response({
            'status': 200,
            'data': {
                'message': 'subscriber added'
                # 'channels': channel_data,
            }
        })
