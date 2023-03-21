from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class ChannelAccountManager(models.Manager):

    def create_channel(self,channel_name,**other_fields):
        if not channel_name:
            raise ValueError(_('You must specify a channel name'))

        channel = self.model(channel_name=channel_name, **other_fields)
        channel.save()
        return channel

class SChannel(models.Model):
    channel_name = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField('subscriber.Subscriber',blank=True)
    signals = models.ManyToManyField('signals.Signals',blank=True)
    objects = ChannelAccountManager()
    REQUIRED_FIELDS = ['channel_name']

