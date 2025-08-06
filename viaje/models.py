from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Viaje(models.Model):
    titulo = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viajes")
    origen_Viaje = models.CharField(max_length=100)
    destino_Viaje = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.titulo} ({self.user.username})"