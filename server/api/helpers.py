from django.core.exceptions import ImproperlyConfigured
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from server import hooks


def get_router(hook_name, router=None):
    """Registered viewsets"""
    hook_funcs = hooks.get_hooks(hook_name)
    if router is None:
        router = DefaultRouter()
    for func in hook_funcs:
        hook = func()
        router.register("%s" % hook["prefix"], hook["viewset"], hook["basename"])
    return router


def get_apiview(hook_name):
    urlpatterns = []
    hook_funcs = hooks.get_hooks(hook_name)
    for hook in hook_funcs:
        apiview = hook()
        # Validate apiview dictionary
        if not isinstance(apiview, (dict,)):
            raise TypeError("API_V1_VIEW_HOOK type must be a dict instance!")

        # Validate viewclass
        view_class = apiview.get("view_class", None)
        if view_class is None:
            raise TypeError("API_V1_VIEW_HOOK result must have a 'view_class' key!")
        if not issubclass(view_class, (APIView,)):
            raise ImproperlyConfigured("%s must subclass of DRF APIView!")

        url_path = apiview.get("url_path", None)
        if url_path is None:
            raise TypeError("API_V1_VIEW_HOOK result must have a 'url_path' key!")

        if not isinstance(url_path, (str,)):
            raise ImproperlyConfigured("%s must be a string!")

        regex_path = apiview.get("regex", False)
        path_func = re_path if regex_path else path
        path_name = apiview.get("name", False) or apiview.__class__.__name__.lower()

        urlpatterns.append(path_func(url_path, view_class.as_view(), name=path_name))

    return urlpatterns


def get_urls(hook_name):
    urlpatterns = []
    hook_funcs = hooks.get_hooks(hook_name)
    for hook in hook_funcs:
        url_path, urls_module = hook()
        urlpatterns.append(path(url_path, include(urls_module)))
    return urlpatterns
