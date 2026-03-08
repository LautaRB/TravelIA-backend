from django.contrib import admin
from .models import Viaje

# Register your models here.
@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'user', 'origen', 'destino', 'rango_fechas', 'cantidad_personas', 'precio')