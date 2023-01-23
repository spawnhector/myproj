from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from myproj.schannels.models import SChannel
class SubscriberAccountManager(models.Manager):
    def add_subscriber(self,channel_id,user_id,channel_type,**other_fields):
        if not channel_id:
            raise ValueError(_('You must specify a channel id'))

        schannels = SChannel(id=channel_id)
        subscriber = self.model(channel_id=channel_id,user_id=user_id,channel_type=channel_type **other_fields)
        subscriber.save()
        schannels.subscribers.add(subscriber.id)
        return subscriber

class Subscriber(models.Model):
    channel = models.ForeignKey('schannels.SChannel',related_name='_subscriber', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('users.NewUser',related_name='_user', on_delete=models.CASCADE, null=True)
    channel_type = models.CharField(max_length=150, unique=True)
    objects = SubscriberAccountManager()
    REQUIRED_FIELDS = ['channel_name']


