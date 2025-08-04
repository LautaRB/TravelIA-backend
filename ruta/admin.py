from django.contrib import admin
from .models import Ruta

# Register your models here.
@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre_Ruta', 'origen', 'destino', 'km', 'tiempo')