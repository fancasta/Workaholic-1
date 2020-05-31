from django.urls import path

from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    path('project/<str:pk>/chat/', consumers.ChatConsumer)
]