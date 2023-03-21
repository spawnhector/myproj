from django.conf import settings
from django.core.management.base import BaseCommand
import os
class Command(BaseCommand):
    def handle(self, *args, **options):
        os.system('python trade_socket/__.py')
