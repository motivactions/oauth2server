from django.utils.translation import gettext_lazy as _
from oauth2_provider.urls import (
    management_urlpatterns,
    oidc_urlpatterns,
)

app_name = "oauth2_provider"


urlpatterns = management_urlpatterns + oidc_urlpatterns
