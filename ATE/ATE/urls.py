"""ATE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
# from chats.views import index, chatPage

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include('ace_the_essay.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('client.urls')),
    path('auth/', include('writer.urls')),
    path('auth/chat/', include('chat.urls')),

    # path('chat2-home', index, name='home'),
    # path('<str:username>/', chatPage, name='chat'),

    path('register/', user_views.register, name='register'),
])


if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
