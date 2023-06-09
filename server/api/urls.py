from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("oauth/", include("server.api.endpoints.oauth")),
    path("v1/", include("server.api.endpoints.v1")),
    path("v2/", include("server.api.endpoints.v2")),
]
