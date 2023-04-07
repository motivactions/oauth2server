from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class UserAdmin(UserAdminBase):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Name"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_filter = ("is_staff", "is_superuser", "date_joined")
    list_display = ("username", "email", "is_staff", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    actions = list(UserAdminBase.actions) + ["send_welcome_message"]

    def get_inlines(self, request, obj=None):
        if not obj:
            return []
        return super().get_inlines(request, obj)

    @admin.action(description="Send welcome message")
    def send_welcome_message(self, request, queryset):
        for user in queryset:
            user.email_user(subject="Welcome message", message=f"Welcome {user}!")
