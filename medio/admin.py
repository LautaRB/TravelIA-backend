from django.contrib import admin
from .models import Medio

# Register your models here.
@admin.register(Medio)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')