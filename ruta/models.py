from django.db import models

# Create your models here.
class Ruta(models.Model):
    nombre_Ruta = models.CharField(max_length=50)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    km = models.IntegerField(default=0)
    tiempo = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre_Ruta} : {self.km} km"
