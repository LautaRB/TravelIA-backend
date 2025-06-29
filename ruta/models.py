from django.db import models

# Create your models here.
class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.origen} → {self.destino}"
