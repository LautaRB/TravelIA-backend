from django.contrib import admin
from .models import Medio

# Register your models here.
@admin.register(Medio)
class MedioAdmin(admin.ModelAdmin):
    list_display = ('nombre_Medio', 'tipo')