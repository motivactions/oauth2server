def get_user_serializer():
    from djoser.serializers import UserSerializer

    return UserSerializer


def get_site_serializer(site):
    from django.contrib.sites.models import Site
    from rest_framework.serializers import ModelSerializer

    class SiteSerialier(ModelSerializer):
        class Meta:
            model = Site
            fields = "__all__"

    return SiteSerialier(instance=site).data
