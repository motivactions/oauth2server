import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from djoser.views import UserViewSet as BaseUserViewset
from rest_framework import status
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
        if self.action == "refferal":
            return serializers.ReferralSerializer
        elif self.action == "refferal_codes" and self.request.method == "GET":
            return serializers.ReferralCodeSerializer
        elif self.action == "refferal_codes" and self.request.method == "POST":
            return serializers.ReferralCodeCreateSerializer
        elif self.action == "upload_avatar":
            return serializers.AvatarSerializer
        elif self.action == "upload_cover":
            return serializers.CoverSerializer
        return super().get_serializer_class()

    def _get_referrer(self, request):
        code = request.META.get("HTTP_X_REFFERAL_CODE", None)
        user = models.ReferralCode.get_user_from_code(code)
        return user

    def _get_referral(self, user, referrer=None):
        try:
            referral = models.Referral.objects.get(user=user)
        except models.Referral.DoesNotExist:
            referral = models.Referral(parent=referrer, user=user)
            referral.save()
        return referral

    @action(methods=["GET"], detail=False, url_path="referral")
    def refferal(self, request, *args, **kwargs):
        """return user refferal objects"""
        refferrer = self._get_referrer(request)
        refferal = self._get_referral(request.user, refferrer)
        serializer = self.get_serializer(instance=refferal)
        return Response(serializer.data)

    @action(methods=["GET", "POST"], detail=False, url_path="referral-codes")
    def refferal_codes(self, request, *args, **kwargs):
        refferrer = self._get_referrer(request)
        refferal = self._get_referral(request.user, refferrer)
        if request.method == "GET":
            referral_codes = refferal.referral_codes.all()
        elif request.method == "POST":
            create_serializer = self.get_serializer(data=request.data)
            create_serializer.is_valid(raise_exception=True)
            create_serializer.save(referral=refferal)
            referral_codes = refferal.referral_codes.all()
        serializer = serializers.ReferralCodeSerializer(
            instance=referral_codes, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["DELETE"],
        detail=False,
        url_path="referral-codes/(?P<referral_code>[^/.]+)",
    )
    def remove_refferal_codes(self, request, referral_code, *args, **kwargs):
        refferrer = self._get_referrer(request)
        refferal = self._get_referral(request.user, refferrer)
        referral_codes = refferal.referral_codes.filter(code=referral_code)
        referral_codes.delete()
        return Response(
            {"message": f"{referral_code} deleted!"}, status=status.HTTP_200_OK
        )

    @action(methods=["POST"], url_path="upload-avatar", detail=False)
    def upload_avatar(self, request, *args, **kwargs):
        print(request.data)
        instance = request.user
        serializer = self.get_serializer(
            instance=instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path="upload-cover", detail=False)
    def upload_cover(self, request, *args, **kwargs):
        instance = request.user
        print(request.data)
        serializer = self.get_serializer(
            instance=instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
