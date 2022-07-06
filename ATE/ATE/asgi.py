"""
ASGI config for ATE project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# import chats.routing
# import chats.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ATE.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(
    #         # chats.routing.websocket_urlpatterns,
    #         # chats.routing.websocket_urlpatterns
    #     )
    # ),
})
