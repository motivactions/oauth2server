from typing import Optional

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from ...models import Tag, Category, Referral, ReferralCode


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ContentTypeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ContentType
        fields = "__all__"

    def get_name(self, obj) -> str:
        return f"{obj.app_label}.{obj.model}"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class UserCreateSerializer(TaggitSerializer, BaseUserCreateSerializer):
    tags = TagListSerializerField()

    class Meta(BaseUserCreateSerializer.Meta):
        fields = list(BaseUserCreateSerializer.Meta.fields) + ["tags"]


class UserSerializer(TaggitSerializer, BaseUserSerializer):
    tags = TagListSerializerField()
    groups = GroupSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)

    class Meta(BaseUserSerializer.Meta):
        fields = list(BaseUserSerializer.Meta.fields) + [
            "tags",
            "user_permissions",
            "groups",
        ]


class ReferralCodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ["code"]


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = "__all__"


class ReferralSerializer(serializers.ModelSerializer):
    referral_codes = ReferralCodeSerializer(many=True)

    class Meta:
        model = Referral
        fields = "__all__"
