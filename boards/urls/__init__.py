from importlib import import_module

from allauth import app_settings
from allauth.socialaccount import providers
from django.urls import include, path
from .. import views
from . import accounts

urlpatterns = [
    # path("", views.AccountIndexView.as_view(), name="account_index"),
    path("profile/", views.AccountProfileView.as_view(), name="account_profile"),
    path("accounts/", include(accounts)),
]

if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]

# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns
