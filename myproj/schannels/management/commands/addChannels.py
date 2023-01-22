from django.conf import settings
from django.core.management.base import BaseCommand
from myproj.schannels.models import SChannel

class Command(BaseCommand):
    def handle(self, *args, **options):
        if SChannel.objects.count() == 0:
            for pair in settings.PAIRLIST:
                print('Adding %s To Channel' % (pair[0],))
                app_channel = SChannel.objects.create_channel(channel_name=pair[0])
                app_channel.save()
        else:
            print('Channel can only be added if no pair exist')
