from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/match/(?P<room_name>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/$", consumers.PlayerConsumer.as_asgi()),
]
