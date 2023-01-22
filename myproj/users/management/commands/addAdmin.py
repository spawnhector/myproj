from django.conf import settings
from django.core.management.base import BaseCommand
from myproj.users.models import NewUser

class Command(BaseCommand):

    def handle(self, *args, **options):
        if NewUser.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                full_name = user[1]
                email = user[2]
                password = '123456'
                print('Creating NewUser for %s (%s)' % (username, email))
                admin = NewUser.objects.create_superuser(email=email, username=username,full_name=full_name, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin NewUsers can only be initialized if no NewUsers exist')
