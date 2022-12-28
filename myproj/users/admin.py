from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from myproj.users.models import NewUser
from django.utils.translation import gettext_lazy as _

from myproj.users.forms import UserAdminChangeForm, UserAdminCreationForm

# User = get_user_model()


admin.register(NewUser)
