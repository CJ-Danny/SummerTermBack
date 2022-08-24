from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^saveDocument/(?P<docURL>\w+)/$', consumers.SaveDocument.as_asgi()),
    # re_path(r'^savePrototype/(?P<proURL>\w+)/$', consumers.SavePrototype.as_asgi()),
]
