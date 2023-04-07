from typing import Optional

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers


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


class UserSerializer(BaseUserSerializer):

    is_partner = serializers.SerializerMethodField(required=False)
    partner_id = serializers.SerializerMethodField(required=False)
    groups = GroupSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)

    class Meta(BaseUserSerializer.Meta):
        fields = list(BaseUserSerializer.Meta.fields) + [
            "is_partner",
            "partner_id",
            "user_permissions",
            "groups",
        ]

    def get_partner_id(self, obj) -> Optional[int]:
        partner = obj.get_partner()
        return None if not partner else partner.id

    def get_is_partner(self, obj) -> bool:
        return obj.is_partner
