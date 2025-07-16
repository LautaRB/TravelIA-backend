from django.contrib import admin
from .models import Ruta

# Register your models here.
@admin.register(Ruta)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('origen', 'destino', 'km', 'tiempo')