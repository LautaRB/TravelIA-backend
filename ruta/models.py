from django.db import models

# Create your models here.
class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    km = models.IntegerField(default=0)
    tiempo = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.origen} → {self.destino}"
