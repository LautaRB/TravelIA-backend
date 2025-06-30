from django.db import models

# Create your models here.

class Medio(models.Model):
    TYPE_CHOICES = [
        ("AUTO", "AUTO"),
        ("AVION", "AVION"),
        ("AUTOBUS", "AUTOBUS"),
        ("TREN", "TREN"),
    ]
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(choices=TYPE_CHOICES, default="Sin definir", max_length=10)

    def __str__(self):
        return f"{self.nombre} - " + self.tipo