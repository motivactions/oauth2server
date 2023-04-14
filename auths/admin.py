from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportMixin
from mptt.admin import DraggableMPTTAdmin
from .models import ReferralCode, Referral, Category, Tag
from .resources import CategoryResource


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, DraggableMPTTAdmin):
    menu_icon = "tag"
    inspect_enabled = False
    list_display = [
        "tree_actions",
        "indented_title",
        "name",
        "slug",
    ]
    search_fields = ["name", "slug"]
    list_select_related = ["parent"]
    resource_class = CategoryResource


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "description"]
    ordering = ["name", "slug"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(get_user_model())
class UserAdmin(UserAdminBase):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Name"), {"fields": ("avatar", "cover", "first_name", "last_name", "tags")}),
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


class ReferralCodeInline(admin.TabularInline):
    model = ReferralCode
    extra = 1
    max_num = ReferralCode.max_num


@admin.register(Referral)
class ReferralAdmin(DraggableMPTTAdmin):
    inlines = [ReferralCodeInline]
    list_filter = ["level"]
    list_select_related = ["user", "parent"]
    search_fields = ["user__first_name", "user__last_name"]
    list_display = [
        "tree_actions",
        "indented_title",
        "decendants",
        "downlines",
        "level",
        "created_at",
    ]

    def decendants(self, obj):
        return obj.get_descendant_count()

    def downlines(self, obj):
        return obj.downlines.count()

    def get_queryset(self, request):
        return super().get_queryset(request).only("user", "parent")
