from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myproj.subscriber'
    verbose_name = _("Subscriber")
