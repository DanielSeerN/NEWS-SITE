from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/articles/(?P<slug>\w+)/$', consumers.CommentsConsumer.as_asgi()),
]