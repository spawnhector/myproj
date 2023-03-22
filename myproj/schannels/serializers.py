from rest_framework import serializers,validators
from myproj.schannels.models import SChannel

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SChannel
        fields = '__all__'
