"""
ASGI config for channels_celery_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddleware, AuthMiddlewareStack

from django.core.asgi import get_asgi_application
from notifications_app.routing import websocket_urlpatterns
django.setup()#it is used is you run your django app as standalone,it will load your setting and pupulate django application registry



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channels_celery_project.settings')

application = ProtocolTypeRouter(#The ProtocolTypeRouter creates routes for different types of protocols used in the application
    {
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    }
)
