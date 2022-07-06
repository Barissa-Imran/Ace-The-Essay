from importlib.resources import path
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<id>\w+)/$', consumers.PersonalChatConsumer.as_asgi())
]
