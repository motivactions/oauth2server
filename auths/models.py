import uuid
from datetime import timedelta

from django.contrib.auth.models import (  # NOQA
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models
from django.utils import timesince, timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .helpers import get_user_serializer
from .tasks import send_mail
from .validators import AlphaNumericValidator


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
        **kwargs
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
