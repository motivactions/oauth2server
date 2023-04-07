from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter
from oauth2_provider import urls as oauth_urls
from .viewsets import ContentTypeViewSet, GroupViewSet, PermissionViewSet

router = DefaultRouter()
router.register("user", UserViewSet, "user")
router.register("group", GroupViewSet, "group")
router.register("contenttype", ContentTypeViewSet, "contenttype")
router.register("permission", PermissionViewSet, "permission")

urlpatterns = []

urlpatterns += router.urls
