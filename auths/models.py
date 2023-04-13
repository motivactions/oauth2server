import uuid
from datetime import timedelta

from django.contrib.auth.models import (  # NOQA
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timesince, timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from coreplus.utils.slugs import unique_slugify
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey
from taggit.models import TagBase, ItemBase
from taggit.managers import TaggableManager

from .helpers import get_user_serializer
from .tasks import send_mail
from .validators import AlphaNumericValidator
from .managers import ReferralManager, TagManager

MAX_USER_REFERRAL_CODE = 3


class Category(MPTTModel):
    order = models.IntegerField(
        default=0,
        help_text=_("Ordering number"),
    )
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_(
            "Categories, unlike tags, can have a hierarchy. You might have a "
            "Jazz category, and under that have children categories for Bebop"
            " and Big Band. Totally optional."
        ),
    )
    icon = models.SlugField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_("Icon"),
    )
    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_("Category Name"),
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        editable=False,
        max_length=80,
    )
    image = ThumbnailerImageField(
        null=True,
        blank=True,
        upload_to="icon_images",
        verbose_name=_("image"),
    )
    category_id = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_("Category ID"),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        permissions = (
            ("import_category", _("Can import Category")),
            ("export_category", _("Can export Category")),
        )

    def __str__(self):
        return self.name

    @property
    def opts(self):
        return self.__class__._meta

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


class Tag(TagBase):
    icon = models.SlugField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_("Icon"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_modified_at = models.DateTimeField(default=timezone.now)

    objects = TagManager()
    icon = "tag-outline"

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    @property
    def opts(self):
        return self._meta

    @property
    def title(self):
        return self.name

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class TaggedItemBase(ItemBase):
    tag = models.ForeignKey(
        Tag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        max_length=255,
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )

    username_validator = AlphaNumericValidator()

    email = models.EmailField(_("email address"), blank=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters and digits only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    tags = TaggableManager(_("tags"), to=Tag, through="TaggedUser", blank=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def to_dict(self):
        return get_user_serializer()(instance=self).data

    def email_user(
        self,
        subject,
        message,
        from_email=None,
        template_prefix="account/emails/default_email",
        **kwargs,
    ):
        """Send an email to this user."""
        if template_prefix is None:
            template_prefix = ""
        kwargs.update(
            {
                "subject": subject,
                "message": message,
                "from_email": from_email,
                "to_email": [self.email],
                "user": self.to_dict(),
            }
        )
        send_mail.delay(template_prefix, kwargs)


class TaggedUser(TaggedItemBase):
    content_object = models.ForeignKey(
        User, related_name="user_tags", on_delete=models.CASCADE
    )


class Referral(MPTTModel, models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name="uuid",
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="downlines",
        verbose_name=_("Up Line"),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    downline_limit = 3

    objects = ReferralManager()

    class Meta:
        verbose_name = _("Referral")
        verbose_name_plural = _("Referral")
        unique_together = ("parent", "user")

    @property
    def opts(self):
        return self.__class__._meta

    def __str__(self):
        return str(self.user)

    def get_referral_limit(self):
        return getattr(settings, "REFERRAL_DOWNLINE_LIMIT", self.downline_limit)

    def get_uplines(self):
        return self.get_ancestors(include_self=False, ascending=True)[
            : self.get_referral_limit()
        ]

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError("Parent category cannot be self.")
            if parent.parent and parent.parent == self:
                raise ValidationError("Cannot have circular Parents.")

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ReferralCode(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name="uuid",
    )
    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name="referral_codes",
        verbose_name=_("referral"),
    )
    code = models.SlugField(
        validators=[MaxLengthValidator(10), MinLengthValidator(6)],
        max_length=15,
        unique=True,
        verbose_name=_("Code"),
    )

    max_num = MAX_USER_REFERRAL_CODE

    class Meta:
        verbose_name = _("Referral Code")
        verbose_name_plural = _("Referral Codes")

    def __str__(self) -> str:
        return f"{self.user} - {self.code}"

    def clean(self):
        count = self.user.referral_codes.count()
        if self._state.adding and count >= self.max_num:
            raise ValidationError({"code": _("Max referral code reached!")})
        return super().clean()

    @classmethod
    def get_user_from_code(cls, code):
        code = cls.objects.filter(code=code).first()
        return None if code is None else code.user

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Deactivation(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    executed_at = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Deactivation")
        verbose_name_plural = _("Deactivations")

    def __str__(self):
        return self.time_left

    @cached_property
    def deactivated_at(self):
        return self.started_at + timedelta(days=14)

    @cached_property
    def time_left(self):
        return timesince.timeuntil(self.deactivated_at)
