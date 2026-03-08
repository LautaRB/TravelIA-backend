from django.db import models
from django.contrib.auth import get_user_model
from ruta.models import Ruta
from medio.models import Medio
from alojamiento.models import Alojamiento

User = get_user_model()

# Create your models here.
class Viaje(models.Model):
    titulo = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origen = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True)
    medio = models.ForeignKey(Medio, on_delete=models.SET_NULL, null=True, blank=True)
    alojamiento = models.ForeignKey(Alojamiento, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rango_fechas = models.CharField(max_length=150, default="Sin especificar")
    cantidad_personas = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.titulo} ({self.user.username})"