from django.urls import include, path

urlpatterns = [
    path("", include("plausible_proxy.urls")),
]
