from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SignalsConfig(AppConfig):
    name = "myproj.signals"
    verbose_name = _("Signals")
    default_auto_field = 'django.db.models.BigAutoField'
