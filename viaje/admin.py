from django.contrib import admin
from .models import Viaje

# Register your models here.
@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'user', 'fecha_inicio', 'fecha_fin')