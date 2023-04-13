import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet as BaseUserViewset
from django.shortcuts import get_object_or_404
from . import serializers
from ... import models

logger = logging.getLogger(__name__)

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ["@name"]


class CategoryViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ["@name"]


class ContentTypeViewSet(ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["app_label"]
    search_fields = ["$app_label", "$model"]


class PermissionViewSet(ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class UserViewSet(BaseUserViewset):
    def get_serializer_class(self):
        if self.action == "get_referral":
            return serializers.ReferralSerializer
        return super().get_serializer_class()

    @action(methods=["GET"], detail=True, url_path="referral")
    def get_refferal(self, *args, **kwargs):
        """return user refferal objects"""
        user = self.request.user
        referral = get_object_or_404(models.Referral, user=user)
        serializer = self.get_serializer(instance=referral)
        return Response(serializer.data)
