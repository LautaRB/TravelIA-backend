from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe
from .models import User
from travelia.settings import DEFAULT_PROFILE_PICTURE

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

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return DEFAULT_PROFILE_PICTURE
    
    def profile_picture_preview(self, obj):
        url = obj.profile_picture or DEFAULT_PROFILE_PICTURE
        return mark_safe(
            f'<img src="{url}" width="50" height="50" style="object-fit:cover;border-radius:50%" />'
        )
    profile_picture_preview.short_description = "Profile Picture"