from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (  # editando un usuario
        ("Rol personalizado", {"fields": ("role", "profile_picture", "profile_picture_preview")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (  # creando un usuario
        ("Rol personalizado", {"fields": ("role", "profile_picture")}),
    )
    
    readonly_fields = ("profile_picture_preview",)

    list_display = ("username", "email", "role", "profile_picture_preview")

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return "—"
    profile_picture_preview.short_description = "Profile Picture"