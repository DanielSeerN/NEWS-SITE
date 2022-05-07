from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'ws/articles/(?P<slug>\w+)/$', consumers.CommentsConsumer.as_asgi()),
]