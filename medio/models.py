from django.db import models

# Create your models here.
from django.db import models

class Medio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre