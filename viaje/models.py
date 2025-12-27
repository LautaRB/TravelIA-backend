from django.db import models
from django.contrib.auth import get_user_model
from ruta.models import Ruta
from medio.models import Medio

User = get_user_model()

# Create your models here.
class Viaje(models.Model):
    titulo = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viajes")
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, related_name="viajes")
    medio = models.ForeignKey(Medio, on_delete=models.SET_NULL, null=True, blank=True, related_name="viajes")
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.titulo} ({self.user.username})"