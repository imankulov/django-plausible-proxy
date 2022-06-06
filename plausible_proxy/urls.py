from django.urls import path

from plausible_proxy.services import get_script_prefix
from plausible_proxy.views import event_proxy, script_proxy

app_name = "plausible"

urlpatterns = [
    path(f"{get_script_prefix()}/<str:script_name>", script_proxy, name="script-proxy"),
    path("api/event", event_proxy, name="event-proxy"),
]
