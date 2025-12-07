from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Preferencias y Rol", {"fields": ("role", "currency", "distance_unit", "profile_picture", "profile_picture_preview")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Preferencias y Rol", {"fields": ("role", "currency", "distance_unit", "profile_picture")}),
    )

    readonly_fields = ("profile_picture_preview",)

    list_display = ("username", "email", "role", "currency", "distance_unit", "profile_picture_preview")

    def profile_picture_preview(self, obj):
        if obj.profile_picture_url:
            return mark_safe(
                f'<img src="{obj.profile_picture_url}" width="50" height="50" '
                f'style="object-fit:cover;border-radius:50%;" />'
            )
        return "-"
    profile_picture_preview.short_description = "Foto"