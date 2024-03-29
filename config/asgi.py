# """
# ASGI config for myproj project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

# """
import os
import sys
from pathlib import Path
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware.TokenAuthMiddlewareStack import TokenAuthMiddlewareStack

from django.core.asgi import get_asgi_application

# # This allows easy placement of apps within the interior
# # hectperscalper directory.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "myproj"))

# # If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# # This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()
# # Apply ASGI middleware here.
# # from helloworld.asgi import HelloWorldApplication
# # application = HelloWorldApplication(application)

# # Import websocket application here, so apps from django_application are loaded first
from config.websocket import websocket_application  # noqa isort:skip
from config import routing
application = ProtocolTypeRouter({
    # "https": django_application,
    "http": django_application,
   "websocket": TokenAuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
})

# async def application(scope, receive, send):
#     if scope["type"] == "http":
#         await django_application(scope, receive, send)
#     elif scope["type"] == "websocket":
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")
