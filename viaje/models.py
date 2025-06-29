from django.db import models
from django.contrib.auth import get_user_model
from .models import Ruta, Medio

User = get_user_model()

# Create your models here.
class Viaje(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viajes")
    ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True)
    medio = models.ForeignKey(Medio, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.user.username}: {self.ruta} ({self.fecha_inicio})"