from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/parking/(?P<room_name>\w+)/$", consumers.ParkingConsumer.as_asgi()),
]