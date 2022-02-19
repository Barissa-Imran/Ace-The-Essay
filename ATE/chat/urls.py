# chat/urls.py
from django.urls import path

from chat import views

urlpatterns = [
    path('', views.chatView, name='chat_home'),
    path('<str:room_name>/', views.chatRoomView, name='chat_room'),
]
