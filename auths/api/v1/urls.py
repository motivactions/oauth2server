from rest_framework.routers import DefaultRouter
from .viewsets import (
    ContentTypeViewSet,
    GroupViewSet,
    PermissionViewSet,
    UserViewSet,
    CategoryViewSet,
    TagViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet, "user")
router.register("groups", GroupViewSet, "group")
router.register("contenttypes", ContentTypeViewSet, "contenttype")
router.register("permissions", PermissionViewSet, "permission")
router.register("categories", CategoryViewSet, "category")
router.register("tags", TagViewSet, "tag")

urlpatterns = []

urlpatterns += router.urls
