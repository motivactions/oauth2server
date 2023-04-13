from mptt.models import TreeManager
from django.db import models


class ReferralManager(TreeManager):
    pass


class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
