from django.urls import re_path
from . import consumers1

websocket_urlpatterns = [
    #re_path(r"ws/chart/", consumers1.ChartConsumer.as_asgi()),
    re_path(r"ws/chart/(?P<nombre_grupo>\w+)/$", consumers1.ChartConsumer.as_asgi()),
]