from rest_framework import serializers,validators
from myproj.signals.models import Signals

class SignalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signals
        fields = '__all__'
