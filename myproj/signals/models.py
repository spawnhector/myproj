from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from myproj.schannels.models import SChannel
from datetime import datetime
import pytz

class SignalAccountManager(models.Manager):
    def add_signal(self,channel_id,data,**other_fields):
        if not channel_id:
            raise ValueError(_('You must specify a channel id'))
        schannels = SChannel(id=channel_id)
        # Set timezone to Jamaica
        jamaica_tz = pytz.timezone('America/Jamaica')
        current_time = datetime.now(jamaica_tz)
        signal = self.model(channel_id=channel_id,trade_ticket=data['trade_ticket'],trade_type=data['trade_type'],trade_price=data['trade_price'],take_profit=data['take_profit'],trade_date=current_time,trade_status=data['trade_status'])
        signal.save()
        schannels.signals.add(signal.id)
        return signal

class Signals(models.Model):
    channel = models.ForeignKey('schannels.SChannel',related_name='_signal', on_delete=models.CASCADE, null=True)
    trade_ticket = models.CharField(max_length=255)
    trade_type = models.CharField(max_length=255)
    trade_price = models.CharField(max_length=255)
    take_profit = models.CharField(max_length=255)
    trade_date = models.CharField(max_length=255)
    trade_status = models.CharField(max_length=255)
    objects = SignalAccountManager()
    REQUIRED_FIELDS = ['channel_name']


