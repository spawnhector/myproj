from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SchannelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myproj.schannels'
    verbose_name = _("Schannels")
