from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + ( #editando un usuario
        ("Rol personalizado", {"fields": ("role",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + ( # creando un usuario
        ("Rol personalizado", {"fields": ("role",)}),
    )
