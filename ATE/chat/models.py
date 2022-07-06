from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatMessage(models.Model):
    """
    This model creates a message instance from message sent by user in the websocket consumer. Makes it easy to save and load the message
    """
    sender = models.CharField(max_length=100, default=None)
    content = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    # get recent 10 messages to be viewed in the feed
    def last_10_messages(self):
        return ChatMessage.objects.order_by("timestamp").all()[:10]
