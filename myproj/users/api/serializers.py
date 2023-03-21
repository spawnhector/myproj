from django.contrib.auth import get_user_model
from rest_framework import serializers,validators
from myproj.users.models import NewUser
from myproj.schannels.models import SChannel
from myproj.subscriber.models import Subscriber
from myproj.signals.models import Signals

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["id","username", "full_name"]

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('username','full_name','email','password')

        extra_kwargs = {
            "password": {'write_only': True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        NewUser.objects.all(),'A user with that email already exists'
                    )
                ]
            }
        }

    def create(self,validated_data):
        username = validated_data.get('username')
        full_name = validated_data.get('full_name')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = NewUser.objects.create_user(email,username,full_name,password)
        return user

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class SignalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signals
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):
    subscribers = SubscriberSerializer(many=True, read_only=True)
    signals = SignalsSerializer(many=True, read_only=True)
    class Meta:
        model = SChannel
        fields = ('id','channel_name','subscribers','signals')
